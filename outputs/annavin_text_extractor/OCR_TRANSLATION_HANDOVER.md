# OCR-Origin Translation Handover

Updated: 2026-08-30

## Objective

Complete all 962 canonical OCR-origin works as bilingual Markdown documents:

| Category | OCR target | Translated | Pending |
|---|---:|---:|---:|
| katturaigal | 552 | 539 | 13 |
| nadagangal | 61 | 35 | 26 |
| sirukathaigal | 108 | 108 | 0 |
| sorpozhivugal | 241 | 196 | 45 |
| **Total** | **962** | **878** | **84** |

The authoritative live pending list is:

`translated_contents/_translation_state/ocr_pending_links.md`

Its current split is 79 works needing OCR/source recovery and 5 works whose
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

`sorpozhivugal/1967.md` is complete.

- All 28 relevant scans were visually reconciled; two unrelated inserted Rajya
  Sabha scans remain documented and excluded.
- The date, Justice Party footnote, English quotations, institutional names,
  degrees, vote counts and other damaged readings were recovered and verified.
- The complete speech was translated and promoted from its checkpointed draft.
- The bilingual source-retention audit passes.
- The live pending report has been refreshed to 84 works.

## Next Work

Screen `katturaigal/periyapuranaputhayal.md` next. It is one of the five works
remaining under `OCR translation pending`, with 70 scans across six mapped web
parts. There is no partial draft.

In the latest continuation, four complete but unreliable sources were moved to
recovery after direct scan checks:

- `katturaigal/viduthalaippor.md` (33 scans, three parts): corrected the printed
  date, `(Dravidian League)`, the `4 1/2 கோடி` figure and a scan-absent inserted
  line; commit `eafbcc2`.
- `katturaigal/ulaga_periyar.md` (45 scans, two parts): restored the printed
  title date and bounded funeral facts, but its opening chronological table and
  prose require full recovery; commit `e5107cb`.
- `nadagangal/chandrodhayam.md` (62 scans, seven parts, 26 scenes): restored
  bounded character-list, dialogue and closing readings, but corruption recurs
  throughout the play; commit `371d450`.
- `katturaigal/latchiya_varalaru.md` (58 scans, six parts): corrected the title
  date and opening word and removed three scan-absent noise insertions; commit
  `bc6b082`.

All four commits were pushed to `origin/main`. The authoritative OCR-only state
is 878/962 complete, 84 pending, split into 79 recovery and 5 translation-ready.
All 15 tests pass and the bilingual audit has zero issues. Items found
incomplete or unreliable must be moved to source recovery rather than
translated by guesswork.

`report_ocr_pending_links.py` recognises `No OCR text detected` markers. The
current accurate split is 79 recovery / 5 translation, 84 total. The recovery
count now correctly includes two canonical files already marked as incorrect
sources; this is a classification correction, not a new source defect.

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

The GitHub page the user watches is therefore updated by every completed-work
commit:

<https://github.com/pugazg/anna-corpus/blob/main/outputs/annavin_text_extractor/translated_contents/_translation_state/ocr_pending_links.md>

## Interruption and Weekly-Limit Protocol

The weekly limit may end without warning. Keep the repository resumable at all
times:

1. Translate in scan-sized batches and save an incomplete English translation
   only under `translated_contents/_translation_state/working/`. State the last
   completed part/image and the exact next image at the top of that file.
2. Never place a partial work at its canonical path under
   `translated_contents/<category>/`; that path means the whole bilingual work
   is complete and audit-ready.
3. After each batch, commit and push the working draft and any scan-proven OCR
   corrections. A partial checkpoint must not refresh or reduce pending counts.
4. After the whole work is complete, build the canonical bilingual file, run
   `python3 refresh_ocr_translation_state.py`, verify that the work disappeared
   from `ocr_pending_links.md`, run tests, then commit and push all related files
   together.
5. Before stopping, update the `Next Work` section of this handover with the
   exact completed boundary, next scan, unresolved readings, test result, and
   latest commit. If the limit ends before that edit, the header in the working
   draft is the fallback checkpoint.

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

The most recently completed canonical work is
sorpozhivugal/annal_nabi.md. All 27 scans across its two parts were visually
reconciled, the complete collection was translated, and the bilingual audit
passes. There is no partial working draft. `sorpozhivugal/desiya131159.md` was
screened next and moved to source recovery: its 22 scans are present, but
Tamil-only OCR destroyed the English quotation on Image 3 and substantial
Tamil across Images 1 and 3-5, with recurring corruption elsewhere.
`sorpozhivugal/nilaseer200460.md` was then moved to recovery because its 22-page
Land Reform Bill speech is corrupted from the title and date through figures,
legal argument and closing clauses. `sorpozhivugal/satta_17_07_1957.md` was
also moved to recovery after its two-speech structure was established and
three destroyed English passages were confirmed directly from the scans.
`sorpozhivugal/nattu_mathip111157.md` was then moved to recovery after direct
comparison confirmed corruption from its title and English subtitle through
the final pages. `sorpozhivugal/210367.md` was likewise moved to recovery after
its three-speech structure and two destroyed English quotations were verified
from the scans. `sorpozhivugal/230367.md` was then moved to recovery after its
three-speech structure, missing Speech 7 header, destroyed English quotation,
and extensive Tamil losses were verified from the scans. Screen
`sorpozhivugal/230868.md` next. Record scan-proven OCR corrections in
ocr_concerns.csv and do not translate missing or damaged source text by
guessing.

After every single completed work, run
python3 refresh_ocr_translation_state.py from
outputs/annavin_text_extractor/. Confirm that the work disappeared from
ocr_pending_links.md, run all test_*.py tests, review the diff, commit, and push
to origin/main. This refresh is what updates the GitHub pending-links page the
user is monitoring. Commit and push partial working-draft checkpoints too, but
do not reduce pending counts until a complete canonical bilingual work passes
the audit. Continue to the next pending OCR-origin work without waiting for
permission. Preserve both Tamil and English titles and follow every fidelity,
recovery, interruption, and completion rule in the handover.
```
