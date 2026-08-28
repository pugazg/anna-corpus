# Translation Guide

## Output format

- Retain both Tamil and English titles.
- For Tamil originals, keep the source Tamil verbatim before the English translation.
- For English originals, keep the source English verbatim before the Tamil translation.
- Preserve the source URL, category, publication details, and dates.
- Mirror the folder and filename used by `organized_contents/`.
- Correct words only in OCR-extracted source text, and only when the correction is
  supported by the page image or reliable context. Record every OCR repair in a
  translator's note and the difficult-terms register.
- For HTML-extracted source text, preserve the source exactly. Do not modernize or
  normalize spelling, punctuation, spacing, grammar, sandhi, or typography.
- Record difficult words, idioms, historical terms, and uncertain renderings in
  `_translation_state/difficult_terms.csv` with their original context.
- Never silently guess when damaged text cannot be recovered.

## Translation direction

- Tamil source: Tamil to English.
- English source: English to Tamil.
- Mixed-language source: preserve quoted material in its original language and
  translate the main text into the other language.

## Translation style

- Prefer faithful, natural English over word-for-word English.
- Preserve Anna's rhetoric, repetition, direct address, humour, and political tone.
- Retain historically meaningful names and organization names consistently.
- Explain culturally specific language only when English readers would otherwise
  miss an important implication.
- Reuse approved glossary choices only when the sense and context match; never
  apply a global word replacement without checking the sentence.

## Required document structure

```markdown
# English Title

**Tamil title:** தமிழ் தலைப்பு
**English title:** English Title
**Category:** Category
**Source:** <source URL>

## Source Tamil (verbatim)

...

## English Translation

...

## Translator's Notes

...
```

## Required per-work checkpoint

After completing and verifying every individual work, run this from
`outputs/annavin_text_extractor/`:

```bash
python3 refresh_ocr_translation_state.py
```

This refreshes the resumable queue, category `CONTENTS.md` files, bilingual
audit, category status tables, and `_translation_state/ocr_pending_links.md`.
Do not postpone this until the end of a batch: the pending-links report must
lose the completed work immediately, so a fresh chat can trust it after an
interruption.

Before committing, confirm that the completed file is absent from
`_translation_state/ocr_pending_links.md` and that its source-retention audit
passes.
