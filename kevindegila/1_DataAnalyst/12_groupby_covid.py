import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from tools.utils import *


if __name__ == "__main__":

    cls()

    w = 237

    pathFile = "datasets\\COVID-19-geographic-disbtribution-worldwide-2020-12-14.xls"
    if os.path.exists(pathFile):
        df = pd.read_excel(pathFile)
    else:
        print("Fichier introuvable :", pathFile)
        exit()

    print(df)

    sl(w)
    print(df.isna().sum())

    # exit()
    sl(w)
    nans = df.isna().sum().sum()
    print("Nombre total des NaN :", nans)

    sl(w)
    print("% des NaN :", f"{nans.sum()/len(df)*100:,.2f} %")
    print('shape :', df.shape)

    sl(w)
    print("comme peu important (5 % des données), on drop les NaN")
    df.dropna(inplace=True)

    sl(w)
    print("Nouveau nombre des NaN :", df.isna().sum().sum())

    sl(w)
    print("Nouveau shape :", df.shape)

    sl(w)
    df_c_by_country = (
        df.groupby("countriesAndTerritories")[["cases", "deaths"]]
        .sum()
        .sort_values("cases", ascending=False)
    )
    df_c_by_country.reset_index(inplace=True)
    df_c_by_country["%"] = (
        df_c_by_country["deaths"] / df_c_by_country["cases"] * 100
    ).round(2)
    print(f"{df_c_by_country.shape[0]} pays dans le dataset ({df_c_by_country.shape[1]} colonnes):")
    # pd.set_option("display.max_rows", None)  # Afficher toutes les lignes
    # pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes si besoin
    print(df_c_by_country.sort_values("%", ascending=False))
    # print(df_c_by_country)

    # exit()
    # # Graphique du top 5 de décès avec noms de pays en abscisse
    top5 = df_c_by_country.sort_values("%", ascending=False).head(5)
    plt.figure(figsize=(8, 6))
    plt.bar(top5["countriesAndTerritories"], top5["%"])
    plt.xlabel("Pays")
    plt.ylabel("Taux de mortalité (%)")
    plt.title("Top 5 des pays par taux de mortalité")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # exit()
    # Agrégation par continent
    df_c_by_continent = (
        df.groupby("continentExp")[["cases", "deaths"]]
        .sum()
        .sort_values("cases", ascending=False)
    )

    # Calcul du taux de mortalité par continent
    df_c_by_continent["mortality_rate_pct"] = (
        df_c_by_continent["deaths"] / df_c_by_continent["cases"] * 100
    ).round(2)

    # Formatage à la française (optionnel)
    df_c_by_continent["mortality_rate_fmt"] = df_c_by_continent[
        "mortality_rate_pct"
    ].map(lambda x: f"{x:.2f}".replace(".", ",") + " %")

    # Affichage
    print(df_c_by_continent.sort_values("mortality_rate_pct", ascending=False))

    plt.figure(figsize=(10, 6))
    plt.bar(
        df_c_by_continent.index,
        df_c_by_continent["mortality_rate_pct"].sort_values(ascending=False),
    )
    plt.xlabel("Continent")
    plt.ylabel("Taux de mortalité (%)")
    plt.title("Taux de mortalité par continent")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    sl(w)
    print("Ready.")
