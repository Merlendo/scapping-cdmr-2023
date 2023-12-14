# -*- coding: utf-8 -*-
"""
Collection de fonctions utilitaires
"""

import os
import webbrowser
import time


def remplacer_html(file_name: str, valeurs_a_remplacer: dict):
    """
    Remplace les valeurs spécifiées dans un fichier HTML.

    Parameters:
    file_name : str 
        Nom du fichier HTML à modifier.
    valeurs_a_remplacer : dict 
        Dictionnaire contenant les remplacements à effectuer.

    Returns:
    contenu : str 
        Contenu du fichier HTML modifié.
    """
    with open(os.path.join("contenus",
                           "templates",
                           file_name),
              encoding="utf-8") as f:
        contenu = f.read()

        for key, value in valeurs_a_remplacer.items():
            contenu = contenu.replace("{{" + key + "}}", value)

    return contenu


def nom_pays():
    """
    Retourne une liste de noms de pays en fonction des fichiers présents dans 
    le répertoire "data/informations_joueurs".

    Returns:
     list: Liste des noms de pays.
    """
    if os.path.exists(path("data", "informations_joueurs")):
        return os.listdir(path("data", "informations_joueurs"))


def open_html(file_path: str):
    """
    Ouvre le fichier HTML spécifié dans un nouvel onglet du navigateur.

    Parameters:
        file_path : str
            Chemin du fichier HTML à ouvrir.
    """
    return webbrowser.open_new_tab(f"file://{file_path}")


def path(*args) -> str:
    """
    Retourne le chemin absolu en utilisant les arguments fournis.

    Parameters:
        args: Arguments à utiliser pour construire le chemin.

    Returns:
        str: Chemin absolu résultant.
    """
    return os.path.realpath(os.path.join(*args))


def clear():
    """Nettoie la console Spyder ou l'invite de commande."""
    print("\033[H\033[J")


def timing(func):
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction.

    Parameters:
        func: Fonction à mesurer.

    Returns:
        wrapper: Fonction décorée.
    """
    def wrapper(*args, **kwargs):
        # Enregistre le début du script
        start_time = time.time()

        # Fonction dont on veut calculer le temps d'exécution
        result = func(*args, **kwargs)

        # Enregistre la fin du script
        end_time = time.time()

        # Calcule la durée du script
        elapsed_time = end_time - start_time

        # Calcule les minutes et secondes
        minutes, secondes = divmod(elapsed_time, 60)

        # Affiche la durée du script
        print(
            f"Temps passé au total : {minutes:.0f} minutes et {secondes:.2f} secondes")

        return result
    return wrapper
