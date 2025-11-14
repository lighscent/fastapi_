import os, sys

# Code à mettre au début de chaque script utilisant tools.py
# Récupère le chemin absolu du dossier du script
# Chemin vers le dossier où se trouve tools.py (remonte de 2 niveaux)
# Ajoute au path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# tools_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
# sys.path.append(tools_path)
# from tools import *


def sl(w=17):
    print("─" * w, "\b→")  # Ligne séparatrice


def cls():
    os.system("cls" if os.name == "nt" else "clear")
    # Envoie directement les codes ANSI pour effacer l'écran (+ robuste)
    # cls()
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


if __name__ == "__main__":

    cls()
    print("Ready.")
    sl(97)
