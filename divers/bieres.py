import numpy as np
import matplotlib.pyplot as plt
from tools import *

# Prix des bières
p1 = 0.85
p2 = 1.20

# Budget possible
x = np.linspace(0, 20, 200)

# Nombre de bières achetées
bieres_p1 = x / p1
bieres_p2 = x / p2

w = 57
cls()

print(f"Rapport : {p2 / p1:.2f} bières à {p1} € = 1 bière à {p2} €")

sl(w)
print(123)
sl(w)

# --- Création des deux graphes côte à côte ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 1) Graphe de gauche : Budget → Nombre de bières
axes[0].plot(x, bieres_p1, label="Bières à 0.85 €")
axes[0].plot(x, bieres_p2, label="Bières à 1.20 €")

ratio = p2 / p1
axes[0].axhline(
    ratio,
    linestyle="--",
    label=f"Rapport : {ratio:.2f} bières à 0.85 € = 1 bière à 1.20 €",
)

axes[0].set_xlabel("Budget (€)")
axes[0].set_ylabel("Nombre de bières")
axes[0].set_title("Budget → Nombre de bières")
axes[0].grid(True)
axes[0].legend()

# 2) Graphe de droite : Nombre de bières → Budget
bieres = np.linspace(0, 25, 200)
budget_p1 = bieres * p1
budget_p2 = bieres * p2

axes[1].plot(bieres, budget_p1, label="Bières à 0.85 €")
axes[1].plot(bieres, budget_p2, label="Bières à 1.20 €")

axes[1].set_xlabel("Nombre de bières")
axes[1].set_ylabel("Budget (€)")
axes[1].set_title("Nombre de bières → Budget")
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()
