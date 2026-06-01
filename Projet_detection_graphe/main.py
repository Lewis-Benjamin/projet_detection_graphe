#coding: utf-8

import creation_graph
import classification
import new_base_de_donnees

base_de_donnees.clear_database()
graphe = creation_graph.generation_graph()
historique = base_de_donnees.creation_base_de_donnees(graphe)
base_de_donnees.creation_liens(graphe, historique)
