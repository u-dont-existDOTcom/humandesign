from __future__ import annotations

import inspect
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from pydantic import ValidationError

import hdmatch.model.v4_3_prevalence as prevalence_module
from hdmatch.century_cache.models import (
    CenturyStateRecord,
    FeatureValue,
    required_feature_ids_sha256,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file, sha256_json
from hdmatch.model.v4_3_prevalence import (
    V43ConditionalPrevalenceArtifactV1,
    V43ConditionalPrevalencePolicyV1,
    V43FeatureClauseV1,
    V43FeaturePredicateV1,
    V43PredicateOperator,
    V43PrevalenceAnchorV1,
    V43PrevalenceError,
    V43PrevalenceParentLevelV1,
    V43PrevalencePlanV1,
    build_v4_3_prevalence_artifact,
    capped_information_rubric_bits,
    load_v4_3_prevalence_plan,
    v4_3_predicate_matches,
    verify_v4_3_prevalence_artifact,
    write_v4_3_prevalence_artifact_new,
    write_v4_3_prevalence_plan_new,
)

_SEMANTIC_REGISTRY_SHA256 = "1" * 64
_PHYSICAL_REGISTRY_SHA256 = "2" * 64
_LOGICAL_UNIVERSE_SHA256 = "3" * 64
_RECONCILIATION_SHA256 = "4" * 64
_BUILD_PLAN_SHA256 = "5" * 64
_BUILD_SPEC_SHA256 = "6" * 64
_MAPPING_SHA256 = "7" * 64
_MAPPING_REGISTRY_SHA256 = "8" * 64
_EPHEMERIS_SHA256 = "9" * 64


def _plan() -> V43PrevalencePlanV1:
    required = ("architecture.type", "structure.flag")
    return V43PrevalencePlanV1(
        mapping_artifact_sha256=_MAPPING_SHA256,
        mapping_required_feature_registry_sha256=_MAPPING_REGISTRY_SHA256,
        expected_cache_semantic_feature_registry_sha256=(
            _SEMANTIC_REGISTRY_SHA256
        ),
        expected_cache_feature_registry_sha256=_PHYSICAL_REGISTRY_SHA256,
        required_feature_ids=required,
        required_feature_ids_sha256=required_feature_ids_sha256(required),
        anchors=(
            V43PrevalenceAnchorV1(
                anchor_id="anchor:flag",
                predicate=V43FeaturePredicateV1(
                    clauses=(
                        V43FeatureClauseV1(
                            feature_id="structure.flag",
                            operator=V43PredicateOperator.EQUALS,
                            expected=True,
                        ),
                    )
                ),
                parent_hierarchy=(
                    V43PrevalenceParentLevelV1(
                        level_id="given_type",
                        parent_feature_ids=("architecture.type",),
                    ),
                    V43PrevalenceParentLevelV1(
                        level_id="global",
                        parent_feature_ids=(),
                    ),
                ),
            ),
        ),
    )


def _row(
    index: int,
    start: datetime,
    duration_seconds: int,
    *,
    chart_type: str,
    flag: bool,
) -> CenturyStateRecord:
    end = start + timedelta(seconds=duration_seconds)
    return CenturyStateRecord(
        state_id=f"state-{index:04d}",
        utc_start=start,
        utc_end=end,
        duration_seconds=float(duration_seconds),
        representative_utc=start + (end - start) / 2,
        design_timestamp=start - timedelta(days=88),
        chart_features_sha256=f"{index % 16:x}" * 64,
        feature_vector_schema_version="chart-feature-vector-v2",
        semantic_feature_registry_sha256=_SEMANTIC_REGISTRY_SHA256,
        feature_registry_sha256=_PHYSICAL_REGISTRY_SHA256,
        astronomy_engine_version="verified-swieph-fixture",
        ephemeris_file_set_sha256=_EPHEMERIS_SHA256,
        node_convention="true",
        mandala_mapping_version="fixture-v1",
        mandala_mapping_sha256="a" * 64,
        bodygraph_mapping_sha256="b" * 64,
        feature_values=(
            FeatureValue(feature_id="architecture.type", value=chart_type),
            FeatureValue(feature_id="structure.flag", value=flag),
        ),
    )


def _install_cache_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    rows: tuple[CenturyStateRecord, ...],
) -> tuple[Path, Path]:
    trust_lock_path = tmp_path / "v1.trust-lock.json"
    manifest_path = tmp_path / "cache" / "manifest.json"
    manifest_path.parent.mkdir()
    trust_lock_path.write_bytes(b"tracked trust lock fixture")
    manifest_path.write_bytes(b"verified manifest fixture")
    ephemeris_provenance = SimpleNamespace(
        source_manifest_sha256="c" * 64,
        ephemeris_file_set_sha256=_EPHEMERIS_SHA256,
    )
    engine = SimpleNamespace(
        ephemeris_provenance=ephemeris_provenance,
        model_dump=lambda mode: {"engine": "SWIEPH", "mode": mode},
    )
    exact_state_provenance = SimpleNamespace(
        model_dump=lambda mode: {"logical_universe_sha256": _LOGICAL_UNIVERSE_SHA256}
    )
    manifest = SimpleNamespace(
        cache_version="century-cache-v1",
        utc_start=rows[0].utc_start,
        utc_end_exclusive=rows[-1].utc_end,
        interval_count=len(rows),
        feature_registry=(
            SimpleNamespace(feature_id="architecture.type"),
            SimpleNamespace(feature_id="structure.flag"),
        ),
        feature_vector_schema_version="chart-feature-vector-v2",
        semantic_feature_registry_sha256=_SEMANTIC_REGISTRY_SHA256,
        feature_registry_sha256=_PHYSICAL_REGISTRY_SHA256,
        build_plan_sha256=_BUILD_PLAN_SHA256,
        reconciliation_aggregate_sha256=_RECONCILIATION_SHA256,
        exact_state_provenance=exact_state_provenance,
        logical_universe_sha256=_LOGICAL_UNIVERSE_SHA256,
        engine=engine,
        boundary_policy_version="exact-boundaries-v1",
        generation_commit="d" * 40,
    )
    verified = SimpleNamespace(
        cache_directory=manifest_path.parent,
        manifest_path=manifest_path,
        manifest_sha256=sha256_file(manifest_path),
        manifest=manifest,
        required_feature_coverage=1.0,
    )
    lock = SimpleNamespace(
        cache_locator="data/century_cache/v1",
        build_spec_sha256=_BUILD_SPEC_SHA256,
    )
    monkeypatch.setattr(
        prevalence_module,
        "load_century_cache_trust_lock",
        lambda path: cast(Any, lock),
    )
    monkeypatch.setattr(
        prevalence_module,
        "open_century_cache_for_recovery",
        lambda cache_directory, *, trust_lock_path: cast(Any, verified),
    )
    monkeypatch.setattr(
        prevalence_module,
        "iter_verified_century_cache_rows",
        lambda cache: iter(rows),
    )
    return manifest_path.parent, trust_lock_path


