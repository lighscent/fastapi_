from calendar import c
from re import M
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime, os

import subs.get_dataframe_from_gh_csv_files as gh


def sl():
    w = 99
    print("-" * w + "→")


if __name__ == "__main__":
    import pandas as pd

    df = gh.getGhCsvFilesAndSaveThem()
    # print(df)
    sl()
    # exit()

    print("5 samples :")
    df_sample5 = df.sample(5)

    pd.set_option("display.max_columns", None)  # Affiche toutes les colonnes
    pd.set_option("display.expand_frame_repr", False)  # Empêche le retour à la ligne
    print(df_sample5)

    pd.set_option("display.max_columns", 7)  # Affiche 7 les colonnes
    # pd.set_option('display.expand_frame_repr', True)  # Re-autorise le retour à la ligne
    print(df_sample5)

    sl()
    print(df.info())

    sl()
    print("Nettoyage des comonnes")

    df.columns = df.columns.str.strip()
    from collections import Counter

    print(Counter(df.columns))

    df = df.loc[:, ~df.columns.duplicated()]
    from collections import Counter

    print(Counter(df.columns))

    sl()
    print(df.isnull().sum(axis=0))
    sl()

    val_manquantes = df[df.isnull().any(axis=1)]
    print(val_manquantes)

    sl()
    print(val_manquantes.isnull().all())

    sl()
    print(df.shape)
    df.dropna(inplace=True)
    print(df.shape)

    sl()
    print(df.isnull().any())

    sl()
    print(df.describe())

    sl()
    print("1548".isdigit())

    sl()
    print(df[df["Order Date"] == "Order Date"])
    print((df["Order Date"].str.strip() == "Order Date").any())

    # print(df.loc[~df["Order ID"].str.isdigit(), :])
    # print((df['Order Date']))
    mask = df["Order Date"].str.strip() == "Order Date"
    df_clean = df.drop(df[mask].index)
    print("Lignes supprimées :", mask.sum())
    print("Nouveau shape :", df_clean.shape)
    print(df_clean.loc[~df_clean["Order ID"].str.isdigit(), :])

    sl()
    print(df_clean.head(3))

    sl()
    print(df_clean.info())
    df_clean["Quantity Ordered"] = df_clean["Quantity Ordered"].astype("int")
    print(df_clean.info())
    df_clean["Price Each"] = pd.to_numeric(df_clean["Price Each"])
    print(df_clean.info())

    sl()
    # df_clean["Order Date"] = pd.to_datetime(df_clean["Order Date"])
    df_clean["Order Date"] = pd.to_datetime(
        df_clean["Order Date"], format="%m/%d/%y %H:%M", errors="coerce"
    )
    nb_nat = df_clean["Order Date"].isna().sum()
    print(f"{nb_nat} ligne n'a pas pu être convertie en datetime.")

    df_clean["Order Date FR"] = df_clean["Order Date"].dt.strftime("%d/%m/%Y %H:%M")
    print(df_clean.info())
    print(df_clean[["Order Date", "Order Date FR"]])

    print(
        pd.DataFrame(
            {
                "Order Date": df["Order Date"].reset_index(drop=True),
                "Order Date FR": df_clean["Order Date FR"].reset_index(drop=True),
            }
        ).rename(
            columns={
                "Order Date": "Order Date (df)",
                "Order Date FR": "Order Date FR (df_clean)",
            }
        )
    )

    sl()

    df_affichage = pd.DataFrame(
        {
            "df['Order Date']": df["Order Date"].reset_index(drop=True),
            "df_clean['Order Date FR']": df_clean["Order Date FR"].reset_index(
                drop=True
            ),
            "df_clean['Order Date']": df_clean["Order Date"].reset_index(drop=True),
        }
    )

    print(df_affichage)

    sl()
    print(df_clean)
    print(df_clean.index)

    df_clean = df_clean.set_index("Order Date")
    print(df_clean)

    sl()
    df_clean["Month"] = df_clean.index.month_name()
    print(df_clean)

    sl()
    df_clean.sort_index(inplace=True)
    print(df_clean)

    sl()
    df_clean.drop("Order Date FR", axis=1, inplace=True)

    df_clean["chiffre_daffaire"] = df_clean["Quantity Ordered"] * df_clean["Price Each"]
    print(df_clean)

    sl()
    df = (
        df_clean.groupby("Month")["chiffre_daffaire"].sum().sort_values(ascending=False)
    )
    print(df)

    monthes = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    sl()
    df_ca_grouped_by_month = df_clean.groupby("Month").sum(["chiffre_daffaire"])
    print(df_ca_grouped_by_month.loc[monthes, ["chiffre_daffaire"]])
    # df_ca_grouped_by_month.loc[monthes, ["chiffre_daffaire"]].plot.bar(figsize=(13, 8))
    # plt.title("Chiffre d'affaire global par mois")
    # plt.show()
    print(df_ca_grouped_by_month.loc[monthes, ["chiffre_daffaire"]].max())
    ca_dec = float(
        df_ca_grouped_by_month["chiffre_daffaire"].sort_values(ascending=False).December
    )
    print(
        f"CA Décembre : ${ca_dec:,.2f} (Soit env.",
        f"{ca_dec*.85:,.2f}".replace(",", " ").replace(".", ","),
        "€)",
    )

    sl()
    print(df_clean["Purchase Address"].unique())

    # plt.savefig("ca_par_mois.png")
    def get_ville(addresse):
        return addresse.split(",")[1].strip()

    print("        python        ".strip())
    print(get_ville("760 Church St, San Francisco, CA 94016"))

    sl()
    df_clean["Ville"] = df_clean["Purchase Address"].apply(get_ville)
    print(df_clean.sample(5))
    print('Villes uniques :')
    print(*enumerate(df_clean["Ville"].unique()), sep="\n")

    ca_by_city = (
        df_clean.groupby("Ville").sum()["chiffre_daffaire"].sort_values(ascending=False)
    )
    print(ca_by_city)

    # plt.title("Chiffre d'affaire global par ville")
    # #ca_by_city.plot.barh(figsize=(8, 6))
    # ca_by_city.plot.bar(figsize=(8, 6))
    # plt.show()

    sl()
    df_clean['Heure'] = df_clean.index.hour
    ca_par_heure = pd.DataFrame(df_clean.groupby("Heure")["chiffre_daffaire"].sum())
    print(ca_par_heure)

    sns.lineplot(data=ca_par_heure["chiffre_daffaire"])
    # plt.xticks(ticks=range(0, 24))
    # plt.grid()
    # plt.title("Chiffre d'affaire par heure")
    # plt.show()

    sl()
    print(df_clean.groupby("Product")["Quantity Ordered"].sum().sort_values(ascending=False).head(7))
