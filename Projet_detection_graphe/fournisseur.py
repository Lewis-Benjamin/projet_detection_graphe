#coding: utf-8

import etudiant
import dealer

class Fournisseur(etudiant.Etudiant):
    nombre_de_fournisseurs = 0
    def __init__(self):
        super().__init__()
        Fournisseur.nombre_de_fournisseurs += 1
        self.dealers = list()
        self.nb_dealers = 0

    def corruption(self, revendeur):
        obj = dealer.Dealer()
        try:
            revendeur.taux_d_addiction
        except AttributeError:
            try:
                revendeur.dealers
            except AttributeError:
                obj.niveau = revendeur.niveau
                obj.id = revendeur.id
                obj.sexe = revendeur.sexe
                obj.compte_banc = revendeur.compte_banc
                obj.num_tel = revendeur.num_tel
                self.nb_dealers += 1
                self.dealers.append(obj)
                etudiant.Etudiant.nombre_etudiant -= 1
                return obj  # return the new dealer
        return revendeur  # unchanged