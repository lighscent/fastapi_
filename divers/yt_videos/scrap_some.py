from datetime import datetime
import json
import locale
import os
import time
from pymox_kit import *

import yt_dlp


locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

# AUTHOR = "Gravenilvectuto"  # 174 videos - 49 heures et 39 minutes
AUTHOR = "LionelCOTE"
AUTHOR = "KevinDegila"

URL = f"https://www.youtube.com/@{AUTHOR}/videos"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(SCRIPT_DIR, "cache")
OUTPUT_FILE = os.path.join(STORAGE_DIR, f".{AUTHOR}_videos_scrap_some.json")

YDL_OPTS_LIST = {
    "extract_flat": True,
    "quiet": False,
    "ignoreerrors": True,
    "retries": 2,
    "extractor_retries": 2,
}

YDL_OPTS_DETAIL = {
    "extract_flat": False,
    "quiet": False,
    "progress": True,  # Afficher une barre de progression
    "ignoreerrors": True,
    "retries": 3,
    "extractor_retries": 3,
}


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


def write_result(videos, der_id, total_playlist):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    now_ts = time.time()
    scrapees = len(videos)
    payload = {
        "videos": videos,
        "url": URL,
        "timestamp": now_ts,
        "timestamp_fr": timestamp2fr(now_ts),
        "scrapees": scrapees,
        "total_playlist": total_playlist,
        "der_id": der_id,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def read_previous_result():
    if not os.path.isfile(OUTPUT_FILE):
        return [], None

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        videos = data.get("videos") if isinstance(data.get("videos"), list) else []
        der_id = data.get("der_id") if isinstance(data.get("der_id"), str) else None
        return videos, der_id
    except Exception:
        return [], None


def get_simulated_failure_position(existing_scrapees):
    """Retourne la position globale de panne simulée selon l'avancement."""
    if existing_scrapees < 2:
        return 3
    if existing_scrapees < 5:
        return 6
    return None


def scrap_some():
    print(f"SCRAP des vidéos de {AUTHOR}\n{URL}")

    videos, start_after_id = read_previous_result()
    existing_ids = {v.get("id") for v in videos if isinstance(v, dict) and v.get("id")}
    # existing_scrapees = len(videos)
    # simulated_failure_position = get_simulated_failure_position(existing_scrapees)
    # simulated_failure_position = None  # Simulation désactivée
    der_id = start_after_id
    total_playlist = None

    if start_after_id:
        print(
            f"État précédent détecté (der_id={start_after_id}). Vérification complète des IDs pour combler les trous."
        )
    else:
        print("Aucun état précédent trouvé, démarrage depuis la première vidéo.")

    # if simulated_failure_position is not None:
    #     print(
    #         f"Panne simulée configurée sur la vidéo globale #{simulated_failure_position}."
    #     )
    # else:
    #     print("Aucune panne simulée: ce run doit aller jusqu'au bout.")

    try:
        with yt_dlp.YoutubeDL(YDL_OPTS_LIST) as ydl_list:
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
        missing_in_cache = [video_id for video_id in playlist_ids if video_id not in existing_ids]

        if missing_in_cache:
            print(
                f"{YELLOW}{len(missing_in_cache)} vidéo(s) absente(s) du cache seront (re)téléchargées.{R}"
            )
        else:
            print("Aucun trou détecté dans le cache pour les IDs connus de la playlist.")

        with yt_dlp.YoutubeDL(YDL_OPTS_DETAIL) as ydl_detail:
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

                video_detail = ydl_detail.extract_info(video_url, download=False)
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

        # der_id doit rester le dernier ID de la playlist (pas le dernier ajouté),
        # pour conserver une métadonnée stable même en mode rattrapage de trous.
        if playlist_ids:
            der_id = playlist_ids[-1]

    except Exception as e:
        print(f"Scrap interrompu: {e}")

    videos = sorted(videos, key=video_sort_key, reverse=True)
    write_result(videos=videos, der_id=der_id, total_playlist=total_playlist)
    scrapees = len(videos)
    complete = (
        isinstance(total_playlist, int) and total_playlist == scrapees
    )
    print(f"Fichier JSON écrit: {OUTPUT_FILE}")
    print(f"scrapees={scrapees}, total_playlist={total_playlist}, complete={complete}")
    print(f"der_id={der_id}")


if __name__ == "__main__":
    scrap_some()
