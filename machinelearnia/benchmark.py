from tools import *
import time as top

if __name__ == "__main__":

    w = 55
    cls()

    n = int(1e8)
    prevent = f"Je compte jusqu'à {n}..."
    print(prevent)
    s = top.time()
    for i in range(n):
        if i < 8:
            print(f"{i} ", sep=" ", end="")

    print(f"... {n}")
    print(f"Boucle classique : {(top.time() - s):.2f}\"")

    print(prevent)
    s = top.time()
    print(*(i for i in range(n) if i < 9), end="\b")
    print(f"... {n}")
    print(f"Boucle compréhension : {(top.time() - s):.2f}\"")

    top.sleep(3)
    sl(w)
