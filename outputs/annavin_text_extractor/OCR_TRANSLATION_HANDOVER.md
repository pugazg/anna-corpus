# OCR-Origin Translation Handover

Updated: 2026-09-09

## Objective

Complete all 962 canonical OCR-origin works as bilingual Markdown documents:

| Category | OCR target | Translated | Pending |
|---|---:|---:|---:|
| katturaigal | 552 | 547 | 5 |
| nadagangal | 61 | 35 | 26 |
| sirukathaigal | 108 | 108 | 0 |
| sorpozhivugal | 241 | 196 | 45 |
| **Total** | **962** | **886** | **76** |

The authoritative live pending list is:

`translated_contents/_translation_state/ocr_pending_links.md`

Its current split is 76 works needing OCR/source recovery and no works whose
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

`katturaigal/latchiya_varalaru.md` (`இலட்சிய வரலாறு` / `History of an Ideal`) is complete: all six parts and 58 scans translated and comparatively reviewed. Tamil retention is exact; retained-body SHA-256: `19bed4883353f09abe79e4d295b0a7a311c8f16504f2c641bd9758d5114afb35`. Translator notes and difficult-term records preserve printed anomalies and uncertain interpretations separately. Recovery hold released; state refreshed to 885/962 OCR-origin works verified, 77 pending. The work is absent from the pending list. Audit: zero issues; all 15 tests pass.

## Previous Recovery Completion

`katturaigal/pazhaya_company.md` (`பழைய கம்பெனி!` / `The Old Company!`) is now complete. The five-paragraph newspaper article is translated in full, with its page/column boundary and recovered Tamil retained verbatim. User screenshots and RMRL viewer page 9 establish the source. The unrelated Roosevelt fragment remains preserved separately and incomplete; all old scans remain. First-column punctuation concerns and variant reprint readings are documented in translator notes. State refreshed: 884/962 OCR-origin works verified, 78 pending; this work is absent from the pending list. Audit: zero issues. All 15 tests pass after replacing the obsolete permanent-hold assertion with recovery and fragment-preservation checks. Retained-source SHA-256: `65914f946d741cffe9ac37f2b672eb5811cce693554da105ebf8ca2420a72b7b`.

## Previously Completed Work

`katturaigal/kambarasam.md` (`கம்பரசம்` / `Kamban’s Nectar`) is complete.

- All thirteen parts have complete English translations, approximately 39,363 words.
- All 127 archive slots were reconciled: 126 distinct scans plus one exact duplicate.
  The missing Part 4 passage was recovered from the visually checked Wikisource
  witness and cross-checked against Project Madurai; duplicate text is not repeated.
- The corrected Tamil body is retained verbatim, including all thirteen part
  headings and 126 retained image sections. Retained-body SHA-256:
  `e1fb347b5801b410b6ef53a1f0575d1ebb639fcbe101eede6776a483ae6c14c9`.
- Translator notes explain lexical uncertainties, variant names, the differing
  ornament descriptions, unusual printed dialogue and the Pampa transition.
- The recovery hold is resolved. State was refreshed; Kambarasam is absent from
  both the OCR pending list and recovery holds. Audit: zero issues. All 15 tests pass.
- Final full-English draft checkpoint: `934a15e`; the canonical completion commit
  contains the bilingual document and refreshed state: `a8ea47c`, pushed to origin/main.

## Next Work

Continue source recovery with `katturaigal/periyapuranaputhayal.md` (பெரிய புராணப் புதையல்), the first remaining OCR-origin work. All seven parts and 70 scans are locally present; the pending report lacks a live link for Part 5 but its ten scans exist. Reconcile all scans before translation, starting Part 1 Image 1. Part 1 Images 1–11 and Part 2 Images 1–10 and Part 3 Images 1–10 and Part 4 Images 1–10 and Part 5 Images 1–10 and Part 6 Images 1–10 and Part 7 Images 1–9 are visually compared (70/70; Part 2 Image 1 and Part 5 Image 3 printer footers remain unresolved); resolve those two footer readings before source release and complete translation. English working draft now covers all 11 Part 1 images and the prose/examples/dialogue of Part 2 Images 1–10, plus all 10 Part 3 images and all 10 Part 4 images, plus all Part 5 prose and Part 6 Images 1–2. The Part 2 Image 1 and Part 5 Image 3 printer footers are explicitly unresolved in the draft; do not count those scans fully translated. Next: Part 6 Image 3 (`003-3d526bc2d7.png`). See `working/periyapuranaputhayal_translation.md` and `working/periyapuranaputhayal_recovery.md` for the checkpoints. The footer hold remains open. No state refresh; last completed-work test result remains 15 passing tests, not rerun for this partial prose checkpoint. Previous pushed checkpoint: `fa14b5e`. Use RMRL for missing or unreadable evidence as requested.

