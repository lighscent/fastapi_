import this

def sl():
    w = 99
    print("─" * w + "→")


if __name__ == "__main__":
    sl()

    profil = ("Lionel", "COTE", 61, "Dijon")
    p, *infos = profil
    print(infos)
