# Anna Corpus

Digitized works collected from `annavinpadaippugal.info`, including extracted
HTML text, corrected OCR text, bilingual translations, source manifests, audit
reports, and the scripts used to reproduce the corpus.

The primary reader-facing collection is in:

- `outputs/annavin_text_extractor/translated_contents/`

Supporting source collections are in:

- `outputs/annavin_text_extractor/md_pages/`
- `outputs/annavin_text_extractor/ocr_text/`
- `outputs/annavin_text_extractor/ocr_text_corrected/`

## Scan image cache

The local `ocr_images/` directory is approximately 11 GB and is intentionally
excluded from Git because it is a regenerable working cache. Its state manifest
is retained at `outputs/annavin_text_extractor/ocr_images/_state/manifest.jsonl`.
Use `outputs/annavin_text_extractor/extract_page_images.py` to recreate the
cache from the source pages.

See `outputs/annavin_text_extractor/README.md` and
`outputs/annavin_text_extractor/TRANSLATE_ALL_README.md` for extraction and
translation workflows.
