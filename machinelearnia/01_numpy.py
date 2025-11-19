from sklearn.preprocessing import TargetEncoder
from tools import *

from time import sleep
from rich import print
import numpy as np


if __name__ == "__main__":

    w = 55
    cls()
    print("Numpy :")

    A = np.array(
        [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
    )

    print(A.T)
    print(A.T.ndim, A.T.shape)

    sl(w)
    print("A: ", A.ndim, A.shape, A)

    sl(w)
    B = np.ones((3, 2))
    print("B: ", B.ndim, B.shape, B)

    sl(w)
    print((A + B).ndim, (A + B).shape, A + B)

    print ('Produit matriciel')
    print (A@B.T)
    
    
    sleep(3)
    sl(w)
