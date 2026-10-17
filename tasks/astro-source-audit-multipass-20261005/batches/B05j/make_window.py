#!/usr/bin/env python3
"""Freeze first-edition source witnesses for the *next* chapter, no record admission."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


original = {
    "batch": "B05j",
    "status": "PRIMARY_SOURCE_WINDOW_VERIFIED_PENDING_ANNOTATION_EXTRACTION",
    "baseline_git_commit": "f1cbdfb4acb798cd040093f565f22e908e67110f",
    "baseline_accepted_lilly": 6671,
    "baseline_retained_ptolemy": 1066,
    "baseline_historical_total": 7737,
    "next_record_id": "R6672",
    "primary_source": "William Lilly Christian Astrology first edition 1647, Wellcome b30338724",
    "full_original_pdf_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
    "next_chapter": {
        "printed_numeral": "CXI",
        "editorial_numeral": "CXII",
        "heading": "Nature of the Signes; Colour of the Face and Haire",
        "original_pdf_start": 581,
        "original_pdf_end": 583,
        "original_printed_page_start_as_seen": "539",
        "following_printed_chapter": "CXII",
        "following_heading": "Of the grossenesse or leannesse of Bodies",
        "following_heading_pdf_page": 583,
        "following_heading_position": "Below horizontal divider near foot of original PDF583",
        "following_following_heading": (
            "CHAP CXIII. Of the generall Fortune or Misery of the Native"
        ),
        "following_following_heading_pdf_page": 585,
    },
    "printed_folios_original_scans": {
        "581": "539",
        "582": "548",
        "583": "549",
        "584": "542",
        "585": "543",
        "586": "552",
    },
    "source_pagination_note": (
        "Printed folio 539 PDF581 follows 538 PDF580 after printed545, PDF582-583 show "
        "548/549, PDF584-585 show 542/543 after 549, PDF586 shows 552. "
        "Source text/chapters continue in image order. Never reorder by "
        "inconsistent original folios."
    ),
    "body_source_topics": [
        "Cross-reference to Book I first edition pp.93-99 for sign qualities.",
        "Five categorical groups assigning stature to zodiac signs, not measured height.",
        (
            "Six or more distinct purported indicators for complexion/face/hair "
            "involving signs, planetary conditions, fixed stars and humours."
        ),
        "Seasonal descriptions of bodily form, hair, eye shape and temperament.",
        (
            "Explicit historical climate/country proviso: author says a "
            "Spaniard/Dane illustration can contradict isolated chart-based "
            "colouring."
        ),
        (
            "Conditional stature fallbacks when no planet partile-aspects Lord "
            "Ascendant, and when Lord is retrograde or in fall."
        ),
        (
            "Historically disparaging 'deformity', appearance and colour judgments "
            "are author claims, not human biometric, ancestry, health or racial "
            "evidence."
        ),
    ],
    "admission": {
        "historical_records_added": 0,
        "empirical_human_stature_validations": 0,
        "empirical_hair_or_face_validations": 0,
        "race_or_ancestry_predictions_authorized": False,
        "clinical_disability_predictions_authorized": False,
        "runtime_promotions": 0,
    },
    "original_scans": {},
}
for n in range(581, 587):
    file = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = file.read_bytes()
    assert len(raw) > 200_000 and raw[:2] == bytes.fromhex("ffd8")
    original["original_scans"][str(n)] = {
        "file": str(file.relative_to(B)),
        "sha256": h(file),
        "bytes": len(raw),
        "folio_as_seen": original["printed_folios_original_scans"][str(n)],
    }
(B / "SOURCE_WINDOW_20261017.json").write_text(
    json.dumps(original, indent=2, ensure_ascii=False) + "\n"
)
print("Verified next source window: 6 original images; canonical source frontier remains R6671.")
