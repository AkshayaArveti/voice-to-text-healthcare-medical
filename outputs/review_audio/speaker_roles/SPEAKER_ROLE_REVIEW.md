# Speaker-role review packet

## Goal

Confirm which anonymous diarization ID belongs to the doctor, patient, and nurse in each recording. The existing file `outputs/task4_speaker_role_review.csv` has three IDs per language, but its `role_reviewed_by_human` values are blank. Treat every ID-to-role mapping as unknown until checked against the audio.

The diarization model supplies anonymous speaker IDs; it does not know job roles. Per-language intervals are in `outputs/diarization/pyannote/{arabic,bengali,malayalam,urdu}.json` with RTTM versions beside them. Speaker-labeled raw Whisper drafts are available for Arabic, Bengali, and Urdu in `outputs/reference_transcripts/*_whisper_with_speaker_ids.txt`; Malayalam ASR timestamps were invalid, so its draft was not merged with the pyannote intervals. The ASR excerpts in the CSV are noisy, so use them only to locate speech, not to confirm wording.

## Clips prepared locally

For each language, compare the opening with the nurse interruption. These clips are in `outputs/review_audio/speaker_roles/` and are not committed to Git; original recordings remain outside the repository.

| Language | Opening, 0–13 sec | Nurse interruption, 29–42 sec |
| --- | --- | --- |
| Arabic | `arabic_opening.mp3` | `arabic_nurse_interruption.mp3` |
| Bengali | `bengali_opening.mp3` | `bengali_nurse_interruption.mp3` |
| Malayalam | `malayalam_opening.mp3` | `malayalam_nurse_interruption.mp3` |
| Urdu | `urdu_opening.mp3` | `urdu_nurse_interruption.mp3` |

## Reviewer steps

1. Open the matching language's diarization JSON and row groups in `outputs/task4_speaker_role_review.csv`.
2. Listen to the opening and interruption clips, then use the full recording if needed to confirm recurring voices.
3. Identify the nurse as the voice that interrupts to say the ECG machine is available. Record the ID that voice consistently uses.
4. Map the remaining voices to doctor and patient from the dialogue and consistent voice identity. Mark any uncertain segments instead of forcing a role.
5. Enter the reviewer's name in `role_reviewed_by_human` and add the role mapping and uncertainties in `review_notes` (add this column if needed).

Do not infer roles only from speaker ID ordering. Do not mark the transcript as fully verified from this role check: word accuracy and medical values require the separate language transcript review.
