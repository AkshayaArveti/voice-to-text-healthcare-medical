# Task 4 — Phase 4: official Whisper Large-v3 ASR run

## Run details

- Model: `openai/whisper-large-v3` from the official OpenAI Whisper package (`20250625`)
- Runtime: Google Colab Tesla T4
- Model load time: 110.2 seconds
- Peak allocated GPU memory: 6.25 GiB
- Per-file inference time: Arabic 50.3 s; Bengali 192.1 s; Malayalam 125.9 s; Urdu 59.0 s
- Processing was local in the Colab GPU runtime; no paid speech API was used.

The raw transcripts and timing metadata are saved in `whisper_large_v3_results.json` and `whisper_large_v3_results.csv`. Treat every transcript as an **unverified draft**.

## Script sanity check

This checks only whether alphabetic characters fall in the expected Unicode script range. It does not measure word accuracy, meaning, translation fidelity, medical terms, numeric values, or speaker diarization.

| Language | Whisper Large-v3 | Earlier WhisperX large-v3-turbo | SeamlessM4T v2 Large |
|---|---:|---:|---:|
| Arabic | 100.0% | 100.0% | 100.0% |
| Bengali | 94.9% | 96.1% | 100.0% |
| Malayalam | 36.2% | 0.0% | 99.2% |
| Urdu | 100.0% | 99.1% | 100.0% |

The Arabic and Urdu outputs were entirely in Arabic script. Bengali was mostly in Bengali script. Malayalam was only 36.2% Malayalam-script alphabetic characters and contained a mixture of scripts, so this run is not acceptable as a Malayalam transcript draft without replacement/review. A high script percentage is not evidence of a correct transcript.

A quick qualitative inspection also shows transcription problems, including malformed Bengali wording, script mixing in Malayalam, and omissions/substitutions in otherwise readable Arabic and Urdu drafts. Do not create clinical reports directly from these ASR outputs.

## What can and cannot be concluded

This establishes that the official Whisper Large-v3 checkpoint loads and completes all four clips on a Colab T4, with the measured resource use above. It does **not** establish that it is more accurate than WhisperX turbo or SeamlessM4T. No word error rate (WER) or character error rate (CER) is reported because the fluent-reviewed regional-language reference transcripts are not yet in the evaluation files. Script checks cannot substitute for those references.

The same source script was converted to speech by TTS, but the exact regional-language text supplied to TTS must be added as a reviewed reference, including any wording or pronunciation changes introduced during synthesis. A fluent reviewer should verify the references and ASR outputs, especially drug names, diagnoses, lab values, and speaker turns.

## Next project action

Create one reviewed reference transcript per language and confirm role labels by listening to each speaker. Then calculate per-language WER/CER for WhisperX turbo, SeamlessM4T, and Whisper Large-v3. Keep the ASR choice provisional until that benchmark is complete. Only use a reviewed transcript for the later clinical extraction stage.
