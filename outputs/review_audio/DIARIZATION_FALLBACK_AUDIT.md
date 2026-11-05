# Speaker-diarization fallback audit

## Status

The pyannote Community-1 pipeline cannot run on this computer because no Hugging Face token is saved here. A local attempt with the public `speechbrain/spkrec-ecapa-voxceleb` model was evaluated as a fallback, but it did not produce reliable three-speaker clusters for these recordings. The experimental Bengali, Malayalam, and Urdu cluster files were removed instead of retaining misleading labels.

## Why the fallback was rejected

- ECAPA produced highly imbalanced clusters. For Bengali, 41 of 43 Whisper segments landed in one cluster, while the other two clusters contained one segment each.
- Fixed 2.5-second acoustic windows also collapsed most Bengali speech into one cluster and produced inconsistent results for the other samples.
- Malayalam's saved Whisper timestamps end at about 198.8 seconds, but the local source audio is about 175.2 seconds long. Those timestamps cannot be used to assign speakers reliably.
- The ECAPA checkpoint was trained on English VoxCeleb recordings, not these regional-language synthetic voices.

## Recommended remaining step

Run the project's documented pyannote Community-1 setup after a user with model access signs in locally with `hf auth login`. Keep the token on that computer and out of project files. Then listen to the output, map anonymous IDs to doctor, patient, and nurse, and record the result in `outputs/task4_speaker_role_review.csv`. If authentication is unavailable, leave role assignments marked unverified rather than using the failed fallback.
