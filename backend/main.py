"""Local, no-paid-API speech recognition backend for the project dashboard."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import mlx_whisper
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "outputs" / "dashboard"
MODEL = os.getenv("WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")
MAX_AUDIO_BYTES = int(os.getenv("MAX_AUDIO_MB", "100")) * 1024 * 1024
ALLOWED_SUFFIXES = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm", ".mp4", ".mpeg", ".mpga"}
LANGUAGE_CODES = {
    "Arabic": "ar",
    "Bengali": "bn",
    "Malayalam": "ml",
    "Urdu": "ur",
    "English": "en",
}

app = FastAPI(
    title="Voice to Text — Healthcare Medical",
    description="Local multilingual speech recognition. Audio stays on this computer.",
    version="1.0.0",
)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "engine": "mlx-whisper",
        "model": MODEL,
        "device": "Apple Silicon (MLX)",
        "audio_storage": "temporary; deleted after each request",
        "speaker_diarization": "not_configured",
    }


def _transcribe(path: str, language_code: str | None) -> dict[str, Any]:
    options: dict[str, Any] = {
        "path_or_hf_repo": MODEL,
        "task": "transcribe",
        "word_timestamps": False,
        "condition_on_previous_text": False,
        "verbose": False,
    }
    if language_code:
        options["language"] = language_code
    return mlx_whisper.transcribe(path, **options)


@app.post("/api/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = Form("auto"),
) -> dict[str, Any]:
    suffix = Path(audio.filename or "audio").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail="Unsupported audio type. Use MP3, WAV, M4A, FLAC, OGG, or WEBM.")
    if language != "auto" and language not in LANGUAGE_CODES:
        raise HTTPException(status_code=422, detail="Language must be auto, Arabic, Bengali, Malayalam, Urdu, or English.")

    temp_path: str | None = None
    size = 0
    try:
        with tempfile.NamedTemporaryFile(prefix="healthcare-stt-", suffix=suffix, delete=False) as temp:
            temp_path = temp.name
            while chunk := await audio.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_AUDIO_BYTES:
                    raise HTTPException(status_code=413, detail=f"Audio exceeds the {MAX_AUDIO_BYTES // (1024 * 1024)} MB upload limit.")
                temp.write(chunk)

        result = await run_in_threadpool(
            _transcribe,
            temp_path,
            LANGUAGE_CODES.get(language),
        )
        text = str(result.get("text", "")).strip()
        if not text:
            raise HTTPException(status_code=422, detail="No speech was recognized in this audio.")

        segments = [
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "text": str(segment.get("text", "")).strip(),
                "speaker": None,
            }
            for segment in result.get("segments", [])
        ]
        return {
            "transcript": text,
            "detected_language": result.get("language", LANGUAGE_CODES.get(language, "unknown")),
            "model": MODEL,
            "segments": segments,
            "speakers": [],
            "diarization_status": "not_configured",
            "review_required": True,
            "notice": "Automatic speech recognition can mishear medical terms, names, numbers, and speaker changes. Review against the audio.",
        }
    except HTTPException:
        raise
    except ImportError as exc:
        raise HTTPException(status_code=503, detail=f"Speech model dependencies are unavailable: {exc}") from exc
    except Exception as exc:
        message = str(exc)
        if "ffmpeg" in message.lower():
            message = "ffmpeg is missing. Install it with: brew install ffmpeg"
        elif "connection" in message.lower() or "download" in message.lower():
            message = f"Could not download/load model {MODEL}. Check internet access and try again."
        raise HTTPException(status_code=500, detail=message[:500]) from exc
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
        await audio.close()


if DASHBOARD.is_dir():
    app.mount("/dashboard", StaticFiles(directory=DASHBOARD), name="dashboard")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    index = DASHBOARD / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Dashboard files not found.")
    return FileResponse(index)
