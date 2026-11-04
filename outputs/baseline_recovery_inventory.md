# Phase 1 — Baseline recovery inventory

Status: **baseline files inspected; configuration discrepancy found; recovery decision pending.** No replacement model was trained in this phase.

## Existing baseline notebook

- Notebook: `TASK_3_ (1).ipynb` (26 cells; located in Downloads).
- The code names the base model `unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit`, loads it with Unsloth and `load_in_4bit=True`, and sets `max_seq_length=2048`.
- A cell prints “Loading Qwen2.5-7B-Instruct...”, but the configured model ID is **Qwen2.5-1.5B-Instruct**, not 7B. The previous baseline must therefore not be reported as a 7B run unless the checkpoint is separately verified.
- Fine-tuning uses LoRA (rank 16, alpha 16; attention and MLP projection modules), 3,000 shuffled training examples, one epoch, seed 3407, FP16 and gradient checkpointing. The notebook reports 24,000 train, 3,000 validation, and 3,000 test examples from `AmareshHebbar/clinical-summarizer-sft`.
- The notebook output records a Tesla T4 with about 14.56 GiB available GPU memory. The Drive output path is `/content/drive/MyDrive/qwen_clinical_finetuned_3k`; outputs list checkpoints 200, 300, and 375 plus `final_adapter`.
- The final example asks for a SOAP summary. The new project instructions specify a 12-field report format, so the Task 4 format still needs to follow the new instructions while documenting SOAP as the prior baseline prompt.

## Existing baseline evaluation and limitations

- The notebook includes a base-versus-fine-tuned comparison on 10 test examples with ROUGE-1/2/L. Its final printed values are base 0.3630/0.2094/0.2404 and fine-tuned 0.3979/0.3541/0.3619. These are the notebook's recorded values, not an independently reproduced evaluation.
- Another score block in the same notebook prints a different set of ROUGE values. Reconcile which run produced each set before citing baseline metrics.
- No multilingual, ASR, medical-term, number-preservation, translation, or qualified-human clinical evaluation is present in this baseline notebook.

## Other files and work found

- Task 4 notebooks in the local `outputs/` folder: `TASK_4_Stage_1_ASR_Diarization.ipynb` and `TASK_4_Multilingual_Clinical_Benchmark.ipynb`.
- Task 4 outputs include WhisperX/Seamless draft transcripts, diarized speaker-turn drafts, a blank speaker-role review CSV, and an experimental Qwen 3B report CSV. The report experiment contains clear language/content errors and is not a valid result.
- No fluent-reviewed regional reference transcript was found in the local outputs. The audio recordings were processed in Colab, but the reference scripts and a dataset split manifest are missing from the current workspace.
- Task 1 and Task 2 PDFs were referenced via temporary WhatsApp paths that are no longer present, so their requirements could not be checked.

## Drive structure prepared

Created `My Drive/Medical_Summarization_Project/` with the requested baseline, dataset, ASR, transcript verification, model evaluation, prompt optimization, fine-tuning, final evaluation, comparison, report, and notebook folders, including the requested language/model subfolders.

## Reuse and recovery decision

1. Preserve the Task 3 notebook and its Drive checkpoints as the historical baseline.
2. Correct the baseline identity in documentation: current notebook code indicates Qwen2.5-1.5B, not Qwen2.5-7B.
3. Before Phase 2, verify which checkpoint was intended and resolve the duplicate ROUGE reports. Do not overwrite or retrain the existing adapter.
4. Reattach Task 1/Task 2 PDFs if their requirements must be included in the recovery record.
