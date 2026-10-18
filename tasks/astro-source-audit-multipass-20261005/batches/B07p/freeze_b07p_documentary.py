#!/usr/bin/env python3
"""Original first-edition Lilly CLIX: source-first freeze without person forecasts."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARTS = sorted(B.glob("SOURCE_PART_0*.json"))


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert len(PARTS) == 4
all_groups = []
for ordinal, file in enumerate(PARTS, 1):
    part = load(file)
    assert part["batch"] == "B07p" and part["part"] == ordinal
    all_groups.extend(part["groups"])
assert len(all_groups) == 17
assert [g["source_span"] for g in all_groups] == [f"B07p-S{x:03d}" for x in range(1, 18)]

rows, mapped, groups = [], [], []
for original in all_groups:
    sid = original["source_span"]
    pages = original["p"]
    assert pages and set(pages) <= set(range(691, 703))
    ids = []
    claims = []
    for role, anchor, meaning, qualifier in original["r"]:
        number = 10733 + len(rows)
        rid = f"R{number}"
        assert role and len(anchor) >= 5 and len(meaning) >= 38
        assert qualifier
        historic = {
            "id": rid,
            "role": role,
            "source_anchor_not_diplomatic": anchor,
            "historical_meaning_only": meaning,
            "qualification": qualifier,
            "source_only": True,
            "individual_human_direction_outcome_validated": False,
            "real_person_medical_danger_religion_morality_label_authorized": False,
            "runtime_promoted": False,
        }
        claims.append(historic)
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07p",
                "source_span": sid,
                "original_pdf_frames": pages,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": qualifier,
                "historical_source_documented": True,
                "independent_real_event_timing_accuracy_validated": False,
                "independent_health_or_death_prediction_validated": False,
                "independent_relationship_or_financial_prediction_validated": False,
                "independent_faith_personality_or_crime_label_validated": False,
                "original_directions_angle_date_conversion_verified": False,
                "original_1647_fixed_star_modern_epoch_parity_verified": False,
                "real_person_health_safety_social_status_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    groups.append(
        {
            "source_span": sid,
            "original_pdf_frames": pages,
            "topic": original["topic"],
            "claims": claims,
        }
    )
    mapped.append(
        {
            "source_span": sid,
            "original_pdf_frames": pages,
            "source_group": original["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 335
assert [x["record_number"] for x in rows] == list(range(10733, 11068))
assert [x["id"] for x in rows if x["role"].startswith("next_CLX")] == ["R11065", "R11066", "R11067"]
assert len(set(x["role"] for x in rows)) == 335
assert len(set(x["id"] for x in rows)) == 335

star_table = load(B / "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json")
assert len(star_table["entries"]) == 16
assert star_table["printed_chapter"] == "CLIX"
assert not star_table["calculational_parity_verified"]
assert star_table["independent_person_predictions_validated"] == 0
assert all(
    not e["modern_star_identity_validated"] and not e["modern_ephemeris_longitude_parity_validated"]
    for e in star_table["entries"]
)
assert [x["source_table_row"] for x in star_table["entries"]] == list(range(1, 17))

photos = {}
for frame in range(691, 704):
    file = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = file.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    photos[str(frame)] = {
        "file": str(file.relative_to(B)),
        "sha256": sha(file),
        "bytes": len(raw),
        "printed_folio": str(frame - 34),
        "source_role": (
            "CLIX_original_1647_body" if frame <= 702 else "following_printed_CLX_context_only"
        ),
    }

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    {
        "batch": "B07p",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition Wellcome b30338724"
        ),
        "status": "FIRST_EDITION_CLIX_ASCENDANT_DIRECTION_SOURCE_FIRST",
        "printed_chapter": "CLIX",
        "body_pdf_frames": list(range(691, 703)),
        "following_printed": "CLX",
        "following_heading_original_pdf": 702,
        "groups": groups,
        "source_only": True,
        "real_person_directions_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07p",
        "source": (
            "William Lilly 1647 Christian Astrology original first edition Wellcome b30338724"
        ),
        "full_original_1647_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_original_pdf_frames": list(range(691, 703)),
        "following_printed_CLX_heading_pdf": 702,
        "images": photos,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07p",
        "source_groups": mapped,
        "source_group_count": 17,
        "historical_records": 335,
        "substantive": 332,
        "next_navigation": 3,
        "fixed_star_source_table": "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json",
        "source_parts": [p.name for p in PARTS],
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07p",
        "issues": [
            (
                "Printed CLIX occupies original PDF691 lower through PDF702 upper. "
                "Distinct CLX 'Directions of the Mid-heaven to Promittors' "
                "starts after horizontal divider later the SAME PDF702."
            ),
            (
                "The title suggests direction of Ascendant to Jupiter, "
                "but source contains separate Jupiter/Mars/Sun/Venus/Mercury/"
                "Moon body/soft/hard/terms, lunar nodes, Part Fortune, "
                "second-third-fourth cusps and named fixed stars."
            ),
            (
                "Do not treat body, sextile/trine, square/opposition, terms, "
                "cusp and star directions as equivalent, nor mix the "
                "different radial/sinister/dexter source cases."
            ),
            (
                "The source's success, property, marriage, parenting, fame, "
                "comfort, ill health, accidents, imprisonment, supposed "
                "crime and mortality all have independent target "
                "definitions; broad alternatives cannot rescue failures."
            ),
            (
                "Several severe historic danger/death claims are subject "
                "to hyleg/anareta/another malefic/violent fixed-star, "
                "radix-position, solar sign, year/age, or social-class "
                "prerequisites; omission creates a false unconditional rule."
            ),
            (
                "Historical health labels such as blood disorders, flux, "
                "dropsy, liver afflictions, melancholy, drowning and "
                "various injuries do not constitute valid diagnosis, "
                "disease risk, treatment recommendations or person advice."
            ),
            (
                "The source assigns sexual, reproductive, gender, "
                "religious and criminal stereotypes as presumed "
                "planetary effects; actual people must never be "
                "classified from these documentary assertions."
            ),
            (
                "Source repeatedly adjusts economic/honor outcomes by "
                "birth circumstance: royal rulers, clergy, merchants, "
                "craftspeople and poor people get different claims "
                "under a nominally common direction."
            ),
            (
                "The original 16 fixed-star/asterism sources have "
                "period zodiac sign/degree entries. Their exact "
                "modern star identity, longitude epoch, precession "
                "correction, stellar-motion parity and direction "
                "orbs are not verified. Some minute values are "
                "missing or ambiguous in original printed lines."
            ),
            (
                "Previous chapter CLVIII includes Ascendant-to-Saturn "
                "conditions on PDF690–691; do not re-admit as CLIX. "
                "Following printed CLX begins in same PDF702, "
                "and does not belong to current body."
            ),
            (
                "No original arc-to-date algorithm, birth time rectification "
                "quality, astronomical sign accuracy, Regiomontanus "
                "latitude calculation, zodiac epoch or event window "
                "for this complex primary-directions passage "
                "has been independently verified."
            ),
            (
                "The fixed-stars section includes pejorative "
                "claims about people of particular gender/class, "
                "sexual preferences, criminal conduct and mental "
                "or social dispositions. Historical bias, not facts."
            ),
            (
                "No live or historical verified human lives/birth "
                "times/time-to-event records, independent age "
                "comparators or prospective blind predictions "
                "were evaluated. Zero personal applications."
            ),
            (
                "Source images support short exact/reversible anchors "
                "and qualified paraphrases, not full diplomatic "
                "transcription or independently verified "
                "modern angular/date calculations."
            ),
        ],
        "source_full_diplomatic_transcription_complete": False,
        "original_all_glyphs_verified": False,
        "original_fixed_star_modern_longitude_epoch_parity": False,
        "original_primary_directions_time_engine_verified": False,
        "independent_human_event_timing_predictions": 0,
        "real_person_medical_criminal_religious_or_safety_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07p",
        "status": "ORIGINAL_1647_CLIX_ASCENDANT_DIRECTIONS_HISTORICAL_ONLY",
        "printed_chapter": "CLIX",
        "record_count": 335,
        "first_record": "R10733",
        "last_record": "R11067",
        "substantive": 332,
        "following_navigation": 3,
        "source_groups": 17,
        "body_pdf_frames": list(range(691, 703)),
        "following_printed": "CLX",
        "following_heading_original_pdf": 702,
        "original_fixed_star_table": "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json",
        "full_original_glyph_collation_completed": False,
        "primary_directions_chart_engine_verified": False,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07p",
        "status": "FIRST_EDITION_CLIX_SOURCE_LOCALLY_FROZEN",
        "prior_lilly": 10732,
        "new_historical_annotations": 335,
        "lilly_if_published": 11067,
        "ptolemy_retained": 1066,
        "combined_if_published": 12133,
        "substantive": 332,
        "navigation": 3,
        "source_groups": 17,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CLX",
        "next_original_pdf": 702,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "fixed_star_source_table_sha256": sha(B / "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json"),
        "empirical_validations": 0,
        "human_event_timing_predictions_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07p: 335 original historical CLIX records R10733–R11067; 16 fixed-star rows.")
