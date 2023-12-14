# -*- coding: utf-8 -*-
"""
Génère les pages stats_joueur.html
"""

import os
import pandas as pd
from utilitaires import remplacer_html, path, nom_pays


def generer_stats(pays: str):
    """
    Génère le fichier stats_joueur selon le pays

    Parameters
    ----------
    pays : str

    """
    # Récupère les données du pays
    path_data = path("data", "informations_joueurs", pays, pays + ".csv")
    data = pd.read_csv(
        os.path.join(path_data),
        sep=";", encoding="utf-8")

    # Convertie les succès de tacle en pourcentage
    data["TackleSuccess"] = data["TackleSuccess"] * 100

    # Convertir les colonnes float en entiers
    float_columns = data.select_dtypes(include='float').columns
    data[float_columns] = data[float_columns].fillna(0).astype(int)

    # Convertie les données
    data = data.fillna('-')
    data = data.astype(str)

    # Créer le dossier des stats joueurs
    path_dossier = path("contenus", "stats_joueurs", pays)
    if not os.path.exists(path_dossier):
        os.makedirs(path_dossier)

    # Parcours la liste des joueurs
    for _, row in data.iterrows():
        valeurs_remplacer = dict(row)
        valeurs_remplacer["pays"] = pays
        nouvelle_page = remplacer_html(
            "stats_joueur_template.html", valeurs_remplacer)

        # Créer la page stats du joueur
        path_joueur = path(path_dossier, row["id"] + ".html")
        with open(path_joueur, "w", encoding="utf-8") as f:
            f.write(nouvelle_page)


def main():
    """
    Créer les stats joueurs pour tout les pays
    """
    for pays in nom_pays():
        generer_stats(pays)
        print(f"Statistiques de l'équipe de {pays} générés")


if __name__ == "__main__":
    main()
