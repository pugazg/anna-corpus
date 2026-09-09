#!/usr/bin/env python3
"""Focused tests for OCR completeness detection in the bilingual audit."""

import unittest
import csv
import subprocess
import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("audit_bilingual_translations.py")
SPEC = importlib.util.spec_from_file_location("audit_bilingual_translations", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)
blank_ocr_pages = MODULE.blank_ocr_pages


class BlankOcrPagesTest(unittest.TestCase):
    def test_counts_empty_and_explicit_sections(self):
        source = """## Image 1: one.png
- Image: `one.png`

## Image 2: two.png
- Image: `two.png`
_No OCR text detected._

## Image 3: three.png
- Image: `three.png`
Recovered text
"""
        self.assertEqual(blank_ocr_pages(source), 2)

    def test_marker_with_ocr_noise_is_still_blank(self):
        source = """## Image 1: one.png
- Image: `one.png`
123
_No OCR text detected._
"""
        self.assertEqual(blank_ocr_pages(source), 1)

    def test_counts_blank_pages_under_nested_headings(self):
        source = """### Image 1: one.png
- Image: `one.png`
_No OCR text detected._

### Image 2: two.png
- Image: `two.png`
Recovered text
"""
        self.assertEqual(blank_ocr_pages(source), 1)

    def test_manual_recovery_hold_is_reported(self):
        subprocess.run(["python3", str(MODULE_PATH)], check=True, capture_output=True, text=True)
        report = MODULE.REPORT.read_text(encoding="utf-8")
        self.assertIn("### Manually Verified Recovery Holds", report)
        holds_path = MODULE_PATH.parent / "translated_contents/_translation_state/needs_source_recovery.csv"
        with holds_path.open(encoding="utf-8", newline="") as handle:
            holds = list(csv.DictReader(handle))
        for hold in holds:
            with self.subTest(source_file=hold["file"]):
                self.assertIn(f"`{hold['file']}`", report)


if __name__ == "__main__":
    unittest.main()
