from __future__ import annotations

import inspect
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from hdmatch.evaluation.behavioral_difference import (
    BehavioralDifferenceAudit,
    VerifiedBehavioralDifferenceBinding,
    audit_behavioral_difference,
    load_behavioral_difference_audit,
    require_behavioral_difference,
    verify_behavioral_difference_audit,
)
from hdmatch.experiments.canonical import sha256_file, write_new_canonical_json
from hdmatch.runtime.universe_cache import (
    CachedUniverse,
    MonthRequest,
    load_cached_universe,
)
from hdmatch.schemas import (
    BehavioralResponse,
    CandidateState,
    ChartFeatures,
    LocalDateOverlap,
    ScoredState,
)

_ENGINE_FINGERPRINT = "e" * 64
_REQUEST = MonthRequest(2000, 1, "UTC")
_AUDITED_AT = datetime(2026, 8, 21, 22, tzinfo=UTC)


def _response(question_id: str, answer: str, cluster: str) -> BehavioralResponse:
    return BehavioralResponse(
        question_id=question_id,
        cluster_id=cluster,
        answer=answer,
        behavioral_confidence=1.0,
        measurement_reliability=1.0,
    )


def _state(state_id: str, *, channel: str, day: int) -> CandidateState:
    start = datetime(2000, 1, 1 if day == 1 else 16, tzinfo=UTC)
    end = (
        datetime(2000, 1, 16, tzinfo=UTC)
        if day == 1
        else datetime(2000, 2, 1, tzinfo=UTC)
    )
    chart = ChartFeatures(
        personality_utc=start,
        design_utc=start - timedelta(days=88),
        type="generator",
        strategy="wait_to_respond",
        authority="sacral",
        profile="3/5",
        definition="single_definition",
        defined_centers=("g", "throat"),
        channels=(channel,),
        activations={},
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=("a" if state_id.endswith("A") else "b") * 64,
        chart_features=chart,
        local_date_overlaps=tuple(
            LocalDateOverlap(
                date=(start + timedelta(days=offset)).date(),
                seconds=86400.0,
            )
            for offset in range((end - start).days)
        ),
    )


class _FakeModelA:
    model_sha256 = "1" * 64
    mapping_sha256 = "2" * 64
    question_bank_sha256 = "3" * 64
    library = SimpleNamespace(frozen_mappings=())

    def score_signature(self, chart: ChartFeatures) -> tuple[object, ...]:
        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            chart.defined_centers,
        )

    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        return (_response("A01", "wait_to_respond", "core"),)

    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        return _score(state.state_id, 1.0)


class _FakeModelB:
    model_sha256 = "4" * 64
    question_bank_sha256 = "3" * 64

    def __init__(self, compiled: Path, freeze: Path) -> None:
        self.compiled_artifact_path = compiled
        self.freeze_receipt_path = freeze
        self.mapping_sha256 = sha256_file(compiled)
        self.freeze_receipt = SimpleNamespace(
            frozen_at_utc=datetime(2026, 8, 21, 21, tzinfo=UTC)
        )

    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        answer = "distinctly_own" if "1-8" in chart.channels else "unknown"
        return (
            _response("A01", "wait_to_respond", "core"),
            _response("T01", answer, "original"),
        )

    def prepare_prevalence(self, states: object) -> object:
        return object()

    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        items = tuple(responses)  # type: ignore[arg-type]
        answer = next(item.answer for item in items if item.question_id == "T01")
        matches = answer == "distinctly_own" and "1-8" in state.chart_features.channels
        return _score(state.state_id, 2.0 if matches else 0.0)


class _NoDifferenceModelB(_FakeModelB):
    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        return (
            _response("A01", "wait_to_respond", "core"),
            _response("T01", "unknown", "original"),
        )


class _AdverseModelB(_FakeModelB):
    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        items = tuple(responses)  # type: ignore[arg-type]
        answer = next(item.answer for item in items if item.question_id == "T01")
        adverse = answer == "distinctly_own" and "1-8" not in state.chart_features.channels
        return _score(state.state_id, 2.0 if adverse else 0.0)


