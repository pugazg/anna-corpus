#!/usr/bin/env python3
"""Build a resumable translation queue from the organized Markdown archive."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "organized_contents"
DEFAULT_OUTPUT = SCRIPT_DIR / "translated_contents"
INCORRECT_SOURCES = DEFAULT_OUTPUT / "_translation_state" / "incorrect_sources.csv"

EXCLUDED_SECTIONS = {"oviyam", "photos", "_merge_state"}
BOILERPLATE_PATTERNS = (
    r"^Source:\s*<.*>$",
    r"^அறிஞர் அண்ணாவின் .+$",
    r"^.+ பட்டியல்$",
    r"^முகப்பு \| எழுத்து \| பேச்சு \| புகைப்படம் \| ஓவியம் \| தொடர்பு$",
    r"^- Source image folder:.*$",
    r"^- OCR language:.*$",
    r"^- Tesseract page segmentation mode:.*$",
    r"^- OCR cleanup:.*$",
    r"^- Image:.*$",
    r"^## Image \d+:.*$",
)
BOILERPLATE_REGEXES = tuple(re.compile(pattern, re.I) for pattern in BOILERPLATE_PATTERNS)


def load_incorrect_sources(path: Path = INCORRECT_SOURCES) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["file"]: row.get("reason", "Source explicitly marked incorrect")
            for row in csv.DictReader(handle)
            if row.get("file")
        }


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5 :]
    return text


def meaningful_text(text: str) -> str:
    text = strip_frontmatter(text)
    kept: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line in {"_No OCR text detected._", "No OCR text detected."}:
            continue
        if any(pattern.match(line) for pattern in BOILERPLATE_REGEXES):
            continue
        kept.append(line)
    return "\n".join(kept)


def classify(source: Path, already_translated: bool) -> tuple[str, str, str, int, int]:
    # Classification only needs enough text to distinguish content from an
    # empty/navigation page; long novels are read fully only during translation.
    with source.open("r", encoding="utf-8", errors="replace") as handle:
        text = handle.read(8192)
    body = meaningful_text(text)
    tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", body))
    latin_words = len(re.findall(r"[A-Za-z]{2,}", body))

    if already_translated:
        return "translated", "complete", "existing translated output", tamil_chars, latin_words
    if "_No OCR text detected._" in text and tamil_chars < 40:
        return "needs_source_recovery", "undetermined", "OCR detected no usable text", tamil_chars, latin_words
    if tamil_chars < 40:
        if latin_words >= 20:
            return "ready", "english_to_tamil", "English body available", tamil_chars, latin_words
        return "needs_source_recovery", "undetermined", "navigation, metadata, or title only", tamil_chars, latin_words
    return "ready", "tamil_to_english", "Tamil body available", tamil_chars, latin_words


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--inspect-content",
        action="store_true",
        help="Inspect source text to assign direction and flag empty pages (slower).",
    )
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    state_dir = output_dir / "_translation_state"
    state_dir.mkdir(parents=True, exist_ok=True)

    source_map = input_dir / "_merge_state" / "source_map.csv"
    if not source_map.exists():
        raise SystemExit(f"Missing archive source map: {source_map}")
    with source_map.open(encoding="utf-8", newline="") as handle:
        intended_files = sorted(
            (row["file"], row.get("chosen_path") or "")
            for row in csv.DictReader(handle)
            if row.get("file")
        )

    rows: list[dict[str, object]] = []
    translated_keys = {
        path.relative_to(output_dir).as_posix()
        for path in output_dir.rglob("*.md")
        if "_translation_state" not in path.parts and path.name != "TRANSLATION_GUIDE.md"
    }
    incorrect_sources = load_incorrect_sources(state_dir / "incorrect_sources.csv")
    for rel_value, chosen_path in intended_files:
        rel = Path(rel_value)
        if rel.name == "index.md" or any(part in EXCLUDED_SECTIONS for part in rel.parts):
            continue
        source = Path(chosen_path) if chosen_path else input_dir / rel
        translated = output_dir / rel
        already_translated = rel.as_posix() in translated_keys
        if rel.as_posix() in incorrect_sources:
            status, direction, reason, tamil_chars, latin_words = (
                "incorrect_source", "none", incorrect_sources[rel.as_posix()], 0, 0
            )
        elif already_translated:
            status, direction, reason, tamil_chars, latin_words = (
                "translated", "complete", "existing translated output", 0, 0
            )
        elif args.inspect_content:
            status, direction, reason, tamil_chars, latin_words = classify(source, False)
        else:
            status, direction, reason, tamil_chars, latin_words = (
                "pending", "auto_detect", "awaiting content inspection", 0, 0
            )
        rows.append({
            "file": rel.as_posix(),
            "status": status,
            "direction": direction,
            "reason": reason,
            "tamil_characters": tamil_chars,
            "latin_words": latin_words,
            "source_path": str(source.resolve()),
            "translated_path": str(translated),
        })

    queue_path = state_dir / "translation_queue.csv"
    fields = list(rows[0]) if rows else ["file", "status", "reason"]
    with queue_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(str(row["status"]) for row in rows)
    summary = [
        "# Translation Queue Summary",
        "",
        f"- Documents considered: {len(rows)}",
        f"- Pending content inspection: {counts['pending']}",
        f"- Ready for translation: {counts['ready']}",
        f"- Already translated: {counts['translated']}",
        f"- Needs source/OCR recovery: {counts['needs_source_recovery']}",
        f"- Incorrect sources skipped: {counts['incorrect_source']}",
        f"- Tamil to English: {sum(row['status'] == 'ready' and row['direction'] == 'tamil_to_english' for row in rows)}",
        f"- English to Tamil: {sum(row['status'] == 'ready' and row['direction'] == 'english_to_tamil' for row in rows)}",
        "",
        "The source archive is never modified. Re-running this command resumes by",
        "recognizing non-empty files already present in `translated_contents/`.",
    ]
    (state_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    print(f"\nQueue: {queue_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
