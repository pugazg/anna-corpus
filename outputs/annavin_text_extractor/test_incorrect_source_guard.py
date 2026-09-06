#!/usr/bin/env python3
"""Regression tests for corrupt-source holds and evidence-backed recovery."""

import csv
import subprocess
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parent
STATE = BASE / "translated_contents" / "_translation_state"


class IncorrectSourceGuardTest(unittest.TestCase):
    def test_pazhaya_company_recovered_and_unrelated_fragment_preserved(self):
        with (STATE / "incorrect_sources.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        self.assertNotIn("katturaigal/pazhaya_company.md", rows)
        self.assertEqual(rows["katturaigal/singam_sirunari_1.md"]["status"], "incorrect_source")
        self.assertEqual(rows["katturaigal/singam_sirunari_2.md"]["status"], "incorrect_source")
        evidence = STATE / "working/pazhaya_company_evidence"
        original = (evidence / "original_mixed_corrected_ocr.md").read_text()
        fragment = (evidence / "roosevelt_unrelated_fragment.md").read_text()
        self.assertEqual(fragment.split("\n\n", 2)[2], original[original.index("## Image 2:"):])
        source = (BASE / "ocr_text_corrected/katturaigal/pazhaya_company.md").read_text()
        self.assertIn("### Column 1", source)
        self.assertIn("### Column 2", source)
        self.assertIn("பைசல்செய்துகொள்வோம்.", source)
        self.assertNotIn("## Image 2:", source)
        self.assertNotIn("ரூஸ்வெல்ட்", source)
        self.assertTrue((evidence / "rmrl-viewer-page-9.png").is_file())


    def test_queue_releases_recovered_article_and_preserves_other_holds(self):
        subprocess.run(
            ["python3", str(BASE / "prepare_translation_queue.py"), "--inspect-content"],
            check=True,
            capture_output=True,
            text=True,
        )
        with (STATE / "translation_queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["file"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["katturaigal/pazhaya_company.md"]["status"], "translated")
        self.assertEqual(rows["katturaigal/pazhaya_company.md"]["direction"], "complete")
        self.assertEqual(rows["katturaigal/singam_sirunari_1.md"]["status"], "incorrect_source")

    def test_contents_distinguishes_recovered_and_incorrect_sources(self):
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
        self.assertIn(" - translated", line)
        held = next(line for line in contents.splitlines() if "singam_sirunari_1.md" in line)
        self.assertIn("incorrect source - skipped", held)

    def test_permanent_incorrect_sources_are_not_recovery_candidates(self):
        with (STATE / "incorrect_sources.csv").open(encoding="utf-8-sig", newline="") as handle:
            incorrect = {row["file"] for row in csv.DictReader(handle)}
        with (STATE / "needs_source_recovery.csv").open(encoding="utf-8-sig", newline="") as handle:
            recovery = {row["file"] for row in csv.DictReader(handle)}
        self.assertTrue(incorrect.isdisjoint(recovery))

    def test_queue_preserves_recorded_holds_and_releases_recovered_work(self):
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
        recovered_transition = rows["katturaigal/ilamayil_muthumai.md"]
        self.assertEqual(recovered_transition["status"], "translated")
        self.assertEqual(recovered_transition["direction"], "complete")
        source = (
            BASE / "ocr_text_corrected/katturaigal/ilamayil_muthumai.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Image 4:", source)
        self.assertIn("## Image 7:", source)
        self.assertNotIn("## Image 5:", source)
        self.assertNotIn("## Image 6:", source)
        self.assertLess(source.index("## Image 4:"), source.index("## Image 7:"))

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
                "--file", "katturaigal/singam_sirunari_1.md", "--dry-run",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("skip incorrect source: katturaigal/singam_sirunari_1.md", result.stdout)
        self.assertEqual(recovery.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
