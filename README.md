# Emotion-Aware Mood-to-Music Recommendation

A mini-project that detects emotion from user text, fuses lightweight context signals, and recommends matching music tracks in real time.

## Features

- Text-based emotion detection with optional transformer model
- Context-aware recommendation using time, activity, and weather
- Explainable song recommendations
- Responsive Streamlit UI for real-time interaction
- FastAPI backend for API-style usage
- Optional Spotify recommendations when credentials are configured
- Local CSV song catalog for offline demo usage
- Docker support for straightforward deployment

## Project Structure

```text
NeuroBeat/
|-- app.py
|-- api.py
|-- requirements.txt
|-- README.md
|-- data/
|   `-- songs.csv
|-- models/
|   `-- emotion_model.py
`-- src/
    |-- context_fusion.py
    |-- pipeline.py
    |-- recommender.py
    `-- spotify_client.py
```

## Run

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Launch the app:

```powershell
streamlit run app.py
```

3. Optional API server:

```powershell
uvicorn api:app --reload
```

4. Run tests:

```powershell
pytest
```

## Deploy

For Streamlit-style deployment:

```powershell
streamlit run app.py
```

For Docker:

```powershell
docker build -t neurobeat .
docker run -p 8501:8501 neurobeat
```

## Optional Spotify Setup

Set these environment variables if you want Spotify-based recommendations:

```powershell
$env:SPOTIPY_CLIENT_ID="your_client_id"
$env:SPOTIPY_CLIENT_SECRET="your_client_secret"
```

Without these values, the project automatically falls back to the local CSV catalog.

## Notes

- The app works with a keyword-based fallback model by default.
- To enable the transformer model explicitly, set `NEUROBEAT_ENABLE_TRANSFORMER=1`.
- Spotify support is optional and non-blocking.
- The API docs are available at `/docs` when the FastAPI server is running.
