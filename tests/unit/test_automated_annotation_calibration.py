from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.automated_annotation_calibration import (
    AutomatedCodingEnsembleReceipt,
    AutomatedCodingPassReceipt,
    AutomatedHumanCalibrationComparisonPayload,
    BlindHumanCalibrationAuditReceipt,
    automated_human_calibration_integrity_errors,
    build_automated_human_calibration_artifact,
    load_automated_human_calibration_artifact,
    write_automated_human_calibration_artifact,
)


def _pass(pass_id: str, output_char: str) -> AutomatedCodingPassReceipt:
    return AutomatedCodingPassReceipt(
        pass_id=pass_id,
        corpus_sha256="1" * 64,
        codebook_sha256="2" * 64,
        coding_procedure_sha256="3" * 64,
        prompt_sha256="4" * 64,
        model_identity="SYNTHETIC-MODEL",
        model_version="synthetic-v1",
        output_sha256=output_char * 64,
        created_at_utc=datetime(2026, 9, 4, 0, 10, tzinfo=UTC),
    )


def _ensemble() -> AutomatedCodingEnsembleReceipt:
    return AutomatedCodingEnsembleReceipt(
        passes=(_pass("P1", "5"), _pass("P2", "6"), _pass("P3", "7")),
        consensus_rule_sha256="8" * 64,
        consensus_report_sha256="9" * 64,
        total_units=10,
        unanimous_units=7,
        majority_units=2,
        unresolved_units=1,
    )


def _audit() -> BlindHumanCalibrationAuditReceipt:
    return BlindHumanCalibrationAuditReceipt(
        auditor_id="BLIND-HUMAN-AUDITOR-SYNTHETIC",
        sample_manifest_sha256="a" * 64,
        parent_corpus_sha256="1" * 64,
        codebook_sha256="2" * 64,
        coding_procedure_sha256="3" * 64,
        audit_output_sha256="b" * 64,
        created_at_utc=datetime(2026, 9, 4, 0, 20, tzinfo=UTC),
    )


def test_ensemble_requires_three_unique_passes_and_coherent_counts() -> None:
    ensemble = _ensemble()
    assert ensemble.corpus_sha256 == "1" * 64
    assert ensemble.unresolved_units == 1

    with pytest.raises(ValueError, match="duplicate pass IDs"):
        AutomatedCodingEnsembleReceipt(
            **{**ensemble.model_dump(), "passes": (_pass("P1", "5"), _pass("P1", "6"), _pass("P3", "7"))}
        )

    with pytest.raises(ValueError, match="sum to total_units"):
        AutomatedCodingEnsembleReceipt(
            **{**ensemble.model_dump(), "unresolved_units": 2}
        )


def test_ensemble_fails_closed_when_pipeline_hashes_differ() -> None:
    changed = _pass("P2", "6").model_copy(update={"prompt_sha256": "c" * 64})
    with pytest.raises(ValueError, match="same frozen prompt"):
        AutomatedCodingEnsembleReceipt(
            passes=(_pass("P1", "5"), changed, _pass("P3", "7")),
            consensus_rule_sha256="8" * 64,
            consensus_report_sha256="9" * 64,
            total_units=10,
            unanimous_units=7,
            majority_units=2,
            unresolved_units=1,
        )


def test_human_audit_must_bind_same_corpus_codebook_and_procedure() -> None:
    payload = AutomatedHumanCalibrationComparisonPayload(
        ensemble=_ensemble(),
        human_audit=_audit(),
        comparison_report_sha256="c" * 64,
        sampled_units=5,
        raw_applicability_agreement=0.8,
        raw_value_agreement=0.75,
        unresolved_sample_units=1,
        created_at_utc=datetime(2026, 9, 4, 0, 30, tzinfo=UTC),
    )
    assert payload.human_audit.llm_outputs_available_before_first_pass is False

    bad_audit = _audit().model_copy(update={"codebook_sha256": "d" * 64})
    with pytest.raises(ValueError, match="does not bind the ensemble codebook"):
        AutomatedHumanCalibrationComparisonPayload(
            **{**payload.model_dump(), "human_audit": bad_audit}
        )


def test_calibration_artifact_is_content_addressed_read_only(tmp_path: Path) -> None:
    payload = AutomatedHumanCalibrationComparisonPayload(
        ensemble=_ensemble(),
        human_audit=_audit(),
        comparison_report_sha256="c" * 64,
        sampled_units=5,
        unresolved_sample_units=1,
        created_at_utc=datetime(2026, 9, 4, 0, 30, tzinfo=UTC),
    )
    artifact = build_automated_human_calibration_artifact(payload)
    assert artifact.artifact_id == f"LPAC-{artifact.artifact_sha256[:20].upper()}"
    assert automated_human_calibration_integrity_errors(artifact) == ()

    path = tmp_path / "calibration.json"
    write_automated_human_calibration_artifact(path, artifact)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_automated_human_calibration_artifact(path) == artifact
    with pytest.raises(FileExistsError):
        write_automated_human_calibration_artifact(path, artifact)
