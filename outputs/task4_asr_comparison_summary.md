# Task 4: Updated multilingual ASR run

Run date: 2026-11-05. Models were run locally without a paid speech API.

## Current model choice

| Audio language | Candidate selected for the current transcript | Why | Status |
|---|---|---|---|
| Bengali | Bodhan AI / AI4Bharat Indic-Transcribe-core (1.2B) | Correct native script; preserves the key lab values and medicine words better than the earlier draft | Raw ASR; family-history error remains |
| Malayalam | Bodhan AI / AI4Bharat Indic-Transcribe-core (1.2B) | Correct native script; avoids WhisperX's Devanagari output | Raw ASR; medicine spelling and omitted family detail need review |
| Urdu | Bodhan AI / AI4Bharat Indic-Transcribe-core (1.2B) | Correct Urdu script; preserves the key values | Raw ASR; family-history phrase is incomplete |
| Arabic | OpenAI Whisper large-v3 | Tested on the actual audio; main lab values were retained. Qwen3-ASR 0.6B and 1.7B were also tested but misrecognized critical values. | Raw ASR; mother's diabetes is garbled as a question about alcohol |

For Indic-Transcribe-core, long recordings were decoded in chunks of at most 30 seconds at natural pauses. Inference used the explicit language code and native-script mode. On this Mac, Bengali took about 90 seconds, Malayalam 106 seconds, and Urdu 103 seconds. The model card specifies single-speaker input, however; because these audios contain three speakers, these whole-call runs are preliminary. For the next accuracy-focused run, diarize first and transcribe speaker turns separately. The local CPU is slower than a T4 GPU, but it did not require a paid endpoint.

## Accuracy: project data vs published benchmark

No honest per-audio WER/CER percentage can be reported yet. The project contains regional-language translations aligned to the English source, but they are draft translations rather than exact original ElevenLabs input texts or fluent-reviewed references. They are useful for checking intended meaning, but not sufficient as verified acoustic ground truth for WER/CER. The English script itself is not a valid reference string for WER/CER in Bengali, Malayalam, Urdu, or Arabic.

Indic-Transcribe-core's official model card reports Voice of India benchmark OIWER values of Bengali 4.3, Malayalam 11.3, and Urdu 5.0 (lower is better). These published benchmark values are **not** scores on the four internship recordings. The same model card states that the model is not certified for safety-critical/medical use. [Model card](https://huggingface.co/bodhan-ai/indic-transcribe-core)

## Critical clinical-content review

The model outputs retained HbA1c 8.4%, fasting glucose 186 mg/dL, post-meal glucose 252 mg/dL, and blood pressure 148/94 in the inspected transcripts. This is a content spot-check, not proof that every phrase is correct.

The family-history sentence is a high-risk failure across the available drafts: the source says the patient's father had a heart attack and the mother has diabetes. Bengali changes or repeats the nearby smoking question; Malayalam omits or garbles the mother's condition; Urdu leaves the clause incomplete; Arabic Whisper and the earlier Seamless draft garble it. A second-pass transcription on focused audio crops did not resolve this line. Keep raw outputs unchanged and mark it unclear until checked against the recording by a fluent reviewer. Check medication names, especially Telmisartan and Atorvastatin, in the same review.

## Speaker roles and bilingual output

The provided speaker diarization gives anonymous `SPEAKER_00` etc. IDs; it does not verify which voice is doctor, patient, or nurse. The new Indic model returns whole-file text without timestamps, so attaching pyannote IDs directly to individual Indic text spans would be misleading. Existing diarization files remain under `outputs/diarization/pyannote/`.

The bundle includes four raw audio transcripts, focused family-history spot-checks, four source-script-corrected bilingual candidates, and the English source script. The candidate files restore intended facts from the English script where ASR failed, while preserving the raw ASR separately. They are not word-for-word verified acoustic transcripts. in `outputs/four_language_asr_run_20261105.zip`. English source text is included as the source-script reference; it is not a machine-generated English translation of each regional audio.

## What is needed to claim accuracy

Use the exact regional-language TTS source texts as references, then have one fluent listener per language correct the model transcript while listening to the audio. Verify the three speaker changes, family history, all numerical values, and medicine names. Mark references reviewed in `outputs/task4_transcript_review_template.csv`; then run `outputs/task4_asr_wer_cer.py` to calculate per-language WER/CER. Until then these are improved ASR drafts, not verified transcripts or clinical records.


## Provisional reference-draft comparison

A numerical comparison was run against the regional-language reference-aligned drafts in the workspace. The drafts are not confirmed exact ElevenLabs inputs or fluent-reviewed acoustic references, so these WER/CER values are **not valid project accuracy scores**.

| Language | WER | CER |
|---|---:|---:|
| Arabic | 48.67% | 37.72% |
| Bengali | 10.31% | 3.33% |
| Malayalam | 20.48% | 4.88% |
| Urdu | 2.88% | 2.45% |

Use these only to find lines for review. In the scoped clinical fact check, all four raw transcripts contained the four main measured values, while none reliably captured the mother's diabetes phrase. That 4/4 and 0/4 observation is a narrow fact check, not an overall accuracy score. Full details: `outputs/four_language_asr_run_20261105/provisional_reference_draft_comparison.md`.
