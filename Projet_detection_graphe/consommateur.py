#coding: utf-8
import random
"""
La classe 
"""
class Consommateur:
    nombre_consommateur = 0
    def __init__(self):
        super().__init__()
        self.test_cannabis = "Positif"
        self.taux_d_addiction = self.test_taux_d_addiction()

        Consommateur.nombre_consommateur += 1
        self.numero_du_consommateur = self.get_numero()

    def test_taux_d_addiction(self):
        tirage = random.randint(0, 2)
        if tirage == 0:
            taux = 1        # pour "Basse"
        elif tirage == 1:
            taux = 2        # pour "Moyenne"
        else:
            taux = 3        # pour "Haut"
        return taux
    
    def get_numero(self):
        numero = f"Consommateur_{self.nombre_consommateur}"
        return numero
