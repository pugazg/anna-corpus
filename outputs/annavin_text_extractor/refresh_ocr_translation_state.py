#!/usr/bin/env python3
"""Refresh all translation tracking artifacts after completing one work."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(script, *args):
    command = [sys.executable, str(ROOT / script), *args]
    print(f"\n==> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    run("prepare_translation_queue.py", "--inspect-content")
    run("generate_section_contents.py")
    run("audit_bilingual_translations.py")
    run("report_ocr_pending_links.py")
    print("\nTranslation state refreshed, including ocr_pending_links.md.")


if __name__ == "__main__":
    main()
