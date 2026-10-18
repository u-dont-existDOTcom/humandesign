#!/usr/bin/env python3
"""Freeze photographed preliminary source window for CLX without accepting rules."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


i = json.loads(IDX.read_text())
c = json.loads(CHINESE.read_text())
assert i["records_count"] == 11067
assert i["batches"][-1]["id"] == "B07p"
assert i["next"]["chapter"] == "CLX"
assert i["next"]["pdf_page"] == 702
assert i["next"]["printed_chapter_numeral"] == "CLX"
assert i["runtime_promotions"] == i["empirical_validations"] == 0
assert c["sum_source_annotations"] == 72
assert c["runtime_promotions"] == 0

images = {}
for num in range(702, 721):
    path = B / "evidence" / f"pdf_1647-{num}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    if num <= 711:
        role = "printed_CLX_body_with_CLXI_divider_on_711"
    elif num <= 713:
        role = "following_printed_CLXI_fixed_stars_with_CLXII_divider_on_713"
    else:
        role = "further_CLXII_source_context_not_CLX"
    images[str(num)] = {
        "file": str(path.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(path),
        "printed_folio": str(num - 34),
        "role": role,
    }

manifest = {
    "schema": "LILLY_1647_CLX_SOURCE_WINDOW_PRELIMINARY_V1",
    "batch": "B07q",
    "status": "PHOTOGRAPHIC_SOURCE_WINDOW_NOT_EXTRACTED_NOT_ACCEPTED",
    "source": "William Lilly 1647 Christian Astrology original first edition Wellcome b30338724",
    "original_pdf_894_frames_sha256": (
        "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
    ),
    "current_accepted_lilly": 11067,
    "current_accepted_ptolemy": 1066,
    "current_western_total": 12133,
    "next_historical_record": "R11068",
    "accepted_index_sha256": sha(IDX),
    "parallel_chinese_source_annotations": 72,
    "numbered_chapters_added": 0,
    "historical_records_added": 0,
    "printed_CLX": {
        "heading": "Directions of the Mid-heaven to PROMITTORS",
        "starts_original_pdf": 702,
        "starts_printed_page": 668,
        "body_original_pdf_frames": list(range(702, 712)),
        "ends_original_pdf": 711,
        "ends_printed_page": 677,
        "source_divider": (
            "Original CLX begins after divider lower PDF702; "
            "its final paragraph on Midheaven/horoscope ends "
            "before printed CLXI divider upper/middle PDF711."
        ),
    },
    "following_printed_CLXI": {
        "heading": "The Mid-heaven Directed to FIXED STARRES",
        "heading_original_pdf": 711,
        "body_original_pdf_frames": [711, 712, 713],
        "source_divider": (
            "Original CLXI starts beneath a separate divider "
            "mid PDF711 and ends before separately numbered "
            "CLXII after divider on PDF713."
        ),
    },
    "following_printed_CLXII": {
        "heading": "The Sunne directed to PROMITTORS",
        "heading_original_pdf": 713,
        "context_pdfs": list(range(713, 721)),
        "source_divider": "Original separate CLXII begins later PDF713; not part of CLX or CLXI.",
    },
    "photos": images,
    "claim_scope": (
        "The photographs show historical book pages. "
        "No CLI-X source rules extracted or admitted in B07q. "
        "Medical, mortality, social standing, partner, money, "
        "or violent-harm claims are NOT real human predictions."
    ),
    "printed_dividers_visually_checked": True,
    "complete_CLX_diplomatic_transcription": False,
    "actual_primary_directions_chart_engine_verified": False,
    "independent_human_predictions_validated": 0,
    "runtime_rule_promotions": 0,
}
out = B / "ORIGINAL_SOURCE_WINDOW_V1.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(
    "B07q preliminary source window",
    len(images),
    "original photos, accepted source remains 11067 Lilly",
)
