#!/usr/bin/env python3
"""Resumably translate the complete Annavin Markdown archive with OpenAI."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "organized_contents"
OUTPUT_DIR = SCRIPT_DIR / "translated_contents"
SOURCE_MAP = INPUT_DIR / "_merge_state" / "source_map.csv"
STATE_DIR = OUTPUT_DIR / "_translation_state"
MANIFEST = STATE_DIR / "translation_manifest.jsonl"
TERMS_FILE = STATE_DIR / "difficult_terms.csv"
NO_SOURCE_FILE = STATE_DIR / "needs_source_recovery.csv"
INCORRECT_SOURCES_FILE = STATE_DIR / "incorrect_sources.csv"
API_URL = "https://api.openai.com/v1/responses"
MODEL_PRICES_PER_MILLION = {
    "gpt-5.6-sol": (5.00, 30.00),
    "gpt-5.6-terra": (2.50, 15.00),
    "gpt-5.6-luna": (1.00, 6.00),
}
TERM_FIELDS = [
    "source_file", "direction", "source_term", "context",
    "proposed_translation", "term_type", "status", "notes",
]

SYSTEM_INSTRUCTIONS = """You are translating the collected works of C. N. Annadurai.
Produce a faithful, natural literary and historical translation. Preserve rhetoric,
repetition, humour, direct address, headings, dates, names, and political meaning.
Correct only evident OCR or typographical errors in the source. Never invent missing
text. If a reading is uncertain, retain it and explain the uncertainty in notes.
For Tamil sources translate to English; for English sources translate to Tamil.
Return corrected source text as well as the translation. Identify difficult terms,
idioms, historical terminology, wordplay, literary allusions, and OCR-sensitive
readings. Existing approved glossary choices are guidance only when context matches."""

SCHEMA = {
    "type": "object",
    "properties": {
        "tamil_title": {"type": "string"},
        "english_title": {"type": "string"},
        "corrected_source": {"type": "string"},
        "translation": {"type": "string"},
        "notes": {"type": "array", "items": {"type": "string"}},
        "difficult_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source_term": {"type": "string"},
                    "context": {"type": "string"},
                    "proposed_translation": {"type": "string"},
                    "term_type": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["candidate", "provisional", "approved", "context_dependent", "unresolved"],
                    },
                    "notes": {"type": "string"},
                },
                "required": ["source_term", "context", "proposed_translation", "term_type", "status", "notes"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["tamil_title", "english_title", "corrected_source", "translation", "notes", "difficult_terms"],
    "additionalProperties": False,
}

BOILERPLATE = (
    re.compile(r"^Source:\s*<.*>$", re.I),
    re.compile(r"^Source pages:$", re.I),
    re.compile(r"^- <https?://.*>$", re.I),
    re.compile(r"^அறிஞர் அண்ணாவின் .+$"),
    re.compile(r"^.+ பட்டியல்$"),
    re.compile(r"^முகப்பு \| எழுத்து \| பேச்சு \| புகைப்படம் \| ஓவியம் \| தொடர்பு$"),
    re.compile(r"^- Source image folder:.*$", re.I),
    re.compile(r"^- OCR language:.*$", re.I),
    re.compile(r"^- Tesseract page segmentation mode:.*$", re.I),
    re.compile(r"^- OCR cleanup:.*$", re.I),
    re.compile(r"^- Image:.*$", re.I),
)


def load_incorrect_sources(path: Path = INCORRECT_SOURCES_FILE) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["file"]: row.get("reason", "Source explicitly marked incorrect")
            for row in csv.DictReader(handle)
            if row.get("file")
        }


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    if not text.startswith("---\n"):
        return metadata, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return metadata, text
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, text[end + 5 :]


def clean_source(text: str) -> tuple[dict[str, str], str, str]:
    metadata, body = strip_frontmatter(text)
    title = ""
    kept: list[str] = []
    for raw in body.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not title and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if any(pattern.match(stripped) for pattern in BOILERPLATE):
            continue
        if stripped == "_No OCR text detected._":
            continue
        if stripped.startswith("## Image "):
            kept.append(re.sub(r"^## Image \d+:.*$", "---", stripped))
            continue
        kept.append(line)
    body = "\n".join(kept).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return metadata, title, body


def direction_for(text: str) -> str:
    tamil = len(re.findall(r"[\u0B80-\u0BFF]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "tamil_to_english" if tamil >= max(40, latin * 0.25) else "english_to_tamil"


def has_translatable_text(text: str) -> bool:
    tamil = len(re.findall(r"[\u0B80-\u0BFF]", text))
    words = len(re.findall(r"[A-Za-z]{2,}", text))
    return tamil >= 40 or words >= 20


def split_chunks(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            sentences = re.split(r"(?<=[.!?।])\s+|(?<=[.!?])\n", paragraph)
        else:
            sentences = [paragraph]
        for unit in sentences:
            addition = len(unit) + 2
            if current and size + addition > max_chars:
                chunks.append("\n\n".join(current).strip())
                current, size = [], 0
            if len(unit) > max_chars:
                for start in range(0, len(unit), max_chars):
                    piece = unit[start:start + max_chars]
                    if current:
                        chunks.append("\n\n".join(current).strip())
                        current, size = [], 0
                    chunks.append(piece)
            else:
                current.append(unit)
                size += addition
    if current:
        chunks.append("\n\n".join(current).strip())
    return [chunk for chunk in chunks if chunk]


def response_text(payload: dict[str, object]) -> str:
    for item in payload.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                return str(content.get("text") or "")
    raise ValueError("API response did not contain output text")


def call_openai(api_key: str, model: str, prompt: str, retries: int) -> tuple[dict[str, object], dict[str, object]]:
    request_data = {
        "model": model,
        "instructions": SYSTEM_INSTRUCTIONS,
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "translation_result",
                "strict": True,
                "schema": SCHEMA,
            }
        },
    }
    encoded = json.dumps(request_data, ensure_ascii=False).encode("utf-8")
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            API_URL,
            data=encoded,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=900) as response:
                raw = json.loads(response.read().decode("utf-8"))
            result = json.loads(response_text(raw))
            return result, dict(raw.get("usage") or {})
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            if attempt >= retries:
                raise RuntimeError(f"OpenAI request failed after {retries + 1} attempts: {exc}") from exc
            time.sleep(min(60, 2 ** attempt * 3))
    raise AssertionError("unreachable")


def load_glossary() -> str:
    if not TERMS_FILE.exists():
        return ""
    with TERMS_FILE.open(encoding="utf-8", newline="") as handle:
        approved = [row for row in csv.DictReader(handle) if row.get("status") == "approved"]
    lines = [
        f"- {row['source_term']} -> {row['proposed_translation']} ({row['notes']})"
        for row in approved[:200]
    ]
    return "\n".join(lines)


def build_prompt(rel: str, title: str, direction: str, chunk: str, index: int, total: int, glossary: str) -> str:
    target = "English" if direction == "tamil_to_english" else "Tamil"
    return f"""Translate this source into {target}.

