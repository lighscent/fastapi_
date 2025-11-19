from sklearn.preprocessing import TargetEncoder
from tools import *

from time import sleep


if __name__ == "__main__":

    w = 55
    cls()
    print("Régression linéaire :")

    ## 1 - Dataset (m 6 lignes, n 1 feature)
    # y: Target
    # x: Features

    ## 2 - Modèle: f(x) = ax + b (Prédis y)
    # paramètres (a & b à approcher par l'algo)

    ## 3 - Fonction Coût (Mesure des erreurs)
    # (f(x_i) - y_i) ** 2 - Distance (ou Norme) Euclidienne
    # j(a, b) = 1/2m * S(m-i) (f(x_i) - y_i) ** 2 - Erreur Quadratique moyenne
    # soit Mean Squared Error (MSE)

    ## 4 - Algorithme d'apprentissage, de minimisation (des erreurs)
    # Soit 1 - Méthode des moindres carrés (Recherche immédiate de la tengente horizontale)
    # Soit 2 - Descente de gradients

    sleep(3)
    sl(w)
