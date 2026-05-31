#coding: utf-8
from consommateur import Consommateur
from etudiant import Etudiant
from etudiant_consommateur import Etudiant_consommateur as ec
import random

class Dealer(Consommateur, Etudiant):
    nb_dealer = 0
    def __init__(self):
        super().__init__()
        self.clients = list()
        self.nb_transaction = 0
        self.nb_client = 0
        self.nb_consomme = self.consommation()

        #Augmenter le nombre de dealer
        Dealer.nb_dealer += 1
        #Etudiant.nombre_etudiant -= 1
        self.dealer_id = Dealer.nb_dealer
    
    def transaction(self, etu: Etudiant):
        obj = ec()
        try:
            etu.taux_d_addiction
        except AttributeError:
            try:
                etu.dealers
            except AttributeError:
                obj.niveau = etu.niveau
                obj.id = etu.id
                obj.sexe = etu.sexe
                obj.compte_banc = etu.compte_banc
                obj.num_tel = etu.num_tel
                self.nb_transaction += obj.nb_transaction
                self.solde += obj.nb_transaction * 71
                self.nb_client += 1
                self.clients.append(obj)
                Etudiant.nombre_etudiant -= 1
                return obj  
        return etu 
        
    def consommation(self):      #le total de depense mensuel en euro
        self.taux_d_addiction = random.randint(0, 3)
        if self.taux_d_addiction == 1:
            self.nb_consomme = random.randint(1, 3)
            self.solde -= 71*self.nb_consomme
        elif self.taux_d_addiction == 2:
            self.nb_consomme = random.randint(5, 10)
            self.solde -= 71*self.nb_consomme
        elif self.taux_d_addiction == 3:
            self.nb_consomme = random.randint(20, 25)
            self.solde -= 71*self.nb_consomme
