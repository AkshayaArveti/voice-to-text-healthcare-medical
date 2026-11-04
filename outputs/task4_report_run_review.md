# Task 4 report run review

The quantized `Qwen/Qwen2.5-3B-Instruct` report-extraction cell completed on Colab's T4 and produced eight rows: English and requested-language drafts for Arabic, Bengali, Malayalam, and Urdu.

These are **unreviewed experimental drafts**, not validated reports. A spot check found clear failures:

- The Malayalam outputs were generated in Chinese rather than Malayalam or English.
- The Urdu output describes cough and shortness of breath, which conflicts with the consultation script shared in this chat (fever, fatigue, and weight loss). This may indicate a bad ASR transcript or model hallucination; it must be checked against the actual Urdu transcript/audio.
- Some output keys or values differ from the requested schema and include unsupported details.
- The CSV has no populated `sample_id` values, so the rows need language-based identification.

Do not present this run as evidence of clinical accuracy. The next work should be to review and correct each language's transcript against its reference text/audio, then rerun extraction on verified text and inspect both output languages. Keep diagnosis and medication extraction limited to what the verified transcript explicitly says.
