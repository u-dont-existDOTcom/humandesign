from __future__ import annotations

import inspect
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

import hdmatch.model.v4_3_prevalence as prevalence_module
import tests.unit.test_century_cache_contract as cache_fixtures
import tests.unit.test_v4_3_mapping_library as mapping_fixtures
from hdmatch.century_cache import (
    CenturyCacheStreamIdentity,
    ExactStateReconciliationStream,
    OverlappingVerifiedExactStateBatch,
    StreamingCenturyCachePublisher,
    VerifiedCenturyCache,
    exact_state_reconciliation_aggregate_sha256,
    iter_verified_century_cache_rows,
    trust_lock_from_verified_cache,
    write_century_cache_trust_lock_new,
)
from hdmatch.century_cache.models import FeatureColumnSpec, FeatureStorageType
from hdmatch.chart.feature_registry import FeatureId
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file
from hdmatch.model.v4_3.integration import (
    CanonicalV43ScoringSession,
    V43IntegrationError,
    V43ObservedResponse,
    mapping_prevalence_parent_hierarchy_sha256,
    mapping_prevalence_plan_sha256,
)
from hdmatch.model.v4_3_compiler import compile_mapping_library_v2
from hdmatch.model.v4_3_mapping import (
    MappingLibraryV2,
    PredicateOperatorV2,
    StructuralPredicateV2,
)
from hdmatch.model.v4_3_prevalence import (
    V43BoundCandidateRecord,
    V43ConditionalPrevalenceArtifactV1,
    V43ConditionalPrevalencePolicyV1,
    V43PrevalenceError,
    V43PrevalencePlanV1,
    VerifiedV43ConditionalPrevalence,
    build_v4_3_prevalence_artifact,
    capped_information_rubric_bits,
    derive_v4_3_prevalence_plan,
    load_v4_3_prevalence_plan,
    v4_3_predicate_matches,
    verify_v4_3_prevalence_artifact,
    write_v4_3_prevalence_artifact_new,
    write_v4_3_prevalence_plan_new,
)
from hdmatch.model.v4_3_profile_mapping import (
    BEST_CURRENT_COMPILED_PATH,
    BEST_CURRENT_SOURCE_PATH,
    LESS_CONTAMINATED_COMPILED_PATH,
    LESS_CONTAMINATED_SOURCE_PATH,
)
from hdmatch.model.v4_3_responses import (
    BEST_CURRENT_RESPONSE_PATH,
    LESS_CONTAMINATED_RESPONSE_PATH,
    compile_v4_3_direct_target_responses,
    verify_v4_3_direct_target_responses,
)
from hdmatch.model.v4_3_run import (
    V43ExternalRankStore,
    V43MinimalScoreRecordV1,
    V43RunFailedError,
    run_verified_v4_3_cache,
    verify_v4_3_run,
)

ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "mappings/v4_3_v3_6_best_current_mapping_library_v2.json"
MAPPING_SOURCE = (
    ROOT / "mappings/v4_3_v3_6_best_current_mapping_library_v2_source.json"
)


@dataclass(frozen=True, slots=True)
class _RealPrevalenceHarness:
    cache_directory: Path
    trust_lock_path: Path
    verified_cache: VerifiedCenturyCache
    plan_path: Path
    plan: V43PrevalencePlanV1
    artifact_path: Path
    artifact: V43ConditionalPrevalenceArtifactV1
    provider: VerifiedV43ConditionalPrevalence


def _mapping_kwargs() -> dict[str, Path]:
    return {
        "mapping_library_path": MAPPING,
        "mapping_source_library_path": MAPPING_SOURCE,
        "mapping_repository_root": ROOT,
    }


@pytest.fixture(scope="module")
def real_harness(tmp_path_factory: pytest.TempPathFactory) -> _RealPrevalenceHarness:
    root = tmp_path_factory.mktemp("real-v43-prevalence")
    provider, batch = cache_fixtures._exact_provider_and_batch()
    source = OverlappingVerifiedExactStateBatch._from_factory_verified_batch_for_test(
        batch=batch,
        core_start_utc=cache_fixtures._START,
        core_end_exclusive=cache_fixtures._END,
        source_staged_receipt_sha256="1" * 64,
        source_replay_verification_sha256="2" * 64,
        source_all_call_audit_sha256="3" * 64,
        source_build_plan_sha256="5" * 64,
    )
    stream = ExactStateReconciliationStream._for_factory_verified_test_sources(
        provider,
        engine_identity=cache_fixtures._reconciliation_engine_identity(),
    )
    assert stream.append(source) is None
    finalization = stream.finalize()
    aggregate = finalization.aggregate_provenance
    spec = cache_fixtures._spec().model_copy(
        update={
            "reconciliation_aggregate_sha256": (
                exact_state_reconciliation_aggregate_sha256(aggregate)
            )
        }
    )
    cache_directory = root / "cache"
    publisher = StreamingCenturyCachePublisher(
        cache_directory,
        identity=CenturyCacheStreamIdentity.from_build_spec(spec),
        build_mode="explicit_rebuild",
    )
    publisher.finish_reconciliation(finalization)
    verified = publisher.finalize_and_publish(
        spec=spec,
        evidence=cache_fixtures._evidence_inputs(
            root / "inputs",
            reconciliation_payload=aggregate.model_dump(mode="json"),
        ),
    )
    trust_lock = trust_lock_from_verified_cache(
        verified,
        build_spec=spec,
        cache_locator="data/century_cache/v1",
    )
    lock_path = write_century_cache_trust_lock_new(
        root / "century-cache.trust-lock.json",
        trust_lock,
    )
    plan = derive_v4_3_prevalence_plan(
        cache_directory,
        trust_lock_path=lock_path,
        **_mapping_kwargs(),
    )
    plan_path = write_v4_3_prevalence_plan_new(root / "prevalence-plan.json", plan)
    artifact = build_v4_3_prevalence_artifact(
        cache_directory,
        trust_lock_path=lock_path,
        prevalence_plan_path=plan_path,
        **_mapping_kwargs(),
    )
    artifact_path = write_v4_3_prevalence_artifact_new(
        root / "prevalence-artifact.json",
        artifact,
    )
    verified_provider = verify_v4_3_prevalence_artifact(
        artifact_path,
        cache_directory=cache_directory,
        trust_lock_path=lock_path,
        prevalence_plan_path=plan_path,
        **_mapping_kwargs(),
    )
    return _RealPrevalenceHarness(
        cache_directory=cache_directory,
        trust_lock_path=lock_path,
        verified_cache=verified,
        plan_path=plan_path,
        plan=plan,
        artifact_path=artifact_path,
        artifact=artifact,
        provider=verified_provider,
    )


