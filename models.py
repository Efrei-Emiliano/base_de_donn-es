#liste des ennemis et création de l'équipe du joueur.

from time import sleep
from db_init import db

NB_PERSONNAGES = 3  


#Lit la collection "ennemis"
def ennemi():
    ennemis = {}
    #Parcourt tous les documents de la collection "ennemis"
    for db_ennemi in db.ennemis.find():
        ennemis[db_ennemi["ennemi"]] = {
            "ATK": db_ennemi["ATK"],
            "DEF": db_ennemi["DEF"],
            "PV": db_ennemi["PV"]
        }
    return ennemis


#Convertit le numéro saisi en nom de personnage parmi les personnages disponibles
#Renvoie le nom du personnage
def trouver_nom(saisie, disponibles):
    saisie = saisie.strip()
    
    if not saisie.isdigit():
        return None
    numero = int(saisie)
    #Refuse les numéros hors de la liste
    if numero < 1 or numero > len(disponibles):
        return None
    return list(disponibles.keys())[numero - 1]


#Affiche les personnages encore disponibles
def afficher_personnages(disponibles, numero):
    print(f"\nPersonnage {numero} :")
    #Une ligne par personnage 
    for i, (nom, stats) in enumerate(disponibles.items(), start=1):
        print(f"{i}. {nom} (ATK : {stats['ATK']}, DEF : {stats['DEF']}, PV : {stats['PV']})")
        sleep(0.1)


#Demande le numéro d'un personnage jusqu'à ce qu'il soit valide, puis renvoie son nom
def demander_personnage(disponibles):
    choix = input("Entrez le numéro du personnage choisi : ")
    nom_choisi = trouver_nom(choix, disponibles)
    while nom_choisi is None:
        print(f"Choix invalide, entrez un numéro entre 1 et {len(disponibles)}.")
        choix = input("Entrez le numéro du personnage choisi : ")
        nom_choisi = trouver_nom(choix, disponibles)
    return nom_choisi


#Affiche l'équipe.
def afficher_equipe(equipe):
    print("\nVotre équipe est composée de :")
    #Affiche chaque membre avec ses stats
    for nom, stats in equipe.items():
        print(nom, ":", stats)
    sleep(0.5)


#Fait choisir 3 personnages différents au joueur et renvoie son équipe.
def creer_equipe(personnages):
    equipe = {}
    disponibles = dict(personnages) 
    #Répète le choix autant de fois qu'il y a de places dans l'équipe
    for i in range(NB_PERSONNAGES):
        afficher_personnages(disponibles, i + 1)
        nom_choisi = demander_personnage(disponibles)
        equipe[nom_choisi] = dict(disponibles[nom_choisi])
        # Retire le personnage choisi pour empêcher de le prendre deux fois
        del disponibles[nom_choisi]
    afficher_equipe(equipe)
    return equipe
