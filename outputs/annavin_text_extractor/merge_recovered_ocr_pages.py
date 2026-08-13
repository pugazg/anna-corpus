#!/usr/bin/env python3
"""Merge newly recovered OCR into blank image blocks without replacing reviewed text."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


IMAGE_BLOCK = re.compile(
    r"(?ms)^## Image (?P<number>\d+): (?P<name>[^\n]+)\n\n"
    r"- Image: `(?P<image>[^`]+)`\n\n"
    r"(?P<body>.*?)(?=^## Image \d+:|\Z)"
)
BLANK_MARKERS = {"_No OCR text detected._", "No OCR text detected."}


def blocks(text: str) -> dict[str, re.Match[str]]:
    return {match.group("name"): match for match in IMAGE_BLOCK.finditer(text)}


def merge(target_text: str, recovered_text: str) -> tuple[str, list[str]]:
    recovered = blocks(recovered_text)
    replacements: list[tuple[int, int, str]] = []
    merged_names: list[str] = []

    for match in IMAGE_BLOCK.finditer(target_text):
        if match.group("body").strip() not in BLANK_MARKERS:
            continue
        source = recovered.get(match.group("name"))
        if not source or source.group("body").strip() in BLANK_MARKERS:
            continue
        replacement = (
            f"## Image {match.group('number')}: {match.group('name')}\n\n"
            f"- Image: `{match.group('image')}`\n\n"
            f"{source.group('body').strip()}\n\n"
        )
        replacements.append((match.start(), match.end(), replacement))
        merged_names.append(match.group("name"))

    updated = target_text
    for start, end, replacement in reversed(replacements):
        updated = updated[:start] + replacement + updated[end:]
    return updated.rstrip() + "\n", merged_names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("recovered", type=Path)
    parser.add_argument("--check", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    target_text = args.target.read_text(encoding="utf-8", errors="replace")
    recovered_text = args.recovered.read_text(encoding="utf-8", errors="replace")
    updated, names = merge(target_text, recovered_text)
    if not args.check and updated != target_text:
        args.target.write_text(updated, encoding="utf-8")
    action = "would merge" if args.check else "merged"
    print(f"{action} {len(names)} blank image block(s): {args.target}")
    for name in names:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
