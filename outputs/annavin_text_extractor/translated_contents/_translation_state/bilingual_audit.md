# Bilingual Translation Audit

`photos` and `oviyam` are excluded from the translation workload.

| Section | Translation target | Completed | Bilingual with source retained | Pending |
|---|---:|---:|---:|---:|
| english | 1 | 1 | 1 | 0 |
| kadithangal | 275 | 8 | 8 | 267 |
| katturaigal | 1388 | 540 | 540 | 848 |
| kavithaigal | 77 | 77 | 77 | 0 |
| Kurunavalgal | 25 | 0 | 0 | 25 |
| nadagangal | 62 | 25 | 25 | 37 |
| navalgal | 6 | 0 | 0 | 6 |
| paettigal | 26 | 26 | 26 | 0 |
| root | 5 | 5 | 5 | 0 |
| sirukathaigal | 109 | 108 | 108 | 1 |
| sorpozhivugal | 537 | 184 | 184 | 353 |
| **All included sections** | **2511** | **974** | **974** | **1537** |

## OCR-Origin Translation Progress

| Section | OCR target | Completed | Bilingual with source retained | Pending |
|---|---:|---:|---:|---:|
| katturaigal | 552 | 539 | 539 | 13 |
| nadagangal | 61 | 25 | 25 | 36 |
| sirukathaigal | 108 | 108 | 108 | 0 |
| sorpozhivugal | 241 | 184 | 184 | 57 |
| **All OCR-origin sections** | **962** | **856** | **856** | **106** |

## OCR Source Recovery Status

| Section | Works with blank image sections | Blank pages |
|---|---:|---:|
| katturaigal | 0 | 0 |
| nadagangal | 33 | 413 |
| sirukathaigal | 0 | 0 |
| sorpozhivugal | 5 | 10 |
| **All OCR-origin sections** | **38** | **423** |

A blank image section has an explicit no-text marker or no OCR body after its image reference. The canonical Tamil source is not translation-ready even when the scan itself may be readable.

### Sources Requiring Recovery

- `nadagangal/aadiyapatham.md`: 14 blank page(s)
- `nadagangal/aalai_arumugam.md`: 7 blank page(s)
- `nadagangal/ambal_kadatcham.md`: 9 blank page(s)
- `nadagangal/avan_pithana.md`: 6 blank page(s)
- `nadagangal/bagirathiyin_1.md`: 10 blank page(s)
- `nadagangal/bankak_bankaja_1.md`: 7 blank page(s)
- `nadagangal/bankar_1.md`: 3 blank page(s)
- `nadagangal/bharatham_1.md`: 5 blank page(s)
- `nadagangal/chandramohan.md`: 22 blank page(s)
- `nadagangal/dhrogi_kaplan_1.md`: 3 blank page(s)
- `nadagangal/gandhi_jayanthi_1.md`: 9 blank page(s)
- `nadagangal/ilangogin_sabatham_1.md`: 4 blank page(s)
- `nadagangal/inba_oli.md`: 57 blank page(s)
- `nadagangal/jananayaga_1.md`: 5 blank page(s)
- `nadagangal/kaasurar_1.md`: 3 blank page(s)
- `nadagangal/kadhal_jothi.md`: 54 blank page(s)
- `nadagangal/kalappu_manam.md`: 6 blank page(s)
- `nadagangal/kannayirathin.md`: 28 blank page(s)
- `nadagangal/kanneerthuli.md`: 6 blank page(s)
- `nadagangal/magudabishegam_1.md`: 7 blank page(s)
- `nadagangal/mangalapuri_1.md`: 5 blank page(s)
- `nadagangal/nadanthathuthan_1.md`: 2 blank page(s)
- `nadagangal/nankodai.md`: 11 blank page(s)
- `nadagangal/neethidevan.md`: 16 blank page(s)
- `nadagangal/oorar_urayadal_1.md`: 5 blank page(s)
- `nadagangal/paavayin.md`: 12 blank page(s)
- `nadagangal/periayamanithargal_1.md`: 5 blank page(s)
- `nadagangal/ragavayanam_1.md`: 4 blank page(s)
- `nadagangal/rottithundu.md`: 18 blank page(s)
- `nadagangal/sanmanam.md`: 11 blank page(s)
- `nadagangal/sorgavaasal.md`: 33 blank page(s)
- `nadagangal/suyechai.md`: 16 blank page(s)
- `nadagangal/yar_kaetka.md`: 10 blank page(s)
- `sorpozhivugal/150767.md`: 1 blank page(s)
- `sorpozhivugal/200268.md`: 3 blank page(s)
- `sorpozhivugal/230168.md`: 3 blank page(s)
- `sorpozhivugal/nithi080361.md`: 1 blank page(s)
- `sorpozhivugal/sudhanthira_kaiyelu.md`: 2 blank page(s)

