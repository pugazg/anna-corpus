# Recovery screen — `sorpozhivugal/230868.md`

Status: `needs_source_recovery`

Screened from current `main` after the completed `sorpozhivugal/annal_nabi.md` boundary.

## Canonical work

- OCR source: `outputs/annavin_text_extractor/ocr_text_corrected/sorpozhivugal/230868.md`
- Website part 1: `http://www.annavinpadaippugal.info/sorpozhivugal/230868_1.htm`
- Website part 2: `http://www.annavinpadaippugal.info/sorpozhivugal/230868_2.htm`
- Date printed in the source: 23.08.1968
- Subject: no-confidence motion against the C. N. Annadurai ministry

## Screening result

Do **not** translate the current corrected OCR. The work requires complete bilingual re-OCR / visual reconciliation before translation.

The corruption is pervasive rather than local. Confirmed examples in the current canonical OCR include:

- Part 1 Image 1: the title is damaged (`தர்மானம்` for the printed resolution heading), the eleven-charge list contains malformed numbering and dropped text, and the `தமிழர் சேனை` line is broken.
- Part 1 Images 3-6: repeated dropped Tamil clauses, stray glyphs/numerals and malformed figures interrupt the Assembly exchanges.
- Part 1 Image 7: factory names and an English/industrial list collapse into mixed-script OCR noise.
- Part 1 Images 9-10: strike statistics, labour-policy text and speaker exchanges contain malformed figures and missing wording.
- Part 1 Images 15-17: ranking figures and parliamentary exchanges are corrupted; words ordered removed by the Deputy Speaker are represented by OCR noise, and the English parliamentary explanation on Image 17 is unreadable mixed-script text.
- Part 2 Images 1-4: procurement quantities/prices and several sentences contain dropped words, malformed numerals and non-lexical OCR.
- Part 2 Images 5-9: fire-relief, housing and police-interference passages repeatedly lose words and line fragments.
- Part 2 Image 10: the printed English procedural / sub-judice quotation is effectively destroyed by Tamil-only OCR and cannot be translated faithfully from the current text.
- Part 2 Images 11-12: the student/transport-worker inquiry discussion and subsequent medical analogy continue to contain dropped or malformed text.

## Required recovery action

Re-OCR **all scans in both parts with Tamil and English models**, then visually reconcile every page against the scan. Particular care is required for:

1. title, date and the eleven grounds of the no-confidence motion;
2. all factory names, strike statistics, percentages, prices and quantities;
3. every speaker turn and page join;
4. words formally expunged from the Assembly record;
5. the English parliamentary/procedural quotations, especially Part 1 Image 17 and Part 2 Image 10;
6. the continuation and closing of the complete canonical work.

Only after that reconciliation should a bilingual canonical file be created.

## Queue implication

This work should move from `OCR translation pending` to `OCR/source recovery pending`. Total OCR-origin pending remains unchanged; only the recovery/translation split changes by +1 / -1.
