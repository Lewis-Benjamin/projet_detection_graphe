#coding utf-8

from neo4j import GraphDatabase
import etudiant
import dealer
import random

#Authentification dans le neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))


#Generation des membres de la communaute
def generate_communite(nb_membres: int)->list:
    nb_dealer = nb_membres * random.randint(5, 7) / 100 #nombre de dealers entre 5% et 7% de la communaute
    decompte = 0 #pour garder en compte le pourcentage de dealer et consommateur lors de la creation
    communaute = list() #la liste finale des membres de la societe
    verification_id = list() #pour eviter la repetition des id dans la societe 
    ajout = 0 #pour marquer l'ajout de membres dans la communaute

    while ajout < nb_membres:
        tirrage = random.randint(0, 1) #0 pour les etudiants normaux et 1 pour les dealers
        if tirrage == 0:
            new_membre = etudiant.Etudiant()
            if new_membre.id not in verification_id:
                communaute.append(new_membre)
                verification_id.append(new_membre.id)
                ajout += 1
        elif tirrage == 1 and decompte < nb_dealer:
            new_membre = dealer.Dealer()
            if new_membre.id not in verification_id:
                decompte += 1
                communaute.append(new_membre)
                verification_id.append(new_membre.id)
                ajout += 1

    return communaute

#Generation des liens d'amitiers entre les differents membres de la communaute
def generate_friendship(communaute: list)-> dict:
    #dictionaire final
    amitier = dict()

    #recuperaton des id des membres de la communaute
    ids = list()
    for membres in communaute:
        ids.append(membres.id)

    #generation de l'amitier
    for personne in ids:
        #ensemble pour le dictionaire
        relation = set()

        #nombre d'essai pour la generation des relations d'amitier
        essai = 0

        #nombre d'amis entre 1 et 5
        nb_amis = random.randint(1, 5)

        while len(relation) < nb_amis and essai < 100:
            ami = random.choice(ids)

            if ami == personne:
                essai += 1
                continue

            relation.add(ami)

            if amitier:
                for ident, friend in amitier.items():
                    for temp in friend.copy():
                        if temp == ident:
                            friend.remove(temp)

        amitier[personne] = relation
    
    return amitier

def simulation_transaction(communaute: list, relations: dict)->list:
    #fonction anonyme pour retourner des membres de la communaute a partir de leur id
    trouver_etudiant = lambda membres, id: next(
        (membre for membre in membres if membre.id == id),
        None
    )

    #simulation de la transaction entre dealer et etudiant et les dealers vont choisir leurs amiis pour cibles
    for vendeur in communaute:
        try:
            vendeur.clients
        except AttributeError:
            pass
        else:
            for client_id in relations[vendeur.id]:
                client = trouver_etudiant(communaute, client_id)
                # Pour etre sur que les consommateur n'ont qu'un seul dealer et pas plusieurs
                try:
                    client.taux_de_prostitution
                except AttributeError:
                    for place in range(len(communaute)):
                        if client == communaute[place]:
                            communaute[place] = vendeur.transaction(client)
                else:
                    pass

    return communaute

def creaton_sommet(student):
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
        MERGE (b)-[:AMI_DE]->(a)
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

def creation_base_de_donnees(societe: list, relations: dict):
    trouver_etudiant = lambda communaute, id: next(
        (student for student in communaute if student.id == id),
        None
    )

    for membre in societe:
        creaton_sommet(membre)
    
    for membre_a_id, amis_id in relations.items():
        for membre_b_id in amis_id:
            creation_lien_amitier(membre_a_id, membre_b_id)
            
            try:
                student = trouver_etudiant(societe, membre_a_id)
                student.clients
            except AttributeError:
                pass
            else:
                for client in student.clients:
                    creation_lien_client(student.id, client.id)

def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
