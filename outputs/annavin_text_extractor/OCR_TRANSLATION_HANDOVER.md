# OCR-Origin Translation Handover

Updated: 2026-08-28

## Objective

Complete all 962 canonical OCR-origin works as bilingual Markdown documents:

| Category | OCR target | Translated | Pending |
|---|---:|---:|---:|
| katturaigal | 552 | 539 | 13 |
| nadagangal | 61 | 35 | 26 |
| sirukathaigal | 108 | 108 | 0 |
| sorpozhivugal | 241 | 188 | 53 |
| **Total** | **962** | **870** | **92** |

The authoritative live pending list is:

`translated_contents/_translation_state/ocr_pending_links.md`

Its current split is 50 works needing OCR/source recovery and 42 works whose
OCR source is available but whose bilingual translation is pending. Always
regenerate the report after completing one work; do not rely on the numbers in
this handover after work resumes.

## Repository

- Local root: `/Users/pugazhendhirajendran/Documents/Codex/2026-07-09/https-www-annavinpadaippugal-info`
- GitHub: <https://github.com/pugazg/anna-corpus>
- Branch: `main`
- Git author should be `pugazg`.
- Commit and push completed work frequently. The user has explicitly allowed
  commits and pushes from this workspace without asking again.

## Most Recently Completed Work

`nadagangal/jananayaga_1.md` is complete.

- All 11 scans were visually reconciled.
- Six pages that previously contained no OCR text were recovered by converting
  the grayscale PNG scans to JPEG and rerunning `tam+eng` OCR before visual
  verification.
- The duplicated raw-OCR fragment on Image 9 was removed, Images 10-11 were
  restored, and the complete 1960 ending was retained.
- The bilingual translation preserves the courtroom labels, narrator's direct
  address, and the independent-thought / contagious-disease satire.
- The bilingual source-retention audit passes.
- Its temporary recovery hold has been removed.
- The live pending report has been refreshed from 93 to 92 works.

## Next Work

Select the next work from the live report. There is no partially edited source
after `nadagangal/jananayaga_1.md`. Prefer one of the 42 items under
`OCR translation pending` unless deliberately beginning a complete visual
recovery. The first translation-ready item is now
`sorpozhivugal/muthamizh_manad.md` when prioritizing the shortest remaining
candidate. The preceding items were inspected and moved to source recovery.
`katturaigal/aariyamaayai.htm.md` is the 69-scan Parts 2-7 continuation of the
already translated opening and
contains unreadable mixed-script English citations, especially at Part 5 Image
11 and Part 6 Image 1. `katturaigal/anthikalambagam.md` was likewise moved to
recovery after direct scan checks confirmed recurring corruption across its 12
parts and 122 scans. `sorpozhivugal/aalunar090259.md` requires bilingual re-OCR
of all 20 pages, particularly the destroyed English quotations on Images 8-9.

`report_ocr_pending_links.py` recognises `No OCR text detected` markers. The
current accurate split is 50 recovery / 42 translation, 92 total.

The other explicit recovery hold encountered immediately before this work is
`sorpozhivugal/sattamandram_first.md`; its embedded English was badly damaged by
Tamil-only OCR and needs bilingual re-OCR or visual reconstruction.

## Authoritative Inputs

- Canonical inventory and OCR-origin classification:
  `organized_contents/_merge_state/source_map.csv`
- Corrected OCR sources: `ocr_text_corrected/`
- Original page scans: `ocr_images/`
- Bilingual outputs: `translated_contents/`
- Translation queue: `translated_contents/_translation_state/translation_queue.csv`
- Recovery holds: `translated_contents/_translation_state/needs_source_recovery.csv`
- OCR repair log: `translated_contents/_translation_state/ocr_concerns.csv`
- Difficult terms: `translated_contents/_translation_state/difficult_terms.csv`
- Incorrect sources to skip: `translated_contents/_translation_state/incorrect_sources.csv`
- Bilingual audit: `translated_contents/_translation_state/bilingual_audit.md`
- Category status: `translated_contents/_translation_state/section_translation_status.md`

Never use file counts from the whole translation queue as the OCR-origin count.
The whole archive also contains HTML-origin works. OCR-origin membership is
defined only by `source_map.csv` rows whose `source` is `ocr_replaces_html` or
`ocr_only`.

## Fidelity Rules

1. Visually compare OCR-origin Tamil against every available scan before
   translation. Titles, opening lines, closing lines, page transitions, dates,
   names, figures, quotations, and embedded English require particular care.
2. Correct only errors proven by the scan. Keep period spelling, rhetoric,
   punctuation, and unusual but printed wording. Never modernize the source.
