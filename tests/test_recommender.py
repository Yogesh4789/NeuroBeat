import pandas as pd

from src.recommender import recommend_tracks


def test_recommend_tracks_returns_ranked_results():
    songs_df = pd.DataFrame(
        [
            {
                "track_name": "Calm One",
                "artist": "A",
                "genre": "ambient",
                "tempo": 60,
                "energy": 0.2,
                "valence": 0.5,
                "instrumentalness": 0.9,
            },
            {
                "track_name": "Workout One",
                "artist": "B",
                "genre": "workout",
                "tempo": 145,
                "energy": 0.95,
                "valence": 0.88,
                "instrumentalness": 0.05,
            },
        ]
    )

    target = {
        "tempo": 62,
        "energy": 0.22,
        "valence": 0.52,
        "instrumentalness": 0.88,
        "genres": ["ambient"],
    }

    results = recommend_tracks(
        songs_df=songs_df,
        emotion="calm",
        target_profile=target,
        context={"time_of_day": "night", "activity": "relaxing", "weather": "cloudy"},
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["track_name"] == "Calm One"
    assert "calm" in results[0]["reason"]
