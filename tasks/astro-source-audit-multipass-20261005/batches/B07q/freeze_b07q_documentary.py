#!/usr/bin/env python3
"""Freeze original 1647 Lilly printed CLX source annotations without runtime promotion."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARTS = sorted(B.glob("SOURCE_PART_0*.json"))


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def hash_file(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


assert len(PARTS) == 4
source_window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert source_window["next_historical_record"] == "R11068"
assert source_window["current_accepted_lilly"] == 11067
assert source_window["parallel_chinese_source_annotations"] == 72
assert source_window["printed_CLX"]["body_original_pdf_frames"] == list(range(702, 712))
assert source_window["following_printed_CLXI"]["heading_original_pdf"] == 711

groups = []
for i, file in enumerate(PARTS, 1):
    part = load(file)
    assert part["batch"] == "B07q" and part["part"] == i
    assert part["source_only"] and not part["verified_human_predictions"]
    assert not part["runtime_promotions"]
    groups.extend(part["groups"])

assert len(groups) == 27
rules, source_groups, reverse = [], [], []
seen_roles = set()
for i, original in enumerate(groups, 1):
    span = f"B07q-S{i:03d}"
    pages = original["original_pdf_frames"]
    assert pages and set(pages) <= set(range(702, 712))
    assert pages == sorted(set(pages))
    records = []
    ids = []
    for claim in original["claims"]:
        role = claim["role"]
        anchor = claim["source_anchor_not_diplomatic"]
        meaning = claim["historical_meaning_only"]
        qualifier = claim["qualification"]
        assert role not in seen_roles
        seen_roles.add(role)
        assert len(anchor) >= 5 and len(meaning) >= 18 and len(qualifier) >= 3
        number = 11068 + len(rules)
        rid = f"R{number}"
        historic = dict(
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
        records.append(historic)
        rules.append(
            dict(
                id=rid,
                record_number=number,
                batch="B07q",
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
    source_groups.append(
        dict(
            source_span=span,
            original_pdf_frames=pages,
            topic=original["topic"],
            claims=records,
        )
    )
    reverse.append(
        dict(
            source_span=span,
            original_pdf_frames=pages,
            source_group=original["topic"],
            mapped_record_ids=ids,
        )
    )

assert len(rules) == 258
assert [v["record_number"] for v in rules] == list(range(11068, 11326))
assert [v["role"] for v in rules[-2:]] == [
    "next_CLXI_divider",
    "next_fixedstars",
]

photos = {}
for frame in range(702, 714):
    photo = source_window["photos"][str(frame)]
    file = B / photo["file"]
    raw = file.read_bytes()
    assert raw[:2] == b"\xff\xd8" and len(raw) > 150000
    assert len(raw) == photo["bytes"] and hash_file(file) == photo["sha256"]
    photos[str(frame)] = dict(
        photo,
        frame=frame,
        role=("CLX_BODY_OR_BOUNDARY" if frame <= 711 else "CLXI_CONTEXT_NOT_CLX"),
    )

save(
    "SOURCE_FIRST_AUTHORING_20261018.json",
    dict(
        batch="B07q",
        source=source_window["source"],
        status="FIRST_EDITION_CLX_MIDHEAVEN_DIRECTIONS_SOURCE_FIRST",
        printed_chapter="CLX",
        body_pdf_frames=list(range(702, 712)),
        following_printed="CLXI",
        following_heading_original_pdf=711,
        groups=source_groups,
        source_only=True,
        real_person_directions_validated=0,
        runtime_promotions=0,
    ),
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    dict(
        batch="B07q",
        source_groups=reverse,
        source_group_count=len(reverse),
        historical_records=len(rules),
        substantive=len(rules) - 2,
        next_navigation=2,
        source_parts=[p.name for p in PARTS],
    ),
)
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    dict(
        batch="B07q",
        source=source_window["source"],
        full_original_1647_pdf_sha256=source_window["original_pdf_894_frames_sha256"],
        body_original_pdf_frames=list(range(702, 712)),
        following_printed_CLXI_heading_pdf=711,
        photos=photos,
    ),
)
save(
    "RULES.json",
    dict(
        batch="B07q",
        status="ORIGINAL_1647_CLX_MIDHEAVEN_DIRECTIONS_HISTORICAL_ONLY",
        printed_chapter="CLX",
        record_count=len(rules),
        first_record="R11068",
        last_record="R11325",
        substantive=len(rules) - 2,
        following_navigation=2,
        source_groups=len(source_groups),
        body_pdf_frames=list(range(702, 712)),
        following_printed="CLXI",
        following_heading_original_pdf=711,
        full_original_glyph_collation_completed=False,
        primary_directions_chart_engine_verified=False,
        empirical_validations=0,
        runtime_promotions=0,
        rules=rules,
    ),
)
save(
    "CLX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json",
    dict(
        schema="LILLY_CLX_DOCUMENTARY_ONLY_NONPROMOTION_GUARD_V1",
        original_source_collated=True,
        historical_claims_only=True,
        primary_directions_arc_time_engine_verified=False,
        original_1647_zodiac_era_and_accurate_star_parity_verified=False,
        independent_human_outcomes_validated=0,
        runtime_rules_promoted=0,
        owner_person_specific_health_harm_mortality_finance_relationship_inference_authorized=False,
        negative_and_conditional_predictions_recorded=True,
        class_and_radix_preconditions_retained=True,
        real_human_predictive_accuracy_demonstrated=False,
    ),
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    dict(
        batch="B07q",
        original_all_glyphs_verified=False,
        some_symbols_or_diplomatic_spelling_unresolved=True,
        original_primary_directions_time_engine_verified=False,
        exact_medieval_zodiac_and_fixed_star_epoch_parity_verified=False,
        social_class_biased_and_moralizing_claims_historical_only=True,
        real_person_medical_criminal_religious_or_safety_advice_authorized=False,
        no_blinded_human_backtest=True,
        original_1647_source_text_referred_to_as_documents_not_truth=True,
        directions_sextile_trine_square_opposition_and_terms_separately_anchored=True,
    ),
)
save(
    "ACCEPTANCE.json",
    dict(
        batch="B07q",
        candidate_status="DOCUMENTARY_VERIFICATION_PENDING",
        prior_lilly=11067,
        prior_ptolemy=1066,
        new_historical_annotations=258,
        substantive=256,
        next_navigation=2,
        numbered_chapters_added=1,
        lilly_if_published=11325,
        combined_if_published=12391,
        chapter="CLX",
        body_pdf_frames=list(range(702, 712)),
        source_group_count=len(source_groups),
        rules_sha256=hash_file(B / "RULES.json"),
        empirical_validations=0,
        runtime_promotions=0,
    ),
)
print(
    f"Freeze prepared: {len(rules)} proposed historical source notes, "
    f"{len(source_groups)} source groups, last {rules[-1]['id']}; index unchanged."
)
