#!/usr/bin/env python3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "organized_contents"
OUTPUT = BASE / "translated_contents"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_reverse_translation.py SOURCE_RELATIVE_PATH DRAFT_PATH")
    relative = Path(sys.argv[1])
    source = SOURCE / relative
    draft = Path(sys.argv[2])
    raw = source.read_text(encoding="utf-8")
    translated = draft.read_text(encoding="utf-8").strip()
    notes = ""
    if "\n---NOTES---\n" in translated:
        translated, notes = translated.split("\n---NOTES---\n", 1)
    title = translated.splitlines()[0].removeprefix("# ").strip()
    result = [
        f"# {title}", "",
        "## Source English (verbatim)", "", raw.strip(), "",
        "## Tamil Translation", "", translated.strip(), "",
    ]
    if notes.strip():
        result.extend(["## Translator Notes", "", notes.strip(), ""])
    target = OUTPUT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(result), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
