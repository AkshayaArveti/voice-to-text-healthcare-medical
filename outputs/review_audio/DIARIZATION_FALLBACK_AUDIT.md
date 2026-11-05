# Speaker-diarization fallback audit

## Initial fallback status

The initial pyannote attempt could not run because no Hugging Face token was saved on this computer. A local attempt with the public `speechbrain/spkrec-ecapa-voxceleb` model was evaluated as a fallback, but it did not produce reliable three-speaker clusters for these recordings. The experimental Bengali, Malayalam, and Urdu cluster files were removed instead of retaining misleading labels.

## Why the fallback was rejected

- ECAPA produced highly imbalanced clusters. For Bengali, 41 of 43 Whisper segments landed in one cluster, while the other two clusters contained one segment each.
- Fixed 2.5-second acoustic windows also collapsed most Bengali speech into one cluster and produced inconsistent results for the other samples.
- Malayalam's saved Whisper timestamps end at about 198.8 seconds, but the local source audio is about 175.2 seconds long. Those timestamps cannot be used to assign speakers reliably.
- The ECAPA checkpoint was trained on English VoxCeleb recordings, not these regional-language synthetic voices.

## Follow-up: pyannote successfully ran

After the user completed Hugging Face login locally, pyannote Community-1 ran against all four recordings using the known speaker count of three. Results are in `outputs/diarization/pyannote/`:

- Arabic: 51 diarization intervals.
- Bengali: 45 diarization intervals.
- Malayalam: 63 diarization intervals.
- Urdu: 57 diarization intervals.

Each JSON reports three anonymous IDs and durations. These outputs do not assign doctor/patient/nurse roles. Speaker-labeled raw Whisper drafts were created for Arabic, Bengali, and Urdu. They were not merged with Malayalam ASR because its saved Whisper timestamps extend past the actual audio duration. All transcripts and role mappings still require human review. The Hugging Face token remains in the local credential store and is not included in project files.

Next, use `outputs/review_audio/speaker_roles/SPEAKER_ROLE_REVIEW.md` to review the IDs against the audio and record roles in `outputs/task4_speaker_role_review.csv`.