def _registry(*specs: FeatureColumnSpec) -> tuple[FeatureColumnSpec, ...]:
    return tuple(sorted(specs, key=lambda item: item.feature_id))


def _spec(feature_id: FeatureId, storage: FeatureStorageType) -> FeatureColumnSpec:
    return FeatureColumnSpec(feature_id=feature_id.value, storage_type=storage)


def test_real_cache_plan_and_artifact_bind_complete_identity_chain(
    real_harness: _RealPrevalenceHarness,
) -> None:
    plan = real_harness.plan
    provenance = real_harness.provider.provenance
    library = MappingLibraryV2.model_validate_json(MAPPING.read_bytes(), strict=True)

    assert plan.mapping_library_sha256 == sha256_file(MAPPING) == library.sha256()
    assert plan.mapping_source_library_sha256 == sha256_file(MAPPING_SOURCE)
    assert plan.mapping_prevalence_plan_sha256 == mapping_prevalence_plan_sha256(
        library
    )
    assert plan.mapping_required_feature_registry_sha256 == (
        library.required_feature_registry_sha256
    )
    assert provenance.anchor_ids == tuple(sorted(provenance.anchor_ids))
    assert provenance.anchor_ids == tuple(anchor.anchor_id for anchor in plan.anchors)
    assert provenance.plan_sha256 == sha256_file(real_harness.plan_path)
    assert provenance.artifact_sha256 == sha256_file(real_harness.artifact_path)
    assert provenance.mapping_library_sha256 == plan.mapping_library_sha256
    assert provenance.mapping_source_library_sha256 == (
        plan.mapping_source_library_sha256
    )
    assert provenance.mapping_prevalence_plan_sha256 == (
        plan.mapping_prevalence_plan_sha256
    )
    assert provenance.parent_hierarchy_sha256 == (
        mapping_prevalence_parent_hierarchy_sha256(library)
    )
    assert provenance.required_feature_registry_sha256 == (
        plan.mapping_required_feature_registry_sha256
    )
    assert provenance.cache_manifest_sha256 == (
        real_harness.verified_cache.manifest_sha256
    )
    assert provenance.cache_trust_lock_sha256 == sha256_file(
        real_harness.trust_lock_path
    )
    assert provenance.cache_build_plan_sha256 == (
        real_harness.verified_cache.manifest.build_plan_sha256
    )
    assert provenance.conditional is True
    assert provenance.duration_weighted is True
    assert provenance.exact_stable_intervals is True


def test_real_provider_opens_and_completes_canonical_scoring_session(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
) -> None:
    source = mapping_fixtures._source(bind_question_bank=True)
    library = compile_mapping_library_v2(source)
    source_path = tmp_path / "mapping-source.json"
    library_path = tmp_path / "mapping.json"
    source_path.write_bytes(canonical_json_bytes(source))
    library_path.write_bytes(canonical_json_bytes(library))
    mapping_kwargs = {
        "mapping_library_path": library_path,
        "mapping_source_library_path": source_path,
        "mapping_repository_root": ROOT,
    }
    plan = derive_v4_3_prevalence_plan(
        real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        **mapping_kwargs,
    )
    plan_path = write_v4_3_prevalence_plan_new(tmp_path / "plan.json", plan)
    artifact = build_v4_3_prevalence_artifact(
        real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence_plan_path=plan_path,
        **mapping_kwargs,
    )
    artifact_path = write_v4_3_prevalence_artifact_new(
        tmp_path / "artifact.json",
        artifact,
    )
    provider = verify_v4_3_prevalence_artifact(
        artifact_path,
        cache_directory=real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence_plan_path=plan_path,
        **mapping_kwargs,
    )
    session = CanonicalV43ScoringSession.open(
        mapping_library=library,
        cache_directory=real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence=provider,
    )
    responses = tuple(
        V43ObservedResponse(
            observation_id=rule.observation_id,
            response_token=rule.response_rule.unknown_response_tokens[0],
        )
        for rule in library.rules
    )
    tuple(session.stream_verified_universe(responses))
    complete = session.require_streamed_universe_compliance()
    assert complete.compliance.v4_3_compliant is True
    assert complete.scored_candidate_count == (
        real_harness.verified_cache.manifest.interval_count
    )


