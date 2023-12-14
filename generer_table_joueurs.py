# -*- coding: utf-8 -*-
"""
Génère les pages tables_joueur.html
"""

import os
import pandas as pd
from utilitaires import remplacer_html, path, nom_pays


def generer_table(pays: str):
    """
    Génère le fichier tables_joueur selon le pays

    Parameters
    ----------
    pays : str

    """
    # Récupère les données du pays
    path_data = path("data", "informations_joueurs", pays, pays + ".csv")
    data = pd.read_csv(path_data, sep=";", encoding="utf-8")
    # Convertie les données
    data = data.fillna('-')
    data = data.astype(str)

    # Générer les cartes joueurs
    joueurs = ""
    for index, row in data.iterrows():
        valeurs_remplacer = dict(row)
        valeurs_remplacer["pays"] = pays
        nouvelle_carte = remplacer_html(
            "card_template.html", valeurs_remplacer)
        joueurs += nouvelle_carte

    # Intègre les joueurs dans le template table_joueurs
    valeurs_remplacer = {
        "pays": pays,
        "joueurs": joueurs
    }
    table_joueur = remplacer_html(
        "table_joueurs_template.html", valeurs_remplacer)

    # Créer le dossier des tables joueurs
    path_dossier = path("contenus", "tables_joueurs")
    if not os.path.exists(path_dossier):
        os.makedirs(path_dossier)

    # Créer la page table de joueurs
    path_fichier = path(path_dossier, f"table_joueurs_{pays}.html")
    with open(path_fichier, "w", encoding="utf-8") as f:
        f.write(table_joueur)


def main():
    """
    Génère les fichiers table_joueurs pour tout les pays
    """
    for pays in nom_pays():
        generer_table(pays)
        print(f"Table des joueurs de l'équipe de {pays} générée")


if __name__ == "__main__":
    main()
