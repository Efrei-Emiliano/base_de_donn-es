def afficher_header():
    titre = "Jeu de combat"
    print("-" * 50)
    print(titre.center(50))
    print("-" * 50)


def afficher_menu():
    afficher_header()
    print("1. Démarrer une nouvelle partie")
    print("2. Afficher les 5 meilleurs scores")
    print("3. Quitter")
    choix = input("Entrez votre choix : ").strip()
    while choix not in ["1", "2", "3"]:
        print("Choix invalide, entrez 1, 2 ou 3.")
        choix = input("Entrez votre choix : ").strip()
    return choix
