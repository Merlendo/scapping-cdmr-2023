# -*- coding: utf-8 -*-
"""
Récupère les informations sur les poules
"""

# Importation des modules nécessaires
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import os
from io import StringIO


def main():
    """
    Fonction principale

    """
    # Définition de l'URL de la page Wikipedia pour la Coupe du Monde de Rugby 2023
    url = "https://fr.wikipedia.org/wiki/Coupe_du_monde_de_rugby_%C3%A0_XV_2023"

    # Ouverture de l'URL et récupération du HTML
    html = urllib.request.urlopen(url, timeout=5)

    # Utilisation de BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html, "html.parser")

    # Recherche des noms des poules dans le HTML
    nom_poules = soup.find_all("span", {"id": re.compile(r"Poule_(A|B|C|D)")})

    # Création d'un dictionnaire pour stocker les tableaux de chaque poule
    tableaux_poules = {poule.text: poule.findNext(
        "table") for poule in nom_poules}

    # Lecture des tableaux de chaque poule avec pandas
    df_poule_A = pd.read_html(
        StringIO(str(tableaux_poules["Poule A"])))[0]
    df_poule_B = pd.read_html(
        StringIO(str(tableaux_poules["Poule B"])))[0]
    df_poule_C = pd.read_html(
        StringIO(str(tableaux_poules["Poule C"])))[0]
    df_poule_D = pd.read_html(
        StringIO(str(tableaux_poules["Poule D"])))[0]

    # Ecritures des données en csv
    df_poule_A.to_csv(os.path.join("data", "informations_poule_A.csv"),
                      sep=";",
                      index=False)
    print("Fichier informations_poule_A.csv généré")
    df_poule_B.to_csv(os.path.join("data", "informations_poule_B.csv"),
                      sep=";",
                      index=False)
    print("Fichier informations_poule_B.csv généré")
    df_poule_C.to_csv(os.path.join("data", "informations_poule_C.csv"),
                      sep=";",
                      index=False)
    print("Fichier informations_poule_C.csv généré")
    df_poule_D.to_csv(os.path.join("data", "informations_poule_D.csv"),
                      sep=";",
                      index=False)
    print("Fichier informations_poule_D.csv généré")


if __name__ == "__main__":
    main()
