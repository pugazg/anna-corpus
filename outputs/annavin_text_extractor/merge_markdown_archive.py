#!/usr/bin/env python3
"""
Merge HTML-extracted Markdown and OCR-corrected Markdown into one archive.

The merged folder keeps the same website-style paths used by md_pages/. HTML
extraction is used as the base. OCR-corrected files replace matching HTML files,
because those pages were scanned/no-text pages in the HTML extractor.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import json
import re
import shutil
import urllib.parse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_HTML_DIR = SCRIPT_DIR / "md_pages"
DEFAULT_OCR_DIR = SCRIPT_DIR / "ocr_text_corrected"
DEFAULT_OUT_DIR = SCRIPT_DIR / "merged_md_pages"
DEFAULT_EXTRACTION_MANIFEST = DEFAULT_HTML_DIR / "_extract_state" / "manifest.jsonl"


SECTION_NAMES = {
    "Kurunavalgal": "குறுநாவல்கள்",
    "english": "English",
    "kadithangal": "கடிதங்கள்",
    "katturaigal": "கட்டுரைகள்",
    "kavithaigal": "கவிதைகள்",
    "nadagangal": "நாடகங்கள்",
    "navalgal": "நாவல்கள்",
    "oviyam": "ஓவியம்",
    "paettigal": "பேட்டிகள்",
    "photos": "புகைப்படம்",
    "sirukathaigal": "சிறுகதைகள்",
    "sorpozhivugal": "சொற்பொழிவுகள்",
}

ROOT_URL_FOLDERS = (
    (re.compile(r"^annavin_english_", re.I), "english"),
    (re.compile(r"^annavin_kadithangal(?:[_\.]|$)", re.I), "kadithangal"),
    (re.compile(r"^annavin_katturaigal(?:[_\.]|$)", re.I), "katturaigal"),
    (re.compile(r"^annavin_sirukathaigal(?:[_\.]|$)", re.I), "sirukathaigal"),
    (re.compile(r"^annavin_navalgal(?:[_\.]|$)", re.I), "navalgal"),
    (re.compile(r"^annavin_kurunavalgal(?:[_\.]|$)", re.I), "Kurunavalgal"),
    (re.compile(r"^annavin_kavithaigal(?:[_\.]|$)", re.I), "kavithaigal"),
    (re.compile(r"^annavin_nadagangal(?:[_\.]|$)", re.I), "nadagangal"),
    (re.compile(r"^(?:annavin_oviyam_|oaviyam(?:\.|$))", re.I), "oviyam"),
    (re.compile(r"^(?:annavin_pugaipadangal|photos(?:\.|$)|parimalam_photos)", re.I), "photos"),
    (re.compile(r"^speech", re.I), "sorpozhivugal"),
)

KNOWN_URL_CORRECTIONS = {
    "http://www.annavinpadaippugal.info/annavin_kurunavalgal.htm../annavin_kavithaigal.htm":
        "http://www.annavinpadaippugal.info/annavin_kavithaigal.htm",
    "https://www.annavinpadaippugal.info/annavin_kurunavalgal.htm../annavin_kavithaigal.htm":
        "https://www.annavinpadaippugal.info/annavin_kavithaigal.htm",
    "http://www.annavinpadaippugal.info/kadithangal/ivanae_tamil_maravan4.htm":
        "http://www.annavinpadaippugal.info/kadithangal/ivanae_tamil_maravan_4.htm",
    "https://www.annavinpadaippugal.info/kadithangal/ivanae_tamil_maravan4.htm":
        "https://www.annavinpadaippugal.info/kadithangal/ivanae_tamil_maravan_4.htm",
    "http://www.annavinpadaippugal.info/katturaigal/Diary_of_a_Democrat_2.htm":
        "http://www.annavinpadaippugal.info/katturaigal/diary_of_a_democrat_2.htm",
    "https://www.annavinpadaippugal.info/katturaigal/Diary_of_a_Democrat_2.htm":
        "https://www.annavinpadaippugal.info/katturaigal/diary_of_a_democrat_2.htm",
    "http://www.annavinpadaippugal.info/katturaigal/naatin_nayagargal.htm":
        "http://www.annavinpadaippugal.info/katturaigal/naatin_nayagargal_1.htm",
    "https://www.annavinpadaippugal.info/katturaigal/naatin_nayagargal.htm":
        "https://www.annavinpadaippugal.info/katturaigal/naatin_nayagargal_1.htm",
    "http://www.annavinpadaippugal.info/katturaigal/periyaperiyapuranaputhayal_5.htm":
        "http://www.annavinpadaippugal.info/katturaigal/periyapuranaputhayal_5.htm",
    "https://www.annavinpadaippugal.info/katturaigal/periyaperiyapuranaputhayal_5.htm":
        "https://www.annavinpadaippugal.info/katturaigal/periyapuranaputhayal_5.htm",
    "http://www.annavinpadaippugal.info/sorpozhivugal/150767_2.htm":
        "http://www.annavinpadaippugal.info/sorpozhivugal/150767_2.html",
    "https://www.annavinpadaippugal.info/sorpozhivugal/150767_2.htm":
        "https://www.annavinpadaippugal.info/sorpozhivugal/150767_2.html",
    "http://www.annavinpadaippugal.info/sorpozhivugal/dravidar_kazhaga_thani_2.htm":
        "http://www.annavinpadaippugal.info/sorpozhivugal/dravidar_kazhaga_thani_2.html",
    "https://www.annavinpadaippugal.info/sorpozhivugal/dravidar_kazhaga_thani_2.htm":
        "https://www.annavinpadaippugal.info/sorpozhivugal/dravidar_kazhaga_thani_2.html",
    "http://www.annavinpadaippugal.info/sorpozhivugal/sudhanthira_kaiyelu_1.htm":
        "http://www.annavinpadaippugal.info/sorpozhivugal/sudhanthira_kaiyelu_1.html",
    "https://www.annavinpadaippugal.info/sorpozhivugal/sudhanthira_kaiyelu_1.htm":
        "https://www.annavinpadaippugal.info/sorpozhivugal/sudhanthira_kaiyelu_1.html",
}

KNOWN_OUTPUT_CORRECTIONS = {
    "annavin_kavithaigal.htm": "kavithaigal/annavin_kavithaigal.md",
    "ivanae_tamil_maravan4.htm": "kadithangal/ivanae_tamil_maravan.md",
    "Diary_of_a_Democrat_2.htm": "katturaigal/Diary_of_a_Democrat.md",
    "naatin_nayagargal.htm": "katturaigal/naatin_nayagargal.md",
    "periyaperiyapuranaputhayal_5.htm": "katturaigal/periyapuranaputhayal.md",
    "150767_2.htm": "sorpozhivugal/150767.md",
    "dravidar_kazhaga_thani_2.htm": "sorpozhivugal/dravidar_kazhaga_thani.md",
    "sudhanthira_kaiyelu_1.htm": "sorpozhivugal/sudhanthira_kaiyelu.md",
}

SUCCESSFUL_URL_OUTPUT_OVERRIDES = {
    "http://www.annavinpadaippugal.info/katturaigal/diary_of_a_democrat_2.htm":
        "katturaigal/Diary_of_a_Democrat.md",
    "https://www.annavinpadaippugal.info/katturaigal/diary_of_a_democrat_2.htm":
        "katturaigal/Diary_of_a_Democrat.md",
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def is_state_path(path: Path) -> bool:
    return any(part.startswith("_") for part in path.parts)


def list_markdown(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    if not root.exists():
        return files
    for path in root.rglob("*.md"):
        rel_path = path.relative_to(root)
        if is_state_path(rel_path):
            continue
        if path.stem.endswith(" 2") and path.with_name(path.stem[:-2] + path.suffix).exists():
            continue
        files[rel_path.as_posix()] = path
    return files


def file_size(path: Path) -> int:
    return path.stat().st_size


def place_file_atomic(src: Path, dst: Path, file_mode: str) -> int:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    if file_mode == "symlink":
        relative_target = os.path.relpath(src, dst.parent)
        tmp.symlink_to(relative_target)
    elif file_mode == "hardlink":
        try:
            os.link(src, tmp)
        except OSError:
            shutil.copyfile(src, tmp)
    else:
        shutil.copyfile(src, tmp)
    tmp.replace(dst)
    return file_size(src)


def remove_temp_files(out_dir: Path) -> int:
    if not out_dir.exists():
        return 0
    removed = 0
    for path in out_dir.rglob("*.tmp"):
        if path.is_file():
            path.unlink()
            removed += 1
    return removed


def remove_duplicate_output_links(out_dir: Path) -> int:
    if not out_dir.exists():
        return 0
    removed = 0
    for path in out_dir.rglob("* 2.md"):
        canonical = path.with_name(path.stem[:-2] + path.suffix)
        if path.is_symlink() and (canonical.exists() or not path.exists()):
            path.unlink()
            removed += 1
    return removed


def load_previous_outputs(out_dir: Path) -> set[str]:
    manifest_path = out_dir / "_merge_state" / "source_map.csv"
    if not manifest_path.exists():
        return set()
    outputs: set[str] = set()
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rel = row.get("file")
            if rel:
                outputs.add(rel)
    return outputs


def remove_stale_previous_outputs(out_dir: Path, current_outputs: set[str]) -> int:
    removed = 0
    previous = load_previous_outputs(out_dir)
    for rel in sorted(previous - current_outputs):
        path = out_dir / rel
        if path.exists() and path.is_file():
            path.unlink()
            removed += 1
    return removed


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def existing_combined_output(rel: str, final_keys: set[str]) -> str | None:
    candidate = Path(rel)
    stem = candidate.stem
    while True:
        match = re.match(r"^(.+)_\d+$", stem)
        if not match:
            return None
        stem = match.group(1)
        combined = candidate.with_name(stem + candidate.suffix).as_posix()
        if combined in final_keys:
            return combined


def successful_source_pages(manifest_path: Path, html_dir: Path) -> dict[str, dict[str, str]]:
    """Return the final Markdown mapping for every successfully fetched URL."""
    pages: dict[str, dict[str, str]] = {}
    if not manifest_path.exists():
        return pages

    with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("status") not in {"done", "partial"}:
                continue
            output_value = str(record.get("output_path") or "")
            if not output_value:
                continue
            try:
                output_rel = Path(output_value).resolve().relative_to(html_dir).as_posix()
            except (OSError, ValueError):
                continue

            record_pages = record.get("pages")
            if isinstance(record_pages, list) and record_pages:
                for page in record_pages:
                    if not isinstance(page, dict) or not page.get("url"):
                        continue
                    url = str(page["url"])
                    pages[url] = {
                        "url": url,
                        "http_status": str(page.get("http_status") or ""),
                        "markdown_file": output_rel,
                        "combined": "yes" if record.get("combined") else "no",
                    }
            else:
                urls = record.get("urls") or [record.get("url")]
                if isinstance(urls, list):
                    for url_value in urls:
                        if not url_value:
                            continue
                        url = str(url_value)
                        pages[url] = {
                            "url": url,
                            "http_status": str(record.get("http_status") or ""),
                            "markdown_file": output_rel,
                            "combined": "yes" if record.get("combined") else "no",
                        }
    return pages


def write_coverage_audit(
    out_dir: Path,
    manifest_path: Path,
    html_dir: Path,
    final_keys: set[str],
) -> tuple[int, int]:
    successful = successful_source_pages(manifest_path, html_dir)
    rows: list[dict[str, object]] = []
    missing: list[dict[str, object]] = []
    for url, page in sorted(successful.items(), key=lambda item: item[0].lower()):
        rel = SUCCESSFUL_URL_OUTPUT_OVERRIDES.get(url, page["markdown_file"])
        if rel != page["markdown_file"]:
            page = {**page, "markdown_file": rel, "combined": "yes"}
        if rel not in final_keys:
            combined_rel = existing_combined_output(rel, final_keys)
            if combined_rel:
                rel = combined_rel
                page = {**page, "markdown_file": rel, "combined": "yes"}
        if rel not in final_keys:
            same_name = sorted(key for key in final_keys if Path(key).name == Path(rel).name)
            if len(same_name) == 1:
                rel = same_name[0]
                page = {**page, "markdown_file": rel}
        output = out_dir / rel
        exists = rel in final_keys and output.exists() and output.is_file()
        nonempty = exists and output.stat().st_size > 0
        status = "covered" if nonempty else "missing"
        row = {**page, "coverage": status, "output_path": str(output)}
        rows.append(row)
        if status == "missing":
            missing.append(row)

    state_dir = out_dir / "_merge_state"
    write_csv(
        state_dir / "successful_link_coverage.csv",
        rows,
        ["url", "http_status", "markdown_file", "combined", "coverage", "output_path"],
    )
    write_csv(
        state_dir / "missing_successful_links.csv",
        missing,
        ["url", "http_status", "markdown_file", "combined", "coverage", "output_path"],
    )
    lines = [
        "# Successful Link Coverage",
        "",
        f"- Generated: {now_iso()}",
        f"- Successfully fetched source links: {len(rows)}",
        f"- Covered by a non-empty Markdown file: {len(rows) - len(missing)}",
        f"- Missing Markdown files: {len(missing)}",
        "- Numbered source pages may share one combined Markdown file.",
        "",
    ]
    if missing:
        lines.extend(["## Missing Links", ""])
        lines.extend(f"- <{row['url']}> -> `{row['markdown_file']}`" for row in missing)
    else:
        lines.append("All successfully fetched source links are covered.")
    (state_dir / "successful_link_coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(rows), len(missing)


def write_discovered_link_audit(
    out_dir: Path,
    manifest_path: Path,
    html_dir: Path,
    final_keys: set[str],
) -> tuple[int, int, int]:
    """Audit every internal HTML URL in the crawler's discovered-link file."""
    links_path = SCRIPT_DIR.parent / "annavinpadaippugal_links.md"
    text = links_path.read_text(encoding="utf-8", errors="replace")
    links = list(dict.fromkeys(re.findall(r"<(https?://[^>\s]+)>", text)))
    start_match = re.search(r"^- Start URL:\s*(https?://\S+)", text, re.MULTILINE)
    if start_match and start_match.group(1) not in links:
        links.insert(0, start_match.group(1))
    selected = []
    for url in links:
        parsed = urllib.parse.urlsplit(url)
        path = parsed.path.lower()
        if parsed.netloc.lower() != "www.annavinpadaippugal.info":
            continue
        if path not in {"", "/"} and not path.endswith((".htm", ".html", "/")):
            continue
        selected.append(url)

    def numbered_info(url: str) -> tuple[str, int] | None:
        parsed = urllib.parse.urlsplit(url)
        if parsed.query:
            return None
        parts = [part for part in parsed.path.split("/") if part]
        if not parts or re.match(r"^.+_[0-9]{4}_[0-9]{2}\.html?$", parts[-1], re.I):
            return None
        match = re.match(r"^(.+)_part([0-9]+)(\.html?)$", parts[-1], re.I)
        if not match:
            match = re.match(r"^(.+)_([0-9]+)(\.html?)$", parts[-1], re.I)
        if not match:
            return None
        stem, number, extension = match.groups()
        parts[-1] = f"{stem}{extension}"
        base = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/" + "/".join(parts), "", ""))
        return base, int(number)

    groups: dict[str, list[str]] = {}
    for url in selected:
        info = numbered_info(url)
        if info:
            groups.setdefault(info[0], []).append(url)
    selected_set = set(selected)

    def output_rel(url: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        parts = [urllib.parse.unquote(part).strip() for part in parsed.path.split("/") if part] or ["index"]
        filename = parts[-1]
        filename = re.sub(r"\.html?$", ".md", filename, flags=re.I)
        if not filename.lower().endswith(".md"):
            filename += ".md"
        parts[-1] = filename
        if len(parts) == 1:
            for pattern, folder in ROOT_URL_FOLDERS:
                if pattern.match(parts[0]):
                    parts.insert(0, folder)
                    break
        return Path(*parts).as_posix()

    page_state: dict[str, str] = {}
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for page in record.get("pages") or []:
                    if isinstance(page, dict) and page.get("url"):
                        page_state[str(page["url"])] = "success"
                for failure in record.get("failures") or []:
                    if isinstance(failure, dict) and failure.get("url"):
                        page_state[str(failure["url"])] = "failed"
                if record.get("status") == "failed":
                    for url in record.get("urls") or []:
                        page_state[str(url)] = "failed"

    rows: list[dict[str, object]] = []
    missing: list[dict[str, object]] = []
    failed: list[dict[str, object]] = []
    for source_url in selected:
        mapped_url = KNOWN_URL_CORRECTIONS.get(source_url, source_url)
        info = numbered_info(mapped_url)
        combined = bool(info and (len(groups.get(info[0], [])) > 1 or info[0] in selected_set))
        if source_url in SUCCESSFUL_URL_OUTPUT_OVERRIDES:
            expected = SUCCESSFUL_URL_OUTPUT_OVERRIDES[source_url]
            combined = True
        elif source_url in KNOWN_URL_CORRECTIONS:
            expected = KNOWN_OUTPUT_CORRECTIONS[Path(urllib.parse.urlsplit(source_url).path).name]
            combined = True
        else:
            expected = output_rel(info[0] if combined and info else mapped_url)
        if expected not in final_keys:
            combined_rel = existing_combined_output(expected, final_keys)
            if combined_rel:
                expected = combined_rel
                combined = True
        if expected not in final_keys:
            same_name = sorted(key for key in final_keys if Path(key).name == Path(expected).name)
            if len(same_name) == 1:
                expected = same_name[0]
        output = out_dir / expected
        available = expected in final_keys and output.exists() and output.is_file() and output.stat().st_size > 0
        if source_url in KNOWN_URL_CORRECTIONS and available:
            coverage = "covered_via_corrected_url"
        elif page_state.get(source_url) == "failed":
            coverage = "known_failed_source"
        elif available:
            coverage = "covered"
        else:
            coverage = "missing"
        row = {
            "url": source_url,
            "markdown_file": expected,
            "combined": "yes" if combined else "no",
            "manifest_state": page_state.get(source_url, "not_recorded"),
            "coverage": coverage,
            "output_path": str(output),
        }
        rows.append(row)
        if coverage == "missing":
            missing.append(row)
        elif coverage == "known_failed_source":
            failed.append(row)

    state_dir = out_dir / "_merge_state"
    fields = ["url", "markdown_file", "combined", "manifest_state", "coverage", "output_path"]
    write_csv(state_dir / "all_discovered_link_coverage.csv", rows, fields)
    write_csv(state_dir / "missing_discovered_links.csv", missing, fields)
    write_csv(state_dir / "known_failed_discovered_links.csv", failed, fields)
    covered_count = len(rows) - len(missing) - len(failed)
    lines = [
        "# Complete Website Link Coverage",
        "",
        f"- Generated: {now_iso()}",
        f"- Internal HTML links discovered: {len(rows)}",
        f"- Covered by a non-empty Markdown file: {covered_count}",
        f"- Known failed source links: {len(failed)}",
        f"- Missing Markdown coverage: {len(missing)}",
        "- Numbered source pages may share one combined Markdown file.",
        "",
    ]
    if missing:
        lines.extend(["## Missing Coverage", ""])
        lines.extend(f"- <{row['url']}> -> `{row['markdown_file']}`" for row in missing)
    else:
        lines.append("Every discovered link except known source failures is covered.")
    (state_dir / "complete_website_coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(rows), len(failed), len(missing)


def section_for_rel(rel: str) -> str:
    parts = Path(rel).parts
    if len(parts) > 1:
        return parts[0]
    return "root"


def write_index(out_dir: Path, source_rows: list[dict[str, object]]) -> None:
    by_section: dict[str, list[str]] = {}
    for row in source_rows:
        rel = str(row["file"])
        by_section.setdefault(section_for_rel(rel), []).append(rel)

    lines = [
        "# Annavin Padaippugal - Merged Markdown Archive",
        "",
        f"- Generated: {now_iso()}",
        f"- Total Markdown files: {len(source_rows)}",
        "- Source priority: OCR-corrected Markdown replaces HTML-extracted Markdown when both exist.",
        "",
        "## Sections",
        "",
    ]
    for section in sorted(by_section, key=lambda item: (item != "root", item.lower())):
        display = SECTION_NAMES.get(section, section)
        lines.append(f"- [{display}](#{section.lower().replace('_', '-')}) - {len(by_section[section])} files")

    for section in sorted(by_section, key=lambda item: (item != "root", item.lower())):
        display = SECTION_NAMES.get(section, section)
        lines.extend(["", f"## {display}", ""])
        for rel in sorted(by_section[section], key=str.lower):
            name = Path(rel).stem
            lines.append(f"- [{name}]({rel})")

    (out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Merge md_pages/ and ocr_text_corrected/ into one Markdown archive.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--html-dir", type=Path, default=DEFAULT_HTML_DIR, help="HTML-extracted Markdown folder.")
    parser.add_argument("--ocr-dir", type=Path, default=DEFAULT_OCR_DIR, help="OCR-corrected Markdown folder.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Merged Markdown output folder.")
    parser.add_argument("--extraction-manifest", type=Path, default=DEFAULT_EXTRACTION_MANIFEST, help="HTML extraction manifest used to audit successful source links.")
    parser.add_argument("--prefer-html", action="store_true", help="Do not replace overlapping HTML files with OCR files.")
    parser.add_argument("--file-mode", choices=["symlink", "hardlink", "copy"], default="symlink", help="How merged Markdown files are placed in the output folder.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.html_dir = args.html_dir.resolve()
    args.ocr_dir = args.ocr_dir.resolve()
    args.out_dir = args.out_dir.resolve()
    args.extraction_manifest = args.extraction_manifest.resolve()

    html_files = list_markdown(args.html_dir)
    ocr_files = list_markdown(args.ocr_dir)
    redundant_html_parts = []
    for rel in list(html_files):
        path = Path(rel)
        match = re.match(r"^(.+)_\d+$", path.stem)
        if not match:
            continue
        combined_rel = path.with_name(match.group(1) + path.suffix).as_posix()
        if combined_rel in ocr_files:
            redundant_html_parts.append(rel)
            del html_files[rel]
    overlaps = set(html_files) & set(ocr_files)
    ocr_only = set(ocr_files) - set(html_files)

    temp_removed = remove_temp_files(args.out_dir)
    duplicate_links_removed = remove_duplicate_output_links(args.out_dir)
    final_keys = set(html_files) | set(ocr_files)
    stale_removed = remove_stale_previous_outputs(args.out_dir, final_keys)

    source_rows: list[dict[str, object]] = []
    overlap_rows: list[dict[str, object]] = []
    section_counts: dict[str, dict[str, int]] = {}

    print(f"HTML Markdown folder: {args.html_dir}", flush=True)
    print(f"OCR Markdown folder: {args.ocr_dir}", flush=True)
    print(f"Merged output folder: {args.out_dir}", flush=True)
    print(f"HTML files: {len(html_files)}", flush=True)
    print(f"OCR files: {len(ocr_files)}", flush=True)
    print(f"Overlaps: {len(overlaps)}", flush=True)
    print(f"OCR-only files: {len(ocr_only)}", flush=True)
    print(f"Redundant numbered HTML parts excluded: {len(redundant_html_parts)}", flush=True)
    print(f"File mode: {args.file_mode}", flush=True)

    for rel in sorted(final_keys, key=str.lower):
        has_html = rel in html_files
        has_ocr = rel in ocr_files
        if has_html and (not has_ocr or args.prefer_html):
            source = "html"
            src = html_files[rel]
        elif has_ocr and has_html:
            source = "ocr_replaces_html"
            src = ocr_files[rel]
            overlap_rows.append(
                {
                    "file": rel,
                    "chosen": "ocr",
                    "html_bytes": file_size(html_files[rel]),
                    "ocr_bytes": file_size(ocr_files[rel]),
                    "html_path": str(html_files[rel]),
                    "ocr_path": str(ocr_files[rel]),
                }
            )
        else:
            source = "ocr_only"
            src = ocr_files[rel]

        dst = args.out_dir / rel
        byte_count = place_file_atomic(src, dst, args.file_mode)
        section = section_for_rel(rel)
        section_counts.setdefault(section, {"total": 0, "html": 0, "ocr_replaces_html": 0, "ocr_only": 0})
        section_counts[section]["total"] += 1
        section_counts[section][source] += 1
        source_rows.append(
            {
                "file": rel,
                "section": section,
                "source": source,
                "html_exists": "yes" if has_html else "no",
                "ocr_exists": "yes" if has_ocr else "no",
                "chosen_path": str(src),
                "output_path": str(dst),
                "bytes": byte_count,
            }
        )

    state_dir = args.out_dir / "_merge_state"
    write_csv(
        state_dir / "source_map.csv",
        source_rows,
        ["file", "section", "source", "html_exists", "ocr_exists", "chosen_path", "output_path", "bytes"],
    )
    write_csv(
        state_dir / "ocr_replacements.csv",
        overlap_rows,
        ["file", "chosen", "html_bytes", "ocr_bytes", "html_path", "ocr_path"],
    )
    write_csv(
        state_dir / "section_counts.csv",
        [
            {"section": section, **counts}
            for section, counts in sorted(section_counts.items(), key=lambda item: item[0].lower())
        ],
        ["section", "total", "html", "ocr_replaces_html", "ocr_only"],
    )

    summary = [
        "# Merged Markdown Archive Summary",
        "",
        f"- Generated: {now_iso()}",
        f"- HTML input files: {len(html_files)}",
        f"- OCR input files: {len(ocr_files)}",
        f"- Overlapping files: {len(overlaps)}",
        f"- OCR-only files: {len(ocr_only)}",
        f"- Final Markdown files: {len(source_rows)}",
        f"- File mode: {args.file_mode}",
        f"- Temporary files removed before merge: {temp_removed}",
        f"- Stale duplicate links removed: {duplicate_links_removed}",
        f"- Stale previously managed files removed: {stale_removed}",
        f"- Source priority: {'HTML preferred over OCR' if args.prefer_html else 'OCR replaces HTML on overlap'}",
        "",
        "Reports:",
        "- `source_map.csv`",
        "- `ocr_replacements.csv`",
        "- `section_counts.csv`",
    ]
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    write_index(args.out_dir, source_rows)
    successful_links, missing_successful = write_coverage_audit(
        args.out_dir,
        args.extraction_manifest,
        args.html_dir,
        final_keys,
    )
    discovered_links, known_failed_links, missing_discovered = write_discovered_link_audit(
        args.out_dir,
        args.extraction_manifest,
        args.html_dir,
        final_keys,
    )

    print("\nFinished.", flush=True)
    print(f"Final Markdown files: {len(source_rows)}", flush=True)
    print(f"OCR replacements: {len(overlap_rows)}", flush=True)
    print(f"Successful source links covered: {successful_links - missing_successful}/{successful_links}", flush=True)
    print(f"Discovered website links: {discovered_links} ({known_failed_links} known failed, {missing_discovered} missing)", flush=True)
    print(f"Summary: {state_dir / 'summary.md'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
