# Translate All Markdown Files

`translate_all_markdown.py` translates the archive in both directions:

- Tamil source to corrected Tamil plus English translation.
- English source to corrected English plus Tamil translation.

The output mirrors the folders under `organized_contents/` and is written to
`translated_contents/`. Existing completed files are skipped. Progress is stored
in `_translation_state/translation_manifest.jsonl`, so an interrupted run resumes.

## Setup

Set the API key in the terminal. Do not put it in a source file:

```bash
export OPENAI_API_KEY="your-key"
```

## Test first

```bash
cd /Users/pugazhendhirajendran/Documents/Codex/2026-07-09/https-www-annavinpadaippugal-info/outputs/annavin_text_extractor
python3 translate_all_markdown.py --limit 3
```

Review those translations and the difficult-terms register before launching the
complete collection.

## Local spending guard

OpenAI project budgets are notification thresholds rather than hard caps. The
runner can stop between files when its recorded API cost reaches a chosen amount:

```bash
python3 translate_all_markdown.py --model gpt-5.6-luna --max-cost-usd 25
```

The guard uses token usage returned by the API. A single file already in progress
can take the recorded total slightly above the chosen amount. Re-running with a
higher amount resumes from completed files.

## Translate the complete archive

```bash
python3 translate_all_markdown.py
```

The default model is `gpt-5.6-terra`. Override it when needed:

```bash
python3 translate_all_markdown.py --model gpt-5.6-luna
```

Use `--dry-run` to inspect classification without making API requests. Pages with
no usable source body are written to
`translated_contents/_translation_state/needs_source_recovery.csv`.
