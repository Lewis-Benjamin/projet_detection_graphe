#coding: utf-8
from etudiant import Etudiant
from consommateur import Consommateur
import random

class Etudiant_consommateur(Etudiant, Consommateur):
    def __init__(self):
        super().__init__()
        self.taux_de_prostitution = 0
        self.nb_transaction = 0
        self.transaction(self.taux_d_addiction)

    
    def transaction(self, taux_d_addiction):      #le total de depense mensuel en euro
        if taux_d_addiction == 1:
            self.nb_transaction = random.randint(1, 3)
            self.solde -= 71*self.nb_transaction
        elif taux_d_addiction == 2:
            self.nb_transaction = random.randint(5, 10)
            self.solde -= 71*self.nb_transaction
        else:
            self.nb_transaction = random.randint(20, 25)
            self.solde -= 71*self.nb_transaction

        if self.solde < 0:
            self.prostitution()

    def prostitution(self):
        while self.solde < 0:
            if self.sexe == "Masculin":
                self.solde += 90
            else:
                self.solde += 150

            self.taux_de_prostitution += 1


"""
prix de la prostitution 150 euro de l'heure pour les hommes et 250 pour les femmes:
    en faisant une estimation de 60% de ce prix pour leurs salaire on a les chiffres ci-dessus
prix du cannabis: 71 euro le gramme du THC(cannabis raffine illegal)
consommation mensuel de cannabis pur en g par taux d'addiction:
    basse: 1 ~ 3
    moyenne: 5 ~ 10 (soit 15~20 join par mois)
    haute: 20 ~ 25(certains etude montre plus de 50g/mois)
"""