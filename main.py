from pymongo.errors import PyMongoError
from utils import afficher_menu
from models import ennemi, NB_PERSONNAGES
from game import personnage, jouer, afficher_meilleurs_scores


#Charge les données puis affiche le menu principal en boucle jusqu'à "Quitter".
def main():
    
    donnees = load_data()
    if donnees is None:
        return
    personnages, ennemis = donnees
    #Boucle du menu
    while True:
        choix = afficher_menu()
        if choix == "1":
            jouer(personnages, ennemis)
        elif choix == "2":
            afficher_meilleurs_scores()
        else:
            print("Au revoir !")
            break


#Charge les personnages et les ennemis depuis MongoDB
def load_data():

    try:
        personnages = personnage()
        ennemis = ennemi()
    except (PyMongoError, KeyError) as erreur:
        print("Impossible de charger les données depuis MongoDB :", erreur)
        return None
    #Vérifie qu'il y a assez de données pour jouer
    if len(personnages) < NB_PERSONNAGES or len(ennemis) == 0:
        print(f"Données insuffisantes dans MongoDB (il faut au moins {NB_PERSONNAGES} personnages et 1 ennemi).")
        return None
    return personnages, ennemis


main()
