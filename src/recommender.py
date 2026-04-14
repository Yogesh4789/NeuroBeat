from __future__ import annotations

from typing import Dict, List

import pandas as pd


def load_song_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def _normalized_gap(value: float, target: float, scale: float) -> float:
    return min(abs(value - target) / scale, 1.0)


def _context_bonus(song: pd.Series, context: Dict[str, str]) -> float:
    bonus = 0.0
    genre = str(song["genre"]).lower()

    activity = context.get("activity")
    time_of_day = context.get("time_of_day")
    weather = context.get("weather")

    if activity == "studying" and genre in {"lofi", "classical", "ambient", "piano"}:
        bonus += 0.08
    if activity == "workout" and song["energy"] >= 0.8:
        bonus += 0.08
    if activity == "relaxing" and song["tempo"] <= 85:
        bonus += 0.06
    if time_of_day == "night" and song["tempo"] <= 80:
        bonus += 0.05
    if time_of_day == "morning" and song["valence"] >= 0.75:
        bonus += 0.05
    if weather == "rainy" and genre in {"acoustic", "ambient", "indie", "piano"}:
        bonus += 0.04
    if weather == "sunny" and song["valence"] >= 0.8:
        bonus += 0.04

    return bonus


def score_song(song: pd.Series, target_profile: Dict[str, object], context: Dict[str, str]) -> float:
    energy_score = 1.0 - _normalized_gap(song["energy"], target_profile["energy"], 1.0)
    valence_score = 1.0 - _normalized_gap(song["valence"], target_profile["valence"], 1.0)
    tempo_score = 1.0 - _normalized_gap(song["tempo"], target_profile["tempo"], 100.0)
    instrumental_score = 1.0 - _normalized_gap(
        song["instrumentalness"], target_profile["instrumentalness"], 1.0
    )

    genre_bonus = 0.1 if str(song["genre"]).lower() in target_profile.get("genres", []) else 0.0
    context_bonus = _context_bonus(song, context)

    return round(
        0.35 * energy_score
        + 0.30 * valence_score
        + 0.20 * tempo_score
        + 0.15 * instrumental_score
        + genre_bonus
        + context_bonus,
        4,
    )


def build_explanation(
    emotion: str,
    song: pd.Series,
    context: Dict[str, str],
) -> str:
    parts = [f"detected emotion '{emotion}'"]

    if context.get("activity"):
        parts.append(f"activity '{context['activity']}'")
    if context.get("time_of_day"):
        parts.append(f"time '{context['time_of_day']}'")
    if context.get("weather"):
        parts.append(f"weather '{context['weather']}'")

    parts.append(
        f"song fit: tempo {int(song['tempo'])}, energy {song['energy']:.2f}, valence {song['valence']:.2f}"
    )
    return "Recommended because of " + ", ".join(parts) + "."


def _select_diverse_tracks(ranked: pd.DataFrame, top_k: int) -> pd.DataFrame:
    selected_rows = []
    seen_genres = set()

    for _, row in ranked.iterrows():
        genre = str(row["genre"]).lower()
        if genre not in seen_genres or len(selected_rows) + 2 >= top_k:
            selected_rows.append(row)
            seen_genres.add(genre)
        if len(selected_rows) == top_k:
            break

    if len(selected_rows) < top_k:
        selected_names = {row["track_name"] for row in selected_rows}
        for _, row in ranked.iterrows():
            if row["track_name"] in selected_names:
                continue
            selected_rows.append(row)
            if len(selected_rows) == top_k:
                break

    return pd.DataFrame(selected_rows)


def recommend_tracks(
    songs_df: pd.DataFrame,
    emotion: str,
    target_profile: Dict[str, object],
    context: Dict[str, str],
    top_k: int = 5,
) -> List[Dict[str, object]]:
    ranked = songs_df.copy()
    ranked["score"] = ranked.apply(
        lambda row: score_song(row, target_profile=target_profile, context=context),
        axis=1,
    )
    ranked = ranked.sort_values("score", ascending=False)
    ranked = _select_diverse_tracks(ranked, top_k=top_k)

    results = []
    for _, row in ranked.iterrows():
        item = row.to_dict()
        item["reason"] = build_explanation(emotion=emotion, song=row, context=context)
        results.append(item)
    return results
