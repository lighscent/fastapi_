from sqlalchemy import null
import yt_dlp
import json
import os
import time
import random
from datetime import datetime
import pandas as pd
import numpy as np
from tabulate import tabulate

print("Attention, exit() car écrase des data potentiellement...")
# exit()  # Lancer se script écrasera un fichier peut-être déjà présent. À décommenter seulement si vous savez ce que vous faites. //2ar

# //2do faire effacer le .json lourd et devenu inutile à la fin du script.

SUFFIX = ""
# Mettre un nombre pour limiter le nombre de vidéos pour les tests, sinon None
TEST_COUNT = None

if TEST_COUNT:
    SUFFIX = f"_test{TEST_COUNT}"
    
# Définir l'auteur de la chaîne YouTube à analyser
# ❌ AUTHOR = "KevinDegila"
# ❌ AUTHOR = "c57-u5s"
# AUTHOR = "doro2255"
# ❌ AUTHOR = "MachineLearnia"
# AUTHOR = "donaldprogrammeur"
AUTHOR = "LionelCOTE"


url = f"https://www.youtube.com/@{AUTHOR}/videos"
CACHE_DIR = "D:/fastapi/kevindegila/cache"

CACHE_FILE = os.path.join(CACHE_DIR, f"{AUTHOR}_videos{SUFFIX}.json")

ydl_opts = {
    # "extract_flat": "in_playlist",
    "extract_flat": False,
    # "dump_single_json": True,
    "dump_single_json": False,
    "quiet": False,  # Afficher la progression
    "playlistend": None,  # Pas de limite sur le nombre de vidéos
    "progress": True,  # Afficher une barre de progression
    # "sleep_interval": "3-30",  # Délai aléatoire en secondes entre chaque vidéo
    # "sleep_interval_requests": 30, # Délai en secondes entre chaque requête
    # "max_sleep_interval": 30,  # Délai max en secondes
    # "sleep_before_extractor": 3,  # Délai avant la toute première extraction
}


