from __future__ import annotations

from copy import deepcopy
from typing import Dict, Optional


EMOTION_PROFILE_MAP = {
    "happy": {
        "tempo": 124,
        "energy": 0.82,
        "valence": 0.9,
        "instrumentalness": 0.12,
        "genres": ["pop", "indie", "dance"],
    },
    "sad": {
        "tempo": 74,
        "energy": 0.28,
        "valence": 0.24,
        "instrumentalness": 0.56,
        "genres": ["acoustic", "piano", "indie"],
    },
    "angry": {
        "tempo": 136,
        "energy": 0.88,
        "valence": 0.34,
        "instrumentalness": 0.08,
        "genres": ["rock", "rap", "edm"],
    },
    "calm": {
        "tempo": 66,
        "energy": 0.2,
        "valence": 0.56,
        "instrumentalness": 0.86,
        "genres": ["ambient", "lofi", "classical", "meditation"],
    },
    "stress": {
        "tempo": 68,
        "energy": 0.24,
        "valence": 0.42,
        "instrumentalness": 0.8,
        "genres": ["lofi", "ambient", "acoustic", "meditation"],
    },
    "excited": {
        "tempo": 140,
        "energy": 0.95,
        "valence": 0.88,
        "instrumentalness": 0.05,
        "genres": ["edm", "dance", "workout", "pop"],
    },
}


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(value, max_value))


def build_target_profile(
    emotion: str,
    time_of_day: Optional[str] = None,
    activity: Optional[str] = None,
    weather: Optional[str] = None,
) -> Dict[str, object]:
    profile = deepcopy(EMOTION_PROFILE_MAP.get(emotion, EMOTION_PROFILE_MAP["calm"]))

    if time_of_day == "morning":
        profile["valence"] += 0.05
        profile["tempo"] += 6
    elif time_of_day == "night":
        profile["energy"] -= 0.08
        profile["tempo"] -= 10
        profile["instrumentalness"] += 0.05

    if activity == "studying":
        profile["energy"] -= 0.08
        profile["instrumentalness"] += 0.18
        profile["genres"] = ["lofi", "classical", "ambient", "piano"]
    elif activity == "working":
        profile["tempo"] += 4
        profile["instrumentalness"] += 0.12
        profile["genres"] = ["lofi", "ambient", "indie", "classical"]
    elif activity == "relaxing":
        profile["energy"] -= 0.05
        profile["tempo"] -= 6
        profile["instrumentalness"] += 0.08
    elif activity == "workout":
        profile["energy"] += 0.18
        profile["tempo"] += 14
        profile["instrumentalness"] -= 0.08
        profile["genres"] = ["workout", "edm", "rock", "dance"]
    elif activity == "commuting":
        profile["tempo"] += 8
        profile["energy"] += 0.05
    elif activity == "sleeping":
        profile["energy"] = 0.08
        profile["tempo"] = 52
        profile["instrumentalness"] = 0.95
        profile["genres"] = ["ambient", "meditation", "classical"]

    if weather == "rainy":
        profile["tempo"] -= 4
        profile["valence"] -= 0.04
        if "acoustic" not in profile["genres"]:
            profile["genres"].append("acoustic")
    elif weather == "sunny":
        profile["valence"] += 0.07
        profile["energy"] += 0.04
    elif weather == "cloudy":
        profile["tempo"] -= 2
    elif weather == "cool":
        profile["instrumentalness"] += 0.03

    profile["energy"] = _clamp(profile["energy"])
    profile["valence"] = _clamp(profile["valence"])
    profile["instrumentalness"] = _clamp(profile["instrumentalness"])
    profile["tempo"] = max(45, min(profile["tempo"], 170))
    return profile
