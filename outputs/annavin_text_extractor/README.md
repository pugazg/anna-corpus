# Annavin Padaippugal HTML Text Extractor

This local tool reads `annavinpadaippugal_links.md`, fetches HTML pages, extracts readable text, and writes Markdown files.

Numbered page sequences are combined by default. This works for both `_1/_2` style pages and `_part1/_part2` style pages. For example, these pages:

```text
Kurunavalgal/appothae_sonnaen_1.htm
Kurunavalgal/appothae_sonnaen_2.htm
Kurunavalgal/appothae_sonnaen_3.htm
```

become one Markdown file:

```text
md_pages/Kurunavalgal/appothae_sonnaen.md
```

And these pages:

```text
annavin_english_katturaigal_part1.htm
annavin_english_katturaigal_part2.htm
```

become:

```text
md_pages/english/annavin_english_katturaigal.md
```

## Quick Start

From this folder:

```bash
python3 extract_html_text.py
```

Default input:

```text
../annavinpadaippugal_links.md
```

Default output:

```text
./md_pages/
```

The output folder mirrors the website path. For a single-page item:

```text
http://www.annavinpadaippugal.info/contact.htm
```

becomes:

```text
md_pages/contact.md
```

Some pages on the site are stored at the website root even though the menu places them inside a section. The tool applies small site-specific folder rules for those cases. For example:

```text
http://www.annavinpadaippugal.info/annavin_english_katturaigal_part1.htm
```

becomes:

```text
md_pages/english/annavin_english_katturaigal.md
```

Other root-level section pages are routed into folders such as `kadithangal/`, `katturaigal/`, `sirukathaigal/`, `Kurunavalgal/`, `kavithaigal/`, `nadagangal/`, `navalgal/`, `photos/`, `oviyam/`, and `sorpozhivugal/`.

## Resume After Stopping

You can stop the tool at any time with `Ctrl+C`.

Run the same command again:

```bash
python3 extract_html_text.py
```

Already-created Markdown files are skipped, and unfinished links continue processing. Known failed links and partial combined files are also skipped on normal reruns, so the tool does not sit for a long time retrying broken website URLs.

Progress is recorded here:

```text
md_pages/_extract_state/manifest.jsonl
```

The latest run summary is written here:

```text
md_pages/_extract_state/summary.md
```

The remaining failed or partial items are listed here:

```text
md_pages/_extract_state/known_problems.md
```

## Useful Commands

Test with only the first 10 pages:

```bash
python3 extract_html_text.py --limit 10
```

Use a different output folder:

```bash
python3 extract_html_text.py --out-dir ./my_text_archive
```

Fetch again and overwrite existing Markdown files:

```bash
python3 extract_html_text.py --force
```

Retry links that previously failed:

```bash
python3 extract_html_text.py --retry-failed
```

Use this only when you want to check whether the website has fixed those links. If the site still returns `404 Not Found`, the output is expected and no new Markdown file can be created for that source page.

Retry combined files that were previously partial:

```bash
python3 extract_html_text.py --retry-partial
```

Use a shorter wait for slow pages:

```bash
python3 extract_html_text.py --timeout 5
```

If you use HTTPS links and your local machine rejects the site's certificate, the tool now retries with relaxed certificate checking automatically. You can still force relaxed checking:

```bash
python3 extract_html_text.py --insecure
```

Reduce terminal output:

```bash
python3 extract_html_text.py --quiet
```

Show every skipped and written file:

```bash
python3 extract_html_text.py --verbose
```

Create a separate report for pages with little or no extracted body text, useful for finding scanned/image-only pages:

```bash
python3 extract_html_text.py --scan-no-text
```

By default, that report excludes `oviyam`, `photos`, `contact/contacts`, and `speech_audios` pages.

Adjust the threshold if needed:

```bash
python3 extract_html_text.py --scan-no-text --min-body-chars 250
```

Include all sections in the no-text report:

```bash
python3 extract_html_text.py --scan-no-text --include-all-no-text-sections
```

Keep the old one-file-per-source-page behavior:

```bash
python3 extract_html_text.py --no-combine-numbered-pages
```

## Extract Images For OCR

After creating `no_text_or_scanned_pages.md`, download the images from those source pages:

```bash
python3 extract_page_images.py
```

Default input:

```text
md_pages/_extract_state/no_text_or_scanned_pages.md
```

Default output:

```text
ocr_images/
```

The tool creates grayscale, auto-contrasted PNG files for OCR, organized by section and page:

