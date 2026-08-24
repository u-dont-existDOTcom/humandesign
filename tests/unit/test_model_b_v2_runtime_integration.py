from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest

from hdmatch.cli import (
    _command_audit_model_b_v2_new_difference,
    _command_compile_model_b_v2_new,
    _command_freeze_model_b_v2_new,
    _command_generate,
    _command_recover,
    _parser,
    _v2_generation_timing,
    _verify_v2_freeze_precedes_manifest,
)
from hdmatch.cli import main as hdmatch_main
from hdmatch.evaluation import (
    BehavioralDifferenceMonthRequest,
    VerifiedBehavioralDifferenceBinding,
)
from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.model.mapping_library import load_mapping_library
from hdmatch.model_b.prevalence import ConditionalPrevalenceEngine
from hdmatch.model_b_v2_new import FrozenModelBV2New, PreparedPrevalence
from hdmatch.runtime.keyless_boundary import (
    KeylessIsolationError,
    RecoveryBoundaryRequest,
    SourceProvenance,
    build_recovery_mount_plan,
)
from hdmatch.runtime.recovery import (
    RecoverySettings,
    _known_date_runtime_prevalence,
    recover_blind_file,
)
from hdmatch.runtime.symbolic_adapter import (
    MODEL_A_ID,
    MODEL_B_ID,
    MODEL_B_V2_NEW_ID,
    load_runtime_model,
)
from hdmatch.schemas import Activation, CandidateState, ChartFeatures, LocalDateOverlap
from hdmatch.search import AggregationMode
from hdmatch.util import sha256_json

ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "mappings/mapping_library_v1.json"
MODEL_B_V1 = ROOT / "mappings/model_b_mapping_library_v1.json"


def _difference_binding() -> VerifiedBehavioralDifferenceBinding:
    return VerifiedBehavioralDifferenceBinding(
        audit_file_sha256="1" * 64,
        audited_at_utc=datetime(2026, 1, 2, tzinfo=UTC),
        model_a_sha256="2" * 64,
        model_a_mapping_sha256="3" * 64,
        model_b_compiled_file_sha256="4" * 64,
        model_b_freeze_receipt_file_sha256="5" * 64,
        model_b_sha256="6" * 64,
        question_bank_sha256="7" * 64,
        candidate_cache_file_sha256="8" * 64,
        candidate_engine_fingerprint="9" * 64,
        candidate_universe_request=BehavioralDifferenceMonthRequest(
            year=2000,
            month=1,
            timezone_name="UTC",
        ),
        candidate_universe_sha256="a" * 64,
        candidate_state_count=2,
    )


def _chart(chart_type: str = "generator") -> ChartFeatures:
    return ChartFeatures(
        personality_utc=datetime(2000, 1, 1, tzinfo=UTC),
        design_utc=datetime(1999, 10, 2, tzinfo=UTC),
        type=chart_type,
        strategy="wait_to_respond",
        authority="sacral",
        profile="4/6",
        definition="split_definition",
        defined_centers=("sacral", "throat"),
        channels=(),
        activations={
            "personality:sun": Activation(
                side="personality",
                body="sun",
                longitude=0.0,
                gate=1,
                line=4,
            )
        },
    )


def _state(identifier: str, chart_type: str, hours: int) -> CandidateState:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    return CandidateState(
        state_id=identifier,
        start_utc=start,
        end_utc=start + timedelta(hours=hours),
        chart_features_hash=(identifier[-1].lower() * 64),
        chart_features=_chart(chart_type),
        local_date_overlaps=(LocalDateOverlap(date=date(2000, 1, 1), seconds=hours * 3600),),
    )


