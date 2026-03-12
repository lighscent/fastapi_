from datetime import datetime
import json, locale, os, time, yt_dlp
from importlib import import_module
import pandas as pd
from typing import TYPE_CHECKING, TypedDict, cast
from pymox_kit import *

_cache_utils_module = import_module(
    f"{__package__}.cache_utils" if __package__ else "cache_utils"
)
get_valid_cache_entry = _cache_utils_module.get_valid_cache_entry
write_videos_cache = _cache_utils_module.write_videos_cache

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

if TYPE_CHECKING:
    from yt_dlp.YoutubeDL import _Params

# ❌ liste avec * [ ] de toutes https://www.youtube.com/@InformatiqueSansComplexe/videos
# ainsi : * [ ] [sujet/titre durée vues likes commentaires date](url) → fichier .md

# ❌ Si le fichier .md existe déjà, regarder la date du scrapt, et si + d'un mois, essayer de capter que les nouvelles vidéos récentes
# print("Attention, exit() car écrase des data potentiellement...")
# exit()  # Lancer se script écrasera un fichier peut-être déjà présent. À décommenter seulement si vous savez ce que vous faites.

# //2do faire effacer le .json lourd et devenu inutile à la fin du script.
SUFFIX = ""

# Définir l'auteur de la chaîne YouTube à suivre ou pour test du script
# Ici,uniquement des ressources francophones

# Pour mise au point du script
AUTHOR = "doro2255"   # 1 seule vidéo (7')
# AUTHOR = "LionelCOTE"  # Pour mise au point car peu de vidéos (~12 - 1H30)
# AUTHOR = "c57-u5s"    # 16 videos - 11 heures et 23 minutes
# AUTHOR = "Alphorm" # Limiteur necessaire
# AUTHOR = "tseries"    # Compte le + rémunérateur au monde, pour tester le script sur un gros volume de vidéos (plus de 25 000 vidéos !!! → Limiteur necessaire )

# Initiation à Python (Bases)
# AUTHOR = "Gravenilvectuto"  # 174 videos - 49 heures et 39 minutes
# AUTHOR = "CodeAvecJonathan" #  10 videos - 15 heures et 16 minutes
# AUTHOR = "hassanbahi"       # ❌ 843 vidéos - total duration

# Python approfondi
# AUTHOR = "donaldprogrammeur" # Des bases à DevOps (424 vidéos) → Limitateur nécessaire

# Python pour l'I.A. ❌
# AUTHOR = "KevinDegila"  # 262 vidéos -
# AUTHOR = "InformatiqueSansComplexe"
# AUTHOR = "MachineLearnia"

AUTHOR = "LionelCOTE"  # Pour mise au point car peu de vidéos (~12 - 1H30)
AUTHOR = "KevinDegila"  # 262 vidéos -

url = f"https://www.youtube.com/@{AUTHOR}/videos"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SCRIPT_DIR, f"cache/.{AUTHOR}_videos.json")
CACHE_TTL = 3600  # 3600 (1 heure) 86400 (1 jour)


class YdlOpts(TypedDict, total=False):
    extract_flat: bool
    dump_single_json: bool
    quiet: bool
    playlistend: None
    progress: bool
    ignoreerrors: bool
    retries: int
    extractor_retries: int
    sleep_interval: float
    max_sleep_interval: float
    sleep_interval_requests: float
    sleep_before_extractor: float


YDL_OPTS: YdlOpts = {
    # "extract_flat": "in_playlist",
    "extract_flat": False,
    # "dump_single_json": True,
    "dump_single_json": False,
    "quiet": False,  # Afficher la progression
    "playlistend": None,  # Pas de limite sur le nombre de vidéos
    "progress": True,  # Afficher une barre de progression
    # Évite qu'une vidéo indisponible fasse échouer toute la playlist.
    "ignoreerrors": True,
    # Limiteur des impacts de rate-limit YouTube en espacant les requêtes.
    # "sleep_before_extractor": 1,
    # "sleep_interval_requests": 2,
    # "sleep_interval": 2,
    # "max_sleep_interval": 6,
    # Réessaie automatiquement en cas d'échec temporaire côté YouTube.
    "retries": 5,
    "extractor_retries": 5,
}


