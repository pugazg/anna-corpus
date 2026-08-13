#!/usr/bin/env python3
"""
Extract text from annavinpadaippugal.info HTML links into Markdown files.

The tool is dependency-free and resumable. Normal reruns skip completed files,
known failed links, and partial files unless you ask to retry them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LINKS = SCRIPT_DIR.parent / "annavinpadaippugal_links.md"
DEFAULT_OUT_DIR = SCRIPT_DIR / "md_pages"
DEFAULT_DOMAIN = "www.annavinpadaippugal.info"
USER_AGENT = "annavin-text-extractor/1.1"


ROOT_FILENAME_FOLDERS = (
    (re.compile(r"^annavin_english_", re.IGNORECASE), ("english",)),
    (re.compile(r"^annavin_kadithangal(?:[_\.]|$)", re.IGNORECASE), ("kadithangal",)),
    (re.compile(r"^annavin_katturaigal(?:[_\.]|$)", re.IGNORECASE), ("katturaigal",)),
    (re.compile(r"^annavin_sirukathaigal(?:[_\.]|$)", re.IGNORECASE), ("sirukathaigal",)),
    (re.compile(r"^annavin_navalgal(?:[_\.]|$)", re.IGNORECASE), ("navalgal",)),
    (re.compile(r"^annavin_kurunavalgal(?:[_\.]|$)", re.IGNORECASE), ("Kurunavalgal",)),
    (re.compile(r"^annavin_kavithaigal(?:[_\.]|$)", re.IGNORECASE), ("kavithaigal",)),
    (re.compile(r"^annavin_nadagangal(?:[_\.]|$)", re.IGNORECASE), ("nadagangal",)),
    (re.compile(r"^(?:annavin_oviyam_|oaviyam(?:\.|$))", re.IGNORECASE), ("oviyam",)),
    (re.compile(r"^(?:annavin_pugaipadangal|photos(?:\.|$)|parimalam_photos)", re.IGNORECASE), ("photos",)),
    (re.compile(r"^speech", re.IGNORECASE), ("sorpozhivugal",)),
)


class ExtractedTextParser(HTMLParser):
    BLOCK_TAGS = {
        "address", "article", "aside", "blockquote", "br", "caption", "center",
        "dd", "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer",
        "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "li",
        "main", "nav", "ol", "p", "pre", "section", "table", "tbody", "td",
        "tfoot", "th", "thead", "tr", "ul",
    }
    SKIP_TAGS = {"script", "style", "noscript", "object", "embed"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.skip_depth = 0
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag == "title":
            self.in_title = True
            return
        if self.skip_depth:
            return
        if tag == "li":
            self._break()
            self._add_text("- ")
        elif tag in self.BLOCK_TAGS:
            self._break()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag == "title":
            self.in_title = False
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self._break()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        clean = html.unescape(data).replace("\xa0", " ")
        clean = re.sub(r"\s+", " ", clean).strip()
        if not clean:
            return
        if self.in_title:
            self.title_parts.append(clean)
        else:
            self._add_text(clean)

    def _add_text(self, text: str) -> None:
        if (
            self.parts
            and not self.parts[-1].endswith((" ", "\n"))
            and not text.startswith((".", ",", ";", ":", "?", "!", ")", "]", "}", "”", "’"))
        ):
            self.parts.append(" ")
        self.parts.append(text)

    def _break(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    @property
    def title(self) -> str:
        return normalize_spaces(" ".join(self.title_parts))

    @property
    def text(self) -> str:
        return normalize_text("".join(self.parts))


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_text(value: str) -> str:
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in value.replace("\r", "\n").split("\n")]
    kept: list[str] = []
    blank = False
    for line in lines:
        if not line:
            if kept and not blank:
                kept.append("")
            blank = True
        else:
            kept.append(line)
            blank = False
    while kept and not kept[-1]:
        kept.pop()
    return "\n".join(kept)


def read_links(path: Path) -> list[str]:
    seen: set[str] = set()
    links: list[str] = []
    patterns = (re.compile(r"<(https?://[^>\s]+)>"), re.compile(r"(?<!<)(https?://[^\s)]+)"))
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            for pattern in patterns:
                for raw in pattern.findall(line):
                    url = raw.rstrip(".,;")
                    if url not in seen:
                        seen.add(url)
                        links.append(url)
    return links


def is_internal(url: str, domain: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() == domain.lower()


def looks_like_html(url: str) -> bool:
    path = urllib.parse.urlsplit(url).path.lower()
    return path in {"", "/"} or path.endswith((".htm", ".html", "/"))


def safe_segment(segment: str) -> str:
    segment = urllib.parse.unquote(segment).strip()
    segment = re.sub(r'[<>:"\\|?*\x00-\x1f]', "_", segment).replace("/", "_")
    return segment if segment and segment not in {".", ".."} else "_"


def root_filename_folder(filename: str) -> tuple[str, ...]:
    for pattern, folder_parts in ROOT_FILENAME_FOLDERS:
        if pattern.match(filename):
            return folder_parts
    return ()


def output_path_for_url(url: str, out_dir: Path, domain: str) -> Path:
    parsed = urllib.parse.urlsplit(url)
    raw_parts = [part for part in (parsed.path or "/").split("/") if part and part not in {".", ".."}]
    parts = [safe_segment(part) for part in raw_parts] or ["index"]

    filename = parts[-1]
    lower = filename.lower()
    if lower.endswith(".html"):
        filename = filename[:-5] + ".md"
    elif lower.endswith(".htm"):
        filename = filename[:-4] + ".md"
    else:
        filename += ".md"

    if parsed.query:
        stem, suffix = os.path.splitext(filename)
        digest = hashlib.sha1(parsed.query.encode("utf-8")).hexdigest()[:10]
        filename = f"{stem}-{digest}{suffix or '.md'}"

    parts[-1] = filename
    if is_internal(url, domain):
        folder_parts = root_filename_folder(raw_parts[0]) if len(raw_parts) == 1 else ()
        if folder_parts:
            return out_dir.joinpath(*folder_parts, *parts)
        return out_dir.joinpath(*parts)

    external_domain = safe_segment(parsed.netloc or "external")
    return out_dir / "_external" / external_domain / Path(*parts)


def numbered_page_info(url: str) -> tuple[str, int] | None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.query:
        return None
    path_parts = [part for part in parsed.path.split("/") if part]
    if not path_parts:
        return None

    filename = path_parts[-1]
    if re.match(r"^.+_[0-9]{4}_[0-9]{2}\.html?$", filename, re.IGNORECASE):
        return None

    match = re.match(r"^(.+)_part([0-9]+)(\.html?)$", filename, re.IGNORECASE)
    if not match:
        match = re.match(r"^(.+)_([0-9]+)(\.html?)$", filename, re.IGNORECASE)
    if not match:
        return None

    stem, number, extension = match.groups()
    path_parts[-1] = f"{stem}{extension}"
    base_path = "/" + "/".join(path_parts)
    base_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, base_path, "", ""))
    return base_url, int(number)


def make_single_item(url: str) -> dict[str, object]:
    return {"item_id": url, "output_url": url, "urls": [url], "part_numbers": [None], "combined": False}


def make_combined_item(base_url: str, pages: list[tuple[int, int, str]]) -> dict[str, object]:
    pages = sorted(pages, key=lambda item: (item[0], item[1]))
    return {
        "item_id": f"combined:{base_url}",
        "output_url": base_url,
        "urls": [url for _, _, url in pages],
        "part_numbers": [number for number, _, _ in pages],
        "combined": True,
    }


def build_work_items(args: argparse.Namespace, selected: list[str]) -> list[dict[str, object]]:
    if not args.combine_numbered_pages:
        return [make_single_item(url) for url in selected]

    groups: dict[str, dict[str, object]] = {}
    numbered_urls: set[str] = set()
    for index, url in enumerate(selected):
        info = numbered_page_info(url)
        if not info:
            continue
        base_url, number = info
        numbered_urls.add(url)
        group = groups.setdefault(base_url, {"first_index": index, "pages": []})
        group["first_index"] = min(int(group["first_index"]), index)
        group["pages"].append((number, index, url))

    ordered: list[tuple[int, dict[str, object]]] = []
    absorbed_base_urls: set[str] = set()
    for index, url in enumerate(selected):
        if url in numbered_urls:
            continue
        group = groups.get(url)
        if group:
            existing_numbers = {int(number) for number, _, _ in group["pages"]}
            if 1 not in existing_numbers:
                group["pages"].append((1, index, url))
            group["first_index"] = min(int(group["first_index"]), index)
            absorbed_base_urls.add(url)
        else:
            ordered.append((index, make_single_item(url)))

    for base_url, group in groups.items():
        pages = list(group["pages"])
        item = make_combined_item(base_url, pages) if len(pages) > 1 or base_url in absorbed_base_urls else make_single_item(pages[0][2])
        ordered.append((int(group["first_index"]), item))

    return [item for _, item in sorted(ordered, key=lambda entry: entry[0])]


def load_latest_manifest(manifest_path: Path) -> dict[str, dict[str, object]]:
    latest: dict[str, dict[str, object]] = {}
    if not manifest_path.exists():
        return latest
    with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            for key in (str(record.get("item_id", "")), str(record.get("url", ""))):
                if key:
                    latest[key] = record
    return latest


def append_manifest(manifest_path: Path, record: dict[str, object]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def detect_encoding(content_type: str, data: bytes) -> str:
    match = re.search(r"charset=[\"']?([\w.-]+)", content_type, re.IGNORECASE)
    if not match:
        match_bytes = re.search(br"charset=[\"']?([\w.-]+)", data[:4096], re.IGNORECASE)
        if match_bytes:
            return match_bytes.group(1).decode("ascii", "ignore") or "utf-8"
    return match.group(1) if match else "utf-8"


def fetch_html(url: str, timeout: int, insecure: bool) -> tuple[int, str, str, bytes]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "close",
        },
    )

    def open_url(context: ssl.SSLContext | None) -> tuple[int, str, str, bytes]:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            data = response.read()
            return int(getattr(response, "status", 200)), response.geturl(), str(response.headers.get("content-type", "")), data

    context = ssl._create_unverified_context() if insecure else None
    try:
        return open_url(context)
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        if not insecure and isinstance(reason, ssl.SSLCertVerificationError):
            return open_url(ssl._create_unverified_context())
        raise


def parse_html(data: bytes, content_type: str) -> tuple[str, str]:
    encoding = detect_encoding(content_type, data)
    try:
        html_text = data.decode(encoding, errors="replace")
    except LookupError:
        html_text = data.decode("utf-8", errors="replace")
    parser = ExtractedTextParser()
    parser.feed(html_text)
    parser.close()
    return parser.title, parser.text


def derived_title(url: str, html_title: str, text: str) -> str:
    generic = {
        "",
        "-:: annavin padaippugal ::-",
        ":: annavin padaippugal ::",
        ":: annavin padaippugal :: அறிஞர் அண்ணாவின் படைப்புகள்",
        "annavin padaippugal",
    }
    normalized_title = normalize_spaces(html_title)
    if normalized_title.lower() not in generic:
        return normalized_title
    for line in text.splitlines()[:20]:
        line = normalize_spaces(line)
        if "பட்டியல்" in line or line.startswith("அறிஞர் அண்ணாவின்"):
            continue
        if 3 <= len(line) <= 120 and not line.isdigit():
            return line
    return (Path(urllib.parse.urlsplit(url).path).stem or "index").replace("_", " ")


def yaml_quote(value: object) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def clean_combined_part_text(text: str, title: str, part_number: object) -> str:
    lines = text.strip().splitlines()

    def is_boilerplate(line: str) -> bool:
        clean = normalize_spaces(line)
        return (
            not clean
            or clean == str(part_number)
            or clean == title
            or "பட்டியல்" in clean
            or clean.startswith("அறிஞர் அண்ணாவின்")
        )

    dropped = 0
    while lines and dropped < 12 and is_boilerplate(lines[0]):
        lines.pop(0)
        dropped += 1
    while lines and normalize_spaces(lines[-1]) in {
        "முகப்பு | எழுத்து | பேச்சு | புகைப்படம் | ஓவியம் | தொடர்பு",
        "முகப்பு|எழுத்து|பேச்சு|புகைப்படம்|ஓவியம்|தொடர்பு",
    }:
        lines.pop()
    return "\n".join(lines).strip()


def markdown_for_page(page: dict[str, object], fetched_at: str) -> str:
    title = derived_title(str(page["url"]), str(page.get("html_title", "")), str(page.get("text", "")))
    body = str(page.get("text", "")).strip() or "_No extractable text found on this page._"
    return "\n".join(
        [
            "---",
            f"source_url: {yaml_quote(page['url'])}",
            f"final_url: {yaml_quote(page['final_url'])}",
            f"fetched_at: {yaml_quote(fetched_at)}",
            f"http_status: {page['status']}",
            f"content_type: {yaml_quote(page['content_type'])}",
            f"html_title: {yaml_quote(page.get('html_title', ''))}",
            "---",
            "",
            f"# {title}",
            "",
            f"Source: <{page['url']}>",
            "",
            body,
            "",
        ]
    )


def markdown_for_combined_pages(item: dict[str, object], pages: list[dict[str, object]], failures: list[dict[str, object]], fetched_at: str) -> str:
    urls = list(item["urls"])
    part_numbers = list(item["part_numbers"])
    first_page = pages[0]
    title = derived_title(str(first_page["url"]), str(first_page.get("html_title", "")), str(first_page.get("text", "")))
    lines = [
        "---",
        f"combined: {str(bool(item['combined'])).lower()}",
        f"partial: {str(bool(failures)).lower()}",
        f"source_url_count: {len(urls)}",
        "source_urls:",
    ]
    lines.extend(f"  - {yaml_quote(url)}" for url in urls)
    lines.extend([f"fetched_at: {yaml_quote(fetched_at)}", "---", "", f"# {title}", "", "Source pages:"])
    lines.extend(f"- <{url}>" for url in urls)
    lines.append("")

    page_by_url = {str(page["url"]): page for page in pages}
    for url, part_number in zip(urls, part_numbers):
        page = page_by_url.get(str(url))
        heading = f"Part {part_number}" if part_number is not None else "Page"
        lines.extend([f"## {heading}", ""])
        if page:
            body = clean_combined_part_text(str(page.get("text", "")), title, part_number)
            lines.extend([body or "_No extractable text found on this page._", ""])
        else:
            lines.extend(["_This source page could not be fetched during this run._", ""])

    if failures:
        lines.extend(["## Fetch Issues", ""])
        for failure in failures:
            lines.append(f"- <{failure['url']}> - {failure.get('error', 'unknown error')}")
        lines.append("")
    return "\n".join(lines)


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_text(content, encoding="utf-8")
    os.replace(tmp_path, path)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def fetch_extracted_page(url: str, args: argparse.Namespace) -> dict[str, object]:
    status, final_url, content_type, data = fetch_html(url, args.timeout, args.insecure)
    html_title, text = parse_html(data, content_type)
    return {
        "url": url,
        "status": status,
        "final_url": final_url,
        "content_type": content_type,
        "html_title": html_title,
        "text": text,
        "html_sha256": hashlib.sha256(data).hexdigest(),
    }


def process_item(item: dict[str, object], args: argparse.Namespace, manifest_path: Path, latest: dict[str, dict[str, object]], counts: dict[str, int]) -> None:
    urls = list(item["urls"])
    item_id = str(item["item_id"])
    out_path = output_path_for_url(str(item["output_url"]), args.out_dir, args.domain)
    previous = latest.get(item_id) or latest.get(str(urls[0]), {})
    previous_status = previous.get("status")

    if previous_status == "failed" and not args.retry_failed:
        counts["skipped_failed"] += 1
        if args.verbose:
            print(f"skip known failed: {urls[0]}", flush=True)
        return
    if previous_status == "partial" and out_path.exists() and not args.retry_partial:
        counts["skipped_partial"] += 1
        if args.verbose:
            print(f"skip partial: {out_path.relative_to(args.out_dir)}", flush=True)
        return
    if out_path.exists() and not args.force:
        counts["skipped_existing"] += 1
        if args.verbose:
            print(f"skip existing: {out_path.relative_to(args.out_dir)}", flush=True)
        return

    fetched_at = now_iso()
    pages: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    for url in urls:
        try:
            pages.append(fetch_extracted_page(str(url), args))
            counts["pages_done"] += 1
        except urllib.error.HTTPError as exc:
            failures.append({"url": url, "http_status": exc.code, "error": str(exc)})
            counts["pages_failed"] += 1
        except Exception as exc:  # noqa: BLE001 - CLI records and continues.
            failures.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
            counts["pages_failed"] += 1
        if args.sleep > 0:
            time.sleep(args.sleep)

    if not pages:
        record = {
            "item_id": item_id,
            "url": urls[0] if len(urls) == 1 else item_id,
            "urls": urls,
            "status": "failed",
            "output_path": str(out_path),
            "failures": failures,
            "fetched_at": fetched_at,
        }
        append_manifest(manifest_path, record)
        latest[item_id] = record
        counts["failed"] += 1
        print(f"failed: {urls[0]} ({failures[0].get('error', 'unknown error')})", file=sys.stderr, flush=True)
        return

    markdown = markdown_for_combined_pages(item, pages, failures, fetched_at) if bool(item["combined"]) else markdown_for_page(pages[0], fetched_at)
    write_atomic(out_path, markdown)
    status_name = "partial" if failures else "done"
    record = {
        "item_id": item_id,
        "url": urls[0] if len(urls) == 1 else item_id,
        "urls": urls,
        "status": status_name,
        "combined": bool(item["combined"]),
        "output_path": str(out_path),
        "fetched_at": fetched_at,
        "page_count": len(pages),
        "failed_page_count": len(failures),
        "failures": failures,
        "pages": [
            {
                "url": page["url"],
                "http_status": page["status"],
                "content_type": page["content_type"],
                "final_url": page["final_url"],
                "html_sha256": page["html_sha256"],
                "text_chars": len(str(page["text"])),
            }
            for page in pages
        ],
    }
    append_manifest(manifest_path, record)
    latest[item_id] = record
    counts["partial" if failures else "done"] += 1
    if args.verbose:
        label = "partial" if failures else "done"
        print(f"{label}: {out_path.relative_to(args.out_dir)} ({len(pages)}/{len(urls)} pages)", flush=True)


def iter_selected_links(args: argparse.Namespace, links: Iterable[str]) -> list[str]:
    selected: list[str] = []
    for url in links:
        if not args.include_external and not is_internal(url, args.domain):
            continue
        if not args.include_non_html and not looks_like_html(url):
            continue
        selected.append(url)
        if args.limit and len(selected) >= args.limit:
            break
    return selected


def make_summary(out_dir: Path, manifest_path: Path, counts: dict[str, int], started_at: str, finished_at: str) -> None:
    problem_report = out_dir / "_extract_state" / "known_problems.md"
    failed_links_report = out_dir / "_extract_state" / "failed_links.md"
    lines = [
        "# Extraction Summary",
        "",
        f"- Started: {started_at}",
        f"- Finished: {finished_at}",
        f"- Output folder: `{out_dir}`",
        f"- Manifest: `{manifest_path}`",
        f"- Done files this run: {counts.get('done', 0)}",
        f"- Partial files this run: {counts.get('partial', 0)}",
        f"- Skipped existing: {counts.get('skipped_existing', 0)}",
        f"- Skipped known failed: {counts.get('skipped_failed', 0)}",
        f"- Skipped known partial: {counts.get('skipped_partial', 0)}",
        f"- Failed this run: {counts.get('failed', 0)}",
        f"- Source pages fetched this run: {counts.get('pages_done', 0)}",
        f"- Source pages failed this run: {counts.get('pages_failed', 0)}",
        f"- Total output files considered: {counts.get('total_considered', 0)}",
        f"- Known problem report: `{problem_report}`",
        f"- Failed links report: `{failed_links_report}`",
        "",
        "Normal reruns skip completed files, known failed links, and partial files. Use `--retry-failed` or `--retry-partial` when you want to try those again.",
        "",
    ]
    write_atomic(out_dir / "_extract_state" / "summary.md", "\n".join(lines))


def problem_error_text(record: dict[str, object]) -> str:
    failures = record.get("failures")
    if isinstance(failures, list) and failures:
        first = failures[0]
        if isinstance(first, dict):
            return str(first.get("error", "unknown error"))
    return str(record.get("error", "unknown error"))


def canonical_problem_key(record: dict[str, object]) -> str:
    url = str(record.get("url") or record.get("item_id") or "")
    url = re.sub(r"^https://", "http://", url)
    return url


def write_problem_report(out_dir: Path, latest: dict[str, dict[str, object]]) -> Path:
    failed: dict[str, dict[str, object]] = {}
    partial: dict[str, dict[str, object]] = {}

    for record in latest.values():
        status = record.get("status")
        if status == "failed":
            failed[canonical_problem_key(record)] = record
        elif status == "partial":
            partial[canonical_problem_key(record)] = record

    lines = [
        "# Known Extraction Problems",
        "",
        "These are the remaining source-site problems recorded by the extractor.",
        "Normal runs skip these so the tool finishes quickly.",
        "",
        f"- Failed items: {len(failed)}",
        f"- Partial combined files: {len(partial)}",
        "",
    ]

    if failed:
        lines.extend(["## Failed Items", ""])
        for record in sorted(failed.values(), key=lambda r: str(r.get("url") or r.get("item_id"))):
            url = str(record.get("url") or record.get("item_id"))
            output_path = str(record.get("output_path") or "")
            lines.append(f"- Source: <{url}>")
            if output_path:
                lines.append(f"  Output: `{output_path}`")
            lines.append(f"  Error: {problem_error_text(record)}")
        lines.append("")

    if partial:
        lines.extend(["## Partial Combined Files", ""])
        for record in sorted(partial.values(), key=lambda r: str(r.get("url") or r.get("item_id"))):
            url = str(record.get("url") or record.get("item_id"))
            output_path = str(record.get("output_path") or "")
            lines.append(f"- Item: `{url}`")
            if output_path:
                lines.append(f"  Output: `{output_path}`")
            failures = record.get("failures")
            if isinstance(failures, list):
                for failure in failures:
                    if isinstance(failure, dict):
                        lines.append(f"  Missing source: <{failure.get('url', '')}>")
                        lines.append(f"  Error: {failure.get('error', 'unknown error')}")
            else:
                lines.append(f"  Error: {problem_error_text(record)}")
        lines.append("")

    report_path = out_dir / "_extract_state" / "known_problems.md"
    write_atomic(report_path, "\n".join(lines))

    failed_lines = [
        "# Failed Links",
        "",
        "This file contains source URLs that could not be fetched.",
        "",
        "## Failed Items",
        "",
    ]
    if failed:
        for record in sorted(failed.values(), key=lambda r: str(r.get("url") or r.get("item_id"))):
            url = str(record.get("url") or record.get("item_id"))
            failed_lines.append(f"- <{url}>")
            failed_lines.append(f"  Error: {problem_error_text(record)}")
    else:
        failed_lines.append("None.")

    failed_lines.extend(["", "## Missing Links From Partial Files", ""])
    partial_missing_count = 0
    for record in sorted(partial.values(), key=lambda r: str(r.get("url") or r.get("item_id"))):
        failures = record.get("failures")
        if isinstance(failures, list):
            for failure in failures:
                if isinstance(failure, dict):
                    partial_missing_count += 1
                    failed_lines.append(f"- <{failure.get('url', '')}>")
                    failed_lines.append(f"  Error: {failure.get('error', 'unknown error')}")
    if partial_missing_count == 0:
        failed_lines.append("None.")

    failed_report_path = out_dir / "_extract_state" / "failed_links.md"
    write_atomic(failed_report_path, "\n".join(failed_lines) + "\n")
    return report_path


def markdown_source_urls(text: str) -> list[str]:
    urls: list[str] = []
    urls.extend(re.findall(r'source_url:\s+"([^"]+)"', text))
    urls.extend(re.findall(r"source_url:\s+(\S+)", text))
    urls.extend(re.findall(r"^\s+-\s+\"(https?://[^\"]+)\"", text, flags=re.MULTILINE))
    urls.extend(re.findall(r"<(https?://[^>]+)>", text))
    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def useful_markdown_body_chars(text: str) -> int:
    text = re.sub(r"(?s)^---\n.*?\n---\n", "", text, count=1)
    useful_lines: list[str] = []
    for line in text.splitlines():
        clean = normalize_spaces(line)
        if not clean:
            continue
        if clean.startswith("#"):
            continue
        if clean.startswith("Source:") or clean == "Source pages:":
            continue
        if re.fullmatch(r"-\s+<https?://[^>]+>", clean):
            continue
        if clean.startswith("_No extractable text found"):
            continue
        if clean.startswith("_This source page could not be fetched"):
            continue
        useful_lines.append(clean)
    return len(normalize_spaces(" ".join(useful_lines)))


def no_text_section_for(output_path: str, url: str, out_dir: Path) -> str:
    if output_path:
        try:
            rel = Path(output_path).resolve().relative_to(out_dir.resolve())
            if rel.stem.lower() == "speech_audios":
                return "speech_audios"
            if len(rel.parts) > 1:
                return rel.parts[0].lower()
            stem = rel.stem.lower()
            if stem.startswith("contact"):
                return "contact"
        except ValueError:
            pass

    path_parts = [part.lower() for part in urllib.parse.urlsplit(url).path.split("/") if part]
    if path_parts:
        if path_parts[0] in {"oviyam", "photos", "contact", "contacts"}:
            return path_parts[0]
        if path_parts[-1].startswith("annavin_oviyam") or path_parts[-1].startswith("oaviyam"):
            return "oviyam"
        if path_parts[-1].startswith("annavin_pugaipadangal") or path_parts[-1].startswith("photos") or path_parts[-1].startswith("parimalam_photos"):
            return "photos"
        if path_parts[-1].startswith("speech_audios"):
            return "speech_audios"
        if path_parts[-1].startswith("contact"):
            return "contact"
    return ""


def write_no_text_report(out_dir: Path, min_body_chars: int, excluded_sections: set[str]) -> Path:
    latest = load_latest_manifest(out_dir / "_extract_state" / "manifest.jsonl")
    candidates: dict[str, tuple[int, str, str]] = {}
    excluded_count = 0
    seen_records: set[int] = set()

    for record in latest.values():
        record_id = id(record)
        if record_id in seen_records:
            continue
        seen_records.add(record_id)
        if record.get("status") not in {"done", "partial"}:
            continue

        output_path = str(record.get("output_path") or "")
        if output_path and not Path(output_path).exists():
            continue
        pages = record.get("pages")
        if isinstance(pages, list) and pages:
            for page in pages:
                if not isinstance(page, dict):
                    continue
                url = str(page.get("url") or "")
                try:
                    text_chars = int(page.get("text_chars") or 0)
                except (TypeError, ValueError):
                    text_chars = 0
                if url and text_chars < min_body_chars:
                    section = no_text_section_for(output_path, url, out_dir)
                    if section in excluded_sections:
                        excluded_count += 1
                        continue
                    candidates[url] = (text_chars, output_path, url)
            continue

        url = str(record.get("url") or "")
        try:
            text_chars = int(record.get("text_chars") or 0)
        except (TypeError, ValueError):
            text_chars = 0
        if url and text_chars < min_body_chars:
            section = no_text_section_for(output_path, url, out_dir)
            if section in excluded_sections:
                excluded_count += 1
                continue
            candidates[url] = (text_chars, output_path, url)

    report_path = out_dir / "_extract_state" / "no_text_or_scanned_pages.md"
    lines = [
        "# No Text Or Scanned Page Candidates",
        "",
        "These source pages had little or no text recorded during extraction.",
        "They may be scanned images, photo pages, audio/index pages, or otherwise not plain HTML text.",
        "",
        f"- Text character threshold: {min_body_chars}",
        f"- Excluded sections: {', '.join(sorted(excluded_sections)) if excluded_sections else 'none'}",
        f"- Excluded source pages: {excluded_count}",
        f"- Candidate source pages: {len(candidates)}",
        "",
    ]
    for text_chars, output_path, url in sorted(candidates.values(), key=lambda item: item[2]):
        lines.append(f"- <{url}>")
        lines.append(f"  Text characters: {text_chars}")
        if output_path:
            lines.append(f"  Output: `{output_path}`")
        lines.append("")
    write_atomic(report_path, "\n".join(lines))
    return report_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract website HTML text into resumable Markdown files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--links", type=Path, default=DEFAULT_LINKS, help="Markdown file containing links.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Folder where Markdown pages are written.")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="Internal domain to mirror into folders.")
    parser.add_argument("--include-external", action="store_true", help="Also fetch external HTTP(S) links.")
    parser.add_argument("--include-non-html", action="store_true", help="Try links that do not look like HTML pages.")
    parser.add_argument("--no-combine-numbered-pages", dest="combine_numbered_pages", action="store_false", help="Keep numbered pages as separate Markdown files.")
    parser.add_argument("--force", action="store_true", help="Re-fetch and overwrite existing Markdown files.")
    parser.add_argument("--retry-failed", action="store_true", help="Retry URLs previously recorded as failed.")
    parser.add_argument("--retry-partial", action="store_true", help="Retry combined files previously recorded as partial.")
    parser.add_argument("--limit", type=int, default=0, help="Only process the first N selected links; 0 means no limit.")
    parser.add_argument("--timeout", type=int, default=10, help="Network timeout per page, in seconds.")
    parser.add_argument("--sleep", type=float, default=0.05, help="Pause between page requests, in seconds.")
    parser.add_argument("--insecure", action="store_true", help="Disable HTTPS certificate verification.")
    parser.add_argument("--quiet", action="store_true", help="Print only failures and final summary.")
    parser.add_argument("--verbose", action="store_true", help="Print every skipped and written file.")
    parser.add_argument("--scan-no-text", action="store_true", help="Write a report of Markdown files with little or no body text, then exit.")
    parser.add_argument("--min-body-chars", type=int, default=120, help="Useful body character threshold for --scan-no-text.")
    parser.add_argument(
        "--exclude-no-text-sections",
        default="oviyam,photos,contact,contacts,speech_audios",
        help="Comma-separated sections to exclude from --scan-no-text.",
    )
    parser.add_argument("--include-all-no-text-sections", action="store_true", help="Do not exclude any sections from --scan-no-text.")
    parser.set_defaults(combine_numbered_pages=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.links = args.links.resolve()
    args.out_dir = args.out_dir.resolve()

    if not args.links.exists():
        print(f"Link file not found: {args.links}", file=sys.stderr, flush=True)
        return 2

    if args.scan_no_text:
        excluded_sections = set()
        if not args.include_all_no_text_sections:
            excluded_sections = {
                section.strip().lower()
                for section in args.exclude_no_text_sections.split(",")
                if section.strip()
            }
        report_path = write_no_text_report(args.out_dir, args.min_body_chars, excluded_sections)
        print(f"No-text/scanned-page report: {report_path}", flush=True)
        return 0

    print(f"Links file: {args.links}", flush=True)
    print(f"Output folder: {args.out_dir}", flush=True)

    manifest_path = args.out_dir / "_extract_state" / "manifest.jsonl"
    latest = load_latest_manifest(manifest_path)
    links = read_links(args.links)
    selected = iter_selected_links(args, links)
    work_items = build_work_items(args, selected)
    started_at = now_iso()
    counts = {
        "done": 0,
        "partial": 0,
        "failed": 0,
        "skipped_existing": 0,
        "skipped_failed": 0,
        "skipped_partial": 0,
        "skipped_filtered": max(0, len(links) - len(selected)),
        "pages_done": 0,
        "pages_failed": 0,
        "total_considered": len(work_items),
    }

    print(f"Selected links: {len(selected)}", flush=True)
    print(f"Output files to consider: {len(work_items)}", flush=True)
    print(f"Combine numbered pages: {'yes' if args.combine_numbered_pages else 'no'}", flush=True)
    print("Resume: completed, known failed, and partial files are skipped unless retry flags are used.", flush=True)

    try:
        for index, item in enumerate(work_items, start=1):
            if args.verbose:
                urls = list(item["urls"])
                label = str(item["output_url"])
                if len(urls) > 1:
                    label = f"{label} ({len(urls)} source pages)"
                print(f"[{index}/{len(work_items)}] {label}", flush=True)
            elif not args.quiet and (index == 1 or index % 100 == 0 or index == len(work_items)):
                print(f"Progress: {index}/{len(work_items)}", flush=True)
            process_item(item, args, manifest_path, latest, counts)
    except KeyboardInterrupt:
        print("\nStopped by user. Progress is saved; run the same command to resume.", file=sys.stderr, flush=True)
        make_summary(args.out_dir, manifest_path, counts, started_at, now_iso())
        write_problem_report(args.out_dir, latest)
        return 130

    make_summary(args.out_dir, manifest_path, counts, started_at, now_iso())
    problem_report = write_problem_report(args.out_dir, latest)
    print("\nFinished.", flush=True)
    print(f"Done files this run: {counts['done']}", flush=True)
    print(f"Partial files this run: {counts['partial']}", flush=True)
    print(f"Skipped existing: {counts['skipped_existing']}", flush=True)
    print(f"Skipped known failed: {counts['skipped_failed']}", flush=True)
    print(f"Skipped known partial: {counts['skipped_partial']}", flush=True)
    print(f"Failed this run: {counts['failed']}", flush=True)
    print(f"Source pages fetched this run: {counts['pages_done']}", flush=True)
    print(f"Source pages failed this run: {counts['pages_failed']}", flush=True)
    print(f"Summary: {args.out_dir / '_extract_state' / 'summary.md'}", flush=True)
    print(f"Known problems: {problem_report}", flush=True)
    print(f"Failed links: {args.out_dir / '_extract_state' / 'failed_links.md'}", flush=True)
    return 0 if counts["failed"] == 0 and counts["partial"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
