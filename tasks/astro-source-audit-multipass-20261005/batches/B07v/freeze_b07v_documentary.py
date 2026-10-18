#!/usr/bin/env python3
"""Original 1647 lunar fixed-star unnumbered source freeze; NOT empirical rules."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARTS = sorted(B.glob("SOURCE_PART_*.json"))


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


assert len(PARTS) == 2
w = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
stars = j(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json")
assert w["prior_lilly_records"] == 12168
assert w["first_new_historical_record"] == "R12169"
assert w["source_is_numbered_chapter"] is False
assert w["numbered_chapter_delta_on_acceptance"] == 0
assert w["following_printed_numbered_chapter"] == "CLXV"
assert w["following_printed_heading_original_pdf"] == 737
assert stars["source_star_entries"] == len(stars["entries"]) == 13
assert stars["source_heading_effects"] == 13
assert all(not x["modern_fixed_star_identity_verified"] for x in stars["entries"])

all_groups = []
for i, file in enumerate(PARTS, 1):
    part = j(file)
    assert part["batch"] == "B07v" and part["part"] == i
    assert part["numbered"] is False and part["source_only"]
    assert part["human_predictions_validated"] == part["runtime_promotions"] == 0
    all_groups.extend(part["groups"])
assert len(all_groups) == 15

rules, groups, inverse = [], [], []
used_roles = set()
for i, group in enumerate(all_groups, 1):
    span = f"B07v-S{i:03d}"
    pages = group["original_pdf_frames"]
    assert pages and pages == sorted(set(pages))
    assert set(pages) <= {735, 736, 737}
    ids, claims = [], []
    for source in group["claims"]:
        role = source["role"]
        anchor = source["source_anchor_not_diplomatic"]
        meaning = source["historical_meaning_only"]
        condition = source["qualification"]
        assert role not in used_roles and len(anchor) >= 5 and len(meaning) >= 20 and condition
        used_roles.add(role)
        number = 12169 + len(rules)
        rid = f"R{number}"
        claims.append(
            {
                "id": rid,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": condition,
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
                "batch": "B07v",
                "source_span": span,
                "original_pdf_frames": pages,
                "role": role,
                "source_anchor_not_diplomatic": anchor,
                "historical_meaning_only": meaning,
                "qualification": condition,
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
            "topic": group["topic"],
            "claims": claims,
        }
    )
    inverse.append(
        {
            "source_span": span,
            "original_pdf_frames": pages,
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == len(used_roles) == 100
assert [r["record_number"] for r in rules] == list(range(12169, 12269))
assert [r["role"] for r in rules[-2:]] == ["next_clxv_heading", "next_fortune_saturn"]
photos = {}
for page in range(735, 739):
    x = w["photos"][str(page)]
    file = B / x["file"]
    assert file.stat().st_size == x["bytes"] and sha(file) == x["sha256"]
    photos[str(page)] = x

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    {
        "batch": "B07v",
        "heading": "The Moon Directed to FIXED STARRES",
        "unnumbered": True,
        "source": w["source"],
        "original_pdf_frames": [735, 736, 737],
        "next_printed_chapter": "CLXV",
        "next_heading_pdf": 737,
        "groups": groups,
        "source_only": True,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07v",
        "source_group_count": 15,
        "source_groups": inverse,
        "historical_records": 100,
        "substantive": 98,
        "following_navigation": 2,
        "numbered_chapters_added": 0,
        "source_parts": [p.name for p in PARTS],
        "period_star_table": "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json",
    },
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07v",
        "source": w["source"],
        "full_original_pdf_sha256": w["original_full_pdf_sha256"],
        "body_original_pdf_frames": [735, 736, 737],
        "following_numbered_heading_pdf": 737,
        "following_context_pdf": 738,
        "photos": photos,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07v",
        "status": "UNNUMBERED_ORIGINAL_1647_MOON_FIXED_STARS_HISTORICAL_ONLY",
        "source_heading": "The Moon Directed to FIXED STARRES",
        "printed_numbered_chapter": None,
        "numbered_chapter_added": 0,
        "record_count": 100,
        "first_record": "R12169",
        "last_record": "R12268",
        "substantive": 98,
        "following_navigation": 2,
        "source_groups": 15,
        "source_pdf_frames": [735, 736, 737],
        "following_printed": "CLXV",
        "following_heading_original_pdf": 737,
        "complete_diplomatic_transcription_verified": False,
        "modern_star_identity_epoch_parity_verified": False,
        "primary_directions_time_engine_verified": False,
        "empirical_human_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    {
        "batch": "B07v",
        "unnumbered_source_unit": True,
        "historic_17th_century_stellar_assertions_only": True,
        "clinical_mortality_crime_gender_religion_morality_human_inference_allowed": False,
        "source_pairings_are_independent_prediction_samples": False,
        "modern_star_epoch_and_precession_verified": False,
        "hyleg_direction_time_engine_verified": False,
        "author_legacy_social_stereotypes_not_endorsed": True,
        "favorable_adverse_exceptions_and_prior_paragraph_dependencies_retained": True,
        "human_predictions_validated": 0,
        "runtime_model_promotions": 0,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07v",
        "original_all_glyphs_collated": False,
        "original_star_coordinate_modern_parity_verified": False,
        "original_moon_primary_direction_arc_year_engine_verified": False,
        "period_crime_death_health_moral_language_not_real_person_evidence": True,
        "independent_expert_sinologist_astrology_historian_review_completed": False,
        "original_1647_source_review_not_blind_empirical_validation": True,
        "annual_direction_time_table_a_later_separate_task": True,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07v",
        "candidate_status": "SOURCE_VERIFICATION_PENDING",
        "prior_lilly": 12168,
        "prior_ptolemy": 1066,
        "parallel_chinese": 97,
        "new_historical_annotations": 100,
        "substantive": 98,
        "following_navigation": 2,
        "numbered_chapters_added": 0,
        "unnumbered_source_units_added": 1,
        "lilly_if_accepted": 12268,
        "western_if_accepted": 13334,
        "next_record": "R12269",
        "next_printed_chapter": "CLXV",
        "next_source_original_pdf": 737,
        "source_group_count": 15,
        "source_star_entries": 13,
        "source_photo_frames": 4,
        "rules_sha256": sha(B / "RULES.json"),
        "star_table_sha256": sha(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json"),
        "empirical_human_validations": 0,
        "runtime_promotions": 0,
    },
)
print("B07v source freeze: 100 unnumbered historical R12169–R12268; next CLXV PDF737")
