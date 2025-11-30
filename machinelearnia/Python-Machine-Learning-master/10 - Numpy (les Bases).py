# %% [markdown]
# <a href="https://colab.research.google.com/github/MachineLearnia/Python-Machine-Learning/blob/master/10%20-%20Numpy%20(les%20Bases).ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %% [markdown]
# # 10/30 Numpy : Tableau ndarray

# %%
import numpy as np


# %% [markdown]
# ## 1. Générateurs de tableaux **ndarray**
# - générateur par défaut : **ndarray()**
# - générateur 1D : **np.linspace** et **np.arange()**
# - générateur ND : **np.zeros()**, **np.ones()**, **np.random.randn()** (ce sont les plus utiles)

# %%
A = np.array(
    [1, 2, 3]
)  # générateur par défaut, qui permet de convertir des listes (ou autres objets) en tableau ndarray
A = np.zeros((2, 3))  # tableau de 0 aux dimensions 2x3
B = np.ones((2, 3))  # tableau de 1 aux dimensions 2x3
C = np.random.randn(2, 3)  # tableau aléatoire (distribution normale) aux dimensions 2x3
D = np.random.rand(2, 3)  # tableau aléatoire (distribution uniforme)

E = np.random.randint(
    0, 10, [2, 3]
)  # tableau d'entiers aléatoires de 0 a 10 et de dimension 2x3


# %%
A = np.ones(
    (2, 3), dtype=np.float16
)  # définit le type et la place a occuper sur la mémoire
B = np.eye(
    4, dtype=np.bool
)  # créer une matrice identité et convertit les éléments en type bool.


# %%
A = np.linspace(1, 10, 7)
B = np.arange(0, 10.5, 0.5)


# %% [markdown]
# ## 2. Attributs importants
# - size
# - shape

# %%
A = np.zeros((2, 3))  # création d'un tableau de shape (2, 3)

print(A.size)  # le nombre d'éléments dans le tableau A
print(A.shape)  # les dimensions du tableau A (sous forme de Tuple)

print(type(A.shape))  # voici la preuve que la shape est un tuple

print(A.shape[0])  # le nombre d'éléments dans la premiere dimension de A


# %% [markdown]
# ## 3. Méthodes importantes
# - **reshape()** : pour redimensionner un tableau
# - **ravel()** : pour applatir un tableau (qu'il ne fasse plus qu'une dimension)
# - **squeeze()** : quand une dimension est égale a 1, cette dimension disparait
# - **concatenate()** : assemble 2 tableaux ensemble selon un axes (existe aussi en hstack et vstack)

# %%
A = np.zeros((2, 3))  # création d'un tableau de shape (2, 3)

A = A.reshape((3, 2))  # redimensionne le tableau A (3 lignes, 2 colonnes)
A = A.ravel()  # Aplatit le tableau A (une seule dimension)
print(A.shape)

A = A.reshape(6, 1)
print(A.shape)

A = A.squeeze()  # élimine les dimensions "1" de A.
print(A.shape)


# %%
A = np.zeros((2, 3))  # création d'un tableau de shape (2, 3)
B = np.ones((2, 3))  # création d'un tableau de shape (2, 3)

C = np.concatenate((A, B), axis=0)  # axe 0 : équivalent de np.vstack((A, B))


# %%
D = np.concatenate((A, B), axis=1)  # axe 1 : équivalent de np.hstack((A, B))

D2 = np.hstack((A, B))

D3 = D2.reshape(4, 3)

## Reshape and reverse

A = np.array([1, 2, 3])
print(A.shape)
A = A.reshape((3, 1))
print(A.shape)
A = A.squeeze()
print(A.shape)


# %% [markdown]
# ## 4. Exercice et Solutions


# %%
def initialisation(m, n):
    # m : nombre de lignes
    # n : nombre de colonnes
    # retourne une matrice aléatoire (m, n+1)
    # avec une colonne biais (remplie de "1") tout a droite

    return X


# %%
# SOLUTION
def initialisation(m, n):
    # m : nombre de lignes
    # n : nombre de colonnes
    # retourne une matrice aléatoire (m, n+1)
    # avec une colonne biais (remplie de "1") tout a droite
    X = np.random.randn(m, n)
    X = np.concatenate((X, np.ones((X.shape[0], 1))), axis=1)

    return X


X = initialisation(3, 4)

pass  # Pour mettre point d'arrêt
# %%
