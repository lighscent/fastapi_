import os, sys


def sl(w=377):
    print("─" * (w // 2), "→")


def cls():
    os.system("cls" if os.name == "nt" else "clear")
    # Envoie directement les codes ANSI pour effacer l'écran (+ robuste)
    # cls()
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


if __name__ == "__main__":

    cls()
    print('Ready.')
    sl()
