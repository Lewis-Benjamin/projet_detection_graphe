#coding: utf-8

import recuperation_des_donnees_neo4j as rdd

def parcour_graph():
    marque = list()
    suspects = list()
    consommateurs = list()
    dealers = list()
    maybe_dealers = list()

    communaute = rdd.recup_personnes()
    relation = rdd.recup_relation(communaute)

    retourner_personne = lambda societe, id_membre: next(
        (personne for personne in societe if personne.id == id_membre),
        None
    )

    # parcours en largeur de la graph
    for id, voisins in relation.items():
        marque.append(id)
        personne = retourner_personne(communaute, id)
        if personne.taux_d_addiction > 0 and id not in consommateurs:
            consommateurs.append(id)
            for id_voisin in voisins:
                if id_voisin not in suspects:
                    suspects.append(id_voisin)

    # compter le nombre de consommateurs autour des suspects
    nb_conso_par_suspects = {}
    for id, voisins in relation.items():
        nb_conso_par_suspects[id] = sum(1 for voisin_id in voisins if voisin_id in consommateurs)

    # collecter les dealers
    for id, nb_conso in nb_conso_par_suspects.items():
        individu = retourner_personne(communaute, id)
        if nb_conso > 0 and individu.solde > 500:
            dealers.append(id)
        elif nb_conso == 1:
            est_client = any(dealer in relation[id] for dealer in dealers)
            if not est_client:
                maybe_dealers.append(id)

    # Réduire le nombre des dealers suspects
    to_remove = []

    for possible in maybe_dealers:
        # Verifie si 'possible' a un voisin qui est un vrai dealer
        connected_to_dealer = any(voisin in dealers for voisin in relation[possible])
        
        # Verifie si 'possible' est lui-meme consommateur
        is_consumer = possible in consommateurs

        # Si aucun lien avec un vrai dealer et pas lui-meme dealer -> simple ami
        if not connected_to_dealer and not is_consumer:
            to_remove.append(possible)

    for possible in to_remove:
        maybe_dealers.remove(possible)

    return dealers, maybe_dealers, consommateurs
"""
dealers, maybe_dealers, consommateurs = parcour_graph()

for i in dealers:
    print(f"{i}\n---------------")

for j in maybe_dealers:
    print(j)"""