#!/usr/bin/env python3
"""Freeze first-edition CLXI fixed-star source records without human promotions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
FILES = sorted(B.glob("SOURCE_PART_0*.json"))


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(name, x):
    (B / name).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert len(FILES) == 2
window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
stars = load(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json")
assert window["next_R"] == "R11326"
assert window["accepted_before_clxi"] == 11325
assert window["chinese_v2_records"] == 97
assert stars["entries_count"] == len(stars["entries"]) == 14
assert sum(x["historical_degree"] is None for x in stars["entries"]) == 1
assert all(not x["modern_epoch_longitude_validated"] for x in stars["entries"])

groups = []
for ordinal, f in enumerate(FILES, 1):
    part = load(f)
    assert part["part"] == ordinal and part["batch"] == "B07r"
    assert part["source_only"] and part["runtime_promotions"] == 0
    groups += part["groups"]
assert len(groups) == 12
rows = []
groups_reversible = []
inverse = []
seen_roles = set()
for i, g in enumerate(groups, 1):
    span = f"B07r-S{i:03d}"
    pages = g["original_pdf_frames"]
    assert pages and pages == sorted(set(pages))
    assert set(pages) <= set((711, 712, 713))
    ids = []
    clauses = []
    for original in g["claims"]:
        role = original["role"]
        assert role not in seen_roles, role
        seen_roles.add(role)
        anchor = original["source_anchor_not_diplomatic"]
        meaning = original["historical_meaning_only"]
        qualifier = original["qualification"]
        assert len(anchor) >= 5 and len(meaning) >= 29 and qualifier
        number = 11326 + len(rows)
        rid = f"R{number}"
        clauses.append(
            dict(
                id=rid,
                role=role,
                source_anchor_not_diplomatic=anchor,
                historical_meaning_only=meaning,
                qualification=qualifier,
                source_only=True,
                individual_human_direction_outcome_validated=False,
                real_person_medical_danger_religion_morality_label_authorized=False,
                runtime_promoted=False,
            )
        )
        rows.append(
            dict(
                id=rid,
                record_number=number,
                batch="B07r",
                source_span=span,
                original_pdf_frames=pages,
                role=role,
                source_anchor_not_diplomatic=anchor,
                historical_meaning_only=meaning,
                qualification=qualifier,
                historical_source_documented=True,
                independent_real_event_timing_accuracy_validated=False,
                independent_health_or_death_prediction_validated=False,
                independent_relationship_or_financial_prediction_validated=False,
                independent_faith_personality_or_crime_label_validated=False,
                original_directions_angle_date_conversion_verified=False,
                original_1647_fixed_star_modern_epoch_parity_verified=False,
                real_person_health_safety_social_status_advice_authorized=False,
                runtime_model_promoted=False,
            )
        )
        ids.append(rid)
    groups_reversible.append(
        dict(
            source_span=span,
            original_pdf_frames=pages,
            topic=g["topic"],
            claims=clauses,
        )
    )
    inverse.append(
        dict(
            source_span=span,
            original_pdf_frames=pages,
            source_group=g["topic"],
            mapped_record_ids=ids,
        )
    )
assert len(rows) == 90, (len(rows), list(seen_roles))
assert [x["record_number"] for x in rows] == list(range(11326, 11416))
assert [x["role"] for x in rows[-2:]] == ["next_clxii", "next_sun_intro"]
photos = {}
for n in range(711, 715):
    x = window["photos"][str(n)]
    picture = B / x["file"]
    raw = picture.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8")
    assert (sha(picture), picture.stat().st_size) == (x["sha256"], x["bytes"])
    photos[str(n)] = x

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    dict(
        batch="B07r",
        original_source=window["source"],
        status="FIRST_EDITION_CLXI_MIDHEAVEN_FIXED_STARS_SOURCE_FIRST",
        printed_chapter="CLXI",
        body_pdf_frames=[711, 712, 713],
        next_heading_frame=713,
        following_printed="CLXII",
        groups=groups_reversible,
        real_person_direction_outcomes_validated=0,
        runtime_promotions=0,
        source_only=True,
    ),
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    dict(
        batch="B07r",
        source_groups=inverse,
        source_group_count=12,
        historical_records=90,
        substantive=88,
        following_navigation=2,
        fixed_star_table="FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json",
        source_parts=[f.name for f in FILES],
    ),
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    dict(
        batch="B07r",
        source=window["source"],
        full_original_pdf_sha256=window["original_full_pdf_sha256"],
        body_frames=[711, 712, 713],
        following_heading_frame=713,
        photos=photos,
    ),
)
save(
    "RULES.json",
    dict(
        batch="B07r",
        status="FIRST_EDITION_CLXI_FIXED_STARS_HISTORICAL_ONLY",
        printed_chapter="CLXI",
        record_count=90,
        first_record="R11326",
        last_record="R11415",
        substantive=88,
        following_navigation=2,
        source_groups=12,
        original_pdf_frames=[711, 712, 713],
        next_chapter="CLXII",
        full_original_glyph_collation_completed=False,
        original_star_epoch_parity_verified=False,
        primary_directions_date_engine_verified=False,
        empirical_human_validations=0,
        runtime_promotions=0,
        rules=rows,
    ),
)
save(
    "HIGH_STAKES_NONPROMOTION_GUARD_V1.json",
    dict(
        batch="B07r",
        historical_documentary_only=True,
        independent_human_outcomes_validated=0,
        runtime_rules_promoted=0,
        source_1647_fixed_star_positions_are_modern_identifications=False,
        original_1647_zodiac_epoch_and_precession_verified=False,
        natal_direction_arc_to_date_calculation_verified=False,
        violence_crime_capital_punishment_health_safety_predictions_allowed=False,
        class_gender_religion_morality_interpretation_for_actual_people_allowed=False,
        historical_conditionals_and_counterexamples_retained=True,
    ),
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    dict(
        batch="B07r",
        original_diplomatic_glyph_transcription_complete=False,
        right_shoulder_orion_coordinate_missing_here=True,
        star_name_modern_parity_verified=False,
        printed_astrological_epoch_verified=False,
        original_primary_direction_time_engine_verified=False,
        real_person_predictions_verified=False,
        original_label_Goat_vs_Goats_and_historical_asterism_unresolved=True,
        high_stakes_author_anecdotes_not_empirical_evidence=True,
    ),
)
save(
    "ACCEPTANCE.json",
    dict(
        batch="B07r",
        candidate_status="DOCUMENTARY_FOCUSED_VERIFICATION_PENDING",
        prior_lilly=11325,
        prior_ptolemy=1066,
        parallel_chinese=97,
        new_historical_annotations=90,
        substantive=88,
        following_navigation=2,
        numbered_chapters_added=1,
        lilly_if_accepted=11415,
        western_if_accepted=12481,
        next_record="R11416",
        original_pdf_frames=[711, 712, 713],
        next_printed_chapter="CLXII",
        source_group_count=12,
        period_star_entries=14,
        rules_sha256=sha(B / "RULES.json"),
        table_sha256=sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json"),
        empirical_human_validations=0,
        runtime_promotions=0,
    ),
)
print("B07r frozen 90 source notes 12 reversible passages; next R11416; index untouched")