`katturaigal/nirubarin_nilai.md` (நிருபரின் நிலைமை / The Reporter's Predicament) is complete. Nine retained archive scans plus the missing dialogue recovered from RMRL 2 January 1944 page 6 are fully translated and comparatively reviewed. Unrelated Image 9 and original mixed OCR remain preserved separately. Exact retained Tamil SHA-256: `4c87934de6e7cb70f548286f5d45f23a676b56eb7fc4144a6de2db09f134d130`. Hold released, state refreshed, absent from pending list; audit zero issues and all 15 tests pass. The recovery-hold test now checks current inventory entries rather than permanently requiring this completed work.

Current OCR total: **886/962 complete and verified, 76 pending**: 5 katturaigal, 26 nadagangal, 0 sirukathaigal and 45 sorpozhivugal.

## Historical Kambarasam Recovery Chronology

The following records describe the earlier source-recovery process. All of
Kambarasam is now complete; these are historical observations, not the next task.

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
(60 distinct scans plus one duplicate). Part 7's ten scans were then fully
reconciled, including the invisible-form episode, the நீராடும் மாதர் comparison,
the difficult நைடதம் verse cross-checked against the clearer Wikisource scan,
the பாரதிதாசன் comparison, and the `கம்பரசம் - 2` transition. Recovery coverage
is 71/127 image slots (70 distinct scans plus one duplicate). Part 8's ten scans
were then fully reconciled, including the rebuttal discussion, the moat simile,
the approach to Mithila, both elephant and garland comparisons, their deliberately
segmented verses, and the closing prose gloss. Recovery coverage is 81/127 image
slots (80 distinct scans plus one duplicate). Part 9's ten scans were then fully
reconciled, including the gambling discussion, the மலைமிசை comparison, the
procession verse and prose, the quoted young-men-and-women scenes, and the closing
water-play passage. Difficult compressed verses were cross-checked against
Wikisource without replacing Anna's printed wording or lineation. Recovery
coverage is 91/127 image slots (90 distinct scans plus one duplicate). Part 10's
ten scans were then fully reconciled, including the concluding water-play
discussion, the drinking scenes, the printed `(Blood)` intervention, the
compressed நறை கமழலங்கல் verse and gloss, the closing sound catalogue, and the
opening of `கம்பர் “விழா”`. Recovery coverage is 101/127 image slots (100
distinct scans plus one duplicate). Part 11's ten scans were then fully reconciled, including
the `கம்பர் “விழா”` discussion, the omitted `விட்டான்` dialogue ending, the
journey-to-a-wedding scenes, the nested colloquial drinking dialogue, the
`பூக்கம ழோதியர்` verse and gloss, and the closing `மின்னென நுடங்குகின்ற` verse.
Recovery coverage is 111/127 image slots (110 distinct scans plus one duplicate).
Part 12's ten scans were then fully reconciled, including the embedded `பம்ப
இராமாயணம்` essay, the complete train-ticket episode, the comparison of the
Kamba and Pampa Ramayanas, and the opening Pampa narrative through Narada's
warning to Dasaratha. Unusual scan readings such as `மறைவிடத் தருகே`, the
quotation boundary in `“விசுவாசிகளுக்"குக்`, `அண்ணனைத்தடுத்து`, and `என்ற
கேள்விப்படும்போது` were retained without normalization. Recovery coverage is
121/127 image slots (120 distinct scans plus one duplicate); continue with Part
13 Image 1. No translation has begun, and the six Part 13 image slots remain in
source recovery.

Part 13's six scans were then fully reconciled, including Narada's warning, the
wandering Dasaratha and Janaka episode, Prabhamandala's abduction and portrait
scene, the marriage dialogue, and the closing Pampa Ramayana summary. Recovery
coverage is now 127/127 image slots (126 distinct scans plus the exact Part 4
duplicate). All thirteen parts are visually reconciled with their unusual
printed readings preserved; begin the complete bilingual translation next.

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

## Source-recovery preference

The user explicitly requested on 2026-09-06 that RMRL (https://rmrl.in/) be used for future works whenever material is missing. Search its periodical collection for the relevant issue and article when archive scans are missing, mixed, truncated or unreadable. Verify the title, date, complete column/page sequence and ending visually; record the exact issue URL and printed/viewer page references. Preserve replaced or unrelated archive material separately. A matching title or catalogue record alone is not proof of full recovery. This preference applies throughout the remaining 962-work goal.

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
   source issue is genuinely repaired. `பழைய கம்பெனி!` was recovered from its
   complete newspaper witness on 2026-09-06; its former mixed source is preserved separately.
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

## பழைய கம்பெனி! recovery completed

The user-supplied 18 March 1945 newspaper evidence was reconciled with RMRL viewer page 9 (printed page A). The complete canonical bilingual document is built and audited; the incorrect-source hold is released. The evidence folder contains the full newspaper witness, screenshots, historical draft/review, English draft, original mixed corrected OCR and separated Roosevelt fragment. Read its README for current status. Resume இலட்சிய வரலாறு with full English translation; all 58 scans are reconciled.
