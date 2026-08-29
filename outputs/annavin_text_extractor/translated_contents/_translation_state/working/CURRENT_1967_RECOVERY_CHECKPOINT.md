# 1967 OCR Recovery Checkpoint

- Canonical work: `sorpozhivugal/1967.md`
- Website scope: 30 scans, two parts; 28 scans belong to this speech and 2 unrelated scans are quarantined
- Recovery candidate: `working/1967_reocr_candidate.md`
- OCR method: Tesseract `tam+eng`, PSM 6, followed by the project correction pipeline
- Candidate word count before manual reconciliation: 5,886

## Verified So Far

- Part 1 Images 1-5: full page bodies visually reconciled against the archived scans. Corrections include `தேர்ந்தெடுத்துக்`, `ஆண்டு`, `ஆகின்றது`, `ஆனால்`, `முன்னேறவேண்டும்`, `மறந்துவிட்டிருக்கின்றோமோ`, `நினைக்கின்றேன்`, `ஆண்டுகொண்டிருந்த`, `ஆளுக்கொரு`, the complete D. Madhava Nair footnote, `ஆசிரியர்களைக்கூட`, `ஆவார்கள்`, and repaired broken words at the Image 4-5 transition.
- Part 1 Image 1: title and date read directly as `“1967”` and `11-08-1957`; the introductory editorial footnote begins `1957இல்`.
- Part 1 Image 2: the body year is `1917`; the footnote date is `11-11-1916`.
- Part 1 Image 4: the footnote reads `நூற்றுக்கணக்கான சிறப்புக் கூட்டங்களும் நடைபெற்றதை Justice என்ற இதழ் கூறுகிறது.`
- Part 1 Image 6: the English quotation is `At any time Tamilians will prefer London to Delhi`; the organisation is `South Indian Liberal Federation`.
- Part 1 Images 6-10: full page bodies visually reconciled against the archived scans. Corrections include `ஆங்கிலப்`, `கருத்துக் கருவூலம்`, `அடிமைப்பட்டிருக்கிறாயா`, `ஆந்திர`, `South Indian Liberal Federation`, `ஜஸ்டிஸ்`, `சமுதாயம்`, `வசூலித்தார்கள்`, and repaired broken words and punctuation.
- Part 1 Image 9: degree abbreviations are `B.A.` and `M.A.`; the scan reads `கைவண்டி இழுக்கின்ற கந்தன்`.
- Part 1 Image 10: `SCHL சேர்வை விழா` is restored directly from the scan as `கருட சேவை விழா`.
- Part 1 Images 11, 12 and 15: full page bodies visually reconciled. Website Images 13-14 are unrelated Rajya Sabha material; Image 15 directly resumes Image 12's interrupted finance-minister exchange. They are documented in `working/1967_quarantined_scans.md` and excluded from the recovery candidate.
- Part 1 Image 15: `Sappers and Miners` is correctly recovered.
- Part 2 Images 1-5: full page bodies and joins visually reconciled. Meaning-changing repairs include `ஆசை`, `எதிரியினுடைய`, `ஆண்டுகளில்`, `ஒருநாளைக்கு`, `கேட்டீர்களா`, `பூசாரிக்குத்தான்`, `கைதூக்கிவிடாத`, `ஒட்டிக்கொண்டிருக்கிறார்கள்`, and `400 கோடி`.
- Part 2 Image 8: `பிரேோரேபணையை` is restored directly from the scan as `பிரேரேபணையை`.
- Part 2 Image 12: the damaged line reads `புதிதாக எந்தச் சட்டமும் வரவில்லை.`
- Part 2 Image 14: the name is `வ. உ. சிதம்பரனார்`.
- The Image 12 to Image 15 join has been visually confirmed; the earlier structural-only claim covering all 29 website transitions was invalidated by the two unrelated inserted scans.
- The public-domain Wikisource edition of *எதிர்க்கட்சித் தலைவர் பேரறிஞர் அண்ணாவின் சட்டமன்ற உரைகள் 1957-1962*, section 002, independently confirms the `Sappers and Miners` passage quoted in the speech: <https://ta.wikisource.org/wiki/எதிர்க்கட்சித்_தலைவர்_பேரறிஞர்_அண்ணாவின்_சட்டமன்ற_உரைகள்_1957-1962/002>.

## Remaining Work

- Visually reconcile all remaining unverified page bodies and confirm each of the 27 joins between the 28 relevant scans against its two adjacent scans.
- Remove OCR-only spacing and punctuation defects without modernising the printed Tamil.
- Promote the candidate to `ocr_text_corrected` only after complete visual review; then update `source_map.csv`, document corrections in `ocr_concerns.csv`, and translate the recovered source.
