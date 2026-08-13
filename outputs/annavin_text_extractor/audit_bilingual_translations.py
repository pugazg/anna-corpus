#!/usr/bin/env python3
"""Audit completed translations for both languages and exact source retention."""

import csv
import importlib.util
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
ORGANIZED = BASE / "organized_contents"
TRANSLATED = BASE / "translated_contents"
SOURCE_MAP = ORGANIZED / "_merge_state/source_map.csv"
REPORT = TRANSLATED / "_translation_state/bilingual_audit.md"
STATUS_MD = TRANSLATED / "_translation_state/section_translation_status.md"
STATUS_CSV = TRANSLATED / "_translation_state/section_translation_status.csv"
RECOVERY_CSV = TRANSLATED / "_translation_state/needs_source_recovery.csv"
IGNORED_SECTIONS = {"oviyam", "photos"}


def blank_ocr_pages(text: str) -> int:
    """Count explicit and structurally empty OCR image sections."""
    sections = re.split(r"(?m)^## Image \d+:[^\n]*\n", text)[1:]
    blank_count = 0
    for section in sections:
        content_lines = []
        for raw in section.splitlines():
            stripped = raw.strip()
            if not stripped or stripped.startswith("- Image:"):
                continue
            content_lines.append(stripped)
        has_explicit_marker = any(
            line in {"_No OCR text detected._", "[No text recognized]"}
            for line in content_lines
        )
        if has_explicit_marker or not content_lines or all(
            line in {"_No OCR text detected._", "[No text recognized]"}
            for line in content_lines
        ):
            blank_count += 1
    return blank_count


