"""Local, no-paid-API speech recognition backend for the project dashboard."""

from __future__ import annotations

import os
import json
import importlib.util
import subprocess
import threading
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "outputs" / "dashboard"
MODEL = os.getenv("WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")
OPENAI_WHISPER_MODEL = os.getenv("OPENAI_WHISPER_MODEL", "large-v3-turbo")
WHISPER_TRANSLATION_MODEL = os.getenv("WHISPER_TRANSLATION_MODEL", "large-v3")
ASR_BACKEND = os.getenv("ASR_BACKEND", "auto").strip().lower()
REPORT_BASE_MODEL = os.getenv("REPORT_BASE_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
REPORT_ADAPTER = os.getenv("REPORT_ADAPTER", str(ROOT / "outputs" / "final_adapter.zip"))
REPORT_MAX_INPUT_TOKENS = int(os.getenv("REPORT_MAX_INPUT_TOKENS", "2048"))
REPORT_MAX_NEW_TOKENS = int(os.getenv("REPORT_MAX_NEW_TOKENS", "768"))
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
_openai_whisper_model: Any = None
_translation_whisper_model: Any = None
_asr_engine: str | None = None
_asr_model_id: str | None = None
_report_model: Any = None
_report_tokenizer: Any = None
_report_device: str | None = None
_report_lock = threading.Lock()

REPORT_LANGUAGES = {"Arabic", "Bengali", "Malayalam", "Urdu"}
SOAP_FIELDS = ("S", "O", "A", "P")


class ReportRequest(BaseModel):
    language: str
    verified_transcript: str = Field(min_length=1, max_length=30000)
    transcript_status: str
    transcript_reviewer: str = Field(min_length=2, max_length=120)
    speaker_roles_verified: bool


@app.get("/api/health")
def health() -> dict[str, Any]:
    report_deps_installed = all(importlib.util.find_spec(package) for package in ("torch", "transformers", "peft"))
    return {
        "status": "ok",
        "engine": _asr_engine or ("openai-whisper-cpu" if ASR_BACKEND == "cpu" else "MLX with local CPU fallback"),
        "model": _asr_model_id or (OPENAI_WHISPER_MODEL if ASR_BACKEND == "cpu" else {"mlx": MODEL, "cpu_fallback": OPENAI_WHISPER_MODEL}),
        "device": "CPU" if ASR_BACKEND == "cpu" else "Apple Metal when available; CPU fallback otherwise",
        "audio_storage": "temporary; deleted after each request",
        "speaker_diarization": "configured" if HF_TOKEN else "needs_optional_huggingface_token",
        "diarization_model": DIARIZATION_MODEL,
        "report_model": REPORT_BASE_MODEL,
        "report_generation": (
            "adapter_not_found" if not Path(REPORT_ADAPTER).exists()
            else "ready_to_load" if report_deps_installed
            else "optional_install_required"
        ),
    }


def _transcribe(path: str, language_code: str | None) -> dict[str, Any]:
    global _openai_whisper_model, _asr_engine, _asr_model_id
    import torch

    if ASR_BACKEND != "cpu" and torch.backends.mps.is_available():
        try:
            import mlx_whisper

            options: dict[str, Any] = {
                "path_or_hf_repo": MODEL,
                "task": "transcribe",
                "word_timestamps": False,
                "condition_on_previous_text": False,
                "verbose": False,
            }
            if language_code:
                options["language"] = language_code
            result = mlx_whisper.transcribe(path, **options)
            _asr_engine, _asr_model_id = "mlx-whisper", MODEL
            return result
        except (ImportError, RuntimeError):
            # If MLX is unavailable despite MPS support, continue with CPU Whisper.
            pass

    # Headless sessions without Metal use the same checkpoint through CPU PyTorch.
    import whisper

    if _openai_whisper_model is None:
        _openai_whisper_model = whisper.load_model(OPENAI_WHISPER_MODEL, device="cpu")
    options = {
        "task": "transcribe",
        "fp16": False,
        "condition_on_previous_text": False,
        "verbose": False,
    }
    if language_code:
        options["language"] = language_code
    result = _openai_whisper_model.transcribe(path, **options)
    _asr_engine, _asr_model_id = "openai-whisper-cpu", OPENAI_WHISPER_MODEL
    return result


def _translate_to_english(path: str, language_code: str | None) -> dict[str, Any]:
    """Translate non-English speech to English with a multilingual Whisper checkpoint."""
    global _translation_whisper_model
    import whisper

    if _translation_whisper_model is None:
        _translation_whisper_model = whisper.load_model(WHISPER_TRANSLATION_MODEL, device="cpu")
    options: dict[str, Any] = {
        "task": "translate",
        "fp16": False,
        "condition_on_previous_text": False,
        "verbose": False,
    }
    if language_code:
        options["language"] = language_code
    return _translation_whisper_model.transcribe(path, **options)


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
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix="healthcare-diarization-", suffix=".wav", delete=False) as wav_file:
            wav_path = wav_file.name
        # Re-encode compressed uploads: some MP3 decoders return a slightly
        # different sample count than pyannote expects from container metadata.
        subprocess.run(
            ["ffmpeg", "-y", "-i", path, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", wav_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        # This project’s consultation script has three voices (doctor, patient,
        # nurse). Pyannote IDs remain anonymous; people must review role labels.
        output = _diarization_pipeline(wav_path, num_speakers=3)
        annotation = getattr(output, "exclusive_speaker_diarization", None)
        if annotation is None:
            annotation = output.speaker_diarization
        return [
            {"start": round(turn.start, 3), "end": round(turn.end, 3), "speaker": str(speaker)}
            for turn, _, speaker in annotation.itertracks(yield_label=True)
        ]
    finally:
        if wav_path:
            Path(wav_path).unlink(missing_ok=True)


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


def _resolve_adapter_path() -> Path:
    adapter_path = Path(REPORT_ADAPTER).expanduser()
    if adapter_path.is_dir():
        return adapter_path
    if not adapter_path.is_file() or adapter_path.suffix.lower() != ".zip":
        raise FileNotFoundError(f"Qwen adapter not found: {adapter_path}")
    destination = Path(tempfile.gettempdir()) / "healthcare-stt-qwen-adapter"
    configs = list(destination.rglob("adapter_config.json")) if destination.exists() else []
    if configs and (configs[0].parent / "adapter_model.safetensors").is_file():
        return configs[0].parent
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(adapter_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if destination.resolve() not in target.parents and target != destination.resolve():
                raise ValueError("Unsafe path found in adapter archive.")
        archive.extractall(destination)
    configs = list(destination.rglob("adapter_config.json"))
    if not configs or not (configs[0].parent / "adapter_model.safetensors").is_file():
        raise FileNotFoundError("The adapter archive is missing adapter_config.json or adapter_model.safetensors.")
    return configs[0].parent


def _load_report_model() -> tuple[Any, Any, str]:
    global _report_model, _report_tokenizer, _report_device
    if _report_model is not None and _report_tokenizer is not None and _report_device:
        return _report_model, _report_tokenizer, _report_device
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    adapter_path = _resolve_adapter_path()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if device == "mps" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(str(adapter_path), use_fast=True)
    base = AutoModelForCausalLM.from_pretrained(
        REPORT_BASE_MODEL,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(base, str(adapter_path), is_trainable=False)
    model.to(device)
    model.eval()
    _report_model, _report_tokenizer, _report_device = model, tokenizer, device
    return model, tokenizer, device


def _report_prompt(language: str, transcript: str) -> str:
    schema = {
        "english_soap": {field: "string" for field in SOAP_FIELDS},
        "source_language_soap": {field: f"string in {language}, using its native script" for field in SOAP_FIELDS},
        "source_evidence": {field: "short exact quote from the source transcript, or empty string" for field in SOAP_FIELDS},
    }
    return (
        "Format a human-verified consultation transcript as a draft SOAP summary. "
        "Use only facts explicitly present in the transcript. Do not infer diagnoses, medicines, doses, "
        "or advice. Attribute patient-reported facts to S, measurements and tests to O, clinician-stated "
        "assessment to A, and clinician-stated actions to P. If a section has no supported facts, write "
        "'Not stated' (or a faithful equivalent in the source language). If a fact is ambiguous, write "
        "'Unclear'; never guess. Both reports must contain the same facts. Keep each evidence value an exact "
        "verbatim source-language quote, or empty when no fact is stated. Output valid JSON only, exactly this schema: "
        f"{json.dumps(schema, ensure_ascii=False)}\n"
        f"Verified source language: {language}\nVerified transcript:\n{transcript}"
    )


def _generate_report(language: str, transcript: str) -> dict[str, Any]:
    import torch

    with _report_lock:
        model, tokenizer, device = _load_report_model()
        messages = [{"role": "user", "content": _report_prompt(language, transcript)}]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        encoded = tokenizer(prompt, return_tensors="pt", truncation=False)
        input_tokens = int(encoded["input_ids"].shape[-1])
        if input_tokens > REPORT_MAX_INPUT_TOKENS:
            raise ValueError(
                f"Transcript needs {input_tokens} tokens, exceeding the {REPORT_MAX_INPUT_TOKENS}-token limit; it was not truncated."
            )
        encoded = {name: value.to(device) for name, value in encoded.items()}
        with torch.inference_mode():
            generated = model.generate(
                **encoded,
                max_new_tokens=REPORT_MAX_NEW_TOKENS,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        raw = tokenizer.decode(generated[0, input_tokens:], skip_special_tokens=True).strip()
        output_tokens = int(generated.shape[-1] - input_tokens)
        del encoded, generated

    try:
        parsed = json.loads(raw)
        expected_top = {"english_soap", "source_language_soap", "source_evidence"}
        expected_inner = set(SOAP_FIELDS)
        schema_valid = (
            isinstance(parsed, dict)
            and set(parsed) == expected_top
            and all(isinstance(parsed[key], dict) and set(parsed[key]) == expected_inner for key in expected_top)
            and all(isinstance(parsed[key][field], str) for key in expected_top for field in expected_inner)
        )
        if not schema_valid:
            return {"status": "invalid_schema_review_required", "raw_output": raw, "input_tokens": input_tokens, "output_tokens": output_tokens}
        evidence_mismatches = [
            field for field, quote in parsed["source_evidence"].items()
            if quote and quote not in transcript
        ]
        return {
            "status": "draft_review_required",
            "english_soap": parsed["english_soap"],
            "source_language_soap": parsed["source_language_soap"],
            "source_evidence": parsed["source_evidence"],
            "evidence_mismatches": evidence_mismatches,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }
    except json.JSONDecodeError:
        return {"status": "invalid_json_review_required", "raw_output": raw, "input_tokens": input_tokens, "output_tokens": output_tokens}


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

        detected_language = result.get("language", LANGUAGE_CODES.get(language, "unknown"))

        segments = [
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "text": str(segment.get("text", "")).strip(),
            }
            for segment in result.get("segments", [])
        ]
        english_transcript = ""
        english_segments: list[dict[str, Any]] = []
        translation_status = "failed"
        translation_error = None
        if detected_language == "en":
            english_transcript = text
            english_segments = [dict(segment) for segment in segments]
            translation_status = "source_is_english"
        else:
            try:
                translation_result = await run_in_threadpool(
                    _translate_to_english,
                    temp_path,
                    detected_language,
                )
                english_transcript = str(translation_result.get("text", "")).strip()
                english_segments = [
                    {
                        "start": segment.get("start"),
                        "end": segment.get("end"),
                        "text": str(segment.get("text", "")).strip(),
                    }
                    for segment in translation_result.get("segments", [])
                ]
                translation_status = "available" if english_transcript else "failed"
            except Exception as exc:
                # Keep the source-language transcript if optional translation fails.
                translation_error = str(exc)[:240]

        diarization_status = "disabled_no_huggingface_token"
        diarization_error = None
        speaker_turns: list[dict[str, Any]] = []
        if HF_TOKEN:
            try:
                speaker_turns = await run_in_threadpool(_diarize, temp_path)
                segments = _attach_speakers(segments, speaker_turns)
                english_segments = _attach_speakers(english_segments, speaker_turns)
                diarization_status = "available_review_roles"
            except Exception as exc:
                # Preserve the ASR result if optional diarization setup or inference fails.
                diarization_status = "failed"
                diarization_error = str(exc)[:240]
        return {
            "transcript": text,
            "detected_language": result.get("language", LANGUAGE_CODES.get(language, "unknown")),
            "model": _asr_model_id or MODEL,
            "segments": segments,
            "english_transcript": english_transcript,
            "english_segments": english_segments,
            "translation_model": WHISPER_TRANSLATION_MODEL if detected_language != "en" else None,
            "translation_status": translation_status,
            "translation_error": translation_error,
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


@app.post("/api/report")
async def generate_report(request: ReportRequest) -> dict[str, Any]:
    if request.language not in REPORT_LANGUAGES:
        raise HTTPException(status_code=422, detail="Report language must be Arabic, Bengali, Malayalam, or Urdu.")
    if request.transcript_status.strip().lower() != "verified":
        raise HTTPException(status_code=422, detail="A fluent human reviewer must verify the transcript before report generation.")
    if not request.transcript_reviewer.strip():
        raise HTTPException(status_code=422, detail="Enter the fluent transcript reviewer's name.")
    if not request.speaker_roles_verified:
        raise HTTPException(status_code=422, detail="Verify speaker roles by listening before report generation.")
    transcript = request.verified_transcript.strip()
    required_roles = ("[DOCTOR]", "[PATIENT]", "[NURSE]")
    missing_roles = [role for role in required_roles if role not in transcript.upper()]
    if missing_roles:
        raise HTTPException(
            status_code=422,
            detail=f"Add the verified role labels to the transcript before continuing: {', '.join(missing_roles)}.",
        )
    try:
        draft = await run_in_threadpool(_generate_report, request.language, transcript)
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="Report dependencies are not installed. Follow backend/README.md to install the optional report requirements.") from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"Qwen LoRA adapter unavailable: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Report generation failed ({type(exc).__name__}). No report was returned.") from exc
    return {
        **draft,
        "model": REPORT_BASE_MODEL,
        "adapter": Path(REPORT_ADAPTER).name,
        "language": request.language,
        "transcript_reviewer": request.transcript_reviewer.strip(),
        "verified_transcript": transcript,
        "clinical_use": "draft_only_human_review_required",
        "review_notice": "Check every fact, attribution, number, medicine, translation, and evidence quote against the audio and verified transcript.",
    }


if DASHBOARD.is_dir():
    app.mount("/dashboard", StaticFiles(directory=DASHBOARD), name="dashboard")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    index = DASHBOARD / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Dashboard files not found.")
    return FileResponse(index)
