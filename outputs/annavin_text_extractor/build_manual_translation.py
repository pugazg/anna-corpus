#!/usr/bin/env python3
"""Build a bilingual Markdown file from verbatim source plus an English draft."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "organized_contents"
OUTPUT = ROOT / "translated_contents"
SOURCE_MAP = ARCHIVE / "_merge_state" / "source_map.csv"


def source_rows() -> dict[str, dict[str, str]]:
    with SOURCE_MAP.open(encoding="utf-8", newline="") as handle:
        return {row["file"]: row for row in csv.DictReader(handle)}


def extract_source(text: str) -> tuple[str, str, str]:
    source_url = ""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        frontmatter = text[4:end]
        match = re.search(r'^source_url:\s*"?([^"\n]+)', frontmatter, re.M)
        if match:
            source_url = match.group(1)
        text = text[end + 5 :]
    lines = text.splitlines()
    title = ""
    body: list[str] = []
    duplicate_removed = False
    for raw in lines:
        stripped = raw.strip()
        if not title and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if re.match(r"^Source:\s*<.*>$", stripped, re.I):
            continue
        if stripped.startswith("அறிஞர் அண்ணாவின் ") or stripped.endswith(" பட்டியல்"):
            continue
        if stripped == "முகப்பு | எழுத்து | பேச்சு | புகைப்படம் | ஓவியம் | தொடர்பு":
            continue
        if title and stripped == title and not duplicate_removed:
            duplicate_removed = True
            continue
        body.append(raw)
    if "/" in title:
        # OCR files use a generated `section/stem` heading. A printed title, when
        # present, is the first short text block after the first image marker.
        # Never scan later numbered lists or dates: they are body content.
        image_index = next(
            (index for index, raw in enumerate(body) if raw.strip().startswith("- Image:")),
            -1,
        )
        index = image_index + 1
        while index < len(body):
            if not body[index].strip():
                index += 1
                continue
            block: list[str] = []
            while index < len(body) and body[index].strip():
                block.append(body[index].strip().rstrip("/"))
                index += 1
            candidate = " ".join(block)
            if len(block) <= 3 and len(candidate) <= 140:
                numbered = re.match(
                    r"^[\[\(\s்]*\d+\s*[/.,)]*\s*(.+)$",
                    block[0],
                )
                title = numbered.group(1).strip() if numbered else candidate
                break
            # The first prose block is not safely identifiable as a title.
            break
    return title, source_url, "\n".join(body).strip()


def parse_draft(path: Path) -> tuple[str, str, str, str]:
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"Draft must start with '# English Title': {path}")
    title = lines[0][2:].strip()
    tamil_title_override = ""
    content_start = 1
    if len(lines) > 1 and lines[1].startswith("Tamil title: "):
        tamil_title_override = lines[1].removeprefix("Tamil title: ").strip()
        content_start = 2
    remainder = "\n".join(lines[content_start:]).strip()
    if "\n---NOTES---\n" in remainder:
        translation, notes = remainder.split("\n---NOTES---\n", 1)
    else:
        translation, notes = remainder, ""
    return title, tamil_title_override, translation.strip(), notes.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("relative_file")
    parser.add_argument("draft", type=Path, nargs="+")
    args = parser.parse_args()
    row = source_rows().get(args.relative_file)
    if not row:
        raise SystemExit(f"Not found in source map: {args.relative_file}")
    source_path = Path(row["chosen_path"])
    tamil_title, source_url, tamil = extract_source(source_path.read_text(encoding="utf-8", errors="replace"))
    parsed_drafts = [parse_draft(path) for path in args.draft]
    english_title = parsed_drafts[0][0]
    tamil_title_overrides = {draft[1] for draft in parsed_drafts if draft[1]}
    if len({draft[0] for draft in parsed_drafts}) != 1:
        raise SystemExit("All drafts must use the same English title")
    if len(tamil_title_overrides) > 1:
        raise SystemExit("Drafts contain conflicting Tamil title overrides")
    if tamil_title_overrides:
        tamil_title = tamil_title_overrides.pop()
    english = "\n\n".join(draft[2] for draft in parsed_drafts if draft[2])
    notes = "\n\n".join(draft[3] for draft in parsed_drafts if draft[3])
    lines = [
        f"# {tamil_title} / {english_title}", "",
        f"**Tamil title:** {tamil_title}  ",
        f"**English title:** {english_title}  ",
        f"**Source:** <{source_url}>" if source_url else f"**Source file:** `{args.relative_file}`",
        "", "## Source Tamil (verbatim)", "", tamil,
        "", "## English Translation", "", english,
    ]
    if notes:
        lines.extend(["", "## Translator's Notes", "", notes])
    destination = OUTPUT / args.relative_file
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
