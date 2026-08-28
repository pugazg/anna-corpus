#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_MAP = ROOT / "organized_contents/_merge_state/source_map.csv"
TRANSLATED = ROOT / "translated_contents"
RECOVERY = TRANSLATED / "_translation_state/needs_source_recovery.csv"
MANIFEST = ROOT / "ocr_images/_state/manifest.jsonl"
OUTPUT = TRANSLATED / "_translation_state/ocr_pending_links.md"
GITHUB_ROOT = (
    "https://github.com/pugazg/anna-corpus/blob/main/"
    "outputs/annavin_text_extractor"
)


def load_recovery_holds():
    with RECOVERY.open(encoding="utf-8-sig", newline="") as handle:
        return {row["file"]: row["reason"] for row in csv.DictReader(handle)}


def load_page_urls():
    urls = {}
    with MANIFEST.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            page_url = row.get("page_url")
            ocr_path = row.get("ocr_path", "")
            if not page_url or "/ocr_images/" not in ocr_path:
                continue
            relative = ocr_path.split("/ocr_images/", 1)[1]
            parts = Path(relative).parts
            if len(parts) >= 3:
                key = Path(*parts[:2]).as_posix()
                urls.setdefault(key, [])
                if page_url not in urls[key]:
                    urls[key].append(page_url)
    return urls


def urls_for(relative, page_urls):
    path = Path(relative)
    section = path.parent.as_posix()
    stem = path.stem
    if stem.endswith(".htm"):
        stem = stem[:-4]
    matches = []
    for key, urls in page_urls.items():
        candidate = Path(key)
        if candidate.parent.as_posix() != section:
            continue
        if candidate.name == stem or candidate.name.startswith(stem + "_"):
            for url in urls:
                if url not in matches:
                    matches.append(url)
    return matches


def has_blank_page_marker(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    markers = (
        "No OCR text was extracted",
        "No OCR text detected",
        "No text extracted",
        "OCR text unavailable",
    )
    return any(marker in text for marker in markers)


def main():
    holds = load_recovery_holds()
    page_urls = load_page_urls()
    pending = []
    with SOURCE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["source"] not in {"ocr_replaces_html", "ocr_only"}:
                continue
            relative = row["file"]
            if (TRANSLATED / relative).exists():
                continue
            source_path = Path(row["chosen_path"])
            recovery_reason = holds.get(relative)
            if recovery_reason:
                state = "OCR/source recovery pending"
                reason = recovery_reason
            elif has_blank_page_marker(source_path):
                state = "OCR/source recovery pending"
                reason = "One or more image sections contain no extracted OCR text."
            else:
                state = "OCR translation pending"
                reason = "OCR source exists; bilingual translation has not yet been created."
            pending.append((row["section"], relative, state, reason, urls_for(relative, page_urls)))

    pending.sort(key=lambda item: (item[2], item[0].lower(), item[1].lower()))
    state_counts = Counter(item[2] for item in pending)
    section_counts = Counter(item[0] for item in pending)
    lines = [
        "# Pending OCR and OCR Translation Links",
        "",
        "This report covers only canonical OCR-origin works that do not yet have a bilingual translation file.",
        "",
        f"- Total pending: **{len(pending)}**",
        f"- OCR/source recovery pending: **{state_counts['OCR/source recovery pending']}**",
        f"- OCR translation pending: **{state_counts['OCR translation pending']}**",
        "",
        "## Category Summary",
        "",
        "| Category | Pending |",
        "|---|---:|",
    ]
    for section in sorted(section_counts, key=str.lower):
        lines.append(f"| {section} | {section_counts[section]} |")

    for state in ("OCR/source recovery pending", "OCR translation pending"):
        lines.extend(["", f"## {state}", ""])
        items = [item for item in pending if item[2] == state]
        if not items:
            lines.append("None.")
            continue
        for _, relative, _, reason, page_urls_for_file in items:
            if page_urls_for_file:
                website = ", ".join(
                    f"[website {index}]({url})"
                    for index, url in enumerate(page_urls_for_file, start=1)
                )
            else:
                website = "website URL unavailable"
            source = f"[OCR Markdown]({GITHUB_ROOT}/ocr_text_corrected/{relative})"
            lines.append(f"- `{relative}`: {website} | {source}")
            if state == "OCR/source recovery pending":
                lines.append(f"  - Reason: {reason}")

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(dict(state_counts))
    print(dict(section_counts))


if __name__ == "__main__":
    main()
