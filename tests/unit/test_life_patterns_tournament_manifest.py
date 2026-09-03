from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.tournament_manifest import (
    AnalysisAuthorizationArtifact,
    AnalysisAuthorizationPayload,
    MetricPlan,
    ModelManifestEntry,
    TournamentManifestArtifact,
    TournamentManifestPayload,
    build_analysis_authorization,
    build_tournament_manifest,
    load_analysis_authorization,
    load_tournament_manifest,
    tournament_execution_blockers,
    tournament_manifest_integrity_errors,
    write_analysis_authorization,
    write_tournament_manifest,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json


def _authorization(
    *,
    birth: bool = True,
    storage: bool = True,
    purpose: str = "research_comparison_and_participant_reveal",
    scope: tuple[str, ...] = (
        "non_birth_baseline",
        "human_design",
        "conventional_astrology",
    ),
) -> AnalysisAuthorizationArtifact:
    return build_analysis_authorization(
        AnalysisAuthorizationPayload(
            session_id="LP-TESTSESSION0001",
            freeze_id="BPF-ABCDEF0123456789ABCD",
            freeze_sha256="1" * 64,
            purpose=purpose,  # type: ignore[arg-type]
            model_family_scope=scope,
            exact_birth_data_use_authorized=birth,
            result_storage_authorized=storage,
            authorized_at_utc=datetime(2026, 9, 3, 17, 0, tzinfo=UTC),
        )
    )


def _model(
    model_id: str,
    family: str,
    *,
    baseline: bool = False,
    planned: bool = False,
    bridge: bool = True,
    output_type: str = "ranked_candidates",
    requires_birth: bool = True,
    scientific_status: str = "confirmatory_predeclared",
    hash_digit: str = "2",
) -> ModelManifestEntry:
    present = None if planned else hash_digit * 64
    bridge_hash = None if planned or not bridge else hash_digit * 64
    return ModelManifestEntry(
        model_id=model_id,
        label=model_id.replace("_", " ").title(),
        family=family,
        scientific_status=scientific_status,  # type: ignore[arg-type]
        implementation_status="planned_only" if planned else "implemented",
        implementation_version="v1",
        implementation_sha256=present,
        adapter_id=f"{model_id}-adapter-v1",
        adapter_sha256=present,
        measurement_bridge_id=f"{model_id}-bridge-v1",
        measurement_bridge_sha256=bridge_hash,
        scoring_contract_id=f"{model_id}-score-v1",
        scoring_contract_sha256=present,
        requires_birth_data=requires_birth,
        is_baseline=baseline,
        output_type=output_type,  # type: ignore[arg-type]
        candidate_universe_sha256="a" * 64 if output_type == "ranked_candidates" else None,
        candidate_universe_state_count=288_938 if output_type == "ranked_candidates" else None,
        tuning_or_search_budget="frozen before target evaluation; no target-case tuning",
        limitations=("synthetic test manifest entry",),
    )


def _metrics(*, proper: tuple[str, ...] = ()) -> MetricPlan:
    return MetricPlan(
        primary_metric_ids=("mean_reciprocal_rank", "top_1_fractional_credit"),
        secondary_metric_ids=("mean_percentile", "tie_rate"),
        proper_scoring_rule_ids=proper,
        tie_policy="fractional-credit-random-within-tie",
        missing_claim_policy="missing neutral observables remain missing; no model-specific imputation",
        rejected_claim_policy="participant-rejected claims are excluded from scoring",
        uncertain_claim_policy="participant-uncertain claims are excluded from primary scoring",
        exclusion_policy="apply only exclusions frozen in this manifest before target results",
    )


def _ready_roster() -> tuple[ModelManifestEntry, ...]:
    return (
        _model(
            "permutation_baseline",
            "non_birth_baseline",
            baseline=True,
            requires_birth=False,
            hash_digit="2",
        ),
        _model("human_design_v1", "human_design", hash_digit="3"),
        _model("western_astrology_v1", "conventional_astrology", hash_digit="4"),
    )


def _payload(
    authorization: AnalysisAuthorizationArtifact,
    *,
    roster: tuple[ModelManifestEntry, ...] | None = None,
    metrics: MetricPlan | None = None,
    cohort_role: str = "validation",
    preregistration_status: str = "confirmatory_preregistered",
    reveal_policy: str = "participant_reveal_after_locked_execution",
    include_birth: bool = True,
) -> TournamentManifestPayload:
    return TournamentManifestPayload(
        session_id=authorization.payload.session_id,
        freeze_id=authorization.payload.freeze_id,
        freeze_sha256=authorization.payload.freeze_sha256,
        authorization_id=authorization.authorization_id,
        authorization_sha256=authorization.authorization_sha256,
        birth_input_sha256="8" * 64 if include_birth else None,
        civil_time_resolution_sha256="9" * 64 if include_birth else None,
        cohort_role=cohort_role,  # type: ignore[arg-type]
        preregistration_status=preregistration_status,  # type: ignore[arg-type]
        reveal_policy=reveal_policy,  # type: ignore[arg-type]
        model_roster=roster or _ready_roster(),
        metric_plan=metrics or _metrics(),
        runtime_code_commit="abcdef0123456789abcdef0123456789abcdef01",
        minimum_distinct_nonbaseline_families=2,
        created_at_utc=datetime(2026, 9, 3, 17, 30, tzinfo=UTC),
    )


def test_ready_manifest_has_exact_triple_binding_and_round_trips(tmp_path: Path) -> None:
    authorization = _authorization()
    manifest = build_tournament_manifest(_payload(authorization), authorization)
    assert manifest.execution_ready is True
    assert manifest.execution_blockers == ()
    assert manifest.manifest_sha256 == sha256_json(manifest.payload)
    assert manifest.manifest_id == f"LPT-{manifest.manifest_sha256[:20].upper()}"
    assert manifest.payload.freeze_sha256 == authorization.payload.freeze_sha256
    assert manifest.payload.authorization_sha256 == authorization.authorization_sha256
    assert tournament_manifest_integrity_errors(manifest, authorization) == ()

    authorization_path = tmp_path / "authorization.json"
    manifest_path = tmp_path / "manifest.json"
    write_analysis_authorization(authorization_path, authorization)
    write_tournament_manifest(manifest_path, manifest, authorization)
    assert stat.S_IMODE(authorization_path.stat().st_mode) == 0o400
    assert stat.S_IMODE(manifest_path.stat().st_mode) == 0o400
    assert load_analysis_authorization(authorization_path) == authorization
    assert load_tournament_manifest(manifest_path, authorization) == manifest
    with pytest.raises(FileExistsError):
        write_tournament_manifest(manifest_path, manifest, authorization)


def test_non_executable_manifest_is_valid_auditable_artifact(tmp_path: Path) -> None:
    authorization = _authorization()
    roster = (
        _ready_roster()[0],
        _model(
            "human_design_planned",
            "human_design",
            planned=True,
            bridge=False,
            hash_digit="3",
        ),
        _ready_roster()[2],
    )
    manifest = build_tournament_manifest(_payload(authorization, roster=roster), authorization)
    assert manifest.execution_ready is False
    assert any("planned only" in blocker for blocker in manifest.execution_blockers)
    assert any("measurement-bridge" in blocker for blocker in manifest.execution_blockers)
    assert tournament_manifest_integrity_errors(manifest, authorization) == ()

    path = tmp_path / "planned-manifest.json"
    write_tournament_manifest(path, manifest, authorization)
    assert load_tournament_manifest(path, authorization) == manifest


def test_manifest_requires_a_real_baseline_and_distinct_model_families() -> None:
    authorization = _authorization(scope=("human_design",))
    roster = (
        _model("hd_a", "human_design", hash_digit="3"),
        _model("hd_b", "human_design", hash_digit="4"),
    )
    manifest = build_tournament_manifest(_payload(authorization, roster=roster), authorization)
    assert manifest.execution_ready is False
    assert "model roster has no declared non-birth/context baseline" in manifest.execution_blockers
    assert any("distinct non-baseline model families" in blocker for blocker in manifest.execution_blockers)


def test_manifest_blocks_missing_measurement_bridge_even_for_implemented_model() -> None:
    authorization = _authorization()
    roster = (
        _ready_roster()[0],
        _model("hd_no_bridge", "human_design", bridge=False, hash_digit="3"),
        _ready_roster()[2],
    )
    manifest = build_tournament_manifest(_payload(authorization, roster=roster), authorization)
    assert manifest.execution_ready is False
    assert "model hd_no_bridge lacks a pinned measurement-bridge hash" in manifest.execution_blockers


def test_birth_use_and_family_scope_are_separate_authorization_gates() -> None:
    no_birth = _authorization(birth=False)
    birth_blocked = build_tournament_manifest(_payload(no_birth), no_birth)
    assert "participant did not authorize exact birth-data use" in birth_blocked.execution_blockers

    restricted = _authorization(scope=("non_birth_baseline", "human_design"))
    family_blocked = build_tournament_manifest(_payload(restricted), restricted)
    assert any("conventional_astrology" in blocker for blocker in family_blocked.execution_blockers)


def test_storage_and_reveal_permissions_can_block_execution_without_invalidating_authorization(
    tmp_path: Path,
) -> None:
    authorization = _authorization(
        storage=False,
        purpose="research_comparison",
    )
    path = tmp_path / "limited-authorization.json"
    write_analysis_authorization(path, authorization)
    assert load_analysis_authorization(path) == authorization

    manifest = build_tournament_manifest(_payload(authorization), authorization)
    assert "participant did not authorize storage of model-analysis results" in manifest.execution_blockers
    assert "participant-facing reveal is outside the authorized purpose" in manifest.execution_blockers


def test_probabilistic_output_requires_predeclared_proper_scoring_rule() -> None:
    authorization = _authorization()
    roster = (
        _ready_roster()[0],
        _model(
            "hd_probability",
            "human_design",
            output_type="probabilistic_observables",
            hash_digit="3",
        ),
        _ready_roster()[2],
    )
    without = build_tournament_manifest(
        _payload(authorization, roster=roster, metrics=_metrics(proper=())),
        authorization,
    )
    assert "probabilistic model output lacks a predeclared proper scoring rule" in without.execution_blockers

    with_rule = build_tournament_manifest(
        _payload(authorization, roster=roster, metrics=_metrics(proper=("brier_score",))),
        authorization,
    )
    assert "probabilistic model output lacks a predeclared proper scoring rule" not in with_rule.execution_blockers


def test_development_cohort_cannot_be_labeled_confirmatory_validation() -> None:
    authorization = _authorization()
    manifest = build_tournament_manifest(
        _payload(authorization, cohort_role="development"),
        authorization,
    )
    assert "development cohort cannot support confirmatory validation status" in manifest.execution_blockers


def test_manifest_detects_payload_tampering_and_stale_readiness_flags(tmp_path: Path) -> None:
    authorization = _authorization()
    manifest = build_tournament_manifest(_payload(authorization), authorization)
    path = tmp_path / "manifest.json"
    write_tournament_manifest(path, manifest, authorization)

    raw = manifest.model_dump(mode="json")
    raw["payload"]["runtime_code_commit"] = "1234567890abcdef1234567890abcdef12345678"
    path.chmod(0o600)
    path.write_bytes(canonical_json_bytes(raw))
    with pytest.raises(ValueError, match="content-address verification"):
        load_tournament_manifest(path, authorization)

    stale = TournamentManifestArtifact(
        manifest_id=manifest.manifest_id,
        manifest_sha256=manifest.manifest_sha256,
        payload=manifest.payload,
        execution_ready=False,
        execution_blockers=(),
    )
    errors = tournament_manifest_integrity_errors(stale, authorization)
    assert "stored execution-ready flag disagrees with recomputed blockers" in errors
