import numpy as np
import matplotlib.pyplot as plt
from tools import *

# Prix des bières
p1 = 0.85
p2 = 1.2

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

# Graphe
plt.plot(x, bieres_p1, label="Bières à 0.85 €")
plt.plot(x, bieres_p2, label="Bières à 1.25 €")

# Marquer le rapport
ratio = p2 / p1
plt.axhline(
    ratio,
    linestyle="--",
    label=f"Rapport : {ratio:.2f} bières à 0.85 € = 1 bière à 1.25 €",
)

plt.xlabel("Budget (€)")
plt.ylabel("Nombre de bières")
plt.title("Comparaison : Bières à 0.85€ vs. 1.25€")
plt.grid(True)
# plt.legend()
# plt.show()
