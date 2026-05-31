#coding: utf-8

import random
import fournisseur
import etudiant
import creation_graph

def trouver_personne(id, communaute):
    for personne in communaute:
        if personne.id == id:
            break
    
    return personne

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
            if valid and len(clique) >= 5:
                cliques_vus.add(frozenset(clique))
    
    return cliques_vus

def classification_fournisseurs_etudiants(noeud, verification_id: list, fournisseurs: list):
    if noeud in fournisseurs:
        noeud_classifie = fournisseur.Fournisseur()
    else:
        noeud_classifie = etudiant.Etudiant()

    id_noeud = noeud_classifie.id

    # Verifier les repetitions d'ids
    while id_noeud in verification_id:
        noeud_classifie.rectification_id()
        id_noeud = noeud_classifie.id

    verification_id.append(noeud_classifie.id)

    return noeud_classifie

def generation_sommet_classifie(graph:dict):
    graphe_classifie = dict()
    fournisseurs = list()
    reseaux_fournisseurs = detection_clique(graph)
    vefirfication_id = list()
    # une liste pour garder les noeuds classifie
    noeuds_classifie = list()
    # garder l'historique de classification pour savoir quel noeud a obtenu quel classe
    historique_classification = dict()

    for sets in reseaux_fournisseurs:
        for noeud in sets:
            fournisseurs.append(noeud)

    for noeud in list(graph.keys()):
        noeud_classifie = classification_fournisseurs_etudiants(noeud, vefirfication_id, fournisseurs)
        noeuds_classifie.append(noeud_classifie)
        vefirfication_id.append(noeud_classifie.id)
        historique_classification[noeud] = noeud_classifie.id

    return noeuds_classifie, historique_classification

def generation_graphe_classifie(graphe: dict):
    graphe_classifie = dict()
    liste_noeuds_clasifie, historique = generation_sommet_classifie(graphe)

    for noeud, voisins in graphe.items():
        voisins_classifies = set()
        for voisin in voisins:
            voisins_classifies.add(historique[voisin])
        graphe_classifie[historique[noeud]] = voisins_classifies

    classification_dealers(graphe_classifie, liste_noeuds_clasifie)
    classifiction_consommateurs(graphe_classifie, liste_noeuds_clasifie)
    #confirmer_payment_fournisseurs(liste_noeuds_clasifie)
    
    return liste_noeuds_clasifie, graphe_classifie

def classification_dealers(graphe: dict, liste_sommets: list):
    for noeud in graphe.keys():
        personne = trouver_personne(noeud, liste_sommets)
        try:
            personne.dealers
        except AttributeError:
            pass
        else:
            for place in range(len(liste_sommets)):
                if liste_sommets[place].id in graphe[noeud]:
                    liste_sommets[place] = personne.corruption(liste_sommets[place])


def classifiction_consommateurs(graphe: dict, liste_sommets: list):
    for noeud in graphe.keys():
        personne = trouver_personne(noeud, liste_sommets)
        try:
            personne.clients
        except AttributeError:
            pass
        else:
            for place in range(len(liste_sommets)):
                if liste_sommets[place].id in graphe[noeud]:
                    liste_sommets[place] = personne.transaction(liste_sommets[place])

def confirmer_payment_fournisseurs(liste_sommets: list):
    for sommet in liste_sommets:
        try:
            sommet.dealers
        except AttributeError:
            pass
        else:
            if sommet.dealers:
                for Dealer in sommet.dealers:
                    produit_vendu = Dealer.nb_transaction
                    sommet.solde += (71*0.8*produit_vendu)
                    Dealer.solde -= (71*0.8*produit_vendu)
