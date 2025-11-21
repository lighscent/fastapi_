import numpy as np
import matplotlib.pyplot as plt

# Créons des données réalistes : chaque ligne = un échantillon, chaque colonne = une feature

# Exemple : 5 échantillons et 3 features

B = np.array(
    [
        [1, 2, 5],  # échantillon 1
        [2, 4, 3],  # échantillon 2
        [3, 6, 4],  # échantillon 3
        [4, 8, 2],  # échantillon 4
        [5, 10, 1],  # échantillon 5
    ]
)

# Calcul de la matrice de corrélation entre les colonnes (features)

corr_matrix = np.corrcoef(B, rowvar=False)

print("Matrice de corrélation :")
print(corr_matrix)

# Visualisation simple avec matplotlib

plt.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Corrélation")
plt.xticks([0, 1, 2], ["Feature1", "Feature2", "Feature3"])
plt.yticks([0, 1, 2], ["Feature1", "Feature2", "Feature3"])
plt.title("Matrice de corrélation entre features")
plt.show()
