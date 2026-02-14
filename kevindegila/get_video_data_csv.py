from sqlalchemy import null
from datetime import datetime
import os, random, time
import numpy as np
import pandas as pd
from tabulate import tabulate
import flet as ft

# AUTHOR = "KevinDegila"
# AUTHOR = "c57-u5s"
# AUTHOR = "doro2255"
# AUTHOR = "LionelCOTE"
# AUTHOR = "MachineLearnia"

AUTHOR = "donaldprogrammeur"

# 2fix Améliorer script pour sauvegarde progressive permettant reprise sans perte si perte de connexion

TEST = 0

SUFFIX = f"_test{TEST}" if TEST else ""

CACHE_DIR = "D:/fastapi/kevindegila/cache"
CACHED_CSV_PATH = os.path.join(CACHE_DIR, f"{AUTHOR}_videos{SUFFIX}.csv")


def analyze_dataset(df):
    """Affiche quelques statistiques sur le dataset"""
    print("\n=== Statistiques du dataset ===")
    print(f"Nombre total de vidéos : {len(df)}")
    print(f"\nPériode couverte :")
    print(f"- Première vidéo : {df['upload_date'].min()}")
    print(f"- Dernière vidéo : {df['upload_date'].max()}")

    print(f"\nDurée moyenne des vidéos : {df['duration'].mean():.2f} secondes")

    if "view_count" in df.columns:
        print(f"\nVues :")
        print(f"- Total : {df['view_count'].sum():,}")
        print(f"- Moyenne : {df['view_count'].mean():,.0f}")
        print(f"- Médiane : {df['view_count'].median():,.0f}")

    # Vidéos par année
    videos_by_year = df.groupby(df["upload_date"].dt.year).size()
    print("\nVidéos par année :")
    print(videos_by_year)


def format_date(date):
    """Formate une date ou retourne 'N/A' si None"""
    if pd.isna(date) or date is None:
        return "N/A"
    try:
        return date.strftime("%Y-%m-%d")
    except:
        return "N/A"


def format_title(title, max_length=55):
    """Tronque le titre à max_length caractères et ajoute ... si nécessaire"""
    title = str(title or "N/A")
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title


def format_duration(seconds):
    """Convertit une durée en format HH:MM:SS"""
    if pd.isna(seconds):
        return "N/A"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def display_videos_table(df):
    """Affiche un tableau formaté des vidéos"""
    # Nettoyer les dates
    df["upload_date"] = pd.to_datetime(df["upload_date"], errors="coerce")

    # Préparer les données pour le tableau
    table_data = []
    for _, row in df.iterrows():
        views = row.get("view_count")
        likes = row.get("like_count")
        ratio = likes / views * 100
        url = row.get("url", "N/A")
        table_data.append(
            [
                format_date(row["upload_date"]),
                format_title(row.get("title", "N/A")),
                format_duration(row.get("duration")),
                views,
                f"{likes} ({ratio:.1f}" + " %)",
                row.get("comment_count") if pd.notna(row.get("comment_count")) else 0,
                format_title(url),
            ]
        )

    # Ajoute la ligne des totaux
    views = df["view_count"].sum()
    likes = df["like_count"].sum()
    ratio = likes / views * 100
    table_data.append(
        ["Date", "Titre", "Durée", "Views", "Likes ( % views)", "Commentaires", "url"]
    )
    table_data.append(
        [
            str(len(df)),  # Nombre total sous la dernière date
            "vidéos pour une durée totale de ",  # Titre pour la ligne des totaux
            format_duration(
                df["duration"].sum()
            ),  # Durée totale sous la dernière durée
            views,
            f"{likes} ({ratio:.1f}" + " %)",
            df["comment_count"].sum(),
            "---",
        ]
    )

    # En-têtes du tableau
    headers = [
        "Date",
        "Titre",
        "Durée",
        "Views",
        "Likes ( % views)",
        "Commentaires",
        "Url",
    ]

    # Afficher le tableau
    print(f"\n=== Liste des vidéos de {AUTHOR} ===")
    print(
        tabulate(
            table_data,
            headers=headers,
            tablefmt="grid",
            maxcolwidths=[15, 55, 10, 10, 20, 15, 30],
        )
    )


# Charger ou créer le dataset
def get_videos_dataset():

    # Si le fichier CSV n'existe pas, on fait une récupération complète
    if not os.path.exists(CACHED_CSV_PATH) or os.path.getsize(CACHED_CSV_PATH) == 0:
        return

    # Si le fichier CSV existe, on charge et on met à jour
    print("Chargement du dataset local...")
    df = pd.read_csv(CACHED_CSV_PATH)
    df["upload_date"] = pd.to_datetime(df["upload_date"])

    # Récupération des nouvelles vidéos
    last_date = df["upload_date"].max().strftime("%Y%m%d")
    print(f"Recherche des nouvelles vidéos depuis le {last_date}...")

    return df


if __name__ == "__main__":
    # Récupérer et trier le dataset
    df = get_videos_dataset()
    if df is None:
        print(f"Aucun dataset local trouvé: {CACHED_CSV_PATH}.")
        exit(1)
    df = df.sort_values("upload_date", ascending=False)

    # print(df.info())
    # print(df[1:2])
    pd.set_option("display.max_columns", None)
    pd.set_option("display.expand_frame_repr", False)  # Empêche le retour à la ligne
    display_videos_table(df.head(1))

    # exit()

    # Afficher le tableau
    # display_videos_table(df[1:2])
    display_videos_table(df)
    print(f"Fin de la liste des vidéos de \033[1m{AUTHOR}\033[0m")

    # print(df)
    # exit()  # Affiche les graphs

    import pandas as pd
    import matplotlib.pyplot as plt

    # 1. Conversion de la date en datetime
    df["upload_date"] = pd.to_datetime(df["upload_date"])

    # 2. Conversion de la durée en minutes
    df["duration_minutes"] = df["duration"] / 60

    # 3. Tracer la courbe
    plt.figure(figsize=(15, 8))
    plt.plot(df["upload_date"], df["duration"], marker="o")
    plt.xlabel("Date de publication")
    plt.ylabel("Durée (minutes)")
    plt.title(f"Durée des vidéos de $\\bf{{{AUTHOR}}}$ publiées au fil du temps")
    plt.grid(True)
    plt.show()
    # Regroupe par semaine et sommer les minutes
    weekly_prod = df.resample("W", on="upload_date")["duration"].sum()

    plt.figure(figsize=(10, 5))
    plt.plot(weekly_prod.index, weekly_prod.values, marker="o")

    exit()  # Affiche les autres graphs

    # Légendes plus explicites
    plt.xlabel("Date (par semaine)")  # Axe des x
    plt.ylabel("Durée totale des vidéos (minutes, échelle log)")  # Axe des y
    plt.title("Évolution hebdomadaire de la production vidéo")  # Titre

    plt.grid(True)
    plt.yscale("log")
    # https://prnt.sc/SgpuvAnZsxpf
    plt.show()

    # import seaborn as sns
    # sns.boxplot(x=weekly_prod.values)
    # plt.show()

    # plt.ylim(0, 7000)  # par exemple, limite à 7000 minutes
    # https://prnt.sc/KdXFvTV_45sh

    plt.plot(
        weekly_prod.index,
        weekly_prod.values,
        marker="o",
        label="Production hebdomadaire",
    )
    plt.plot(
        weekly_prod.index, weekly_prod.cumsum(), marker="x", label="Production cumulée"
    )
    plt.legend()
    plt.show()
    # https://prnt.sc/3ZWd-G1t-vTD
