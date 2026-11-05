# Original Arabic recording — experimental speaker clustering

The original Arabic recording was run through a local fallback speaker-clustering workflow because this computer is not authenticated to Hugging Face and the configured pyannote pipeline could not run.

- The public SpeechBrain ECAPA-TDNN speaker-embedding checkpoint was applied to the 47 Whisper timestamped segments.
- Agglomerative clustering with three clusters produced anonymous IDs `SPEAKER_00`, `SPEAKER_01`, and `SPEAKER_02`.
- Matching the clusters to the expected script turn order suggests `SPEAKER_00` is likely the doctor, `SPEAKER_01` the patient, and `SPEAKER_02` the nurse.
- This is experimental. The checkpoint was trained on English VoxCeleb, not specifically Arabic. Role mapping comes from scripted order, not a fluent listener's acoustic review.
- The family-history/smoking transition around 64–70 seconds is ambiguous: Whisper appears to have merged or mis-transcribed a turn there. Check the audio before using the labels.

Files:

- `arabic_original_speaker_clusters.json` — timestamps and anonymous speaker IDs.
- `arabic_original_speaker_clusters.txt` — readable segment list with tentative role mapping.

This fallback does not replace the backend's pyannote Community-1 setup and is not a validated diarization result.
