#!/usr/bin/env python3
"""Lilly original 1647 CXLI travel success, danger and regions: historical only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, obj):
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


a = read("SOURCE_FIRST_AUTHORING_20261018.json")
assert a["batch"] == "B06u"
assert a["printed_chapter"] == "CXLI"
assert a["body_original_pdf_frames"] == [644, 645]
assert a["next_printed"] == "CXLII"
assert a["next_heading_pdf"] == 645
assert len(a["groups"]) == 6

rules, mapping = [], []
for i, group in enumerate(a["groups"], 1):
    sid = f"B06u-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {644, 645}
    ids = []
    for c in group["clauses"]:
        number = 8860 + len(rules)
        rid = f"R{number}"
        assert c["id"] == rid
        assert len(c["source_anchor_not_diplomatic"]) >= 5
        assert len(c["historical_meaning_only"]) >= 40
        assert not c["independently_validated_human_outcome"]
        assert not c["actual_travel_risk_or_region_advice_authorized"]
        assert not c["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B06u",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": c["role"],
                "source_anchor_not_diplomatic": c["source_anchor_not_diplomatic"],
                "historical_meaning_only": c["historical_meaning_only"],
                "qualification": c["source_qualification"],
                "documentary_source_accepted": True,
                "real_travel_success_or_profit_validated": False,
                "real_travel_hazard_crime_or_death_validated": False,
                "real_favorable_country_location_validated": False,
                "historical_p93_country_table_verified": False,
                "person_level_travel_medical_or_safety_advice_authorized": False,
                "real_person_criminality_or_religion_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 76
assert [x["record_number"] for x in rules] == list(range(8860, 8936))
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R8934", "R8935"]
assert len({x["id"] for x in rules}) == 76

photos = {}
for n in [644, 645, 646, 647, 648]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(n)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "role": (
            "travel_success_hazard_regions_body"
            if n <= 645
            else "following_religion_chapter_context"
        ),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06u",
        "source": "William Lilly Christian Astrology 1647 first edition Wellcome b30338724",
        "full_original_volume_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [644, 645],
        "following_printed_CXLII_heading_frame": 645,
        "original_source_images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06u",
        "source_groups": mapping,
        "source_group_count": 6,
        "historical_annotations": 76,
        "substantive": 74,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06u",
        "issues": [
            (
                "This printed CXLI source starts PDF644 middle after Haly "
                "causes and ends PDF645 before numbered CXLII religion; "
                "do not mix source claims from different chapters."
            ),
            (
                "The historical positive branch requires potent "
                "journey significators, benefic aspects OR "
                "essential domicile. Personal travel safety "
                "cannot be inferred from such testimony."
            ),
            (
                "Prosperity, friendship, honor and travel free of "
                "danger are distinct subjective or objective "
                "outcomes, relative to source social class, "
                "not independent accuracy replications."
            ),
            (
                "Negative cases depend on weak travel signifiers, "
                "malefic aspects and accidental positions/house "
                "rulership. Pronoun scope is unclear in one "
                "malefic 'their Houses' passage."
            ),
            (
                "Travel trouble, imprisonment, criminal acts, "
                "loss of money, family betrayal, military harm "
                "and physical injury are different risk targets "
                "without observations or time windows."
            ),
            (
                "Moist, fixed except Scorpio, movable, humane, "
                "bestial, watery and Scorpio classifications "
                "have distinct old danger taxonomies and "
                "many alternative or overlapping hazards."
            ),
            (
                "Drowning is claimed under a COMPUND condition "
                "of watery travel signifier AND malefic "
                "affliction AND violent fixed stars; "
                "fixed-star identities/orbs not specified."
            ),
            (
                "The source specifically excludes Scorpio "
                "from fixed-Saturn fall/storm case, then "
                "gives a separate alleged flux/poison case. "
                "Do not generalize all Saturn-fixed signs "
                "as identical or issue medical advice."
            ),
            (
                "Saturn with ninth ruler in twelfth and ninth "
                "ruler in Saturn's domicile are DIFFERENT "
                "source cases associated with murder vs theft. "
                "No real person danger warning is justified."
            ),
            (
                "The internal fortunate-regions section "
                "assigns historic zodiac Signs to Kingdoms "
                "and Cities by houses, planets and nodes. "
                "No reproducible country geometry or modern "
                "geographic baseline follows from the text."
            ),
            (
                "Original source positive glyph after Jupiter/"
                "Venus and negative after Saturn/Mars is "
                "not fully deciphered, and cannot be guessed "
                "as a particular North/South Node for runtime."
            ),
            (
                "The source explicitly refers to Part I "
                "printed page 93 for country-to-zodiac mapping. "
                "That separate table is NOT collated here."
            ),
            (
                "The 'avoid' rule includes alleged adverse "
                "seventh/sixth/eighth/fourth-house signs, "
                "malefic occupation and absent Jupiter/Venus "
                "benefic aspect; do not apply as actual travel "
                "destination planning or religious judgment."
            ),
            (
                "No real birth-verified travel itineraries, "
                "danger or death registries, injuries, "
                "relative wealth data, actual destination "
                "choices or base-rate controls were used."
            ),
            (
                "The image-based packet contains short "
                "qualified source paraphrases and checksums, "
                "not a full diplomatic original transcription."
            ),
        ],
        "original_node_heraldic_glyphs_fully_verified": False,
        "geographical_zodiac_country_table_p93_verified": False,
        "independent_real_travel_hazard_predictions": 0,
        "person_travel_safety_or_criminality_forecasts_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06u",
        "status": "ORIGINAL_1647_TRAVEL_SUCCESS_HAZARDS_REGIONS_HISTORICAL_ONLY",
        "printed_chapter": "CXLI",
        "editorial_chapter": "CXLII",
        "record_count": 76,
        "first_record": "R8860",
        "last_record": "R8935",
        "substantive": 74,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [644, 645],
        "following_printed_chapter": "CXLII",
        "following_heading_pdf": 645,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "independently_verified_real_travel_outcomes": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06u",
        "status": "FIRST_EDITION_TRAVEL_SUCCESS_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 8859,
        "new_historical_annotations": 76,
        "lilly_if_published": 8935,
        "ptolemy_retained": 1066,
        "combined_if_published": 10001,
        "substantive": 74,
        "navigation": 2,
        "source_groups": 6,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXLII",
        "next_original_pdf": 645,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "empirical_validations": 0,
        "travel_safety_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("Original CXLI travel success: 76 historic R8860–R8935; corpus 10001.")
