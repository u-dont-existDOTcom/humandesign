#!/usr/bin/env python3
"""Protect original 1647 first-edition Sun direction photo frames and page seams."""

import hashlib
import json
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PRIOR = B.parent / "B07q"
SOURCE_PDF = Path("/mnt/hdd/home/joel/ai-research-source-cache/lilly-1647-b30338724-original.pdf")
NEW = Path("/mnt/hdd/var/tmp/b07s_photo_probe")
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


assert SOURCE_PDF.stat().st_size == 141842963
assert sha(SOURCE_PDF) == "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
index = j(INDEX)
assert index["records_count"] == 11415
assert index["batches"][-1]["id"] == "B07r"
assert index["next"]["chapter"] == "CLXII"
assert index["next"]["pdf_page"] == 713
assert j(CHINA)["sum_source_annotations"] == 97
old = j(PRIOR / "ORIGINAL_SOURCE_WINDOW_V1.json")
photos = {}
for page in range(713, 726):
    previous = PRIOR / "evidence" / f"pdf_1647-{page}.jpg"
    if page <= 720:
        original = previous
        assert sha(previous) == old["photos"][str(page)]["sha256"]
        assert previous.stat().st_size == old["photos"][str(page)]["bytes"]
        method = "ORIGINAL_WELLCOME_FIRST_EDITION_JPEG_PREVIOUS_B07q"
    else:
        original = NEW / f"page-{page}.jpg"
        method = "SOURCE_PDF_POPPLER_PD fTOPPM_F_721_L_729_SCALE_TO_1600_JPEG_Q93".replace(
            "PD fTOPPM", "PDFTOPPM"
        )
    target = B / "evidence" / f"pdf_1647-{page}.jpg"
    if not target.exists():
        shutil.copyfile(original, target)
    assert target.read_bytes() == original.read_bytes()
    photos[str(page)] = dict(
        file=str(target.relative_to(B)),
        original_pdf_frame=page,
        printed_page=page - 34,
        sha256=sha(target),
        bytes=target.stat().st_size,
        extraction_method=method,
        body_role=(
            "CLXII_BODY_AND_PRIOR_CLXI_DIVIDER"
            if page == 713
            else "CLXII_BODY_AND_NEXT_CLXIII_DIVIDER"
            if page == 723
            else "CLXIII_NEXT_CONTEXT_AND_FOLLOWING_CLXIIII_SEAM"
            if page == 725
            else "CLXIII_NEXT_CONTEXT"
            if page == 724
            else "CLXII_BODY_ONLY"
        ),
    )
window = {
    "schema": "LILLY_1647_PRINTED_CLXII_ORIGINAL_SOURCE_WINDOW_V1",
    "batch": "B07s",
    "source": "William Lilly Christian Astrology 1647 Wellcome b30338724 first edition",
    "original_pdf_sha256": sha(SOURCE_PDF),
    "original_pdf_bytes": SOURCE_PDF.stat().st_size,
    "source_pdf_frame_count": 894,
    "original_pdf_local_private_cache_path": str(SOURCE_PDF),
    "local_rasterization_note": (
        "PDF pages 721-725 are faithful Poppler renders from the SHA-locked "
        "primary original PDF. Earlier JPEGs 713-720 are retained photo "
        "witnesses from B07q."
    ),
    "prior_accepted_lilly": 11415,
    "prior_index_sha256": sha(INDEX),
    "prior_retained_ptolemy": 1066,
    "independent_chinese_v2_count": 97,
    "new_source_record_starts": "R11416",
    "printed_clxii": {
        "printed_numeral": "CLXII",
        "heading": "The Sunne directed to PROMITTORS",
        "starts_frame": 713,
        "starts_printed_page": 679,
        "body_frames": list(range(713, 724)),
        "ends_frame": 723,
        "ends_printed_page": 689,
        "chapter_start_after_prior_divider": True,
        "chapter_end_before_next_divider": True,
    },
    "following_printed_clxiii": {
        "printed_numeral": "CLXIII",
        "heading": "The Sunne Directed to FIXED STARRES",
        "starts_frame": 723,
        "ends_frame": 725,
        "start_below_divider_frame": 723,
        "next_printed_clxiiii_heading_frame": 725,
        "body_not_part_of_clxii": True,
    },
    "photos": photos,
    "source_only": True,
    "empirical_person_validations": 0,
    "runtime_promotions": 0,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(window, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("B07s source window saved", len(photos), "images; CLXII ends printed 689/PDF723")
