# Urdu review packet

## Recording

- Full audio on Akshaya's computer: `~/Desktop/urdu.mp3`.
- Focus clips: `urdu_history_check.mp3` (about 58–76 seconds) and `urdu_values_check.mp3` (about 91–127 seconds).
- Candidate drafts are in `outputs/task4_transcript_review_template.csv`; the intended source-script translation is `outputs/reference_transcripts/urdu_reference_aligned.txt`.

## Automatic-transcription problems found

- SeamlessM4T's draft reports fasting glucose 128 mg/dL, post-meal glucose 220 mg/dL, and blood pressure 140/40. These conflict with the shared English script's 186 mg/dL, 252 mg/dL, and 148/94. Listen and transcribe the audio itself; do not replace its values with the English script by default.
- The family-history section is garbled across the machine drafts. In particular, the mother's condition is confused with alcohol in at least one draft.
- Medication names are rendered phonetically and need careful listening.
- The other ASR drafts contain more script-consistent numbers, but that does not make them ground truth.

## What the reviewer should return

Listen to the full recording, using the short clips for the family-history and values sections. Please provide:

1. A corrected full transcript in Urdu script, preserving what the audio actually says.
2. Speaker turns for doctor, patient, and nurse; note any point where attribution is uncertain.
3. Confirmed wording for the family-history answer, tests, each lab/vital value, diagnoses, medication names, and follow-up advice.
4. `[غیر واضح]` for anything genuinely unclear rather than guessing from the English script.

The English source script is only a comparison aid. Keep this transcript marked **unverified** until a fluent Urdu reviewer checks the complete recording.
