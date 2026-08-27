from __future__ import annotations

from hdmatch.evaluation.holistic_profile_information import observable_id, predicate_matches
from hdmatch.schemas import StructuralChartFeatures


def _features() -> StructuralChartFeatures:
    return StructuralChartFeatures(
        type="Projector",
        strategy="Wait for the Invitation",
        authority="Splenic",
        profile="2/4",
        definition="Split",
        defined_centers=("Spleen", "Heart", "G"),
        channels=("1-8", "23-43", "24-61"),
        activation_gates={
            "personality:moon": 24,
            "design:mars": 61,
            "personality:sun": 1,
            "design:sun": 8,
        },
    )


def test_legacy_predicates_match_structural_cache_features() -> None:
    features = _features()
    assert predicate_matches(features, {"feature": "type", "equals": "Projector"})
    assert predicate_matches(features, {"feature": "authority", "equals": "Splenic"})
    assert predicate_matches(
        features, {"feature": "center", "name": "Sacral", "defined": False}
    )
    assert predicate_matches(
        features, {"feature": "center", "name": "Spleen", "defined": True}
    )
    assert predicate_matches(features, {"feature": "profile", "equals": "2/4"})
    assert predicate_matches(features, {"feature": "profile_has_line", "line": 4})
    assert predicate_matches(features, {"feature": "channel", "equals": "8-1"})
    assert predicate_matches(features, {"feature": "gate", "equals": 24})
    assert predicate_matches(
        features,
        {
            "feature": "activation",
            "side": "personality",
            "body": "moon",
            "gate": 24,
        },
    )
    assert not predicate_matches(
        features,
        {"feature": "activation", "side": "design", "body": "mars", "gate": 54},
    )


def test_observable_id_collapses_mechanical_alternatives_but_not_profile_behaviors() -> None:
    channel = {
        "id": "CH_1_8_ORIGINAL",
        "cluster": "ORIGINAL_CONTRIBUTION",
    }
    gate = {
        "id": "GATE_1_ORIGINAL_ALT",
        "cluster": "ORIGINAL_CONTRIBUTION",
    }
    profile_24 = {"id": "PROFILE_24", "cluster": "PROFILE_STRUCTURE"}
    profile_5 = {"id": "PROFILE_LINE5_PROJECTION", "cluster": "PROFILE_STRUCTURE"}
    assert observable_id(channel) == "ORIGINAL_CONTRIBUTION"
    assert observable_id(gate) == "ORIGINAL_CONTRIBUTION"
    assert observable_id(profile_24) == "PROFILE_24"
    assert observable_id(profile_5) == "PROFILE_LINE5_PROJECTION"
