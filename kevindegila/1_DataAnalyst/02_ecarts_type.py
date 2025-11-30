from tools import *
import numpy as np
import math
from tabulate import tabulate
import matplotlib.pyplot as plt


cls()
x = np.array([[1, 2, 3], [4, 5, 6]])
# x = np.delete(x, 0, axis=0) <=> x.drop(0) d'un df (pandas)
print(f"{x.shape[0]} lignes, {x.shape[1]} colonnes :")
print(x)

sl()
xmean = x.mean(axis=0)
print("Moyenne par colonne    : ", xmean)
xstd = x.std(axis=0)
print("Écart-type par colonne :", x.std())

xvar = x.var(axis=0)  # Variance par colonne
print("Variance par colonne   :", xvar)

print("Moyenne globale        :", np.mean(x))

print(np.median(x), np.median(x, axis=0))  # Ignore les extrêmes

sl()
# Un percentile (ou centile) est une valeur qui sépare un ensemble de données selon un pourcentage.
# Le 25ᵉ percentile (appelé aussi 1er quartile – Q1) est la valeur en dessous de laquelle se trouvent 25 % des données.
# Le 75ᵉ percentile (appelé aussi 3ᵉ quartile – Q3) est la valeur en dessous de laquelle se trouvent 75 % des données.
# Intervalle interquartile (IQR) : Q3 - Q1 ➡️ Il mesure l’étendue des données "centrales"
print("percentile", np.percentile(x, 25), np.percentile(x, 75))  # Quartiles

plt.figure()
plt.boxplot(x)
plt.title("Box-plot des données")
plt.xlabel("Élèves")
plt.ylabel("Notes")
plt.show()

sl()
x_centre_et_reduit = (x - xmean) / xstd
print(x_centre_et_reduit, "Moyenne = ", x_centre_et_reduit.mean(), x.std(), xstd)