```text
ocr_images/katturaigal/example_page/001-abcd1234ef.png
```

It is resumable. Progress is stored here:

```text
ocr_images/_state/manifest.jsonl
```

Test with only the first 5 source pages:

```bash
python3 extract_page_images.py --limit 5
```

Also save the original downloaded images:

```bash
python3 extract_page_images.py --save-originals
```

Save only originals, without OCR PNG preparation:

```bash
python3 extract_page_images.py --save-original-only
```

Keep smaller images too:

```bash
python3 extract_page_images.py --include-small
```

## Extract OCR Text

After images are available in `ocr_images/`, run OCR and write Markdown text:

```bash
python3 extract_ocr_text.py
```

Default input:

```text
ocr_images/
```

Default output:

```text
ocr_text/
```

The tool writes one Markdown file per scanned source page:

```text
ocr_text/katturaigal/example_page.md
```

It is resumable. Existing Markdown files are skipped unless you use `--force`.

Test with only a few page folders:

```bash
python3 extract_ocr_text.py --limit-pages 3
```

OCR only selected page folders:

```bash
python3 extract_ocr_text.py --page katturaigal/aangilampol --page katturaigal/aaruthal_kooru
```

The default OCR language is Tamil:

```bash
python3 extract_ocr_text.py --lang tam
```

Use mixed Tamil/English OCR only when needed:

```bash
python3 extract_ocr_text.py --lang tam+eng
```

## Apply OCR Corrections

After OCR text is created, apply reviewed cleanup rules to a separate corrected folder:

```bash
python3 apply_ocr_corrections.py
```

Default input:

```text
ocr_text/
```

Default output:

```text
ocr_text_corrected/
```

The raw OCR Markdown files are not changed. Reports are written under:

```text
ocr_text_corrected/_state/
```

Numbered OCR Markdown files are combined by default during correction. For example:

```text
ocr_text/katturaigal/1858-1948_1.md
ocr_text/katturaigal/1858-1948_2.md
ocr_text/katturaigal/1858-1948_3.md
```

become:

```text
ocr_text_corrected/katturaigal/1858-1948.md
```

Keep numbered files separate only if needed:

```bash
python3 apply_ocr_corrections.py --no-combine-numbered-pages
```

Test selected pages:

```bash
python3 apply_ocr_corrections.py \
  --page katturaigal/aangilampol \
  --page katturaigal/aaruthal_kooru \
  --page katturaigal/anuthabam
```

More detail:

```text
annavin-ocr-guide.md
```

## Merge HTML And OCR Markdown

After HTML extraction, OCR, and OCR correction are complete, create one combined archive:

```bash
python3 merge_markdown_archive.py
```

Default inputs:

```text
md_pages/
ocr_text_corrected/
```

Default output:

```text
merged_md_pages/
```

The merge keeps the website-style folder layout. HTML-extracted Markdown is used
as the base, and OCR-corrected Markdown replaces matching scanned/no-text pages.

By default the merged archive uses relative symlinks, so it is fast and does not
duplicate the large Markdown files. If you need physical copies instead:

```bash
python3 merge_markdown_archive.py --file-mode copy
```

Merge reports are written under:

```text
merged_md_pages/_merge_state/
```

## Notes

- `extract_html_text.py` uses only Python's standard library.
- `extract_page_images.py` needs Pillow for OCR PNG preparation. If Pillow is not installed, run `python3 -m pip install Pillow`, or use `--save-original-only`.
- `extract_ocr_text.py` needs the `tesseract` command with Tamil language data. Check with `tesseract --list-langs | grep tam`.
- If a scan is visibly readable but OCR reports `_No OCR text detected._`, rerun that page with `--normalize-images`. This re-encodes the pixels before Tesseract and also happens automatically as a fallback after an empty first attempt.
- Mixed-language OCR can sometimes read Tamil shapes as English words, so `extract_ocr_text.py` defaults to `tam` instead of `tam+eng`.
- `apply_ocr_corrections.py` preserves raw OCR in `ocr_text/` and writes corrected Markdown to `ocr_text_corrected/`.
- `merge_markdown_archive.py` writes the final combined archive to `merged_md_pages/`.
- The image extractor reads `no_text_or_scanned_pages.md` by default, so it follows the same exclusions you requested for `oviyam`, `photos`, `contact/contacts`, and `speech_audios`.
- Image download progress is recorded in `ocr_images/_state/manifest.jsonl`; run the same command again to continue after stopping.
