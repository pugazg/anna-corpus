#!/usr/bin/env python3
"""
Apply audited OCR corrections to Annavin Markdown OCR output.

This is the Markdown equivalent of the correction stage used in the Kalaignar
OCR pipeline: normalize text, apply reviewed token/phrase corrections, write
every input Markdown file to the output folder, and keep CSV reports.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SRC = SCRIPT_DIR / "ocr_text"
DEFAULT_OUT = SCRIPT_DIR / "ocr_text_corrected"
DEFAULT_CORRECTIONS = SCRIPT_DIR / "reference_verified_source_dictionary" / "automatic_corrections.csv"
DEFAULT_CURATED = SCRIPT_DIR / "curated" / "annavin-ocr-overrides.json"

CONF_ORDER = {"low": 0, "medium": 1, "high": 2}
ZERO_WIDTH = re.compile(r"[\u200b\u200c\u200d\ufeff]")
TOKEN_SHAPE = re.compile(r'^([\'"“”‘’(\[«]*)(.*?)([\'"“”‘’)\]»,.!?;:…]*)$', re.S)
TAMIL = re.compile(r"[\u0b80-\u0bff]")
LATIN_TOKEN = re.compile(r"\b[A-Za-z][A-Za-z.]*\b")
INVALID_TAMIL_SEQUENCE = re.compile(r"[ாிீுூெேைொோௌ][்ாிீுூெேைொோௌ]")
NUMBERED_STEM = re.compile(r"^(.+?)(?:_part([0-9]+)|_([0-9]+))$", re.IGNORECASE)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def norm(text: str) -> str:
    return ZERO_WIDTH.sub("", unicodedata.normalize("NFC", text))


def split_token(token: str) -> tuple[str, str, str]:
    match = TOKEN_SHAPE.match(token)
    if not match:
        return "", token, ""
    return match.group(1), match.group(2), match.group(3)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_token_corrections(paths: list[Path], min_confidence: str) -> dict[str, dict[str, str]]:
    threshold = CONF_ORDER[min_confidence]
    mapping: dict[str, dict[str, str]] = {}
    for path in paths:
        for row in read_csv_rows(path):
            wrong = norm((row.get("wrong") or "").strip())
            right = norm((row.get("right") or "").strip())
            confidence = (row.get("confidence") or "medium").strip().lower()
            if not wrong or not right or wrong == right:
                continue
            if CONF_ORDER.get(confidence, 1) < threshold:
                continue
            mapping[wrong] = {
                "right": right,
                "confidence": confidence,
                "category": (row.get("category") or "").strip(),
                "reason": (row.get("reason") or "").strip(),
                "source": str(path),
            }
    return mapping


def load_curated(paths: list[Path]) -> dict[str, dict[str, list[dict[str, str]]]]:
    merged: dict[str, dict[str, list[dict[str, str]]]] = {}
    for path in paths:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        files = data.get("files", {}) if isinstance(data, dict) else {}
        for file_name, entry in files.items():
            target = merged.setdefault(file_name, {"phraseCorrections": [], "tokenCorrections": []})
            for key in ("phraseCorrections", "tokenCorrections"):
                values = entry.get(key, []) if isinstance(entry, dict) else []
                if isinstance(values, list):
                    for value in values:
                        if isinstance(value, dict) and value.get("wrong") and value.get("right"):
                            target[key].append({k: str(v) for k, v in value.items()})
    return merged


def find_markdown_files(src: Path, page_filters: list[str]) -> list[Path]:
    files = []
    normalized_filters = [item.lower().strip("/") for item in page_filters if item.strip()]
    for path in src.rglob("*.md"):
        rel = path.relative_to(src).as_posix()
        if any(part.startswith("_") for part in path.relative_to(src).parts):
            continue
        if normalized_filters and not any(item in rel.lower() for item in normalized_filters):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(src).as_posix().lower())


def numbered_part_info(path: Path, src: Path) -> tuple[str, int] | None:
    rel = path.relative_to(src)
    match = NUMBERED_STEM.match(path.stem)
    if not match:
        return None
    part_number = int(match.group(2) or match.group(3))
    base_name = match.group(1) + path.suffix
    base_rel = rel.with_name(base_name).as_posix()
    return base_rel, part_number


def build_processing_items(files: list[Path], src: Path, combine_numbered_pages: bool) -> list[dict[str, object]]:
    if not combine_numbered_pages:
        return [
            {
                "output_rel": path.relative_to(src).as_posix(),
                "sources": [(path, None)],
                "combined": False,
            }
            for path in files
        ]

    groups: dict[str, list[tuple[int, Path]]] = {}
    singles: list[Path] = []
    grouped_paths: set[Path] = set()
    for path in files:
        info = numbered_part_info(path, src)
        if not info:
            singles.append(path)
            continue
        base_rel, part_number = info
        groups.setdefault(base_rel, []).append((part_number, path))

    items: list[dict[str, object]] = []
    for base_rel, parts in groups.items():
        if len(parts) <= 1:
            singles.append(parts[0][1])
            continue
        parts.sort(key=lambda item: item[0])
        grouped_paths.update(path for _, path in parts)
        items.append(
            {
                "output_rel": base_rel,
                "sources": [(path, part_number) for part_number, path in parts],
                "combined": True,
            }
        )

    for path in singles:
        if path in grouped_paths:
            continue
        items.append(
            {
                "output_rel": path.relative_to(src).as_posix(),
                "sources": [(path, None)],
                "combined": False,
            }
        )
    return sorted(items, key=lambda item: str(item["output_rel"]).lower())


def apply_phrase_corrections(text: str, rel: str, curated: dict[str, dict[str, list[dict[str, str]]]], events: list[dict[str, object]]) -> str:
    entry = curated.get(rel) or curated.get(Path(rel).stem) or {}
    for rule in entry.get("phraseCorrections", []):
        wrong = norm(rule["wrong"])
        right = norm(rule["right"])
        count = text.count(wrong)
        if count:
            text = text.replace(wrong, right)
            events.append(
                {
                    "file": rel,
                    "type": "phrase",
                    "wrong": wrong,
                    "right": right,
                    "count": count,
                    "reason": rule.get("reason", "curated"),
                }
            )
    return text


def token_rules_for_file(rel: str, curated: dict[str, dict[str, list[dict[str, str]]]], mapping: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    rules = dict(mapping)
    entry = curated.get(rel) or curated.get(Path(rel).stem) or {}
    for rule in entry.get("tokenCorrections", []):
        wrong = norm(rule["wrong"])
        right = norm(rule["right"])
        if wrong and right:
            rules[wrong] = {
                "right": right,
                "confidence": "high",
                "category": "curated",
                "reason": rule.get("reason", "curated"),
                "source": "curated",
            }
    return rules


def apply_token_corrections(text: str, rel: str, mapping: dict[str, dict[str, str]], events: list[dict[str, object]]) -> tuple[str, int]:
    counts: Counter[tuple[str, str, str]] = Counter()
    fixed_parts: list[str] = []
    fixes = 0
    for token in re.split(r"(\s+)", text):
        if not token or token.isspace():
            fixed_parts.append(token)
            continue
        lead, core, trail = split_token(token)
        if core in mapping:
            right = mapping[core]["right"]
            fixed_parts.append(lead + right + trail)
            fixes += 1
            counts[(core, right, mapping[core].get("reason", ""))] += 1
        elif token in mapping:
            right = mapping[token]["right"]
            fixed_parts.append(right)
            fixes += 1
            counts[(token, right, mapping[token].get("reason", ""))] += 1
        else:
            fixed_parts.append(token)

    for (wrong, right, reason), count in counts.items():
        events.append(
            {
                "file": rel,
                "type": "token",
                "wrong": wrong,
                "right": right,
                "count": count,
                "reason": reason,
            }
        )
    return "".join(fixed_parts), fixes


def body_lines(text: str) -> list[str]:
    lines = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("- Source image folder:"):
            continue
        if stripped.startswith("- OCR ") or stripped.startswith("- Tesseract ") or stripped.startswith("- Image:"):
            continue
        lines.append(line)
    return lines


def collect_review_candidates(text: str, rel: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_no, line in enumerate(body_lines(text), start=1):
        if TAMIL.search(line):
            for token in LATIN_TOKEN.findall(line):
                rows.append({"file": rel, "line": str(line_no), "token": token, "issue": "latin_in_tamil_line", "context": line.strip()})
        for token in re.split(r"\s+", line):
            _, core, _ = split_token(token)
            if core and INVALID_TAMIL_SEQUENCE.search(core):
                rows.append({"file": rel, "line": str(line_no), "token": core, "issue": "invalid_tamil_sequence", "context": line.strip()})
    return rows


def extract_part_body(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("## "):
            return "\n".join(lines[index:]).strip()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and (not lines[0].strip() or lines[0].startswith("- ")):
        lines = lines[1:]
    return "\n".join(lines).strip()


def demote_markdown_headings(text: str) -> str:
    demoted = []
    for line in text.splitlines():
        if line.startswith("###### "):
            demoted.append(line)
        elif line.startswith("#"):
            demoted.append("#" + line)
        else:
            demoted.append(line)
    return "\n".join(demoted).strip()


def combined_markdown(output_rel: str, parts: list[dict[str, object]]) -> str:
    title = Path(output_rel).with_suffix("").as_posix()
    lines = [
        f"# {title}",
        "",
        f"- Combined OCR parts: {len(parts)}",
        "- OCR correction stage: `apply_ocr_corrections.py`",
        "",
    ]
    for index, part in enumerate(parts, start=1):
        part_rel = str(part["rel"])
        part_number = part.get("part_number") or index
        lines.extend(
            [
                f"## Part {part_number}: {Path(part_rel).name}",
                "",
                f"- Source OCR file: `{part_rel}`",
                "",
            ]
        )
        body = demote_markdown_headings(extract_part_body(str(part["text"])))
        lines.extend([body or "_No OCR text detected._", ""])
    return "\n".join(lines).rstrip() + "\n"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply reviewed OCR corrections to Annavin OCR Markdown.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC, help="Source OCR Markdown folder.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Corrected Markdown output folder.")
    parser.add_argument("--corrections", action="append", type=Path, default=[], help="Correction CSV. Can be repeated.")
    parser.add_argument("--curated", action="append", type=Path, default=[], help="Curated override JSON. Can be repeated.")
    parser.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium", help="Minimum correction confidence to apply.")
    parser.add_argument("--page", action="append", default=[], help="Only process relative paths containing this text. Can be repeated.")
    parser.add_argument("--combine-numbered-pages", action=argparse.BooleanOptionalAction, default=True, help="Combine numbered OCR Markdown files into one corrected file.")
    parser.add_argument("--quiet", action="store_true", help="Print only final summary.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.src = args.src.resolve()
    args.out = args.out.resolve()

    correction_paths = args.corrections or [DEFAULT_CORRECTIONS]
    curated_paths = args.curated or [DEFAULT_CURATED]
    mapping = load_token_corrections([path.resolve() for path in correction_paths], args.min_confidence)
    curated = load_curated([path.resolve() for path in curated_paths])

    files = find_markdown_files(args.src, args.page)
    items = build_processing_items(files, args.src, args.combine_numbered_pages)
    report: list[dict[str, object]] = []
    events: list[dict[str, object]] = []
    review_rows: list[dict[str, str]] = []

    print(f"Source OCR folder: {args.src}", flush=True)
    print(f"Corrected output folder: {args.out}", flush=True)
    print(f"Markdown files to process: {len(files)}", flush=True)
    print(f"Corrected files to write: {len(items)}", flush=True)
    print(f"Combine numbered pages: {'yes' if args.combine_numbered_pages else 'no'}", flush=True)
    print(f"Token correction rules loaded: {len(mapping)}", flush=True)

    combined_count = 0
    stale_removed = 0
    for index, item in enumerate(items, start=1):
        output_rel = str(item["output_rel"])
        if not args.quiet:
            source_count = len(item["sources"])
            suffix = f" ({source_count} source files)" if item["combined"] else ""
            print(f"[{index}/{len(items)}] {output_rel}{suffix}", flush=True)

        part_records: list[dict[str, object]] = []
        normalized_changed = False
        phrase_fixes = 0
        token_fixes = 0
        item_review_count = 0
        for src_path, part_number in item["sources"]:
            rel = src_path.relative_to(args.src).as_posix()
            original = src_path.read_text(encoding="utf-8", errors="replace")
            text = norm(original)
            normalized_changed = normalized_changed or text != original
            before_phrases = len(events)
            text = apply_phrase_corrections(text, rel, curated, events)
            rules = token_rules_for_file(rel, curated, mapping)
            text, part_token_fixes = apply_token_corrections(text, rel, rules, events)
            review = collect_review_candidates(text, rel)
            review_rows.extend(review)
            part_phrase_fixes = sum(int(event["count"]) for event in events[before_phrases:] if event["type"] == "phrase")
            phrase_fixes += part_phrase_fixes
            token_fixes += part_token_fixes
            item_review_count += len(review)
            part_records.append({"rel": rel, "part_number": part_number, "text": text})

        text = combined_markdown(output_rel, part_records) if item["combined"] else str(part_records[0]["text"])
        if item["combined"]:
            combined_count += 1

        out_path = args.out / output_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
        tmp_path.write_text(text, encoding="utf-8")
        tmp_path.replace(out_path)

        if item["combined"]:
            for src_path, _ in item["sources"]:
                stale_path = args.out / src_path.relative_to(args.src)
                if stale_path != out_path and stale_path.exists():
                    stale_path.unlink()
                    stale_removed += 1

        report.append(
            {
                "file": output_rel,
                "output": str(out_path),
                "source_files": ";".join(str(part["rel"]) for part in part_records),
                "combined": "yes" if item["combined"] else "no",
                "parts": len(part_records),
                "normalized": "yes" if normalized_changed else "no",
                "phrase_fixes": phrase_fixes,
                "token_fixes": token_fixes,
                "review_candidates": item_review_count,
                "status": "written",
            }
        )

    state_dir = args.out / "_state"
    write_csv(state_dir / "correction_report.csv", report, ["file", "output", "source_files", "combined", "parts", "normalized", "phrase_fixes", "token_fixes", "review_candidates", "status"])
    write_csv(state_dir / "correction_events.csv", events, ["file", "type", "wrong", "right", "count", "reason"])
    write_csv(state_dir / "review_candidates.csv", review_rows, ["file", "line", "token", "issue", "context"])

    summary = [
        "# Annavin OCR Correction Summary",
        "",
        f"- Generated: {now_iso()}",
        f"- Input files: {len(files)}",
        f"- Files written: {len(report)}",
        f"- Combined numbered outputs: {combined_count}",
        f"- Stale numbered output files removed: {stale_removed}",
        f"- Token correction rules loaded: {len(mapping)}",
        f"- Phrase/token events: {len(events)}",
        f"- Review candidates: {len(review_rows)}",
        "",
        "Correction edits are written to `ocr_text_corrected/`; raw OCR files are unchanged.",
    ]
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("\nFinished.", flush=True)
    print(f"Files written: {len(report)}", flush=True)
    print(f"Combined numbered outputs: {combined_count}", flush=True)
    print(f"Stale numbered output files removed: {stale_removed}", flush=True)
    print(f"Phrase/token events: {len(events)}", flush=True)
    print(f"Review candidates: {len(review_rows)}", flush=True)
    print(f"Summary: {state_dir / 'summary.md'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