File: {rel}
Original title: {title}
Direction: {direction}
Chunk: {index} of {total}

Approved glossary guidance (use only when context matches):
{glossary or '(none)'}

Requirements:
1. Correct only clear OCR/typographical errors in corrected_source.
2. Preserve paragraph structure and Markdown headings.
3. Do not summarize, omit, expand, censor, or modernize the argument.
4. Give both a Tamil title and an English title. For later chunks, repeat the same titles.
5. Put uncertainties in notes and difficult_terms; do not guess silently.

SOURCE TEXT:
{chunk}
"""


def source_rows() -> list[dict[str, str]]:
    with SOURCE_MAP.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def completed_hashes() -> set[str]:
    completed: set[str] = set()
    if not MANIFEST.exists():
        return completed
    with MANIFEST.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "done" and row.get("source_sha256"):
                completed.add(str(row["source_sha256"]))
    return completed


def usage_cost(model: str, usage: dict[str, object]) -> float:
    prices = MODEL_PRICES_PER_MILLION.get(model)
    if not prices:
        return 0.0
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    return (input_tokens * prices[0] + output_tokens * prices[1]) / 1_000_000


def previous_cost(model: str) -> float:
    if not MANIFEST.exists():
        return 0.0
    total = 0.0
    with MANIFEST.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("status") == "done" and record.get("model") == model:
                total += float(record.get("estimated_cost_usd") or usage_cost(model, record.get("usage") or {}))
    return total


def append_manifest(record: dict[str, object]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_terms() -> list[dict[str, str]]:
    if not TERMS_FILE.exists():
        return []
    with TERMS_FILE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def merge_terms(existing: list[dict[str, str]], rel: str, direction: str, results: list[dict[str, object]]) -> list[dict[str, str]]:
    keyed = {
        (row["source_file"], row["direction"], row["source_term"], row["context"]): row
        for row in existing
    }
    for result in results:
        for term in result.get("difficult_terms", []):
            if not isinstance(term, dict) or not term.get("source_term"):
                continue
            row = {
                "source_file": rel,
                "direction": direction,
                "source_term": str(term.get("source_term") or ""),
                "context": str(term.get("context") or ""),
                "proposed_translation": str(term.get("proposed_translation") or ""),
                "term_type": str(term.get("term_type") or "difficult_word"),
                "status": str(term.get("status") or "candidate"),
                "notes": str(term.get("notes") or ""),
            }
            keyed[(rel, direction, row["source_term"], row["context"])] = row
    return sorted(keyed.values(), key=lambda row: (row["status"], row["source_term"].casefold(), row["source_file"]))


def write_terms(rows: list[dict[str, str]]) -> None:
    with TERMS_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TERM_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(rel: str, metadata: dict[str, str], direction: str, results: list[dict[str, object]]) -> str:
    first = results[0]
    tamil_title = str(first["tamil_title"]).strip()
    english_title = str(first["english_title"]).strip()
    source_url = metadata.get("source_url") or metadata.get("final_url") or ""
    corrected_heading = "Corrected Tamil" if direction == "tamil_to_english" else "Corrected English"
    translation_heading = "English Translation" if direction == "tamil_to_english" else "Tamil Translation"
    corrected = "\n\n".join(str(result["corrected_source"]).strip() for result in results)
    translated = "\n\n".join(str(result["translation"]).strip() for result in results)
    notes = [str(note).strip() for result in results for note in result.get("notes", []) if str(note).strip()]
    lines = [
        f"# {english_title if direction == 'tamil_to_english' else tamil_title}", "",
        f"**Tamil title:** {tamil_title}  ",
        f"**English title:** {english_title}  ",
        f"**Translation direction:** {direction.replace('_', ' ')}  ",
        f"**Source file:** `{rel}`  ",
    ]
    if source_url:
        lines.append(f"**Source:** <{source_url}>  ")
    lines.extend(["", f"## {corrected_heading}", "", corrected, "", f"## {translation_heading}", "", translated])
    if notes:
        lines.extend(["", "## Translator's Notes", ""])
        lines.extend(f"- {note}" for note in dict.fromkeys(notes))
    return "\n".join(lines).rstrip() + "\n"


def write_recovery(rows: list[dict[str, str]]) -> None:
    merged: dict[str, dict[str, str]] = {}
    if NO_SOURCE_FILE.exists():
        with NO_SOURCE_FILE.open(encoding="utf-8-sig", newline="") as handle:
            merged.update(
                (row["file"], row)
                for row in csv.DictReader(handle)
                if row.get("file")
            )
    merged.update((row["file"], row) for row in rows if row.get("file"))
    with NO_SOURCE_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "reason", "source_path"])
        writer.writeheader()
        writer.writerows(merged[key] for key in sorted(merged, key=str.casefold))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--limit", type=int, default=0, help="Maximum files to process; 0 means all.")
    parser.add_argument("--file", action="append", default=[], help="Process one relative path; repeatable.")
    parser.add_argument("--max-chars", type=int, default=24000)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--max-cost-usd",
        type=float,
        default=0.0,
        help="Stop before starting another file after recorded model cost reaches this amount.",
    )
    args = parser.parse_args()

    if not SOURCE_MAP.exists():
        raise SystemExit(f"Missing source map: {SOURCE_MAP}")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not args.dry_run and not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Set it in the shell before running translations.")
    if args.max_cost_usd and args.model not in MODEL_PRICES_PER_MILLION:
        raise SystemExit(f"No local price information for {args.model}; omit --max-cost-usd or add its prices.")

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    selected = set(args.file)
    rows = [row for row in source_rows() if not selected or row["file"] in selected]
    completed = completed_hashes()
    glossary = load_glossary()
    terms = read_terms()
    recovery: list[dict[str, str]] = []
    incorrect_sources = load_incorrect_sources()
    counts: Counter[str] = Counter()
    processed = 0
    estimated_cost = previous_cost(args.model)

    for position, row in enumerate(rows, 1):
        if args.max_cost_usd and estimated_cost >= args.max_cost_usd:
            print(f"Cost guard reached: ${estimated_cost:.2f} / ${args.max_cost_usd:.2f}", flush=True)
            counts["cost_guard_stopped"] += 1
            break
        rel = row["file"]
        if rel in incorrect_sources:
            print(f"skip incorrect source: {rel}", flush=True)
            counts["incorrect_source"] += 1
            continue
        source = Path(row.get("chosen_path") or INPUT_DIR / rel)
        output = OUTPUT_DIR / rel
        raw = source.read_text(encoding="utf-8", errors="replace")
        source_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if not args.overwrite and output.exists() and output.stat().st_size > 0:
            counts["existing"] += 1
            continue
        if not args.overwrite and source_hash in completed:
            counts["manifest_done"] += 1
            continue
        metadata, title, body = clean_source(raw)
        if not has_translatable_text(body):
            recovery.append({"file": rel, "reason": "No usable source body", "source_path": str(source)})
            counts["needs_source_recovery"] += 1
            continue
        direction = direction_for(body)
        chunks = split_chunks(body, args.max_chars)
        print(f"[{position}/{len(rows)}] {rel} ({direction}, {len(chunks)} chunk(s))", flush=True)
        if args.dry_run:
            counts[f"would_{direction}"] += 1
            processed += 1
            if args.limit and processed >= args.limit:
                break
            continue

        results: list[dict[str, object]] = []
        usage_totals: Counter[str] = Counter()
        try:
            for chunk_index, chunk in enumerate(chunks, 1):
                prompt = build_prompt(rel, title, direction, chunk, chunk_index, len(chunks), glossary)
                result, usage = call_openai(api_key, args.model, prompt, args.retries)
                results.append(result)
                for key, value in usage.items():
                    if isinstance(value, int):
                        usage_totals[key] += value
                if args.delay:
                    time.sleep(args.delay)
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_suffix(output.suffix + ".tmp")
            temporary.write_text(render_markdown(rel, metadata, direction, results), encoding="utf-8")
            temporary.replace(output)
            terms = merge_terms(terms, rel, direction, results)
            write_terms(terms)
            file_cost = usage_cost(args.model, dict(usage_totals))
            estimated_cost += file_cost
            append_manifest({
                "file": rel, "status": "done", "direction": direction,
                "model": args.model, "chunks": len(chunks), "source_sha256": source_hash,
                "usage": dict(usage_totals), "output_path": str(output),
                "estimated_cost_usd": round(file_cost, 6),
            })
            counts["done"] += 1
        except Exception as exc:
            append_manifest({
                "file": rel, "status": "failed", "direction": direction,
                "model": args.model, "source_sha256": source_hash,
                "error": f"{type(exc).__name__}: {exc}",
            })
            counts["failed"] += 1
            print(f"failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        processed += 1
        if args.limit and processed >= args.limit:
            break

    if not args.dry_run:
        write_recovery(recovery)
    print("\nSummary", flush=True)
    for key, value in sorted(counts.items()):
        print(f"- {key}: {value}", flush=True)
    print(f"- manifest: {MANIFEST}", flush=True)
    print(f"- difficult terms: {TERMS_FILE}", flush=True)
    print(f"- source recovery: {NO_SOURCE_FILE}", flush=True)
    if not args.dry_run:
        print(f"- recorded estimated cost for {args.model}: ${estimated_cost:.2f}", flush=True)
    return 0 if not counts["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
