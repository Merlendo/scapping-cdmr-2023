# -*- coding: utf-8 -*-
"""
Génére un fichier csv qui contient les informations des matchs
"""

import urllib.request
import json
import pandas as pd
from utilitaires import path


def main():
    """
    Fonction principale

    """
    # Url du de l'API privé
    url = "https://api.wr-rims-prod.pulselive.com/rugby/v3/event/1893/schedule"

    page = urllib.request.urlopen(url)

    # Récupération du json contenant les information sur les matchs
    matchs = json.loads(page.read().decode())["matches"]

    # Récupère les informations des matchs
    matchs_list = []
    for match in matchs:
        info_match = {}
        info_match["Stade"] = match['venue']['name']
        info_match["Ville"] = match['venue']['city']
        info_match["Date"] = match['time']['label']
        info_match["Equipe A"] = match["teams"][0]["abbreviation"]
        info_match["Score A"] = match['scores'][0]
        info_match["Score B"] = match['scores'][1]
        info_match["Equipe B"] = match["teams"][1]["abbreviation"]
        info_match["Phase"] = match["eventPhase"]
        info_match["Affluence"] = match["attendance"]
        matchs_list.append(info_match)

    df = pd.DataFrame(matchs_list)

    # Remplacement des NA de la colonne Affluence par 0
    df["Affluence"] = df["Affluence"].fillna(0)

    # conversion de la colonne Affluence en int
    df["Affluence"] = df["Affluence"].astype(int)

    # Convertir la colonne 'Date' au format datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Tri du data frame par date
    df = df.sort_values(by="Date", ascending=True)

    # Formater les dates dans le nouveau format "jj/mm/aaaa"
    df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

    # Export du data frame en csv
    path_csv = path("data", "informations_matchs.csv")
    df.to_csv(path_csv,
              sep=";",
              index=False,
              encoding="utf-8")
    print("Fichier informations_matchs.csv généré")


if __name__ == "__main__":
    main()
