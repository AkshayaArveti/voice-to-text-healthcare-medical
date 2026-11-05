# Human review checklist for the four regional recordings

## Why this review is required

These recordings were generated with text-to-speech from the same consultation script. The machine transcripts are drafts, not ground truth. Existing automatic outputs contain clear recognition and speaker-assignment errors, so do not approve a transcript just because it matches an ASR result.

## Recordings and draft transcripts

| Language | Original audio on Akshaya's computer | Draft to compare with the audio |
| --- | --- | --- |
| Arabic | `~/Downloads/arabic.mp3` | `arabic_reference_aligned.txt` and `arabic_original_whisper_result.txt` |
| Bengali | `~/Downloads/bengali.mp3` | `bengali_reference_aligned.txt` and the Bengali row in `outputs/task4_transcript_review_template.csv` |
| Malayalam | `~/Downloads/malayalam.mp3` | `malayalam_reference_aligned.txt` and the Malayalam row in `outputs/task4_transcript_review_template.csv` |
| Urdu | `~/Desktop/urdu.mp3` | `urdu_reference_aligned.txt` and the Urdu row in `outputs/task4_transcript_review_template.csv` |

The `_reference_aligned.txt` files are source-script translations/drafts; they are not verified transcriptions of the recordings. The CSV contains ASR alternatives for comparison only.

## Reviewer instructions

Please ask one fluent reader/listener per language to listen to the full recording while reading its draft. Have them correct the transcript in that language and confirm all speaker changes. Use `[unclear]` where speech cannot be confidently understood; do not fill gaps by guessing from the English script.

Check especially:

- All words and the order of the three voices (doctor, patient, nurse).
- Symptoms and durations, medical/family history, tests, diagnoses, medication names, and follow-up instructions.
- Every numeric value: HbA1c 8.4%, fasting glucose 186 mg/dL, post-meal glucose 252 mg/dL, blood pressure 148/94, 30 minutes of walking, 7–8 hours of sleep, and follow-up in two weeks. These are expected from the shared source script; record what the audio actually says if it differs.
- Whether the final corrected transcript is in the intended language and script.

## Mark the review complete

For each language, fill the matching row in `outputs/task4_transcript_review_template.csv`:

1. Put the full corrected transcript in `verified_reference_transcript`.
2. Enter the reviewer's name or initials in `reviewer`.
3. Mark `medical_terms_checked`, `numbers_and_dates_checked`, and `all_3_speakers_checked` as `yes` only after listening.
4. Record uncertainties or differences from the English source in `review_notes`.

Arabic-specific note: check the family-history line and the transition around 64–70 seconds carefully. The current Whisper output garbles the mother's diabetes line and appears to assign a speaker incorrectly around that transition.

## After review

Return the completed CSV and corrected transcripts. Only then should the verified text be used for report-generation evaluation. A fluent-language review checks transcription; a qualified clinician should separately review any clinical interpretation before it is presented as medically reliable.
