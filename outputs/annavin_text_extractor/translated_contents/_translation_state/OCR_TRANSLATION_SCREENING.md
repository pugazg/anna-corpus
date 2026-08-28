# OCR Translation Candidate Screening

Updated: 2026-08-28

This is a durable screening log for OCR-origin works that are still listed under
`OCR translation pending` but fail the source-fidelity gate when their corrected
OCR Markdown is inspected. It prevents repeated selection of known-bad candidates
before the generated translation-state files are reconciled locally.

The canonical generated state remains `ocr_pending_links.md`; this file does not
replace `refresh_ocr_translation_state.py` or the recovery CSV.

## Screened after `sorpozhivugal/muthamizh_manad.md`

### `sorpozhivugal/manamakkalukku.md`

**Disposition:** source/OCR recovery required before translation.

- Part 1 / Image 2 begins with visibly destroyed Tamil OCR:
  `டங்கள் மிகவும் சுகாதாரமற்றும் கிடப்பதும் நல்லத்?`
  followed by the disconnected line `ப்ப த் திற தும் 8 ்`.
- The damage occurs inside a continuing sentence describing the unsanitary
  surroundings of workers' dwellings, so the missing wording cannot be inferred
  safely from context.
- Do not translate this work until the linked source scan/page is visually
  reconciled and the canonical corrected OCR is repaired.

### `sorpozhivugal/nambikkai301057.md`

**Disposition:** source/OCR recovery required before translation.

- Part 1 / Image 1 contains severe mixed-glyph corruption in the opening
  Legislative Assembly remarks, including multiple disconnected lines after
  `இந்தச் சடை` and before Image 2.
- The corruption removes substantive wording rather than merely punctuation or
  spacing, so a faithful English translation cannot be produced from the current
  canonical OCR.
- Reconcile the affected scan(s) and repair the Tamil source before translation.

### `sorpozhivugal/300367.md`

**Disposition:** source/OCR recovery required before translation.

- Part 1 / Image 1 starts with a long spurious OCR-noise line before the speech
  metadata: `பபப ய ட 2 3௮0ட அள வத்தில் து பவதி ல்கதகைதைகை அலை`.
- The same opening pages contain recurrent substitutions and broken words in the
  Governor's-address debate text.
- The linked scans must be visually reconciled before this work can be treated as
  translation-ready.

### `sorpozhivugal/270667.md`

**Disposition:** source/OCR recovery required before translation.

- Part 1 / Image 1 begins with corrupted header noise and includes obvious OCR
  substitutions in the opening budget-debate text.
- Part 1 / Image 2 contains additional malformed words and a damaged continuation
  near the end of the visible OCR segment.
- Visually reconcile the source scans and repair the canonical text before
  translation.

## Workflow note

When local reconciliation is next run, transfer these dispositions into the
normal recovery state (`needs_source_recovery.csv` and related reason fields as
appropriate), run `refresh_ocr_translation_state.py`, and remove any entries from
this screening log once the generated state fully represents them.