def zzzfetch_and_save_videos():
    """Récupère les vidéos de YouTube et les sauvegarde en local avec une pause aléatoire."""
    # 1. Get flat list of videos
    ydl_opts_flat = ydl_opts.copy()
    ydl_opts_flat["extract_flat"] = True

    print("Étape 1/2 : Récupération de la liste des vidéos...")
    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        playlist_info = ydl.extract_info(url, download=False)

    video_entries = playlist_info.get("entries", [])
    total_videos = len(video_entries)

    print(
        f"{total_videos} vidéo{'s' if total_videos>1 else ''} trouvées dans la playlist"
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
            time.sleep(sleep_duration)

    os.makedirs(CACHE_DIR, exist_ok=True)
    # data = {
    #     "last_update": datetime.now().isoformat(),
    #     "video_count": len(final_info.get("entries", [])),
    #     "data": final_info,
    # }
    # with open(CACHE_FILE, "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=2)

    # return data


def zzzload_cached_videos():
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


def zzz_create_videos_dataset(info):
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


def zzzanalyze_dataset(df):
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
    if date is None:
        return "N/A"
    try:
        return date.strftime("%d/%m/%Y")
    except:
        return "N/A2"


def title_shorter(title, max_length=59):
    """Tronque le titre à max_length caractères et ajoute ... si nécessaire"""
    title = str(title or "N/A")
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title


def format_duration(seconds):
    """Convertit une durée en secondes en MM:SS ou HH:MM:SS."""
    if pd.isna(seconds):
        return "N/A"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    if hours == 0:
        return f"{minutes:02d}:{remaining_seconds:02d}"
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def zzzdisplay_videos_table(df):
    """Affiche un tableau formaté des vidéos"""
    # Nettoyer les dates
    df["upload_date"] = pd.to_datetime(df["upload_date"], errors="coerce")

    # Préparer les données pour le tableau
    table_data = []
    for _, row in df.iterrows():
        table_data.append(
            [
                format_date(row["upload_date"]),
                title_shorter(row.get("title", "N/A")),
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
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Charger ou créer le dataset
def get_videos_dataset():
    """Charge le dataset depuis le CSV, et le met à jour si nécessaire."""

    pass

    # CACHE_FILE = os.path.join(os.path.expanduser("~"), f".{AUTHOR}_videos.md")
    # csv_path = os.path.join(CACHE_DIR, f"{AUTHOR}_videos{SUFFIX}.csv")

    # # Si le fichier CSV n'existe pas, on fait une récupération complète
    # if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    #     # state = (
    #     #     (f"partielle ({TEST_COUNT} items)", "")
    #     #     if TEST_COUNT
    #     #     else ("complète", " (peut être long)")
    #     # )
    #     state = ("complète", " (peut être long)")

    #     print(
    #         f"Aucun dataset local trouvé. Récupération {state[0]} depuis YouTube{state[1]}..."
    #     )
    #     # On utilise load_cached_videos qui gère le cache JSON pour le premier fetch
    #     full_info = load_cached_videos()
    #     df = create_videos_dataset(full_info)
    #     df.to_csv(csv_path, index=False)
    #     print(f"Dataset initial sauvegardé dans {csv_path}")
    #     return df

    # # Si le fichier CSV existe, on charge et on met à jour
    # print("Chargement du dataset local...")
    # df = pd.read_csv(csv_path)
    # df["upload_date"] = pd.to_datetime(df["upload_date"])

    # # Récupération des nouvelles vidéos
    # last_date = df["upload_date"].max().strftime("%Y%m%d")
    # print(f"Recherche des nouvelles vidéos depuis le {last_date}...")

    # # 1. Get flat list of new videos
    # ydl_opts_update_flat = ydl_opts.copy()
    # ydl_opts_update_flat["dateafter"] = last_date
    # ydl_opts_update_flat["extract_flat"] = True

    # print("Étape 1/2 (Mise à jour) : Récupération de la liste de toutes les vidéos...")
    # try:
    #     with yt_dlp.YoutubeDL(ydl_opts_update_flat) as ydl:
    #         new_playlist_infos = ydl.extract_info(url, download=False)
    # except Exception as e:
    #     print(f"Erreur lors de la récupération de la liste des vidéos: {e}")
    #     return df

    # new_video_entries = new_playlist_infos.get("entries", [])
    # # Limiter pour les tests
    # if TEST_COUNT is not None:
    #     new_video_entries = new_video_entries[:TEST_COUNT]

    # if not new_video_entries:
    #     print("Aucune nouvelle vidéo. Le dataset est à jour.")
    #     return df

    # total_new_videos = len(new_video_entries)
    # print(f"{total_new_videos} nouvelle(s) vidéo(s) trouvée(s).")

    # # 2. Loop and get detailed info for each new video
    # full_new_video_info = []
    # # We don't need dateafter for individual video URLs
    # ydl_opts_update = ydl_opts.copy()

    # with yt_dlp.YoutubeDL(ydl_opts_update) as ydl:
    #     for i, entry in enumerate(new_video_entries):
    #         video_url = entry.get("url")
    #         if not video_url:
    #             continue

    #         # Random sleep
    #         sleep_duration = random.uniform(3, 30)
    #         print(
    #             f"Étape 2/2 (Mise à jour) : Traitement de la vidéo {i+1}/{total_new_videos}. Pause de {sleep_duration:.1f}s..."
    #         )
    #         time.sleep(sleep_duration)

    #         try:
    #             video_info = ydl.extract_info(video_url, download=False)
    #             full_new_video_info.append(video_info)
    #         except Exception as e:
    #             print(
    #                 f"Erreur lors de la récupération des détails pour {video_url}: {e}"
    #             )

    # if full_new_video_info:
    #     # Reconstruct the info object for create_videos_dataset
    #     new_info = {"entries": full_new_video_info}
    #     new_df = create_videos_dataset(new_info)

    #     # Mise à jour du DataFrame et sauvegarde
    #     updated_df = pd.concat([df, new_df]).drop_duplicates(
    #         subset=["video_id"], keep="last"
    #     )
    #     updated_df.to_csv(csv_path, index=False)
    #     print(f"Dataset mis à jour dans {csv_path}")
    #     return updated_df
    # else:
    #     print("Aucune nouvelle vidéo traitée avec succès. Le dataset est à jour.")
    #     return df


def extract_video_datetime(video):
    """Retourne la date de publication la plus fiable disponible pour une vidéo yt-dlp."""
    # Champ le plus fiable pour YouTube dans yt-dlp: format YYYYMMDD
    upload_date = video.get("upload_date")
    if upload_date:
        try:
            return datetime.strptime(upload_date, "%Y%m%d")
        except (ValueError, TypeError):
            pass

    # Fallbacks utiles selon la source/format retourné par l'extracteur
    for key in ("timestamp", "release_timestamp", "available_at"):
        ts = video.get(key)
        if ts:
            try:
                return datetime.fromtimestamp(ts)
            except (ValueError, OSError, TypeError):
                continue

    return None


def timestamp2fr(ts, long="court") -> str:
    """_summary_

    Args:
        ts (_type_): _description_
        long (str, optional): _description_. Defaults to 'court'.

    Returns:
        str: _description_
    """
    dt = datetime.fromtimestamp(ts)
    return (
        dt.strftime("%d/%m/%Y %H:%M:%S")
        if long == "court"
        else dt.strftime("%A %d %B %Y - %H:%M:%S")
    )


def fetch_latest_videos():
    """Récupère les vidéos depuis YouTube et retourne un DataFrame."""

    print("Étape 1/2 (Mise à jour) : Récupération de la liste de toutes les vidéos...")
    try:
        with yt_dlp.YoutubeDL(cast("_Params", YDL_OPTS)) as ydl:
            playlist_infos = ydl.extract_info(url, download=False)
            video_entries = playlist_infos.get("entries", [])
            total_videos_global = len(video_entries)
            videos = []
            skipped_entries = 0

            for v in video_entries:
                if not isinstance(v, dict):
                    skipped_entries += 1
                    continue

                date = extract_video_datetime(v)

                videos.append(
                    {
                        "titre": v.get("title"),
                        # "description": v.get("description"),
                        "date": v.get("upload_date"),
                        "date_epoch": v.get("epoch"),
                        "date_epoch_fr": timestamp2fr(v.get("epoch")),
                        "date_available_at": v.get("available_at"),
                        "date_available_at_fr": timestamp2fr(v.get("available_at")),
                        "date_timestamp": v.get("timestamp"),
                        "date_timestamp_fr": timestamp2fr(v.get("timestamp")),
                        "date_upload_date": v.get("upload_date"),
                        "date_upload_date_fr": format_date(v.get("upload_date")),
                        "date_fr": format_date(date),
                        "duration": v.get("duration"),
                        "duree": format_duration(v.get("duration")),
                        "url": v.get("webpage_url"),
                        "vues": v.get("view_count"),
                        "likes": v.get("like_count"),
                    }
                )

            print(
                f"{total_videos_global} vidéo{'s' if total_videos_global>1 else ''} trouvées dans la playlist de {AUTHOR}"
            )
            if skipped_entries:
                print(
                    f"{skipped_entries} entrée(s) ignorée(s) (vidéo indisponible / erreur récupérable)."
                )
            return videos, True

    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des vidéos: {e}")
        return None, False

    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     info = ydl.extract_info(url, download=False)
    # print(f"{len(info.get('entries', []))} vidéo(s) récupérée(s).")
    # exit()
    # return create_videos_dataset(info)


def pluralize_fr(value, singular, plural=None):
    """Retourne le mot au singulier/pluriel selon la valeur."""
    if plural is None:
        plural = singular + "s"
    return singular if value == 1 else plural


def format_remaining_time_fr(total_minutes):
    """Formate un délai en français: minutes ou heures + minutes."""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    parts = []

    if hours > 0:
        parts.append(f"{hours} {pluralize_fr(hours, 'heure')}")
    if minutes > 0:
        parts.append(f"{minutes} {pluralize_fr(minutes, 'minute')}")

    if not parts:
        return "0 minute"

    return " et ".join(parts)


def toSeeToBp(df):
    """Construit le markdown des videos et l'ecrit dans le dossier cache."""

    # print(f'{len(df) = }') # //2ar

    nb_videos = len(df)
    nb_videos_txt = str(nb_videos) + " video" + ("s" if len(df) > 1 else "")
    total_duration = 777

    # stats = df.agg({"duration": ["min", "max", "mean", 'sum']})
    # print(stats)
    # print(stats.at['sum', 'duration'])
    total_duration = format_remaining_time_fr(df["duration"].sum() // 60)
    # print(total_duration)

    md = ""
    md = "# BP Learning - Vidéos à voir\n\n"
    md += f"## Auteur **[{AUTHOR}]({url})** ({nb_videos_txt} - {total_duration})\n\n"
    print(md)

    for _, row in df.iterrows():
        md += (
            "* [ ] ["
            + f"{row['date_fr']} **{row['titre']}** {row['vues']} **{row['duree']}**"
            + "]("
            + row["url"]
            + ")\n"
        )

    cache_dir = os.path.dirname(CACHE_FILE)
    os.makedirs(cache_dir, exist_ok=True)
    output_file = os.path.join(cache_dir, f"{AUTHOR}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Fichier markdown généré : {output_file}")
    return md


def videos_to_see():
    """Fonction principale pour obtenir la liste des vidéos sous forme de DataFrame."""
    cache_entry = get_valid_cache_entry(CACHE_FILE, CACHE_TTL)
    if cache_entry is not None:
        cached = cache_entry["videos"]
        cache_date = cache_entry.get("timestamp_fr")
        remaining_minutes = cache_entry["remaining_minutes"]
        print("Données chargées du cache.")
        if cache_date:
            remaining_text = format_remaining_time_fr(remaining_minutes)
            print(
                f"Dernière mise à jour du cache : {cache_date} (Prochaine dans environ {CYAN}{remaining_text}{R})"
            )
        return pd.DataFrame(cached)

    try:
        latest, ok = fetch_latest_videos()
        if not ok or latest is None:
            return None

        write_videos_cache(CACHE_FILE, latest, timestamp_formatter=timestamp2fr)

        # df = df.sort_values("upload_date", ascending=False) Si necessaire

        return pd.DataFrame(latest)

    except Exception as e:
        print(f"Erreur lors de la récupération des vidéos : {e}")
        return None

    # analyze_dataset(df)
    return df

    # analyze_dataset(df)
    return df


def test_heure(minutes=123):
    print(format_remaining_time_fr(minutes))


if __name__ == "__main__":

    # cls()

    # Obtenir et trier le dataset
    df = videos_to_see()

    md = toSeeToBp(df)

    # Afficher le tableau
    # zzzdisplay_videos_table(df)

    end()

# ❌ dans cache/json, timestamp, mais aussi en date lisi
