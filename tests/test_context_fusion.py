from src.context_fusion import build_target_profile


def test_workout_context_pushes_energy_up():
    profile = build_target_profile(
        emotion="happy",
        time_of_day="morning",
        activity="workout",
        weather="sunny",
    )

    assert profile["energy"] > 0.9
    assert profile["tempo"] >= 138


def test_sleeping_context_pushes_toward_low_tempo():
    profile = build_target_profile(
        emotion="excited",
        time_of_day="night",
        activity="sleeping",
        weather="cool",
    )

    assert profile["tempo"] <= 60
    assert profile["instrumentalness"] >= 0.95
