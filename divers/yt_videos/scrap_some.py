from datetime import datetime
from importlib import import_module
import json
import locale
import os
import time
from typing import TYPE_CHECKING, TypedDict, cast
from pymox_kit import *

import yt_dlp
from yt_dlp.utils import DownloadError


locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

if TYPE_CHECKING:
    from yt_dlp.YoutubeDL import _Params

# Pour mise au point du script
# AUTHOR = "doro2255"  # 1 seule vidéo (7')
# AUTHOR = "LionelCOTE"  # Pour mise au point car peu de vidéos (~12 - 1H30)
# AUTHOR = "c57-u5s"  # 16 videos - 11 heures et 23 minutes
# AUTHOR = "Alphorm"  # ❌ Limiteur necessaire
# AUTHOR = "tseries"  # ❌ rès gros volume, limiter les requêtes

# Initiation à Python (Bases)
# AUTHOR = "Gravenilvectuto"  # 174 videos - 49 heures et 39 minutes
# AUTHOR = "CodeAvecJonathan"  # 10 videos - 15 heures et 16 minutes
# AUTHOR = "hassanbahi"  # ❌ 843 vidéos

# Python approfondi
# AUTHOR = "donaldprogrammeur"  # ❌ Des bases à DevOps (424 vidéos)

# Python pour l'IA
# AUTHOR = "KevinDegila"  # 262 videos - 53 heures et 38 minutes
# AUTHOR = "InformatiqueSansComplexe" ❌ 
# AUTHOR = "MachineLearnia"❌

# AUTHOR = "tseries"
AUTHOR = "KevinDegila"

URL = f"https://www.youtube.com/@{AUTHOR}/videos"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(SCRIPT_DIR, "cache")
OUTPUT_FILE = os.path.join(STORAGE_DIR, f".{AUTHOR}_videos_scrap_some.json")
OUTPUT_MD_FILE = os.path.join(STORAGE_DIR, f"{AUTHOR}.md")
CACHE_TTL = 3600  # 3600 = 1 heure - 86400 = 1 jour

_cache_utils_module = import_module(
    f"{__package__}.cache_utils" if __package__ else "cache_utils"
)
get_valid_cache_entry = _cache_utils_module.get_valid_cache_entry


class YdlOpts(TypedDict, total=False):
    extract_flat: bool
    quiet: bool
    ignoreerrors: bool
    retries: int
    extractor_retries: int
    progress: bool
    check_formats: bool


YDL_OPTS_LIST: YdlOpts = {
    "extract_flat": True,
    "quiet": False,
    "ignoreerrors": True,
    "retries": 2,
    "extractor_retries": 2,
}

YDL_OPTS_DETAIL: YdlOpts = {
    "extract_flat": False,
    "quiet": False,
    "progress": True,  # Afficher une barre de progression
    "ignoreerrors": True,
    "retries": 3,
    "extractor_retries": 3,
    "check_formats": False,
}

MAX_CUMULATED_403_ERRORS = 7


def is_http_403_error(exc):
    msg = str(exc).lower()
    return "403" in msg and ("http error" in msg or "forbidden" in msg)


def timestamp2fr(ts: float) -> str:
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def format_duration(seconds):
    if seconds is None:
        return "N/A"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)

    if hours == 0:
        return f"{minutes:02d}:{remaining_seconds:02d}"
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def format_date(date):
    if date is None:
        return "N/A"
    try:
        return date.strftime("%d/%m/%Y")
    except Exception:
        return "N/A"


def extract_video_datetime(video):
    upload_date = video.get("upload_date")
    if upload_date:
        try:
            return datetime.strptime(upload_date, "%Y%m%d")
        except (ValueError, TypeError):
            pass

    for key in ("timestamp", "release_timestamp", "available_at"):
        ts = video.get(key)
        if ts:
            try:
                return datetime.fromtimestamp(ts)
            except (ValueError, OSError, TypeError):
                continue

    return None


def build_video_payload(v):
    date = extract_video_datetime(v)
    return {
        "id": v.get("id"),
        "titre": v.get("title"),
        "date": v.get("upload_date"),
        "date_fr": format_date(date),
        "duration": v.get("duration"),
        "duree": format_duration(v.get("duration")),
        "url": v.get("webpage_url"),
        "vues": v.get("view_count"),
        "likes": v.get("like_count"),
    }


