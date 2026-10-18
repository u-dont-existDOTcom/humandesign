#!/usr/bin/env python3
"""Freeze first-edition Part-of-Fortune historical notes, without model promotion."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARTS = sorted(B.glob("SOURCE_PART_0*.json"))


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


assert len(PARTS) == 3
window = load("ORIGINAL_SOURCE_WINDOW_V1.json")
stars = load("FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json")
assert window["parent_accepted_lilly"] == 12268
assert window["first_new_historical_record"] == "R12269"
assert window["printed_numeral"] == "CLXV"
assert window["body_pdf_frames"] == list(range(737, 743))
assert window["following_chapter"] == "CLXVI"
assert window["following_heading_pdf"] == 742
assert window["parallel_chinese_v2_source_notes"] == 97
assert stars["historical_headings"] == len(stars["entries"]) == 3
assert all(
    e["original_printed_longitude_degree"] is None
    and e["original_printed_longitude_minute"] is None
    and e["original_printed_sign"] is None
    and not e["star_catalog_id_validated"]
    for e in stars["entries"]
)

source_groups = []
for ordinal, file in enumerate(PARTS, 1):
    part = json.loads(file.read_text(encoding="utf-8"))
    assert part["batch"] == "B07w" and part["part"] == ordinal
    assert part["source_only"] and part["human_predictions_validated"] == 0
    assert part["runtime_promotions"] == 0
    source_groups.extend(part["groups"])
assert len(source_groups) == 35

rules, mapped, groups, seen_roles = [], [], [], set()
for i, original in enumerate(source_groups, 1):
    span = f"B07w-S{i:03d}"
    pages = original["original_pdf_frames"]
    assert pages == sorted(set(pages))
    assert pages and set(pages) <= set(range(737, 743))
    ids, claims = [], []
    for c in original["claims"]:
        role = c["role"]
        anchor = c["source_anchor_not_diplomatic"]
        meaning = c["historical_meaning_only"]
        qualification = c["qualification"]
        assert role not in seen_roles, role
        assert len(anchor) >= 5 and len(meaning) >= 15 and qualification
        seen_roles.add(role)
        number = 12269 + len(rules)
        rid = f"R{number}"
        claims.append(
            {
                "id": rid,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": qualification,
                "source_only": True,
                "independent_human_outcomes_validated": False,
                "real_person_health_safety_legal_morality_inference_authorized": False,
                "runtime_promoted": False,
            }
        )
        rules.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07w",
                "source_span": span,
                "original_pdf_frames": pages,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": qualification,
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
            "source_span": span,
            "original_pdf_frames": pages,
            "topic": original["topic"],
            "claims": claims,
        }
    )
    mapped.append(
        {
            "source_span": span,
            "original_pdf_frames": pages,
            "source_group": original["topic"],
            "mapped_record_ids": ids,
        }
    )

assert len(rules) == len(seen_roles) == 204
assert [r["record_number"] for r in rules] == list(range(12269, 12473))
assert [r["role"] for r in rules[-3:]] == [
    "next_clxvi",
    "next_age_relevance",
    "next_ptolemy_methods",
]
assert [g["source_span"] for g in groups] == [f"B07w-S{i:03d}" for i in range(1, 36)]

photos = {}
for n in range(737, 744):
    p = window["photos"][str(n)]
    file = B / p["file"]
    assert file.stat().st_size == p["bytes"] and sha(file) == p["sha256"]
    photos[str(n)] = p

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    {
        "batch": "B07w",
        "printed_chapter": "CLXV",
        "source": window["source"],
        "body_pdf_frames": list(range(737, 743)),
        "next_chapter": "CLXVI",
        "next_heading_pdf": 742,
        "source_only": True,
        "groups": groups,
        "independent_human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07w",
        "source_groups": mapped,
        "source_group_count": 35,
        "historical_records": 204,
        "substantive": 201,
        "following_navigation": 3,
        "source_parts": [f.name for f in PARTS],
        "source_star_heading_table": "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json",
    },
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07w",
        "source": window["source"],
        "full_original_pdf_sha256": window["full_pdf_original_sha256"],
        "body_pdf_frames": list(range(737, 743)),
        "following_heading_pdf": 742,
        "photos": photos,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07w",
        "status": "ORIGINAL_1647_CLXV_FORTUNE_DIRECTIONS_HISTORICAL_ONLY",
        "printed_chapter": "CLXV",
        "record_count": 204,
        "first_record": "R12269",
        "last_record": "R12472",
        "substantive": 201,
        "following_navigation": 3,
        "source_groups": 35,
        "body_pdf_frames": list(range(737, 743)),
        "following_printed": "CLXVI",
        "following_heading_pdf": 742,
        "full_original_diplomatic_text_collated": False,
        "modern_star_epoch_parity_verified": False,
        "original_direction_arc_to_year_engine_verified": False,
        "empirical_human_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    {
        "batch": "B07w",
        "historical_source_only": True,
        "planetary_conjunction_sextile_trine_combinations_as_original": True,
        "historical_star_without_longitude_not_silently_modernized": True,
        "unnumbered_house_cusp_subheading_counted_as_new_chapter": False,
        "original_direction_numerical_math_verified": False,
        "independent_real_person_predictive_accuracy_validated": False,
        "real_person_crime_sex_gender_class_health_safety_money_inference_permitted": False,
        "favorable_adverse_source_counterexamples_retained": True,
        "author_retrospective_anecdote_not_blinded_evidence": True,
        "runtime_rules_promoted": 0,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07w",
        "full_original_glyph_diplomatic_transcription_completed": False,
        "semantic_edition_critical_independent_expert_review_completed": False,
        "source_star_era_and_catalog_identifications_verified": False,
        "quantitative_directions_year_conversion_verified": False,
        "empirical_human_accuracy_trials_completed": False,
        "following_CLXVI_is_independent_numerical_method": True,
        "Chinese_bazi_ziwei_calendar_parity_not_implied": True,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07w",
        "status": "ORIGINAL_SOURCE_DOCUMENTARY_PENDING_REPLAY",
        "prior_lilly": 12268,
        "prior_ptolemy": 1066,
        "parallel_chinese": 97,
        "new_historical_annotations": 204,
        "substantive": 201,
        "following_navigation": 3,
        "numbered_chapters_added": 1,
        "lilly_if_accepted": 12472,
        "western_if_accepted": 13538,
        "next_id": "R12473",
        "next_chapter": "CLXVI",
        "next_source_pdf": 742,
        "source_groups": 35,
        "three_star_headings_without_coordinates": 3,
        "original_photos": 7,
        "rules_sha256": sha(B / "RULES.json"),
        "star_table_sha256": sha(B / "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json"),
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
print("B07w freeze: 204 source-only records R12269–R12472, 35 original groups.")
