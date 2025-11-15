from tools import *
import numpy as np
import pandas as pd
from tabulate import tabulate

from matplotlib import pyplot as plt


if __name__ == "__main__":

    cls()

    # noms = ["paul", "radji", "bob", "alice"]
    noms = np.array(["paul", "radji", "bob", "alice"])
    noms = np.char.capitalize(noms)

    ages = [41, 53, 56, 38]
    poids = [12, 15.56, 98.25, 14.26]

    data = {"Noms": noms, "Âges": ages, "Poids": poids}
    df = pd.DataFrame(data)

    print(noms, ages, poids, sep="\n")

    sl()
    print(df)
    print(
        "\n"
        + tabulate(
            df, headers="keys", tablefmt="pretty", stralign="center", numalign="center"
        )
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    df["Âges"].plot(kind="line", ax=ax)
    # plt.gca().spines[['top', 'right']].set_visible(True)
    # Calculs
    mean = df["Âges"].mean()
    median = df["Âges"].median()
    std_sample = df["Âges"].std()
    std_pop = df["Âges"].std(ddof=0)

    # Lignes horizontales
    ax.axhline(
        mean, color="red", linestyle="-", linewidth=2, label=f"Moyenne: {mean:.2f} min"
    )
    ax.axhline(
        median,
        color="purple",
        linestyle=":",
        linewidth=5,
        label=f"Médiane: {median:.2f} min",
    )
    ax.axhline(
        std_sample,
        color="blue",
        linestyle=":",
        linewidth=2,
        label=f"Écart-type Échantillon: {std_sample:.2f} min",
    )
    ax.axhline(
        std_pop,
        linestyle="--",
        linewidth=2,
        label=f"Écart-type Population: {std_pop:.2f} min",
    )

    # ✅ Annotations
    ax.text(0.5, mean + 0.5, f"{mean:.2f}", color="red", fontsize=10)
    ax.text(0.5, median + 0.5, f"{median:.2f}", color="purple", fontsize=10)
    ax.text(0.5, std_sample + 0.5, f"{std_sample:.2f}", color="blue", fontsize=10)
    ax.text(0.5, std_pop + 0.5, f"{std_pop:.2f}", color="black", fontsize=10)

    # ✅ Stylisation des ticks
    ax.tick_params(axis="both", labelsize=12)
    ax.set_title("Âges", fontsize=14)
    ax.set_xlabel("Index", fontsize=12)
    ax.set_ylabel("Âge", fontsize=12)

    # ✅ Légende et layout
    ax.legend()
    plt.tight_layout()

    # ✅ Export PNG
    plt.savefig("graphique_ages.png", dpi=300)

    plt.show()
