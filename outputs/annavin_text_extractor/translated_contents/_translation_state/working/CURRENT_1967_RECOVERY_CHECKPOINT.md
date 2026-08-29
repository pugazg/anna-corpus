# 1967 OCR Recovery Checkpoint

- Canonical work: `sorpozhivugal/1967.md`
- Scope: 30 scans, two parts
- Recovery candidate: `working/1967_reocr_candidate.md`
- OCR method: Tesseract `tam+eng`, PSM 6, followed by the project correction pipeline
- Candidate word count before manual reconciliation: 5,886

## Verified So Far

- Part 1 Image 1: title and date read directly as `“1967”` and `11-08-1957`; the introductory editorial footnote begins `1957இல்`.
- Part 1 Image 2: the body year is `1917`; the footnote date is `11-11-1916`.
- Part 1 Image 4: the footnote reads `நூற்றுக்கணக்கான சிறப்புக் கூட்டங்களும் நடைபெற்றதை Justice என்ற இதழ் கூறுகிறது.`
- Part 1 Image 6: the English quotation is `At any time Tamilians will prefer London to Delhi`; the organisation is `South Indian Liberal Federation`.
- Part 1 Image 9: degree abbreviations are `B.A.` and `M.A.`; `MAUI இழுக்கின்ற` is restored as `மாடு இழுக்கின்ற` from the scan-aligned line and context.
- Part 1 Image 15: `Sappers and Miners` is correctly recovered.
- Part 2 Image 12: the damaged line reads `புதிதாக எந்தச் சட்டமும் வரவில்லை.`
- Part 2 Image 14: the name is `வ. உ. சிதம்பரனார்`.

## Remaining Work

- Visually reconcile all unverified pages, especially Part 1 Images 8-10 and Part 2 Images 7-12 where review candidates remain.
- Resolve `SCHL` on Part 1 Image 10 and `பிரேோரேபணையை` on Part 2 before promotion.
- Remove OCR-only spacing and punctuation defects without modernising the printed Tamil.
- Compare every first and last line across all 29 page joins.
- Promote the candidate to `ocr_text_corrected` only after complete visual review; then update `source_map.csv`, document corrections in `ocr_concerns.csv`, and translate the recovered source.
