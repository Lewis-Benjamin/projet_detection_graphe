#coding: utf-8

from neo4j import GraphDatabase
import etudiant
import classification

#Authentification dans le neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

def creation_sommet(student):
    query = """
    CREATE(p:Person {
        id: $id,
        niveau: $niveau,
        sexe: $sexe,
        num_tel: $num_tel
    })
    """

    if student.sexe == 0:
        sexe = "Masculin"
    else:
        sexe = "Feminin"

    with driver.session() as session:
        session.run(query,
                    id=student.id,
                    niveau=student.niveau,
                    sexe=sexe,
                    num_tel=student.num_tel
                    )
        
def creation_lien_amitier(personneA, personneB):
    query="""
        MATCH (a: Person {id: $id1})
        MATCH (b: Person {id: $id2})
        WHERE a <> b
        MERGE (a)-[:AMI_DE]->(b)
    """

    with driver.session() as session:
        session.run(query,
                    id1=personneA,
                    id2=personneB
                    )
        
def creation_lien_client(personneA, personneB):
    query="""
        MATCH (a: Person {id: $id1})
        MATCH (b: Person {id: $id2})
        WHERE a <> b
        MERGE (b)-[:CLIENT_DE]->(a)
    """

    with driver.session() as session:
        session.run(query,
                    id1=personneA,
                    id2=personneB
                    )

def creation_lien_dealer(personneA, personneB):
    query="""
        MATCH (a: Person {id: $id1})
        MATCH (b: Person {id: $id2})
        WHERE a <> b
        MERGE (a)-[:FOURNISSEUR_DE]->(b)
    """

    with driver.session() as session:
        session.run(query,
                    id1=personneA,
                    id2=personneB
                    )
        
def creation_lien_fournisseur(personneA, personneB):
    query="""
        MATCH (a: Person {id: $id1})
        MATCH (b: Person {id: $id2})
        WHERE a <> b
        MERGE (a)-[:FOURNISSEUR_CONNECTE_A]->(b)
    """

    with driver.session() as session:
        session.run(query,
                    id1=personneA,
                    id2=personneB
                    )

def creation_base_de_donnees(graphe: dict):
    verification_id = list()
    historique_de_convertion = dict()

    for noeud in list(graphe.keys()):
        new_personne = etudiant.Etudiant()
        while new_personne.id in verification_id:
            new_personne.rectification_id()
        verification_id.append(new_personne.id)
        historique_de_convertion[noeud] = new_personne.id
        creation_sommet(new_personne)

    return historique_de_convertion

def creation_liens(graphe: dict, history: dict):
    fournisseurs = classification.classification_fournisseurs(graphe)
    dealers = classification.classification_dealers(graphe, fournisseurs)
    consommateurs = classification.classification_consommateurs(graphe, fournisseurs, dealers)
    etudiants = classification.classification_etudiant(graphe, fournisseurs, dealers, consommateurs)

    for sommet, voisins in graphe.items():
        personneA = history[sommet]
        for voisin in voisins:
            personneB = history[voisin]
            creation_lien_amitier(personneA, personneB)
            if sommet in fournisseurs and voisin in fournisseurs:
                creation_lien_fournisseur(personneA, personneB)
            elif sommet in fournisseurs and voisin in dealers:
                creation_lien_dealer(personneA, personneB)
            elif sommet in dealers and voisin in consommateurs:
                creation_lien_client(personneA, personneB)


def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
