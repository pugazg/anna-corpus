#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE_MAP = BASE / "organized_contents/_merge_state/source_map.csv"
OUTPUT = BASE / "translated_contents"
INCORRECT_SOURCES = OUTPUT / "_translation_state/incorrect_sources.csv"

SECTION_TITLES = {
    "english": "English / ஆங்கிலம்",
    "kadithangal": "கடிதங்கள் / Letters",
    "katturaigal": "கட்டுரைகள் / Articles",
    "kavithaigal": "கவிதைகள் / Poems",
    "Kurunavalgal": "குறுநாவல்கள் / Novellas",
    "nadagangal": "நாடகங்கள் / Plays",
    "navalgal": "நாவல்கள் / Novels",
    "oviyam": "ஓவியம் / Artwork",
    "paettigal": "பேட்டிகள் / Interviews",
    "photos": "புகைப்படங்கள் / Photographs",
    "sirukathaigal": "சிறுகதைகள் / Short Stories",
    "sorpozhivugal": "சொற்பொழிவுகள் / Speeches",
}


def display_title(path: Path) -> str:
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return path.stem.replace("_", " ")


def load_incorrect_sources() -> set[str]:
    if not INCORRECT_SOURCES.exists():
        return set()
    with INCORRECT_SOURCES.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["file"]
            for row in csv.DictReader(handle)
            if row.get("status") == "incorrect_source"
        }


def main() -> None:
    grouped = defaultdict(list)
    incorrect_sources = load_incorrect_sources()
    with SOURCE_MAP.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["section"]].append(row)

    for section, title in SECTION_TITLES.items():
        rows = sorted(grouped.get(section, []), key=lambda row: row["file"].lower())
        folder = OUTPUT / section
        folder.mkdir(parents=True, exist_ok=True)
        lines = [f"# {title}", "", f"Total source works: {len(rows)}", ""]
        for row in rows:
            rel = Path(row["file"])
            source = BASE / "organized_contents" / rel
            label = display_title(source)
            target = rel.name
            if rel.as_posix() in incorrect_sources:
                mark = "incorrect source - skipped"
            else:
                mark = "translated" if (folder / target).exists() else "pending"
            lines.append(f"- [{label}]({target}) - {mark}")
        (folder / "CONTENTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
