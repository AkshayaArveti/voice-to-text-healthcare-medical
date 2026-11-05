# Audio-to-script correction log

These are evidence-tagged candidate transcripts, not verified references. We ran full-file ASR on all four audios; Bengali, Malayalam, and Urdu use Indic-Transcribe-core, while Arabic uses Whisper large-v3-turbo. We also ran focused family-history crops.

| Content | Audio model evidence | Source-script correction used in candidate |
|---|---|---|
| Family history | Full and focused outputs fail to reliably recover the mother's condition in all four languages. | The English source says the father had a heart attack and the mother has diabetes. The bilingual candidates restore that intended content. |
| Numeric results | Full ASR text includes HbA1c 8.4%, fasting glucose 186 mg/dL, post-meal glucose 252 mg/dL, and BP 148/94 in all four language transcripts. | Keep the native-script number wording from the bilingual candidates; compare the source audio before clinical use. |
| Medicines | Names are recognized phonetically, with spelling uncertainty especially in Malayalam/Urdu. | Candidate aligns to source names: Metformin, Telmisartan, Vitamin D3, Atorvastatin. |
| Speakers | Pyannote produces anonymous voice clusters. Role mapping is not confirmed by acoustics. | Candidate uses the known script roles [DOCTOR], [PATIENT], [NURSE] in script order. |

The machine outputs remain in `*_asr_raw.txt`. Candidate transcripts are in `*_best_effort_bilingual_candidate.txt`. Keep both. No WER/CER is reported because the exact ElevenLabs regional-language input text and fluent-reviewed acoustic reference are not available in the workspace. The candidate is intended-content corrected, not a word-for-word audio verification.
