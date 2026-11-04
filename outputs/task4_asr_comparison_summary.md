# Task 4: ASR comparison draft

## Run completed

Compared WhisperX `large-v3-turbo` with SeamlessM4T v2 Large on the same four supplied recordings in a Colab T4 runtime. Both used local model inference; no paid speech API was called. SeamlessM4T processed each recording in 20-second chunks.

The model card lists Arabic, Bengali, Malayalam, and Urdu as supported speech-input/text-output languages. It identifies the checkpoint as about 2.3B parameters and lists the CC BY-NC 4.0 license; check that license before any commercial or public deployment. [Official model card](https://huggingface.co/facebook/seamless-m4t-v2-large)

## Expected-script check

This is only a Unicode-script consistency check: the percentage of alphabetic characters in each model draft that belong to the expected script block. It does **not** measure word accuracy, meaning, medical-term accuracy, or speaker-role accuracy.

| Language | WhisperX draft | SeamlessM4T v2 draft |
|---|---:|---:|
| Arabic | 100.0% Arabic-block letters | 100.0% |
| Bengali | 96.1% Bengali-block letters | 100.0% |
| Malayalam | 0.0% Malayalam-block letters | 99.2% |
| Urdu | 99.1% Arabic-block letters | 100.0% |

WhisperX produced Malayalam text in Devanagari in this run. SeamlessM4T produced Malayalam-script text. That shows a script-format difference, not proof that the second transcript is semantically more accurate.

## Files

The [combined results ZIP](task4_stage2_comparison_results.zip) includes the turn-level CSV, JSON, and side-by-side ASR draft CSV.

## What is needed for an accuracy decision

A fluent reviewer should verify the exact regional-language transcripts used to create the ElevenLabs audio. With those references, calculate per-language WER/CER and manually check names, diagnoses, medicine names, and numbers. Until then, keep both model outputs as drafts and do not generate final clinical reports from them.
