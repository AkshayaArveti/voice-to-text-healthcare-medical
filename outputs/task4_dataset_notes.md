# Task 4 dataset preparation notes

## Current data

The initial dataset has four ElevenLabs text-to-speech MP3 files, one per language, generated from the same consultation script translated into Arabic, Bengali, Malayalam, and Urdu (as described by the project owner). Audio properties and current filenames are recorded in `task4_dataset_manifest.csv`.

## Speaker and reference status

- The final turn-level export lists three anonymous speaker IDs in each clip. An earlier whole-clip diarization pass listed only two IDs per clip, so the detected count is inconsistent across passes and needs listening review. These IDs are per-recording labels; doctor/patient/nurse roles have not been assigned by a reviewer.
- The original translated text used to generate each regional audio is not in the current workspace. ASR drafts are not ground-truth transcripts. Reference transcript fields remain blank until the source text is supplied or a fluent reviewer verifies it.

## Dataset limits

- There is currently only one recording for each language, all using the same script and synthetic TTS voices.
- No train/validation/test split is assigned. With one recording per language, a meaningful split is not possible without collecting more independent recordings.
- This pilot set can check the pipeline and reveal obvious language/script failures; it cannot establish real-world clinical speech accuracy or speaker diarization accuracy.
- Medical terms, names, numbers, speaker turns, and roles require reference-text and fluent-speaker review before metric calculations or report generation.
