import json
import os
import time
from typing import Any, Callable, Optional, TypedDict


class ValidCacheEntry(TypedDict):
    videos: list[Any]
    timestamp: float
    timestamp_fr: Optional[str]
    remaining_minutes: int


def read_cache_payload(cache_file: str) -> Optional[dict[str, Any]]:
    """Lit le JSON du cache et retourne son contenu brut."""
    if not os.path.isfile(cache_file):
        return None

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def extract_cache_videos(data: dict[str, Any]) -> Any:
    """Normalise la structure des videos selon les formats de cache rencontres."""
    videos = data.get("videos") or data.get("version")

    # Compat: ancien bug de serialisation -> [[...], true]
    if (
        isinstance(videos, list)
        and len(videos) == 2
        and isinstance(videos[1], bool)
        and isinstance(videos[0], list)
    ):
        videos = videos[0]

    return videos


def get_valid_cache_entry(cache_file: str, cache_ttl: int) -> Optional[ValidCacheEntry]:
    """Retourne une entree cache valide (non expiree) avec metadonnees utiles."""
    data = read_cache_payload(cache_file)
    if not data:
        return None

    timestamp = data.get("timestamp")
    if not isinstance(timestamp, (int, float)):
        return None

    if time.time() - timestamp >= cache_ttl:
        return None

    remaining_seconds = max(0, int(cache_ttl - (time.time() - timestamp)))
    remaining_minutes = max(1, (remaining_seconds + 59) // 60)

    videos = extract_cache_videos(data)
    if not isinstance(videos, list):
        return None

    timestamp_fr = data.get("timestamp_fr")
    if timestamp_fr is not None and not isinstance(timestamp_fr, str):
        timestamp_fr = str(timestamp_fr)

    return {
        "videos": videos,
        "timestamp": float(timestamp),
        "timestamp_fr": timestamp_fr,
        "remaining_minutes": remaining_minutes,
    }


def write_videos_cache(
    cache_file: str,
    videos: list[Any],
    timestamp_formatter: Optional[Callable[[float], str]] = None,
) -> bool:
    """Ecrit un cache videos avec timestamp brut et timestamp formate optionnel."""
    try:
        now_ts = time.time()
        payload: dict[str, Any] = {
            "videos": videos,
            "timestamp": now_ts,
        }

        if timestamp_formatter is not None:
            payload["timestamp_fr"] = timestamp_formatter(now_ts)

        cache_dir = os.path.dirname(cache_file)
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return True
    except Exception:
        return False
