#!/usr/bin/env python3
"""First-edition 1647 unnumbered Moon-to-fixed-stars authentic page witness."""

import hashlib
import json
import os
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BEFORE = B.parent / "B07u"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
ORIGINAL = Path(os.environ["LILLY_1647_SOURCE_PDF"])
RENDER = Path(os.environ["LILLY_1647_RENDER_DIR"])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


assert not (B / "ORIGINAL_SOURCE_WINDOW_V1.json").exists()
parent = j(BEFORE / "ORIGINAL_SOURCE_WINDOW_V1.json")
idx = j(INDEX)
assert idx["batches"][-1]["id"] == "B07u"
assert idx["records_count"] == 12168
assert idx["next"]["chapter"] == "UNNUMBERED_MOON_FIXED_STARRES"
assert idx["next"]["pdf_page"] == 735
assert idx["next"]["printed_chapter_numeral"] is None
assert parent["following_heading_numbered"] is False
assert parent["following_heading_original_pdf"] == 735
assert j(CHINA)["sum_source_annotations"] == 97
assert ORIGINAL.stat().st_size == 141842963
assert sha(ORIGINAL) == parent["full_source_pdf_sha256"]
(B / "evidence").mkdir(exist_ok=True)
images = {}
for page in (735, 736, 737, 738):
    if page <= 736:
        original = BEFORE / "evidence" / f"pdf_1647-{page}.jpg"
        witness = parent["photos"][str(page)]
        assert sha(original) == witness["sha256"]
        assert original.stat().st_size == witness["bytes"]
        method = "ORIGINAL_B07u_SHA_LOCKED_JPEG_RENDER"
    else:
        original = RENDER / f"page-{page}.jpg"
        method = "FIRST_EDITION_IMMUTABLE_PDF_POPPLER_SCALE_TO_1600_JPEG_Q93"
    target = B / "evidence" / f"pdf_1647-{page}.jpg"
    assert original.is_file()
    if not target.exists():
        shutil.copyfile(original, target)
    assert target.read_bytes() == original.read_bytes()
    images[str(page)] = {
        "file": str(target.relative_to(B)),
        "original_pdf_frame": page,
        "printed_page": page - 34,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "source_method": method,
        "scope": (
            "MOON_FIXED_STARRES_AND_PRECEDING_HOUSE_END"
            if page == 735
            else "MOON_FIXED_STARRES_BODY"
            if page == 736
            else "MOON_FIXED_STARRES_AND_NEXT_CLXV_HEADING"
            if page == 737
            else "CLXV_NEXT_CHAPTER_CONTEXT_ONLY"
        ),
    }
window = {
    "schema": "LILLY_1647_UNNUMBERED_MOON_FIXED_STARS_WINDOW_V1",
    "batch": "B07v",
    "source": "William Lilly Christian Astrology first edition 1647 Wellcome b30338724",
    "original_full_pdf_sha256": sha(ORIGINAL),
    "original_full_pdf_bytes": ORIGINAL.stat().st_size,
    "prior_lilly_records": idx["records_count"],
    "prior_ptolemy_records": 1066,
    "independent_chinese_historical_count": 97,
    "prior_canonical_index_sha256": sha(INDEX),
    "first_new_historical_record": "R12169",
    "unnumbered_heading": "The Moon Directed to FIXED STARRES",
    "unnumbered_heading_original_pdf": 735,
    "body_original_pdf_frames": [735, 736, 737],
    "following_printed_numbered_chapter": "CLXV",
    "following_heading": "The Directions of the PART OF FORTUNE",
    "following_printed_heading_original_pdf": 737,
    "following_printed_heading_page": 703,
    "following_context_frame": 738,
    "source_seam_note": (
        "The last Moon/Hercules historical effect is ABOVE an explicit "
        "printed CHAP CLXV horizontal divider on original PDF737/printed703; "
        "Part of Fortune direction paragraphs begin BELOW that divider."
    ),
    "source_is_numbered_chapter": False,
    "numbered_chapter_delta_on_acceptance": 0,
    "source_only": True,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "photos": images,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(window, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(
    "B07v witness prepared",
    len(images),
    "original photos; unnumbered PDF735-737, CLXV begins PDF737",
)
