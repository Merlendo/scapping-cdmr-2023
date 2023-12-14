# -*- coding: utf-8 -*-
"""
Génère la page phase_finale.html
"""

import pandas as pd
from utilitaires import path, remplacer_html


def generer_phase_finale():
    """
    Génère les fichier phase_finale.html

    Returns
    -------
    None.

    """

    # Récupère les données des phases finales
    path_data_matchs = path("data", "informations_matchs.csv")
    data_matchs = pd.read_csv(path_data_matchs, sep=";")
    data_matchs = data_matchs.astype(str)
    data_matchs_phase_finale = data_matchs[~data_matchs["Phase"].str.contains(
        r"Pool [A-D]")]
    data_quart = data_matchs[data_matchs["Phase"].str.contains(
        r"Quarter-final [1-4]")]
    data_demi = data_matchs[data_matchs["Phase"].str.contains(
        r"Semi-final [1-2]")]
    data_bronze = data_matchs[data_matchs["Phase"] == "Bronze Final"]
    data_finale = data_matchs[data_matchs["Phase"] == "Final"]

    # Génère la liste des matchs de la phase finale
    liste_matchs = ""
    for _, row in data_matchs_phase_finale.iterrows():
        valeurs_remplacer = dict(row)
        nouveau_match = remplacer_html(
            "match_template.html", valeurs_remplacer)
        liste_matchs += nouveau_match

    # Génère la liste des matchs des quarts de finale
    matchs_quart = ""
    for _, row in data_quart.iterrows():
        valeurs_remplacer = dict(row)
        nouveau_match = remplacer_html(
            "match_template.html", valeurs_remplacer)
        matchs_quart += nouveau_match

    # Génère la liste des matchs des demi finale
    matchs_demi = ""
    for _, row in data_demi.iterrows():
        valeurs_remplacer = dict(row)
        nouveau_match = remplacer_html(
            "match_template.html", valeurs_remplacer)
        matchs_demi += nouveau_match

    # Génère le match de la petite finale
    match_bronze = remplacer_html(
        "match_template.html", dict(data_bronze.iloc[0]))

    # Génère le match de la finale
    match_finale = remplacer_html(
        "match_template.html", dict(data_finale.iloc[0]))

    # Génère la page html finale
    valeurs_remplacer = {
        "matchs_quart": matchs_quart,
        "matchs_demi": matchs_demi,
        "match_bronze": match_bronze,
        "match_finale": match_finale,
        "liste_matchs": liste_matchs
    }
    page_phase_finale = remplacer_html(
        "phase_finale_template.html", valeurs_remplacer)

    # Ecrit la page phase_finale.html
    path_file = path("contenus", "phase_finale.html")
    with open(path_file, "w", encoding="utf-8") as f:
        f.write(page_phase_finale)


def main():
    """
    Fonction principale
    """
    generer_phase_finale()
    print(f"Fichier phase_finale.html généré")


if __name__ == "__main__":
    main()
