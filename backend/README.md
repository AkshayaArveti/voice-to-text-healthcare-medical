# Local transcription backend

This is the dashboard's local `POST /api/transcribe` service. It uses Whisper `large-v3-turbo` locally, preferring Apple's MLX implementation when Metal is available and falling back to OpenAI Whisper on CPU in headless sessions. It uses no paid API. The model is downloaded the first time it is used; later runs use the local model cache.

For non-English audio, the service also creates an English translation locally with OpenAI Whisper `small` to reduce download and CPU time. The original-language transcript still uses `large-v3-turbo`. The first translated request downloads the smaller model (about 0.5 GB); later requests reuse it. English audio is shown unchanged in both transcript panels. If translation cannot run, the source transcript is still returned. The dashboard lets you edit, copy, and download each transcript separately. The smaller translation model may be less accurate, especially for medical terms, so review the English against the recording.

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
python -m pip install -r backend/requirements.txt -r backend/requirements-diarization.txt -r backend/requirements-report.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

If launching from a managed/headless session where Metal is unavailable, prefix the server command with `ASR_BACKEND=cpu` to select CPU Whisper. This Codex session uses that setting. Leave the default `auto` in a normal Apple Silicon terminal to use MLX when Metal is available.

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

## Optional bilingual SOAP report generation

The guarded local report route uses the recovered **Qwen2.5-1.5B-Instruct LoRA adapter** already in `outputs/final_adapter.zip`. It loads the public full-precision Qwen base plus that adapter locally so it can run on Apple Silicon without bitsandbytes; it does not call a paid API. The adapter was originally prepared against an Unsloth 4-bit base, so this local loading path still needs a successful run and output validation. Install its optional packages:

```bash
python -m pip install -r backend/requirements-report.txt
```

Restart the server. In the dashboard, correct the transcript, replace anonymous speaker IDs with `[DOCTOR]`, `[PATIENT]`, and `[NURSE]`, enter the fluent reviewer's name, choose the conversation language, and affirm both review checkboxes. The endpoint rejects report requests unless the transcript is marked verified and all three role labels are present. It refuses to truncate an overlong input. The first run downloads the base model; allow several GB of free disk space and enough memory for a 1.5B model.

The endpoint returns English and source-language SOAP drafts, exact-quote evidence fields, token counts, and an explicit `draft_review_required` status. It flags evidence quotes that do not exactly match the transcript. These checks do not prove that every generated claim is correct. The LoRA has not been validated for this task, so a fluent reviewer must check both versions against the audio before use. If generation fails or produces invalid JSON, it returns no completed report.

## API

`POST /api/transcribe` accepts multipart fields:

- `audio`: an audio file (up to 100 MB by default)
- `language`: `auto`, `Arabic`, `Bengali`, `Malayalam`, `Urdu`, or `English`

The JSON response includes `transcript`, detected language code, timestamped text segments, and explicit review/diarization status. Temporary uploaded audio is deleted after the request. On MLX it uses `WHISPER_MODEL`; on CPU it uses the OpenAI checkpoint named by `OPENAI_WHISPER_MODEL` (default `large-v3-turbo`). Set `ASR_BACKEND=cpu` to force CPU mode, or leave it as `auto` to prefer MLX when Metal is available. CPU transcription is slower. Change the model names or `MAX_AUDIO_MB` in the environment before starting if needed.

`POST /api/report` accepts JSON fields `language`, `verified_transcript`, `transcript_status`, `transcript_reviewer`, and `speaker_roles_verified`. The report route accepts Arabic, Bengali, Malayalam, or Urdu and requires `[DOCTOR]`, `[PATIENT]`, and `[NURSE]` labels in the reviewed transcript.

## Scope and limitations

- Language selection guides Whisper; `auto` asks it to detect the language.
- Whisper returns transcript segments. Optional pyannote diarization can add anonymous speaker IDs, but it does not identify doctor/patient/nurse roles; a person must verify role labels by listening.
- The `/api/report` endpoint generates bilingual SOAP drafts only after transcript and speaker-role verification. Its Qwen adapter is experimental and outputs still need fluent and clinical review.
- Transcription quality must be measured against fluent-verified references. This backend does not claim clinical accuracy.
- The service binds to localhost by default, so it is intended for use on this computer, not as a publicly exposed server.
