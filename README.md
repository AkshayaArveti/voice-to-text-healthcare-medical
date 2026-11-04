# Voice to Text — Healthcare Medical

A multilingual medical speech-to-text research project for Arabic, Bengali, Malayalam, and Urdu. The current dataset contains four synthetic ElevenLabs consultation recordings, one per language.

## Current project state

- Audio metadata and ASR drafts have been collected for the four language samples.
- ASR candidates were compared in Colab: WhisperX large-v3-turbo and SeamlessM4T v2 Large. Script-family percentages are diagnostic only; they are not word or medical accuracy scores.
- Diarization output is anonymous and speaker roles have not been verified by listeners.
- The fine-tuned clinical report extractor produced unsupported details in a spot check. Its reports are experimental and must not be used as final clinical outputs.
- Colab currently reports that free GPU allocation is unavailable, so the Qwen3-4B follow-up comparison has not run.
- The dashboard is a front-end prototype. It supports audio selection/preview, language selection, editable transcript text, and transcript download. Automatic transcription requires a compatible local backend at `POST /api/transcribe` returning JSON with a `transcript` string.

## Open the dashboard

Open `outputs/dashboard/index.html` in a browser. To enable automatic transcription, run a local ASR backend and set its base URL under **Connect a transcription backend**. The selected audio is sent to that configured endpoint only after **Transcribe audio** is clicked.

## Project files

- `outputs/dashboard/index.html` — upload, preview, transcript editing, and download interface.
- `outputs/TASK_4_Stage_1_ASR_Diarization.ipynb` — Colab audio transcription and diarization workflow.
- `outputs/TASK_4_Clinical_Report_Generation_Guarded.ipynb` — guarded bilingual report-generation workflow.
- `outputs/*_summary.md`, `outputs/*_report.md` — run notes, review findings, and current limitations.
- `outputs/*template*` and review CSVs — transcript, speaker-role, and reference-verification templates.
- `outputs/final_adapter.zip` — recovered Task 3 LoRA adapter files.

## Data and validation notes

The source audio files are not included in this repository; only their metadata and model-generated draft outputs are included. Dataset manifest paths are stored as filenames so they do not disclose the original computer's directory structure. Reference transcripts and speaker-role labels remain unverified. Do not claim clinically accurate output until fluent reviewers validate transcripts, roles, medical terms, medication names, and numbers.
