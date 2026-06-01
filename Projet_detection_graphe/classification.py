#coding: utf-8

import random

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

def detection_clique(graph: dict):
    sommets = list(graph.keys())
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
            if valid and len(clique) >= 3:
                cliques_vus.add(frozenset(clique))
    
    return cliques_vus

def classification_fournisseurs(graphe: dict):
    reseaux_fournisseur = detection_clique(graphe)
    fournisseurs = list()
    suspects = list()
    for liste in reseaux_fournisseur:
        for noeud in liste:
            if noeud not in suspects:
                suspects.append(noeud)

    fournisseurs = verfication_fournisseur(graphe, suspects)

    return fournisseurs

def verfication_fournisseur(graph: dict, suspects: list):
    fournisseurs = list()
    for noeud in suspects:
        verif = 0
        if len(graph[noeud]) > 5:
            for voisin in graph[noeud]:
                if voisin in suspects:
                    verif += 1
        if verif >= 3:
            fournisseurs.append(noeud)

    return fournisseurs

def classification_dealers(graphe: dict, fournisseurs: list):
    dealers = list()
    for noeud in fournisseurs:
        for voisin in graphe[noeud]:
            if voisin not in fournisseurs and voisin not in dealers:
                dealers.append(voisin)

    return dealers

def classification_consommateurs(graphe: dict, fourniseurs: list, dealers: list):
    consommateurs = list()
    for noeud in dealers:
        for voisin in graphe[noeud]:
            if voisin not in dealers and voisin not in fourniseurs and voisin not in consommateurs:
                consommateurs.append(voisin)

    return consommateurs

def classification_etudiant(graphe: dict, fournisseurs:list, dealers: list, consommateurs: list):
    etudiants = list()
    for noeud in list(graphe.keys()):
        if noeud not in fournisseurs and noeud not in dealers and noeud not in consommateurs and noeud not in etudiants:
            etudiants.append(noeud)

    return etudiants

def generation_communaute(graphe: dict):
    fournisseurs = classification_fournisseurs(graphe)
    dealers = classification_dealers(graphe, fournisseurs)
    consommateurs = classification_consommateurs(graphe, fournisseurs, dealers)
    etudiants = classification_etudiant(graphe, fournisseurs, dealers, consommateurs)

    communaute = [fournisseurs, dealers, consommateurs, etudiants]

    return communaute
