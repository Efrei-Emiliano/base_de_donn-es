

#tant que infini:
    #Afficher le menu ( 1- jouer, 2- stats, 3- quitter)
    #pour chaque option dans enumerate(options, start =1)
        #afficher {i}. option
    #Choix = demander un choix a l'utilisateur
    #Choix valide()
    #Si choix  retourner choix valide:
    #afficher message d'erreur
    
    #sinon
    #sortir de la boucle
    #ouvrir choix


#Choix valide:
    #Si choix n'est pas Isdigit():
        #Renvoyer False
    #Convertir en nombre entier
    #Si choix < min ou choix > max
        #Renvoyer false
    #Sinon
        #Renvoyer True

#Jouer:
    #Tant que infini:
        #Création d'équipe()
        #Combat()

#Création d'équipe:
    #demander un pseudo au joueur
    #Affiche liste personnages numéroté
    #tant que infini:
        #demande 1 personnages a l'utilisateur
        #Choix valide()
        #Si choix invalide:
            #afficher message d'erreur
            #redemmander
        #Si choix déja dans équipe:
            #afficher message d'erreur
            #redemmander
        #Si 3 personnages dans équipe:
            #Sortir de la boucle 
    #afficher équipe


#Combat:
    #Lancer vague()
    #Attaque Joueurs()
    #Attaque Ennemi()


#Lancer vague:
    #Afficher "début de vague n°"
    #Choisir ennemi aléatoire
    #Afficher "Un ennemi apparait"


#Attaque Joueurs:
    #réduire pv ennemi de l'atk de l'équipe (1 fois par personnage)
    #Afficher dégats
    #si pv ennemi <= 0:
        #Afficher "ennemi vaincu"
    #sinon:
        #Afficher pv ennemi


#Attaque ennemi:
    #réduire pv personnage aléatoire
    #Afficher dégats
    #Si pv personnage <= 0
        #Afficher "[nom personnage] mort"
    #placer personnage dans liste morts


#Stats
    #Ouvrir mongo DB
    #Afficher les 5 meilleurs scores
    #Afficher le menu ( 1- jouer, 2- stats, 3- quitter)


#Quitter
    #Ferme le programme
