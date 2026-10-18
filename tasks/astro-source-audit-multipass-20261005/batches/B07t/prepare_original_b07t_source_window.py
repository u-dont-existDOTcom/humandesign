#!/usr/bin/env python3
"""Verify and preserve 1647 original Lilly printed CLXIII photographs and exact seams."""

import hashlib
import json
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07s"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def j(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert not (B / "ORIGINAL_SOURCE_WINDOW_V1.json").exists()
before = j(INDEX)
parent = j(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert before["records_count"] == 11721
assert before["next"]["chapter"] == "CLXIII"
assert before["next"]["pdf_page"] == 723
assert before["batches"][-1]["id"] == "B07s"
assert parent["following_printed_clxiii"]["starts_frame"] == 723
assert parent["following_printed_clxiii"]["ends_frame"] == 725
assert j(CHINA)["sum_source_annotations"] == 97

photos = {}
(B / "evidence").mkdir(exist_ok=True)
for page in (723, 724, 725):
    src = PARENT / "evidence" / f"pdf_1647-{page}.jpg"
    prior = parent["photos"][str(page)]
    assert src.stat().st_size == prior["bytes"] and sha(src) == prior["sha256"]
    target = B / "evidence" / src.name
    if not target.exists():
        shutil.copyfile(src, target)
    assert target.read_bytes() == src.read_bytes()
    photos[str(page)] = {
        "file": str(target.relative_to(B)),
        "original_pdf_frame": page,
        "printed_page": page - 34,
        "sha256": sha(target),
        "bytes": target.stat().st_size,
        "role": (
            "prior_CLXII_before_divider_CLXIII_after"
            if page == 723
            else "CLXIII_body"
            if page == 724
            else "CLXIII_before_divider_next_CLXIIII_after"
        ),
    }
window = {
    "schema": "LILLY_1647_CLXIII_SOURCE_WINDOW_V1",
    "batch": "B07t",
    "source": "Original 1647 Lilly Christian Astrology, Wellcome b30338724",
    "full_source_894_frame_pdf_sha256": parent["original_pdf_sha256"],
    "full_source_pdf_bytes": parent["original_pdf_bytes"],
    "photo_origin": "Original PDF Poppler JPEG renders inherited byte-exact from B07s",
    "parent_accepted_lilly": 11721,
    "parent_lilly_index_sha256": sha(INDEX),
    "parent_ptolemy": 1066,
    "separate_chinese_v2": 97,
    "next_historical_id": "R11722",
    "body_original_pdf_frames": [723, 724, 725],
    "first_original_pdf": 723,
    "last_original_pdf": 725,
    "first_printed_page": 689,
    "last_printed_page": 691,
    "printed_chapter": "CLXIII",
    "heading": "The Sunne Directed to FIXED STARRES",
    "next_chapter": "CLXIIII",
    "next_heading": "Directions of the Moon to Promittors",
    "next_heading_pdf": 725,
    "original_star_epoch_and_modern_identity_parity_verified": False,
    "original_direction_arc_to_date_engine_verified": False,
    "independent_real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "photos": photos,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(window, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Window: {len(photos)} authentic first-edition images; 723-725; next R11722")
