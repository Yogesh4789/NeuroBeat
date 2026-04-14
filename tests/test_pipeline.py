from src.pipeline import run_pipeline


def test_pipeline_returns_local_recommendations():
    result = run_pipeline(
        text="I feel drained and stressed after work",
        time_of_day="evening",
        activity="relaxing",
        weather="rainy",
        use_spotify=False,
    )

    assert result["emotion"] in {"stress", "sad", "calm", "angry", "happy", "excited"}
    assert result["recommendation_source"] == "local"
    assert len(result["recommendations"]) == 5
