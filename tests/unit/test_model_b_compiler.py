from __future__ import annotations

import hashlib
from pathlib import Path

from hdmatch.model_b.artifacts import (
    DetailedLayer,
    FeatureStatus,
    MappingStatus,
    load_model_b_artifact,
)
from hdmatch.model_b.compiler import build_model_b_artifact, compile_model_b_artifacts

ROOT = Path(__file__).parents[2]


def test_model_b_is_separate_complete_and_conservative() -> None:
    artifact = build_model_b_artifact(ROOT)

    assert artifact.model_id == "MODEL-B-DETAILED-V1"
    assert artifact.base_model_id == "MODEL-A-CORE-V1"
    assert artifact.base_mapping_path == "mappings/mapping_library_v1.json"
    assert (
        artifact.base_mapping_sha256
        == hashlib.sha256((ROOT / artifact.base_mapping_path).read_bytes()).hexdigest()
    )
    assert len(artifact.channel_catalog) == 36
    assert len(set(artifact.channel_catalog)) == 36
    assert {item.layer for item in artifact.structural_families} == set(DetailedLayer)
    assert (
        sum(item.feature_status is FeatureStatus.FROZEN for item in artifact.structural_families)
        == 3
    )
    assert all(
        mapping.status is MappingStatus.UNRESOLVED
        and mapping.mapping_directness is None
        and mapping.predicted_response is None
        and mapping.contradiction_rule is None
        for mapping in artifact.behavioral_mappings
    )


def test_only_normative_detailed_association_remains_unresolved() -> None:
    artifact = build_model_b_artifact(ROOT)
    association = next(
        item for item in artifact.behavioral_mappings if item.mapping_id == "MBM-CHANNEL-26-44-T08"
    )

    assert association.question_ids == ("T08",)
    assert association.structural_selector == "complete_channel == 26-44"
    assert association.status is MappingStatus.UNRESOLVED
    assert "directness" in association.unresolved_reason
    assert not any(
        forbidden in item.structural_selector
        for item in artifact.behavioral_mappings
        for forbidden in ("Gate 57", "Gate 18", "1, 8, 24, 26, 44, 61")
    )


def test_committed_model_b_artifacts_recompile_byte_for_byte(tmp_path: Path) -> None:
    result = compile_model_b_artifacts(
        ROOT,
        artifact_path=tmp_path / "model_b.json",
        report_path=tmp_path / "model_b_report.json",
    )

    assert (tmp_path / "model_b.json").read_bytes() == (
        ROOT / "mappings/model_b_mapping_library_v1.json"
    ).read_bytes()
    assert (tmp_path / "model_b_report.json").read_bytes() == (
        ROOT / "mappings/model_b_unresolved_mapping_report_v1.json"
    ).read_bytes()
    loaded = load_model_b_artifact(tmp_path / "model_b.json")
    assert loaded.sha256() == result.artifact_semantic_sha256
    assert hashlib.sha256((tmp_path / "model_b.json").read_bytes()).hexdigest() == (
        result.artifact_file_sha256
    )


def test_conditional_parents_do_not_claim_underspecified_fallbacks() -> None:
    artifact = build_model_b_artifact(ROOT)
    families = artifact.family_by_id

    assert families["MBF-COMPLETE-CHANNEL"].conditional_parent_status is FeatureStatus.UNRESOLVED
    assert "does not freeze which block" in (
        families["MBF-COMPLETE-CHANNEL"].conditional_parent_unresolved_reason or ""
    )
    assert families["MBF-DEFINITION"].conditional_parent_status is FeatureStatus.UNRESOLVED
    assert families["MBF-PROMINENT-ACTIVATION"].feature_status is FeatureStatus.UNRESOLVED
    assert artifact.prominent_activation_allowlist == ()
