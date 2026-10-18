#!/usr/bin/env python3
"""Original Lilly 1647 printed CLXV Part of Fortune first-edition source window."""

import hashlib
import json
import os
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07v"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
PDF = Path(os.environ["LILLY_1647_SOURCE_PDF"])
RENDER = Path(os.environ["LILLY_1647_RENDER_DIR"])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


assert not (B / "ORIGINAL_SOURCE_WINDOW_V1.json").exists()
idx = load(INDEX)
before = load(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert idx["records_count"] == 12268
assert idx["next"]["chapter"] == idx["next"]["printed_chapter_numeral"] == "CLXV"
assert idx["next"]["pdf_page"] == 737
assert idx["batches"][-1]["id"] == "B07v"
assert before["following_printed_numbered_chapter"] == "CLXV"
assert before["following_printed_heading_original_pdf"] == 737
assert load(CHINA)["sum_source_annotations"] == 97
assert PDF.stat().st_size == 141842963
assert sha(PDF) == before["original_full_pdf_sha256"]

(B / "evidence").mkdir(exist_ok=True)
images = {}
for n in range(737, 744):
    if n <= 738:
        original = PARENT / "evidence" / f"pdf_1647-{n}.jpg"
        witness = before["photos"][str(n)]
        assert original.stat().st_size == witness["bytes"]
        assert sha(original) == witness["sha256"]
        provenance = "EXACT_PRIOR_B07v_ORIGINAL_PDF_PHOTO"
    else:
        original = RENDER / f"page-{n}.jpg"
        provenance = "SHA_LOCKED_FIRST_EDITION_PDF_POPPLER_SCALE_TO_1600_JPEG_Q93"
    assert original.is_file(), original
    dest = B / "evidence" / f"pdf_1647-{n}.jpg"
    if not dest.exists():
        shutil.copyfile(original, dest)
    assert dest.read_bytes() == original.read_bytes()
    images[str(n)] = {
        "file": str(dest.relative_to(B)),
        "original_pdf_frame": n,
        "printed_page": n - 34,
        "bytes": dest.stat().st_size,
        "sha256": sha(dest),
        "raster_source": provenance,
        "source_section": (
            "CLXV_BEGINS_BELOW_B07v_DIVIDER"
            if n == 737
            else "CLXV_FINISHES_ABOVE_PRINTED_CLXVI_DIVIDER"
            if n == 742
            else "CLXVI_NUMERIC_METHODS_CONTEXT_ONLY"
            if n == 743
            else "CLXV_PART_FORTUNE_BODY"
        ),
    }

data = {
    "schema": "LILLY_1647_CLXV_FIRST_EDITION_SOURCE_WINDOW_V1",
    "batch": "B07w",
    "source": "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724",
    "full_pdf_original_sha256": sha(PDF),
    "full_pdf_original_bytes": PDF.stat().st_size,
    "parent_accepted_lilly": 12268,
    "parent_ptolemy_records": 1066,
    "parallel_chinese_v2_source_notes": 97,
    "parent_index_sha256": sha(INDEX),
    "first_new_historical_record": "R12269",
    "heading": "CHAP CLXV The Directions of the PART OF FORTUNE",
    "printed_numeral": "CLXV",
    "starts_pdf": 737,
    "starts_printed": 703,
    "body_pdf_frames": list(range(737, 743)),
    "ends_pdf": 742,
    "ends_printed": 708,
    "following_chapter": "CLXVI",
    "following_heading": "Of the measure of time in DIRECTIONS",
    "following_heading_pdf": 742,
    "following_heading_printed": 708,
    "next_context_pdf": 743,
    "source_seam": (
        "PDF737 CLXV begins below Moon-star divider; PDF742 ends with "
        "Part Fortune twelfth house above distinct CLXVI divider. "
        "New CLXVI numerical instructions begin below."
    ),
    "following_clxvi_is_numerical_core": True,
    "source_only": True,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "photos": images,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("B07w original CLXV source window PDF737-742, seven authenticated first-edition page images")
