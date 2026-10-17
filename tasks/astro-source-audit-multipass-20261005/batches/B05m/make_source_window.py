#!/usr/bin/env python3
"""Preserve first-edition evidence for unnumbered second-house riches, no new records."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


page_data = {}
for pdf in (586, 587, 588):
    path = B / "evidence" / f"pdf_1647-{pdf}.jpg"
    data = path.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 100000
    page_data[str(pdf)] = {
        "file": str(path.relative_to(B)),
        "size": len(data),
        "sha256": sha(path),
        "printed_folio_original": {586: "552", 587: "553", 588: "554"}[pdf],
    }
manifest = {
    "batch": "B05m",
    "status": "VERIFIED_PRIMARY_SOURCE_WINDOW_PENDING_CLAIM_EXTRACTION",
    "parent_published_commit": "da1e261aaf896552f87eb3dc936e984da6adae7b",
    "primary_source": "Original William Lilly Christian Astrology 1647, Wellcome b30338724",
    "original_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
    "accepted_lilly_before_extraction": 6808,
    "ptolemy_retained": 1066,
    "accepted_combined_before_extraction": 7874,
    "next_new_source_id": "R6809",
    "chapters": {
        "unnumbered_riches": {
            "title": "The second House of RICHES, or the Goods of FORTUNE",
            "original_pdf_start": 586,
            "original_pdf_end": 587,
            "heading_position": "Below ornamental divider around middle PDF586",
            "end_position": "Above divider introducing printed CHAP CXIIII lower PDF587",
        },
        "following_printed_numbered": {
            "printed_numeral": "CXIIII",
            "editorial_numeral": "CXV",
            "title": "Whether the Native shall be Rich",
            "original_pdf_start": 587,
            "continues_pdf": 588,
        },
        "following_following_printed": {
            "printed_numeral": "CXV",
            "title": (
                "From whence, or by what meanes the Native shall come to an Estate or to Poverty"
            ),
            "original_pdf_start": 588,
        },
    },
    "original_source_plan": [
        (
            "Record second-house cusp interval from original wording without "
            "inventing a numerical upper-bound interpretation."
        ),
        (
            "Preserve second-house ruler, intercepted sign/ruler, Part of "
            "Fortune/ruler, Jupiter, occupying planets and distance from cusp as "
            "separate significators."
        ),
        (
            "Separate Ptolemy attributed wealth-cause passages from Lilly's source "
            "narration and Leovitius/Origanus additions."
        ),
        (
            "Preserve inheritance, work, social, religion, navigation and trade "
            "mechanisms without assuming human economic predictive validity."
        ),
        (
            "Do not mistake the unnumbered introductory wealth section for printed "
            "CHAP CXIIII; full CXIIII and CXV deserve their own studies."
        ),
    ],
    "images": page_data,
    "new_documentary_records": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
}
(B / "SOURCE_WINDOW_20261017.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
)
print("Original wealth source window locked, records unchanged at R6808.")
