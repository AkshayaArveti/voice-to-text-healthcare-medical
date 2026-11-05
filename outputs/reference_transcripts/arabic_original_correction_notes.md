# Arabic transcript correction notes

The corrected draft is aligned to the supplied English consultation script. The raw Whisper transcript remains preserved in `arabic_original_whisper_result.json` and `.txt`.

Corrections made from the source meaning:

- Family history: corrected the mother's condition to diabetes (`ووالدتي مصابة بالسكري`). Whisper had rendered this as an unclear phrase about alcohol.
- Kidney function: normalized the medical term to kidney function (`وظائف الكلى`).
- Medication names: normalized Metformin, Telmisartan, Vitamin D3, and Atorvastatin to their Arabic transliterations.
- Values: restored HbA1c 8.4%, fasting glucose 186 mg/dL, post-meal glucose 252 mg/dL, and blood pressure 148/94 from the source script.
- Speaker labels: assigned from the script's turn order; they are not verified from the audio.

This is a corrected **draft translation**, not a fluent-speaker-verified verbatim Arabic transcript. A fluent Arabic listener must check the wording against the recording and the exact Arabic TTS input before using it as ground truth.
