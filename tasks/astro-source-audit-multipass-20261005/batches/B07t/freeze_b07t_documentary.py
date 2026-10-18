#!/usr/bin/env python3
"""Source-first freeze of original 1647 printed CLXIII, no person forecast."""

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
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert len(PARTS) == 2
window = load("ORIGINAL_SOURCE_WINDOW_V1.json")
stars = load("FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json")
assert window["parent_accepted_lilly"] == 11721
assert window["next_historical_id"] == "R11722"
assert window["next_heading_pdf"] == 725
assert window["separate_chinese_v2"] == 97
assert stars["source_distinct_heading_groups"] == 11
assert stars["source_distinct_named_stellar_coordinate_entries"] == len(stars["entries"]) == 13
assert all(not e["modern_star_identity_verified"] for e in stars["entries"])
assert all(not e["epoch_and_precession_parity_verified"] for e in stars["entries"])
assert sum(e["minute_as_printed"] is None for e in stars["entries"]) == 12
assert sum(e["degree_as_printed"] is None for e in stars["entries"]) == 2

original_groups = []
for part_index, file in enumerate(PARTS, 1):
    part = json.loads(file.read_text(encoding="utf-8"))
    assert part["part"] == part_index and part["batch"] == "B07t"
    assert part["source_only"] and not part["runtime_promotions"]
    assert not part["independent_human_predictions_validated"]
    original_groups.extend(part["groups"])
assert len(original_groups) == 13

rows, reconstructed, inverse = [], [], []
roles = set()
for i, group in enumerate(original_groups, 1):
    span = f"B07t-S{i:03d}"
    pages = group["original_pdf_frames"]
    assert pages and set(pages) <= {723, 724, 725}
    assert pages == sorted(set(pages))
    ids, historical_claims = [], []
    for claim in group["claims"]:
        role = claim["role"]
        anchor = claim["source_anchor_not_diplomatic"]
        meaning = claim["historical_meaning_only"]
        qualification = claim["qualification"]
        assert role and role not in roles
        roles.add(role)
        assert len(anchor) >= 5 and len(meaning) >= 20 and qualification
        number = 11722 + len(rows)
        rid = f"R{number}"
        historical_claims.append(
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
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B07t",
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
    reconstructed.append(
        {
            "source_span": span,
            "original_pdf_frames": pages,
            "topic": group["topic"],
            "claims": historical_claims,
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

assert len(rows) == 104 and len(roles) == 104
assert [r["record_number"] for r in rows] == list(range(11722, 11826))
assert [r["role"] for r in rows[-2:]] == [
    "next_clxiiii_heading",
    "next_moon_saturn",
]
photos = {}
for n in (723, 724, 725):
    photo = window["photos"][str(n)]
    file = B / photo["file"]
    assert file.stat().st_size == photo["bytes"]
    assert sha(file) == photo["sha256"]
    photos[str(n)] = photo
save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    {
        "batch": "B07t",
        "printed_chapter": "CLXIII",
        "source": window["source"],
        "original_pdf_frames": [723, 724, 725],
        "next_printed_chapter": "CLXIIII",
        "next_heading_pdf": 725,
        "source_only": True,
        "groups": reconstructed,
        "independent_human_predictions_validated": 0,
        "runtime_promotions": 0,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07t",
        "source_groups": inverse,
        "source_group_count": 13,
        "historical_records": 104,
        "substantive": 102,
        "next_navigation": 2,
        "stellar_table": "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json",
        "source_parts": [p.name for p in PARTS],
    },
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07t",
        "source": window["source"],
        "full_original_pdf_sha256": window["full_source_894_frame_pdf_sha256"],
        "body_original_pdf_frames": [723, 724, 725],
        "following_heading_pdf": 725,
        "photos": photos,
    },
)
save(
    "RULES.json",
    {
        "batch": "B07t",
        "printed_chapter": "CLXIII",
        "status": "ORIGINAL_1647_SUN_FIXED_STARS_HISTORICAL_ONLY",
        "record_count": 104,
        "first_record": "R11722",
        "last_record": "R11825",
        "substantive": 102,
        "following_navigation": 2,
        "source_groups": 13,
        "source_pdf_frames": [723, 724, 725],
        "following_printed": "CLXIIII",
        "following_heading_original_pdf": 725,
        "full_original_glyph_collation_completed": False,
        "epoch_stellar_parity_verified": False,
        "primary_directions_time_engine_verified": False,
        "empirical_human_validations": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    {
        "batch": "B07t",
        "historical_source_only": True,
        "independent_human_outcomes_validated": 0,
        "runtime_rules_promoted": 0,
        "physical_source_chapter_seams_verified": True,
        "printed_star_pairs_separate_from_independent_prediction_samples": True,
        "original_star_epoch_parity_verified": False,
        "primary_directions_arc_age_date_engine_verified": False,
        "crime_mortality_disease_religion_gender_morality_real_person_predictions_permitted": False,
        "conditioned_benefit_and_explicit_negative_reversals_retained": True,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07t",
        "complete_diplomatic_glyph_transcription": False,
        "printed_solar_fixed_star_epoch_unverified": True,
        "modern_star_names_not_verified": True,
        "Cheles_paired_individual_identifications_unverified": True,
        "two_Asses_north_south_degree_assignments_unverified": True,
        "meaning_and_source_commentary_not_expert_independent_reviewed": True,
        "individual_predictive_accuracy_unverified": True,
        "author_anecdotes_not_independent_samples": True,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B07t",
        "candidate_status": "DOCUMENTARY_PENDING_ARCHIVE_AND_REVIEW",
        "prior_lilly": 11721,
        "prior_ptolemy": 1066,
        "parallel_chinese_source_notes": 97,
        "new_historical_annotations": 104,
        "substantive": 102,
        "following_navigation": 2,
        "numbered_chapters_added": 1,
        "lilly_if_accepted": 11825,
        "western_if_accepted": 12891,
        "next_record": "R11826",
        "source_group_count": 13,
        "stellar_entries": 13,
        "source_photo_frames": 3,
        "next_chapter": "CLXIIII",
        "rules_sha256": sha(B / "RULES.json"),
        "fixed_star_table_sha256": sha(B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json"),
        "empirical_human_validations": 0,
        "runtime_promotions": 0,
    },
)
print("Freeze B07t: 104 historical source records R11722-R11825; index unchanged")
