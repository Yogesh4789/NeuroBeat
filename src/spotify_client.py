from __future__ import annotations

import os
from typing import Dict, List


def is_spotify_configured() -> bool:
    return bool(os.getenv("SPOTIPY_CLIENT_ID") and os.getenv("SPOTIPY_CLIENT_SECRET"))


def _get_spotify_client():
    if not is_spotify_configured():
        return None

    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials

        auth_manager = SpotifyClientCredentials()
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception:
        return None


def fetch_spotify_recommendations(
    target_profile: Dict[str, object],
    limit: int = 5,
) -> List[Dict[str, object]]:
    client = _get_spotify_client()
    if client is None:
        return []

    genre_seeds = [genre for genre in target_profile.get("genres", []) if genre]
    seed_genres = genre_seeds[: min(5, len(genre_seeds))] or ["pop"]

    try:
        response = client.recommendations(
            seed_genres=seed_genres,
            limit=limit,
            target_energy=float(target_profile["energy"]),
            target_valence=float(target_profile["valence"]),
            target_tempo=float(target_profile["tempo"]),
        )
    except Exception:
        return []

    results = []
    for track in response.get("tracks", []):
        artists = ", ".join(artist["name"] for artist in track.get("artists", []))
        results.append(
            {
                "track_name": track.get("name", "Unknown Track"),
                "artist": artists or "Unknown Artist",
                "genre": ",".join(seed_genres),
                "tempo": target_profile["tempo"],
                "energy": target_profile["energy"],
                "valence": target_profile["valence"],
                "instrumentalness": target_profile["instrumentalness"],
                "score": 1.0,
                "reason": "Recommended from Spotify using the fused mood profile.",
                "source": "spotify",
                "url": track.get("external_urls", {}).get("spotify", ""),
            }
        )
    return results
