#!/usr/bin/env python3
"""Restore verbatim HTML source text inside completed translation files."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_MAP = ROOT / "organized_contents" / "_merge_state" / "source_map.csv"
TRANSLATED = ROOT / "translated_contents"
REPORT = TRANSLATED / "_translation_state" / "verbatim_source_sync.csv"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5 :]
    return text


def extract_verbatim_body(text: str) -> tuple[str, str]:
    lines = strip_frontmatter(text).splitlines()
    title = ""
    output: list[str] = []
    title_removed = False
    for raw in lines:
        stripped = raw.strip()
        if not title and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if re.match(r"^Source:\s*<.*>$", stripped, re.I):
            continue
        if stripped.startswith("அறிஞர் அண்ணாவின் "):
            continue
        if stripped.endswith(" பட்டியல்"):
            continue
        if stripped == "முகப்பு | எழுத்து | பேச்சு | புகைப்படம் | ஓவியம் | தொடர்பு":
            continue
        if title and stripped == title and not title_removed:
            title_removed = True
            continue
        output.append(raw)
    return title, "\n".join(output).strip()


def replace_source_section(translated: str, body: str, language: str) -> str:
    pattern = re.compile(
        r"^## (?:Corrected|Source) (?:Tamil|English)(?: \(verbatim\))?\n\n.*?(?=^## (?:English|Tamil) Translation\n)",
        re.MULTILINE | re.DOTALL,
    )
    replacement = f"## Source {language} (verbatim)\n\n{body}\n\n"
    updated, count = pattern.subn(replacement, translated, count=1)
    if count != 1:
        raise ValueError("source section not found")
    return updated


def main() -> int:
    with SOURCE_MAP.open(encoding="utf-8", newline="") as handle:
        source_rows = {row["file"]: row for row in csv.DictReader(handle)}

    report_rows: list[dict[str, str]] = []
    for translated_path in sorted(TRANSLATED.rglob("*.md")):
        if "_translation_state" in translated_path.parts or translated_path.name == "TRANSLATION_GUIDE.md":
            continue
        rel = translated_path.relative_to(TRANSLATED).as_posix()
        row = source_rows.get(rel)
        if not row:
            report_rows.append({"file": rel, "action": "skipped", "reason": "not in source map"})
            continue
        if row.get("source") != "html":
            report_rows.append({"file": rel, "action": "skipped", "reason": "OCR source requires reviewed corrections"})
            continue
        source_path = Path(row["chosen_path"])
        _, body = extract_verbatim_body(source_path.read_text(encoding="utf-8", errors="replace"))
        translated_text = translated_path.read_text(encoding="utf-8")
        language = "Tamil" if len(re.findall(r"[\u0B80-\u0BFF]", body)) >= 40 else "English"
        updated = replace_source_section(translated_text, body, language)
        if updated != translated_text:
            translated_path.write_text(updated, encoding="utf-8")
            report_rows.append({"file": rel, "action": "restored", "reason": f"verbatim {language} HTML source"})
        else:
            report_rows.append({"file": rel, "action": "unchanged", "reason": "already verbatim"})

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "action", "reason"])
        writer.writeheader()
        writer.writerows(report_rows)
    restored = sum(row["action"] == "restored" for row in report_rows)
    skipped = sum(row["action"] == "skipped" for row in report_rows)
    print(f"Restored verbatim source sections: {restored}")
    print(f"Skipped for manual handling: {skipped}")
    print(f"Report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

