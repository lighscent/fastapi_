# //2do À tester :


#  Environnements isolés : python -m venv .venv → évite les conflits de dépendances.
# 2️⃣ F-strings : f"Bonjour {name}" → plus lisible que "Hello " + name.
# 3️⃣ Pathlib : Path("data") / "file.csv" → mieux que os.path.
# 4️⃣ Logging > print : logging.info("Start") → configurable et propre.
# 5️⃣ Typage léger : def add(a: int, b: int) -> int: → plus clair pour l’IDE.
# 6️⃣ Dataclasses : @dataclass class Config: → évite le boilerplate.
# 7️⃣ Générateurs : yield → traite les gros fichiers sans tout charger.
# 8️⃣ Context managers : with open("f.txt") as f: → ferme auto les ressources.
# 9️⃣ Enumerate : for i, v in enumerate(lst, 1): → pas besoin de range().
# 🔟 Unpacking : a, b, *rest = seq → élégant et concis.
# 1️⃣1️⃣ itertools : chain, islice, groupby → pour du code efficace.
# 1️⃣2️⃣ pytest : simple, lisible, parfait pour les tests rapides.
# 1️⃣3️⃣ Black + Ruff : formatage + lint auto → code homogène.
# 1️⃣4️⃣ Profiler : python -m cProfile → optimise ce qui compte vraiment.
# 1️⃣5️⃣ Futures : concurrent.futures → easy multithreading / multiprocessing.
# 1️⃣6️⃣ Exceptions précises : éviter except Exception: aveugle.
# 1️⃣7️⃣ Entrée script : if name == "main": → importable sans exécution.
# 1️⃣8️⃣ Petites pépites :
#  • tqdm → barres de progression
#  • functools.lru_cache → cache rapide
#  • shutil → gestion fichiers robuste
