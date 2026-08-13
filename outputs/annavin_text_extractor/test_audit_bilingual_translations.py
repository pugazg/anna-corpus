#!/usr/bin/env python3
"""Focused tests for OCR completeness detection in the bilingual audit."""

import unittest
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


if __name__ == "__main__":
    unittest.main()
