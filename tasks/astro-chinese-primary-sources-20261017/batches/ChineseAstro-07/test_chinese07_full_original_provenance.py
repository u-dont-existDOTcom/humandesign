"""Independent full original raw-volume SHA and extract-span verification."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
EXPECTED = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"


def sha(x):
    return hashlib.sha256(x).hexdigest()


class WholeOriginalVolume(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (B / "SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt").read_bytes()
        cls.text = cls.source.decode("utf-8")
        cls.notes = json.loads(
            (B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json").read_text()
        )
        cls.witness = json.loads(
            (B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json").read_text()
        )

    def test_full_original_pinned_revision_not_only_excerpt(self):
        self.assertEqual(len(self.source), 106736)
        self.assertEqual(sha(self.source), EXPECTED)
        self.assertEqual(self.notes["pinned_original_volume2_full_raw_SHA256"], EXPECTED)

    def test_cut_exact_full_volume_to_excerpt_provenance(self):
        start = self.notes["original_text_segment_absolute_start_codepoint"]
        end = self.notes["original_text_segment_absolute_end_codepoint"]
        excerpt = (B / "SOURCE_1963110_AUXILIARY_AND_BUREAU_EXCERPT.txt").read_text()
        self.assertEqual(self.text[start:end], excerpt)
        self.assertEqual(sha(excerpt.encode()), self.notes["full_original_excerpt_SHA256"])

    def test_reconstructed_each_grid_exact_original_chinese(self):
        for x in self.witness["diagram_reversible_witnesses"]:
            snippet = self.text[x["original_codepoint_start"] : x["original_codepoint_end"]]
            self.assertEqual(snippet, x["diagram_content"])
            self.assertEqual(sha(snippet.encode()), x["original_utf8_sha256"])
            self.assertGreater(len(snippet), 400)


if __name__ == "__main__":
    unittest.main()
