#!/usr/bin/env python3
"""Turn the latest image-extraction summary into durable fidelity reports."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUMMARY = ROOT / "ocr_images" / "_state" / "summary.md"
STATE = ROOT / "translated_contents" / "_translation_state"
DECORATIVE_URLS = {"http://www.annavinpadaippugal.info/images/anna_mic.jpg"}


def corrected_source_candidates(relative: Path) -> list[Path]:
    page_rel = relative.parent.with_suffix(".md")
    candidates = [ROOT / "ocr_text_corrected" / page_rel]
    canonical_stem = re.sub(r"_[0-9]+$", "", page_rel.stem)
    if canonical_stem != page_rel.stem:
        candidates.append(ROOT / "ocr_text_corrected" / page_rel.with_name(canonical_stem + ".md"))
    return candidates


def main() -> int:
    text = SUMMARY.read_text(encoding="utf-8")
    image_block, failure_block = text.split("## Failures", 1)
    images = re.findall(
        r"^- `([^`]+)`\n  Page: <([^>]+)>\n  Source image: <([^>]+)>",
        image_block,
        re.M,
    )
    failures = re.findall(r"^- <([^>]+)>\n  Error: (.+)$", failure_block, re.M)

    content_images = [item for item in images if item[2] not in DECORATIVE_URLS]
    decorative_images = [item for item in images if item[2] in DECORATIVE_URLS]
    recovered = [
        "# Recovered Missing Scans",
        "",
        "These images were newly downloaded by the scan-completeness recovery pass after lowering the old 300 px minimum-height filter. Each must be OCR-checked before a previously translated document is considered scan-complete.",
        "",
        f"- Recovered content images: {len(content_images)}",
        f"- Ignored decorative images: {len(decorative_images)}",
        "",
    ]
    for path_text, page_url, image_url in content_images:
        path = Path(path_text)
        relative = path.relative_to(ROOT / "ocr_images")
        candidates = corrected_source_candidates(relative)
        represented = any(
            source.exists() and path.name in source.read_text(encoding="utf-8", errors="replace")
            for source in candidates
        )
        recovered.extend(
            [
                f"## `{relative.as_posix()}`",
                "",
                f"- Page: <{page_url}>",
                f"- Source image: <{image_url}>",
                f"- Corrected Tamil source: `{'represented' if represented else 'missing or not yet incorporated'}`",
                "",
            ]
        )

    missing = [
        "# Website Content Image 404s",
        "",
        "These content-image URLs were linked by the website but returned HTTP 404 during the completed archive sweep. Decorative-image timeouts are excluded.",
        "",
    ]
    not_found = [(url, error) for url, error in failures if "404" in error]
    missing.extend([f"- 404 URLs: {len(not_found)}", ""])
    for url, _ in not_found:
        missing.append(f"- <{url}>")
    missing.append("")

    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "recovered_missing_scans.md").write_text("\n".join(recovered), encoding="utf-8")
    (STATE / "content_image_404s.md").write_text("\n".join(missing), encoding="utf-8")
    print(f"Recovered content images: {len(content_images)}")
    print(f"Ignored decorative images: {len(decorative_images)}")
    print(f"Content image 404s: {len(not_found)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
