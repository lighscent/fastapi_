# //2do À tester :

# flet run .\python\tips.py

#   1️⃣ Environnements isolés : python -m venv .venv → évite les conflits de dépendances.
# python -m venv .venv
# .\.venv\Scripts\activate
# pip install flet PyYAML
# py -m pip freeze > requirements.txt
# py -m pip install -r requirements.txt

# Complète reinstall de l'env
# sortir de l'env
# deactivate

# supprimer .venv
# Remove-Item -Recurse -Force .venv

# recréer l'env
# python -m venv .venv
# .\.venv\Scripts\activate

# réinstaller tes packages
# pip install flet flet-cli flet-desktop PyYAML pytest tqdm


#   2️⃣ F-strings : f"Bonjour {name}" → plus lisible que "Hello " + name.
name = "Lionel"
print(f"Hi, {name} !")


#   3️⃣ Pathlib : Path("data") / "file.csv" → mieux que os.path.
from pathlib import Path

print(Path("data") / "file.csv")


#   4️⃣ Logging > print : logging.info("Start") → configurable et propre.
import logging

# logging.basicConfig(level=logging.DEBUG)

# logging.basicConfig(
#     filename="python/app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

logging.debug("Détail technique")
logging.info("Start")
logging.warning("Attention")
logging.error("Erreur")
logging.critical("Crash")


#   5️⃣ Typage léger : def add(a: int, b: int) -> int: → plus clair pour l’IDE.
def add(a: int, b: int) -> str:
    return f"{a} + {b} = {a + b}"


print(add(1, 2))


#   6️⃣ Dataclasses : @dataclass class Config: → évite le boilerplate.
# Cf. ./dataclass_tip.txt


#   7️⃣ Générateurs : yield → traite les gros fichiers sans tout charger.
#   8️⃣ Context managers : with open("f.txt") as f: → ferme auto les ressources.
# Cf. ./yield_tip.txt


#   9️⃣ Enumerate : for i, v in enumerate(lst, 1): → pas besoin de range().
fruits = ["pomme", "banane", "cerise"]

for i in range(len(fruits)):
    print(i + 1, fruits[i])
for i, fruit in enumerate(fruits, 1):
    print(i, fruit)
# Pourquoi enumerate(lst, 1) est mieux
# i = index (ici commence à 1)
# fruit = valeur
# Pas de range()
# Code plus lisible et plus pythonique 🐍


#   🔟 Unpacking : a, b, *rest = seq → élégant et concis.
seq = [1, 2, 3, 4, 5]
a, b, *rest = seq
print(a)  # 1
print(b)  # 2
print(rest)  # [3, 4, 5]


ligne = "2026-01-14;Alice;Paris;Admin"
date, user, *infos = ligne.split(";")
print(date)  # 2026-01-14
print(user)  # Alice
print(infos)  # ['Paris', 'Admin']


first, *middle, last = [10, 20, 30, 40, 50]
print(first)  # 10
print(middle)  # [20, 30, 40]
print(last)  # 50


a = 5
b = 10
a, b = b, a


points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(x, y)

print("-" * 77)
# 1️⃣1️⃣ itertools : chain, islice, groupby → pour du code efficace.

# chain → enchaîner des itérables
from itertools import chain

a = [1, 2, 3]
b = [4, 5]
c = [6, 7]
for x in chain(a, b, c):
    print(x)
# ➡️ Équivalent à a + b + c mais sans créer une nouvelle liste.


# Cas pratiques :

print("-" * 77)
# all_users = chain(admins, moderators, users)
# islice → découper un itérateur
from itertools import islice


def compteur():
    i = 0
    while True:
        yield i
        i += 1


for x in islice(compteur(), 5):
    print(x, end=" ")
# Sortie : 0 1 2 3 4


# ➡️ Comme un slice, mais pour générateurs / streams.

# groupby → grouper des éléments consécutifs
from itertools import groupby

data = [
    ("FR", "Paris"),
    ("FR", "Lyon"),
    ("DE", "Berlin"),
    ("DE", "Munich"),
]
# ⚠️ Important : les données doivent être déjà triées par la clé.
data.sort(key=lambda x: x[0])

for country, cities in groupby(data, key=lambda x: x[0]):
    print(country, list(cities))
# Sortie :
# DE [('DE', 'Berlin'), ('DE', 'Munich')]
# FR [('FR', 'Paris'), ('FR', 'Lyon')]


# Exemple réaliste : pipeline efficace :

# from itertools import chain, islice, groupby
# logs = chain(logs_app1, logs_app2)
# errors = (l for l in logs if "ERROR" in l)
# for level, group in groupby(errors, key=lambda l: l.split()[0]):
#     for line in islice(group, 10):
#         print(line)

# ➡️ Tout est lazy, rapide, mémoire minimale.
# À retenir
# chain → concatène sans copier
# islice → découpe un flux
# groupby → regroupe (si trié)
# itertools = boîte à outils pro 🧰


print("\n" + "-" * 77)
# 1️⃣2️⃣ pytest : simple, lisible, parfait pour les tests rapides.
# Se lance avec: python -m pytest


# 1️⃣3️⃣ Black + Ruff : formatage + lint auto → code homogène.
# fichier: messy.py
# def add(a, b):return a + b
# x = 10
# y = 20
# print( add(x, y))
# =>
# fichier: messy.py
# def add(a, b):
#     return a + b
# x = 10
# y = 20
# print(add(x, y))
# = prettier

# 1️⃣4️⃣ Profiler : python -m cProfile → optimise ce qui compte vraiment.
# Lancer: python -m cProfile python/compute.py
# Analyse
# slow_function prend 1 seconde → goulot d’étranglement
# fast_function prend 0.01 seconde → négligeable
# cProfile te permet de repérer exactement ce qui ralentit ton programme

# 1️⃣5️⃣ Futures : concurrent.futures → easy multithreading / multiprocessing.
# cf. ./multi_thread.txt


# 1️⃣6️⃣ Exceptions précises : éviter except Exception: aveugle.
# cf. ./exception_tip.txt


# 1️⃣7️⃣ Entrée script : if name == "main": → importable sans exécution.


# 1️⃣8️⃣ Petites pépites :
#  • tqdm → barres de progression
from tqdm import tqdm
import time

for i in tqdm(range(10), desc="Chargement"):
    time.sleep(0.5)  # simulate some work


#  • functools.lru_cache → cache rapide
# cf. ./functools_lru_cache_tip.txt


#  • shutil → gestion fichiers robuste
