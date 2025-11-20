from tools import *
import time as top
import locale


def fr_n_format(n):
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    return locale.format_string("%.2f", n, grouping=True)


def simple_comptage(n=1e8):  # 1e8
    n = int(n)
    formated_n = fr_n_format(n)

    prevent = f"Je compte jusqu'à {formated_n}..."
    print(prevent)
    s = top.time()
    # global i
    for i in range(n):
        if i < 8:
            print(f"{i} ", sep=" ", end="")
    print(f"... {fr_n_format(i)}.")
    print(f'Boucle classique : {(top.time() - s):.2f}"')
    # Mise dans une fonction, les var sont locales... + rapides !

    sl(w)
    print(prevent)
    s = top.time()
    print(*(i for i in range(n) if i < 9), end="\b")
    print(f"... {fr_n_format(i)}.")
    print(f'Boucle compréhension : {(top.time() - s):.2f}"')


if __name__ == "__main__":

    w = 55
    cls()

    simple_comptage()

    top.sleep(3)
    sl(w)
