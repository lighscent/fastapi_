# Code à mettre au début de chaque script utilisant tools.py
# Récupère le chemin absolu du dossier du script
# Chemin vers le dossier où se trouve tools.py (remonte de 2 niveaux)

import sys, os

from zmq import OUT_BATCH_SIZE
# from pathlib import Path

# # Ajoute le dossier parent "fastapi" au sys.path
# BASE_DIR = Path(__file__).resolve().parents[2]   # remonte 2 niveaux
# sys.path.append(str(BASE_DIR))

# OU

# Copier 1 seule fois D:\c2\fastapi\tools\sitecustomize.py
# (Lire instructions dedans)


def sl(w=99):
    print("─" * (w - 1), "\b→")  # Ligne séparatrice


def cls(empty_line=1):
    os.system("cls" if os.name == "nt" else "clear")
    # Envoie directement les codes ANSI pour effacer l'écran (+ robuste)
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()
    if empty_line:
        print()


if __name__ == "__main__":

    cls()
    print("Ready.")
    sl(97)
