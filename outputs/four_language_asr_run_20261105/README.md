# Four-language ASR run (5 Nov 2026)

These files are raw transcripts generated from the four supplied ElevenLabs recordings. The English file is the user's source consultation script, included as a reference. The English source script is not a second ASR transcript and must not be treated as proof that every translated recording says exactly the same thing.

## Models

- Bengali, Malayalam, Urdu: Bodhan AI / AI4Bharat Indic-Transcribe-core (1.2B), local CPU inference, explicit language code, native script, long-form chunking at pauses with a 30-second maximum. Its model card specifies single-speaker input, so the full-call runs on the project's three-speaker audio are preliminary; diarized speaker-turn transcription is needed for a better controlled run.
- Arabic: OpenAI Whisper large-v3, local CPU inference. It correctly recognized the main lab values on this audio, but misrecognized the family-history phrase about the mother's diabetes. Qwen3-ASR 0.6B and 1.7B were also tested and rejected because they misrecognized clinical values.

## What is and is not measured

A per-language WER/CER accuracy percentage is **not available**. The workspace does not contain the exact four regional-language ElevenLabs input texts or a fluent-reviewed transcript for each audio. The English source alone cannot be used as the reference text for a regional-language WER/CER score. The Indic model card publishes Voice of India benchmark OIWER values of Bengali 4.3, Malayalam 11.3, and Urdu 5.0; those are external benchmark results, not accuracy scores for these synthetic recordings: https://huggingface.co/bodhan-ai/indic-transcribe-core

The transcripts need a fluent reviewer to compare them against the audio and the exact regional-language input. In particular, check family history (the mother's diabetes line), medicine spellings, and role changes. The English source explicitly contains the mother's diabetes; ASR hypotheses omit or garble that phrase. Do not silently patch raw ASR with the English source.

## Corrected candidate transcripts

The `*_best_effort_bilingual_candidate.txt` files restore the intended source-script facts and include English and regional-language text with doctor/patient/nurse labels. They are clearly labeled candidates: the corrected family-history and medicine content comes from the source script where ASR was uncertain, and the role names follow the script rather than verified voice-cluster mapping. The raw audio recognizer outputs remain separate.

## Speaker labels

The existing pyannote Community-1 output is preserved separately in `../diarization/pyannote/`. It identifies anonymous speaker clusters, not verified doctor/patient/nurse roles. The ASR text here is whole-conversation text without speaker tags; per-turn role labels need a language-aware pass/review. The per-turn ASR attempt was stopped because CPU inference per short segment was much slower than full-file chunked transcription.

## Medical use

These are research/internship drafts. They are not clinically verified and should not be used for care or to generate a final clinical report before human review.
