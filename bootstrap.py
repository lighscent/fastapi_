# bootstrap.py — version auto‑détectable

import sys
from pathlib import Path

# Trouve la racine du projet en remontant jusqu'à trouver ce fichier
current = Path(__file__).resolve()
ROOT = current.parent

# Ajoute la racine au sys.path
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
