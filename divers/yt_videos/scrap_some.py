from datetime import datetime
from importlib import import_module
import json, locale, os, sys, time
from typing import TYPE_CHECKING, TypedDict, cast

import yt_dlp
from yt_dlp.utils import DownloadError

# ❌ Compatibilité de PyMoX-Kit avec Linux (Cf. GH spaces)
from pymox_kit import *


# try:
#     from pymox_kit import cls, end
# except Exception:
#     # Fallback minimal si pymox_kit échoue (ex: locale fr_FR absente).
#     def cls():
#         import subprocess

#         try:
#             subprocess.run(["clear"], check=False)
#         except Exception:
#             print("\033[2J\033[H", end="")

# ❌ Loker ce qui n'a pas été refait ici et redonner le nom to_see à ce script

# ❌ ⚠️ Cf si locale marche en linux
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

if TYPE_CHECKING:
    from yt_dlp.YoutubeDL import _Params

# Pour mise au point du script
# AUTHOR = "doro2255"                 #   1 seule vidéo (7')
# AUTHOR = "LionelCOTE"               #  Pour mise au point car peu de vidéos (12 - 1H27)
# AUTHOR = "c57-u5s"                  #  16 videos - 11 heures et 23 minutes
# AUTHOR = "Alphorm"                  # Extrême  - 4064 videos - 665 heures et 3 minutes - Diverses notions liées à l'informatique
AUTHOR = "tseries"                  # Top Extrême - 23 458 vidéos - ❌ - Compte qui génère le + de gains au Monde avec YT !

# Initiation à Python (Bases)
# AUTHOR = "CodeAvecJonathan"         #  10 videos -  15 heures et 16 minutes
# AUTHOR = "Gravenilvectuto"          # 174 videos -  49 heures et 39 minutes
# AUTHOR = "hassanbahi"               # 843 vidéos - 191 heures et 13 minutes - Top pour comprendre super bien les bases - Attention: Pas mal de vidéos + anciennes avec le langage C, mais facielement adaptable... D'ailleurs, c 1 super exo ;-) !

# Python approfondi
# AUTHOR = "donaldprogrammeur"        # Des bases à DevOps (424 vidéos - 303 heures et 56 minutes)


# Python - FastAPI

# AUTHOR = "DataAvecJB"               # Les bases
AUTHOR = "bandedecodeurs"           # Les bases
AUTHOR = "MasteringAI-q9g"          # Les bases


# Python pour l'IA
# AUTHOR = "KevinDegila"              # 262 videos - 53 heures et 38 minutes
# AUTHOR = "InformatiqueSansComplexe" # 284 videos - 33 heures et 8 minutes
# AUTHOR = "MachineLearnia"           #  65 videos - 22 heures et 53 minutes

# AUTHOR = "doro2255"                 #   1 seule vidéo (7') # Garde fou !

if "AUTHOR" not in globals():
    sys.exit(f"{RED}AUTHOR n'est pas défini. Arrêt du script.{R}")


URL = f"https://www.youtube.com/@{AUTHOR}/videos"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(SCRIPT_DIR, "cache")
# OUTPUT_FILE = os.path.join(
#     STORAGE_DIR, f".{AUTHOR}_videos.json"
# )  # ❌ Simplify file name author_videos.json
OUTPUT_FILE = os.path.join(
    STORAGE_DIR, f".{AUTHOR}_videos_scrap_some.json"
)  # 2ar
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
    logger: object


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
PAUSE_ON_RATE_LIMIT = 5  # secondes d'attente avant reprise automatique
MAX_STALL_RETRIES = 3  # passes sans progression avant arrêt définitif
TOTAL_PLAYLIST_DROP_GUARD_RATIO = 0.03  # 3%


def is_counted_ytdlp_error(exc):
    msg = str(exc).lower()
    is_403 = "403" in msg and ("http error" in msg or "forbidden" in msg)
    is_rate_limited = (
        "rate-limited" in msg
        or "rate limited" in msg
        or "current session has been rate-limited" in msg
        or "this content isn't available, try again later" in msg
    )
    return is_403 or is_rate_limited


class CountedErrorTracker:
    """Compteur d'erreurs 403/rate-limit avec anti double-comptage immédiat."""

    def __init__(self, threshold):
        self.threshold = threshold
        self.count = 0
        self.total_count = 0
        self.stop_requested = False
        self._last_signature = None

    def increment(self, message, url=None, source="logger"):
        signature = (str(message).strip().lower(), str(url or ""), source)
        if signature == self._last_signature:
            return
        self._last_signature = signature

        self.count += 1
        self.total_count += 1
        print(
            f"{YELLOW}Erreur cumulée (403/rate-limit) {self.count}/{self.threshold} [{source}] {url or ''}{R}"
        )
        if self.count >= self.threshold:
            self.stop_requested = True

    def reset(self):
        """Remet le compteur de passe à zéro (total_count conservé)."""
        self.count = 0
        self.stop_requested = False
        self._last_signature = None

    def progress_suffix(self):
        return f"| {YELLOW}403/rate-limit : {self.count}/{self.threshold}{R}"


