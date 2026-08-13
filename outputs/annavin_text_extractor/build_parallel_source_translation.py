#!/usr/bin/env python3
"""Build a bilingual OCR work from a verified parallel English archive page."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from build_manual_translation import OUTPUT, extract_source, source_rows


def paragraphize(text: str) -> str:
    return "\n\n".join(line.strip() for line in text.splitlines() if line.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("relative_file")
    parser.add_argument("parallel_source", type=Path)
    parser.add_argument("--english-title", required=True)
    parser.add_argument("--tamil-title", required=True)
    parser.add_argument("--start", required=True, help="First phrase of the English speech body")
    parser.add_argument("--end", required=True, help="Last phrase of the English speech body")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    row = source_rows().get(args.relative_file)
    if not row:
        raise SystemExit(f"Not found in source map: {args.relative_file}")
    chosen = Path(row["chosen_path"])
    _, tamil_url, tamil = extract_source(chosen.read_text(encoding="utf-8", errors="replace"))

    parallel_raw = args.parallel_source.read_text(encoding="utf-8", errors="replace")
    _, parallel_url, parallel_body = extract_source(parallel_raw)
    start = parallel_body.find(args.start)
    if start < 0:
        raise SystemExit("English start phrase not found")
    end = parallel_body.find(args.end, start)
    if end < 0:
        raise SystemExit("English end phrase not found")
    english = paragraphize(parallel_body[start : end + len(args.end)])

    lines = [
        f"# {args.tamil_title} / {args.english_title}", "",
        f"**Tamil title:** {args.tamil_title}  ",
        f"**English title:** {args.english_title}  ",
        f"**Tamil source:** <{tamil_url}>" if tamil_url else f"**Source file:** `{args.relative_file}`",
        f"**Parallel English source:** <{parallel_url}>" if parallel_url else f"**Parallel English source file:** `{args.parallel_source}`",
        "", "## Source Tamil (verbatim)", "", tamil,
        "", "## English Translation", "", english,
    ]
    if args.notes:
        lines.extend(["", "## Translator's Notes", "", args.notes])
    destination = OUTPUT / args.relative_file
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
