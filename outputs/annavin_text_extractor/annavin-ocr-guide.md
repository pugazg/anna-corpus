# Annavin OCR Correction Workflow

This mirrors the useful parts of the Kalaignar/Murasoli OCR pipeline, adapted for
the Annavin Markdown archive.

## Flow

```text
no_text_or_scanned_pages.md
  -> extract_page_images.py
  -> ocr_images/
  -> extract_ocr_text.py
  -> ocr_text/
  -> apply_ocr_corrections.py
  -> ocr_text_corrected/
  -> merge_markdown_archive.py
  -> merged_md_pages/
```

## Why Correction Is Separate

OCR creates text. Correction edits text. Keeping those stages separate gives us:

- raw OCR preserved in `ocr_text/`
- corrected Markdown in `ocr_text_corrected/`
- audit reports under `ocr_text_corrected/_state/`
- no silent file loss: every source Markdown file is written to the corrected folder

## Run

From this folder:

```bash
python3 extract_page_images.py
python3 extract_ocr_text.py
python3 apply_ocr_corrections.py
```

## Correction Inputs

Reusable token corrections:

```text
reference_verified_source_dictionary/automatic_corrections.csv
```

Page-specific, human-reviewed corrections:

```text
curated/annavin-ocr-overrides.json
```

Starter OCR pattern notes:

```text
reference_verified_source_dictionary/ocr_patterns.json
```

Starter trusted terms for a future dictionary loop:

```text
reference_verified_source_dictionary/trusted_seed.json
```

## Reports

After correction:

```text
ocr_text_corrected/_state/summary.md
ocr_text_corrected/_state/correction_report.csv
ocr_text_corrected/_state/correction_events.csv
ocr_text_corrected/_state/review_candidates.csv
```

`review_candidates.csv` is where suspicious leftovers go, such as Latin tokens
inside Tamil OCR lines or invalid Tamil vowel-sign sequences.

## Final Merge

Run:

```bash
python3 merge_markdown_archive.py
```

The merge uses `md_pages/` as the base and lets `ocr_text_corrected/` replace
matching scanned/no-text pages. The final folder is:

```text
merged_md_pages/
```

Reports are in:

```text
merged_md_pages/_merge_state/
```

The default merge uses relative symlinks for speed. Use `--file-mode copy` if
you need a physical duplicate of every Markdown file.

## Numbered Pages

The raw OCR stage writes one file per scanned HTML page. If the website has a
numbered sequence like:

```text
ocr_text/katturaigal/1858-1948_1.md
ocr_text/katturaigal/1858-1948_2.md
ocr_text/katturaigal/1858-1948_3.md
```

the correction stage combines those into one final Markdown file:

```text
ocr_text_corrected/katturaigal/1858-1948.md
```

This also works for `_part1/_part2` style names. The report records all source
files in `source_files`.

## Testing A Few Pages

```bash
python3 apply_ocr_corrections.py \
  --page katturaigal/aangilampol \
  --page katturaigal/aaruthal_kooru \
  --page katturaigal/anuthabam
```

The script writes to `ocr_text_corrected/` and leaves `ocr_text/` unchanged.
