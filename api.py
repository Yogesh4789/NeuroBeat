from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.pipeline import run_pipeline


app = FastAPI(
    title="NeuroBeat API",
    description="Emotion-aware mood-to-music recommendation API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    time_of_day: Optional[str] = "evening"
    activity: Optional[str] = "relaxing"
    weather: Optional[str] = "cloudy"
    use_spotify: bool = False


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "app": "NeuroBeat API",
        "status": "online",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/recommend")
def recommend_music(payload: RecommendationRequest):
    return run_pipeline(
        text=payload.text,
        time_of_day=payload.time_of_day,
        activity=payload.activity,
        weather=payload.weather,
        use_spotify=payload.use_spotify,
    )
