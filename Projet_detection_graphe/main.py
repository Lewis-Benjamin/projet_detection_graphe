#coding: utf-8

import base_de_donnees
import graphe
import detection_des_dealers as ddd

# Destruction de la base de donnees dans neo4j
base_de_donnees.clear_database()

# Creation base de donnees
nb_membres = input("Entrez la taille du graphe: ")
societe = base_de_donnees.generate_communite(nb_membres)
relations = base_de_donnees.generate_friendship(societe)
societe = base_de_donnees.simulation_transaction(societe, relations)
base_de_donnees.creation_base_de_donnees(societe, relations)

# Detection des dealers, consommateurs et des suspects
dealers, maybe_dealers, consommateurs = ddd.parcour_graph()

# Affichage sous networkx et matplotlib.pyplot
graphe.generation_du_graphe_sur_matplotib()