def test_global_cache_prevalence_is_duration_weighted_not_row_weighted(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = (
        _row(0, start, 10, chart_type="A", flag=True),
        _row(1, start + timedelta(seconds=10), 30, chart_type="A", flag=False),
        _row(2, start + timedelta(seconds=40), 60, chart_type="B", flag=False),
    )
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)

    artifact = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )

    root = artifact.tables[0].cells[-1]
    assert root.level_id == "global"
    assert root.numerator_duration_microseconds == 10_000_000
    assert root.denominator_duration_microseconds == 100_000_000
    assert root.numerator_duration_microseconds / root.denominator_duration_microseconds == 0.1
    assert root.numerator_duration_microseconds / root.denominator_duration_microseconds != (
        1 / 3
    )
    assert artifact.source.logical_universe_sha256 == _LOGICAL_UNIVERSE_SHA256
    assert artifact.source.cache_manifest_sha256 == sha256_file(cache / "manifest.json")
    assert artifact.source.cache_trust_lock_sha256 == sha256_file(lock)
    assert artifact.source.reconciliation_aggregate_sha256 == _RECONCILIATION_SHA256
    assert artifact.source.ephemeris_source_manifest_sha256 == "c" * 64
    assert artifact.source.ephemeris_file_set_sha256 == _EPHEMERIS_SHA256
    assert artifact.source.boundary_policy_version == "exact-boundaries-v1"
    assert artifact.source.generation_commit == "d" * 40
    assert artifact.source.total_duration_microseconds == 100_000_000
    assert artifact.policy.candidate_file_frequencies_forbidden is True


