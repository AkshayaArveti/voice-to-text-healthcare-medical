# Original Arabic recording — preliminary review

- Source: the user's original `arabic.mp3` three-speaker recording.
- Local ASR: OpenAI Whisper `large-v3-turbo` on CPU; detected language `ar`.
- Output: 47 timestamped segments. This is an ASR draft, not a fluent-speaker-verified transcript.
- Diarization did **not** run because this computer has no Hugging Face login/token. The result contains no speaker IDs or role labels.
- A spot-check against the supplied English consultation script shows a material family-history error: after the family-history question, Whisper turns “my mother has diabetes” into a phrase about alcohol. Some medical terms and medicine names also appear as uncertain phonetic spellings.
- Main lab values are present in the raw transcript, but still require listening review.
- The Arabic reference draft in this folder was reconstructed from English. It is not the exact Arabic ElevenLabs source text, so it cannot serve as ground truth for WER.

## What is still needed

A fluent Arabic listener must correct the transcript against the audio and the exact Arabic TTS input. To test diarization, sign in on this machine with the Hugging Face account that has access to `pyannote/speaker-diarization-community-1`, then rerun the original recording. Speaker IDs still need a human to map them to doctor, patient, and nurse.
