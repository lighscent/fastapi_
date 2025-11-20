from tools import *
import time as top

if __name__ == "__main__":

    w = 55
    cls()

    n = int(1e8)
    prevent = f"Je compte jusqu'à {n}..."
    print(prevent)
    s = top.time()
    for i in range(n): # Ce i est global... <=> Recherche dans un dictionnaire
        if i < 8:
            print(f"{i} ", sep=" ", end="")

    print(f"... {i}")
    print(f"Boucle classique : {(top.time() - s):.2f}\"")
    
    sl(w)
    print(prevent)
    s = top.time()
    print(*(i for i in range(n) if i < 9), end="\b") # Ici, les var sont générées
    print(f"... {i}")
    print(f"Boucle compréhension : {(top.time() - s):.2f}\"")

    top.sleep(3)
    sl(w)
