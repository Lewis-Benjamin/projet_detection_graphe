#coding: utf-8

import random

def generation_sommets(taille_graph):
    liste_sommet =list()
    for sommet in range(taille_graph):
        liste_sommet.append(sommet)
        
    return liste_sommet

def generation_graph():
    taille = int(input("Entrez la taille graphe: "))
    liste_sommet = generation_sommets(taille)
    graph = dict()
    probat = 0.002

    for personne in liste_sommet:
        voisins = set()

        # generation arete oriente
        for iteration in range(len(liste_sommet)):
            voisin = random.choice(liste_sommet)
            pourcent_lien = random.randint(0, 1000) / 1000

            # Empecher les boucles
            if voisin == personne or pourcent_lien > probat:
                continue

            voisins.add(voisin)
            
        graph[personne] = voisins
    
    graph = est_connexe(graph, liste_sommet)
    graph = est_non_oriente(graph)
    
    return graph

def est_non_oriente(graph: dict):
    for personne_id, voisins_id in graph.items():
        for voisin_id in voisins_id.copy():
            if personne_id not in graph[voisin_id]:
                graph[voisin_id].add(personne_id)

    return graph

def est_connexe(graph: dict, sommets: list):
    probat_lien = 0.002
    for noeud in sommets:
        if not graph[noeud]:
            for iteration in range(len(sommets)):
                voisin = random.choice(sommets)
                probat = random.randint(0, 1000) / 1000
                if voisin != noeud and probat <= probat_lien:
                    graph[noeud].add(voisin)

    for noeud in sommets:
        if not graph[noeud]:
            graph = est_connexe(graph, sommets)

    return graph