class YtDlpCountedErrorLogger:
    """Logger yt-dlp: relaie les logs et compte les erreurs ciblées."""

    def __init__(self, tracker):
        self.tracker = tracker

    def _handle(self, msg, level):
        text = str(msg)
        print(text)
        if is_counted_ytdlp_error(text):
            self.tracker.increment(text, source=f"log:{level}")

    def debug(self, msg):
        self._handle(msg, "debug")

    def info(self, msg):
        self._handle(msg, "info")

    def warning(self, msg):
        self._handle(msg, "warning")

    def error(self, msg):
        self._handle(msg, "error")


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


def write_markdown(videos, total_playlist=None):
    if not isinstance(videos, list):
        return

    total_duration_seconds = sum(
        int(v.get("duration") or 0) for v in videos if isinstance(v, dict)
    )
    total_duration_txt = format_remaining_time_fr(total_duration_seconds // 60)
    nb_videos_txt = f"**{len(videos)}** video{'s' if len(videos) > 1 else ''}"

    md = "# BP Learning - Vidéos à voir\n\n"
    partiel_txt1 = ""
    partiel_txt2 = ""
    if isinstance(total_playlist, int) and len(videos) < total_playlist:
        partiel_txt1 = f" ⚠️ PARTIEL → "
        partiel_txt2 = f"/ **{total_playlist}** "

    md += f"## Auteur **[{AUTHOR}]({URL})** ({partiel_txt1} {nb_videos_txt} {partiel_txt2}- {total_duration_txt} )\n\n"

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
    print(f"SCRAP des vidéos de {SB}{AUTHOR}{R}\n{URL}")

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

        if (
            isinstance(scraped, int)
            and isinstance(total_playlist, int)
            and not cache_is_complete
        ):
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
                print("Markdown non regénéré (cache TTL valide).")
                return

    videos = read_previous_result()
    initial_video_count = len(videos)
    existing_ids = {v.get("id") for v in videos if isinstance(v, dict) and v.get("id")}
    # existing_scraped = len(videos)
    # simulated_failure_position = get_simulated_failure_position(existing_scraped)
    # simulated_failure_position = None  # Simulation désactivée
    _, total_playlist = (
        read_previous_counts()
    )  # récupère total connu pour la vérification de complétude
    previous_total_playlist = total_playlist
    error_tracker = CountedErrorTracker(MAX_CUMULATED_403_ERRORS)

    if videos:
        print(
            "État précédent détecté. Vérification complète des IDs pour combler les trous."
        )
    else:
        print("Aucun état précédent trouvé, démarrage depuis la première vidéo.")

    # if simulated_failure_position is not None:
    #     print(
    #         f"Panne simulée configurée sur la vidéo globale #{simulated_failure_position}."
    #     )
    # else:
    #     print("Aucune panne simulée: ce run doit aller jusqu'au bout.")

    stall_retries = 0
    scraped_before_pass = len(videos)

    def log_threshold_pause_message():
        print(
            f"{RED}Seuil d'erreurs 403/rate-limit atteint ({MAX_CUMULATED_403_ERRORS}). Pause {PAUSE_ON_RATE_LIMIT}s puis reprise...{R}"
        )

    def handle_detail_exception(exc, video_url, fallback_prefix):
        if is_counted_ytdlp_error(exc):
            error_tracker.increment(str(exc), url=video_url, source="exception")
            if error_tracker.stop_requested:
                log_threshold_pause_message()
                return True
            return False

        print(f"{fallback_prefix} {video_url}: {exc}")
        return False

    while True:
        # ── Vérification complétude avant chaque passe ──────────────────────
        if isinstance(total_playlist, int) and len(videos) >= total_playlist:
            break

        try:
            with yt_dlp.YoutubeDL(cast("_Params", YDL_OPTS_LIST)) as ydl_list:
                playlist_infos = ydl_list.extract_info(URL, download=False)
                entries = playlist_infos.get("entries", [])

            total_videos = playlist_infos.get("playlist_count")
            detected_total_playlist = (
                total_videos if isinstance(total_videos, int) else None
            )

            if isinstance(detected_total_playlist, int):
                total_playlist = detected_total_playlist
                if (
                    isinstance(previous_total_playlist, int)
                    and previous_total_playlist > 0
                    and detected_total_playlist < previous_total_playlist
                ):
                    drop_ratio = (
                        previous_total_playlist - detected_total_playlist
                    ) / previous_total_playlist
                    if drop_ratio > TOTAL_PLAYLIST_DROP_GUARD_RATIO:
                        print(
                            f"{YELLOW}Protection total_playlist: nouveau total détecté {detected_total_playlist} inférieur de {drop_ratio * 100:.2f}% à l'ancien {previous_total_playlist}. Ancienne valeur conservée dans le JSON.{R}"
                        )
                        total_playlist = previous_total_playlist
            else:
                total_playlist = None

            total_videos_txt = (
                str(total_videos)
                if isinstance(total_videos, int)
                else f"Nombre inconnu (au moins {len(entries)}) de"
            )
            print(f"{RED}{total_videos_txt} vidéo(s){R} trouvée(s) dans la playlist.")
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
                break

            ydl_opts_detail = dict(YDL_OPTS_DETAIL)
            ydl_opts_detail["logger"] = YtDlpCountedErrorLogger(error_tracker)

            with yt_dlp.YoutubeDL(cast("_Params", ydl_opts_detail)) as ydl_detail:
                for idx, entry in enumerate(entries, start=1):
                    if error_tracker.stop_requested:
                        log_threshold_pause_message()
                        break

                    if not isinstance(entry, dict):
                        continue

                    current_id = entry.get("id")

                    # On saute immédiatement les vidéos déjà présentes dans le cache.
                    if isinstance(current_id, str) and current_id in existing_ids:
                        continue

                    video_url = entry.get("url") or entry.get("webpage_url")
                    if not video_url:
                        continue

                    print(
                        f"{CYAN}[progress] Vidéo globale {SB}{idx} / {total_entries} - {round(100*idx/total_entries,1)} %{R} {CYAN}| Exécutées : {SB}{run_processed} ( {(run_processed) / len(missing_in_cache) * 100:.1f} % ) {R}{error_tracker.progress_suffix()}"
                    )

                    try:
                        video_detail = ydl_detail.extract_info(
                            video_url, download=False
                        )
                    except DownloadError as e:
                        if handle_detail_exception(
                            e, video_url, "Erreur yt-dlp ignorée sur"
                        ):
                            break
                        continue
                    except Exception as e:
                        if handle_detail_exception(
                            e, video_url, "Erreur lors du détail pour"
                        ):
                            break
                        continue

                    if error_tracker.stop_requested:
                        log_threshold_pause_message()
                        break

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

        # ── Fin de passe: décider si on continue, on pause, ou on abandonne ──
        scraped_now = len(videos)

        if not error_tracker.stop_requested:
            # Passe terminée normalement sans atteindre le seuil: on sort.
            break

        # Détection de stall: pas de progression sur cette passe
        if scraped_now <= scraped_before_pass:
            stall_retries += 1
            print(
                f"{RED}Aucune progression détectée (passe #{stall_retries}/{MAX_STALL_RETRIES}).{R}"
            )
            if stall_retries >= MAX_STALL_RETRIES:
                print(
                    f"{RED}Abandon définitif après {MAX_STALL_RETRIES} passes sans progression.{R}"
                )
                break
        else:
            stall_retries = 0

        scraped_before_pass = scraped_now
        error_tracker.reset()
        # Sauvegarde de la progression avant la pause (persistance entre passes)
        write_result(
            videos=sorted(videos, key=video_sort_key, reverse=True),
            total_playlist=total_playlist,
        )
        write_markdown(
            sorted(videos, key=video_sort_key, reverse=True),
            total_playlist=total_playlist,
        )
        print(f"JSON intermédiaire écrit ({scraped_now} vidéos).")
        print(
            f"{YELLOW}Pause {PAUSE_ON_RATE_LIMIT}s avant reprise (scraped={scraped_now}, total={total_playlist})...{R}"
        )
        # exit() # Pour tests sans attendre et redémarrer auto
        time.sleep(PAUSE_ON_RATE_LIMIT)

    videos = sorted(videos, key=video_sort_key, reverse=True)
    write_result(videos=videos, total_playlist=total_playlist)
    if len(videos) != initial_video_count:
        write_markdown(videos, total_playlist=total_playlist)
    else:
        print("Markdown non regénéré (aucun changement détecté).")
    scraped = len(videos)
    complete = isinstance(total_playlist, int) and total_playlist == scraped
    print(f"Fichier JSON écrit: {OUTPUT_FILE}")
    print(f"scraped={scraped}, total_playlist={total_playlist}, complete={complete}")
    print(
        f"Erreurs cumulées (403/rate-limit) total toutes passes: {error_tracker.total_count}"
    )
    print(f"Fin du scrap des vidéos de {SB}{AUTHOR}{R}.")


if __name__ == "__main__":
    scrap_some()
