from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_gate_archetype_registry_has_exactly_all_64_unique_gates() -> None:
    registry = _load("reference/core/gate_archetypes_v1.json")
    gates = registry["gates"]
    assert isinstance(gates, list)
    gate_numbers = [item["gate"] for item in gates]
    assert len(gate_numbers) == 64
    assert set(gate_numbers) == set(range(1, 65))
    assert len(gate_numbers) == len(set(gate_numbers))
    assert all(item["label"] and item["construct"] for item in gates)


def test_channel_archetype_registry_has_36_unique_canonical_channels() -> None:
    registry = _load("reference/core/channel_archetypes_v1.json")
    channels = registry["channels"]
    assert isinstance(channels, list)
    ids = [item["channel"] for item in channels]
    assert len(ids) == 36
    assert len(ids) == len(set(ids))
    assert all("-" in channel_id for channel_id in ids)
    assert all(item["label"] and item["construct"] for item in channels)


def test_profile_archetype_registry_has_all_12_unique_profiles() -> None:
    registry = _load("reference/core/profile_archetypes_v1.json")
    profiles = registry["profiles"]
    assert isinstance(profiles, list)
    ids = [item["profile"] for item in profiles]
    assert len(ids) == 12
    assert len(ids) == len(set(ids))
    assert set(ids) == {
        "1/3", "1/4", "2/4", "2/5", "3/5", "3/6",
        "4/6", "4/1", "5/1", "5/2", "6/2", "6/3",
    }
    assert all(item["label"] and item["construct"] for item in profiles)


def test_every_survey_v2_domain_preserves_life_stage_context_and_other() -> None:
    survey = _load("reference/core/survey_v2_behavioral_domains.json")
    domains = survey["domains"]
    assert isinstance(domains, list)
    assert {item["id"] for item in domains} == {
        "V2_PROFILE_ROLE",
        "V2_MOON_DRIVE",
        "V2_MERCURY_COMMUNICATION",
        "V2_VENUS_VALUES",
        "V2_CHANNEL_PROCESS",
        "V2_ADAPTIVE_PLANETARY_TIE_BREAKER",
    }
    for domain in domains:
        assert domain["prompt"]
        assert domain["childhood_probe"]
        assert domain["current_probe"]
        assert domain["contrast_probe"]
        assert "other" in domain["response_format"].lower()
        assert domain["minimum_evidence"]


def test_blind_classifier_forbids_candidate_direction_and_birth_metadata() -> None:
    protocol = _load("reference/core/survey_v2_blind_classifier_protocol.json")
    forbidden = {str(item).lower() for item in protocol["classifier_forbidden_inputs"]}
    required_phrases = {
        "birth date",
        "birth time",
        "birth place",
        "candidate chart",
        "predicted gate",
        "predicted channel",
        "candidate rank",
    }
    assert required_phrases <= forbidden
    output = protocol["required_output"]
    assert output["forced_choice"] is False
    statuses = set(output["status"])
    assert {"other", "mixed", "insufficient_evidence", "unclassifiable"} <= statuses


def test_classifier_freeze_binds_model_prompt_and_vocabularies() -> None:
    protocol = _load("reference/core/survey_v2_blind_classifier_protocol.json")
    freeze = "\n".join(str(item).lower() for item in protocol["cohort_freeze"])
    assert "question/domain bank" in freeze
    assert "gate archetype registry" in freeze
    assert "profile archetype registry" in freeze
    assert "channel archetype registry" in freeze
    assert "classifier system prompt" in freeze
    assert "classifier model" in freeze
    assert "confidence threshold" in freeze