def test_model_a_and_model_b_v1_artifacts_and_responses_remain_frozen() -> None:
    model_a = load_runtime_model(MODEL_A_ID, model_a_mapping_path=MAPPING)
    model_b = load_runtime_model(
        MODEL_B_ID,
        model_a_mapping_path=MAPPING,
        model_b_artifact_path=MODEL_B_V1,
    )

    assert sha256_file(MAPPING) == (
        "3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200"
    )
    assert model_a.model_sha256 == (
        "e4b1ed725f0310b5434ca58745972b23902ee9e23a10ac795ea420ce0de8d69e"
    )
    assert sha256_file(MODEL_B_V1) == (
        "c4b806b90fef3a91d98121a303174503e5f2949ef8be8ec0c6823242f1ecf1aa"
    )
    assert model_b.model_sha256 == (
        "5c1aeb4df29c68a1a3202a8a6a2cf7974bcc1894b6b54a88c17a8deb6665181f"
    )
    assert model_a.question_bank_sha256 == model_b.question_bank_sha256
    responses_a = tuple(item.model_dump(mode="json") for item in model_a.oracle_responses(_chart()))
    responses_b = tuple(item.model_dump(mode="json") for item in model_b.oracle_responses(_chart()))
    assert responses_a == responses_b
    assert sha256_json(responses_a) == (
        "4ad4c569414fad6bb23c2f3a5aac206202bb5c380dbd30cacbe45cdff81b13b0"
    )


def test_v2_loader_requires_both_public_runtime_artifacts() -> None:
    with pytest.raises(ValueError, match="compiled and freeze"):
        load_runtime_model(MODEL_B_V2_NEW_ID, model_a_mapping_path=MAPPING)
    with pytest.raises(ValueError, match="compiled and freeze"):
        load_runtime_model(
            MODEL_B_V2_NEW_ID,
            model_a_mapping_path=MAPPING,
            model_b_v2_compiled_path="compiled.json",
        )


