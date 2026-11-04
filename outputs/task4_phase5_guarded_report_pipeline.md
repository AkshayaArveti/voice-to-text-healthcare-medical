# Phase 5 — Guarded bilingual clinical extraction

Prepared `TASK_4_Clinical_Report_Generation_Guarded.ipynb` as the report-generation implementation. It uses the recovered fine-tuned Qwen2.5-1.5B adapter, quantized to 4-bit on a Colab GPU, and produces English plus the source-language report across the existing 12 fields.

## Safety gates in the notebook

- Requires `transcript_status=verified`, a named fluent reviewer, and `speaker_roles_verified=yes` for every input row.
- Accepts only Arabic, Bengali, Malayalam, or Urdu.
- Skips an input longer than the configured context instead of silently truncating it.
- Requests valid JSON with exactly the 12 report fields, source-language text, and a short verbatim evidence quote for each field.
- Preserves prompt/output token counts, generation time, and peak allocated GPU memory.
- Marks malformed output as requiring review; every valid response remains a draft for human review.

The adapter was recovered from the existing Google Drive `qwen_clinical_finetuned_3k/final_adapter` folder and saved locally as `outputs/final_adapter.zip` (67.2 MB). Its `adapter_config.json` names `unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit` as the base model. I updated the notebook to load that exact model/adapter pair. The notebook remains unrun because no completed, fluent-reviewed transcript-and-role CSV is available yet. Running the known-bad prior Qwen3B output again would not validate this guarded path.

## Required CSV

`verified_transcripts.csv` must contain `sample_id`, `language`, `verified_transcript`, `transcript_status`, `transcript_reviewer`, and `speaker_roles_verified`. Use `[DOCTOR]`, `[PATIENT]`, and `[NURSE]` labels only after confirming them by listening. Package the matching Task 3 `final_adapter` folder as `final_adapter.zip`.
