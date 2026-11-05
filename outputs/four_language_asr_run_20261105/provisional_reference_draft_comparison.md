# Provisional transcript-to-reference-draft comparison

This is the first numerical comparison pass. It calculates word error rate (WER) and character error rate (CER) between the selected audio-derived transcript and the project’s regional-language reference-aligned draft. The project references are translations reconstructed from the English source script, not confirmed copies of the exact ElevenLabs text and not fluent-reviewed transcripts. Therefore these are **provisional draft-to-draft distances, not valid accuracy scores for the recordings**. Do not report `100 − WER` as accuracy.

| Language | Audio model | WER vs reference draft | CER vs reference draft |
|---|---|---:|---:|
| Arabic | Whisper large-v3-turbo | 48.67% | 37.72% |
| Bengali | Indic-Transcribe-core | 10.31% | 3.33% |
| Malayalam | Indic-Transcribe-core | 20.48% | 4.88% |
| Urdu | Indic-Transcribe-core | 2.88% | 2.45% |

The differences partly reflect different translation wording and script normalization; Arabic/Indic word tokenization also varies. Low draft-to-draft error does not prove semantic correctness: Urdu has a low comparison score while the family-history phrase is still missing/garbled. Use these numbers only to identify where to review, not to claim model accuracy.

Separately, a narrow content check found the HbA1c, fasting glucose, post-meal glucose, and blood pressure values in all four raw transcript drafts (4/4 recordings for those four values). The mother’s diabetes statement was not reliably recognized in any raw output (0/4). This is a small clinical-fact check, not an overall transcript accuracy score.

To calculate reportable WER/CER, replace each draft with the exact regional-language ElevenLabs input or a fluent-reviewed transcript of the audio, then rerun the project scorer.
