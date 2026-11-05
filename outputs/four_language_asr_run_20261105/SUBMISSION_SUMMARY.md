# Voice to Text — Healthcare Medical
## Four-language ASR submission summary

**Run date:** 5 November 2026  
**Languages:** Arabic, Bengali, Malayalam, Urdu  
**Audio source:** Four ElevenLabs text-to-speech consultation recordings, based on the same English consultation script supplied for this project.

## Models used

- **Bengali, Malayalam, Urdu:** Bodhan AI / AI4Bharat Indic-Transcribe-core (1.2B parameters), local inference, explicit language selection, native script, pause-aware chunks capped at 30 seconds. The model card specifies single-speaker audio; the full-call runs here are preliminary because the source recordings contain three speakers.
- **Arabic:** OpenAI Whisper large-v3, local CPU inference (selected after testing against the existing large-v3-turbo output and Qwen3-ASR 0.6B/1.7B).
- No paid speech API was used. The three Indic-language full recordings ran on CPU and took about 90 seconds (Bengali), 106 seconds (Malayalam), and 103 seconds (Urdu).

## Work completed

1. Ran ASR on all four supplied full-length recordings.
2. Used pyannote Community-1 results already available in the project for anonymous speaker clusters. The system finds speaker changes; the mapping of those IDs to doctor, patient, and nurse has not been independently confirmed from voice alone.
3. Re-transcribed the family-history audio crops to check a clinically important phrase.
4. Compared the audio-derived outputs against the English source script and the project’s regional-language script-aligned drafts.
5. Created bilingual, source-script-corrected transcript candidates while preserving raw ASR results separately.

## Results and limitations

The selected Whisper large-v3 Arabic transcript contains the key values from the source script: HbA1c 8.4%, fasting glucose 186 mg/dL, post-meal glucose 252 mg/dL, and blood pressure 148/94. It took about 70 seconds to transcribe the full audio on this CPU after the model was downloaded. This is a content spot-check; it is not a WER/CER accuracy score.

A Whisper large-v3 English-translation pass on the Bengali audio recovered glucose values 186 and 252, but changed the family-history sentence to say the mother died, mistranslated the blood pressure as 148.92, and altered other symptoms/advice. The earlier smaller translation output was worse on the glucose values. Neither English translation is accurate enough for a report without human correction.

ASR does not reliably recover the family-history phrase about the mother having diabetes. Whisper large-v3 rendered it as a question about alcoholic drinks. The focused audio re-transcription did not resolve it. Qwen3-ASR also misrecognized critical Arabic glucose and blood-pressure values, so it was not selected. Several medication names are also spelled phonetically in the raw outputs. The bilingual candidates use the source script to restore the intended medical facts; they must be treated as source-corrected candidates, not word-for-word ASR proof.

A first provisional WER/CER comparison has been run against the project’s regional-language reference-aligned drafts: Arabic 48.67/37.72, Bengali 10.31/3.33, Malayalam 20.48/4.88, Urdu 2.88/2.45 (WER/CER). These are draft-to-draft distances, not reportable accuracy scores: the references are not confirmed exact ElevenLabs inputs or fluent-reviewed audio transcripts, and translation wording changes the scores. See `provisional_reference_draft_comparison.md` and the CSV. A valid project WER/CER still requires the exact language input text or fluent-reviewed references.

The official Indic-Transcribe-core model card reports Voice of India benchmark OIWER values of Bengali 4.3, Malayalam 11.3, and Urdu 5.0 (lower is better). These published values are external benchmark results, not scores on these four recordings. The same card specifies single-speaker input; the next accuracy-focused run should diarize the call and transcribe speaker turns separately before selecting this model for the three-speaker audio. [Official model card](https://huggingface.co/bodhan-ai/indic-transcribe-core).

## Files in this pack

- `transcripts/*_asr_raw.txt`: raw outputs generated from the audio.
- `../qwen3_asr_arabic/arabic_whisper_large_v3_raw.txt`: full Whisper large-v3 Arabic run. Qwen3-ASR experiments are stored alongside it for audit and were rejected due to clinical-value errors.
- `transcripts/*_best_effort_bilingual_candidate.txt`: English and regional-language source-script-corrected candidate, with speaker roles following the supplied script.
- `family_history_audio_spotchecks.txt` and `.json`: focused audio crop outputs from the second pass.
- `audio_to_script_correction_log.md`: explains which candidate facts come from the source script where ASR was unclear.
- `qa_findings.csv`: language-level review summary.
- `provisional_reference_draft_scores.csv` and `provisional_reference_draft_comparison.md`: first numerical draft-to-draft comparison; not project accuracy.

## Project status

**ASR and bilingual candidate generation are complete. Transcript verification is pending.** Do not describe the candidates as clinically verified or use them as clinical records. A fluent language reviewer should check the family-history line, medicines, numbers, and speaker-role labels against the audio before final report generation.
