"""Census the 1647 Lilly Book III *contents*, not rules or survey scores.

The input is the original public-domain 1647 archive OCR whose hash was
independently frozen in the accepted Lilly religion/dream chapter audit.
Exact anchors and decoded character offsets make the inventory reproducible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("LILLY3-NATAL-DOMAIN-CENSUS-v1.json")
V7 = ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"
SHA = "7c08b55359c41049c5d43901b8da869a326f8eb852e4a30603a4b698533626aa"
N_BYTES = 2005702

# id, normalized source topic, exact historical OCR anchor, approximate original
# printed pages, subject class, relation to V7, actual named V7 families.
# Page numbers derive from the TOC and require individual facsimile readback
# before being treated as rules or precise page-located quotations.
ROWS = [
    (
        "L3-TOC-001",
        "birth-time rectification",
        "Trutine  of  Hermes",
        "500–509",
        "technical_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-002",
        "preconditions before judging a nativity",
        "things  mftderable",
        "524",
        "technical_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-003",
        "claims about longevity",
        "pace  of  life",
        "525–530",
        "high_stakes",
        "exclude_from_routine_survey",
        [],
    ),
    (
        "L3-TOC-004",
        "lord of geniture chart technique",
        "Lord  of  the  Geniture",
        "531",
        "technical_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-005",
        "body complexion and temperament",
        "Complexion",
        "532–533",
        "physical_characteristics",
        "outside_behavioral_survey_scope",
        [],
    ),
    (
        "L3-TOC-006",
        "character and manners",
        "Manners  of  the  Native",
        "534–542",
        "psychological_disposition",
        "partial",
        ["emotion", "friend_company", "trust"],
    ),
    (
        "L3-TOC-007",
        "understanding and intellectual ability",
        "Vnder  Handing",
        "543–545",
        "psychological_disposition",
        "partial",
        ["understanding", "method", "ability"],
    ),
    (
        "L3-TOC-008",
        "physical stature and appearance",
        "ftature",
        "546–550",
        "physical_characteristics",
        "outside_behavioral_survey_scope",
        [],
    ),
    (
        "L3-TOC-009",
        "actual overall life fortune",
        "general!  fortune",
        "551–552",
        "life_history",
        "proxy_only",
        ["development"],
    ),
    (
        "L3-TOC-010",
        "wealth acquisition and retention",
        "fecond  Houfe",
        "553–563",
        "life_history",
        "proxy_only",
        ["resources"],
    ),
    (
        "L3-TOC-011",
        "siblings and kinship relations",
        "Kinred,  Brethren",
        "564–568",
        "life_history",
        "absent",
        [],
    ),
    (
        "L3-TOC-012",
        "parents, inheritance and household family",
        "fourth  Houfe,  concerning  Parents",
        "569–575",
        "life_history",
        "absent",
        [],
    ),
    (
        "L3-TOC-013",
        "bodily illness and disability claims",
        "Infirmities  of  Bod",
        "576–585",
        "high_stakes",
        "exclude_from_routine_survey",
        [],
    ),
    (
        "L3-TOC-014",
        "servants and livestock",
        "Servants  and  fmall  Cattle",
        "586",
        "life_history",
        "absent",
        [],
    ),
    (
        "L3-TOC-015",
        "marriage history and spousal relations",
        "mens  Marriages",
        "587–602",
        "life_history",
        "proxy_only",
        ["romance"],
    ),
    (
        "L3-TOC-016",
        "children and parenthood claims",
        "fift  Houle",
        "603–605",
        "life_history",
        "absent",
        [],
    ),
    (
        "L3-TOC-017",
        "foreign travel and journeys",
        "Journeys  and  Religion",
        "606–611",
        "life_history",
        "proxy_only",
        ["understanding"],
    ),
    (
        "L3-TOC-018",
        "religious conviction and affiliation",
        "Religion  of  the  Native",
        "611–613",
        "phenomenology_and_worldview",
        "absent",
        [],
    ),
    (
        "L3-TOC-019",
        "dreams and dream interpretation",
        "OfDreames",
        "613–614",
        "phenomenology_and_worldview",
        "absent",
        [],
    ),
    (
        "L3-TOC-020",
        "honors, recognition and public rank",
        'Honour  or  "Dignity',
        "615–623",
        "life_history",
        "proxy_only",
        ["resources", "external_role"],
    ),
    (
        "L3-TOC-021",
        "occupation and vocation",
        "Profeffion  of  the  Native",
        "624–633",
        "life_history",
        "proxy_only",
        ["work_energy", "purpose", "practice_focus"],
    ),
    (
        "L3-TOC-022",
        "actual friendships and concord",
        "Of  Friends",
        "634–638",
        "life_history",
        "partial",
        ["connections", "trust", "friend_company"],
    ),
    (
        "L3-TOC-023",
        "opposition and personal conflict",
        "Of  enemies",
        "639–642",
        "life_history",
        "partial",
        ["trust", "emotion"],
    ),
    (
        "L3-TOC-024",
        "captivity and imprisonment outcomes",
        "Captivity  or  Imprijonment",
        "643",
        "high_stakes",
        "exclude_from_routine_survey",
        [],
    ),
    (
        "L3-TOC-025",
        "mortality and violent death claims",
        "Of  death",
        "644–648",
        "high_stakes",
        "exclude_from_routine_survey",
        [],
    ),
    (
        "L3-TOC-026",
        "astrological directions and timing technique",
        "effe&s  of  Dire&ions",
        "651–714",
        "timing_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-027",
        "annual profections and year lords",
        "annual!  Pro  feet",
        "715–733",
        "timing_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-028",
        "revolutions and planetary returns",
        "Of  Revolutions",
        "734–740",
        "timing_method",
        "not_a_participant_trait",
        [],
    ),
    (
        "L3-TOC-029",
        "transits and worked merchant nativity",
        "tranfits^upon",
        "741–742 onward",
        "timing_method",
        "not_a_participant_trait",
        [],
    ),
]

ALREADY_AUDITED = {
    "L3-TOC-018": "Lilly Book III CXLII, 31-unit combined religion/dream ledger",
    "L3-TOC-019": "Lilly Book III CXLIII, 31-unit combined religion/dream ledger",
}


def compile_census(ocr: bytes) -> dict:
    if len(ocr) != N_BYTES or hashlib.sha256(ocr).hexdigest() != SHA:
        raise ValueError("1647 source OCR bytes/hash mismatch; do not infer anchors")
    text = ocr.decode("utf-8", errors="replace")
    start_marker = "The  Contents  of  the  third  R  ookii"
    end_marker = "AN \n\n\nINTRODUCTION"
    if text.count(start_marker) != 1:
        raise ValueError("Cannot uniquely identify original Book III contents")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    contents = text[start:end]
    available_families = set(json.loads(V7.read_text())["families"])
    census = []
    for row_id, topic, needle, printed_pages, subject_class, v7_status, families in ROWS:
        if not set(families) <= available_families:
            raise ValueError(f"Unrecognized existing V7 family: {row_id}")
        matches = [start + pos for pos in range(len(contents)) if contents.startswith(needle, pos)]
        if len(matches) != 1:
            raise ValueError(f"Missing/ambiguous source contents anchor {row_id}: {len(matches)}")
        pos = matches[0]
        witness_excerpt = text[max(start, pos - 30) : min(end, pos + len(needle) + 85)]
        record = {
            "id": row_id,
            "topic_for_source_inventory_only": topic,
            "original_book": "Christian Astrology 1647, Book III: Nativities",
            "original_contents_heading_ocr_exact": needle,
            "original_ocr_character_offset": pos,
            "original_ocr_excerpt": witness_excerpt,
            "printed_pages_from_contents": printed_pages,
            "printed_page_fidelity": (
                "approximate_original_OCR_table_of_contents_not_facsimile_page_rule"
            ),
            "subject_class": subject_class,
            "v7_coverage_category": v7_status,
            "v7_families_with_partial_or_proxy_relevance_only": families,
            "actual_chart_rule_checked": False,
            "this_record_predictive_scoring_authorized": False,
            "rule_not_to_be_inferred_from_index": True,
            "already_independently_audited": ALREADY_AUDITED.get(row_id),
        }
        census.append(record)
    if len({r["id"] for r in census}) != len(census):
        raise ValueError("Repeated source inventory identity")
    return {
        "schema": "lilly3-natal-original-contents-domain-census-v1",
        "status": "CONTENTS_ONLY_NOT_RULE_LEVEL_OR_PREDICTIVE_VALIDATION",
        "source": {
            "author": "William Lilly",
            "work": "Christian Astrology, 1647",
            "book": "III — Nativities",
            "original_archive_url": "https://archive.org/details/b30338724",
            "original_public_domain_ocr_url": "https://archive.org/download/b30338724/b30338724_djvu.txt",
            "original_full_ocr_size_bytes": N_BYTES,
            "original_full_ocr_sha256": SHA,
            "contents_section_char_start": start,
            "contents_section_char_end": end,
            "contents_marker_start": start_marker,
            "contents_marker_end": end_marker,
            "original_printed_page_scope": (
                "Book III front contents, natal topics through printed p.742"
            ),
            "source_limit": (
                "Old-type OCR interleaves printed columns and corrupts page/glyph text; "
                "not a rule-level witness."
            ),
        },
        "survey": {
            "bank": "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json",
            "version": json.loads(V7.read_text())["version"],
            "coverage_interpretation": (
                "A V7 scene about an action does not establish actual historical life outcomes."
            ),
        },
        "counts": {
            "source_topics": len(census),
            "subject_class": dict(sorted(Counter(x["subject_class"] for x in census).items())),
            "v7_coverage_category": dict(
                sorted(Counter(x["v7_coverage_category"] for x in census).items())
            ),
            "distinct_named_v7_families_used": len(
                {
                    f
                    for item in census
                    for f in item["v7_families_with_partial_or_proxy_relevance_only"]
                }
            ),
            "complete_original_page_folio_adjudication": False,
        },
        "records": census,
        "gates": {
            "historical_rule_from_contents_only": False,
            "empirical_astrological_prediction_established": False,
            "scorer_or_gpt_changed": False,
            "sensitive_event_interview_compulsory": False,
            "already_completed_people_requestioned": False,
            "no_birth_data_accessed": True,
            "next_step": (
                "Continue original body and facsimile rule review, then design optional "
                "outcome-appropriate instruments and blinded predictions."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = (
        json.dumps(compile_census(args.ocr.read_bytes()), indent=2, ensure_ascii=False) + "\n"
    ).encode()
    if args.check:
        if OUT.read_bytes() != value:
            raise ValueError("Versioned Book III domain census differs from original source bytes")
    else:
        OUT.write_bytes(value)
    print(
        json.dumps(
            {
                "mode": "VERIFIED" if args.check else "WRITTEN",
                "records": len(ROWS),
                "bytes": len(value),
                "sha256": hashlib.sha256(value).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
