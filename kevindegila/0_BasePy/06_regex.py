from tools import *
import re


# réf.: http://www.regex101.com
if __name__ == "__main__":

    cls()
    print("Lionel\nCOTE\n" + r"Lionel\nCOTE\n")

    sl()
    txt = "Je m'appelle Lionel et mes pseudos sont Lionel25, Lionel59 ou encore        Lionel181 ce 2025-09-25."
    print(txt, "\n", "Lio" in txt, sep="")

    sl()
    # pseudos  = re.findall(r'Lionel[0-9]+', txt)
    pseudos = re.findall(r"Lionel\d+", txt)
    print(pseudos)

    sl()
    clean = re.sub(r"\s+", " ", txt).strip()
    print(clean)

    pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    date = pattern.search(txt)
    print("La date est", date.group(3), date.group(2), date.group(1))

    # Remplacement avec une fonction pour réutiliser les groupes
    def replacer(match):
        return f"{match.group(3)}/{match.group(2)}/{match.group(1)}"

    # Utilisation du pattern compilé
    tr = pattern.sub(replacer, clean)
    print(tr)  # → La date est 25/09/2025.

    sl()
    print(
        # pattern.sub(lambda m: f"{m.group(3)}/{m.group(2)}/{m.group(1)}", clean)
        pattern.sub(r"\3/\2/\1", clean)
    )  # → La date est 25/09/2025.
