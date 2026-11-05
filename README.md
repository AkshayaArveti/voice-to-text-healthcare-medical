# Voice to Text — Healthcare Medical

A multilingual medical speech-to-text research project for Arabic, Bengali, Malayalam, and Urdu. The current dataset contains four synthetic ElevenLabs consultation recordings, one per language.

## Current project state

- Audio metadata and ASR drafts have been collected for the four language samples.
- Speaker-labeled reference-aligned text drafts are available for Arabic, Bengali, Malayalam, and Urdu under `outputs/reference_transcripts/`. The Arabic draft is reconstructed from the English source script and may differ from the Arabic ElevenLabs input; all four need fluent review against audio.
- ASR candidates were compared in Colab: WhisperX large-v3-turbo and SeamlessM4T v2 Large. Script-family percentages are diagnostic only; they are not word or medical accuracy scores.
- Diarization output is anonymous and speaker roles have not been verified by listeners.
- The fine-tuned clinical report extractor produced unsupported details in a spot check. Its reports are experimental and must not be used as final clinical outputs.
- Colab currently reports that free GPU allocation is unavailable, so the Qwen3-4B follow-up comparison has not run.
- The dashboard connects to a local FastAPI backend at `POST /api/transcribe`. It uses Whisper large-v3-turbo locally through MLX when Apple Metal is available and falls back to CPU otherwise. Optional pyannote Community-1 diarization provides anonymous speaker IDs, and the guarded `POST /api/report` route uses the experimental Qwen2.5-1.5B adapter to draft bilingual SOAP notes after transcript and role review. No paid API is used. See `backend/README.md` for setup and limitations.

## Open the dashboard

Start the backend following `backend/README.md`, then open `http://127.0.0.1:8000`. The selected audio is processed locally only after **Transcribe audio** is clicked.

## Project files

- `outputs/dashboard/index.html` — upload, preview, transcript editing, and download interface.
- `outputs/TASK_4_Stage_1_ASR_Diarization.ipynb` — Colab audio transcription and diarization workflow.
- `outputs/TASK_4_Clinical_Report_Generation_Guarded.ipynb` — guarded bilingual report-generation workflow.
- `outputs/*_summary.md`, `outputs/*_report.md` — run notes, review findings, and current limitations.
- `outputs/*template*` and review CSVs — transcript, speaker-role, and reference-verification templates.
- `outputs/reference_transcripts/*_reference_aligned.txt` — speaker-labeled draft transcripts for review and download; these are not human-verified audio transcripts.
- `outputs/reference_transcripts/arabic_mms_tts_preview.mp3` — local single-voice Arabic TTS preview from the reconstructed Arabic draft. It is not three-speaker audio or the original ElevenLabs recording. The `facebook/mms-tts-ara` checkpoint is licensed CC BY-NC 4.0.
- `outputs/reference_transcripts/arabic_mms_preview_whisper_result.txt` and `.json` — raw local Whisper output for the TTS preview. It contains recognition errors and cannot evaluate diarization because the preview has one voice.
- `outputs/reference_transcripts/arabic_original_whisper_result.txt` and `.json` — raw local Whisper output for the original Arabic recording; diarization was unavailable on this computer.
- `outputs/reference_transcripts/arabic_original_review.md` — preliminary error findings and the remaining human-review requirement for the original Arabic audio.
- `outputs/final_adapter.zip` — recovered Task 3 LoRA adapter files.

## Data and validation notes

The source audio files are not included in this repository; only their metadata and model-generated draft outputs are included. Dataset manifest paths are stored as filenames so they do not disclose the original computer's directory structure. Reference transcripts and speaker-role labels remain unverified. Do not claim clinically accurate output until fluent reviewers validate transcripts, roles, medical terms, medication names, and numbers.