def load_tamil_extractor():
    spec = importlib.util.spec_from_file_location("translation_builder", BASE / "build_manual_translation.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module.extract_source


def between(text: str, start: str, end: str | None = None) -> str:
    if start not in text:
        return ""
    value = text.split(start, 1)[1]
    if end and end in value:
        value = value.split(end, 1)[0]
    return value.strip()


def main() -> int:
    extract_tamil = load_tamil_extractor()
    with SOURCE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with RECOVERY_CSV.open(encoding="utf-8-sig", newline="") as handle:
        manual_recovery = {row["file"]: row["reason"] for row in csv.DictReader(handle)}

    section_counts = defaultdict(lambda: {"total": 0, "done": 0, "valid": 0})
    ocr_counts = defaultdict(lambda: {"total": 0, "done": 0, "valid": 0})
    ocr_source_gaps = defaultdict(lambda: {"works": 0, "pages": 0})
    source_gap_files = []
    manual_gap_files = []
    issues = []
    for row in rows:
        section = row["section"] or "root"
        if section in IGNORED_SECTIONS:
            continue
        is_ocr = row["source"] in {"ocr_replaces_html", "ocr_only"}
        section_counts[section]["total"] += 1
        if is_ocr:
            ocr_counts[section]["total"] += 1
        relative = Path(row["file"])
        chosen = Path(row["chosen_path"])
        if is_ocr:
            raw_source = chosen.read_text(encoding="utf-8", errors="replace")
            blank_pages = blank_ocr_pages(raw_source)
            if blank_pages:
                ocr_source_gaps[section]["works"] += 1
                ocr_source_gaps[section]["pages"] += blank_pages
                source_gap_files.append((relative.as_posix(), blank_pages))
            if relative.as_posix() in manual_recovery:
                manual_gap_files.append((relative.as_posix(), manual_recovery[relative.as_posix()]))
        target = TRANSLATED / relative
        if not target.exists():
            continue
        section_counts[section]["done"] += 1
        if is_ocr:
            ocr_counts[section]["done"] += 1
        text = target.read_text(encoding="utf-8", errors="replace")
        if "## Source Tamil (verbatim)" in text:
            source = between(text, "## Source Tamil (verbatim)", "## English Translation")
            translation = between(text, "## English Translation")
            expected = extract_tamil(chosen.read_text(encoding="utf-8", errors="replace"))[2]
            language_ok = bool(source and translation)
            source_ok = source == expected
        elif "## Source English (verbatim)" in text:
            source = between(text, "## Source English (verbatim)", "## Tamil Translation")
            translation = between(text, "## Tamil Translation", "## Translator Notes")
            raw_source = chosen.read_text(encoding="utf-8", errors="replace")
            # English catalogue files retain the complete Markdown source, while
            # individual articles use the same website-boilerplate extraction as Tamil works.
            expected_options = {raw_source.strip(), extract_tamil(raw_source)[2]}
            language_ok = bool(source and translation)
            source_ok = source in expected_options
        else:
            language_ok = False
            source_ok = False

        source_complete = not (is_ocr and blank_ocr_pages(raw_source))

        if language_ok and source_ok and source_complete:
            section_counts[section]["valid"] += 1
            if is_ocr:
                ocr_counts[section]["valid"] += 1
        else:
            reasons = []
            if not language_ok:
                reasons.append("missing or empty language block")
            if not source_ok:
                reasons.append("source block differs from organized source")
            if not source_complete:
                reasons.append("OCR source contains one or more blank-page markers; scan recovery required")
            issues.append((relative.as_posix(), "; ".join(reasons)))

    total = sum(x["total"] for x in section_counts.values())
    done = sum(x["done"] for x in section_counts.values())
    valid = sum(x["valid"] for x in section_counts.values())
    lines = [
        "# Bilingual Translation Audit", "",
        "`photos` and `oviyam` are excluded from the translation workload.", "",
        "| Section | Translation target | Completed | Bilingual with source retained | Pending |", 
        "|---|---:|---:|---:|---:|",
    ]
    for section in sorted(section_counts, key=str.lower):
        values = section_counts[section]
        lines.append(
            f"| {section} | {values['total']} | {values['done']} | {values['valid']} | "
            f"{values['total'] - values['done']} |"
        )
    lines.extend([
        f"| **All included sections** | **{total}** | **{done}** | **{valid}** | **{total - done}** |",
        "", "## OCR-Origin Translation Progress", "",
        "| Section | OCR target | Completed | Bilingual with source retained | Pending |",
        "|---|---:|---:|---:|---:|",
    ])
    for section in sorted(ocr_counts, key=str.lower):
        values = ocr_counts[section]
        lines.append(
            f"| {section} | {values['total']} | {values['done']} | {values['valid']} | "
            f"{values['total'] - values['done']} |"
        )
    ocr_total = sum(x["total"] for x in ocr_counts.values())
    ocr_done = sum(x["done"] for x in ocr_counts.values())
    ocr_valid = sum(x["valid"] for x in ocr_counts.values())
    lines.extend([
        f"| **All OCR-origin sections** | **{ocr_total}** | **{ocr_done}** | **{ocr_valid}** | **{ocr_total - ocr_done}** |",
        "", "## OCR Source Recovery Status", "",
        "| Section | Works with blank image sections | Blank pages |",
        "|---|---:|---:|",
    ])
    for section in sorted(ocr_counts, key=str.lower):
        gaps = ocr_source_gaps[section]
        lines.append(f"| {section} | {gaps['works']} | {gaps['pages']} |")
    gap_works = sum(x["works"] for x in ocr_source_gaps.values())
    gap_pages = sum(x["pages"] for x in ocr_source_gaps.values())
    lines.extend([
        f"| **All OCR-origin sections** | **{gap_works}** | **{gap_pages}** |",
        "",
        "A blank image section has an explicit no-text marker or no OCR body after its image reference. The canonical Tamil source is not translation-ready even when the scan itself may be readable.",
        "",
        "### Sources Requiring Recovery", "",
    ])
    if source_gap_files:
        lines.extend(f"- `{path}`: {pages} blank page(s)" for path, pages in source_gap_files)
    else:
        lines.append("None.")
    lines.extend(["", "### Manually Verified Recovery Holds", ""])
    if manual_gap_files:
        lines.extend(f"- `{path}`: {reason}" for path, reason in manual_gap_files)
    else:
        lines.append("None.")
    lines.extend([
        "", "## English Essay Clarification", "",
        "The `english` inventory entry is only a 129-title catalogue. The actual English essay bodies are stored under `katturaigal`; only `we_welcome.md` has been translated so far.",
        "", "## Issues", "",
    ])
    if issues:
        lines.extend(f"- `{path}`: {reason}" for path, reason in issues)
    else:
        lines.append("No bilingual or source-retention issues found in completed translations.")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    status_lines = [
        "# Translation Status by Category and Source Origin", "",
        "Inventory source: `organized_contents/_merge_state/source_map.csv`", "",
        "`photos` and `oviyam` are excluded from the translation workload.", "",
        "| Category | OCR total | OCR translated | OCR source retained | OCR pending | HTML total | HTML translated | HTML source retained | HTML pending | All total | All translated | All source retained | All pending |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    status_rows = []
    for section in sorted(section_counts, key=str.lower):
        all_values = section_counts[section]
        ocr_values = ocr_counts[section]
        html_total = all_values["total"] - ocr_values["total"]
        html_done = all_values["done"] - ocr_values["done"]
        html_valid = all_values["valid"] - ocr_values["valid"]
        values = {
            "section": section,
            "ocr_total": ocr_values["total"],
            "ocr_done": ocr_values["done"],
            "ocr_valid": ocr_values["valid"],
            "ocr_pending": ocr_values["total"] - ocr_values["done"],
            "html_total": html_total,
            "html_done": html_done,
            "html_valid": html_valid,
            "html_pending": html_total - html_done,
            "total": all_values["total"],
            "done": all_values["done"],
            "valid": all_values["valid"],
            "pending": all_values["total"] - all_values["done"],
        }
        status_rows.append(values)
        status_lines.append(
            f"| {section} | {values['ocr_total']} | {values['ocr_done']} | {values['ocr_valid']} | {values['ocr_pending']} | "
            f"{values['html_total']} | {values['html_done']} | {values['html_valid']} | {values['html_pending']} | "
            f"{values['total']} | {values['done']} | {values['valid']} | {values['pending']} |"
        )
    html_total = total - ocr_total
    html_done = done - ocr_done
    html_valid = valid - ocr_valid
    status_lines.extend([
        f"| **All included categories** | **{ocr_total}** | **{ocr_done}** | **{ocr_valid}** | **{ocr_total - ocr_done}** | "
        f"**{html_total}** | **{html_done}** | **{html_valid}** | **{html_total - html_done}** | "
        f"**{total}** | **{done}** | **{valid}** | **{total - done}** |",
        "", "## Verification", "",
        f"- All {valid} completed files are bilingual and retain their organized source text exactly.",
        "- `Source retained` is an automated fidelity check; it does not claim character-by-character comparison against every scan.",
        f"- Bilingual or source-retention issues: {len(issues)}.",
        f"- OCR-origin progress: {ocr_done} of {ocr_total} files translated ({ocr_done / ocr_total:.1%}).",
        f"- HTML-origin progress: {html_done} of {html_total} files translated ({html_done / html_total:.1%}).",
        f"- Overall progress: {done} of {total} files translated ({done / total:.1%}).",
    ])
    STATUS_MD.write_text("\n".join(status_lines) + "\n", encoding="utf-8")
    with STATUS_CSV.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "section", "ocr_total", "ocr_translated", "ocr_verified", "ocr_pending",
            "html_total", "html_translated", "html_verified", "html_pending",
            "total", "translated", "verified", "pending",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for values in status_rows:
            writer.writerow({
                "section": values["section"],
                "ocr_total": values["ocr_total"],
                "ocr_translated": values["ocr_done"],
                "ocr_verified": values["ocr_valid"],
                "ocr_pending": values["ocr_pending"],
                "html_total": values["html_total"],
                "html_translated": values["html_done"],
                "html_verified": values["html_valid"],
                "html_pending": values["html_pending"],
                "total": values["total"],
                "translated": values["done"],
                "verified": values["valid"],
                "pending": values["pending"],
            })
        writer.writerow({
            "section": "ALL_INCLUDED",
            "ocr_total": ocr_total,
            "ocr_translated": ocr_done,
            "ocr_verified": ocr_valid,
            "ocr_pending": ocr_total - ocr_done,
            "html_total": html_total,
            "html_translated": html_done,
            "html_verified": html_valid,
            "html_pending": html_total - html_done,
            "total": total,
            "translated": done,
            "verified": valid,
            "pending": total - done,
        })
    print(f"Translation target: {total}")
    print(f"Completed: {done}")
    print(f"Bilingual and source-verified: {valid}")
    print(f"Pending: {total - done}")
    print(f"Issues: {len(issues)}")
    print(f"Report: {REPORT}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
