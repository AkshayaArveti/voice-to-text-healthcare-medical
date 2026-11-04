# Task 4 — Phase 3 dataset validation

Status: **metadata checks passed; transcript/content validation is pending.** No accuracy score or dataset split has been created.

## Audio checks

All four expected local MP3 files opened successfully with `afinfo`. Each is mono, 44.1 kHz, and 128 kb/s. Durations are about 2:46–2:55. A per-file checklist is in `task4_phase3_validation_checklist.csv`.

## ASR script diagnostic

A Unicode script-family count was run on the two ASR draft outputs. This is only a script sanity check, not transcription accuracy:

- Arabic: both drafts contain Arabic-script text.
- Bengali: both are primarily Bengali script; the WhisperX draft also contains a few Devanagari characters.
- Malayalam: WhisperX produced Devanagari text; SeamlessM4T produced Malayalam script.
- Urdu: both drafts are primarily Arabic-script text.

The counts are saved in `task4_asr_script_diagnostics.csv`. They do not establish that words, medical terms, or numbers are correct.

## Speaker-count mismatch

The earlier whole-clip diarization output found two speaker IDs in each audio. The later turn-level export contains three IDs in each. The mismatch occurs for all four languages; the added IDs differ by clip. No doctor/patient/nurse role has been confirmed by a listener. Treat speaker counts and roles as unresolved until the audio is reviewed.

## Validation still required

The original Arabic, Bengali, Malayalam, and Urdu text used to create the TTS audios is missing from the workspace. Without it or a fluent-reviewed transcript, we cannot compute WER/CER or verify medical terms, medicine names, lab numbers, and dialogue completeness. Those items remain blank/pending in the checklist.

There is one scripted TTS conversation per language, so this set cannot support a meaningful train/validation/test split or generalization claim. Keep it as a pilot set; add independent recordings before assigning splits.