def _score(state_id: str, value: float) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=value,
        evidence_rubric_bits=value,
        contradiction_rubric_bits=0.0,
        detailed_support=100.0 if value > 1.0 else 0.0,
        core_fit=100.0,
        meaningful_contradictions=0,
    )


def _cache(tmp_path: Path, states: tuple[CandidateState, ...]) -> CachedUniverse:
    path = tmp_path / "candidate-cache.json"
    write_new_canonical_json(
        path,
        {
            "schema_version": "candidate-universe-cache-v1",
            "year": _REQUEST.year,
            "month": _REQUEST.month,
            "timezone": _REQUEST.timezone_name,
            "start_utc": datetime(2000, 1, 1, tzinfo=UTC),
            "end_utc": datetime(2000, 2, 1, tzinfo=UTC),
            "engine_fingerprint": _ENGINE_FINGERPRINT,
            "state_count": len(states),
            "states": [state.model_dump(mode="json") for state in states],
        },
    )
    return load_cached_universe(
        path,
        request=_REQUEST,
        engine_fingerprint=_ENGINE_FINGERPRINT,
    )


def _models(tmp_path: Path, model_b_type: type[_FakeModelB] = _FakeModelB) -> tuple[Any, Any]:
    compiled = tmp_path / "compiled.json"
    freeze = tmp_path / "freeze.json"
    write_new_canonical_json(compiled, {"artifact": "compiled"})
    write_new_canonical_json(freeze, {"artifact": "freeze"})
    return _FakeModelA(), model_b_type(compiled, freeze)


def _build_audit(
    tmp_path: Path,
    model_b_type: type[_FakeModelB] = _FakeModelB,
) -> tuple[BehavioralDifferenceAudit, CachedUniverse, Any, Any]:
    states = (
        _state("STATE-A", channel="1-8", day=1),
        _state("STATE-B", channel="28-38", day=2),
    )
    cache = _cache(tmp_path, states)
    model_a, model_b = _models(tmp_path, model_b_type)
    audit = audit_behavioral_difference(  # type: ignore[arg-type]
        cache,
        model_a,
        model_b,
        engine_fingerprint=_ENGINE_FINGERPRINT,
        audited_at_utc=_AUDITED_AT,
    )
    return audit, cache, model_a, model_b


def _write_audit(tmp_path: Path, audit: object, name: str = "audit.json") -> Path:
    path = tmp_path / name
    write_new_canonical_json(path, audit)
    return path


def test_answer_key_free_audit_requires_response_delta_and_tie_split(
    tmp_path: Path,
) -> None:
    audit, cache, _, model_b = _build_audit(tmp_path)

    assert audit.status == "passed"
    assert audit.schema_version == "model-b-v2-new-behavioral-difference-audit-v2"
    assert audit.audited_at_utc == _AUDITED_AT
    assert audit.answer_keys_used is False
    assert audit.candidate_truth_used is False
    assert audit.model_b_compiled_file_sha256 == sha256_file(
        model_b.compiled_artifact_path
    )
    assert audit.model_b_freeze_receipt_file_sha256 == sha256_file(
        model_b.freeze_receipt_path
    )
    assert audit.candidate_cache_file_sha256 == cache.sha256
    assert audit.candidate_engine_fingerprint == _ENGINE_FINGERPRINT
    assert audit.candidate_universe_request.to_runtime() == _REQUEST
    assert audit.candidate_state_count == len(cache.states)
    assert audit.groups_with_non_unknown_response_delta == 1
    assert audit.groups_with_pairwise_tie_split == 1
    assert audit.groups_with_source_favoring_tie_split == 1
    assert audit.groups_with_adverse_tie_split == 0
    assert audit.witnesses[0].non_unknown_detailed_delta_question_ids == ("T01",)
    assert audit.witnesses[0].model_a_pair_relation == "tie"
    assert audit.witnesses[0].model_b_pair_relation == "source_above_comparison"
    require_behavioral_difference(audit)


