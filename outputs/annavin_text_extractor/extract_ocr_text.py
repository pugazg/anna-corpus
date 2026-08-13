#!/usr/bin/env python3
"""
Run Tesseract OCR over downloaded OCR images and write Markdown text files.

The tool reads images produced by extract_page_images.py, groups them by page
folder, and writes one Markdown file per page. It is resumable: existing output
Markdown files are skipped unless --force is used.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_IMAGE_DIR = SCRIPT_DIR / "ocr_images"
DEFAULT_OUT_DIR = SCRIPT_DIR / "ocr_text"
TAMIL_TEXT_FIXES = {
    "௮வர்": "அவர்",
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def append_manifest(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def page_output_path(page_dir: Path, image_dir: Path, out_dir: Path) -> Path:
    relative = page_dir.relative_to(image_dir)
    if len(relative.parts) == 1:
        return out_dir / f"{relative.parts[0]}.md"
    return out_dir / relative.parent / f"{relative.name}.md"


def find_page_dirs(image_dir: Path) -> list[Path]:
    page_dirs: set[Path] = set()
    for image_path in image_dir.rglob("*.png"):
        relative_parts = image_path.relative_to(image_dir).parts
        if any(part.startswith("_") for part in relative_parts):
            continue
        if "originals" in relative_parts:
            continue
        page_dirs.add(image_path.parent)
    return sorted(page_dirs, key=lambda path: str(path.relative_to(image_dir)).lower())


def filter_page_dirs(page_dirs: list[Path], image_dir: Path, patterns: list[str]) -> list[Path]:
    if not patterns:
        return page_dirs
    filtered: list[Path] = []
    normalized_patterns = [pattern.lower().strip("/") for pattern in patterns if pattern.strip()]
    for page_dir in page_dirs:
        relative = page_dir.relative_to(image_dir).as_posix().lower()
        name = page_dir.name.lower()
        if any(pattern in relative or pattern == name for pattern in normalized_patterns):
            filtered.append(page_dir)
    return filtered


def tesseract_command(image_path: Path, args: argparse.Namespace, psm: int | None = None) -> list[str]:
    return [
        args.tesseract,
        str(image_path),
        "stdout",
        "-l",
        args.lang,
        "--oem",
        str(args.oem),
        "--psm",
        str(args.psm if psm is None else psm),
    ]


def invoke_tesseract(
    image_path: Path, args: argparse.Namespace, psm: int | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        tesseract_command(image_path, args, psm),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=args.timeout,
        check=False,
    )


def save_normalized_ocr_image(image: Image.Image, path: Path) -> None:
    grayscale = ImageOps.autocontrast(image.convert("L"), cutoff=1)
    grayscale.save(path, quality=100, subsampling=0)


def run_tesseract(image_path: Path, args: argparse.Namespace) -> tuple[str, str]:
    normalized_path: Path | None = None
    retry_path: Path | None = None
    with Image.open(image_path) as image:
        has_alpha = image.mode in {"LA", "RGBA"} or "transparency" in image.info
        if has_alpha:
            # Some source PNGs carry their page in an alpha channel. Image viewers
            # display them normally, but Tesseract sees a blank foreground unless
            # the image is explicitly composited onto white.
            rgba = image.convert("RGBA")
            flattened = Image.new("RGBA", image.size, "white")
            flattened.alpha_composite(rgba)
            flattened = flattened.convert("L")
            handle = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            handle.close()
            normalized_path = Path(handle.name)
            flattened.save(normalized_path)

    try:
        if args.normalize_images and normalized_path is None:
            with Image.open(image_path) as image:
                handle = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                handle.close()
                retry_path = Path(handle.name)
                save_normalized_ocr_image(image, retry_path)
        result = invoke_tesseract(retry_path or normalized_path or image_path, args)
        if result.returncode == 0 and not result.stdout.strip():
            # Some valid grayscale PNGs render normally but produce no symbols in
            # Tesseract. A JPEG round-trip normalizes their pixel representation.
            with Image.open(normalized_path or image_path) as image:
                handle = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                handle.close()
                retry_path = Path(handle.name)
                save_normalized_ocr_image(image, retry_path)
            result = invoke_tesseract(retry_path, args)
    finally:
        if normalized_path:
            normalized_path.unlink(missing_ok=True)
        if retry_path:
            retry_path.unlink(missing_ok=True)
    if result.returncode != 0:
        message = result.stderr.strip() or f"Tesseract exited with {result.returncode}"
        raise RuntimeError(message)
    return result.stdout.strip(), result.stderr.strip()


def cleanup_ocr_text(text: str, args: argparse.Namespace) -> str:
    if args.no_cleanup or "tam" not in args.lang.lower():
        return text
    for wrong, right in TAMIL_TEXT_FIXES.items():
        text = text.replace(wrong, right)
    return re.sub(r"(?<![A-Za-z])Hout(?![A-Za-z])", "அவர்", text)


def markdown_for_page(page_dir: Path, image_dir: Path, out_dir: Path, args: argparse.Namespace) -> tuple[str, int]:
    relative = page_dir.relative_to(image_dir)
    image_paths = sorted(page_dir.glob("*.png"), key=lambda path: path.name.lower())
    if args.max_images_per_page:
        image_paths = image_paths[: args.max_images_per_page]

    lines = [
        f"# {relative.as_posix()}",
        "",
        f"- Source image folder: `{page_dir}`",
        f"- OCR language: `{args.lang}`",
        f"- Tesseract page segmentation mode: `{args.psm}`",
        f"- OCR cleanup: `{'disabled' if args.no_cleanup else 'enabled'}`",
        "",
    ]

    text_count = 0
    for index, image_path in enumerate(image_paths, start=1):
        text, stderr = run_tesseract(image_path, args)
        text = cleanup_ocr_text(text, args)
        rel_image = image_path.relative_to(image_dir).as_posix()
        lines.extend(
            [
                f"## Image {index}: {image_path.name}",
                "",
                f"- Image: `{rel_image}`",
                "",
            ]
        )
        if text:
            text_count += len(text)
            lines.extend([text, ""])
        else:
            lines.extend(["_No OCR text detected._", ""])
        if args.include_tesseract_notes and stderr:
            lines.extend(["```text", stderr, "```", ""])

    return "\n".join(lines).rstrip() + "\n", text_count


def write_page_ocr(page_dir: Path, image_dir: Path, out_dir: Path, args: argparse.Namespace) -> dict[str, object]:
    output_path = page_output_path(page_dir, image_dir, out_dir)
    relative = page_dir.relative_to(image_dir).as_posix()
    if output_path.exists() and not args.force:
        return {
            "status": "skipped_existing",
            "page": relative,
            "output": str(output_path),
            "at": now_iso(),
        }

    text, text_count = markdown_for_page(page_dir, image_dir, out_dir, args)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    temp_path.write_text(text, encoding="utf-8")
    temp_path.replace(output_path)
    return {
        "status": "done",
        "page": relative,
        "output": str(output_path),
        "characters": text_count,
        "images": len(list(page_dir.glob("*.png"))),
        "at": now_iso(),
    }


def write_summary(out_dir: Path, records: list[dict[str, object]], failures: list[dict[str, object]]) -> None:
    lines = [
        "# OCR Text Extraction Summary",
        "",
        f"- Generated: {now_iso()}",
        f"- Markdown files written this run: {sum(1 for item in records if item.get('status') == 'done')}",
        f"- Existing files skipped this run: {sum(1 for item in records if item.get('status') == 'skipped_existing')}",
        f"- Failures this run: {len(failures)}",
        "",
        "## Outputs",
        "",
    ]
    written = [item for item in records if item.get("status") == "done"]
    if written:
        for item in written:
            lines.append(f"- `{item.get('output')}`")
            lines.append(f"  Page: `{item.get('page')}`")
    else:
        lines.append("None written this run.")

    lines.extend(["", "## Failures", ""])
    if failures:
        for item in failures:
            lines.append(f"- `{item.get('page', '')}`")
            lines.append(f"  Error: {item.get('error', 'unknown error')}")
    else:
        lines.append("None.")

    (out_dir / "_state").mkdir(parents=True, exist_ok=True)
    (out_dir / "_state" / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run OCR on downloaded page images and write Markdown text.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR, help="Folder containing OCR-ready images.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Folder where OCR Markdown files are written.")
    parser.add_argument("--lang", default="tam", help="Tesseract language code.")
    parser.add_argument("--psm", type=int, default=3, help="Tesseract page segmentation mode.")
    parser.add_argument("--oem", type=int, default=1, help="Tesseract OCR engine mode.")
    parser.add_argument("--tesseract", default="tesseract", help="Tesseract command path.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout per image, in seconds.")
    parser.add_argument("--limit-pages", type=int, default=0, help="Only process the first N page folders; 0 means no limit.")
    parser.add_argument("--max-images-per-page", type=int, default=0, help="Only OCR the first N images in each page folder; 0 means all.")
    parser.add_argument("--page", action="append", default=[], help="Only process page folders whose path contains this text. Can be repeated.")
    parser.add_argument("--force", action="store_true", help="Run OCR again even if the Markdown output already exists.")
    parser.add_argument("--quiet", action="store_true", help="Print only failures and final summary.")
    parser.add_argument("--include-tesseract-notes", action="store_true", help="Include Tesseract stderr notes in the Markdown output.")
    parser.add_argument(
        "--normalize-images",
        action="store_true",
        help="Re-encode images before OCR; useful for readable PNGs that Tesseract treats as blank.",
    )
    parser.add_argument("--no-cleanup", action="store_true", help="Disable small Tamil OCR cleanup replacements.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.image_dir = args.image_dir.resolve()
    args.out_dir = args.out_dir.resolve()

    if not args.image_dir.exists():
        print(f"Image folder not found: {args.image_dir}", file=sys.stderr)
        return 2
    if shutil.which(args.tesseract) is None:
        print(f"Tesseract command not found: {args.tesseract}", file=sys.stderr)
        return 2

    page_dirs = find_page_dirs(args.image_dir)
    page_dirs = filter_page_dirs(page_dirs, args.image_dir, args.page)
    if args.limit_pages:
        page_dirs = page_dirs[: args.limit_pages]

    manifest_path = args.out_dir / "_state" / "manifest.jsonl"
    records: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []

    print(f"Image folder: {args.image_dir}", flush=True)
    print(f"OCR text folder: {args.out_dir}", flush=True)
    print(f"Page folders to OCR: {len(page_dirs)}", flush=True)

    try:
        for index, page_dir in enumerate(page_dirs, start=1):
            relative = page_dir.relative_to(args.image_dir).as_posix()
            if not args.quiet:
                print(f"[{index}/{len(page_dirs)}] {relative}", flush=True)
            try:
                record = write_page_ocr(page_dir, args.image_dir, args.out_dir, args)
                records.append(record)
                append_manifest(manifest_path, record)
                if not args.quiet and record["status"] == "done":
                    print(f"wrote: {record['output']}", flush=True)
                elif not args.quiet and record["status"] == "skipped_existing":
                    print(f"skip existing: {record['output']}", flush=True)
            except Exception as exc:  # noqa: BLE001 - CLI records and continues.
                failure = {
                    "status": "failed",
                    "page": relative,
                    "error": f"{type(exc).__name__}: {exc}",
                    "at": now_iso(),
                }
                failures.append(failure)
                append_manifest(manifest_path, failure)
                print(f"failed: {relative} ({failure['error']})", file=sys.stderr, flush=True)
    except KeyboardInterrupt:
        print("\nStopped by user. Progress is saved; run the same command to resume.", file=sys.stderr, flush=True)
        write_summary(args.out_dir, records, failures)
        return 130

    write_summary(args.out_dir, records, failures)
    print("\nFinished.", flush=True)
    print(f"Markdown files written this run: {sum(1 for item in records if item.get('status') == 'done')}", flush=True)
    print(f"Existing files skipped this run: {sum(1 for item in records if item.get('status') == 'skipped_existing')}", flush=True)
    print(f"Failures this run: {len(failures)}", flush=True)
    print(f"Summary: {args.out_dir / '_state' / 'summary.md'}", flush=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