### Manually Verified Recovery Holds

- `katturaigal/ilamayil_muthumai.md`: At least one page is absent between Images 4 and 5: Image 4 ends mid-sentence at 'பண்டிதருக்கோ, இயற்கைக்கு ஏற்றபடி', while Image 5 begins abruptly with 'கோடானுகோடி ஏழைமக்கள்'. The live webpage exposes the same broken 15-image sequence. Recover the intervening discussion of Jayaprakash Narayan before translation
- `katturaigal/nirubarin_nilai.md`: Printed pages 182-184 are absent after Image 8 (page 181); Image 9 is unrelated page 185 from an article on science, and Image 10 resumes only the final fragment of the reporter article. Recover the three missing pages and remove the misassigned scan before translation
- `katturaigal/udan_piranthar_1.md`: The 19-scan OCR source ends immediately after the killing of Tiberius Gracchus although the title promises two brothers. The complete four-part HTML counterpart exists at Kurunavalgal/udanpiranthar_iruvar.md and continues through Gaius Gracchus and the conclusion. Reconcile the OCR opening against the scans, then recover and merge Parts 2-4 from that counterpart before translating.
- `katturaigal/valarppupen.md`: The sixth and final extracted image ends mid-argument after Periyar's claimed five or six years of trust in Maniammai; recover the continuation before producing a complete translation
- `nadagangal/avanasiyar_1.md`: 4 of 5 scan pages contain no OCR text; only image 1 classroom scene is presently recoverable
- `nadagangal/avar_pesathathu_1.md`: 5 of 8 scan pages contain no OCR text; political conversation begins and ends mid-sentence
- `nadagangal/avargal_ullam_1.md`: 7 of 8 scan pages contain no OCR text; only image 4 Maratha dialogue is presently recoverable
- `nadagangal/bagirathiyin_1.md`: Ten scan pages have no OCR text, leaving only metadata and an unusable fragment; recover the false-empty pages before translation
- `nadagangal/bajirao_1.md`: Final images 3-4 contain no OCR text; palace scene ends mid-question
- `nadagangal/congresswala_1.md`: Final images 4-5 contain no OCR text; 1938 Legislature satire ends mid-sentence
- `nadagangal/dharmam_thalai_1.md`: 4 of 6 scan pages contain no OCR text; only images 3-4 fundraising dialogue are recoverable
- `nadagangal/enthan_thiru_1.md`: 4 of 7 scan pages contain no OCR text; title page and conclusion of counterfeit-note fraud are absent
- `nadagangal/gandhi_jayanthi_1.md`: Images 1, 3, 4, 11 and 12 contain no OCR text, including the opening and material immediately before the closing exchange
- `nadagangal/kaasurar_1.md`: The source explicitly labels itself an unfinished short play and its surviving final scene ends without completion; retain for recovery or classify as an intentionally unfinished work before final translation
- `nadagangal/kailayam_1.md`: 4 of 7 scan pages contain no OCR text; two Purana critiques and conclusion survive
- `nadagangal/kal_sumantha_1.md`: 11 of 13 scan pages contain no OCR text; only opening image 1 and final image 13 are recoverable
- `nadagangal/kattaiviral_1.md`: 6 of 8 scan pages contain no OCR text; only images 4 and 7 are recoverable
- `nadagangal/mangai_oorugai_1.md`: 7 of 9 scan pages contain no OCR text; only images 3 and 9 are recoverable
- `nadagangal/mangalapuri_1.md`: Images 1, 2, 4 and 5 contain no OCR text, leaving the play's opening and internal scenes incomplete despite a surviving 1959-to-1966 frame
- `nadagangal/morarji_thesai.md`: 14 of 16 scan images contain no OCR text; only Part 1 Image 7 and Part 2 Image 3 survive, leaving the political stage scene incomplete
- `nadagangal/mudhalalithuva_1.md`: 2 of 4 scan pages contain no OCR text; images 2 and 4 leave a dialogue gap
- `nadagangal/orae_oru_vithi_1.md`: 5 of 6 scan pages contain no OCR text; only image 6 dialogue is presently recoverable
- `nadagangal/ragavayanam_1.md`: Images 3, 7 and 8 contain no OCR text, removing transitions and the ending of the play
- `nadagangal/roam_erigirathu_1.md`: Final image 3 contains no OCR text; dialogue stops when Hitler answers the telephone
- `nadagangal/sellapillai_1.md`: Images 2 and 4-5 contain no OCR text; setup and final motor-shed scene survive with gaps
- `nadagangal/sumangalipooja_1.md`: 10 of 11 scan pages contain no OCR text; only image 9 charity dialogue is presently recoverable
- `sirukathaigal/rajapart.md`: 14 of 16 scan pages contain no OCR text; recover images 2-4 and 6-9 in part 1 plus images 1-3 and 5-7 in part 2 before translation
- `sirukathaigal/sollathathu.md`: 9 of 13 scan pages contain no OCR text; recover images 1, 5-10, and 12 before translation
- `sorpozhivugal/060767.md`: Recover the damaged closing lines of Image 7 in Anna's distinction between fringe actors and responsible party leadership
- `sorpozhivugal/110667.md`: The four-part 1967-68 revised-budget speech contains pervasive dropped lines, numeral substitutions and mixed-script corruption across its 54 numbered paragraphs, beginning on Part 1 Image 1 and continuing through the closing page. Re-OCR every scan with Tamil and English models and reconcile all fiscal figures, English administrative terms and paragraph transitions before translation.
- `sorpozhivugal/130767.md`: Re-OCR embedded English in Images 2-3 and 6-7, recover damaged Image 6 lines, and obtain continuation after Anna begins proposing a simple resolution
- `sorpozhivugal/170868.md`: Passage between Images 3 and 4 is absent after the current-year total begins with Rs. 2 crore; grant numbers and the Cauvery irrigation work also need scan verification
- `sorpozhivugal/180767.md`: Recover all of Image 3, damaged Images 6-7 transition, embedded English intervention on Image 8, and continuation of Anna's final reply to Vinayakam
- `sorpozhivugal/180767_2.md`: Image 3 contains no OCR text; historic Tamil Nadu naming speech has a middle gap
- `sorpozhivugal/200268.md`: The combined two-part 20 February 1968 Governor's Address debate is incomplete and heavily corrupted. Part 1 Image 15 and Part 2 Images 4 and 15 have no OCR text; long speaker exchanges in Part 1 Images 3-5 and Part 2 Images 14-16 are largely unreadable. Re-OCR all 36 scans with Tamil and English models, restore the missing pages, and reconcile every speaker intervention before translation.
- `sorpozhivugal/200368.md`: The 22-page police-department debate has pervasive line loss and glyph substitution, including the opening motion, Churchill quotation on Image 4, speaker exchanges on Images 18-20, and most of the final reply on Image 22. Re-OCR every scan with Tamil and English models and reconcile interventions and quotations before translation.
- `sorpozhivugal/200868.md`: The 16-page supplementary-grants debate contains unrecovered English rule citations and policy quotations plus malformed amounts and speaker exchanges, especially on Images 1, 3 and 14-16. Re-OCR every scan with Tamil and English models and reconcile the common-good-fund, labour-policy and industrial-investment passages before translation.
- `sorpozhivugal/250367.md`: The 16-page source is internally inconsistent: its heading identifies a 1967 Legislative Assembly disqualifications bill, but the body is a food-procurement and price-control debate. Images 2-3 lose substantial clauses and Image 16 resumes mid-sentence. Verify the correct title/page mapping and re-OCR all scans before translation.
- `sorpozhivugal/260368.md`: Recover short damaged line clusters at the beginnings of Images 3, 5 and 6, including the office held by Minister Govindasamy
- `sorpozhivugal/270368.md`: Short line clusters at the beginnings of Images 3 and 5 are damaged; verify the oil-lamp wording and the English loan phrase rendered as breathing space
- `sorpozhivugal/271167.md`: Image 5 closing lines are severely garbled after the electricity-tariff sentence; recover from a clearer scan or the 27 November 1967 Assembly record
- `sorpozhivugal/280268.md`: The 16-scan 28 February 1968 budget speech has extensive dropped and non-lexical text, including agricultural targets on Images 2-3 and debt-relief calculations on Images 14-15. Image 16 ends during the Gajendragadkar Commission discussion without the speech's conclusion. Re-OCR all scans with Tamil and English models and recover the missing continuation before translation.
- `sorpozhivugal/280868.md`: The 61-page 28 August 1968 no-confidence debate is predominantly English, but it was processed with Tamil-only OCR. Most English speeches became mixed-script character noise while only Tamil editorial summaries remain readable. Re-OCR every scan with English and Tamil models, reconcile speakers and quotations page by page, and rebuild the canonical source before translation.
- `sorpozhivugal/aalunar_vivath.md`: The 16-page 6 May 1957 Governor's Address debate contains extensive dropped clauses and mixed-script corruption on Images 2-7, including policy and budget passages, the Finance Minister's three portfolios, land-reform reasoning and an English Vinoba quotation. Re-OCR all scans bilingually and reconcile every policy quotation before translation.
- `sorpozhivugal/allal_agala.md`: Substantial passage missing between Images 3 and 4, from the Khrushchev discussion to the proposed aluminium factory; recover it and verify the Seshasayee company reference
- `sorpozhivugal/amaichar160361.md`: Recover damaged Salem court-case lines, election-fund transitions, corporate-contributor discussion, and the end of the proposal that Ministers resign before elections
- `sorpozhivugal/annavin_thalaimai.md`: The 16-page 22 August 1937 first presidential address is continuous, but the current Tamil-only OCR has pervasive material corruption: the Mohenjo-daro/Harappa parenthesis is unreadable on Image 4; names, headings and political terms are damaged throughout; Images 12-14 lose clauses and speaker exchanges; and the closing editorial note is malformed. Re-OCR all scans with Tamil and English models and reconcile every named person, quotation and page transition before translation.
- `sorpozhivugal/chennai151261.md`: The 15-page 15 December 1961 final vote speech on the Madras Appropriation Bill has severe line loss and glyph corruption in its opening metadata and editorial introduction, throughout several fiscal passages, and across the final paragraph. Re-OCR every scan with Tamil and English models and reconcile the date, bill details, figures and closing statement before translation.
- `sorpozhivugal/maedai_paechu.md`: Verify the exact Kalamegam comic-horse measure in Image 5 and the printed year in the heading
- `sorpozhivugal/moondravath111161.md`: The 16-page 17 November 1961 Third Five-Year Plan debate has pervasive dropped lines, malformed dates and figures, and mixed-script corruption from Image 1 onward. Images 1-4 lose parts of the procedural argument and Planning Commission quotation; Images 14-16 damage English interventions, sector names, amounts and the final exchange with Finance Minister C. Subramaniam. Re-OCR every scan bilingually and reconcile all plan totals, quotations and speaker turns before translation.
- `sorpozhivugal/nadagathil_oru.md`: Opening survey of the T. K. S. troupe's historical and literary plays is cut off between Images 1 and 2; recover the missing page or passage
- `sorpozhivugal/nila_ucha290861.md`: The 15-page 29 August 1961 land-ceiling bill speech has extensive dropped Tamil and mixed-script corruption. The English select-committee statement on Image 2, Article 26 quotation and Uttar Pradesh judgment on Images 7-8, exemption discussion on Images 4-6, and multiple page joins cannot be translated faithfully from the current OCR. Re-OCR all scans with Tamil and English models and reconcile the constitutional clauses and case citation before translation.
- `sorpozhivugal/nithi080358.md`: The canonical two-part 8 March 1958 budget debate includes all 39 scans, but at least 12 pages contain dense numeral/glyph substitution and dropped lines, especially Part 1 Images 3, 10 and 13 and Part 2 Images 3, 6-10, 13-14 and 16-17. Re-OCR all scans with Tamil and English models and reconcile the Nehru quotation, financial figures, speaker exchanges and damaged closing argument page by page before translation.
- `sorpozhivugal/nithi300460.md`: Recover the English title of the Salem-iron reference book on Image 2 and damaged passages at the ends of Images 4 and 6
- `sorpozhivugal/nithi_othukka260757.md`: Verify damaged header date and bill year, and recover the illegible embedded English phrase in Rajagopalachari's quoted comparison on Image 5
- `sorpozhivugal/poar_murasu_1.md`: The available 17-scan 1948 War Drum speech is incomplete: Image 17 ends mid-sentence in the section titled வீரர் வழிவந்த இனம், after introducing how a six-sensed human controls five-sensed animals. The HTML page contains no body text and no continuation scan or companion file is present. Locate and transcribe the continuation before translation.
- `sorpozhivugal/poar_murasu_kotti.md`: Recover the passage between Images 5 and 6 concerning Nehru's language assurance and obtain the continuation after the final unfinished readiness appeal
- `sorpozhivugal/porul.md`: The 17-page 19 February 1948 speech titled பொருள் is continuous but not textually reliable: Image 6 renders Jesus's needle-and-camel quotation as mixed-script noise; Image 8 has a malformed population percentage; Images 10-12 lose clauses and English text in the savings, public ownership and Nehru-capitalist passages. Re-OCR all scans bilingually and reconcile every quotation, percentage, date and named participant before translation.
- `sorpozhivugal/satta_11_03_1958.md`: Speech begins mid-argument, loses material between Images 4 and 5, and ends mid-question; recover the complete 11 March 1958 Assembly language debate and verify Article 344
- `sorpozhivugal/sudhanthira_kaiyelu.md`: All 14 handwritten manuscript images are effectively unreadable in the current OCR; one page reports no text and the remaining output is overwhelmingly disconnected glyphs, so the speech must be re-transcribed from the scans before faithful translation
- `sorpozhivugal/thozhil080460.md`: The 18-page 8 April 1960 industrial-grant debate has pervasive dropped clauses and mixed-script corruption. Images 3-4 damage the heavy-industry argument and list of prerequisites; Images 14-18 lose employment figures, industrial names, the Salem-minerals reference, library exchange and part of the closing appeal. Re-OCR all scans bilingually and reconcile every amount, English industrial term and speaker turn before translation.
- `sorpozhivugal/veetirkor_putha.md`: Verify the exact infernal-pit names on Image 5 and the lunar-research wording in the same image
- `sorpozhivugal/velanmai180948.md`: Re-OCR statement-of-objects English on Image 2 and student slogan on Image 8; verify damaged rule-making transition at Images 4-5

## English Essay Clarification

The `english` inventory entry is only a 129-title catalogue. The actual English essay bodies are stored under `katturaigal`; only `we_welcome.md` has been translated so far.

## Issues

No bilingual or source-retention issues found in completed translations.
