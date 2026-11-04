# Regional transcript review instructions

The attached CSV has one row per audio, with two ASR drafts. The WhisperX draft for Malayalam is in Devanagari script, so it is not a usable Malayalam transcript. Use the Seamless draft as a comparison aid only; neither draft is a verified reference.

Ask a fluent reader of each language to compare the audio and the original translated script, then fill `verified_reference_transcript` with the corrected transcript. Please check:

- All dialogue and speaker turns (doctor, patient, nurse).
- Symptom names, durations, family history, tests, lab values, diagnoses, medicine names, and follow-up instructions.
- Any unclear speech: mark it as `[unclear]` rather than guessing.
- Whether the transcript stays in the intended regional language.

The generated Qwen report drafts are not suitable for evaluation until these transcript checks are complete. After completing the CSV, share it here and I can update the pipeline to extract reports only from the verified transcript column.
