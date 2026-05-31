#coding: utf-8

from neo4j import GraphDatabase


#Authentification dans le neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

def creation_sommet(student):
    query = """
    CREATE(p:Person {
        id: $id,
        niveau: $niveau,
        sexe: $sexe,
        compte_banc: $compte_banc,
        solde: $solde,
        num_tel: $num_tel,
        taux_d_addiction: $taux_d_addiction,
        nb_prostitution: $nb_prostitution
    })
    """

    addiction = 0
    prostitution = 0
    if student.sexe == 0:
        sexe = "Masculin"
    else:
        sexe = "Feminin"

    try:
        student.taux_d_addiction
    except AttributeError:
        pass
    else:
        addiction = student.taux_d_addiction
        try:
            student.taux_de_prostitution
        except AttributeError:
            pass
        else:
            prostitution = student.taux_de_prostitution

    with driver.session() as session:
        session.run(query,
                    id=student.id,
                    niveau=student.niveau,
                    sexe=sexe,
                    compte_banc=student.compte_banc,
                    solde=student.solde,
                    num_tel=student.num_tel,
                    taux_d_addiction=addiction,
                    nb_prostitution=prostitution
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

def creation_base_de_donnees(societe: list, graphe: dict):
    trouver_personne = lambda communaute, id: next(
        (p for p in communaute if p.id == id), None
    )

    for sommet in societe:
        creation_sommet(sommet)

    for sommet, voisins in graphe.items():
        personne = trouver_personne(societe, sommet)

        for voisin in voisins:
            creation_lien_amitier(sommet, voisin)

            voisin_obj = trouver_personne(societe, voisin)

            if personne is None or voisin_obj is None:
                continue

            personne_est_dealer      = hasattr(personne, 'clients')
            personne_est_fournisseur = hasattr(personne, 'dealers')
            personne_est_client      = hasattr(personne, 'taux_de_prostitution')

            voisin_est_dealer        = hasattr(voisin_obj, 'clients')
            voisin_est_fournisseur   = hasattr(voisin_obj, 'dealers')

            if personne_est_dealer:
                if voisin_est_fournisseur:
                    # dealer(sommet) -[:FOURNISSEUR_CONNECTE_A]-> fournisseur(voisin)
                    creation_lien_fournisseur(sommet, voisin)
                elif voisin_est_dealer:
                    # fournisseur(voisin) -[:FOURNISSEUR_DE]-> dealer(sommet)
                    creation_lien_dealer(voisin, sommet)
            elif personne_est_fournisseur:
                if voisin_est_dealer:
                    # fournisseur(sommet) -[:FOURNISSEUR_DE]-> dealer(voisin)
                    creation_lien_dealer(sommet, voisin)
            elif personne_est_client:
                if voisin_est_dealer:
                    # client(sommet) -[:CLIENT_DE]-> dealer(voisin)
                    creation_lien_client(voisin, sommet)

def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
