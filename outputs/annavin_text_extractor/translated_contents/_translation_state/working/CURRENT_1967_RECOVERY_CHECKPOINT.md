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
- Part 1 Image 10: `SCHL சேர்வை விழா` is restored directly from the scan as `கருட சேவை விழா`.
- Part 1 Image 15: `Sappers and Miners` is correctly recovered.
- Part 2 Image 8: `பிரேோரேபணையை` is restored directly from the scan as `பிரேரேபணையை`.
- Part 2 Image 12: the damaged line reads `புதிதாக எந்தச் சட்டமும் வரவில்லை.`
- Part 2 Image 14: the name is `வ. உ. சிதம்பரனார்`.
- All 29 OCR page transitions pass a structural continuity screen; none begins or ends with evidence of a missing page.
- The public-domain Wikisource edition of *எதிர்க்கட்சித் தலைவர் பேரறிஞர் அண்ணாவின் சட்டமன்ற உரைகள் 1957-1962*, section 002, independently confirms the `Sappers and Miners` passage quoted in the speech: <https://ta.wikisource.org/wiki/எதிர்க்கட்சித்_தலைவர்_பேரறிஞர்_அண்ணாவின்_சட்டமன்ற_உரைகள்_1957-1962/002>.

## Remaining Work

- Visually reconcile all unverified page bodies and confirm each structurally continuous join against its two adjacent scans.
- Remove OCR-only spacing and punctuation defects without modernising the printed Tamil.
- Promote the candidate to `ocr_text_corrected` only after complete visual review; then update `source_map.csv`, document corrections in `ocr_concerns.csv`, and translate the recovered source.
