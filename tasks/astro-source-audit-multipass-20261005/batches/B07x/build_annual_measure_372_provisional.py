#!/usr/bin/env python3
"""Reconstruct 372 annual-motion cells as SECONDARY transcription candidates.

The searchable modern transcription is not in zodiac sign order. Explicit
photo-checked sign headers, a 7 Libra source worked example, and boundary
continuity determine a reversible column mapping. No OCR or invented fixes.
All cells remain PROVISIONAL unless individually checked against 1647 photo.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parent
SIGN_TO_SECONDARY_BLOCK = {
    "Aries": 9,
    "Taurus": 0,
    "Gemini": 1,
    "Cancer": 2,
    "Leo": 3,
    "Virgo": 4,
    "Libra": 10,
    "Scorpio": 5,
    "Sagittarius": 6,
    "Capricorn": 7,
    "Aquarius": 8,
    "Pisces": 11,
}
SIGN_NAMES = tuple(SIGN_TO_SECONDARY_BLOCK)
AUDITED_EXACT = {
    ("Aries", 0): (54, 26),
    ("Taurus", 0): (55, 40),
    ("Gemini", 0): (59, 52),
    ("Cancer", 0): (62, 18),
    ("Virgo", 0): (55, 16),
    ("Libra", 0): (54, 4),
    ("Libra", 7): (54, 25),
    ("Scorpio", 0): (57, 24),
    ("Sagittarius", 0): (63, 32),
    ("Capricorn", 0): (66, 53),
    ("Aquarius", 0): (66, 33),
    ("Pisces", 0): (57, 35),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def parse(text: str):
    start = text.index("A Table of the annuall measure in Directions.")
    end = text.index("The use of the Table.", start)
    section = text[start:end]
    header = " ".join(str(i) for i in range(31))
    assert header in section
    tail = section[section.index(header) + len(header) :]
    tokens = [int(s) for s in re.findall(r"\b\d+\b", tail)]
    assert len(tokens) == 744, len(tokens)
    candidate_columns = [
        [(tokens[(62 * b + 2 * d)], tokens[(62 * b + 2 * d + 1)]) for d in range(31)]
        for b in range(12)
    ]
    for (sign, degree), pair in AUDITED_EXACT.items():
        pos = SIGN_TO_SECONDARY_BLOCK[sign]
        assert candidate_columns[pos][degree] == pair, (
            sign,
            degree,
            candidate_columns[pos][degree],
            pair,
        )
    records = []
    for sign in SIGN_NAMES:
        block = SIGN_TO_SECONDARY_BLOCK[sign]
        previous_total = None
        for degree, (minute, second) in enumerate(candidate_columns[block]):
            sources = []
            if (sign, degree) in AUDITED_EXACT:
                sources.append("FIRST_EDITION_PHOTO_745_MANUAL_VISUAL_CHECK")
            flags = []
            if not (50 <= minute <= 68 and 0 <= second <= 59):
                flags.append("OUTSIDE_EXPECTED_RATE_RANGE_OR_BAD_SECOND")
            current = 60 * minute + second
            if previous_total is not None and abs(current - previous_total) > 35:
                flags.append("ADJACENT_DEGREE_DISCONTINUITY_GT_35_SECONDS")
            if sign == "Leo" and degree == 0:
                flags.append("SOURCE_GLYPH_CANDIDATE_59_34_DIFFERS_FROM_DERIVATIVE_59_24")
            records.append(
                {
                    "sign": sign,
                    "zodiac_degree": degree,
                    "secondary_text_block_zero_based": block,
                    "candidate_original_annual_equator_rate_minutes": minute,
                    "candidate_original_annual_equator_rate_seconds": second,
                    "first_edition_manual_photo_anchor": (
                        "PDF745/printed711" if sources or (sign == "Leo" and degree == 0) else None
                    ),
                    "original_photo_glyph_alternative_unresolved": (
                        [59, 34] if (sign, degree) == ("Leo", 0) else None
                    ),
                    "verified_direct_first_edition_photo": bool(sources),
                    "source_flags": flags,
                    "transcription_status": (
                        "SELECTED_ORIGINAL_PHOTO_CHECKED"
                        if sources
                        else "DERIVATIVE_TEXT_ONLY_NOT_VERIFIED"
                    ),
                    "corrected_from_source_by_arithmetic": False,
                    "actual_human_prediction_validated": False,
                    "runtime_promoted": False,
                }
            )
            previous_total = current
    assert len(records) == 372
    assert sum(r["verified_direct_first_edition_photo"] for r in records) == len(AUDITED_EXACT)
    issues = [
        dict(
            sign=r["sign"],
            degree=r["zodiac_degree"],
            rate=f"{r['candidate_original_annual_equator_rate_minutes']}:"
            f"{r['candidate_original_annual_equator_rate_seconds']:02d}",
            flags=r["source_flags"],
        )
        for r in records
        if r["source_flags"]
    ]
    out = {
        "schema": "LILLY_1647_ANNUAL_MEASURE_372_DERIVATIVE_CANDIDATES_V1",
        "batch": "B07x",
        "historical_source": (
            "William Lilly, Christian Astrology, original 1647 printed p.711, PDF745"
        ),
        "source_photo_sha256": json.loads((B / "ORIGINAL_SOURCE_WINDOW_V1.json").read_text())[
            "photos"
        ]["745"]["sha256"],
        "secondary_transcription_aid": "https://pdfcoffee.com/william-lilly-christian-astrology-volume-3-pdf-free.html",
        "source_text_section_sha256": digest(section.encode("utf-8")),
        "original_zodiac_sign_order": list(SIGN_NAMES),
        "derivative_flattened_order_bug": True,
        "sign_to_flattened_block": SIGN_TO_SECONDARY_BLOCK,
        "sign_mapping_method": (
            "Restored from individually visually checked original top-row sign fields, "
            "Libra 7°, and neighboring sign-rate continuity. "
            "Never use naive header-order split."
        ),
        "original_printed_degrees_inclusive": [0, 30],
        "rates_are_scalar_equatorial_arcminutes_up_to_around_66": True,
        "particular_Leo_degree_zero_photo_glyph_unresolved": [59, 34],
        "printed_zodiac_signs": 12,
        "source_cells_expected": 372,
        "direct_original_photo_confirmed": len(AUDITED_EXACT),
        "cells_without_direct_photo_check": 372 - len(AUDITED_EXACT),
        "tentative_candidate_pairs": records,
        "source_flags_summary": issues,
        "complete_1647_photo_table_transcription": False,
        "true_1647_epoch_vs_modern_ra_parity_verified": False,
        "independent_human_events_validated": 0,
        "runtime_promotions": 0,
    }
    path = B / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "records": len(records),
                "original_photo_checked": len(AUDITED_EXACT),
                "unverified": 372 - len(AUDITED_EXACT),
                "flag_count": len(issues),
                "flag_samples": issues[:30],
                "sha256": digest(path.read_bytes()),
                "canonical_index_unchanged": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached-readable-text", type=Path, required=True)
    parse(parser.parse_args().cached_readable_text.read_text(encoding="utf-8"))
