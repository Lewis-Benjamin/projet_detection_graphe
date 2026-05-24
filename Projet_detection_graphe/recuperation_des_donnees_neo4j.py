#coding: utf-8
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

class Personne():
    nb_personne = 0

    def __init__(self, id, nv, sexe, compte_b, solde, num_tel, tx_addict, nb_pr):
        self.id = id
        self.niveau = nv
        self.sexe = sexe
        self.compte_banc = compte_b
        self.solde = solde
        self.num_tel = num_tel
        self.taux_d_addiction = tx_addict
        self.nb_prostitution = nb_pr
        Personne.nb_personne += 1

def recup_personnes():
    query = "MATCH (p:Person) RETURN p"
    personnes = []
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            node = dict(record["p"])
            p = Personne(
                id        = node["id"],
                nv        = node["niveau"],
                sexe      = node["sexe"],
                compte_b  = node["compte_banc"],
                solde     = node["solde"],
                num_tel   = node["num_tel"],
                tx_addict = node["taux_d_addiction"],
                nb_pr     = node["nb_prostitution"]
            )
            personnes.append(p)
    return personnes

def recup_relation(communaute: list):
    query = """
    MATCH (p1:Person)-[r:AMI_DE]-(p2:Person)
    RETURN p1.id AS personne1, p2.id AS personne2
    """
    # Build a set of all IDs in communaute for quick lookup
    ids = {individu.id for individu in communaute}

    # Initialize every person with an empty set
    relations = {individu.id: set() for individu in communaute}

    with driver.session() as session:
        result = session.run(query)
        for record in result:
            p1 = record["personne1"]
            p2 = record["personne2"]
            if p1 in ids and p2 in ids:
                relations[p1].add(p2)
                relations[p2].add(p1)

    return relations