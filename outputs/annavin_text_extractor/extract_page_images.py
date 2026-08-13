#!/usr/bin/env python3
"""
Download page images from no-text/scanned-page links into OCR-friendly PNG files.

The tool is dependency-light and resumable. It reads the no-text report produced
by extract_html_text.py, fetches each page, finds useful image references, and
writes grayscale/autocontrasted PNGs suitable as OCR inputs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import io
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

try:
    from PIL import Image, ImageOps
except Exception:  # pragma: no cover - local fallback message is enough.
    Image = None
    ImageOps = None


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LINKS = SCRIPT_DIR / "md_pages" / "_extract_state" / "no_text_or_scanned_pages.md"
DEFAULT_OUT_DIR = SCRIPT_DIR / "ocr_images"
DEFAULT_DOMAIN = "www.annavinpadaippugal.info"
USER_AGENT = "annavin-image-extractor/1.0"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff"}
SKIP_PATH_HINTS = (
    "/titlepage/",
    "/intropage/",
    "/writtings_menu/",
    "/numbers%20for%20links/",
    "/numbers for links/",
    "/menu/",
    "/button",
    "/buttons/",
    "/icons/",
)


class ImageLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v or "") for k, v in attrs if k}
        tag = tag.lower()
        if tag == "img" and attr.get("src"):
            self.images.append(
                {
                    "kind": "img",
                    "url": attr.get("src", ""),
                    "width": attr.get("width", ""),
                    "height": attr.get("height", ""),
                    "alt": attr.get("alt", ""),
                    "title": attr.get("title", ""),
                }
            )
        elif tag == "a" and attr.get("href") and looks_like_image_url(attr.get("href", "")):
            self.images.append({"kind": "link", "url": attr.get("href", ""), "width": "", "height": "", "alt": "", "title": ""})


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def read_source_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    candidates = re.findall(r"<(https?://[^>]+)>", text)
    seen: set[str] = set()
    links: list[str] = []
    for url in candidates:
        if url not in seen:
            seen.add(url)
            links.append(url)
    return links


def safe_segment(value: str) -> str:
    value = urllib.parse.unquote(value).strip()
    value = re.sub(r'[<>:"\\|?*\x00-\x1f]', "_", value)
    value = value.replace("/", "_")
    return value if value and value not in {".", ".."} else "_"


def section_for_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) > 1:
        return safe_segment(parts[0])
    leaf = parts[-1].lower() if parts else "index"
    if leaf.startswith("annavin_english_"):
        return "english"
    if leaf.startswith("annavin_kadithangal"):
        return "kadithangal"
    if leaf.startswith("annavin_katturaigal"):
        return "katturaigal"
    if leaf.startswith("annavin_sirukathaigal"):
        return "sirukathaigal"
    if leaf.startswith("annavin_navalgal"):
        return "navalgal"
    if leaf.startswith("annavin_kurunavalgal"):
        return "Kurunavalgal"
    if leaf.startswith("annavin_kavithaigal"):
        return "kavithaigal"
    if leaf.startswith("annavin_nadagangal"):
        return "nadagangal"
    if leaf.startswith("speech"):
        return "sorpozhivugal"
    return "root"


def page_stem_for_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    leaf = Path(parsed.path).name or "index"
    stem = re.sub(r"\.html?$", "", leaf, flags=re.IGNORECASE)
    return safe_segment(stem or "index")


def page_dir_for_url(url: str, out_dir: Path) -> Path:
    return out_dir / section_for_url(url) / page_stem_for_url(url)


def looks_like_image_url(url: str) -> bool:
    path = urllib.parse.urlsplit(url).path.lower()
    return Path(path).suffix in IMAGE_EXTENSIONS


def normalize_url(raw: str, base: str) -> str | None:
    raw = html.unescape((raw or "").strip())
    if not raw or raw.startswith("#") or raw.lower().startswith(("mailto:", "javascript:", "tel:")):
        return None
    url = urllib.parse.urljoin(base, raw)
    url, _ = urllib.parse.urldefrag(url)
    parsed = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(urllib.parse.unquote(parsed.path), safe="/%:@")
    query = urllib.parse.quote(urllib.parse.unquote_plus(parsed.query), safe="=&?/%:@;+,%")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, query, ""))


def should_skip_by_path(url: str) -> bool:
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path).lower()
    return any(hint in path for hint in SKIP_PATH_HINTS)


def fetch_bytes(url: str, timeout: int, insecure: bool) -> tuple[int, str, str, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Connection": "close"})

    def open_url(context: ssl.SSLContext | None) -> tuple[int, str, str, bytes]:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            return int(getattr(response, "status", 200)), response.geturl(), str(response.headers.get("content-type", "")), response.read()

    context = ssl._create_unverified_context() if insecure else None
    try:
        return open_url(context)
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        if not insecure and isinstance(reason, ssl.SSLCertVerificationError):
            return open_url(ssl._create_unverified_context())
        raise


def decode_html(data: bytes, content_type: str) -> str:
    match = re.search(r"charset=[\"']?([\w.-]+)", content_type, re.IGNORECASE)
    encoding = match.group(1) if match else "utf-8"
    try:
        return data.decode(encoding, errors="replace")
    except LookupError:
        return data.decode("utf-8", errors="replace")


def discover_images(page_url: str, timeout: int, insecure: bool) -> list[dict[str, str]]:
    _, final_url, content_type, data = fetch_bytes(page_url, timeout, insecure)
    parser = ImageLinkParser()
    parser.feed(decode_html(data, content_type))
    parser.close()

    seen: set[str] = set()
    images: list[dict[str, str]] = []
    for item in parser.images:
        image_url = normalize_url(item["url"], final_url)
        if not image_url or image_url in seen:
            continue
        seen.add(image_url)
        item = dict(item)
        item["url"] = image_url
        images.append(item)
    return images


def parse_int(value: str) -> int:
    match = re.search(r"\d+", value or "")
    return int(match.group(0)) if match else 0


def ocr_image_from_bytes(data: bytes, args: argparse.Namespace) -> tuple[bytes, tuple[int, int], tuple[int, int]]:
    if Image is None or ImageOps is None:
        raise RuntimeError("Pillow is required for OCR PNG preparation. Install Pillow or use --save-original-only.")

    with Image.open(io.BytesIO(data)) as img:
        original_size = img.size
        prepared = ImageOps.exif_transpose(img).convert("L")
        prepared = ImageOps.autocontrast(prepared)
        width, height = prepared.size
        shortest = min(width, height)
        if args.upscale and shortest and shortest < args.target_min_edge:
            scale = min(args.max_upscale, max(1.0, args.target_min_edge / shortest))
            new_size = (int(width * scale), int(height * scale))
            prepared = prepared.resize(new_size, Image.Resampling.LANCZOS)
        out = io.BytesIO()
        prepared.save(out, format="PNG", optimize=True)
        return out.getvalue(), original_size, prepared.size


def image_dimensions(data: bytes) -> tuple[int, int]:
    if Image is None:
        return 0, 0
    with Image.open(io.BytesIO(data)) as img:
        return img.size


def append_manifest(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def load_completed(manifest_path: Path) -> set[str]:
    completed: set[str] = set()
    if not manifest_path.exists():
        return completed
    with manifest_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("status") == "done" and record.get("source_image_url"):
                completed.add(str(record["source_image_url"]))
                if record.get("requested_image_url"):
                    completed.add(str(record["requested_image_url"]))
    return completed


def should_keep_image(item: dict[str, str], image_url: str, data: bytes, args: argparse.Namespace) -> tuple[bool, str, tuple[int, int]]:
    hinted_width = parse_int(item.get("width", ""))
    hinted_height = parse_int(item.get("height", ""))
    if not args.include_decorative and should_skip_by_path(image_url):
        return False, "decorative path", (hinted_width, hinted_height)
    if len(data) < args.min_bytes and not args.include_small:
        return False, f"too small bytes ({len(data)})", (hinted_width, hinted_height)

    width, height = image_dimensions(data)
    if not width:
        width, height = hinted_width, hinted_height
    if not args.include_small and width and height:
        if width < args.min_width or height < args.min_height:
            return False, f"too small dimensions ({width}x{height})", (width, height)
    return True, "", (width, height)


def should_skip_before_fetch(item: dict[str, str], image_url: str, args: argparse.Namespace) -> bool:
    """Reject clearly decorative/small images using trustworthy HTML hints."""
    if not args.include_decorative and should_skip_by_path(image_url):
        return True
    if args.include_small:
        return False
    width = parse_int(item.get("width", ""))
    height = parse_int(item.get("height", ""))
    return bool(width and height and (width < args.min_width or height < args.min_height))


def write_index(out_dir: Path, records: list[dict[str, object]], failures: list[dict[str, object]]) -> None:
    lines = [
        "# OCR Image Extraction Summary",
        "",
        f"- Generated: {now_iso()}",
        f"- Images written this run: {len(records)}",
        f"- Failures this run: {len(failures)}",
        "",
        "## Images",
        "",
    ]
    if records:
        for record in records:
            lines.append(f"- `{record['ocr_path']}`")
            lines.append(f"  Page: <{record['page_url']}>")
            lines.append(f"  Source image: <{record['source_image_url']}>")
    else:
        lines.append("None written this run.")

    lines.extend(["", "## Failures", ""])
    if failures:
        for failure in failures:
            lines.append(f"- <{failure.get('url', '')}>")
            lines.append(f"  Error: {failure.get('error', 'unknown error')}")
    else:
        lines.append("None.")
    (out_dir / "_state").mkdir(parents=True, exist_ok=True)
    (out_dir / "_state" / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_page(page_url: str, args: argparse.Namespace, completed: set[str], manifest_path: Path, run_records: list[dict[str, object]], run_failures: list[dict[str, object]]) -> None:
    page_dir = page_dir_for_url(page_url, args.out_dir)
    try:
        images = discover_images(page_url, args.timeout, args.insecure)
    except Exception as exc:  # noqa: BLE001 - CLI records and continues.
        failure = {"url": page_url, "status": "failed_page", "error": f"{type(exc).__name__}: {exc}", "at": now_iso()}
        append_manifest(manifest_path, failure)
        run_failures.append(failure)
        print(f"failed page: {page_url} ({failure['error']})", file=sys.stderr, flush=True)
        return

    ordinal = 0
    for item in images:
        image_url = item["url"]
        if should_skip_before_fetch(item, image_url, args):
            continue
        if image_url in completed and not args.force:
            # Completed images still occupy their original position. Counting
            # them prevents a newly eligible image on a resumed run from being
            # assigned the same ordinal as an existing file.
            ordinal += 1
            continue
        try:
            _, final_image_url, content_type, data = fetch_bytes(image_url, args.timeout, args.insecure)
            keep, reason, size = should_keep_image(item, final_image_url, data, args)
            if not keep:
                if args.verbose:
                    print(f"skip image: {final_image_url} ({reason})", flush=True)
                continue

            ordinal += 1
            digest = hashlib.sha1(final_image_url.encode("utf-8")).hexdigest()[:10]
            base_name = f"{ordinal:03d}-{digest}"
            page_dir.mkdir(parents=True, exist_ok=True)

            if args.save_originals:
                ext = Path(urllib.parse.urlsplit(final_image_url).path).suffix.lower() or ".img"
                original_path = page_dir / "originals" / f"{base_name}{ext}"
                original_path.parent.mkdir(parents=True, exist_ok=True)
                original_path.write_bytes(data)
            else:
                original_path = None

            if args.save_original_only:
                ext = Path(urllib.parse.urlsplit(final_image_url).path).suffix.lower() or ".img"
                ocr_path = page_dir / f"{base_name}{ext}"
                ocr_path.write_bytes(data)
                original_size = prepared_size = size
            else:
                ocr_bytes, original_size, prepared_size = ocr_image_from_bytes(data, args)
                ocr_path = page_dir / f"{base_name}.png"
                ocr_path.write_bytes(ocr_bytes)

            record = {
                "status": "done",
                "page_url": page_url,
                "requested_image_url": image_url,
                "source_image_url": final_image_url,
                "content_type": content_type,
                "ocr_path": str(ocr_path),
                "original_path": str(original_path) if original_path else "",
                "original_size": original_size,
                "prepared_size": prepared_size,
                "bytes": len(data),
                "at": now_iso(),
            }
            append_manifest(manifest_path, record)
            completed.add(image_url)
            run_records.append(record)
            if not args.quiet:
                print(f"image: {ocr_path.relative_to(args.out_dir)}", flush=True)
        except Exception as exc:  # noqa: BLE001 - CLI records and continues.
            failure = {"url": image_url, "page_url": page_url, "status": "failed_image", "error": f"{type(exc).__name__}: {exc}", "at": now_iso()}
            append_manifest(manifest_path, failure)
            run_failures.append(failure)
            print(f"failed image: {image_url} ({failure['error']})", file=sys.stderr, flush=True)

        if args.sleep > 0:
            time.sleep(args.sleep)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download page images into OCR-friendly files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--links", type=Path, default=DEFAULT_LINKS, help="Markdown file containing source page links.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Folder where OCR-ready images are written.")
    parser.add_argument("--limit", type=int, default=0, help="Only process the first N source pages; 0 means no limit.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout per page/image, in seconds.")
    parser.add_argument("--sleep", type=float, default=0.05, help="Pause between image requests, in seconds.")
    parser.add_argument("--min-width", type=int, default=300, help="Minimum image width to keep.")
    parser.add_argument(
        "--min-height",
        type=int,
        default=120,
        help="Minimum image height to keep; short, wide scans often contain an article title and opening lines.",
    )
    parser.add_argument("--min-bytes", type=int, default=5000, help="Minimum downloaded image bytes to keep.")
    parser.add_argument("--target-min-edge", type=int, default=1600, help="Upscale images whose shorter edge is below this size.")
    parser.add_argument("--max-upscale", type=float, default=3.0, help="Maximum OCR preparation upscale factor.")
    parser.add_argument("--include-small", action="store_true", help="Keep small images too.")
    parser.add_argument("--include-decorative", action="store_true", help="Do not skip known menu/decorative image paths.")
    parser.add_argument("--no-upscale", dest="upscale", action="store_false", help="Do not upscale OCR PNGs.")
    parser.add_argument("--save-originals", action="store_true", help="Also save original downloaded images under originals/.")
    parser.add_argument("--save-original-only", action="store_true", help="Skip OCR PNG preparation and save original files only.")
    parser.add_argument("--force", action="store_true", help="Download images again even if already recorded.")
    parser.add_argument("--insecure", action="store_true", help="Disable HTTPS certificate verification.")
    parser.add_argument("--quiet", action="store_true", help="Print only failures and final summary.")
    parser.add_argument("--verbose", action="store_true", help="Print skipped images too.")
    parser.set_defaults(upscale=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.links = args.links.resolve()
    args.out_dir = args.out_dir.resolve()

    if Image is None and not args.save_original_only:
        print("Pillow is not available. Run with --save-original-only or install Pillow.", file=sys.stderr)
        return 2
    if not args.links.exists():
        print(f"Link report not found: {args.links}", file=sys.stderr)
        return 2

    links = read_source_links(args.links)
    if args.limit:
        links = links[: args.limit]
    manifest_path = args.out_dir / "_state" / "manifest.jsonl"
    completed = load_completed(manifest_path)
    run_records: list[dict[str, object]] = []
    run_failures: list[dict[str, object]] = []

    print(f"Source link report: {args.links}", flush=True)
    print(f"OCR image folder: {args.out_dir}", flush=True)
    print(f"Source pages to inspect: {len(links)}", flush=True)

    try:
        for index, page_url in enumerate(links, start=1):
            if not args.quiet and (args.verbose or index == 1 or index % 25 == 0 or index == len(links)):
                print(f"Page {index}/{len(links)}: {page_url}", flush=True)
            process_page(page_url, args, completed, manifest_path, run_records, run_failures)
    except KeyboardInterrupt:
        print("\nStopped by user. Progress is saved; run the same command to resume.", file=sys.stderr, flush=True)
        write_index(args.out_dir, run_records, run_failures)
        return 130

    write_index(args.out_dir, run_records, run_failures)
    print("\nFinished.", flush=True)
    print(f"Images written this run: {len(run_records)}", flush=True)
    print(f"Failures this run: {len(run_failures)}", flush=True)
    print(f"Summary: {args.out_dir / '_state' / 'summary.md'}", flush=True)
    return 0 if not run_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
