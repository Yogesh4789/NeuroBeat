from __future__ import annotations

import os
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


TRANSFORMER_MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

LABEL_MAP = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "stress",
    "surprise": "excited",
    "neutral": "calm",
    "disgust": "angry",
}

KEYWORD_LEXICON: Dict[str, List[str]] = {
    "happy": ["happy", "great", "good", "joy", "cheerful", "smile", "glad", "content"],
    "sad": ["sad", "down", "lonely", "empty", "upset", "cry", "heartbroken", "low"],
    "angry": ["angry", "mad", "furious", "annoyed", "frustrated", "irritated", "rage"],
    "calm": ["calm", "peaceful", "quiet", "relaxed", "steady", "balanced", "gentle"],
    "stress": ["stress", "stressed", "overwhelmed", "anxious", "tense", "worried", "tired", "drained"],
    "excited": ["excited", "thrilled", "hyped", "energetic", "pumped", "eager", "motivated"],
}

_classifier = None


def _load_transformer():
    global _classifier
    if _classifier is not None:
        return _classifier

    if os.getenv("NEUROBEAT_ENABLE_TRANSFORMER", "0") != "1":
        return None

    try:
        from transformers import pipeline

        _classifier = pipeline(
            "text-classification",
            model=TRANSFORMER_MODEL_NAME,
            top_k=None,
            local_files_only=True,
        )
    except Exception:
        _classifier = None

    return _classifier


def _keyword_detect(text: str) -> Tuple[str, float, List[dict], str]:
    lowered = text.lower()
    counts = Counter()

    for emotion, keywords in KEYWORD_LEXICON.items():
        for keyword in keywords:
            if keyword in lowered:
                counts[emotion] += 1

    if not counts:
        return "calm", 0.45, [{"label": "calm", "score": 0.45}], "keyword"

    emotion, matches = counts.most_common(1)[0]
    total_matches = sum(counts.values())
    confidence = min(0.55 + (matches / max(total_matches, 1)) * 0.35, 0.92)

    ranked = [
        {"label": label, "score": round(count / total_matches, 3)}
        for label, count in counts.most_common(3)
    ]
    return emotion, round(confidence, 3), ranked, "keyword"


def detect_emotion(text: str) -> Tuple[str, float, List[dict], str]:
    classifier = _load_transformer()
    if classifier is not None:
        try:
            predictions = classifier(text)[0]
            aggregated = defaultdict(float)
            for item in predictions:
                project_label = LABEL_MAP.get(item["label"].lower(), "calm")
                aggregated[project_label] += float(item["score"])

            normalized = [
                {"label": label, "score": score}
                for label, score in aggregated.items()
            ]

            normalized.sort(key=lambda x: x["score"], reverse=True)
            top = normalized[0]
            return top["label"], round(top["score"], 3), normalized[:3], "transformer"
        except Exception:
            pass

    return _keyword_detect(text)
