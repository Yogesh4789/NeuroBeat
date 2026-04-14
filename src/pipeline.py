from __future__ import annotations

from typing import Dict, Optional

from models.emotion_model import detect_emotion
from src.context_fusion import build_target_profile
from src.recommender import load_song_data, recommend_tracks
from src.spotify_client import fetch_spotify_recommendations


SONG_DATA_PATH = "data/songs.csv"


def run_pipeline(
    text: str,
    time_of_day: Optional[str] = None,
    activity: Optional[str] = None,
    weather: Optional[str] = None,
    use_spotify: bool = False,
) -> Dict[str, object]:
    emotion, confidence, top_emotions, model_used = detect_emotion(text)
    target_profile = build_target_profile(
        emotion=emotion,
        time_of_day=time_of_day,
        activity=activity,
        weather=weather,
    )

    songs_df = load_song_data(SONG_DATA_PATH)
    context = {
        "time_of_day": time_of_day,
        "activity": activity,
        "weather": weather,
    }
    recommendations = []
    recommendation_source = "local"

    if use_spotify:
        recommendations = fetch_spotify_recommendations(
            target_profile=target_profile,
            limit=5,
        )
        if recommendations:
            recommendation_source = "spotify"

    if not recommendations:
        recommendations = recommend_tracks(
            songs_df=songs_df,
            emotion=emotion,
            target_profile=target_profile,
            context=context,
        )

    return {
        "emotion": emotion,
        "confidence": confidence,
        "top_emotions": top_emotions,
        "model_used": model_used,
        "target_profile": target_profile,
        "recommendations": recommendations,
        "recommendation_source": recommendation_source,
    }
