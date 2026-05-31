#coding: utf-8

import creation_graph
import classification
import new_base_de_donnees

graph = creation_graph.generation_graph()
liste_sommets, graph = classification.generation_graphe_classifie(graph)
new_base_de_donnees.clear_database()
new_base_de_donnees.creation_base_de_donnees(liste_sommets, graph)
