# Task 4 output schema aligned with Task 3

Task 3's final inference cell asks the fine-tuned model to summarize a clinical note in **SOAP format**. This replaces the provisional 12-field schema used in the first Task 4 experiment.

For each consultation, the final system should produce two SOAP notes:

1. English
2. The conversation's source language (Arabic, Bengali, Malayalam, or Urdu)

## SOAP sections

- **S — Subjective:** Patient-reported complaint, symptoms, duration, relevant history, family history, and lifestyle details.
- **O — Objective:** Measurements, examination findings, tests, and laboratory results explicitly stated in the transcript.
- **A — Assessment:** Diagnoses or clinical assessment explicitly stated by the doctor. Do not infer a diagnosis from symptoms or measurements.
- **P — Plan:** Medicines and doses if stated, advice, tests ordered, and follow-up instructions explicitly stated by the doctor.

## Evidence and uncertainty rules

- Use only facts found in the verified transcript.
- If a section has no supported information, write `Not stated` / its equivalent in the output language.
- Mark unclear words, numbers, medicine names, or speaker attribution as `Unclear`; do not guess.
- Preserve the patient's words separately from the doctor's assessment.
- Keep a source-language transcript attached to the output for audit.
- The English and regional notes are drafts until a fluent reviewer checks the transcript and both SOAP versions.

## Current status

The Task 4 Qwen 3B test produced language and content errors, so its eight report rows are retained only as unreviewed experimental output. The next extraction run should use a transcript that a fluent reviewer has checked and the SOAP structure above.
