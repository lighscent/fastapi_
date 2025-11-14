import numpy as np
from tabulate import tabulate

from tools import *

cls()

n = np.arange(1, 10)
print(np.vstack([n, n**2, n**3]))

sl()
print("Synthèse - Notes et statistiques avec NumPy")

notes = np.random.randint(21, size=(3, 5))

row_means = np.mean(notes, axis=1)
col_means = np.mean(notes, axis=0)
global_mean = np.mean(notes)

# Préparation du tableau avec les moyennes par ligne (en gras)
table = []
for i, row in enumerate(notes):
    table.append(
        [f"Élève {i+1}"] + list(row) + [f"\033[1m{round(row_means[i], 2)}\033[0m"]
    )

# Ajout de la ligne des moyennes par colonne (en gras) et la moyenne générale en bas à droite
table.append(
    ["Moyenne colonnes"]
    + [f"\033[1m{round(m, 2)}\033[0m" for m in col_means]
    + [f"\033[1m{round(global_mean, 2)}\033[0m"]
)

# Création des entêtes
headers = (
    ["Classe 1"] + [f"Col {j+1}" for j in range(notes.shape[1])] + ["Moyenne lignes"]
)

print(tabulate(table, headers=headers, tablefmt="grid"))

print("-" * 89)

# Math, Physique, SVT
x = np.array(
    [
        [6, 8, 4],
        [12, 10, 7],
        [8, 13, 11],
        [5, 7, 6],
        [10, 2, 11],
    ]
)

moyennes = np.mean(x, axis=1)

print("Moyennes des élèves :", moyennes)

for i, m in enumerate(moyennes, 1):
    print(f"Élève {i} : {m:.2f}")
print("-" * 89)

moyennes = np.mean(x, axis=1)
table = [[f"Élève {i+1}", f"{m:.2f}"] for i, m in enumerate(moyennes)]
# print(tabulate(table, headers=["Étudiant", "Moyenne"], tablefmt="grid"))
# print("-" * 89)

# print(x[x > 10])
# print("-" * 89)
indices = np.argwhere(x > 10)
# for i, j in indices:
#     print(f"Élève {i+1}, Matière {j+1} : {x[i, j]}")
# print("-" * 89)

# print(*[f"\bÉlève {i+1}, Matière {j+1} : {x[i, j]}\n" for i, j in indices])

# print("-" * 89)

# Math, Physique, SVT
x = np.array(
    [
        [6, 8, 4],
        [12, 10, 7],
        [8, 13, 11],
        [5, 7, 6],
        [10, 2, 11],
    ]
)

# notes_sup_5 = np.sum(x > 5)
# notes_sup_8_students = np.sum(x > 8, axis=1)
# nb_student_with_2_notes_sup_8 = np.sum(notes_sup_8_students >= 2)

# tous_les_etudiants_ont_note_sup_7 = np.all(np.any(x > 7, axis=1))

# Est-ce qu'il y au moins un élève ayant au moins une note supérieur à 12 ?
au_moins_un_etudiant_avec_note_sup_12 = np.any(x > 12)

# Quelle est la moyenne en Math et Physique de la classe si on considère uniquement les 3 élèves dont les notes apparaissent en premier ?
moyenne_math_physique_premiers_eleves = np.mean(x[:3, :2])

# print("Notes > 5 :", notes_sup_5)
# print("Notes > 8 par étudiant :", notes_sup_8_students)
# print("Nombre d'étudiants avec 2 notes > 8 :", nb_student_with_2_notes_sup_8)

# print("Tous ont au moins une note > 7 :", tous_les_etudiants_ont_note_sup_7)
# print("Au moins un étudiant a une note > 12 :", au_moins_un_etudiant_avec_note_sup_12)

# print("Moyenne Math et Physique des 3 premiers élèves :", moyenne_math_physique_premiers_eleves)

# la médiane des moyennes (elèves)
mediane_moyennes_eleves = np.median(np.mean(x, axis=1))
print(mediane_moyennes_eleves)

# Combien d'élèves ont au moins 2 notes supérieurs à la médiane des moyennes (élèves) de la classe ?
notes_sup_mediane = np.sum(x > mediane_moyennes_eleves, axis=1)
nb_eleves_avec_2_notes_sup_mediane = np.sum(notes_sup_mediane >= 2)
print(nb_eleves_avec_2_notes_sup_mediane)
