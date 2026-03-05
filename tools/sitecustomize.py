# Le fichier ./v/Lib/site-packages/sitecustomize.py
# est chargé automatiquement par Python au démarrage
# Il configure le sys.path pour tous les scripts, même lancés via Flet

import sys
from pathlib import Path

# Chemin vers la racine de ton projet
ROOT = Path(r"D:\c2\fastapi")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