3. The corrected Tamil in `ocr_text_corrected/` becomes the canonical source.
   Copy it verbatim into `## Source Tamil (verbatim)` in the bilingual file.
4. Retain both Tamil and English titles. Translate the entire body, not merely
   the title or catalogue entry.
5. Preserve all image/part boundaries in the source block so fidelity can be
   audited. Handle multipart works as one canonical file when the correction
   pipeline has merged them.
6. Record every scan-proven OCR correction in `ocr_concerns.csv`. Put difficult
   or uncertain translation terms in `difficult_terms.csv`; do not silently
   guess damaged text.
7. A source with missing pages, wrong scans, unreadable passages, or severe
   mixed-language OCR belongs in `needs_source_recovery.csv`. Do not create a
   deceptively complete translation from incomplete text.
8. Files listed in `incorrect_sources.csv` must remain skipped until their
   source issue is genuinely repaired. In particular, do not repeatedly retry
   the known incorrect `பழைய கம்பெனி!` source.
9. For HTML-origin text, preserve the extracted source exactly. OCR correction
   rules apply only to OCR-origin works.

## Required Document Shape

```markdown
# English Title / தமிழ் தலைப்பு

**Tamil title:** தமிழ் தலைப்பு
**English title:** English Title
**Category:** sorpozhivugal
**Source:** <website URL>

## Source Tamil (verbatim)

<complete corrected Tamil source, unchanged>

## English Translation

<complete faithful English translation>

## Translator's Notes

<only useful historical, lexical, or uncertainty notes>
```

Follow established translated files in the same category when metadata or
image-boundary formatting differs slightly.

## Per-Work Completion Cycle

1. Select the next item from `ocr_pending_links.md`. Prefer ordinary
   translation-pending works when no source recovery is already in progress.
2. Inspect the corrected OCR source and every original scan.
3. Repair scan-proven OCR mistakes in `ocr_text_corrected/<category>/<file>.md`.
4. Update `ocr_concerns.csv` with concise page-specific evidence.
5. Translate the complete corrected source into a bilingual file under the
   identical relative path in `translated_contents/`.
6. Remove a recovery hold only when its stated defect is resolved.
7. Run, from `outputs/annavin_text_extractor/`:

   ```bash
   python3 refresh_ocr_translation_state.py
   ```

8. Confirm the completed work disappeared from `ocr_pending_links.md`, its
   category pending count dropped by one, and the audit reports no fidelity
   issue.
9. Run the tests:

   ```bash
   python3 -m unittest discover -s . -p 'test_*.py'
   ```

10. Review the diff, commit, and push to `origin/main`.

The refresh command is mandatory after every completed work. It rebuilds:

- `translation_queue.csv`
- category `CONTENTS.md` files
- `bilingual_audit.md`
- `section_translation_status.csv` and `.md`
- `ocr_pending_links.md`

## Completion Gate

Do not claim the objective is complete until current evidence proves all of the
following:

- OCR-origin translated count is 962/962.
- OCR-origin verified count is 962/962.
- OCR-origin pending count is zero in both the bilingual audit and pending-links
  report.
- All four category totals remain exactly 552, 61, 108, and 241.
- Every bilingual source block exactly matches its canonical corrected source.
- No unresolved OCR/source recovery hold applies to a target counted complete.
- All tests pass.
- Category contents and status files are refreshed and committed.

## Ready-to-Use Prompt for a Normal Chat

```text
Continue the OCR-origin bilingual translation project in this repository:
/Users/pugazhendhirajendran/Documents/Codex/2026-07-09/https-www-annavinpadaippugal-info

Read and follow this handover first:
outputs/annavin_text_extractor/OCR_TRANSLATION_HANDOVER.md

The objective is to complete all 962 canonical OCR-origin works as bilingual
documents while preserving the visually corrected Tamil source verbatim. Use
organized_contents/_merge_state/source_map.csv as the canonical inventory and
translated_contents/_translation_state/ocr_pending_links.md as the live pending
list. Do not mix HTML-origin queue counts into OCR-origin progress.

The most recently completed work is nadagangal/jananayaga_1.md; all 11 scans
were reconciled and its six formerly blank OCR pages were recovered and
translated. Select the next work from the live pending report, preferably from
the OCR translation-pending section. Record scan-proven OCR corrections in
ocr_concerns.csv and do not translate missing or damaged source text by
guessing.

After every single completed work, run
python3 refresh_ocr_translation_state.py from
outputs/annavin_text_extractor/. Confirm that the work disappeared from
ocr_pending_links.md, run all test_*.py tests, review the diff, commit, and push
to origin/main. Continue to the next pending OCR-origin work without waiting for
permission. Preserve both Tamil and English titles and follow every fidelity,
recovery, and completion rule in the handover.
```
