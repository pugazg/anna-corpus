#!/usr/bin/env python3
"""Make both titles visible in the H1 of every translated poem."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "translated_contents/kavithaigal"


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        tamil = re.search(r"^\*\*Tamil title:\*\*\s*(.+?)\s{2,}$", text, re.M)
        english = re.search(r"^\*\*English title:\*\*\s*(.+?)\s{2,}$", text, re.M)
        if not tamil or not english:
            raise ValueError(f"Missing title metadata: {path}")
        heading = f"# {tamil.group(1).strip()} / {english.group(1).strip()}"
        updated = re.sub(r"^# .+$", heading, text, count=1, flags=re.M)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Updated bilingual headings: {changed}")


if __name__ == "__main__":
    main()