def test_tracked_direct_target_mapping_uses_bound_context_and_claims_complete_universe(
    real_harness: _RealPrevalenceHarness,
) -> None:
    library = MappingLibraryV2.model_validate_json(MAPPING.read_bytes(), strict=True)
    provider = verify_v4_3_prevalence_artifact(
        real_harness.artifact_path,
        cache_directory=real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence_plan_path=real_harness.plan_path,
        **_mapping_kwargs(),
    )
    session = CanonicalV43ScoringSession.open(
        mapping_library=library,
        cache_directory=real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence=provider,
    )
    target_source = next(
        item
        for item in library.source_artifacts
        if item.source_id == library.behavioral_target_source_id
    )
    assert session.bindings.response_source_mode.value == "direct_behavioral_target"
    assert session.bindings.response_source_id == library.behavioral_target_source_id
    assert session.bindings.response_source_sha256 == target_source.sha256
    assert session.bindings.behavioral_target_sha256 == target_source.sha256
    assert session.bindings.question_bank_sha256 is None

    responses = tuple(
        V43ObservedResponse(
            observation_id=rule.observation_id,
            response_token=rule.response_rule.canonical_response_token,
        )
        for rule in library.rules
    )
    with pytest.raises(V43IntegrationError, match="complete declared universe"):
        session.require_streamed_universe_compliance()
    evaluations = tuple(session.stream_verified_universe(responses))

    assert all(
        isinstance(item.scoring_input.candidate_context, V43BoundCandidateRecord)
        for item in evaluations
    )
    assert any(item.score.detailed_support > 0.0 for item in evaluations)
    with pytest.raises(V43PrevalenceError, match="provider-bound cache member"):
        provider.estimate(
            real_harness.plan.anchors[0].anchor_id,
            next(iter_verified_century_cache_rows(real_harness.verified_cache)),
        )
    with pytest.raises(V43IntegrationError, match="cannot mix"):
        session.score_candidate(
            next(iter_verified_century_cache_rows(real_harness.verified_cache)),
            responses,
        )
    complete = session.require_streamed_universe_compliance()
    assert complete.compliance.v4_3_compliant is True
    assert complete.scored_candidate_count == (
        real_harness.verified_cache.manifest.interval_count
    )


@pytest.mark.parametrize(
    ("variant", "compiled_path", "source_path", "response_path"),
    (
        (
            "less_contaminated",
            LESS_CONTAMINATED_COMPILED_PATH,
            LESS_CONTAMINATED_SOURCE_PATH,
            LESS_CONTAMINATED_RESPONSE_PATH,
        ),
        (
            "best_current_descriptive",
            BEST_CURRENT_COMPILED_PATH,
            BEST_CURRENT_SOURCE_PATH,
            BEST_CURRENT_RESPONSE_PATH,
        ),
    ),
)
def test_tracked_direct_target_responses_are_exact_mechanical_compilations(
    variant: str,
    compiled_path: str,
    source_path: str,
    response_path: str,
) -> None:
    artifact = compile_v4_3_direct_target_responses(
        repository_root=ROOT,
        mapping_library_path=ROOT / compiled_path,
        mapping_source_library_path=ROOT / source_path,
        variant=variant,  # type: ignore[arg-type]
    )
    tracked = ROOT / response_path
    assert tracked.read_bytes() == canonical_json_bytes(artifact)
    verified = verify_v4_3_direct_target_responses(
        tracked,
        repository_root=ROOT,
        mapping_library_path=ROOT / compiled_path,
        mapping_source_library_path=ROOT / source_path,
    )
    assert verified.artifact.outcome_data_used is False
    assert verified.artifact.question_bank_source_id is None
    assert tuple(item.observation_id for item in verified.artifact.observations) == (
        tuple(sorted(item.observation_id for item in verified.artifact.observations))
    )


def test_direct_target_response_variant_cannot_be_relabelled() -> None:
    with pytest.raises(ValueError, match="declared canonical V3.6 variant"):
        compile_v4_3_direct_target_responses(
            repository_root=ROOT,
            mapping_library_path=ROOT / BEST_CURRENT_COMPILED_PATH,
            mapping_source_library_path=ROOT / BEST_CURRENT_SOURCE_PATH,
            variant="less_contaminated",
        )


def _rank_record(
    ordinal: int,
    *,
    net: float,
    contradictions: int,
    detailed: float,
    core: float,
    duration_microseconds: int,
) -> V43MinimalScoreRecordV1:
    start = datetime(2000, 1, 1, tzinfo=UTC) + timedelta(seconds=ordinal)
    evidence = max(net, 0.0)
    contradiction_bits = evidence - net
    return V43MinimalScoreRecordV1(
        input_ordinal=ordinal,
        state_id=f"state-{ordinal:03d}",
        candidate_record_sha256=f"{ordinal + 1:064x}",
        utc_start=start,
        utc_end_exclusive=start + timedelta(microseconds=duration_microseconds),
        stable_duration_microseconds=duration_microseconds,
        evidence_rubric_bits=evidence,
        contradiction_rubric_bits=contradiction_bits,
        net_information=net,
        meaningful_contradictions=contradictions,
        detailed_support=detailed,
        core_fit=core,
        unresolved_observation_count=0,
    )


