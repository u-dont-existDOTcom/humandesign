from __future__ import annotations

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
            "personality:north_node": _activation(
                "personality", "north_node", 13, 3
            ),
            "personality:south_node": _activation(
                "personality", "south_node", 7, 3
            ),
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
    assert "cardinal:personality:sun:26.4" in by_id
    assert "cardinal:design:sun:44.2" in by_id
    assert "definition:split_definition" in by_id
    assert "repeated_gate:26:count:2" in by_id
    assert "node:personality:north_node:13.3" in by_id
    assert "hanging_gate:45:toward:21" in by_id
    assert not any(item.anchor_id.startswith("prominent:") for item in anchors)
    assert all(item.behavioral_mapping_status.value == "unresolved" for item in anchors)
    assert all(matches_anchor(_chart(), item) for item in anchors)


def test_cardinal_lines_share_profile_role_dependency() -> None:
    artifact = build_model_b_artifact(ROOT)
    anchors = extract_detailed_anchors(_chart(), artifact)
    personality_sun = next(
        item for item in anchors if item.anchor_id == "cardinal:personality:sun:26.4"
    )
    design_sun = next(
        item for item in anchors if item.anchor_id == "cardinal:design:sun:44.2"
    )

    assert "profile_role_line:personality:4" in personality_sun.dependency_keys
    assert "profile_role_line:design:2" in design_sun.dependency_keys


def test_anchor_extraction_is_deterministic_and_fails_closed() -> None:
    artifact = build_model_b_artifact(ROOT)

    assert detailed_feature_sha256(_chart(), artifact) == detailed_feature_sha256(
        _chart(), artifact
    )
    bad = _chart()
    bad["channels"] = ("1-64",)
    with pytest.raises(ValueError, match="outside frozen catalog"):
        extract_detailed_anchors(bad, artifact)


def test_composite_model_b_keeps_model_a_unchanged() -> None:
    model = FrozenModelB(ROOT / "mappings/model_b_mapping_library_v1.json")

    assert model.model_id == "MODEL-B"
    assert model.detailed_scoring_status == "unresolved"
    assert model.canonical_answers(_chart()) == model.base_library.canonical_answers(_chart())
    assert model.detailed_anchors(_chart())
    assert model.mapping_sha256 != model.artifact.base_mapping_sha256
