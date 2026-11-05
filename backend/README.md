# Local transcription backend

This is the dashboard's local `POST /api/transcribe` service. It runs OpenAI Whisper `large-v3-turbo` through Apple's MLX implementation on Apple Silicon. It uses no paid API. The model is downloaded from Hugging Face the first time it is used; later runs use the local model cache.

## Requirements

- Apple Silicon Mac (M1/M2/M3/M4) and macOS
- Python 3.11 or 3.12
- Homebrew `ffmpeg`
- Internet for the first model download

The dashboard workspace reports Python 3.14, which is not the Python version to use for this environment. MLX wheels are version-sensitive; use Python 3.12.

## Start it

From the project root:

```bash
brew install ffmpeg
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The API docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The first transcription downloads the model and can take a while. Keep the server terminal open while using the dashboard.

## API

`POST /api/transcribe` accepts multipart fields:

- `audio`: an audio file (up to 100 MB by default)
- `language`: `auto`, `Arabic`, `Bengali`, `Malayalam`, `Urdu`, or `English`

The JSON response includes `transcript`, detected language code, timestamped text segments, and explicit review/diarization status. Temporary uploaded audio is deleted after the request. Change `MAX_AUDIO_MB` or `WHISPER_MODEL` in the environment before starting if needed.

## Scope and limitations

- Language selection guides Whisper; `auto` asks it to detect the language.
- Whisper returns transcript segments, not validated doctor/patient/nurse identities. `speaker` is `null` and `diarization_status` is `not_configured`; do not infer speaker roles from this output.
- This endpoint does not generate a clinical report. The existing report workflow requires a transcript and speaker roles verified by a fluent human reviewer; its draft model output is not clinically validated.
- Transcription quality must be measured against fluent-verified references. This backend does not claim clinical accuracy.
- The service binds to localhost by default, so it is intended for use on this computer, not as a publicly exposed server.