def test_verified_lookup_selects_first_sufficient_cell_and_exact_next_backoff(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = tuple(
        _row(
            index,
            start + timedelta(seconds=index),
            1,
            chart_type="A" if index < 600 else "B",
            flag=index < 100,
        )
        for index in range(1_000)
    )
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)
    artifact = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )
    artifact_path = tmp_path / "prevalence.json"
    write_v4_3_prevalence_artifact_new(artifact_path, artifact)
    provider = verify_v4_3_prevalence_artifact(
        artifact_path,
        cache_directory=cache,
        trust_lock_path=lock,
        expected_plan=_plan(),
    )

    group_a = provider.estimate("anchor:flag", rows[0])
    group_b = provider.estimate("anchor:flag", rows[-1])

    assert group_a.selected_level_id == "given_type"
    assert group_a.backoff_ordinal == 0
    assert group_a.numerator_duration_microseconds == 100_000_000
    assert group_a.denominator_duration_microseconds == 600_000_000
    assert group_a.conditional is True
    assert group_a.selected_level_conditional is True
    assert group_b.selected_level_id == "global"
    assert group_b.backoff_ordinal == 1
    assert group_b.numerator_duration_microseconds == 100_000_000
    assert group_b.denominator_duration_microseconds == 1_000_000_000
    assert group_b.attempts[0].minimum_effective_size_met is False
    assert group_b.attempts[1].level_id == "global"
    assert group_b.conditional is True
    assert group_b.selected_level_conditional is False
    assert provider.provenance.conditional is True
    assert provider.provenance.source_scope == "declared-global-utc-universe"


def test_candidate_pool_cannot_be_substituted_for_cache_source(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    parameters = inspect.signature(build_v4_3_prevalence_artifact).parameters
    assert "candidate_rows" not in parameters
    assert "candidate_file" not in parameters
    candidate_file = tmp_path / "candidates.json"
    candidate_file.write_text("[]", encoding="utf-8")
    trust_lock = tmp_path / "trust.json"
    trust_lock.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        prevalence_module,
        "load_century_cache_trust_lock",
        lambda path: SimpleNamespace(),
    )

    def reject_non_cache(cache_directory: object, *, trust_lock_path: object) -> Any:
        raise RuntimeError("ordinary recovery gate rejected candidate pool")

    monkeypatch.setattr(
        prevalence_module,
        "open_century_cache_for_recovery",
        reject_non_cache,
    )
    with pytest.raises(RuntimeError, match="rejected candidate pool"):
        build_v4_3_prevalence_artifact(
            candidate_file,
            trust_lock_path=trust_lock,
            plan=_plan(),
        )


