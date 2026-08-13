#!/usr/bin/env python3
"""Tests for parallel English transcript extraction."""

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("build_parallel_source_translation.py")
SPEC = importlib.util.spec_from_file_location("build_parallel_source_translation", MODULE_PATH)


class ParagraphizeTest(unittest.TestCase):
    def test_each_extracted_html_line_becomes_a_paragraph(self):
        module = importlib.util.module_from_spec(SPEC)
        assert SPEC.loader
        SPEC.loader.exec_module(module)
        self.assertEqual(module.paragraphize(" First paragraph. \n\nSecond paragraph.\n"), "First paragraph.\n\nSecond paragraph.")


if __name__ == "__main__":
    unittest.main()
