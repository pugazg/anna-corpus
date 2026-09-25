import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("report_ocr_pending_links.py")
SPEC = importlib.util.spec_from_file_location("report_ocr_pending_links", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BlankOcrMarkerTests(unittest.TestCase):
    def test_reclassified_work_retains_original_multipart_urls(self):
        pages = {
            "katturaigal/romapuri_ranigal_1": ["https://example.org/part1"],
            "katturaigal/romapuri_ranigal_2": ["https://example.org/part2"],
            "katturaigal/other": ["https://example.org/other"],
        }
        self.assertEqual(
            MODULE.urls_for("nadagangal/romapuri_ranigal.md", pages),
            ["https://example.org/part1", "https://example.org/part2"],
        )

    def test_no_ocr_text_detected_marker_requires_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text("## Image 1\n\n_No OCR text detected._\n", encoding="utf-8")
            self.assertTrue(MODULE.has_blank_page_marker(source))

    def test_normal_ocr_body_is_translation_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text("## Image 1\n\nமுழுமையான உரை\n", encoding="utf-8")
            self.assertFalse(MODULE.has_blank_page_marker(source))

    def test_incorrect_sources_supply_recovery_reasons(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "incorrect_sources.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["file", "reason"])
                writer.writeheader()
                writer.writerow({"file": "katturaigal/broken.md", "reason": "Wrong scans"})
            original = MODULE.INCORRECT
            try:
                MODULE.INCORRECT = path
                self.assertEqual(
                    MODULE.load_incorrect_sources(),
                    {"katturaigal/broken.md": "Wrong scans"},
                )
            finally:
                MODULE.INCORRECT = original


if __name__ == "__main__":
    unittest.main()
