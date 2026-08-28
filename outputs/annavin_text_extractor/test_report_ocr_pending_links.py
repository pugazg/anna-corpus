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


if __name__ == "__main__":
    unittest.main()
