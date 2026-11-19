#Déroulement du jeu : vagues, combat, parties et scores

import random
from time import sleep
from datetime import datetime
from pymongo.errors import PyMongoError
from db_init import db
from models import creer_equipe

HAUSSE_DIFFICULTE = 0.1
NB_SCORES_AFFICHES = 5
PAUSE_COURTE = 1
PAUSE_LONGUE = 2


def jouer(personnages, ennemis):
    #conserve le pseudo si plusieurs parties
    pseudo = demander_pseudo()
    rejouer = True
    while rejouer:
        #Nouvelle équipe à chaque partie
        equipe = creer_equipe(personnages)
        vague = jouer_vagues(equipe, ennemis)
        afficher_defaite(vague)
        sauvegarder_score(pseudo, vague)
        sleep(PAUSE_COURTE)
        rejouer = demander_rejouer()


#Enchaîne les vagues tant que l'équipe gagne
def jouer_vagues(equipe, ennemis):
    vague = 0
    resultat = "victoire"
    while resultat == "victoire":
        vague = vague + 1
        ennemi_choisi = lancer_vague(vague, ennemis)
        resultat = combat(equipe, ennemi_choisi)
    #La vague renvoyée est celle où l'équipe a perdu (= le score)
    return vague


#Lance la vague vaguen : choisit un ennemi au hasard et affiche ses stats
def lancer_vague(vaguen, ennemis):
    afficher_titre_vague(vaguen)
    #Tire un ennemi au hasard parmi la liste
    nom, stats_modele = random.choice(list(ennemis.items()))
    #Applique le bonus de difficulté
    stats = renforcer_ennemi(stats_modele, vaguen)
    print(f"Un {nom} apparaît ! (ATK : {stats['ATK']}, DEF : {stats['DEF']}, PV : {stats['PV']})")
    sleep(PAUSE_LONGUE)
    return (nom, stats)


#Affiche le bandeau de début de la vague numéro vaguen
def afficher_titre_vague(vaguen):
    print("-" * 50)
    print("Début de la vague n°", vaguen)
    print("-" * 50)
    sleep(PAUSE_LONGUE)


#Renvoie une copie des stats de l'ennemi (PV et ATK)
def renforcer_ennemi(stats_modele, vaguen):
    stats = dict(stats_modele)  # copie des stats de base

    facteur = 1 + HAUSSE_DIFFICULTE * (vaguen - 1) #+10 % de PV et d'ATK de l'ennemi à chaque vague
    #Seuls l'ATK et les PV augmentent
    stats["ATK"] = round(stats["ATK"] * facteur)
    stats["PV"] = round(stats["PV"] * facteur)
    return stats


#Fait combattre l'équipe contre l'ennemi
#Renvoie "victoire" si l'ennemi est vaincu, "défaite" si toute l'équipe est morte
def combat(equipe, ennemi_choisi):
    #Récupère le nom et les stats de l'ennemi de la vague
    nom_ennemi, stats_ennemi = ennemi_choisi
    while True:
        #L'équipe attaque
        if attaque_equipe(equipe, nom_ennemi, stats_ennemi):
            return "victoire"
        #l'ennemi attaque
        attaque_ennemi(equipe, nom_ennemi, stats_ennemi)
        if len(equipe) == 0:
            return "défaite"


#Tour de l'équipe
#Dégâts = ATK du personnage - DEF de l'ennemi
def attaque_equipe(equipe, nom_ennemi, stats_ennemi):
    #Chaque membre encore en vie attaque à tour de rôle
    for nom, stats in equipe.items():
        degats = calculer_degats(stats["ATK"], stats_ennemi["DEF"])
        #empêche les PV de devenir négatifs
        stats_ennemi["PV"] = max(0, stats_ennemi["PV"] - degats)
        print(f"{nom} attaque le {nom_ennemi} : {degats} points de dégâts !")
        print(f"Vie restante du {nom_ennemi} : {stats_ennemi['PV']}")
        sleep(PAUSE_COURTE)
        #Si l'ennemi tombe à 0 PV, les personnages suivants n'attaquent pas
        if stats_ennemi["PV"] <= 0:
            print(f"Le {nom_ennemi} a été vaincu !")
            sleep(PAUSE_LONGUE)
            return True
    return False


#Tour de l'ennemi
#Dégâts = ATK de l'ennemi - DEF du personnage
def attaque_ennemi(equipe, nom_ennemi, stats_ennemi):
    #Choisit au hasard la cible parmi les personnages encore en vie
    nom_cible = random.choice(list(equipe.keys()))
    stats_cible = equipe[nom_cible]
    print(f"Le {nom_ennemi} contre-attaque et attaque {nom_cible} !")
    sleep(PAUSE_COURTE)
    degats = calculer_degats(stats_ennemi["ATK"], stats_cible["DEF"])
    stats_cible["PV"] = max(0, stats_cible["PV"] - degats)
    print(f"Le {nom_ennemi} inflige {degats} points de dégâts à {nom_cible} !")
    print(f"Vie restante de {nom_cible} : {stats_cible['PV']}")
    sleep(PAUSE_COURTE)
    #Un personnage à 0 PV est retiré de l'équipe
    if stats_cible["PV"] <= 0:
        print(f"{nom_cible} a été vaincu !")
        del equipe[nom_cible]
        sleep(PAUSE_LONGUE)


#Calcul des dégâts d'une attaque : ATK - DEF, avec un minimum de 1
def calculer_degats(atk, defense):
    degats = atk - defense
    if degats < 1:
        degats = 1
    return degats


#Demande le pseudo du joueur.
def demander_pseudo():
    pseudo = ""
    # Redemande tant que la saisie est vide
    while pseudo == "":
        pseudo = input("Entrez votre pseudo : ")
    return pseudo


#Affiche le message de fin de partie avec la vague atteinte.
def afficher_defaite(vague):
    print("-" * 50)
    print(f"Défaite ! Votre équipe a atteint la vague {vague}.")
    print("-" * 50)
    sleep(PAUSE_LONGUE)


def sauvegarder_score(pseudo, vague):
    try:
        #Insère le score
        db.scores.insert_one({"pseudo": pseudo, "vague": vague})
        print("Score sauvegardé !")
    except PyMongoError:
        print("Impossible de sauvegarder le score.")


#Demande au joueur s'il veut rejouer
def demander_rejouer():
    reponse = input("Voulez-vous rejouer ? (o/n) : ").lower()
    while reponse not in ["o", "n"]:
        print("Répondez par o (oui) ou n (non).")
        reponse = input("Voulez-vous rejouer ? (o/n) : ").lower()
    #True si le joueur a répondu "o", False sinon
    return reponse == "o"


#Lit la collection "personnages"
def personnage():
    personnages = {}
    for db_personnage in db.personnages.find():
        personnages[db_personnage["Personnage"]] = {
            "ATK": db_personnage["ATK"],
            "DEF": db_personnage["DEF"],
            "PV": db_personnage["PV"]
        }
    return personnages


#Affiche les 5 meilleurs scores
def afficher_meilleurs_scores():
    try:
        scores = list(db.scores.find().sort("vague", -1).limit(NB_SCORES_AFFICHES))
    except PyMongoError:
        print("Base de données inaccessible.")
        return
    if len(scores) == 0:
        print("Aucun score enregistré.")
        return
    print(f"\nLes {NB_SCORES_AFFICHES} meilleurs scores :")
    #numérote le classement
    for numero, score in enumerate(scores, start=1):
        print(f"{numero}. {score['pseudo']} - vague {score['vague']}")
    sleep(PAUSE_LONGUE)