def test_known_date_v2_keeps_date_base_but_prepares_detail_from_full_month(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    date_states = (_state("STATE-A", "generator", 6),)
    full_month_states = (*date_states, _state("STATE-B", "projector", 18))
    captured: list[tuple[CandidateState, ...]] = []
    prepared = PreparedPrevalence(
        base_flat={"sentinel": 0.25},
        detailed_context=cast(ConditionalPrevalenceEngine, object()),
        universe_id="full-month",
        universe_sha256="a" * 64,
        total_duration_seconds=24 * 3600,
    )

    def _prepare(_model: object, states: object) -> PreparedPrevalence:
        captured.append(tuple(cast(tuple[CandidateState, ...], states)))
        return prepared

    monkeypatch.setattr("hdmatch.runtime.recovery.prepare_runtime_prevalence", _prepare)
    fake_model = SimpleNamespace(
        model_id=MODEL_B_V2_NEW_ID,
        library=load_mapping_library(MAPPING),
    )

    result = _known_date_runtime_prevalence(
        date_states,
        full_month_states,
        fake_model,
        date(2000, 1, 1),
        "UTC",
    )

    assert isinstance(result, PreparedPrevalence)
    assert captured == [full_month_states]
    assert "sentinel" not in result.base_flat
    matching_generator_anchors = {
        mapping.anchor_id
        for mapping in fake_model.library.frozen_mappings
        if mapping.chart_feature_predicate is not None
        and mapping.chart_feature_predicate.matches(date_states[0].chart_features)
        and mapping.chart_feature_predicate.feature == "type"
    }
    assert matching_generator_anchors
    assert all(result.base_flat[anchor] == 1.0 for anchor in matching_generator_anchors)
    assert result.universe_id == "full-month"


def _boundary_fixture(
    tmp_path: Path,
) -> tuple[RecoveryBoundaryRequest, SourceProvenance, Path, Path, Path, Path]:
    source_root = tmp_path / "source"
    tracked = source_root / "src/hdmatch/__init__.py"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("\n", encoding="utf-8")
    blind = tmp_path / "blind.json"
    questions = tmp_path / "questions.json"
    mapping = tmp_path / "mapping.json"
    compiled = tmp_path / "compiled.json"
    freeze = tmp_path / "freeze.json"
    difference_audit = tmp_path / "difference-audit.json"
    difference_cache = tmp_path / "month-2000-01-UTC-test.json"
    write_new_canonical_json(blind, {"schema_version": "blind-synthetic-v1", "cases": []})
    write_new_canonical_json(questions, {"schema_version": "question-bank-test-v1"})
    write_new_canonical_json(
        mapping,
        {"question_bank_sha256": sha256_file(questions)},
    )
    write_new_canonical_json(compiled, {"public_model": "compiled"})
    write_new_canonical_json(freeze, {"public_model": "freeze"})
    write_new_canonical_json(difference_audit, {"public": "difference-audit"})
    write_new_canonical_json(difference_cache, {"public": "difference-cache"})
    ephemeris = tmp_path / "ephemeris"
    ephemeris.mkdir()
    (ephemeris / "public.se1").write_bytes(b"public")
    output = tmp_path / "output"
    output.mkdir()
    request = RecoveryBoundaryRequest(
        blind_file=blind,
        output_dir=output,
        ephemeris_path=ephemeris,
        mapping_file=mapping,
        question_bank_file=questions,
        python_environment=Path("/usr"),
        model_id=MODEL_B_V2_NEW_ID,
        model_b_v2_compiled=compiled,
        model_b_v2_freeze=freeze,
        model_b_v2_difference_audit=difference_audit,
        model_b_v2_difference_cache=difference_cache,
        candidate_cache=tmp_path,
    )
    provenance = SourceProvenance(
        repository_root=source_root,
        commit="a" * 40,
        tree="b" * 40,
        tracked_decoder_files=(tracked,),
    )
    return request, provenance, compiled, freeze, difference_audit, difference_cache


def test_keyless_v2_mounts_compiled_and_freeze_read_only_without_secret_surface(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, provenance, compiled, freeze, difference_audit, difference_cache = (
        _boundary_fixture(tmp_path)
    )
    monkeypatch.setattr(
        "hdmatch.runtime.keyless_boundary._verify_v2_difference_request",
        lambda *_args, **_kwargs: _difference_binding(),
    )
    plan = build_recovery_mount_plan(request, provenance=provenance, bwrap="/usr/bin/bwrap")

    assert plan.command[plan.command.index(str(compiled.resolve())) - 1] == "--ro-bind"
    assert plan.command[plan.command.index(str(freeze.resolve())) - 1] == "--ro-bind"
    assert plan.command[plan.command.index(str(difference_audit.resolve())) - 1] == "--ro-bind"
    assert plan.command[plan.command.index(str(difference_cache.resolve())) - 1] == "--ro-bind"
    assert "--model-b-v2-compiled" in plan.command
    assert "--model-b-v2-freeze" in plan.command
    assert "--model-b-v2-difference-audit" in plan.command
    assert "--model-b-v2-difference-cache" in plan.command
    difference_cache_argument = plan.command[
        plan.command.index("--model-b-v2-difference-cache") + 1
    ]
    assert difference_cache_argument == str(
        Path("/public/candidate_cache") / difference_cache.name
    )
    assert plan.command.count(str(difference_cache.resolve())) == 1
    child = plan.command[plan.command.index("hdmatch.cli") :]
    assert not any(
        marker in argument.casefold()
        for argument in child
        for marker in ("key-file", "decrypt", "reveal", "envelope", "truth")
    )

    with pytest.raises(KeylessIsolationError, match="compiled, freeze, difference-audit"):
        build_recovery_mount_plan(
            replace(request, model_b_v2_freeze=None),
            provenance=provenance,
            bwrap="/usr/bin/bwrap",
        )


def test_v2_recovery_preflights_public_artifacts_before_model_or_cache(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    compiled = tmp_path / "innocent-model.data"
    freeze = tmp_path / "freeze.json"
    difference_audit = tmp_path / "difference-audit.json"
    difference_cache = tmp_path / "difference-cache.json"
    write_new_canonical_json(
        compiled,
        {
            "schema_version": "answer-key-v1",
            "experiment_id": "EXP",
            "blind_input_sha256": "a" * 64,
            "cases": [{"case_id": "C1", "true_utc": "2000-01-01T00:00:00Z"}],
        },
    )
    write_new_canonical_json(freeze, {"public_model": "freeze"})
    write_new_canonical_json(difference_audit, {"public": "difference-audit"})
    write_new_canonical_json(difference_cache, {"public": "difference-cache"})

    with pytest.raises(SystemExit) as raised:
        hdmatch_main(
            (
                "recover",
                "--model",
                MODEL_B_V2_NEW_ID,
                "--model-b-v2-compiled",
                str(compiled),
                "--model-b-v2-freeze",
                str(freeze),
                "--model-b-v2-difference-audit",
                str(difference_audit),
                "--model-b-v2-difference-cache",
                str(difference_cache),
                "--run-dir",
                str(run_dir),
                "--blind-file",
                str(tmp_path / "missing-blind.json"),
                "--ephemeris",
                str(tmp_path / "missing-ephemeris"),
            )
        )
    assert raised.value.code == 2
    stderr = capsys.readouterr().err
    assert "plaintext answer key file" in stderr
    assert str(compiled) not in stderr


def test_direct_v2_recovery_rejects_missing_gate_before_chart_or_cache(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blind = tmp_path / "blind.json"
    write_new_canonical_json(
        blind,
        {
            "schema_version": "blind-synthetic-v1",
            "experiment_id": "V2-DIRECT-GATE",
            "model_id": MODEL_B_V2_NEW_ID,
            "model_sha256": "1" * 64,
            "question_bank_sha256": "2" * 64,
            "mapping_sha256": "3" * 64,
            "candidate_universe": "known_month",
            "model_capabilities": {},
            "noise_tier": "oracle",
            "cases": [
                {
                    "schema_version": "blind-case-v1",
                    "case_id": "CASE-0001",
                    "known_birth_year": 2000,
                    "known_birth_month": 1,
                    "birthplace": "Synthetic UTC",
                    "iana_timezone": "UTC",
                    "responses": [],
                    "candidate_universe": "known_month",
                }
            ],
        },
    )
    model = SimpleNamespace(
        model_id=MODEL_B_V2_NEW_ID,
        model_sha256="1" * 64,
        question_bank_sha256="2" * 64,
        mapping_sha256="3" * 64,
        capability_metadata={},
    )
    chart_touched = False

    def _chart(*_args: object, **_kwargs: object) -> object:
        nonlocal chart_touched
        chart_touched = True
        raise AssertionError("chart/cache work must not start before V2 gate verification")

    monkeypatch.setattr("hdmatch.runtime.recovery.ExactChartAdapter", _chart)

    with pytest.raises(ValueError, match="requires a verified behavioral-difference gate"):
        recover_blind_file(
            blind,
            decoder_root=tmp_path,
            model=model,  # type: ignore[arg-type]
            ephemeris_path=tmp_path / "ephemeris",
            cache_dir=tmp_path / "cache",
            settings=RecoverySettings(
                aggregation=AggregationMode.DURATION_WEIGHTED_EVIDENCE,
                threshold_rubric_bits=0.0,
            ),
        )
    assert chart_touched is False

    raw = load_json_bytes(blind, require_canonical=True)
    assert isinstance(raw, dict)
    binding = _difference_binding()
    raw["model_b_v2_difference_gate"] = binding.model_dump(mode="json")
    blind.unlink()
    write_new_canonical_json(blind, raw)
    with pytest.raises(ValueError, match="model SHA is mismatched"):
        recover_blind_file(
            blind,
            decoder_root=tmp_path,
            model=model,  # type: ignore[arg-type]
            ephemeris_path=tmp_path / "ephemeris",
            cache_dir=tmp_path / "cache",
            settings=RecoverySettings(
                aggregation=AggregationMode.DURATION_WEIGHTED_EVIDENCE,
                threshold_rubric_bits=0.0,
            ),
            model_b_v2_difference_gate=binding,
        )
    assert chart_touched is False


def test_v2_model_freeze_must_not_postdate_run_manifest() -> None:
    frozen_model = object.__new__(FrozenModelBV2New)
    frozen_model.freeze_receipt = SimpleNamespace(
        frozen_at_utc=datetime(2026, 1, 2, tzinfo=UTC)
    )
    earlier_manifest = SimpleNamespace(created_at_utc=datetime(2026, 1, 1, tzinfo=UTC))
    later_manifest = SimpleNamespace(created_at_utc=datetime(2026, 1, 3, tzinfo=UTC))

    with pytest.raises(ValueError, match="must predate"):
        _verify_v2_freeze_precedes_manifest(frozen_model, earlier_manifest)
    _verify_v2_freeze_precedes_manifest(frozen_model, later_manifest)


def test_v2_recovery_manifest_binds_exact_compiled_and_freeze_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    blind = tmp_path / "blind.json"
    compiled = tmp_path / "compiled.json"
    freeze = tmp_path / "freeze.json"
    difference_audit = tmp_path / "difference-audit.json"
    difference_cache = tmp_path / "difference-cache.json"
    ephemeris = tmp_path / "public.se1"
    binding = _difference_binding()
    write_new_canonical_json(
        blind,
        {
            "schema_version": "blind-synthetic-v1",
            "experiment_id": "V2-MANIFEST",
            "candidate_universe": "known_month",
            "model_b_v2_difference_gate": binding.model_dump(mode="json"),
            "cases": [],
        },
    )
    write_new_canonical_json(compiled, {"public": "compiled"})
    write_new_canonical_json(freeze, {"public": "freeze"})
    write_new_canonical_json(difference_audit, {"public": "difference-audit"})
    write_new_canonical_json(difference_cache, {"public": "difference-cache"})
    ephemeris.write_bytes(b"public-ephemeris")
    fake_model = object.__new__(FrozenModelBV2New)
    fake_model.freeze_receipt = SimpleNamespace(
        frozen_at_utc=datetime(2026, 1, 1, tzinfo=UTC)
    )
    monkeypatch.setattr("hdmatch.cli._load_selected_model", lambda _args: fake_model)
    monkeypatch.setattr(
        "hdmatch.cli._verify_v2_difference_gate",
        lambda *_args, **_kwargs: binding,
    )
    monkeypatch.setattr(
        "hdmatch.cli._require_recovery_cache_matches_gate",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        "hdmatch.cli.recover_blind_file",
        lambda *_args, **_kwargs: {"schema_version": "predictions-v1"},
    )
    args = argparse.Namespace(
        run_dir=str(run_dir),
        blind_file=str(blind),
        mapping=str(MAPPING),
        ephemeris=str(ephemeris),
        cache_dir=None,
        model=MODEL_B_V2_NEW_ID,
        model_b_artifact=str(MODEL_B_V1),
        model_b_v2_compiled=str(compiled),
        model_b_v2_freeze=str(freeze),
        model_b_v2_difference_audit=str(difference_audit),
        model_b_v2_difference_cache=str(difference_cache),
        aggregation="duration_weighted_evidence",
        threshold=0.0,
        workers=1,
    )

    assert _command_recover(args) == 0
    manifest = load_json_bytes(run_dir / "run.manifest.json", require_canonical=True)
    assert isinstance(manifest, dict)
    hashes = manifest["input_hashes"]
    assert isinstance(hashes, dict)
    assert hashes["model_b_v2_compiled_artifact"] == sha256_file(compiled)
    assert hashes["model_b_v2_freeze_receipt"] == sha256_file(freeze)
    assert hashes["model_b_v2_difference_audit"] == binding.audit_file_sha256
    assert hashes["model_b_v2_difference_cache"] == binding.candidate_cache_file_sha256
    assert hashes["model_b_v2_model_semantic"] == binding.model_b_sha256
    assert hashes["model_b_v2_question_bank"] == binding.question_bank_sha256
    assert hashes["model_b_v2_difference_candidate_universe"] == (
        binding.candidate_universe_sha256
    )


def test_behavioral_difference_cli_has_no_secret_surface_and_preserves_failed_audit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parser = _parser()
    command_action = next(
        action for action in parser._actions if action.dest == "command"  # type: ignore[attr-defined]
    )
    command_parser = command_action.choices[  # type: ignore[attr-defined]
        "audit-model-b-v2-new-difference"
    ]
    destinations = {action.dest for action in command_parser._actions}  # type: ignore[attr-defined]
    assert not any(
        marker in destination
        for destination in destinations
        for marker in ("key", "truth", "reveal", "decrypt", "envelope")
    )

    order: list[str] = []
    failed_audit = SimpleNamespace(status="failed", witnesses=(), failure_reasons=("no split",))
    monkeypatch.setattr(
        "hdmatch.cli.assert_no_plaintext_answer_keys_in_paths", lambda _paths: None
    )
    monkeypatch.setattr(
        "hdmatch.cli.ExactChartAdapter", lambda _path: SimpleNamespace(fingerprint="engine")
    )
    monkeypatch.setattr("hdmatch.cli.cache_path", lambda *_args: tmp_path / "cache.json")
    monkeypatch.setattr(
        "hdmatch.cli.load_cached_universe",
        lambda *_args, **_kwargs: SimpleNamespace(states=(_state("STATE-A", "generator", 1),)),
    )
    fake_a_type = type("FakeModelA", (), {})
    fake_b_type = type("FakeModelB", (), {})
    monkeypatch.setattr("hdmatch.cli.FrozenSymbolicModel", fake_a_type)
    monkeypatch.setattr("hdmatch.cli.FrozenModelBV2New", fake_b_type)
    models = iter((fake_a_type(), fake_b_type()))
    monkeypatch.setattr("hdmatch.cli.load_runtime_model", lambda *_args, **_kwargs: next(models))
    monkeypatch.setattr(
        "hdmatch.cli.audit_behavioral_difference",
        lambda *_args, **_kwargs: failed_audit,
    )
    monkeypatch.setattr(
        "hdmatch.cli.write_new_canonical_json",
        lambda *_args: order.append("write"),
    )

    def _reject(_audit: object) -> None:
        order.append("reject")
        raise ValueError("difference gate failed")

    monkeypatch.setattr("hdmatch.cli.require_behavioral_difference", _reject)
    args = argparse.Namespace(
        cache_dir=str(tmp_path),
        ephemeris=str(tmp_path / "ephemeris"),
        mapping=str(MAPPING),
        model_b_v2_compiled=str(tmp_path / "compiled"),
        model_b_v2_freeze=str(tmp_path / "freeze"),
        year=2000,
        month=1,
        timezone="UTC",
        output=str(tmp_path / "audit.json"),
    )

    with pytest.raises(ValueError, match="difference gate failed"):
        _command_audit_model_b_v2_new_difference(args)
    assert order == ["write", "reject"]


def test_v2_freeze_must_precede_synthetic_generator_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Config:
        seed = None
        ephemeris_path = "public-ephemeris"
        year_start = 2000
        year_end = 2000
        month = 1
        timezone = "UTC"

        def model_copy(self, *, update: object) -> _Config:
            del update
            return self

    model = object.__new__(FrozenModelBV2New)
    model.freeze_receipt = SimpleNamespace(
        frozen_at_utc=datetime(2100, 1, 1, tzinfo=UTC)
    )
    generator_called = False

    def _generator(*_args: object) -> object:
        nonlocal generator_called
        generator_called = True
        raise AssertionError("generator must not run before the model freeze ordering check")

    monkeypatch.setattr("hdmatch.cli.load_synthetic_config", lambda _path: _Config())
    monkeypatch.setattr("hdmatch.cli._read_secret_seed", lambda _path: 1)
    monkeypatch.setattr("hdmatch.cli.ExactChartAdapter", lambda _path: object())
    monkeypatch.setattr("hdmatch.cli._load_selected_model", lambda _args: model)
    monkeypatch.setattr(
        "hdmatch.cli._verify_v2_difference_gate",
        lambda *_args, **_kwargs: _difference_binding(),
    )
    monkeypatch.setattr("hdmatch.cli.SyntheticGenerator", _generator)
    args = argparse.Namespace(
        config=str(tmp_path / "config.json"),
        run_dir=str(tmp_path / "run"),
        ephemeris="public-ephemeris",
        seed_file=None,
        key_file=None,
        model=MODEL_B_V2_NEW_ID,
        mapping=str(MAPPING),
        model_b_artifact=str(MODEL_B_V1),
        model_b_v2_compiled="compiled.json",
        model_b_v2_freeze="freeze.json",
        model_b_v2_difference_audit="difference-audit.json",
        model_b_v2_difference_cache="difference-cache.json",
    )

    with pytest.raises(ValueError, match="must predate synthetic generation"):
        _command_generate(args)
    assert generator_called is False

    model.freeze_receipt = SimpleNamespace(
        frozen_at_utc=datetime(2025, 12, 31, tzinfo=UTC)
    )
    started = datetime(2026, 1, 1, tzinfo=UTC)
    assert _v2_generation_timing(model, started) == {
        "generation_started_at_utc": started,
        "model_freeze_created_at_utc": model.freeze_receipt.frozen_at_utc,
    }


def test_v2_compile_and_freeze_cli_surfaces_report_output_hashes(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    compile_args = _parser().parse_args(
        (
            "compile-model-b-v2-new",
            "--preregistration",
            "prereg.json",
            "--output",
            "compiled.json",
        )
    )
    freeze_args = _parser().parse_args(
        (
            "freeze-model-b-v2-new",
            "--preregistration",
            "prereg.json",
            "--compiled",
            "compiled.json",
            "--output",
            "freeze.json",
            "--source-software-commit",
            "a" * 40,
            "--source-software-tree",
            "b" * 40,
        )
    )
    assert compile_args.handler is _command_compile_model_b_v2_new
    assert freeze_args.handler is _command_freeze_model_b_v2_new
    captured_compile: dict[str, object] = {}
    captured_freeze: dict[str, object] = {}
    monkeypatch.setattr(
        "hdmatch.cli.compile_model_b_v2_new",
        lambda **kwargs: (
            captured_compile.update(kwargs)
            or SimpleNamespace(sha256=lambda: "c" * 64)
        ),
    )
    monkeypatch.setattr(
        "hdmatch.cli.freeze_model_b_v2_new",
        lambda **kwargs: (
            captured_freeze.update(kwargs)
            or SimpleNamespace(frozen_at_utc=datetime(2026, 1, 1, tzinfo=UTC))
        ),
    )
    monkeypatch.setattr("hdmatch.cli.sha256_file", lambda _path: "f" * 64)

    assert _command_compile_model_b_v2_new(compile_args) == 0
    assert _command_freeze_model_b_v2_new(freeze_args) == 0
    output = capsys.readouterr().out
    assert "compiled semantic sha256" in output
    assert "compiled file sha256" in output
    assert "freeze receipt sha256" in output
    assert captured_compile["preregistration_path"] == "prereg.json"
    assert captured_freeze["source_software_commit"] == "a" * 40
    assert captured_freeze["source_software_tree"] == "b" * 40
