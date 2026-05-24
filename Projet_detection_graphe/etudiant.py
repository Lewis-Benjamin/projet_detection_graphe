#coding: utf-8

import random
"""
Creation de la classe etudiant
"""
class Etudiant:
    nombre_etudiant = 0                                          #le nombre d'instance de la classe etudiant
    def __init__(self):
        super().__init__()
        self.niveau = self.definir_niveau()
        self.id = self.creation_id() + self.niveau      #l'id de l'etudiant
        self.sexe = random.randint(0, 1)                 #Initialisation du sexe 0 pour masculin et 1 pour feminin
        self.compte_banc = self.definir_compte_banc()
        self.solde = random.randint(400, 500)
        self.num_tel = self.definir_contact()
        Etudiant.nombre_etudiant += 1                            #incrementer le nombre de l'etudiant a chaque creation

    def definir_niveau(self):
        tirage = random.randint(0, 4)
        if tirage == 0:
            niveau = "L1"
        elif tirage == 1:
            niveau = "L2"
        elif tirage == 2:
            niveau = "L3"
        elif tirage == 3:
            niveau = "M1"
        else:
            niveau = "M2"
        return niveau

    def creation_id(self):
        c_id = "AU"
        for i in range(5):
            c_id += f"{random.randint(0, 9)}"
        if random.randint(0, 1) == 0:
            c_id += "FS"
        else:
            c_id += "FL"
        c_id += "2026"
        return c_id
        
    def definir_compte_banc(self):
        numero = str()
        for i in range(4):
            for j in range(4):
                numero += f"{random.randint(0, 9)}"
            if i != 3:
                numero += "-"
        return numero
    
    def definir_contact(self):
        tirage = random.randint(0, 3)
        if tirage == 0:
            contact = "032 "
        elif tirage == 1:
            contact = "033 "
        elif tirage == 2:
            contact = "034 "
        else:
            contact = "038 "

        for i in range(3):
            if i == 1:
                n = 3
            else:
                n = 2
            for j in range(n):
                contact += f"{random.randint(0, 9)}"
            contact += " "
        return contact
    
    def afficher_etudiant(self):
        print(f"ID: {self.id}\nSexe: {self.sexe}\nCompte bancaire: {self.compte_banc}")
        print(f"numero de telephone: {self.num_tel}")

    def affichier_compte(self):
        print(f"Compte: {self.compte_banc}\nSolde: {self.solde}")