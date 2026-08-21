from __future__ import annotations

import json
from pathlib import Path

import pytest

from hdmatch.model_b.compiler import build_model_b_artifact
from hdmatch.model_b.mapping_library import FrozenModelB
from hdmatch.model_b.predicates import (
    detailed_feature_sha256,
    extract_detailed_anchors,
    matches_anchor,
)

ROOT = Path(__file__).parents[2]


def _activation(side: str, body: str, gate: int, line: int) -> dict[str, object]:
    return {"side": side, "body": body, "gate": gate, "line": line}


def _chart() -> dict[str, object]:
    return {
        "type": "projector",
        "strategy": "wait_for_invitation",
        "authority": "splenic",
        "profile": "4/2",
        "definition": "split_definition",
        "defined_centers": ("heart_ego", "spleen", "throat"),
        "channels": ("26-44",),
        "activations": {
            "personality:sun": _activation("personality", "sun", 26, 4),
            "personality:earth": _activation("personality", "earth", 45, 4),
            "design:sun": _activation("design", "sun", 44, 2),
            "design:earth": _activation("design", "earth", 24, 2),
            "personality:north_node": _activation("personality", "north_node", 13, 3),
            "personality:south_node": _activation("personality", "south_node", 7, 3),
            "design:north_node": _activation("design", "north_node", 1, 5),
            "design:south_node": _activation("design", "south_node", 2, 5),
            "personality:moon": _activation("personality", "moon", 26, 1),
        },
    }


def test_full_detailed_inventory_is_extracted_without_behavior_claims() -> None:
    artifact = build_model_b_artifact(ROOT)
    anchors = extract_detailed_anchors(_chart(), artifact)
    by_id = {item.anchor_id: item for item in anchors}

    assert "complete_channel:26-44" in by_id
    assert "cardinal_gate:personality:sun:26" in by_id
    assert "cardinal_line:personality:sun:4" in by_id
    assert "cardinal_gate_line:design:sun:44.2" in by_id
    assert "definition:split_definition" in by_id
    assert "repeated_gate:26:count_at_least:2" in by_id
    assert "node:personality:north_node:13.3" in by_id
    assert "hanging_gate:45:toward:21" in by_id
    assert not any(item.anchor_id.startswith("prominent:") for item in anchors)
    assert all(item.behavioral_mapping_status.value == "unresolved" for item in anchors)
    assert all(matches_anchor(_chart(), item) for item in anchors)


def test_cardinal_lines_share_profile_role_dependency() -> None:
    artifact = build_model_b_artifact(ROOT)
    anchors = extract_detailed_anchors(_chart(), artifact)
    personality_sun = next(
        item for item in anchors if item.anchor_id == "cardinal_gate_line:personality:sun:26.4"
    )
    design_sun = next(
        item for item in anchors if item.anchor_id == "cardinal_gate_line:design:sun:44.2"
    )

    assert "profile_role_line:personality:4" in personality_sun.dependency_keys
    assert "profile_role_line:design:2" in design_sun.dependency_keys
    personality_earth_line = next(
        item for item in anchors if item.anchor_id == "cardinal_line:personality:earth:4"
    )
    assert not any(
        key.startswith("profile_role_line:") for key in personality_earth_line.dependency_keys
    )


def test_repeated_gate_anchor_has_one_declared_threshold_semantics() -> None:
    artifact = build_model_b_artifact(ROOT)
    twice = extract_detailed_anchors(_chart(), artifact)
    chart_with_third = _chart()
    raw_activations = chart_with_third["activations"]
    assert isinstance(raw_activations, dict)
    activations = dict(raw_activations)
    activations["design:moon"] = _activation("design", "moon", 26, 6)
    chart_with_third["activations"] = activations
    three_times = extract_detailed_anchors(chart_with_third, artifact)

    repeated_twice = next(item for item in twice if item.anchor_id.startswith("repeated_gate:26:"))
    repeated_three_times = next(
        item for item in three_times if item.anchor_id.startswith("repeated_gate:26:")
    )
    assert repeated_twice == repeated_three_times
    assert repeated_twice.anchor_id == "repeated_gate:26:count_at_least:2"
    assert matches_anchor(chart_with_third, repeated_twice)


def test_anchor_extraction_is_deterministic_and_fails_closed() -> None:
    artifact = build_model_b_artifact(ROOT)

    assert detailed_feature_sha256(_chart(), artifact) == detailed_feature_sha256(
        _chart(), artifact
    )
    bad = _chart()
    bad["channels"] = ("1-64",)
    with pytest.raises(ValueError, match="outside frozen catalog"):
        extract_detailed_anchors(bad, artifact)

    inconsistent = _chart()
    inconsistent["channels"] = ()
    with pytest.raises(ValueError, match="inconsistent with activation gates"):
        extract_detailed_anchors(inconsistent, artifact)

    invalid_definition = _chart()
    invalid_definition["definition"] = "favorable_custom_definition"
    with pytest.raises(ValueError, match="unknown Definition"):
        extract_detailed_anchors(invalid_definition, artifact)


def test_composite_model_b_keeps_model_a_unchanged() -> None:
    model = FrozenModelB(ROOT / "mappings/model_b_mapping_library_v1.json")

    assert model.model_id == "MODEL-B-DETAILED-V1"
    assert model.detailed_scoring_status == "unresolved"
    assert model.canonical_answers(_chart()) == model.base_library.canonical_answers(_chart())
    assert model.detailed_anchors(_chart())
    assert model.mapping_sha256 != model.artifact.base_mapping_sha256


def test_composite_model_b_rejects_question_bank_dependency_mismatch(
    tmp_path: Path,
) -> None:
    artifact = build_model_b_artifact(ROOT).model_copy(update={"question_bank_sha256": "0" * 64})
    artifact_path = tmp_path / "model-b.json"
    artifact_path.write_text(json.dumps(artifact.model_dump(mode="json")), encoding="utf-8")

    with pytest.raises(ValueError, match="question-bank hash"):
        FrozenModelB(
            artifact_path,
            base_mapping_path=ROOT / "mappings/mapping_library_v1.json",
        )
