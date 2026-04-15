from __future__ import annotations

import os
from typing import Dict, List
import requests
from dotenv import load_dotenv

# Load constants from .env file
load_dotenv()


def is_soundcloud_configured() -> bool:
    return bool(os.getenv("SOUNDCLOUD_CLIENT_ID"))


def fetch_soundcloud_recommendations(
    target_profile: Dict[str, object],
    languages: List[str] = None,
    limit: int = 5,
) -> List[Dict[str, object]]:
    """
    Fetch recommendations from SoundCloud API.
    SoundCloud doesn't natively support querying by target_energy or target_tempo,
    so we query by genre and format the results similarly.
    """
    client_id = os.getenv("SOUNDCLOUD_CLIENT_ID")
    if not client_id:
        return []

    genre_seeds = [genre for genre in target_profile.get("genres", []) if genre]
    seed_genre = genre_seeds[0] if genre_seeds else "pop"
    
    q_str = seed_genre
    if languages:
        q_str = f"{seed_genre} {' '.join(languages)}"

    try:
        url = "https://api-v2.soundcloud.com/search/tracks"
        params = {
            "q": q_str,
            "client_id": client_id,
            "limit": limit
        }
        # Many SoundCloud endpoints are closed or require v2 API endpoints.
        # This uses the v2 endpoint. You can extract a client_id via browser inspection.
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return []

    results = []
    for track in data.get("collection", []):
        if "title" not in track:
            continue
            
        artist_name = track.get("user", {}).get("username", "Unknown Artist")
        track_url = track.get("permalink_url", "")
        
        results.append(
            {
                "track_name": track.get("title", "Unknown Track"),
                "artist": artist_name,
                "genre": seed_genre,
                "tempo": target_profile.get("tempo", 120),
                "energy": target_profile.get("energy", 0.5),
                "valence": target_profile.get("valence", 0.5),
                "instrumentalness": target_profile.get("instrumentalness", 0.0),
                "score": 1.0,  # Placeholder score
                "reason": f"Recommended from SoundCloud based on the {seed_genre} genre constraint.",
                "source": "soundcloud",
                "url": track_url,
            }
        )
        
    return results