def test_failed_difference_is_preserved_and_gate_fails_closed(tmp_path: Path) -> None:
    audit, _, _, _ = _build_audit(tmp_path, _NoDifferenceModelB)
    path = _write_audit(tmp_path, audit)

    assert audit.status == "failed"
    assert audit.witnesses == ()
    assert audit.failure_reasons
    with pytest.raises(ValueError, match="difference gate failed"):
        require_behavioral_difference(audit)
    assert path.is_file()
    assert load_behavioral_difference_audit(path) == audit


def test_adverse_only_tie_split_cannot_pass_difference_gate(tmp_path: Path) -> None:
    audit, _, _, _ = _build_audit(tmp_path, _AdverseModelB)

    assert audit.status == "failed"
    assert audit.groups_with_source_favoring_tie_split == 0
    assert audit.groups_with_adverse_tie_split == 1
    assert audit.witnesses[0].model_b_pair_relation == "comparison_above_source"
    with pytest.raises(ValueError, match="difference gate failed"):
        require_behavioral_difference(audit)


def test_canonical_loader_and_complete_verifier_return_immutable_binding(
    tmp_path: Path,
) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    audit_path = _write_audit(tmp_path, audit)

    loaded = load_behavioral_difference_audit(audit_path)
    binding = verify_behavioral_difference_audit(  # type: ignore[arg-type]
        audit_path,
        model_a=model_a,
        model_b=model_b,
        candidate_cache_path=cache.path,
        candidate_request=_REQUEST,
        engine_fingerprint=_ENGINE_FINGERPRINT,
    )

    assert loaded == audit
    assert binding.audit_file_sha256 == sha256_file(audit_path)
    assert binding.model_b_compiled_file_sha256 == audit.model_b_compiled_file_sha256
    assert binding.model_b_freeze_receipt_file_sha256 == (
        audit.model_b_freeze_receipt_file_sha256
    )
    assert binding.model_b_sha256 == audit.model_b_sha256
    assert binding.question_bank_sha256 == audit.question_bank_sha256
    assert binding.candidate_cache_file_sha256 == cache.sha256
    assert binding.candidate_universe_sha256 == audit.candidate_universe_sha256
    assert binding.candidate_universe_request.to_runtime() == _REQUEST
    with pytest.raises(Exception, match="frozen"):  # pydantic emits a ValidationError
        binding.model_b_sha256 = "f" * 64  # type: ignore[misc]