def test_sqlite_external_rank_is_exactly_python_tuple_equivalent(
    tmp_path: Path,
) -> None:
    records = (
        _rank_record(
            0,
            net=0.0,
            contradictions=0,
            detailed=50.0,
            core=80.0,
            duration_microseconds=6_000_000_000_000_000,
        ),
        _rank_record(
            1,
            net=-0.0,
            contradictions=0,
            detailed=50.0,
            core=80.0,
            duration_microseconds=6_000_000_000_000_000,
        ),
        _rank_record(
            2,
            net=math.nextafter(1.0, 2.0),
            contradictions=2,
            detailed=1.0,
            core=1.0,
            duration_microseconds=1,
        ),
        _rank_record(
            3,
            net=1.0,
            contradictions=0,
            detailed=100.0,
            core=100.0,
            duration_microseconds=2,
        ),
        _rank_record(
            4,
            net=1.0,
            contradictions=0,
            detailed=math.nextafter(100.0, 0.0),
            core=100.0,
            duration_microseconds=3,
        ),
    )
    store = V43ExternalRankStore(tmp_path / "rank.sqlite3")
    try:
        for record in records:
            store.append(record)
        store.finish()
        actual = tuple(store.iter_ranked())
    finally:
        store.close()
    expected_order = tuple(
        sorted(records, key=lambda item: (item.substantive_rank_key, item.display_key))
    )
    assert tuple(item.score for item in actual) == expected_order
    for index, ranked in enumerate(actual):
        tied = tuple(
            item
            for item in expected_order
            if item.substantive_rank_key == ranked.score.substantive_rank_key
        )
        expected_start = expected_order.index(tied[0]) + 1
        assert ranked.rank_start == expected_start
        assert ranked.rank_end == expected_start + len(tied) - 1
        assert ranked.midrank_numerator == ranked.rank_start + ranked.rank_end
        assert ranked.score == expected_order[index]

    verifier_store = V43ExternalRankStore(tmp_path / "verify-rank.sqlite3")
    for record in reversed(expected_order):
        verifier_store.append_unordered_for_verification(record)
    verifier_store.finish_unordered_for_verification()
    assert tuple(verifier_store.iter_input_order()) == records
    verifier_store.close()


def _phase4_kwargs(real_harness: _RealPrevalenceHarness) -> dict[str, object]:
    return {
        "repository_root": ROOT,
        "cache_directory": real_harness.cache_directory,
        "trust_lock_path": real_harness.trust_lock_path,
        "mapping_library_path": MAPPING,
        "mapping_source_library_path": MAPPING_SOURCE,
        "prevalence_plan_path": real_harness.plan_path,
        "prevalence_artifact_path": real_harness.artifact_path,
        "response_artifact_path": ROOT / BEST_CURRENT_RESPONSE_PATH,
    }


