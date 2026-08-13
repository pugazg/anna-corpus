# Difficult Terms Register

`difficult_terms.csv` records translation decisions that require more judgment
than an ordinary dictionary lookup.

## What to record

- Historical and political terminology whose meaning has changed over time.
- Idioms, metaphors, literary allusions, humour, puns, and rhetorical phrases.
- Kinship terms and forms of address carrying political or cultural meaning.
- Names and transliterations that need one consistent spelling.
- Damaged or OCR-sensitive words whose reading affects the translation.
- Any word or phrase for which two plausible translations remain.

## Status values

- `candidate`: noticed but not yet translated confidently.
- `provisional`: usable rendering that should be checked against more examples.
- `approved`: established rendering to reuse when the context is comparable.
- `context_dependent`: must be translated separately in each occurrence.
- `unresolved`: source recovery or outside research is required.

Approval never means blind replacement. Context takes priority, and a repeated
term can have more than one approved translation when its sense genuinely differs.

