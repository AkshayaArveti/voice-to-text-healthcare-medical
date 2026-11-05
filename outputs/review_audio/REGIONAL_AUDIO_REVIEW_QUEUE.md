# Regional audio review queue — machine findings only

These are triage notes from comparing saved ASR drafts with the shared English source script. They do not verify what the recordings actually say. Reviewers must listen and transcribe what they hear; the English script is only a comparison aid.

## 1. Arabic — waiting for fluent review

- Full audio: `~/Downloads/arabic.mp3`.
- Focused family-history clip: `arabic_family_history_check.mp3`.
- Whisper garbles the mother's family-history condition as an alcohol-related phrase. The supplied script says the mother has diabetes.
- Check the family-history answer and the transition into the smoking/alcohol exchange. Current experimental speaker clusters are uncertain near 64–70 seconds.
- Full ASR and draft notes: `../reference_transcripts/arabic_original_review.md`.

## 2. Bengali — next language to review

- Full audio: `~/Downloads/bengali.mp3`.
- Focused clips: `bengali_history_check.mp3` and `bengali_values_check.mp3`.
- The saved Seamless and Whisper drafts disagree on numeric results. Seamless reads fasting glucose as 168 (the source script says 186) and blood pressure as 148/49 (source says 148/94). Confirm the actual Bengali audio; do not silently substitute the source-script values.
- The WhisperX draft contains visibly corrupted text and a stray Devanagari character; Whisper and Seamless are more readable, but still have meaning/wording disagreements in the history section.
- Review all three voices, the family-history line, medication names, and every number.

## 3. Malayalam

- Full audio: `~/Downloads/malayalam.mp3`.
- Focused clips: `malayalam_history_check.mp3` and `malayalam_values_check.mp3`.
- WhisperX produced the transcript in Devanagari instead of Malayalam script. Whisper's output is heavily mixed with other scripts and damaged text. Seamless is the only saved candidate largely in Malayalam script, but remains an unverified ASR draft.
- Review all three voices, the mother's condition, medication names, and numeric results against the audio.

## 4. Urdu

- Full audio: `~/Desktop/urdu.mp3`.
- Focused clips: `urdu_history_check.mp3` and `urdu_values_check.mp3`.
- The Seamless draft conflicts with the source script on important numbers: fasting glucose 128 vs 186, post-meal glucose 220 vs 252, and blood pressure 140/40 vs 148/94. Confirm what the audio actually says.
- Whisper drafts also garble the mother's family-history condition and have medication-name spelling uncertainty.
- Review all three voices, medical terms, and every number.

## Completion rule

For each language, a fluent reviewer must provide the corrected full transcript and confirm the speaker turns, medical words, and numbers after listening to the full recording. Until then, keep the transcript and any report generated from it marked **unverified**. Enter the review in `../task4_transcript_review_template.csv`.