def test_skipped_conditional_level_and_backoff_hierarchy_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = (
        _row(0, start, 10, chart_type="A", flag=True),
        _row(1, start + timedelta(seconds=10), 90, chart_type="B", flag=False),
    )
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)
    artifact = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )
    payload = artifact.model_dump(mode="json")
    payload["tables"][0]["cells"] = [
        cell
        for cell in payload["tables"][0]["cells"]
        if cell["backoff_ordinal"] != 0
    ]
    with pytest.raises(ValidationError, match="skips a backoff level"):
        V43ConditionalPrevalenceArtifactV1.model_validate_json(
            canonical_json_bytes(payload),
            strict=True,
        )

    with pytest.raises(ValidationError, match="strictly remove parent features"):
        V43PrevalenceAnchorV1(
            anchor_id="anchor:invalid",
            predicate=_plan().anchors[0].predicate,
            parent_hierarchy=(
                V43PrevalenceParentLevelV1(
                    level_id="type",
                    parent_feature_ids=("architecture.type",),
                ),
                V43PrevalenceParentLevelV1(
                    level_id="added_feature",
                    parent_feature_ids=("structure.flag",),
                ),
                V43PrevalenceParentLevelV1(level_id="global", parent_feature_ids=()),
            ),
        )


def test_replay_rejects_tampered_durations_and_source_identities(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = (
        _row(0, start, 25, chart_type="A", flag=True),
        _row(1, start + timedelta(seconds=25), 75, chart_type="B", flag=False),
    )
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)
    artifact = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )
    payload = artifact.model_dump(mode="json")
    conditional_cells = [
        cell
        for cell in payload["tables"][0]["cells"]
        if cell["backoff_ordinal"] == 0
    ]
    supported = next(
        cell for cell in conditional_cells if cell["numerator_duration_microseconds"] > 0
    )
    unsupported = next(
        cell for cell in conditional_cells if cell["numerator_duration_microseconds"] == 0
    )
    supported["numerator_duration_microseconds"] -= 1
    unsupported["numerator_duration_microseconds"] += 1
    tampered = V43ConditionalPrevalenceArtifactV1.model_validate_json(
        canonical_json_bytes(payload),
        strict=True,
    )
    path = tmp_path / "tampered.json"
    path.write_bytes(canonical_json_bytes(tampered))
    with pytest.raises(V43PrevalenceError, match="global-cache replay"):
        verify_v4_3_prevalence_artifact(
            path,
            cache_directory=cache,
            trust_lock_path=lock,
            expected_plan=_plan(),
        )

    source_payload = artifact.model_dump(mode="json")
    source_payload["source"]["cache_trust_lock_sha256"] = "f" * 64
    changed_source = V43ConditionalPrevalenceArtifactV1.model_validate_json(
        canonical_json_bytes(source_payload),
        strict=True,
    )
    source_path = tmp_path / "changed-source.json"
    source_path.write_bytes(canonical_json_bytes(changed_source))
    with pytest.raises(V43PrevalenceError, match="global-cache replay"):
        verify_v4_3_prevalence_artifact(
            source_path,
            cache_directory=cache,
            trust_lock_path=lock,
            expected_plan=_plan(),
        )


def test_information_bits_are_capped_and_zero_prevalence_fails_closed() -> None:
    assert capped_information_rubric_bits(1, 1) == 0.0
    assert capped_information_rubric_bits(1, 64) == 6.0
    assert capped_information_rubric_bits(1, 10_000) == 6.0
    with pytest.raises(V43PrevalenceError, match=r"\(0, 1\]"):
        capped_information_rubric_bits(0, 100)
    with pytest.raises(V43PrevalenceError, match=r"\(0, 1\]"):
        capped_information_rubric_bits(101, 100)
    with pytest.raises(ValidationError, match="frozen at six"):
        V43ConditionalPrevalencePolicyV1(information_cap_rubric_bits=7.0)


def test_artifact_bytes_and_hash_are_deterministic(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = (
        _row(0, start, 40, chart_type="A", flag=True),
        _row(1, start + timedelta(seconds=40), 60, chart_type="B", flag=False),
    )
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)
    first = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )
    second = build_v4_3_prevalence_artifact(
        cache,
        trust_lock_path=lock,
        plan=_plan(),
    )

    assert first == second
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert first.sha256() == second.sha256()


