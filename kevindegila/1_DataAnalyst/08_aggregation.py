from tools import *
import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt


if __name__ == "__main__":

    cls()
    w = 237

    local_path = "datasets/Automobile_data.csv"

    # Vérifie si le fichier existe déjà
    if os.path.exists(local_path):
        # Si oui, on lit directement le fichier local
        auto = pd.read_csv(local_path)
        print("Fichier local trouvé, importé depuis", local_path)
    else:
        # Sinon, on télécharge depuis l'URL et on sauvegarde en local
        auto = pd.read_csv(
            "https://raw.githubusercontent.com/kevindegila/data-analyst/refs/heads/main/datasets/Automobile_data.csv"
        )
        os.makedirs("datasets", exist_ok=True)  # crée le dossier si besoin
        auto.to_csv(local_path, index=False)
        print("Fichier téléchargé et sauvegardé en local :", local_path)

    sl(w)
    print(auto)
    
    sl(w)
    print(auto.describe())

    sl(w)
    print(auto.describe().T)

    sl(w)
    print(auto["body-style"].value_counts())

    sl(w)
    print("auto.groupby('body-style').groups :")
    print(auto.groupby("body-style").groups)

    sl(w)
    print("auto.groupby('body-style').groups.keys() :")
    print(auto.groupby("body-style").groups.keys())

    sl(w)
    print("auto.groupby('body-style').groups.values() :")
    print(auto.groupby("body-style").groups.values())

    sl(w)
    print("auto.groupby('body-style').get_group('convertible') :")
    style = auto.groupby("body-style")
    print(style.get_group("convertible"))

    sl(w)
    print(auto["drive-wheels"].value_counts())

    double_groupin = auto.groupby(["body-style", "drive-wheels"])

    print("\ndouble groups", "─" * (w - 14))
    print(double_groupin.groups)
    
    print("\ndouble groupby", "─" * (w - 15))
    print(double_groupin.size())

    print("\ntriple groupby", "─" * (w - 15))
    triple_groupin = auto.groupby(["body-style", "fuel-type", "drive-wheels"])
    print(triple_groupin.size())

    print("\ntriple groupby hardtop", "─" * (w - 23))
    triple_groupin = auto.groupby(["body-style", "fuel-type", "drive-wheels"])
    triple_groupin.size().reset_index(name="count").query("`body-style` == 'hardtop'")
    print(triple_groupin.size().loc["hardtop"])

    print("\ntriple groupby hardtop fuel-type", "─" * (w - 33))
    # Groupement
    grouped = (
        auto.groupby(["body-style", "fuel-type", "drive-wheels"])
        .size()
        .reset_index(name="count")
    )

    # Filtrer les lignes où count == 6
    result = grouped.query(
        "`body-style` == 'hardtop' and `drive-wheels` == 'rwd' and count == 6"
    )

    # Récupérer le fuel-type
    fuel_type = result["fuel-type"].values[0]
    print("Fuel-type des 6 hardtop rwd :", fuel_type)

    print("\n\nfirst()", "─" * (w - 7) + "\n")
    print(double_groupin.first())  # 1ère combinaison de chaque groupe

    print("\n\nsize()", "─" * (w - 7) + "\n")
    print(style.size())

    print("\n\nsum()", "─" * (w - 6) + "\n")
    print(style.sum())

    print("\n\nget_group", "─" * (w - 10) + "\n")
    print(style.get_group("convertible"))

    print("\n\nfirst", "─" * (w - 6) + "\n")
    print(style.first())

    print("\n\ndescribe", "─" * (w - 9) + "\n")
    print(style.describe())

    print("\n\nstyle['city-mpg'].mean()", "─" * (w - 25) + "\n")
    mean_val = style["city-mpg"].mean()
    print(mean_val)
    print(mean_val.describe())

    # print(style["city-mpg"].mean().plot(kind="bar"))
    mean_val.plot(kind="bar")
    plt.title("Moyenne city-mpg")
    plt.ylabel("mpg")
    plt.tight_layout()
    plt.show()
