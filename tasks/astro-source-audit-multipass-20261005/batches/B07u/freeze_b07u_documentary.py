#!/usr/bin/env python3
"""Original 1647 first-edition Moon-to-Promittors source-only reversible freeze."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
FILES = sorted(B.glob("SOURCE_PART_0*.json"))


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


assert len(FILES) == 4
win = load("ORIGINAL_SOURCE_WINDOW_V1.json")
assert win["accepted_lilly_before"] == 11825
assert win["first_unaccepted_source_record"] == "R11826"
assert win["accepted_chinese_v2"] == 97
assert win["accepted_ptolemy"] == 1066
assert win["body_frames"] == list(range(725, 736))
assert win["following_heading_original_pdf"] == 735
assert win["following_heading_numbered"] is False

original_groups = []
for index, file in enumerate(FILES, 1):
    part = json.loads(file.read_text(encoding="utf-8"))
    assert part["batch"] == "B07u" and part["part"] == index
    assert part["source_only"]
    assert not part["independent_human_predictions_validated"]
    assert not part["runtime_promotions"]
    original_groups.extend(part["groups"])
assert len(original_groups) == 41

rules, authoring_groups, mapping = [], [], []
roles = set()
for group_index, g in enumerate(original_groups, 1):
    span = f"B07u-S{group_index:03d}"
    pages = g["original_pdf_frames"]
    assert pages and pages == sorted(set(pages))
    assert set(pages) <= set(range(725, 736))
    ids, clause_records = [], []
    for c in g["claims"]:
        role = c["role"]
        anchor = c["source_anchor_not_diplomatic"]
        meaning = c["historical_meaning_only"]
        qualification = c["qualification"]
        assert role and role not in roles
        assert len(anchor) >= 5 and len(meaning) >= 20 and qualification
        roles.add(role)
        number = 11826 + len(rules)
        rid = f"R{number}"
        clause_records.append(
            {
                "id": rid,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": qualification,
                "source_only": True,
                "individual_human_direction_outcome_validated": False,
                "real_person_medical_danger_religion_morality_label_authorized": False,
                "runtime_promoted": False,
            }
        )
        rules.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07u",
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
    authoring_groups.append(
        {
            "source_span": span,
            "original_pdf_frames": pages,
            "topic": g["topic"],
            "claims": clause_records,
        }
    )
    mapping.append(
        {
            "source_span": span,
            "original_pdf_frames": pages,
            "source_group": g["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == len(roles) == 343
assert [r["record_number"] for r in rules] == list(range(11826, 12169))
assert [r["role"] for r in rules[-2:]] == [
    "next_unnumbered_moon_stars",
    "next_moon_rigel",
]

photos = {}
for i in range(725, 737):
    x = win["photos"][str(i)]
    pic = B / x["file"]
    assert pic.stat().st_size == x["bytes"] and sha(pic) == x["sha256"]
    photos[str(i)] = x

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    {
        "batch": "B07u",
        "printed_chapter": "CLXIIII",
        "source": win["source"],
        "body_original_pdf_frames": list(range(725, 736)),
        "following_unnumbered_heading_pdf": 735,
        "following_unnumbered_heading": "Moon Directed to FIXED STARRES",
        "source_only": True,
        "groups": authoring_groups,
        "independent_real_human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07u",
        "source_groups": mapping,
        "source_group_count": 41,
        "historical_records": 343,
        "substantive": 341,
        "following_navigation": 2,
        "source_parts": [f.name for f in FILES],
    },
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07u",
        "source": win["source"],
        "full_source_pdf_sha256": win["full_source_pdf_sha256"],
        "body_original_pdf_frames": list(range(725, 736)),
        "following_unnumbered_heading_pdf": 735,
        "following_context_pdf": 736,
        "photos": photos,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07u",
        "status": "ORIGINAL_1647_CLXIIII_MOON_DIRECTIONS_HISTORICAL_ONLY",
        "printed_chapter": "CLXIIII",
        "record_count": 343,
        "first_record": "R11826",
        "last_record": "R12168",
        "substantive": 341,
        "following_navigation": 2,
        "source_groups": 41,
        "body_pdf_frames": list(range(725, 736)),
        "following_unnumbered_heading_pdf": 735,
        "following_unnumbered_heading": "Moon Directed to FIXED STARRES",
        "full_original_diplomatic_glyphs_verified": False,
        "original_angle_year_time_engine_verified": False,
        "independent_human_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    {
        "batch": "B07u",
        "historical_source_only": True,
        "printed_numbered_chapter_separated_from_unnumbered_star_section": True,
        "individual_human_predictions_validated": 0,
        "runtime_model_promotions": 0,
        "old_four_humors_disease_claims_not_modern_diagnoses": True,
        "class_gender_morality_crime_mortality_claims_not_real_person_labels": True,
        "natal_aph_hyleg_anareta_and_fixed_star_checks_unverified": True,
        "duration_and_1647_calendar_engine_unverified": True,
        "opposed_favorable_and_adverse_outcomes_retained": True,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07u",
        "all_old_glyphs_diplomatically_collated": False,
        "original_first_edition_source_meaning_independently_expert_reviewed": False,
        "full_natal_ephemeris_calendar_or_arctoage_parity": False,
        "hyleg_anareta_and_profection_math_verified": False,
        "actual_human_illness_mortality_law_or_economic_predictions_validated": False,
        "old_genders_and_classes_historical_only": True,
        "later_unnumbered_moon_fixed_star_heading_separate": True,
        "original_annual_measure_table_followup_separate": True,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07u",
        "candidate_status": "SOURCE_RECORDS_PREPARED_PENDING_ARCHIVE_ACCEPTANCE",
        "prior_lilly": 11825,
        "prior_ptolemy": 1066,
        "parallel_chinese_history": 97,
        "new_historical_annotations": 343,
        "substantive": 341,
        "following_navigation": 2,
        "numbered_chapters_added": 1,
        "lilly_if_accepted": 12168,
        "western_if_accepted": 13234,
        "next_historical_record": "R12169",
        "next_unnumbered_heading": "Moon Directed to Fixed Starres",
        "next_original_pdf": 735,
        "source_group_count": 41,
        "source_images_count": 12,
        "original_source_pdf_sha256": win["full_source_pdf_sha256"],
        "rules_sha256": sha(B / "RULES.json"),
        "independent_real_human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
print("Frozen: B07u 343 historic source notes R11826-R12168; 41 groups; index unchanged")
