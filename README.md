# Voice to Text — Healthcare Medical

A multilingual medical speech-to-text research project for Arabic, Bengali, Malayalam, and Urdu. The current dataset contains four synthetic ElevenLabs consultation recordings, one per language.

## Current project state

- Audio metadata and ASR drafts have been collected for the four language samples.
- ASR candidates were compared in Colab: WhisperX large-v3-turbo and SeamlessM4T v2 Large. Script-family percentages are diagnostic only; they are not word or medical accuracy scores.
- Diarization output is anonymous and speaker roles have not been verified by listeners.
- The fine-tuned clinical report extractor produced unsupported details in a spot check. Its reports are experimental and must not be used as final clinical outputs.
- Colab currently reports that free GPU allocation is unavailable, so the Qwen3-4B follow-up comparison has not run.
- The dashboard is connected to a local FastAPI backend at `POST /api/transcribe`. On Apple Silicon, it uses MLX Whisper large-v3-turbo and makes no paid API calls. Optional pyannote Community-1 diarization can provide anonymous speaker IDs; a human must verify speaker roles. See `backend/README.md` for setup. Clinical report generation remains a separate, guarded workflow.

## Open the dashboard

Start the backend following `backend/README.md`, then open `http://127.0.0.1:8000`. The selected audio is processed locally only after **Transcribe audio** is clicked.

## Project files

- `outputs/dashboard/index.html` — upload, preview, transcript editing, and download interface.
- `outputs/TASK_4_Stage_1_ASR_Diarization.ipynb` — Colab audio transcription and diarization workflow.
- `outputs/TASK_4_Clinical_Report_Generation_Guarded.ipynb` — guarded bilingual report-generation workflow.
- `outputs/*_summary.md`, `outputs/*_report.md` — run notes, review findings, and current limitations.
- `outputs/*template*` and review CSVs — transcript, speaker-role, and reference-verification templates.
- `outputs/final_adapter.zip` — recovered Task 3 LoRA adapter files.

## Data and validation notes

The source audio files are not included in this repository; only their metadata and model-generated draft outputs are included. Dataset manifest paths are stored as filenames so they do not disclose the original computer's directory structure. Reference transcripts and speaker-role labels remain unverified. Do not claim clinically accurate output until fluent reviewers validate transcripts, roles, medical terms, medication names, and numbers.