def video_sort_key(video):
    """Clé de tri des vidéos par date de parution (plus récente d'abord)."""
    if not isinstance(video, dict):
        return datetime.min

    date_str = video.get("date")
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            pass

    date_fr = video.get("date_fr")
    if isinstance(date_fr, str):
        try:
            return datetime.strptime(date_fr, "%d/%m/%Y")
        except ValueError:
            pass

    return datetime.min


def pluralize_fr(value, singular, plural=None):
    if plural is None:
        plural = singular + "s"
    return singular if value == 1 else plural


def format_remaining_time_fr(total_minutes):
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


def write_markdown(videos):
    if not isinstance(videos, list):
        return

    total_duration_seconds = sum(
        int(v.get("duration") or 0) for v in videos if isinstance(v, dict)
    )
    total_duration_txt = format_remaining_time_fr(total_duration_seconds // 60)
    nb_videos_txt = f"**{len(videos)}** video{'s' if len(videos) > 1 else ''}"

    md = "# BP Learning - Vidéos à voir\n\n"
    md += (
        f"## Auteur **[{AUTHOR}]({URL})** ( {nb_videos_txt} - {total_duration_txt} )\n\n"
    )

    for video in videos:
        if not isinstance(video, dict):
            continue

        titre = video.get("titre") or "N/A"
        vues = video.get("vues") if isinstance(video.get("vues"), int) else 0
        duree = video.get("duree") or "N/A"
        date_fr = video.get("date_fr") or "N/A"
        url = video.get("url") or ""

        if not url:
            continue

        md += (
            "* [ ] [" + f"{date_fr} **{titre}** {vues} **{duree}**" + "](" + url + ")\n"
        )

    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(OUTPUT_MD_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Fichier markdown généré : {OUTPUT_MD_FILE}")


def write_result(videos, total_playlist):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    now_ts = time.time()
    scraped = len(videos)
    payload = {
        "url": URL,
        "timestamp": now_ts,
        "timestamp_fr": timestamp2fr(now_ts),
        "scraped": scraped,
        "total_playlist": total_playlist,
        "videos": videos,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def read_previous_result():
    if not os.path.isfile(OUTPUT_FILE):
        return []

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        videos = data.get("videos") if isinstance(data.get("videos"), list) else []
        return videos
    except Exception:
        return []


def read_previous_counts():
    """Retourne les compteurs du dernier JSON pour savoir si le cache est complet."""
    if not os.path.isfile(OUTPUT_FILE):
        return None, None

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        scraped = data.get("scraped") if isinstance(data.get("scraped"), int) else None
        total_playlist = (
            data.get("total_playlist")
            if isinstance(data.get("total_playlist"), int)
            else None
        )
        return scraped, total_playlist
    except Exception:
        return None, None


def get_simulated_failure_position(existing_scraped):
    """Retourne la position globale de panne simulée selon l'avancement."""
    if existing_scraped < 2:
        return 3
    if existing_scraped < 5:
        return 6
    return None


def scrap_some():
    print(f"SCRAP des vidéos de {AUTHOR}\n{URL}")

    cache_entry = get_valid_cache_entry(OUTPUT_FILE, CACHE_TTL)
    if cache_entry is not None:
        cached_videos = cache_entry.get("videos")
        cache_date = cache_entry.get("timestamp_fr")
        remaining_minutes = cache_entry.get("remaining_minutes")
        scraped, total_playlist = read_previous_counts()
        cache_is_complete = (
            isinstance(scraped, int)
            and isinstance(total_playlist, int)
            and scraped >= total_playlist
        )

        if isinstance(scraped, int) and isinstance(total_playlist, int) and not cache_is_complete:
            print(
                f"Cache valide mais incomplet ({scraped}/{total_playlist}) : reprise du scraping pour combler les trous."
            )

        if isinstance(cached_videos, list):
            cached_videos = sorted(cached_videos, key=video_sort_key, reverse=True)
            if cache_is_complete:
                print("Données chargées depuis le cache JSON (valide 1h).")
                if cache_date and isinstance(remaining_minutes, int):
                    remaining_txt = format_remaining_time_fr(remaining_minutes)
                    print(
                        f"Dernière mise à jour: {cache_date} (prochaine actualisation dans environ {CYAN}{remaining_txt}{R})."
                    )
                write_markdown(cached_videos)
                return

    videos = read_previous_result()
    existing_ids = {v.get("id") for v in videos if isinstance(v, dict) and v.get("id")}
    # existing_scraped = len(videos)
    # simulated_failure_position = get_simulated_failure_position(existing_scraped)
    # simulated_failure_position = None  # Simulation désactivée
    total_playlist = None
    cumulated_403_errors = 0

    if videos:
        print("État précédent détecté. Vérification complète des IDs pour combler les trous.")
    else:
        print("Aucun état précédent trouvé, démarrage depuis la première vidéo.")

    # if simulated_failure_position is not None:
    #     print(
    #         f"Panne simulée configurée sur la vidéo globale #{simulated_failure_position}."
    #     )
    # else:
    #     print("Aucune panne simulée: ce run doit aller jusqu'au bout.")

    try:
        with yt_dlp.YoutubeDL(cast("_Params", YDL_OPTS_LIST)) as ydl_list:
            playlist_infos = ydl_list.extract_info(URL, download=False)
            entries = playlist_infos.get("entries", [])

        total_videos = playlist_infos.get("playlist_count")
        total_playlist = total_videos if isinstance(total_videos, int) else None
        total_videos_txt = (
            str(total_videos)
            if isinstance(total_videos, int)
            else f"Nombre inconnu (au moins {len(entries)}) de"
        )
        print(f"{RED}{total_videos_txt} vidéos{R} trouvées dans la playlist.")
        total_entries = len(entries)
        run_processed = 0
        playlist_ids = [
            e.get("id")
            for e in entries
            if isinstance(e, dict) and isinstance(e.get("id"), str)
        ]
        missing_in_cache = [
            video_id for video_id in playlist_ids if video_id not in existing_ids
        ]

        if missing_in_cache:
            print(
                f"{YELLOW}{len(missing_in_cache)} vidéo(s) absente(s) du cache seront (re)téléchargées.{R}"
            )
        else:
            print(
                "Aucun trou détecté dans le cache pour les IDs connus de la playlist."
            )

        with yt_dlp.YoutubeDL(cast("_Params", YDL_OPTS_DETAIL)) as ydl_detail:
            for idx, entry in enumerate(entries, start=1):
                if not isinstance(entry, dict):
                    continue

                current_id = entry.get("id")

                # On saute immédiatement les vidéos déjà présentes dans le cache.
                if isinstance(current_id, str) and current_id in existing_ids:
                    continue

                # Panne simulée progressive: 3e puis 6e, puis plus de panne.
                # if simulated_failure_position is not None and idx == simulated_failure_position:
                #     raise RuntimeError(
                #         f"Erreur simulée sur la vidéo globale #{simulated_failure_position}"
                #     )

                video_url = entry.get("url") or entry.get("webpage_url")
                if not video_url:
                    continue

                print(
                    f"{CYAN}[progress] Vidéo globale {SB}{idx} / {total_entries} - {round(100*idx/total_entries,1)} %{R} {CYAN}| Exécution n°{run_processed + 1}{R}"
                )

                try:
                    video_detail = ydl_detail.extract_info(video_url, download=False)
                except DownloadError as e:
                    if is_http_403_error(e):
                        cumulated_403_errors += 1
                        print(
                            f"{YELLOW}Erreur 403 cumulée {cumulated_403_errors}/{MAX_CUMULATED_403_ERRORS} sur {video_url}{R}"
                        )
                        if cumulated_403_errors >= MAX_CUMULATED_403_ERRORS:
                            print(
                                f"{RED}Seuil de 403 atteint ({MAX_CUMULATED_403_ERRORS}). Arrêt anticipé du scrap détail.{R}"
                            )
                            break
                        continue

                    print(f"Erreur yt-dlp ignorée sur {video_url}: {e}")
                    continue
                except Exception as e:
                    print(f"Erreur lors du détail pour {video_url}: {e}")
                    continue

                if not isinstance(video_detail, dict):
                    continue

                video = build_video_payload(video_detail)
                video_id = video.get("id")
                if video_id in existing_ids:
                    continue
                videos.append(video)
                if video_id:
                    existing_ids.add(video_id)
                run_processed += 1

    except Exception as e:
        print(f"Scrap interrompu: {e}")

    videos = sorted(videos, key=video_sort_key, reverse=True)
    write_result(videos=videos, total_playlist=total_playlist)
    write_markdown(videos)
    scraped = len(videos)
    complete = isinstance(total_playlist, int) and total_playlist == scraped
    print(f"Fichier JSON écrit: {OUTPUT_FILE}")
    print(f"scraped={scraped}, total_playlist={total_playlist}, complete={complete}")
    print(f"403 cumulées sur ce run: {cumulated_403_errors}")


if __name__ == "__main__":
    scrap_some()
