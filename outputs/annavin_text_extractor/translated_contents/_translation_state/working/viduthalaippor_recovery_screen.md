# Recovery screen — `katturaigal/viduthalaippor.md`

Status: `needs_source_recovery`

## Canonical work

- OCR source: `outputs/annavin_text_extractor/ocr_text_corrected/katturaigal/viduthalaippor.md`
- Website parts: `viduthalaippor_1.htm`, `viduthalaippor_2.htm` and `viduthalaippor_3.htm`
- Printed Tamil title: `விடுதலைப் போர்`
- English title: `Liberation War`
- Printed date: `9-12-1945`
- Extent: 33 scans (11 in each part)

## Scan-proven findings

- Part 1 Image 1 clearly prints `9-12-1945`; the OCR reading `59-12-1945` has been corrected.
- Part 1 Image 3 clearly prints `(Dravidian League)`; the OCR had converted the complete English name to mixed-script noise. The exact reading has been restored.
- Part 2 Image 10 clearly prints the population figure `4 1/2 கோடி`; the missing numerator has been restored.
- Part 3 Image 10 contains no text corresponding to the inserted mixed-script line `ட அ உ ட்ரூ [க] ப் த ந2 ்் . ்ி`; that scan-absent line has been removed.
- Dropped letters, substituted characters, broken compounds and malformed names and figures recur in representative scans from all three parts. The printed text is readable, but the current OCR is not a verbatim source from which a faithful translation can be made.
- All three final scans are present, and Part 3 Image 11 closes the collection.

## Required recovery

Re-OCR all 33 scans with Tamil and English models and visually reconcile every title, date, name, figure, quotation and page join. Preserve the three parts as one canonical work and retain the four scan-proven corrections above. Do not create the bilingual document until the complete source is scan-safe.

## Sequential recovery — 2026-09-26

Reopened Part 1 Images 1–3 at full-page resolution and re-OCRed those three scans with installed Tesseract `tam+eng`, PSM 3. Raw machine output is preserved in `working/viduthalaippor_reocr/`; it is explicitly unverified and repeats many original OCR mistakes. It must not overwrite the corrected source.

- Image 1: title and date `விடுதலைப் போர்`, `9-12-1945` visually confirmed; no change.
- Image 2: reviewed heading, five-line poem and all prose. Restored the poem’s five consecutive lines/opening quotation and `மகிழ்வூட்டி வருகிறது.` from malformed OCR. Preserved the printed page-final `தனது`, which joins Image 3’s `நாட்டை`.
- Image 3: restored visible `நமக்குக்`, `கொள்கையாக்கப்`, `ஊக்கமும்`, `நமது கட்சி`; removed false periods in `நாட்டை`, `மிரட்டி`, `திராவிட`, `நாட்டுக்குடை`, `கமிட்டி`, and the stray apostrophe after `காசியிலே`. The `(Dravidian League)` reading remains intact.

Image 3’s `கோருகின்றனர்` still needs a close letter-level check: fresh OCR repeats it, but this is not independent confirmation. Keep its current spelling provisional rather than silently normalizing the honorific. The complete three-scan batch has been visually inspected, but Image 3 is not yet fully reconciled. Next resolve that reading and continue Part 1 Image 4; verify the `கொள்ள / வேண்டுமென்பது` page join. The remaining 30 scans have not received sequential review. No English translation or hold release. Romapuri and Periyapuranaputhayal remain on their existing holds.

## Part 1 Images 4–5 — 2026-09-26

Resolved Image 3’s provisional `கோருகின்றனர்` against native crop x=990–1510, y=745–815, enlarged 3×. The retained spelling is supported; no normalization to a different honorific ending.

Re-OCRed Images 4–5 with tam+eng/PSM 3 and visually compared both complete pages. Corrected Image 4’s `ஆண்டவனின்`, `உப கண்டத்தில்`, two instances of `ஒன்று`, and closing full stop. Retained the scan-visible internal full stop after `நமக்கென்ன.` rather than editorially smoothing it. Corrected Image 5’s `பூகோளத்தையுங்கூட`, `தென்பீட`, `கசிந்து கிடந்த`, `ஐபீரியன்` and false periods after `பாடி`, `கோடி`, `நாலுகோடி`. Preserved all four lines of each quoted poem. The Image 5 poem has no visible closing quotation mark after `ஆடுவோமே`; retain that omission and explain it separately in final notes.

Image 3→4 continues `கொள்ள / வேண்டுமென்பது`; Image 4 ends a full sentence before Image 5’s `சரிதமும் பூகோளமும்`. No missing passage detected at those joins. Images 1–5 now have sequential visual comparison and corrected source; 28 scans remain. Next Part 1 Image 6, including the transition from the geographical argument into `ஐந்து அரசுகள்`. No translation, state refresh, pending-count reduction or tests for this incomplete source checkpoint. Previous pushed checkpoint `ac03f67`.

## Part 1 Images 6–7 — 2026-09-26

Re-OCRed both scans with tam+eng/PSM 3 and visually reviewed the full pages, plus Image 6 bottom crop x=100–1520, y=2100–2350. Restored `கிடைத்திருக்க`, dialogue labels `பெரியார்:-`, the paired single quotes around `திராவிட நாடு`, `ஒரியர்களின்`, and removed false periods in `ஏற்பட்ட`, `கேட்கிறது`, `வழங்கும்படி`. Image 7’s isolated OCR line `ஓஒ வுக்கு தீ தனு` is absent from the scan and was removed. Restored visible initial short vowels in `ஒரிசா`/`ஒரியா`, `பீகாரிலிருந்து`, `ஆகவே`, and scan-visible punctuation. The printed figures `56%` and `44%` are retained.

Image 6 ends `அதனால்`, continuing into Image 7 `பல தொல்லை.` Image 7 ends `இந்து`, awaiting Image 8 continuation. Preserve both scan boundaries. The dialogue’s historical claims are source content, not facts to silently correct during transcription.

Two Image 6 readings remain unresolved: the adjective currently `ஓழ்மையான` in `மிக்க ... மாகாணம்`, and the printer-footer abbreviations between clear `14` and `:470`. Existing OCR is retained provisionally; the footer is not endorsed by this review. Do not infer its expansion from other works or normalize the adjective by context. Seven of 33 scans have now been inspected sequentially; Image 6 is only partially reconciled. Next Image 8, with 26 scans remaining for sequential inspection. No translation, hold release, state refresh or tests. Previous pushed checkpoint `bada694`.
