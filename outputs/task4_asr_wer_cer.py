#!/usr/bin/env python3
"""Score saved ASR hypotheses against fluent-reviewed references (WER/CER)."""
import argparse
import csv
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_REFS = ROOT / "task4_verified_references_template.csv"
DEFAULT_W3 = ROOT / "whisper_large_v3_results.csv"
DEFAULT_COMPARISON_ZIP = ROOT / "task4_stage2_comparison_results.zip"
DEFAULT_OUTPUT = ROOT / "task4_asr_wer_cer_results.csv"


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_hypotheses(whisper_csv, comparison_zip):
    hypotheses = {}
    for row in read_csv(whisper_csv):
        sid = row.get("sample_id", "").strip().lower()
        hypotheses.setdefault(sid, {})["openai_whisper_large_v3"] = row.get("transcript", "")
    with zipfile.ZipFile(comparison_zip) as archive:
        with archive.open("asr_model_comparison_drafts.csv") as raw:
            text = raw.read().decode("utf-8-sig")
        for row in csv.DictReader(io.StringIO(text)):
            sid = row.get("language", "").strip().lower()
            hypotheses.setdefault(sid, {})["whisperx_large_v3_turbo"] = row.get("whisperx_large_v3_turbo_draft", "")
            hypotheses[sid]["seamless_m4t_v2_large"] = row.get("seamless_m4t_v2_large_draft", "")
    return hypotheses


def normalize(s):
    s = unicodedata.normalize("NFC", str(s or "")).casefold()
    # Remove Arabic vocalization marks/tatweel only; Indic combining marks can
    # encode essential vowels and must be retained.
    s = s.replace("\u0640", "")
    s = re.sub(r"[\u064b-\u065f\u0670]", "", s)
    chars = []
    for ch in s:
        if unicodedata.category(ch).startswith("P"):
            chars.append(" ")
        else:
            chars.append(ch)
    return re.sub(r"\s+", " ", "".join(chars)).strip()


def edit_distance(a, b):
    # Memory-efficient Levenshtein distance.
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def score(reference, hypothesis):
    ref_norm, hyp_norm = normalize(reference), normalize(hypothesis)
    ref_words, hyp_words = ref_norm.split(), hyp_norm.split()
    # CER excludes spaces; Unicode code points are counted after NFC.
    ref_chars = list(ref_norm.replace(" ", ""))
    hyp_chars = list(hyp_norm.replace(" ", ""))
    wer = edit_distance(ref_words, hyp_words) / len(ref_words) if ref_words else None
    cer = edit_distance(ref_chars, hyp_chars) / len(ref_chars) if ref_chars else None
    return wer, cer, len(ref_words), len(hyp_words)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--references", type=Path, default=DEFAULT_REFS)
    ap.add_argument("--whisper-large-v3", type=Path, default=DEFAULT_W3)
    ap.add_argument("--comparison-zip", type=Path, default=DEFAULT_COMPARISON_ZIP)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()
    references = {r.get("sample_id", "").strip().lower(): r for r in read_csv(args.references)}
    hypotheses = load_hypotheses(args.whisper_large_v3, args.comparison_zip)
    models = ["whisperx_large_v3_turbo", "seamless_m4t_v2_large", "openai_whisper_large_v3"]
    rows = []
    for sid, ref in references.items():
        lang = ref.get("language", "")
        ref_text = ref.get("reference_text", "").strip()
        status = ref.get("review_status", "").strip().lower()
        reviewer = ref.get("reviewer", "").strip()
        valid = bool(ref_text and reviewer and status == "verified")
        for model in models:
            hyp = hypotheses.get(sid, {}).get(model, "")
            wer, cer, ref_words, hyp_words = (None, None, 0, 0)
            score_status = "reference_pending"
            if valid and not hyp.strip():
                score_status = "hypothesis_missing"
            elif valid:
                wer, cer, ref_words, hyp_words = score(ref_text, hyp)
                score_status = "scored" if wer is not None and cer is not None else "empty_normalized_reference"
            rows.append({
                "sample_id": sid, "language": lang, "model": model,
                "score_status": score_status,
                "review_status": ref.get("review_status", ""),
                "reviewer": reviewer,
                "reference_words": ref_words, "hypothesis_words": hyp_words,
                "wer": "" if wer is None else f"{wer:.6f}",
                "cer": "" if cer is None else f"{cer:.6f}",
                "reference_text": ref_text if valid else "",
            })
    fields = ["sample_id", "language", "model", "score_status", "review_status", "reviewer",
              "reference_words", "hypothesis_words", "wer", "cer", "reference_text"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"Wrote {args.output}")
    print("Scores are blank unless the reference row is marked verified and has a reviewer.")
    print(f"Scored rows: {sum(r['score_status']=='scored' for r in rows)} / {len(rows)}")


if __name__ == "__main__":
    main()
