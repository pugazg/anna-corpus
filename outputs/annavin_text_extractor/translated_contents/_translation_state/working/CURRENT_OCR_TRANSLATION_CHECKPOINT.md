# Current OCR translation checkpoint

Updated from live GitHub `main` after the `sorpozhivugal/annal_nabi.md` completion boundary.

## Authoritative completed count

The last refreshed canonical state remains:

- OCR-origin target: 962
- translated: 873
- pending: 89
- recovery pending in the last generated report: 58
- translation pending in the last generated report: 31

These generated counts have **not yet been refreshed locally** after the screening commits below. The user has explicitly allowed GitHub-first work and will reconcile the local repository later.

## Screening completed after the last generated report

### `sorpozhivugal/230868.md`

Result: `needs_source_recovery`

Durable evidence:
`translated_contents/_translation_state/working/230868_recovery_screen.md`

Reason summary: pervasive OCR corruption across the two-part 23 August 1968 no-confidence debate, including title/charge-list damage, figures and factory names, removed parliamentary words, mixed-script English, and a destroyed procedural quotation on Part 2 Image 10.

### `sorpozhivugal/270667.md`

Result: `needs_source_recovery`

Durable evidence:
`translated_contents/_translation_state/working/270667_recovery_screen.md`

Reason summary: corruption starts in the title/header and recurs through dates, figures, policy passages, anecdotes and speaker text in the 1967-68 budget debate. It requires complete scan reconciliation before translation.

## Effective queue split pending local refresh

If no other concurrent changes occur, these two classifications imply:

- total pending remains 89
- recovery pending becomes 60
- translation pending becomes 29

Do **not** reduce the translated count: neither work has a canonical bilingual translation.

## Next small unit

Screen the next still-unclassified item from the live `OCR translation pending` section, beginning with `sorpozhivugal/280868_2.md` unless current GitHub state has moved again.

After local reconciliation becomes available, add these two works to `needs_source_recovery.csv`, run `python3 refresh_ocr_translation_state.py`, run all `test_*.py`, and replace this provisional checkpoint with the regenerated canonical state.