def test_prevalence_plan_freeze_is_immutable_and_canonical(tmp_path: Path) -> None:
    plan_path = tmp_path / "prevalence-plan.json"
    write_v4_3_prevalence_plan_new(plan_path, _plan())

    assert load_v4_3_prevalence_plan(plan_path) == _plan()
    with pytest.raises(FileExistsError, match="immutable artifact"):
        write_v4_3_prevalence_plan_new(plan_path, _plan())

    noncanonical = tmp_path / "noncanonical-plan.json"
    noncanonical.write_text(json.dumps(_plan().model_dump(mode="json")), encoding="utf-8")
    with pytest.raises(V43PrevalenceError, match="not canonically encoded"):
        load_v4_3_prevalence_plan(noncanonical)


def test_predicate_language_preserves_v4_3_mapping_operator_semantics() -> None:
    features: dict[str, Any] = {
        "architecture.profile": "2/5",
        "architecture.type": "Projector",
        "gates.active": [
            {
                "gate": 24,
                "activation_count": 3,
                "activation_positions": ["design:moon", "personality:sun"],
            }
        ],
        "gates.hanging": [24, 61],
    }
    predicate = V43FeaturePredicateV1(
        clauses=tuple(
            sorted(
                (
                    V43FeatureClauseV1(
                        feature_id="architecture.profile",
                        operator=V43PredicateOperator.PROFILE_HAS_LINE,
                        expected=5,
                    ),
                    V43FeatureClauseV1(
                        feature_id="architecture.type",
                        operator=V43PredicateOperator.EQUALS_ANY,
                        expected=["Generator", "Projector"],
                    ),
                    V43FeatureClauseV1(
                        feature_id="gates.active",
                        operator=(
                            V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NESTED_PREFIX
                        ),
                        expected={
                            "match": {"gate": 24},
                            "field": "activation_positions",
                            "prefix": "personality:",
                        },
                    ),
                    V43FeatureClauseV1(
                        feature_id="gates.active",
                        operator=(
                            V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE
                        ),
                        expected={
                            "match": {"gate": 24},
                            "field": "activation_count",
                            "minimum": 2,
                        },
                    ),
                    V43FeatureClauseV1(
                        feature_id="gates.hanging",
                        operator=V43PredicateOperator.SEQUENCE_CONTAINS_ANY,
                        expected=[18, 24],
                    ),
                ),
                key=lambda clause: (
                    clause.feature_id,
                    clause.operator.value,
                    sha256_json(clause.expected),
                ),
            )
        )
    )

    assert v4_3_predicate_matches(predicate, cast(Any, features)) is True
    changed = dict(features)
    changed["architecture.profile"] = "1/3"
    assert v4_3_predicate_matches(predicate, cast(Any, changed)) is False


def test_noncanonical_or_mismatched_plan_is_rejected_before_streaming(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    rows = (_row(0, start, 100, chart_type="A", flag=True),)
    cache, lock = _install_cache_gate(monkeypatch, tmp_path, rows)
    plan_payload = _plan().model_dump(mode="json")
    plan_payload["expected_cache_feature_registry_sha256"] = "f" * 64
    wrong_plan = V43PrevalencePlanV1.model_validate_json(
        canonical_json_bytes(plan_payload),
        strict=True,
    )
    consumed = False

    def forbidden_iteration(cache: object) -> Any:
        nonlocal consumed
        consumed = True
        return iter(())

    monkeypatch.setattr(
        prevalence_module,
        "iter_verified_century_cache_rows",
        forbidden_iteration,
    )
    with pytest.raises(V43PrevalenceError, match="physical feature registry mismatch"):
        build_v4_3_prevalence_artifact(
            cache,
            trust_lock_path=lock,
            plan=wrong_plan,
        )
    assert consumed is False

    encoded = json.loads(canonical_json_bytes(_plan()))
    encoded["anchors"][0]["parent_hierarchy"].reverse()
    with pytest.raises(ValidationError, match="unconditional root"):
        V43PrevalencePlanV1.model_validate_json(
            canonical_json_bytes(encoded),
            strict=True,
        )
