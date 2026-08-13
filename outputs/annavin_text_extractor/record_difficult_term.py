#!/usr/bin/env python3
"""Add or update one entry in the translation difficult-terms register."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REGISTER = (
    SCRIPT_DIR / "translated_contents" / "_translation_state" / "difficult_terms.csv"
)
FIELDS = [
    "source_file",
    "direction",
    "source_term",
    "context",
    "proposed_translation",
    "term_type",
    "status",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--direction", choices=("tamil_to_english", "english_to_tamil"), required=True)
    parser.add_argument("--term", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--translation", default="")
    parser.add_argument("--type", dest="term_type", default="difficult_word")
    parser.add_argument(
        "--status",
        choices=("candidate", "provisional", "approved", "context_dependent", "unresolved"),
        default="candidate",
    )
    parser.add_argument("--notes", default="")
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    args = parser.parse_args()

    register = args.register.resolve()
    register.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    if register.exists():
        with register.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

    new_row = {
        "source_file": args.source_file,
        "direction": args.direction,
        "source_term": args.term,
        "context": args.context,
        "proposed_translation": args.translation,
        "term_type": args.term_type,
        "status": args.status,
        "notes": args.notes,
    }
    key = (args.source_file, args.direction, args.term, args.context)
    replaced = False
    for index, row in enumerate(rows):
        row_key = (row["source_file"], row["direction"], row["source_term"], row["context"])
        if row_key == key:
            rows[index] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)

    rows.sort(key=lambda row: (row["status"], row["source_term"].casefold(), row["source_file"]))
    with register.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{'Updated' if replaced else 'Added'}: {args.term}")
    print(f"Register: {register}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

