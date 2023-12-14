# -*- coding: utf-8 -*-
"""
Génère la page pays.html 
"""

from utilitaires import remplacer_html, path, nom_pays


def main():
    """
    Fonction principal

    """
    # Génère les cartes pays
    pays_liste = ""
    for pays in nom_pays():
        nouveau_pays = remplacer_html(
            "card_pays_template.html", {"pays": pays})
        pays_liste += nouveau_pays

    # Intègre les cartes pays dans le template pays
    page_final = remplacer_html("pays_template.html", {
                                "pays_liste": pays_liste})

    # Créer la page pays
    path_pays = path("contenus", "pays.html")
    with open(path_pays, "w", encoding="utf-8") as f:
        f.write(page_final)
        print("Fichier pays.html généré")


if __name__ == "__main__":
    main()
