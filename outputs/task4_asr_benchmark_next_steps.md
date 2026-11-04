# Next step: verify transcripts and benchmark ASR

## What I prepared

- `task4_transcript_review_template.csv` now shows three drafts side by side: WhisperX Large-v3-Turbo, SeamlessM4T v2 Large, and official Whisper Large-v3. The reference and review columns remain empty.
- `task4_verified_references_template.csv` has one row per language for a fluent reviewer to enter the exact regional-language words used for TTS and mark `review_status` as `verified`.
- `task4_asr_wer_cer.py` compares the saved three model drafts and leaves WER/CER blank unless the reference has text, a reviewer name, and `review_status=verified`.

## What the reviewer should do

1. A fluent Arabic, Bengali, Malayalam, and Urdu reviewer listens to the corresponding recording while checking the exact source text used for ElevenLabs. They should preserve what was actually spoken, including any changes made for TTS.
2. Fill `reference_text`, `reviewer`, and `reviewed_date` in the reference CSV. Mark medical terms, numbers, and speaker turns as checked only after listening and checking them.
3. Set `review_status` to `verified` only after the full transcript is checked. Do not use an unverified machine translation as ground truth.
4. Run from this folder: `python3 outputs/task4_asr_wer_cer.py` (from the workspace root) or `python3 task4_asr_wer_cer.py` (from `outputs`). The result will be written to `task4_asr_wer_cer_results.csv`.

## Metric notes

The evaluator applies NFC Unicode normalization, lowercases/casefolds, removes punctuation and Arabic vocalization marks/tatweel, and retains Bengali/Malayalam combining marks and all numbers. WER uses whitespace-delimited words; CER uses Unicode characters without spaces. These are conventional comparison scores, not proof that clinical facts are safe. Separately inspect drug names, diagnoses, lab values, and diarization.
