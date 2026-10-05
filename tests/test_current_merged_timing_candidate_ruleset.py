import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "reference" / "research" / "current_merged_timing_candidate_ruleset_v1.json"
EXP = ROOT / "experiments" / "astrohd" / "merged_candidate_ruleset_20261005"


def load(path: Path):
    return json.loads(path.read_text())


def test_current_merged_candidate_registry_preserves_success_and_transfer_miss():
    data = load(REGISTRY)
    assert data["status"] == "CURRENT_DEVELOPMENT_CANDIDATE_REGISTRY"
    rules = {r["rule_id"]: r for r in data["candidates"]}
    assert "daily_three_family_angle_activation_v1" in rules
    assert "father_loss_v4_sudden" in rules
    assert "relationship_timing_v3_empirical" in rules
    assert "inner_transition_two_channel_v4" in rules
    assert "six_rule_carrier_timing_v1" in rules

    daily = rules["daily_three_family_angle_activation_v1"]
    assert daily["frozen_rule"]["slow_exact_hit_within_hours_of_local_noon"] == 24
    assert daily["frozen_rule"]["progression_exact_hit_within_hours_of_local_noon"] == 72
    assert daily["frozen_rule"]["lunar_exact_hit_within_hours_of_local_noon"] == 24
    evidence = {e["case"]: e for e in daily["evidence"]}
    assert evidence["Hale 2026"]["target_match"] is True
    assert evidence["Joel father death 2002"]["target_match"] is False


def test_reproducible_fixed_rule_outputs_match_registry_claims():
    hale = load(EXP / "hale_father_heartattack_Europe_Istanbul.json")
    joel = load(EXP / "joel_father_death_America_New_York.json")

    assert hale["candidate_count"] == 1
    assert [x["local_date"] for x in hale["candidate_dates"]] == ["2026-09-23"]
    assert hale["event_evaluation"]["matches_candidate_rule"] is True

    assert joel["candidate_count"] == 2
    assert [x["local_date"] for x in joel["candidate_dates"]] == ["2002-04-08", "2002-04-09"]
    assert joel["event_evaluation"]["reported_date"] == "2002-06-05"
    assert joel["event_evaluation"]["matches_candidate_rule"] is False
