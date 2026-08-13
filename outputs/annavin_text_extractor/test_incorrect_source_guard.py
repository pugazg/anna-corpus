#!/usr/bin/env python3
"""Regression tests for permanently excluded corrupt source sequences."""

import csv
import subprocess
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parent
STATE = BASE / "translated_contents" / "_translation_state"


class IncorrectSourceGuardTest(unittest.TestCase):
    def test_pazhaya_company_is_permanently_marked_incorrect(self):
        with (STATE / "incorrect_sources.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["katturaigal/pazhaya_company.md"]["status"], "incorrect_source")
        self.assertEqual(rows["katturaigal/singam_sirunari_1.md"]["status"], "incorrect_source")
        self.assertEqual(rows["katturaigal/singam_sirunari_2.md"]["status"], "incorrect_source")

    def test_queue_never_marks_pazhaya_company_ready(self):
        subprocess.run(
            ["python3", str(BASE / "prepare_translation_queue.py"), "--inspect-content"],
            check=True,
            capture_output=True,
            text=True,
        )
        with (STATE / "translation_queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["katturaigal/pazhaya_company.md"]["status"], "incorrect_source")
        self.assertEqual(rows["katturaigal/pazhaya_company.md"]["direction"], "none")

    def test_batch_dry_run_skips_without_rewriting_recovery_state(self):
        recovery = STATE / "needs_source_recovery.csv"
        before = recovery.read_bytes()
        result = subprocess.run(
            [
                "python3", str(BASE / "translate_all_markdown.py"),
                "--file", "katturaigal/pazhaya_company.md", "--dry-run",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("skip incorrect source: katturaigal/pazhaya_company.md", result.stdout)
        self.assertEqual(recovery.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
