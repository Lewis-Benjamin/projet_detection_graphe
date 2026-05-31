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

    for personne in liste_sommet:
        voisins = set()
        probat = 0.05

        # generation arete oriente
        for iteration in range(len(liste_sommet)):
            voisin = random.choice(liste_sommet)
            pourcent_lien = random.randint(0, 100) / 100

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
    probat_lien = 0.05
    for noeud in sommets:
        if not graph[noeud]:
            for iteration in range(len(sommets)):
                voisin = random.choice(sommets)
                probat = random.randint(0, 100) / 100
                if voisin != noeud and probat <= probat_lien:
                    graph[noeud].add(voisin)

    for noeud in sommets:
        if not graph[noeud]:
            graph = est_connexe(graph, sommets)

    return graph

def parcours_largeur(graph:dict, depart):
    marque = list()
    pile = list()

    marque.append(depart)
    pile.append(depart)

    while pile:
        depart = pile.pop(0)
        for voisin in graph[depart]:
            if voisin not in marque:
                marque.append(voisin)
                pile.append(voisin)

    return marque

def detection_clique(graph: dict, sommets: list):
    cliques_vus = set()
    chemin = parcours_largeur(graph, random.choice(sommets))
    for sommet in chemin:
        for voisin in graph[sommet]:
            # Commence avec les voisins en communs entre sommet et voisin
            candidats = set(graph[sommet]) & set(graph[voisin])
            clique = {sommet, voisin}
            for candidat in candidats:
                # Verifie si candidat est connecte a tout les noeuds qui sont deja dans clique
                if all(candidat in graph[membre] for membre in clique):
                    clique.add(candidat)
            # Valide tout les paires
            valid = True
            nodes = list(clique)
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    if nodes[j] not in graph[nodes[i]]:
                        valid = False
                        break
                if not valid:
                    break
            if valid and len(clique) >= 5:
                cliques_vus.add(frozenset(clique))
    return cliques_vus
