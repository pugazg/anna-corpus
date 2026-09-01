# OCR-Origin Translation Handover

Updated: 2026-09-01

## Objective

Complete all 962 canonical OCR-origin works as bilingual Markdown documents:

| Category | OCR target | Translated | Pending |
|---|---:|---:|---:|
| katturaigal | 552 | 543 | 9 |
| nadagangal | 61 | 35 | 26 |
| sirukathaigal | 108 | 108 | 0 |
| sorpozhivugal | 241 | 196 | 45 |
| **Total** | **962** | **882** | **80** |

The authoritative live pending list is:

`translated_contents/_translation_state/ocr_pending_links.md`

Its current split is 80 works needing OCR/source recovery and no works whose
OCR source is currently safe enough for bilingual translation. Always
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

`katturaigal/ilamayil_muthumai.md` (`இளமையில் முதுமை!` / `Old Age in Youth!`) is complete.

- The complete 25 January 1948 issue of `திராவிட நாடு`, vol. 6 no. 33, was
  recovered from the Tamil Digital Library and used as the independent print witness.
- Printed pages 8-12 prove that archive Image 4 joins directly to Image 7. Images
  5-6 are an incomplete, unrelated Jayaprakash Narayan article and were excluded.
- All thirteen relevant archive scans were visually reconciled before translation.
- The corrected Tamil source is preserved verbatim in the canonical bilingual file.
- The six-line parody, both Purananuru passages, the names and the printed English
  phrase `(Over Centralisation)` were restored directly from the scans.
- Difficult or uncertain readings including `கல்லா இளமை`, `மீரா`, `பல தேவர்`,
  the political `அஜீரணம்` metaphor and `துரைத்தனம்` are recorded separately.
- The bilingual source-retention audit passes with zero issues; all 15 tests pass.
- Commit `570376a` contains the final English-draft checkpoint; the canonical
  completion commit follows this handover update.
- The live pending report has been refreshed to 80 works.

## Next Work

Continue source recovery for `katturaigal/kambarasam.md`, the first work in the
refreshed live pending list. It spans 127 scans across thirteen parts. Earlier
representative checks established recurring corruption in prose, quoted Kamba
Ramayana verses, glosses, names and dialogue; only bounded readings and the
closing ornament have been restored. Reconcile every scan before translation,
preserve every verse and gloss exactly, and checkpoint the long recovery in
small batches. Do not translate unreconciled passages by context.

Parts 1-3 are now fully reconciled directly against all 31 scans. The opening
five doses, their quoted Kamba Ramayana verses and glosses, dialogue, section
ornaments and page joins have been restored without context-only
reconstruction. Part 4 Images 1-5 were then checked. Images 4 and 5 are exact
duplicates, and the resulting absent page between Images 3 and 4 was recovered
from visually checked Wikisource PDF pages 54-56 and cross-checked with Project
Madurai; the duplicate OCR block was removed. Recovery coverage is 36/127 image
slots (35 distinct scans plus one duplicate). The remaining five Part 4 scans
were then fully reconciled, including the செவிலி மங்கையர் and X-ray passages.
Recovery coverage is 41/127 image slots (40 distinct scans plus one duplicate);
Part 5's ten scans were then fully reconciled, including the பந்தலிலே பாவக்கா
folk-song passage, the குங்கும மலை and கண் கலுழி ஆறு verses with their glosses,
and the Dose 8 transition. Recovery coverage is 51/127 image slots (50 distinct
scans plus one duplicate). Part 6's ten scans were then fully reconciled,
including the complete Godiva dialogue, both printed Tennyson excerpts and the
opening comparison with the நைடதம். Recovery coverage is 61/127 image slots
(60 distinct scans plus one duplicate); continue with Part 7 Image 1. No
translation has begun, and the 66 image slots in Parts 7-13 remain in source
recovery.

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

Those four commits were pushed to `origin/main`. Three more long works were
then screened directly against representative scans from every part and moved
to recovery:

- `katturaigal/periyapuranaputhayal.md` (70 scans, seven parts): restored the
  printed date, list numbering, bounded village and astronomical readings,
  ornament rows and closing numbering; commit `c4e2c02`.
- `nadagangal/vaelaikari.md` (94 scans, ten parts, 54 scenes): restored bounded
  character-list, `(Fire Engine)`, opening scene and concluding speaker/wording
  readings, but pervasive dialogue and structural damage remains; commit
  `6bdb41c`.
- `nadagangal/oar_iravu.md` (96 scans, ten parts, 49 scenes): restored the
  `ஓர் இரவு` title, three character-list readings, Scenes 1-4 and bounded
  conclusion readings, but corruption recurs throughout; commit `e6ec659`.

All seven screening commits were pushed to `origin/main`. The final two
translation-ready works were then screened and moved to recovery:

- `katturaigal/romapuri_ranigal.md` (82 scans, eight parts): representative
  scans from every part proved recurring historical-name, quotation and prose
  corruption; bounded scan-visible readings and ornaments were restored;
  commit `a68d257`.
- `katturaigal/kambarasam.md` (127 scans, thirteen parts): representative scans
  from every part proved recurring corruption in prose, quoted Kamba Ramayana
  verses, glosses, names and dialogue; bounded readings and the closing ornament
  were restored; commit `c71d60a`.

The authoritative OCR-only state is 882/962 complete, 80 pending, all 80 in
source recovery and zero translation-ready. All 15 tests pass and the bilingual
audit has zero issues. Items found incomplete or unreliable must be recovered
rather than translated by guesswork.

`report_ocr_pending_links.py` recognises `No OCR text detected` markers. The
current accurate split is 80 recovery / 0 translation, 80 total. The recovery
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

The authoritative OCR-only state is 881/962 complete and 81 pending. All 81
pending works require OCR or source recovery; there are currently no
translation-ready OCR-origin works. `katturaigal/anthikalambagam.md` is the most
recently completed work: all 122 scans across twelve parts were visually
reconciled, the complete dialogue collection was translated as `Twilight
Medley`, and the bilingual audit passes. Screen
`katturaigal/ilamayil_muthumai.md` next. Its current 15-scan sequence is missing
at least one page between Images 4 and 5, and the live webpage has the same gap.
Search for a reliable recovery witness for the missing Jayaprakash Narayan
discussion. Record scan-proven OCR corrections in ocr_concerns.csv and do not
translate missing or damaged source text by guessing.

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
