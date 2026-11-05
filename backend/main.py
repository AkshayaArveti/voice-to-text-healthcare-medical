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
DIARIZATION_MODEL = os.getenv("DIARIZATION_MODEL", "pyannote/speaker-diarization-community-1")
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
if not HF_TOKEN:
    try:
        from huggingface_hub import get_token

        HF_TOKEN = get_token() or ""
    except Exception:
        HF_TOKEN = ""
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
_diarization_pipeline: Any = None


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "engine": "mlx-whisper",
        "model": MODEL,
        "device": "Apple Silicon (MLX)",
        "audio_storage": "temporary; deleted after each request",
        "speaker_diarization": "configured" if HF_TOKEN else "needs_optional_huggingface_token",
        "diarization_model": DIARIZATION_MODEL,
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


def _diarize(path: str) -> list[dict[str, Any]]:
    """Return anonymous speaker turns. Role names must be verified by a person."""
    global _diarization_pipeline
    if not HF_TOKEN:
        return []
    if _diarization_pipeline is None:
        import torch
        from pyannote.audio import Pipeline

        _diarization_pipeline = Pipeline.from_pretrained(DIARIZATION_MODEL, token=HF_TOKEN)
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        _diarization_pipeline.to(torch.device(device))
    output = _diarization_pipeline(path)
    annotation = getattr(output, "exclusive_speaker_diarization", None)
    if annotation is None:
        annotation = output.speaker_diarization
    return [
        {"start": round(turn.start, 3), "end": round(turn.end, 3), "speaker": str(speaker)}
        for turn, _, speaker in annotation.itertracks(yield_label=True)
    ]


def _attach_speakers(segments: list[dict[str, Any]], turns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach the anonymous speaker with the most time overlap to each ASR segment."""
    attached = []
    for segment in segments:
        start, end = segment.get("start"), segment.get("end")
        best_speaker, best_overlap = None, 0.0
        if isinstance(start, (float, int)) and isinstance(end, (float, int)):
            for turn in turns:
                overlap = max(0.0, min(end, turn["end"]) - max(start, turn["start"]))
                if overlap > best_overlap:
                    best_overlap, best_speaker = overlap, turn["speaker"]
        attached.append({**segment, "speaker": best_speaker})
    return attached


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
            }
            for segment in result.get("segments", [])
        ]
        diarization_status = "disabled_no_huggingface_token"
        diarization_error = None
        speaker_turns: list[dict[str, Any]] = []
        if HF_TOKEN:
            try:
                speaker_turns = await run_in_threadpool(_diarize, temp_path)
                segments = _attach_speakers(segments, speaker_turns)
                diarization_status = "available_review_roles"
            except Exception as exc:
                # Preserve the ASR result if optional diarization setup or inference fails.
                diarization_status = "failed"
                diarization_error = str(exc)[:240]
        return {
            "transcript": text,
            "detected_language": result.get("language", LANGUAGE_CODES.get(language, "unknown")),
            "model": MODEL,
            "segments": segments,
            "speaker_turns": speaker_turns,
            "speakers": sorted({turn["speaker"] for turn in speaker_turns}),
            "diarization_status": diarization_status,
            "diarization_error": diarization_error,
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
