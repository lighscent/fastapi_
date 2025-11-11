import numpy as np
import pandas as pd
import math, os, platform
from tabulate import tabulate
import urllib.request

from matplotlib import pyplot as plt
import os


def cls():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":

    w = 150

    noms = ["paul", "radji", "bob", "alice"]
    ages = [41, 53, 56, 38]
    poids = [12, 15.56, 98.25, 14.26]

    data = {"noms": noms, "ages": ages, "poids": poids}
    df = pd.DataFrame(data)

    # print("\n" * 99, "\b" + "─" * 70 + ">")
    # print("\n" * 9)
    cls()

    print(noms, ages, poids, sep="\n")
    print("-" * w)
    print(df)
    print(
        "\n"
        + tabulate(
            df, headers="keys", tablefmt="pretty", stralign="center", numalign="center"
        )
    )

    from matplotlib import pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    df["ages"].plot(kind="line", ax=ax)
    # plt.gca().spines[['top', 'right']].set_visible(True)
    ax.axhline(
        df["ages"].mean(),
        color="red",
        linestyle="-",
        linewidth=2,
        label=f"Moyenne: {df['ages'].mean():.2f} min",
    )
    ax.axhline(
        df["ages"].median(),
        color="purple",
        linestyle=":",
        linewidth=5,
        label=f"Médiane: {df['ages'].median():.2f} min",
    )
    ax.axhline(
        df["ages"].std(),
        color="blue",
        linestyle=":",
        linewidth=2,
        label=f"Écart-type Échantillon: {df['ages'].std():.2f} min",
    )
    ax.axhline(
        df["ages"].std(ddof=0),
        linestyle="--",
        linewidth=2,
        label=f"Écart-type de Population: {df['ages'].std(ddof=0):.2f} min",
    )
    # exit()
    ax.set_title("Âges")
    ax.legend()
    plt.tight_layout()
    plt.show()