def test_phase4_run_and_verifier_are_cache_only_and_complete(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import hdmatch.cli as cli

    monkeypatch.setattr(
        cli,
        "ExactChartAdapter",
        lambda *args, **kwargs: pytest.fail("Phase-4 invoked astronomy"),
    )
    output = tmp_path / "run"
    assert cli.main(
        [
            "run-v4-3-cache",
            "--repository-root",
            str(ROOT),
            "--cache",
            str(real_harness.cache_directory),
            "--trust-lock",
            str(real_harness.trust_lock_path),
            "--mapping-library",
            str(MAPPING),
            "--mapping-source-library",
            str(MAPPING_SOURCE),
            "--prevalence-plan",
            str(real_harness.plan_path),
            "--prevalence-artifact",
            str(real_harness.artifact_path),
            "--responses",
            str(ROOT / BEST_CURRENT_RESPONSE_PATH),
            "--output",
            str(output),
            "--detail-limit",
            "1",
        ]
    ) == 0
    verified = verify_v4_3_run(
        output,
        **_phase4_kwargs(real_harness),  # type: ignore[arg-type]
    )
    assert verified.manifest.run_status == "complete"
    assert verified.manifest.compliance is not None
    assert verified.manifest.compliance.v4_3_compliant is True
    assert verified.manifest.successfully_scored_count == (
        real_harness.verified_cache.manifest.interval_count
    )
    assert (output / "ranked-scores.parquet.zst").is_file()
    assert not (output / ".rank.sqlite3").exists()
    assert verified.manifest_path.is_file()


def test_phase4_preflight_mismatch_fails_before_scoring(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hdmatch.model.v4_3.integration import CanonicalV43ScoringSession

    tampered = tmp_path / "responses.json"
    payload = json.loads((ROOT / BEST_CURRENT_RESPONSE_PATH).read_bytes())
    payload["mapping_library_sha256"] = "0" * 64
    tampered.write_bytes(canonical_json_bytes(payload))
    monkeypatch.setattr(
        CanonicalV43ScoringSession,
        "stream_verified_universe",
        lambda *args, **kwargs: pytest.fail("scoring began before preflight completed"),
    )
    kwargs = _phase4_kwargs(real_harness)
    kwargs["response_artifact_path"] = tampered
    with pytest.raises(ValueError):
        run_verified_v4_3_cache(
            output_directory=tmp_path / "must-not-exist",
            **kwargs,  # type: ignore[arg-type]
        )
    assert not (tmp_path / "must-not-exist").exists()


def test_phase4_storage_failure_publishes_noncompliant_failure_package(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = V43ExternalRankStore.append
    calls = 0

    def fail_second_append(
        store: V43ExternalRankStore,
        record: V43MinimalScoreRecordV1,
    ) -> None:
        nonlocal calls
        if calls == 1:
            raise OSError("deterministic injected storage failure")
        calls += 1
        original(store, record)

    monkeypatch.setattr(V43ExternalRankStore, "append", fail_second_append)
    output = tmp_path / "failed-run"
    with pytest.raises(V43RunFailedError) as raised:
        run_verified_v4_3_cache(
            output_directory=output,
            **_phase4_kwargs(real_harness),  # type: ignore[arg-type]
        )
    assert raised.value.failure.stage == "score-store-write"
    assert raised.value.failure.successfully_scored_count == 1
    manifest = json.loads((output / "manifest.json").read_bytes())
    assert manifest["run_status"] == "failed"
    assert manifest["compliance"] is None
    assert manifest["ranked_artifact"] is None
    assert json.loads((output / "failure.json").read_bytes())["state_id"]
    monkeypatch.undo()
    verified = verify_v4_3_run(
        output,
        **_phase4_kwargs(real_harness),  # type: ignore[arg-type]
    )
    assert verified.manifest.run_status == "failed"


def test_phase4_evaluation_failure_records_exact_unscored_row(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hdmatch.model.v4_3.integration import CanonicalV43ScoringSession

    original = CanonicalV43ScoringSession._score_bound_candidate
    calls = 0

    def fail_second_evaluation(
        session: CanonicalV43ScoringSession,
        *args: object,
        **kwargs: object,
    ) -> object:
        nonlocal calls
        if calls == 1:
            raise RuntimeError("deterministic injected evaluation failure")
        calls += 1
        return original(session, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(
        CanonicalV43ScoringSession,
        "_score_bound_candidate",
        fail_second_evaluation,
    )
    output = tmp_path / "failed-evaluation-run"
    with pytest.raises(V43RunFailedError) as raised:
        run_verified_v4_3_cache(
            output_directory=output,
            **_phase4_kwargs(real_harness),  # type: ignore[arg-type]
        )
    failure = raised.value.failure
    assert failure.stage == "evaluation"
    assert failure.input_ordinal == 1
    assert failure.successfully_scored_count == 1
    assert failure.state_id is not None
    assert failure.candidate_record_sha256 is not None
    monkeypatch.undo()
    assert verify_v4_3_run(
        output,
        **_phase4_kwargs(real_harness),  # type: ignore[arg-type]
    ).manifest.run_status == "failed"


def test_prevalence_cli_build_and_verify_use_only_verified_cache(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import hdmatch.cli as cli

    monkeypatch.setattr(
        cli,
        "ExactChartAdapter",
        lambda *args, **kwargs: pytest.fail("prevalence CLI invoked astronomy"),
    )
    plan = tmp_path / "cli-plan.json"
    artifact = tmp_path / "cli-artifact.json"
    common = [
        "--repository-root",
        str(ROOT),
        "--cache",
        str(real_harness.cache_directory),
        "--trust-lock",
        str(real_harness.trust_lock_path),
        "--mapping-library",
        str(MAPPING),
        "--mapping-source-library",
        str(MAPPING_SOURCE),
    ]
    assert cli.main(
        [
            "build-v4-3-prevalence",
            *common,
            "--plan-output",
            str(plan),
            "--artifact-output",
            str(artifact),
        ]
    ) == 0
    assert cli.main(
        [
            "verify-v4-3-prevalence",
            *common,
            "--plan",
            str(plan),
            "--artifact",
            str(artifact),
        ]
    ) == 0


def test_global_prevalence_is_duration_weighted_not_row_weighted(
    real_harness: _RealPrevalenceHarness,
) -> None:
    rows = tuple(iter_verified_century_cache_rows(real_harness.verified_cache))
    registry = real_harness.verified_cache.manifest.feature_registry
    table_by_id = {table.anchor_id: table for table in real_harness.artifact.tables}
    chosen: tuple[int, int, int] | None = None
    for anchor in real_harness.plan.anchors:
        matches = sum(
            v4_3_predicate_matches(anchor.predicate, row.feature_mapping(), registry)
            for row in rows
        )
        root = table_by_id[anchor.anchor_id].cells[-1]
        if (
            0 < matches < len(rows)
            and root.numerator_duration_microseconds
            * len(rows)
            != root.denominator_duration_microseconds * matches
        ):
            chosen = (
                root.numerator_duration_microseconds,
                root.denominator_duration_microseconds,
                matches,
            )
            break
    assert chosen is not None
    numerator, denominator, matching_rows = chosen
    assert numerator / denominator != matching_rows / len(rows)
    assert denominator == 60_000_000


def test_frozen_500_state_equivalent_backoff_uses_terminal_root(
    real_harness: _RealPrevalenceHarness,
) -> None:
    provider = real_harness.provider
    member = next(provider.iter_cache_members())
    candidate = provider.bind_candidate_record(
        member,
        cache_manifest_sha256=provider.provenance.cache_manifest_sha256,
        mapping_library_sha256=provider.provenance.mapping_library_sha256,
    )
    table_by_id = {table.anchor_id: table for table in provider.artifact.tables}
    anchor = next(
        item
        for item in real_harness.plan.anchors
        if len(item.parent_hierarchy) > 1
        and table_by_id[item.anchor_id].cells[-1].numerator_duration_microseconds > 0
    )
    estimate = provider.estimate(anchor.anchor_id, candidate)

    assert provider.artifact.policy.minimum_effective_state_equivalents == 500
    assert estimate.backoff_ordinal == len(anchor.parent_hierarchy) - 1
    assert estimate.selected_level_id == anchor.parent_hierarchy[-1].level_id
    assert estimate.selected_level_conditional is False
    assert estimate.attempts[-1].minimum_effective_size_met is False
    assert estimate.conditional is True
    assert estimate.plan_sha256 == provider.provenance.plan_sha256
    assert estimate.mapping_library_sha256 == (
        provider.provenance.mapping_library_sha256
    )
    assert estimate.mapping_prevalence_plan_sha256 == (
        provider.provenance.mapping_prevalence_plan_sha256
    )
    assert estimate.cache_manifest_sha256 == (
        provider.provenance.cache_manifest_sha256
    )


def test_candidate_membership_is_private_provider_specific_and_identity_bound(
    real_harness: _RealPrevalenceHarness,
) -> None:
    provider = real_harness.provider
    raw = next(iter_verified_century_cache_rows(real_harness.verified_cache))
    with pytest.raises(V43PrevalenceError, match="requested cache manifest mismatch"):
        provider.bind_candidate_record(
            raw,
            cache_manifest_sha256="0" * 64,
            mapping_library_sha256=provider.provenance.mapping_library_sha256,
        )
    bound = provider.bind_candidate_record(
        raw,
        cache_manifest_sha256=provider.provenance.cache_manifest_sha256,
        mapping_library_sha256=provider.provenance.mapping_library_sha256,
    )
    assert bound.state_id == raw.state_id
    substituted = raw.model_copy(update={"state_id": "STATE-V2-SUBSTITUTED"})
    with pytest.raises(V43PrevalenceError, match="next replay-verified"):
        provider.bind_candidate_record(
            substituted,
            cache_manifest_sha256=provider.provenance.cache_manifest_sha256,
            mapping_library_sha256=provider.provenance.mapping_library_sha256,
        )
    member = next(provider.iter_cache_members())
    with pytest.raises(V43PrevalenceError, match="requested mapping library mismatch"):
        provider.bind_candidate_record(
            member,
            cache_manifest_sha256=provider.provenance.cache_manifest_sha256,
            mapping_library_sha256="0" * 64,
        )
    other = verify_v4_3_prevalence_artifact(
        real_harness.artifact_path,
        cache_directory=real_harness.cache_directory,
        trust_lock_path=real_harness.trust_lock_path,
        prevalence_plan_path=real_harness.plan_path,
        **_mapping_kwargs(),
    )
    with pytest.raises(V43PrevalenceError, match="another provider"):
        other.bind_candidate_record(
            member,
            cache_manifest_sha256=other.provenance.cache_manifest_sha256,
            mapping_library_sha256=other.provenance.mapping_library_sha256,
        )


def test_candidate_pool_substitution_has_no_builder_or_lookup_path(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
) -> None:
    parameters = inspect.signature(build_v4_3_prevalence_artifact).parameters
    assert not {"rows", "candidates", "candidate_file", "candidate_pool"} & set(
        parameters
    )
    candidate_file = tmp_path / "candidate-pool.json"
    candidate_file.write_bytes(canonical_json_bytes([{"architecture.type": "projector"}]))
    with pytest.raises(V43PrevalenceError, match="prebuilt verified century cache"):
        derive_v4_3_prevalence_plan(
            candidate_file,
            trust_lock_path=real_harness.trust_lock_path,
            **_mapping_kwargs(),
        )


def test_stale_plan_and_mapping_byte_substitution_fail_closed(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
) -> None:
    stale_payload = real_harness.plan.model_dump(mode="json")
    stale_payload["mapping_library_sha256"] = "0" * 64
    stale_plan = tmp_path / "stale-plan.json"
    stale_plan.write_bytes(canonical_json_bytes(stale_payload))
    with pytest.raises(V43PrevalenceError, match="invalid prevalence plan"):
        build_v4_3_prevalence_artifact(
            real_harness.cache_directory,
            trust_lock_path=real_harness.trust_lock_path,
            prevalence_plan_path=stale_plan,
            **_mapping_kwargs(),
        )

    source_payload = json.loads(MAPPING_SOURCE.read_bytes())
    source_payload["mappings"][0]["rationale"] = (
        f"{source_payload['mappings'][0]['rationale']} tampered"
    )
    tampered_source = tmp_path / "mapping-source.json"
    tampered_source.write_bytes(canonical_json_bytes(source_payload))
    with pytest.raises(V43PrevalenceError, match="another source library"):
        derive_v4_3_prevalence_plan(
            real_harness.cache_directory,
            trust_lock_path=real_harness.trust_lock_path,
            mapping_library_path=MAPPING,
            mapping_source_library_path=tampered_source,
            mapping_repository_root=ROOT,
        )


def test_lock_swap_during_cache_verification_fails_closed(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lock_path = tmp_path / "swapped-lock.json"
    original = real_harness.trust_lock_path.read_bytes()
    lock_path.write_bytes(original)
    real_verify = prevalence_module.verify_century_cache

    def _verify_then_swap(*args: object, **kwargs: object) -> VerifiedCenturyCache:
        verified = real_verify(*args, **kwargs)
        lock_path.write_bytes(original + b"\n")
        return verified

    monkeypatch.setattr(prevalence_module, "verify_century_cache", _verify_then_swap)
    with pytest.raises(V43PrevalenceError, match="trust lock changed"):
        derive_v4_3_prevalence_plan(
            real_harness.cache_directory,
            trust_lock_path=lock_path,
            **_mapping_kwargs(),
        )


def test_mapping_swap_during_cache_verification_fails_closed(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    library_path = tmp_path / "mapping.json"
    source_path = tmp_path / "mapping-source.json"
    original_library = MAPPING.read_bytes()
    library_path.write_bytes(original_library)
    source_path.write_bytes(MAPPING_SOURCE.read_bytes())
    real_verify = prevalence_module.verify_century_cache

    def _verify_then_swap(*args: object, **kwargs: object) -> VerifiedCenturyCache:
        verified = real_verify(*args, **kwargs)
        library_path.write_bytes(original_library + b"\n")
        return verified

    monkeypatch.setattr(prevalence_module, "verify_century_cache", _verify_then_swap)
    with pytest.raises(V43PrevalenceError, match="compiled mapping changed"):
        derive_v4_3_prevalence_plan(
            real_harness.cache_directory,
            trust_lock_path=real_harness.trust_lock_path,
            mapping_library_path=library_path,
            mapping_source_library_path=source_path,
            mapping_repository_root=ROOT,
        )


def test_plan_swap_during_duration_replay_fails_closed(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan_path = tmp_path / "plan.json"
    original_plan = real_harness.plan_path.read_bytes()
    plan_path.write_bytes(original_plan)
    real_rows = prevalence_module.iter_verified_century_cache_rows

    def _rows_then_swap(cache: VerifiedCenturyCache) -> Any:
        changed = False
        for row in real_rows(cache):
            if not changed:
                plan_path.write_bytes(original_plan + b"\n")
                changed = True
            yield row

    monkeypatch.setattr(
        prevalence_module,
        "iter_verified_century_cache_rows",
        _rows_then_swap,
    )
    with pytest.raises(V43PrevalenceError, match="plan changed"):
        build_v4_3_prevalence_artifact(
            real_harness.cache_directory,
            trust_lock_path=real_harness.trust_lock_path,
            prevalence_plan_path=plan_path,
            **_mapping_kwargs(),
        )


def test_artifact_rejects_skipped_conditional_backoff_level(
    real_harness: _RealPrevalenceHarness,
) -> None:
    payload = real_harness.artifact.model_dump(mode="json")
    target_index = next(
        index
        for index, anchor in enumerate(real_harness.plan.anchors)
        if len(anchor.parent_hierarchy) > 1
    )
    payload["tables"][target_index]["cells"] = [
        cell
        for cell in payload["tables"][target_index]["cells"]
        if cell["backoff_ordinal"] != 0
    ]
    with pytest.raises(ValidationError, match="skips a backoff level"):
        V43ConditionalPrevalenceArtifactV1.model_validate_json(
            canonical_json_bytes(payload),
            strict=True,
        )


def test_artifact_tamper_cannot_pass_replay(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
) -> None:
    tampered = tmp_path / "tampered-artifact.json"
    tampered.write_bytes(real_harness.artifact_path.read_bytes() + b"\n")
    with pytest.raises(V43PrevalenceError, match="canonically encoded"):
        verify_v4_3_prevalence_artifact(
            tampered,
            cache_directory=real_harness.cache_directory,
            trust_lock_path=real_harness.trust_lock_path,
            prevalence_plan_path=real_harness.plan_path,
            **_mapping_kwargs(),
        )


def test_predicates_are_feature_aware_and_type_strict() -> None:
    type_predicate = StructuralPredicateV2(
        feature_id=FeatureId.TYPE,
        operator=PredicateOperatorV2.EQUALS_ANY,
        values=("projector",),
    )
    type_registry = _registry(_spec(FeatureId.TYPE, FeatureStorageType.STRING))
    assert v4_3_predicate_matches(
        type_predicate,
        {FeatureId.TYPE.value: "projector"},
        type_registry,
    )
    for invalid in (True, 1, None):
        with pytest.raises(V43PrevalenceError):
            v4_3_predicate_matches(
                type_predicate,
                {FeatureId.TYPE.value: invalid},
                type_registry,
            )
    with pytest.raises(V43PrevalenceError, match="differs from registry"):
        v4_3_predicate_matches(type_predicate, {}, type_registry)
    with pytest.raises(V43PrevalenceError, match="unknown.field"):
        v4_3_predicate_matches(
            type_predicate,
            {
                FeatureId.TYPE.value: "projector",
                "unknown.field": "unexpected",
            },
            type_registry,
        )
    with pytest.raises(ValidationError):
        StructuralPredicateV2.model_validate(
            {
                "feature_id": FeatureId.TYPE.value,
                "operator": "unknown_operator",
                "values": ["projector"],
            }
        )


def test_exclusion_and_structured_predicates_reject_malformed_shapes() -> None:
    centers = StructuralPredicateV2(
        feature_id=FeatureId.CENTERS,
        operator=PredicateOperatorV2.NOT_CONTAINS_ANY,
        values=("heart_ego",),
    )
    centers_registry = _registry(_spec(FeatureId.CENTERS, FeatureStorageType.JSON))
    assert v4_3_predicate_matches(
        centers,
        {
            FeatureId.CENTERS.value: {
                "defined": ["sacral"],
                "undefined": [
                    "ajna",
                    "g",
                    "head",
                    "heart_ego",
                    "root",
                    "solar_plexus",
                    "spleen",
                    "throat",
                ],
            }
        },
        centers_registry,
    )
    with pytest.raises(V43PrevalenceError, match="exact defined/undefined"):
        v4_3_predicate_matches(
            centers,
            {
                    FeatureId.CENTERS.value: {
                        "defined": ["sacral"],
                        "undefined": ["heart_ego"],
                    "unknown": [],
                }
            },
            centers_registry,
        )

    hanging = StructuralPredicateV2(
        feature_id=FeatureId.HANGING_GATES,
        operator=PredicateOperatorV2.HAS_GATE,
        side="personality",
        gate=61,
    )
    hanging_registry = _registry(
        _spec(FeatureId.ACTIVATION_GATE, FeatureStorageType.INT64_LIST),
        _spec(FeatureId.ACTIVATION_SIDE, FeatureStorageType.STRING_LIST),
        _spec(FeatureId.ACTIVE_GATES, FeatureStorageType.JSON),
        _spec(FeatureId.HANGING_GATES, FeatureStorageType.INT64_LIST),
    )
    features: dict[str, Any] = {
        FeatureId.ACTIVATION_GATE.value: [61],
        FeatureId.ACTIVATION_SIDE.value: ["personality"],
        FeatureId.HANGING_GATES.value: [61],
        FeatureId.ACTIVE_GATES.value: [
            {
                "gate": 61,
                "activation_count": 1,
                "activation_positions": ["personality:sun"],
            }
        ],
    }
    assert v4_3_predicate_matches(hanging, features, hanging_registry)
    features[FeatureId.HANGING_GATES.value] = [True]
    with pytest.raises(V43PrevalenceError, match="storage type"):
        v4_3_predicate_matches(hanging, features, hanging_registry)


def test_activation_and_channel_predicates_reject_unknown_fields() -> None:
    activation = StructuralPredicateV2(
        feature_id=FeatureId.PLANETARY_ACTIVATIONS,
        operator=PredicateOperatorV2.MATCHES_ACTIVATION,
        side="personality",
        gate=61,
    )
    activation_registry = _registry(
        _spec(FeatureId.ACTIVATION_GATE, FeatureStorageType.INT64_LIST),
        _spec(FeatureId.ACTIVATION_SIDE, FeatureStorageType.STRING_LIST),
        _spec(FeatureId.PLANETARY_ACTIVATIONS, FeatureStorageType.ACTIVATION_LIST),
    )
    activation_features: dict[str, Any] = {
        FeatureId.ACTIVATION_GATE.value: [61],
        FeatureId.ACTIVATION_SIDE.value: ["personality"],
        FeatureId.PLANETARY_ACTIVATIONS.value: [
            {
                "body": "sun",
                "side": "personality",
                "gate": 61,
                "line": 1,
                "color": None,
                "tone": None,
                "base": None,
            }
        ],
    }
    assert v4_3_predicate_matches(
        activation,
        activation_features,
        activation_registry,
    )
    activation_features[FeatureId.PLANETARY_ACTIVATIONS.value][0]["extra"] = True
    with pytest.raises(V43PrevalenceError, match="unknown activation fields"):
        v4_3_predicate_matches(
            activation,
            activation_features,
            activation_registry,
        )

    channel = StructuralPredicateV2(
        feature_id=FeatureId.COMPLETE_CHANNELS,
        operator=PredicateOperatorV2.CONTAINS_ANY,
        values=("1-8",),
    )
    channel_registry = _registry(
        _spec(FeatureId.COMPLETE_CHANNELS, FeatureStorageType.JSON)
    )
    with pytest.raises(V43PrevalenceError, match="unknown complete-Channel fields"):
        v4_3_predicate_matches(
            channel,
            {
                FeatureId.COMPLETE_CHANNELS.value: [
                    {
                        "channel": "1-8",
                        "gate_a": 1,
                        "gate_b": 8,
                        "center_a": "g",
                        "center_b": "throat",
                        "extra": False,
                    }
                ]
            },
            channel_registry,
        )


def test_plan_and_policy_are_deterministic_and_fail_closed() -> None:
    first = V43ConditionalPrevalencePolicyV1()
    second = V43ConditionalPrevalencePolicyV1()
    assert first == second
    assert first.sha256() == second.sha256()
    assert first.minimum_effective_state_equivalents == 500
    assert capped_information_rubric_bits(1, 1 << 20) == 6.0
    assert capped_information_rubric_bits(1, 2) == 1.0
    assert capped_information_rubric_bits(1, 1) == 0.0
    with pytest.raises(V43PrevalenceError, match="prevalence must be"):
        capped_information_rubric_bits(0, 100)


def test_plan_file_rejects_noncanonical_bytes(
    real_harness: _RealPrevalenceHarness,
    tmp_path: Path,
) -> None:
    noncanonical = tmp_path / "plan.json"
    noncanonical.write_bytes(real_harness.plan_path.read_bytes() + b"\n")
    with pytest.raises(V43PrevalenceError, match="canonically encoded"):
        load_v4_3_prevalence_plan(noncanonical)
