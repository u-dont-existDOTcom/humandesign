#!/usr/bin/env python3
"""Build exact first-edition printed CLXIIII Moon Promittors photographic source witness."""

import hashlib
import json
import os
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07t"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
RENDER = Path(os.environ["LILLY_1647_RENDER_DIR"])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


assert not (B / "ORIGINAL_SOURCE_WINDOW_V1.json").exists()
idx, old = j(INDEX), j(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert idx["records_count"] == 11825
assert idx["batches"][-1]["id"] == "B07t"
assert idx["next"]["chapter"] == "CLXIIII" and idx["next"]["pdf_page"] == 725
assert old["next_heading_pdf"] == 725
assert j(CHINA)["sum_source_annotations"] == 97

(B / "evidence").mkdir(exist_ok=True)
photos = {}
for n in range(725, 737):
    if n == 725:
        input_photo = PARENT / "evidence" / f"pdf_1647-{n}.jpg"
        prior = old["photos"][str(n)]
        assert input_photo.stat().st_size == prior["bytes"]
        assert sha(input_photo) == prior["sha256"]
        origin = "PARENT_B07t_EXACT_PRIOR_ORIGINAL_PDF_RENDER"
    else:
        input_photo = RENDER / f"page-{n}.jpg"
        origin = "IMMUTABLE_FIRST_EDITION_POPPLER_SCALE_TO_1600_JPEG_Q93"
    target = B / "evidence" / f"pdf_1647-{n}.jpg"
    assert input_photo.is_file(), input_photo
    if not target.exists():
        shutil.copyfile(input_photo, target)
    assert input_photo.read_bytes() == target.read_bytes()
    photos[str(n)] = {
        "file": str(target.relative_to(B)),
        "original_pdf_frame": n,
        "printed_folio": n - 34,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "raster_source": origin,
        "scope": (
            "CLXIIII_MOON_BODY_AFTER_CLXIII_DIVIDER"
            if n == 725
            else "CLXIIII_BODY_AND_UNNUMBERED_FIXED_STARS_HEADING"
            if n == 735
            else "UNNUMBERED_FIXED_STARS_CONTEXT_ONLY"
            if n == 736
            else "CLXIIII_MOON_PROMITTORS_BODY"
        ),
    }
window = {
    "schema": "LILLY_1647_CLXIIII_PHOTOGRAPHIC_SOURCE_WINDOW_V1",
    "batch": "B07u",
    "source": "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724",
    "full_source_pdf_sha256": old["full_source_894_frame_pdf_sha256"],
    "original_pdf_frame_count": 894,
    "accepted_lilly_before": 11825,
    "accepted_ptolemy": 1066,
    "accepted_chinese_v2": 97,
    "previous_index_sha256": sha(INDEX),
    "first_unaccepted_source_record": "R11826",
    "printed_numbered_heading": "CHAP CLXIIII Directions of the Moon to PROMITTORS",
    "starts_original_pdf": 725,
    "starts_printed_folio": 691,
    "body_frames": list(range(725, 736)),
    "ends_original_pdf": 735,
    "ends_printed_folio": 701,
    "following_unnumbered_headed_unit": "The Moon Directed to FIXED STARRES",
    "following_heading_original_pdf": 735,
    "following_context_pdf": 736,
    "following_heading_numbered": False,
    "boundary_note": (
        "The twelve Moon house-cusp directions end upper/middle PDF735, "
        "then a centered unnumbered 'Moon Directed to Fixed Starres' "
        "heading and Rigel passage begin BELOW on SAME scanned folio. "
        "Do not invent printed CHAP CLXV here."
    ),
    "photos": photos,
    "source_only": True,
    "empirical_human_validations": 0,
    "runtime_promotions": 0,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(window, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(
    "B07u first-edition Moon source window: images",
    len(photos),
    "PDF725-735, unnumbered next at PDF735",
)
