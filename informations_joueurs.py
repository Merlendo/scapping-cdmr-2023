# -*- coding: utf-8 -*-
"""
Fichier de scrapping sur les informations joueurs
"""

import urllib.request
import urllib3
import pandas as pd
import time
import os
import json
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor


def recupere_info(players: list, pays: str, http: urllib3.poolmanager.PoolManager):
    """
    Fonction qui permet de partitionner les requètes afin d'améliorer la 
    vitesse de collecte de donnée.

    Parameters
    ----------
    players : list
        Liste d'informations joueurs json.
    pays : str
        Nom du pays.
    http : urllib3.poolmanager.PoolManager
        PoolManager pour utiliser urllib3.

    Returns
    -------
    partie_liste_joueur : list
        renvoi une partie des informations joueurs traitée.

    """
    partie_liste_joueur = []
    # Parcours chaque joueur
    for n_joueur, player in enumerate(players, start=1):

        # Récupère l'id
        id_joueur = player["player"]["id"]

        # Téléchargement de l'image du joueur :
        try:
            img_url = f"https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{id_joueur}.png"
            path_img = os.path.join(
                "data", "informations_joueurs", pays, "imgs", id_joueur + ".png")
            urllib.request.urlretrieve(img_url, path_img)
        except HTTPError:
            pass
            # print(f"pas d'image pour {id_joueur}")

        # Téléchargement des stats complémentaires du joueur
        stats_url = f"https://api.wr-rims-prod.pulselive.com/rugby/v3/stats/player/{id_joueur}/ALLTIME_SPORT?sport=mru&detail=2"
        response_stats = http.request("GET", stats_url)
        # Évite le conflie de version de urllib3
        try:
            stats = response_stats.json()
        except AttributeError:
            stats = json.loads(response_stats.data)

        # Créer un dictionnaire pour chaques joueurs
        player_stats = {}
        player_stats["id"] = id_joueur
        player_stats["name"] = player["player"]["name"]["display"]
        player_stats["hometown"] = player["player"]["pob"]
        player_stats["age"] = player["player"]["age"]["years"]
        player_stats["height"] = player["player"]["height"]
        player_stats["weight"] = player["player"]["weight"]
        player_stats["position"] = player["positionLabel"]

        player_stats["Conversions"] = stats["stats"]["Conversions"]
        player_stats["Drawn"] = stats["stats"]["Drawn"]
        player_stats["DropGoals"] = stats["stats"]["DropGoals"]
        player_stats["Lost"] = stats["stats"]["Lost"]
        player_stats["Matches"] = stats["stats"]["Matches"]
        player_stats["MissedConversions"] = stats["stats"]["MissedConversions"]
        player_stats["MissedDropGoals"] = stats["stats"]["MissedDropGoals"]
        player_stats["MissedPenalties"] = stats["stats"]["MissedPenalties"]
        player_stats["Penalties"] = stats["stats"]["Penalties"]
        player_stats["PointsAgainst"] = stats["stats"]["PointsAgainst"]
        player_stats["PointsFor"] = stats["stats"]["PointsFor"]
        player_stats["PointsScored"] = stats["stats"]["PointsScored"]
        player_stats["RedCards"] = stats["stats"]["RedCards"]
        player_stats["Tries"] = stats["stats"]["Tries"]
        player_stats["UsedReplacement"] = stats["stats"]["UsedReplacement"]
        player_stats["Won"] = stats["stats"]["Won"]
        player_stats["YellowCards"] = stats["stats"]["YellowCards"]
        player_stats["TackleSuccess"] = stats["extendedStats"]["TackleSuccess"]
        player_stats["Tackles"] = stats["extendedStats"]["Tackles"]

        partie_liste_joueur.append(player_stats)

    return partie_liste_joueur


def main():
    """
    Fonction principale

    """

    # Récupère les équipes de la coupe du monde
    url_equipe = "https://api.wr-rims-prod.pulselive.com/rugby/v3/event/1893/teams"
    response = urllib.request.urlopen(url_equipe)
    teams = json.loads(response.read().decode())["teams"]

    # Créer un poolmanager pour envoyer des requêtes.
    # urllib3 réduit le temps de requètes pour les stats joueurs
    http = urllib3.PoolManager()

    for num_team, team in enumerate(teams, start=1):

        # Enregistre le début de l'équipe
        start_time_team = time.time()

        # Récupére les infos du pays
        pays_id = team["id"]
        pays = team["abbreviation"]

        # Créer le dossier des images joueurs
        path_dossier = os.path.join(
            "data", "informations_joueurs", pays, "imgs")
        if not os.path.exists(path_dossier):
            os.makedirs(path_dossier)

        # Initialise la liste des joueurs
        liste_joueurs = []

        url_joueur = f"https://api.wr-rims-prod.pulselive.com/rugby/v3/event/1893/squad/{pays_id}"
        response = urllib.request.urlopen(url_joueur)
        players = json.loads(response.read().decode())["players"]

        # Calcul le nombre de joueurs dans chaque subset
        nb_elem_subset = len(players)  # On peux modifier cette valeur
        taille_subset = len(players) // nb_elem_subset  # Egale à 1

        # Utilisation du threading pour réduire le temps de téléchargement
        with ThreadPoolExecutor(max_workers=len(players)) as executor:
            futures = []

            # Soumet les différentes tâches
            for i in range(0, len(players), taille_subset):
                players_subset = players[i:i+taille_subset]
                future = executor.submit(
                    recupere_info, players_subset, pays, http)
                futures.append(future)

            # Recupère les informations quand elles sont prétes
            for future in futures:
                liste_joueurs.extend(future.result())

        # Export l'équipe en csv
        pd.DataFrame(liste_joueurs).to_csv(
            os.path.join("data", "informations_joueurs", pays, pays + ".csv"),
            sep=";",
            index=False)

        # Enregistre la fin de l'équipe
        end_time_team = time.time()

        # Calcul la durée de l'équipe
        elapsed_time_team = end_time_team - start_time_team

        # Affiche la durée de l'équipe
        print(
            f"{num_team:02d}/20 Équipe de {pays} : {elapsed_time_team:.2f} seconds")


if __name__ == "__main__":
    main()
