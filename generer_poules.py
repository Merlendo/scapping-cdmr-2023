# -*- coding: utf-8 -*-
"""
Génère les fichiers poule.html
"""
from utilitaires import path, remplacer_html
import pandas as pd


def generer_poule(lettre_poule: str):
    """
    Génère le fichier poule selon la lettre (A, B, C, D)

    Parameters
    ----------
    lettre_poule : str

    """

    # Récupère les données
    path_data_poule = path("data", f"informations_poule_{lettre_poule}.csv")
    data_poule = pd.read_csv(path_data_poule, sep=";")

    path_data_matchs = path("data", "informations_matchs.csv")
    data_matchs = pd.read_csv(path_data_matchs, sep=";")
    data_matchs = data_matchs[data_matchs["Phase"] == f"Pool {lettre_poule}"]
    data_matchs = data_matchs.astype(str)

    # Génère la liste des matchs de poules
    liste_matchs = ""
    for _, row in data_matchs.iterrows():
        valeurs_remplacer = dict(row)
        nouveau_match = remplacer_html(
            "match_template.html", valeurs_remplacer)
        liste_matchs += nouveau_match

    # Convertie le tableau en html
    table = data_poule.to_html(classes=f"poule_{lettre_poule}", index=False)

    # Génère la page de poule
    valeurs_remplacer = {
        "lettre_poule": lettre_poule,
        "table": table,
        "liste_matchs": liste_matchs
    }
    page_poule = remplacer_html(
        "phase_de_poule_template.html", valeurs_remplacer)

    # Créer la page de poule
    path_file = path("contenus", f"poule_{lettre_poule}.html")
    with open(path_file, "w", encoding="utf-8") as f:
        f.write(page_poule)


def main():
    """
    Génère les quatres fichier poules
    """
    for lettre_poule in ["A", "B", "C", "D"]:
        generer_poule(lettre_poule)
        print(f"Fichier poule_{lettre_poule}.html généré")


if __name__ == "__main__":
    main()