def fetch_and_save_videos():
    """Récupère les vidéos de YouTube et les sauvegarde en local avec une pause aléatoire."""
    # 1. Get flat list of videos
    ydl_opts_flat = ydl_opts.copy()
    ydl_opts_flat["extract_flat"] = True

    print("Étape 1/2 : Récupération de la liste des vidéos...")
    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        playlist_info = ydl.extract_info(url, download=False)

    video_entries = playlist_info.get("entries", [])
    total_videos_global = len(video_entries)
    total_videos = total_videos_global

    # Limiter pour les tests
    if TEST_COUNT is not None:
        video_entries = video_entries[:TEST_COUNT]
        total_videos = len(video_entries)

    print(
        f"{total_videos_global} vidéo{'s' if total_videos_global>1 else ''} trouvées dans la playlist"
        + (
            f" (Limité à {TEST_COUNT} pour les tests)."
            if TEST_COUNT is not None
            else ""
        )
    )

    if not video_entries:
        print("Aucune vidéo trouvée. Le script est terminé.")
        # Create an empty cache file
        os.makedirs(CACHE_DIR, exist_ok=True)
        data = {
            "last_update": datetime.now().isoformat(),
            "video_count": 0,
            "data": {"entries": []},
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data

    # 2. Loop and get detailed info for each video
    full_video_info = []

    # Use the original ydl_opts (with extract_flat: False) for individual videos
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, entry in enumerate(video_entries):
            video_url = entry.get("url")
            if not video_url:
                continue

            # Random sleep
            sleep_duration = random.uniform(3, 25)
            print(
                f"Étape 2/2 : Traitement de la vidéo {i+1}/{total_videos}. Pause de {sleep_duration:.1f}s..."
            )
            time.sleep(sleep_duration)

            try:
                video_info = ydl.extract_info(video_url, download=False)
                full_video_info.append(video_info)
            except Exception as e:
                print(
                    f"Erreur lors de la récupération des détails pour {video_url}: {e}"
                )

    # 3. Reconstruct the info object and save
    final_info = playlist_info.copy()
    final_info["entries"] = full_video_info

    os.makedirs(CACHE_DIR, exist_ok=True)
    data = {
        "last_update": datetime.now().isoformat(),
        "video_count": len(final_info.get("entries", [])),
        "data": final_info,
    }
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
    """Convertit les données brutes de YouTube en DataFrame pandas."""
    videos = []
    for entry in info.get("entries", []):
        views = entry.get("view_count")
        likes = entry.get("like_count")

        like_ratio = (likes / views * 100) if likes and views and views > 0 else 0.0

        video = {
            "title": entry.get("title"),
            "upload_date": pd.to_datetime(entry.get("upload_date"), format="%Y%m%d"),
            "duration": entry.get("duration"),
            "view_count": views,
            "like_count": likes,
            "comment_count": entry.get("comment_count"),
            "url": entry.get("url"),
            "video_id": entry.get("id"),
            "channel": entry.get("channel"),
            "description": entry.get("description"),
            "tags": entry.get("tags", []),
            "categories": entry.get("categories", []),
            "like_ratio": like_ratio,  # Nouvelle ligne
        }
        videos.append(video)

    return pd.DataFrame(videos)


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

    if "like_count" in df.columns:
        print(f"\nLikes :")
        print(f"- Total : {df['like_count'].sum():,}")
        print(f"- Moyenne : {df['like_count'].mean():,.0f}")
        print(f"- Médiane : {df['like_count'].median():,.0f}")
        if "like_ratio" in df.columns:
            print(f"- Ratio Likes/Vues moyen : {df['like_ratio'].mean():.2f}%")

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


def format_title(title, max_length=59):
    """Tronque le titre à max_length caractères et ajoute ... si nécessaire"""
    title = str(title or "N/A")
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title


def format_duration(seconds):
    """Convertit une durée en secondes en format HH:MM:SS"""
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
            format_duration(
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
    """Charge le dataset depuis le CSV, et le met à jour si nécessaire."""
    csv_path = os.path.join(CACHE_DIR, f"{AUTHOR}_videos{SUFFIX}.csv")

    # Si le fichier CSV n'existe pas, on fait une récupération complète
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        state = (
            (f"partielle ({TEST_COUNT} items)", "")
            if TEST_COUNT
            else ("complète", " (peut être long)")
        )
        print(
            f"Aucun dataset local trouvé. Récupération {state[0]} depuis YouTube{state[1]}..."
        )
        # On utilise load_cached_videos qui gère le cache JSON pour le premier fetch
        full_info = load_cached_videos()
        df = create_videos_dataset(full_info)
        df.to_csv(csv_path, index=False)
        print(f"Dataset initial sauvegardé dans {csv_path}")
        return df

    # Si le fichier CSV existe, on charge et on met à jour
    print("Chargement du dataset local...")
    df = pd.read_csv(csv_path)
    df["upload_date"] = pd.to_datetime(df["upload_date"])

    # Récupération des nouvelles vidéos
    last_date = df["upload_date"].max().strftime("%Y%m%d")
    print(f"Recherche des nouvelles vidéos depuis le {last_date}...")

    # 1. Get flat list of new videos
    ydl_opts_update_flat = ydl_opts.copy()
    ydl_opts_update_flat["dateafter"] = last_date
    ydl_opts_update_flat["extract_flat"] = True

    print("Étape 1/2 (Mise à jour) : Récupération de la liste de toutes les vidéos...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts_update_flat) as ydl:
            new_playlist_infos = ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des vidéos: {e}")
        return df

    new_video_entries = new_playlist_infos.get("entries", [])
    # Limiter pour les tests
    if TEST_COUNT is not None:
        new_video_entries = new_video_entries[:TEST_COUNT]

    if not new_video_entries:
        print("Aucune nouvelle vidéo. Le dataset est à jour.")
        return df

    total_new_videos = len(new_video_entries)
    print(f"{total_new_videos} nouvelle(s) vidéo(s) trouvée(s).")

    # 2. Loop and get detailed info for each new video
    full_new_video_info = []
    # We don't need dateafter for individual video URLs
    ydl_opts_update = ydl_opts.copy()

    with yt_dlp.YoutubeDL(ydl_opts_update) as ydl:
        for i, entry in enumerate(new_video_entries):
            video_url = entry.get("url")
            if not video_url:
                continue

            # Random sleep
            sleep_duration = random.uniform(3, 30)
            print(
                f"Étape 2/2 (Mise à jour) : Traitement de la vidéo {i+1}/{total_new_videos}. Pause de {sleep_duration:.1f}s..."
            )
            time.sleep(sleep_duration)

            try:
                video_info = ydl.extract_info(video_url, download=False)
                full_new_video_info.append(video_info)
            except Exception as e:
                print(
                    f"Erreur lors de la récupération des détails pour {video_url}: {e}"
                )

    if full_new_video_info:
        # Reconstruct the info object for create_videos_dataset
        new_info = {"entries": full_new_video_info}
        new_df = create_videos_dataset(new_info)

        # Mise à jour du DataFrame et sauvegarde
        updated_df = pd.concat([df, new_df]).drop_duplicates(
            subset=["video_id"], keep="last"
        )
        updated_df.to_csv(csv_path, index=False)
        print(f"Dataset mis à jour dans {csv_path}")
        return updated_df
    else:
        print("Aucune nouvelle vidéo traitée avec succès. Le dataset est à jour.")
        return df


if __name__ == "__main__":
    # Obtenir et trier le dataset
    df = get_videos_dataset()
    df = df.sort_values("upload_date", ascending=False)

    # Afficher le tableau
    display_videos_table(df)
