from cryptography.fernet import Fernet, InvalidToken
import os

class GestionnaireMotsDePasse: 
    def __init__(self):
        self.cle = None
        self.fichier_mots_de_passe = None
        self.dictionnaire_mots_de_passe = {}

    def creer_cle(self, chemin):
        self.cle = Fernet.generate_key()
        with open(chemin, 'wb') as f:
            f.write(self.cle)
        print(f"Clé générée et sauvegardée dans '{chemin}'.")

    def charger_cle(self, chemin):
        try:
            with open(chemin, 'rb') as f:
                self.cle = f.read()
            print("Clé chargée avec succès.")
        except FileNotFoundError:
            print("Erreur : Le fichier de clé est introuvable.")

    def sauvegarder_fichier(self):
        if not self.cle or not self.fichier_mots_de_passe:
            return
        # On réécrit tout le fichier pour éviter les doublons
        with open(self.fichier_mots_de_passe, 'w') as f:
            for site, mot_de_passe in self.dictionnaire_mots_de_passe.items():
                chiffre = Fernet(self.cle).encrypt(mot_de_passe.encode())
                f.write(f"{site}:{chiffre.decode()}\n")

    def creer_fichier_mots_de_passe(self, chemin, valeurs_initiales=None):
        if not self.cle:
            print("Action impossible : Veuillez d'abord créer ou charger une clé.")
            return
        self.fichier_mots_de_passe = chemin
        if valeurs_initiales:
            self.dictionnaire_mots_de_passe.update(valeurs_initiales)
        self.sauvegarder_fichier()
        print(f"Fichier de mots de passe '{chemin}' initialisé.")

    def charger_fichier_mots_de_passe(self, chemin):
        if not self.cle:
            print("Action impossible : Veuillez d'abord charger une clé.")
            return
        try:
            self.fichier_mots_de_passe = chemin
            self.dictionnaire_mots_de_passe.clear()
            with open(chemin, 'r') as f:
                for ligne in f:
                    if ':' in ligne:
                        site, chiffre = ligne.strip().split(':', 1)
                        mdp_clair = Fernet(self.cle).decrypt(chiffre.encode()).decode()
                        self.dictionnaire_mots_de_passe[site] = mdp_clair
            print("Fichier chargé et déchiffré avec succès.")
        except FileNotFoundError:
            print("Erreur : Fichier de mots de passe introuvable.")
        except InvalidToken:
            print("Erreur critique : La clé fournie ne correspond pas à ce fichier.")

    def ajouter_mot_de_passe(self, site, mot_de_passe): 
        if not self.cle:
            print("Action impossible : Aucune clé chargée.")
            return
        self.dictionnaire_mots_de_passe[site] = mot_de_passe
        if self.fichier_mots_de_passe: 
            self.sauvegarder_fichier()
        print(f"Mot de passe pour '{site}' enregistré.")

    def obtenir_mot_de_passe(self, site):
        return self.dictionnaire_mots_de_passe.get(site, "Mot de passe non trouvé.")
    
    def afficher_sites_et_mots_de_passe(self):
        if not self.dictionnaire_mots_de_passe:
            print("Aucun mot de passe enregistré pour le moment.")
            return
        print("\nSites enregistrés avec leurs mots de passe :")
        for site, mot_de_passe in self.dictionnaire_mots_de_passe.items():
            print(f"- Site : {site} | Mot de passe : {mot_de_passe}")
    
def main():
    gestionnaire_mdp = GestionnaireMotsDePasse()

    menu = """
    Que souhaitez-vous faire ?
    (1) Créer une nouvelle clé
    (2) Charger une clé existante
    (3) Créer un nouveau fichier de mots de passe
    (4) Charger un fichier de mots de passe existant
    (5) Ajouter un nouveau mot de passe
    (6) Obtenir un mot de passe
    (7) Afficher tous les sites et mots de passe
    (q) Quitter
    """

    termine = False
    while not termine: 
        print(menu)
        choix = input("Saisissez votre choix : ").strip()
        
        if choix == "1":
            chemin = input("Nom du fichier pour la clé : ")
            gestionnaire_mdp.creer_cle(chemin)
        elif choix == "2":
            chemin = input("Nom du fichier de la clé : ")
            gestionnaire_mdp.charger_cle(chemin)
        elif choix == "3":
            chemin = input("Nom du nouveau fichier de mots de passe : ")
            gestionnaire_mdp.creer_fichier_mots_de_passe(chemin)
        elif choix == "4":
            chemin = input("Nom du fichier de mots de passe : ")
            gestionnaire_mdp.charger_fichier_mots_de_passe(chemin)
        elif choix == "5":
            site = input("Saisissez le site : ")
            mot_de_passe = input("Saisissez le mot de passe : ")
            gestionnaire_mdp.ajouter_mot_de_passe(site, mot_de_passe)
        elif choix == "6":
            site = input("Pour quel site souhaitez-vous un mot de passe : ")
            print(f"-> {gestionnaire_mdp.obtenir_mot_de_passe(site)}")
        elif choix == "7":
            gestionnaire_mdp.afficher_sites_et_mots_de_passe()
        elif choix.lower() == 'q':
            termine = True
            print("Fermeture du gestionnaire. Au revoir !")
        else: 
            print("Choix invalide !")

if __name__ == "__main__":
    main()