#!/usr/bin/env python3
"""Freeze independent 1647/1659 original merchant-friends text, never human accuracy."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261021.json")
assert a["batch"] == "B07bh"
assert a["parent_accepted_commit"] == "6fc30d221adfc51917cdb04c7bf895989cbb5762"
assert a["source_heading_printed_literal"] == "CLXXXIII"
assert a["editorial_source_ordinal"] == 185
assert a["previous_honours_heading_printed_literal"] == "CLXXXIIII"
assert a["next_imprisonment_heading_printed_literal"] == "CLXXXIV"
assert a["later_death_heading_printed_literal"] == "CLXXXV"
assert len(a["source_groups"]) == 6
assert (
    a["known_merchant"]
    and not a["independent_real_merchant_friendship_or_business_records_obtained"]
)
assert not a["original_glyph_by_glyph_authoritative_transcription_complete"]

photos = {}
for name, edition, folio, frame, role in (
    ("1647-original-folio762-IIIF.jpg", "first_1647", 762, 796, "friendship_opening"),
    ("1647-original-folio763-IIIF.jpg", "first_1647", 763, 797, "friendship_end_next"),
    ("1647-original-folio764-IIIF.jpg", "first_1647", 764, 798, "following_context"),
    ("1659-original-folio762-DjVu.jpg", "second_1659", 762, 791, "friendship_opening"),
    ("1659-original-folio763-DjVu.jpg", "second_1659", 763, 792, "friendship_end_next"),
):
    path = B / "evidence" / name
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150_000
    photos[name] = {
        "path": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "edition": edition,
        "printed_folio": folio,
        "original_scan_frame": frame,
        "source_role": role,
    }
save(
    "ORIGINAL_SOURCE_WITNESS_20261021.json",
    {
        "batch": "B07bh",
        "two_distinct_original_printings_pages_used": True,
        "first_1647_Wellcome_b30338724_whole_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "second_1659_whole_original_file_sha256_authenticated": False,
        "original_1647_body_source_folios": [762, 763],
        "1647_source_pdf_frames": [796, 797],
        "two_printings_agree_on_printed_Friends_CLXXXIII": True,
        "two_printings_agree_on_next_CLXXXIV": True,
        "historical_content_not_independent_expert_diplomatic_text": True,
        "photos": photos,
    },
)

records, mapdata = [], []
for index, group in enumerate(a["source_groups"], 1):
    sid = f"B07bh-S{index:03d}"
    assert group["id"] == sid
    folio = group["original_printed_folio"]
    assert folio in {762, 763}
    first = photos[f"1647-original-folio{folio}-IIIF.jpg"]
    second = photos[f"1659-original-folio{folio}-DjVu.jpg"]
    group_ids = []
    for c in group["clauses"]:
        n = 13237 + len(records)
        rid = f"R{n}"
        assert c["id"] == rid
        assert len(c["short_original_fragment_not_full_diplomatic"]) >= 6
        assert len(c["research_paraphrase_separate"]) >= 45
        assert c["real_person_outcome_verified"] is False
        assert c["runtime_promoted"] is False
        row = {
            "id": rid,
            "record_number": n,
            "batch": "B07bh",
            "original_printed_folio": folio,
            "original_1647_photo_SHA256": first["sha256"],
            "independent_1659_photo_SHA256": second["sha256"],
            "original_1647_PDF_frame": first["original_scan_frame"],
            "independent_1659_DjVu_frame": second["original_scan_frame"],
            "source_span": sid,
            "role": c["role"],
            "historical_evidence_type": (
                "NEXT_SOURCE_NAVIGATION"
                if c["qualifier"] == "next-navigation"
                else "ORIGINAL_FRIENDS_MERCHANT_HISTORICAL_CLAUSE"
            ),
            "source_short_original_1647_verbatim_fragment_NOT_diplomatic_full_glyphs": (
                c["short_original_fragment_not_full_diplomatic"]
            ),
            "research_gloss_separate_from_original_quote": c["research_paraphrase_separate"],
            "qualification": c["qualifier"],
            "merchant_already_known_to_author": True,
            "independent_real_business_associate_outcome_verified": False,
            "independent_real_friendship_count_or_quality_verified": False,
            "original_known_merchant_birth_clock_and_chart_engine_verified": False,
            "independent_human_blind_forecast_tested": False,
            "actual_person_partner_reliability_danger_inference_authorized": False,
            "runtime_astrological_rule_promoted": False,
        }
        records.append(row)
        group_ids.append(rid)
    mapdata.append(
        {
            "source_span": sid,
            "original_printed_folio": folio,
            "source_group": group["source_group"],
            "source_record_ids": group_ids,
            "first_1647_photo_sha256": first["sha256"],
            "independent_1659_photo_sha256": second["sha256"],
        }
    )
assert len(records) == 35
assert [x["record_number"] for x in records] == list(range(13237, 13272))
assert [x["id"] for x in records if x["historical_evidence_type"] == "NEXT_SOURCE_NAVIGATION"] == [
    "R13269",
    "R13270",
    "R13271",
]
assert len({x["id"] for x in records}) == 35

save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07bh",
        "source_groups": mapdata,
        "source_group_count": 6,
        "record_count": 35,
        "substantive_source_records": 32,
        "future_source_navigation": 3,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07bh",
        "historical_scope": (
            "Lilly's retrospective judgment of an already-known "
            "merchant, not a blind human friendship or business-partner test"
        ),
        "issues": [
            "The first 1647 and second 1659 originals repeat the literal "
            "Friends CHAP CLXXXIII after printed Honours CLXXXIIII, "
            "with independent page imagery; do not normalize numerals silently.",
            "The following p763 separately heads twelfth-house "
            "printed CHAP CLXXXIV Of Imprisonment, then eighth-house "
            "CHAP CLXXXV Of Death its quality. Both are next sections only.",
            "The original describes an already-known merchant and gives no "
            "independent named friends, business partnerships, profits, "
            "losses, helping behaviors or observed test outcomes.",
            "Sagittarius bicorporeal cusp eleventh, Moon opposition cusp and "
            "Moon ruling seventh are AUTHORIAL chart claims, not verified "
            "against the original 1616 calendar or an independent ephemeris.",
            "Moon-associated sailors and so-called vulgar fellows are "
            "dismissed as friends. These are historical class prejudices "
            "and cannot classify actual people or their safety.",
            "The source treats one Lunar seventh-house BUSINESS PARTNER "
            "as financially harmful. It does not establish damage, "
            "untrustworthiness or any real person's intent.",
            "Jupiter in Sagittarius / Jovian people favorable; Venus people "
            "also favorable. The literal word 'Venetians' contrasted with "
            "'Mercurians' is semantically ambiguous; no modern Venice "
            "nationality or geographical inference is authorized.",
            "Mercury allegedly rejected as peregrine and combust; the text "
            "does not quantify orbs, specify natal instant or "
            "independently verify these calculations.",
            "Mars trine eleventh cusp, Mars's Leo description and "
            "referenced sign natures give many possible assisting "
            "professions; class and iron-tool trades are broad alternatives.",
            "Original p81 Moon-people list and earlier zodiac/Mars descriptions "
            "are explicitly referenced but NOT redocumented or "
            "assumed complete here.",
            "No denominators, age limits, counterexamples, unselected partners, "
            "matched nonastrology friendship/profit baselines, or "
            "prospective human validation exist in this batch.",
            "Source notes are short anchored paraphrases and two image witnesses, "
            "not a complete expert-independent diplomatic transcription.",
            "Full 1659 source book hash not authenticated; only exact "
            "individual second edition JPEG pages were hashed.",
        ],
        "fully_disambiguated_old_venus_term_Venetians": False,
        "source_mercury_peregrine_combust_independent_astro_verified": False,
        "actual_merchant_friendship_or_trade_outcome_verified": False,
        "real_human_predictive_accuracy_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07bh",
        "status": "FIRST_1647_AND_SECOND_1659_FRIENDS_MERCHANT_SOURCE_ONLY",
        "printed_chapter": "CLXXXIII",
        "editorial_ordinal": 185,
        "record_count": 35,
        "first_R": "R13237",
        "last_R": "R13271",
        "substantive": 32,
        "navigation": 3,
        "source_groups": 6,
        "original_folios": [762, 763],
        "next_printed_chapter": "CLXXXIV",
        "next_original_folio": 763,
        "historical_known_merchant_outcomes_independently_verified": False,
        "genuine_human_blind_predictive_tests": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07bh",
        "status": "ORIGINAL_1647_1659_MERCHANT_FRIENDS_LOCALLY_FROZEN",
        "Lilly_before": 13236,
        "new_historical_source_only_annotations": 35,
        "Lilly_after_if_accepted": 13271,
        "Ptolemy_retained": 1066,
        "Western_after_if_accepted": 14337,
        "source_1647_folios": [762, 763],
        "source_editorial_ordinal": 185,
        "source_literal_printed_CLXXXIII": True,
        "next_printed_CLXXXIV": True,
        "first_R": "R13237",
        "last_R": "R13271",
        "next_R": "R13272",
        "numbered_editorial_chapters_increment": 1,
        "source_photo_count": 5,
        "rules_sha256": sha(B / "RULES.json"),
        "source_first_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261021.json"),
        "witness_sha256": sha(B / "ORIGINAL_SOURCE_WITNESS_20261021.json"),
        "real_friendship_or_business_accuracy_verified": False,
        "real_human_blind_validations": 0,
        "runtime_promotions": 0,
    },
)
print("B07bh first 1647+second1659 Friends: 35 historical notes R13237-R13271.")
