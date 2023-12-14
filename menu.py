# -*- coding: utf-8 -*-
"""
Menu principal de l'appplication.
"""

import informations_joueurs
import informations_poules
import informations_matchs
import generer_pays
import generer_table_joueurs
import generer_stats_joueur
import generer_poules
import generer_phase_finale
import os
from utilitaires import path, open_html, clear, nom_pays, timing


@timing
def genere_donnee_contenus():

    # Récupère les données
    print("RÉCUPÉRATION DES DONNÉES")
    informations_joueurs.main()
    informations_poules.main()
    informations_matchs.main()

    # Génère le contenus
    print("\nGÉNERATION DES CONTENUS")
    generer_stats_joueur.main()
    generer_table_joueurs.main()
    generer_pays.main()
    generer_poules.main()
    generer_phase_finale.main()


menu_banniere = (
    "---------------------------------------------------\n"
    + "----SAE 3-01 Collecte automatisée de données web---\n"
    + "----Scrapping de la Coupe du monde de rugby 2023---\n"
    + "---------------------------------------------------")

menu_generation_donnees = (
    "Appuyer sur Entrée pour générer les données (~2min)")

menu_pays = "Veuillez rentrer le nom d'un pays"

menu_poule = "Veuillez rentrer la lettre d'un poule\n['A', 'B', 'C', 'D']"

menu = ("Faites votre choix dans le menu suivant :\n"
        + "(1) Afficher les pays de la coupe du monde\n"
        + "(2) Afficher les joueurs d'un pays\n"
        + "(3) Afficher les résultats de poule\n"
        + "(4) Afficher les résultats de phase finale\n"
        + "(q) Quitter.")

menu_return = "\nAppuyer sur Entrée pour retourner au menu."


# Création du dossier "data" :
if not os.path.exists("data"):
    os.mkdir("data")

clear()

# Demande à l'utilisateur de générer les données
print(menu_banniere)
print(menu_generation_donnees)
input()

genere_donnee_contenus() # Commentez cette ligne pour skip la génération de données et contenus

input(menu_return)

# Initialisation du menu :
fin_programme = False
while not fin_programme:
    clear()
    print(menu_banniere)
    print(menu)

    reponse = input().strip().lower()
    if reponse == "1":
        open_html(path("contenus", "pays.html"))
        input(menu_return)

    elif reponse == "2":
        reponse_pays = None
        while reponse_pays not in nom_pays():
            print(menu_pays)
            print(nom_pays())
            reponse_pays = input().strip().upper()
        open_html(path("contenus", "tables_joueurs",
                  f"table_joueurs_{reponse_pays}.html"))
        input(menu_return)

    elif reponse == "3":
        reponse_poule = None
        while reponse_poule not in ["A", "B", "C", "D"]:
            print(menu_poule)
            reponse_poule = input().strip().upper()
        open_html(path("contenus", f"poule_{reponse_poule}.html"))
        input(menu_return)

    elif reponse == "4":
        open_html(path("contenus", "phase_finale.html"))
        input(menu_return)

    elif reponse == "q":
        fin_programme = True

    else:
        print("Choix invalide.")
        input(menu_return)
