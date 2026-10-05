import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/"reference"/"research"/"CURRENT_PERSON_LIFE_RULESET_CATALOG_V1.json"
TIMING=ROOT/"reference"/"research"/"current_merged_timing_candidate_ruleset_v1.json"


def test_catalog_contains_retained_best_families_and_negative_controls():
    data=json.loads(CAT.read_text())
    current={x["id"] for x in data["current_or_retained"]}
    assert {
        "astrohd_v14_full_source_library",
        "astrohd_v14_six_rule_signature",
        "cf003_planetary_dominance",
        "numerology_registry_v2_1",
        "timing_candidate_registry",
        "relationship_timing_v3_empirical",
        "father_loss_v4_sudden",
        "inner_transition_two_channel_v4",
        "daily_three_family_angle_activation_v1",
        "six_rule_carrier_timing_v1",
        "human_design_v4_3_v3_6",
        "astrohd_relationship_overlay",
    } <= current

    negative={x["id"] for x in data["material_negative_or_superseded"]}
    assert {
        "relationship_timing_v2",
        "maternal_loss_blind_models",
        "spiritual_transition_blind_model",
        "adb_pair_timing_v1_v2_v3",
        "strong_rule_offender_laureate_search",
        "cf004_southern_inversion",
        "cf005_event_aspect_tables",
    } <= negative

    exploratory={x["id"] for x in data["important_exploratory_not_default"]}
    assert {
        "cf001_prominence_karaka_kendra",
        "cf002_tightness_applying",
        "cf006_sectors",
        "cf007_personality_aspect_moderators",
        "literature_model_v1b_theory_neutral",
        "numerology_owner_comparison_20261004",
    } <= exploratory


def test_timing_registry_contains_all_retained_timing_candidates():
    data=json.loads(TIMING.read_text())
    ids={x["rule_id"] for x in data["candidates"]}
    assert {
        "daily_three_family_angle_activation_v1",
        "father_loss_v4_sudden",
        "relationship_timing_v3_empirical",
        "inner_transition_two_channel_v4",
        "six_rule_carrier_timing_v1",
    } <= ids
