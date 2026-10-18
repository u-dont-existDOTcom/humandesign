#!/usr/bin/env python3
"""Freeze original 1647 Lilly CLXII Sun directions; no human forecast or runtime promotion."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
FILES = sorted(B.glob("SOURCE_PART_0*.json"))


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


assert len(FILES) == 5
win = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert win["prior_accepted_lilly"] == 11415
assert win["new_source_record_starts"] == "R11416"
assert win["prior_retained_ptolemy"] == 1066
assert win["independent_chinese_v2_count"] == 97
assert win["printed_clxii"]["body_frames"] == list(range(713, 724))
assert win["following_printed_clxiii"]["starts_frame"] == 723
assert win["following_printed_clxiii"]["next_printed_clxiiii_heading_frame"] == 725

all_groups = []
for i, file in enumerate(FILES, 1):
    part = load(file)
    assert part["batch"] == "B07s" and part["part"] == i
    assert part["source_only"] and not part["human_predictive_validations"]
    assert not part["runtime_promotions"]
    all_groups.extend(part["groups"])
assert len(all_groups) == 40
rows = []
mapped = []
groups = []
seen_roles = set()
for ordinal, g in enumerate(all_groups, 1):
    sid = f"B07s-S{ordinal:03d}"
    pages = g["original_pdf_frames"]
    assert pages and pages == sorted(set(pages))
    assert set(pages) <= set(range(713, 724))
    items = []
    ids = []
    for c in g["claims"]:
        role = c["role"]
        anchor = c["source_anchor_not_diplomatic"]
        meaning = c["historical_meaning_only"]
        qualifier = c["qualification"]
        assert role not in seen_roles, role
        seen_roles.add(role)
        assert len(anchor) >= 5 and len(meaning) >= 18 and qualifier
        number = 11416 + len(rows)
        rid = f"R{number}"
        items.append(
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
                batch="B07s",
                source_span=sid,
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
    groups.append(
        dict(
            source_span=sid,
            original_pdf_frames=pages,
            topic=g["topic"],
            claims=items,
        )
    )
    mapped.append(
        dict(
            source_span=sid,
            original_pdf_frames=pages,
            source_group=g["topic"],
            mapped_record_ids=ids,
        )
    )
assert len(rows) == 306
assert len(seen_roles) == 306
assert [x["record_number"] for x in rows] == list(range(11416, 11722))
assert [x["role"] for x in rows[-2:]] == ["next_clxiii", "next_rigel"]
assert [x["source_span"] for x in groups] == [f"B07s-S{i:03d}" for i in range(1, 41)]

photos = {}
for n in range(713, 726):
    p = win["photos"][str(n)]
    file = B / p["file"]
    assert sha(file) == p["sha256"] and file.stat().st_size == p["bytes"]
    photos[str(n)] = p
save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    dict(
        batch="B07s",
        source=win["source"],
        status="FIRST_EDITION_CLXII_SUN_DIRECTIONS_HISTORICAL_SOURCE_ONLY",
        printed_chapter="CLXII",
        body_pdf_frames=list(range(713, 724)),
        following_chapter="CLXIII",
        following_heading_frame=723,
        groups=groups,
        source_only=True,
        individual_human_predictions_validated=0,
        runtime_promotions=0,
    ),
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    dict(
        batch="B07s",
        source_groups=mapped,
        source_group_count=40,
        historical_records=306,
        substantive=304,
        following_navigation=2,
        source_parts=[x.name for x in FILES],
    ),
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    dict(
        batch="B07s",
        source=win["source"],
        full_original_pdf_sha256=win["original_pdf_sha256"],
        full_original_pdf_bytes=win["original_pdf_bytes"],
        body_original_pdf_frames=list(range(713, 724)),
        following_printed_clxiii_heading_frame=723,
        following_printed_clxiiii_heading_frame=725,
        photos=photos,
    ),
)
save(
    "RULES.json",
    dict(
        batch="B07s",
        status="ORIGINAL_1647_CLXII_SUN_DIRECTIONS_HISTORICAL_ONLY",
        printed_chapter="CLXII",
        record_count=306,
        first_record="R11416",
        last_record="R11721",
        substantive=304,
        following_navigation=2,
        source_groups=40,
        body_pdf_frames=list(range(713, 724)),
        following_printed="CLXIII",
        following_heading_original_pdf=723,
        full_original_glyph_collation_completed=False,
        original_solar_primary_directions_date_engine_verified=False,
        venus_mercury_sun_opposition_source_feasibility_qualified=True,
        empirical_human_validations=0,
        runtime_promotions=0,
        rules=rows,
    ),
)
save(
    "SUN_DIRECTION_HISTORICAL_NONPROMOTION_GUARD_V1.json",
    dict(
        batch="B07s",
        historic_source_only=True,
        original_sun_venus_opposition_doubted_by_lilly=True,
        original_sun_mercury_opposition_doubted_by_lilly=True,
        source_venus_opposition_reinterpreted_as_square=True,
        exact_modern_primary_direction_math_parity_verified=False,
        exact_lilly_hyleg_anareta_and_climacteric_year_verified=False,
        source_preserves_conditional_natal_and_return_chart_qualifications=True,
        natal_forecasting_at_the_person_level_authorized=False,
        clinical_mortality_injury_crime_moral_gender_social_rank_claims_authorized=False,
        independent_human_outcomes_validated=0,
        runtime_rules_promoted=0,
        predictive_method_scientifically_validated=False,
    ),
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    dict(
        batch="B07s",
        original_all_glyphs_verified=False,
        Sun_to_Venus_opposition_as_ordinary_timed_direction_unresolved=True,
        Sun_to_Mercury_opposition_as_ordinary_timed_direction_unresolved=True,
        original_directions_arc_to_year_conversion_unverified=True,
        accurate_1647_solar_time_and_house_calculation_unverified=True,
        source_period_gender_morality_humours_not_real_person_traits=True,
        all_individual_human_predictions_validated=False,
        natal_hyleg_anareta_and_climacteric_computation_not_executed=True,
        had_source_photo_full_first_edition_713_to_725=True,
        no_real_person_health_safety_legal_interpretation_permitted=True,
    ),
)
save(
    "ACCEPTANCE.json",
    dict(
        batch="B07s",
        candidate_status="DOCUMENTARY_VERIFICATION_PENDING",
        prior_lilly=11415,
        prior_ptolemy=1066,
        parallel_chinese_source_notes=97,
        new_historical_annotations=306,
        substantive=304,
        following_navigation=2,
        numbered_chapters_added=1,
        lilly_if_accepted=11721,
        western_if_accepted=12787,
        next_record="R11722",
        original_source_body_frames=list(range(713, 724)),
        following_printed="CLXIII",
        following_heading_frame=723,
        source_group_count=40,
        source_photo_frames=13,
        original_1647_pdf_sha256=win["original_pdf_sha256"],
        rules_sha256=sha(B / "RULES.json"),
        empirical_human_validations=0,
        runtime_promotions=0,
    ),
)
print("Freeze B07s 306 historical only annotations R11416-R11721; 40 groups; index unchanged.")
