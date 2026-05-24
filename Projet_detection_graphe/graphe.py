#coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt
import recuperation_des_donnees_neo4j as rdd
import detection_des_dealers as ddd
import matplotlib.patches as mpatches

def generation_du_graphe_sur_matplotib():
    couleurs = list()

    trouver_personne = lambda societe, id: next(
        (personne for personne in societe if personne.id == id),
        None
    )

    reseau = rdd.recup_personnes()
    relation = rdd.recup_relation(reseau)
    dealers, suspect, consommateurs = ddd.parcour_graph()

    G = nx.Graph()

    for sommet in reseau:
        G.add_node(sommet.id)

    for personneA, voisins in relation.items():
        for personneB in voisins:
            G.add_edge(personneA, personneB)

    for node in G.nodes():
        personne = trouver_personne(reseau, node)
        if node in dealers:
            couleurs.append("red")
        elif node in suspect:
            couleurs.append("yellow")
        elif node in consommateurs:
            if personne.nb_prostitution > 0:
                couleurs.append("violet")
            else:
                couleurs.append("orange")
        else:
            couleurs.append("green")

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color=couleurs,
        node_size=40,
        edge_color="white"
    )

    legend_elements = [
        mpatches.Patch(color="green", label="Etudiant"),
        mpatches.Patch(color="orange", label="Consommateurs"),
        mpatches.Patch(color="violet", label="Consommateurs prostitue"),
        mpatches.Patch(color="red", label="Dealers"),
        mpatches.Patch(color="yellow", label="Dealers possible")
    ]

    plt.legend(handles=legend_elements, loc="best")

    plt.title("Graph des communautés (sans edges pour lisibilité)")
    plt.axis("off")
    plt.show()

#generation_du_graphe_sur_matplotib()