def test_loader_rejects_missing_and_noncanonical_audit(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="invalid or non-canonical"):
        load_behavioral_difference_audit(tmp_path / "missing.json")

    audit, _, _, _ = _build_audit(tmp_path)
    path = tmp_path / "noncanonical.json"
    path.write_text(
        json.dumps(audit.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="invalid or non-canonical"):
        load_behavioral_difference_audit(path)


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("model_a_sha256", "6" * 64),
        ("model_a_mapping_sha256", "7" * 64),
        ("model_b_sha256", "8" * 64),
        ("model_b_freeze_receipt_file_sha256", "9" * 64),
        ("question_bank_sha256", "a" * 64),
        ("candidate_cache_file_sha256", "b" * 64),
        ("candidate_engine_fingerprint", "c" * 64),
        ("candidate_state_count", 3),
        ("candidate_universe_sha256", "d" * 64),
    ),
)
def test_verifier_rejects_every_stale_audit_binding(
    tmp_path: Path,
    field: str,
    replacement: object,
) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    raw = audit.model_dump(mode="json")
    raw[field] = replacement
    audit_path = _write_audit(tmp_path, raw)

    with pytest.raises(ValueError, match="stale or mismatched"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_verifier_rejects_stale_compiled_and_mapping_hash(tmp_path: Path) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    raw = audit.model_dump(mode="json")
    raw["model_b_mapping_sha256"] = "f" * 64
    raw["model_b_compiled_file_sha256"] = "f" * 64
    audit_path = _write_audit(tmp_path, raw)

    with pytest.raises(ValueError, match="model_b_mapping_sha256"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_loader_rejects_empty_witness_and_inconsistent_pass_claim(tmp_path: Path) -> None:
    audit, _, _, _ = _build_audit(tmp_path)
    empty = audit.model_dump(mode="json")
    empty["witnesses"] = []
    empty_path = _write_audit(tmp_path, empty, "empty.json")
    with pytest.raises(ValueError, match="invalid or non-canonical"):
        load_behavioral_difference_audit(empty_path)

    inconsistent = audit.model_dump(mode="json")
    inconsistent["status"] = "failed"
    inconsistent["failure_reasons"] = ["fabricated failure"]
    inconsistent_path = _write_audit(tmp_path, inconsistent, "inconsistent.json")
    with pytest.raises(ValueError, match="invalid or non-canonical"):
        load_behavioral_difference_audit(inconsistent_path)


def test_verifier_rejects_failed_and_adverse_artifacts_without_deleting_them(
    tmp_path: Path,
) -> None:
    for index, model_type in enumerate((_NoDifferenceModelB, _AdverseModelB)):
        case_root = tmp_path / str(index)
        case_root.mkdir()
        audit, cache, model_a, model_b = _build_audit(case_root, model_type)
        audit_path = _write_audit(case_root, audit)
        with pytest.raises(ValueError, match="difference gate failed"):
            verify_behavioral_difference_audit(  # type: ignore[arg-type]
                audit_path,
                model_a=model_a,
                model_b=model_b,
                candidate_cache_path=cache.path,
                candidate_request=_REQUEST,
                engine_fingerprint=_ENGINE_FINGERPRINT,
            )
        assert audit_path.is_file()
        assert load_behavioral_difference_audit(audit_path) == audit


def test_verifier_rejects_changed_current_model_and_question_bindings(
    tmp_path: Path,
) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    audit_path = _write_audit(tmp_path, audit)

    model_a.model_sha256 = "a" * 64
    with pytest.raises(ValueError, match="model_a_sha256"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )
    model_a.model_sha256 = "1" * 64
    model_b.question_bank_sha256 = "b" * 64
    with pytest.raises(ValueError, match="model_b_question_bank_sha256"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


@pytest.mark.parametrize("artifact", ("compiled", "freeze"))
def test_verifier_rejects_changed_current_v2_artifact_bytes(
    tmp_path: Path,
    artifact: str,
) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    audit_path = _write_audit(tmp_path, audit)
    target = (
        model_b.compiled_artifact_path
        if artifact == "compiled"
        else model_b.freeze_receipt_path
    )
    target.write_bytes(target.read_bytes() + b" ")

    with pytest.raises(ValueError, match=f"model_b_{artifact}"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_verifier_rejects_cache_request_fingerprint_and_exact_bytes(tmp_path: Path) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    audit_path = _write_audit(tmp_path, audit)

    with pytest.raises(ValueError, match="cache year mismatch"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=MonthRequest(2001, 1, "UTC"),
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )
    with pytest.raises(ValueError, match="engine_fingerprint mismatch"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint="f" * 64,
        )

    raw_cache = json.loads(cache.path.read_text(encoding="utf-8"))
    raw_cache["public_note"] = "same states, different exact bytes"
    cache.path.unlink()
    write_new_canonical_json(cache.path, raw_cache)
    with pytest.raises(ValueError, match="candidate_cache_file_sha256"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_full_candidate_state_content_is_covered_by_universe_hash(tmp_path: Path) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    raw_cache = json.loads(cache.path.read_text(encoding="utf-8"))
    raw_cache["states"][0]["boundary_events"] = ["changed-public-boundary-event"]
    cache.path.unlink()
    write_new_canonical_json(cache.path, raw_cache)
    changed_cache_sha256 = sha256_file(cache.path)
    raw_audit = audit.model_dump(mode="json")
    raw_audit["candidate_cache_file_sha256"] = changed_cache_sha256
    audit_path = _write_audit(tmp_path, raw_audit)

    with pytest.raises(ValueError, match="candidate_universe_sha256"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_verifier_rejects_wrong_expected_exact_audit_binding(tmp_path: Path) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    audit_path = _write_audit(tmp_path, audit)
    binding = verify_behavioral_difference_audit(  # type: ignore[arg-type]
        audit_path,
        model_a=model_a,
        model_b=model_b,
        candidate_cache_path=cache.path,
        candidate_request=_REQUEST,
        engine_fingerprint=_ENGINE_FINGERPRINT,
    )
    wrong = VerifiedBehavioralDifferenceBinding.model_validate(
        {
            **binding.model_dump(mode="json"),
            "audit_file_sha256": "f" * 64,
        }
    )
    with pytest.raises(ValueError, match="expected binding"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            audit_path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
            expected_binding=wrong,
        )


def test_audit_and_verifier_enforce_freeze_before_audit_order(tmp_path: Path) -> None:
    states = (
        _state("STATE-A", channel="1-8", day=1),
        _state("STATE-B", channel="28-38", day=2),
    )
    cache = _cache(tmp_path, states)
    model_a, model_b = _models(tmp_path)
    with pytest.raises(ValueError, match="freeze must predate"):
        audit_behavioral_difference(  # type: ignore[arg-type]
            cache,
            model_a,
            model_b,
            engine_fingerprint=_ENGINE_FINGERPRINT,
            audited_at_utc=datetime(2026, 8, 21, 20, tzinfo=UTC),
        )

    audit = audit_behavioral_difference(  # type: ignore[arg-type]
        cache,
        model_a,
        model_b,
        engine_fingerprint=_ENGINE_FINGERPRINT,
        audited_at_utc=_AUDITED_AT,
    )
    raw = audit.model_dump(mode="json")
    raw["audited_at_utc"] = "2026-08-21T20:00:00Z"
    path = _write_audit(tmp_path, raw)
    with pytest.raises(ValueError, match="predates the V2 model freeze"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_verifier_rejects_witness_outside_bound_candidate_universe(tmp_path: Path) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    raw = audit.model_dump(mode="json")
    witness = raw["witnesses"][0]
    witness["source_state_id"] = "STATE-OUTSIDE"
    witness["model_a_source_score"]["state_id"] = "STATE-OUTSIDE"
    witness["model_b_source_score"]["state_id"] = "STATE-OUTSIDE"
    path = _write_audit(tmp_path, raw)

    with pytest.raises(ValueError, match="outside the bound universe"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_verifier_recomputes_and_rejects_fabricated_favorable_result(
    tmp_path: Path,
) -> None:
    audit, cache, model_a, model_b = _build_audit(tmp_path)
    raw = audit.model_dump(mode="json")
    witness = raw["witnesses"][0]
    witness["non_unknown_detailed_delta_question_ids"] = ["FABRICATED"]
    path = _write_audit(tmp_path, raw)

    with pytest.raises(ValueError, match="deterministic recomputation"):
        verify_behavioral_difference_audit(  # type: ignore[arg-type]
            path,
            model_a=model_a,
            model_b=model_b,
            candidate_cache_path=cache.path,
            candidate_request=_REQUEST,
            engine_fingerprint=_ENGINE_FINGERPRINT,
        )


def test_public_audit_interfaces_have_no_truth_key_or_reveal_surface() -> None:
    for function in (audit_behavioral_difference, verify_behavioral_difference_audit):
        parameter_names = set(inspect.signature(function).parameters)
        assert not any(
            marker in parameter
            for parameter in parameter_names
            for marker in ("truth", "answer", "key", "reveal", "decrypt", "envelope")
        )
