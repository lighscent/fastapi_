import yt_dlp
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np
from tabulate import tabulate

url = "https://www.youtube.com/@KevinDegila/videos"
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "kevin_videos.json")

ydl_opts = {
    # "extract_flat": "in_playlist",
    "extract_flat": False,
    # "dump_single_json": True,
    "dump_single_json": False,
    "quiet": False,  # Afficher la progression
    "playlistend": None,  # Pas de limite sur le nombre de vidéos
    "progress": True,  # Afficher une barre de progression
    'sleep_interval': 2,  # délai de 2 secondes entre chaque vidéo
    'max_sleep_interval': 5,  # délai aléatoire jusqu’à 5 secondes
}


def fetch_and_save_videos():
    """Récupère les vidéos de YouTube et les sauvegarde en local"""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Créer le dossier cache s'il n'existe pas
        os.makedirs(CACHE_DIR, exist_ok=True)

        # Ajouter la date de dernière mise à jour
        data = {
            "last_update": datetime.now().isoformat(),
            "video_count": len(info.get("entries", [])),
            "data": info,
        }

        # Sauvegarder dans le fichier JSON
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return data


def load_cached_videos():
    """Charge les vidéos depuis le cache local"""
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Données chargées du cache ({data['video_count']} vidéos)")
            print(f"Dernière mise à jour : {data['last_update']}")
            return data["data"]
    except FileNotFoundError:
        print("Pas de cache trouvé, récupération depuis YouTube...")
        return fetch_and_save_videos()["data"]


def create_videos_dataset(info):
    """Convertit les données YouTube en DataFrame pandas"""
    videos = []
    for entry in info.get("entries", []):
        video = {
            "title": entry.get("title"),
            "upload_date": pd.to_datetime(entry.get("upload_date"), format="%Y%m%d"),
            "duration": entry.get("duration"),
            "view_count": entry.get("view_count"),
            "like_count": entry.get("like_count"),
            "comment_count": entry.get("comment_count"),
            "url": entry.get("url"),
            "video_id": entry.get("id"),
            "channel": entry.get("channel"),
            "description": entry.get("description"),
            "tags": entry.get("tags", []),
            "categories": entry.get("categories", []),
        }
        videos.append(video)

    df = pd.DataFrame(videos)

    # Sauvegarder en CSV pour plus de facilité
    csv_path = os.path.join(CACHE_DIR, "kevin_videos.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset sauvegardé dans {csv_path}")

    return df


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


def format_duration(seconds):
    """Convertit une durée en secondes en format MM:SS"""
    if pd.isna(seconds):
        return "N/A"
    minutes = int(seconds) // 60
    remaining_seconds = int(seconds) % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def format_date(date):
    """Formate une date ou retourne 'N/A' si None"""
    if pd.isna(date) or date is None:
        return "N/A"
    try:
        return date.strftime("%Y-%m-%d")
    except:
        return "N/A"


def format_title(title, max_length=59):
    """Tronque le titre à max_length caractères et ajoute ... si nécessaire"""
    title = str(title or "N/A")
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title


def format_total_duration(seconds):
    """Convertit une durée totale en format HH:MM:SS"""
    if pd.isna(seconds):
        return "N/A"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f"{hours:02d}h:{minutes:02d}m:{remaining_seconds:02d}s"


def display_videos_table(df):
    """Affiche un tableau formaté des vidéos"""
    # Nettoyer les dates
    df["upload_date"] = pd.to_datetime(df["upload_date"], errors="coerce")

    # Préparer les données pour le tableau
    table_data = []
    for _, row in df.iterrows():
        table_data.append(
            [
                format_date(row["upload_date"]),
                format_title(row.get("title", "N/A")),
                format_duration(row.get("duration")),
            ]
        )

    # Ajouter la ligne des totaux
    table_data.append(
        [
            str(len(df)),  # Nombre total sous la dernière date
            "vidéos pour une durée totale de ",  # Titre pour la ligne des totaux
            format_total_duration(
                df["duration"].sum()
            ),  # Durée totale sous la dernière durée
        ]
    )

    # En-têtes du tableau
    headers = ["Date", "Titre", "Durée"]

    # Afficher le tableau
    print("\n=== Liste des vidéos de Kevin Degila ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Charger ou créer le dataset
def get_videos_dataset():
    """Récupère le dataset, soit depuis le cache CSV, soit en le créant"""
    csv_path = os.path.join(CACHE_DIR, "kevin_videos.csv")

    # Si le fichier CSV existe et n'est pas vide
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        try:
            df = pd.read_csv(csv_path)
            # Vérifier si les colonnes requises existent
            required_columns = ["upload_date", "title", "duration"]
            if all(col in df.columns for col in required_columns):
                df["upload_date"] = pd.to_datetime(df["upload_date"])
                return df
        except Exception as e:
            print(f"Erreur lors de la lecture du CSV: {e}")

    # Si le CSV n'existe pas ou est invalide, recharger depuis YouTube
    print("Création d'un nouveau dataset depuis YouTube...")
    info = load_cached_videos()
    return create_videos_dataset(info)


# Obtenir et trier le dataset
df = get_videos_dataset()
df = df.sort_values("upload_date", ascending=False)

# Afficher le tableau
display_videos_table(df)
