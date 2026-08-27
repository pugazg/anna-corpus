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

    def test_contents_marks_pazhaya_company_incorrect(self):
        subprocess.run(
            ["python3", str(BASE / "generate_section_contents.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        contents = (BASE / "translated_contents/katturaigal/CONTENTS.md").read_text(
            encoding="utf-8"
        )
        line = next(line for line in contents.splitlines() if "pazhaya_company.md" in line)
        self.assertIn("incorrect source - skipped", line)

    def test_permanent_incorrect_sources_are_not_recovery_candidates(self):
        with (STATE / "incorrect_sources.csv").open(encoding="utf-8-sig", newline="") as handle:
            incorrect = {row["file"] for row in csv.DictReader(handle)}
        with (STATE / "needs_source_recovery.csv").open(encoding="utf-8-sig", newline="") as handle:
            recovery = {row["file"] for row in csv.DictReader(handle)}
        self.assertTrue(incorrect.isdisjoint(recovery))

    def test_queue_preserves_recorded_recovery_holds(self):
        subprocess.run(
            ["python3", str(BASE / "prepare_translation_queue.py"), "--inspect-content"],
            check=True,
            capture_output=True,
            text=True,
        )
        with (STATE / "translation_queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        row = rows["sorpozhivugal/sudhanthira_kaiyelu.md"]
        self.assertEqual(row["status"], "needs_source_recovery")
        self.assertEqual(row["direction"], "none")
        missing_transition = rows["katturaigal/ilamayil_muthumai.md"]
        self.assertEqual(missing_transition["status"], "needs_source_recovery")
        self.assertEqual(missing_transition["direction"], "none")
        self.assertIn("Images 4 and 5", missing_transition["reason"])

    def test_queue_holds_unrecovered_ocr_works_with_blank_image_sections(self):
        subprocess.run(
            ["python3", str(BASE / "prepare_translation_queue.py"), "--inspect-content"],
            check=True,
            capture_output=True,
            text=True,
        )
        with (STATE / "translation_queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        row = rows["nadagangal/bankak_bankaja_1.md"]
        self.assertEqual(row["status"], "translated")
        recovered_source = (
            BASE / "ocr_text_corrected/nadagangal/bankak_bankaja_1.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("_No OCR text detected._", recovered_source)
        late_blank = rows["sorpozhivugal/150767.md"]
        self.assertEqual(late_blank["status"], "needs_source_recovery")
        self.assertIn("1 blank image section(s)", late_blank["reason"])
        recovered = rows["nadagangal/vazhakku_vapas_1.md"]
        self.assertEqual(recovered["status"], "translated")
        recovered_pending = rows["nadagangal/popular_store_1.md"]
        self.assertEqual(recovered_pending["status"], "translated")
        newly_recovered = rows["nadagangal/irakkam_oru_1.md"]
        self.assertEqual(newly_recovered["status"], "translated")

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
