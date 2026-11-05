# Malayalam review packet

## Recording

- Full audio on Akshaya's computer: `~/Downloads/malayalam.mp3`.
- Focus clips: `malayalam_history_check.mp3` (about 58–76 seconds) and `malayalam_values_check.mp3` (about 91–127 seconds).
- Candidate drafts are in `outputs/task4_transcript_review_template.csv`; the intended source-script translation is `outputs/reference_transcripts/malayalam_reference_aligned.txt`.

## Automatic-transcription problems found

- WhisperX transcribed the Malayalam speech using Devanagari characters, so its draft is not a usable Malayalam-script reference.
- Whisper large-v3 produced heavily mixed scripts and damaged text.
- SeamlessM4T produced mostly Malayalam script, but its family-history line is garbled and includes an apparent phrase about alcohol where the source script says the patient's mother has diabetes. This is an ASR clue, not proof of what the recording says.
- Seamless appears to recognize the main values as HbA1c 8.4%, glucose 186 and 252 mg/dL, and BP 148/94. Confirm each against the audio; do not assume it is correct because the values match the English source.

## What the reviewer should return

Listen to the full recording, using the short clips for the family-history and values sections. Please provide:

1. A corrected full transcript in Malayalam script, preserving what the audio actually says.
2. Speaker turns for doctor, patient, and nurse; note any point where attribution is uncertain.
3. Confirmed wording for the family-history answer, tests, lab values, diagnoses, medication names, and follow-up advice.
4. `[അവ്യക്തം]` for anything genuinely unclear instead of guessing from the English source.

The English source script can help locate expected content, but it is not the ground truth for the audio. Keep this transcript marked **unverified** until the fluent reviewer checks the complete recording.
