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

## Optional speaker diarization

Whisper does not identify speakers. To get anonymous speaker IDs and timestamps, install the optional open-source pyannote pipeline:

```bash
python -m pip install -r backend/requirements-diarization.txt
```

Accept the access conditions for `pyannote/speaker-diarization-community-1` on Hugging Face, then log in locally with `hf auth login` using a read token. The backend will use the saved Hugging Face login automatically. Or set a token in the same Terminal before starting the server:

```bash
export HF_TOKEN='hf_your_token_here'
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The token only authorizes model downloads; inference runs locally. Do not paste a real token into project files or commit it. The API matches audio turns to transcript segments and returns anonymous labels such as `SPEAKER_00`. Listen to the audio and manually verify which speaker is the doctor, patient, or nurse; the model cannot assign those roles reliably. If this optional setup fails, transcription still returns.

## API

`POST /api/transcribe` accepts multipart fields:

- `audio`: an audio file (up to 100 MB by default)
- `language`: `auto`, `Arabic`, `Bengali`, `Malayalam`, `Urdu`, or `English`

The JSON response includes `transcript`, detected language code, timestamped text segments, and explicit review/diarization status. Temporary uploaded audio is deleted after the request. Change `MAX_AUDIO_MB` or `WHISPER_MODEL` in the environment before starting if needed.

## Scope and limitations

- Language selection guides Whisper; `auto` asks it to detect the language.
- Whisper returns transcript segments. Optional pyannote diarization can add anonymous speaker IDs, but it does not identify doctor/patient/nurse roles; a person must verify role labels by listening.
- This endpoint does not generate a clinical report. The existing report workflow requires a transcript and speaker roles verified by a fluent human reviewer; its draft model output is not clinically validated.
- Transcription quality must be measured against fluent-verified references. This backend does not claim clinical accuracy.
- The service binds to localhost by default, so it is intended for use on this computer, not as a publicly exposed server.
