from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from hdmatch import cli as cli_module
from hdmatch.century_cache import workflow as workflow_module
from hdmatch.century_cache.workflow import (
    CenturyCacheWorkflowError,
    build_all_missing_century_jobs,
)
from hdmatch.cli import (
    _command_assemble_century_cache,
    _command_build_century_cache,
    _command_build_century_cache_job,
    _command_finalize_century_cache_publication,
    _command_prepare_century_cache,
    _command_verify_century_cache,
    _parse_utc_timestamp,
    _parser,
)


def _command_parser(name: str) -> argparse.ArgumentParser:
    parser = _parser()
    command_action = next(
        action for action in parser._actions if action.dest == "command"  # type: ignore[attr-defined]
    )
    return command_action.choices[name]  # type: ignore[no-any-return,attr-defined]


def test_century_cache_cli_exposes_only_explicit_phase2_commands() -> None:
    handlers = {
        "prepare-century-cache": _command_prepare_century_cache,
        "build-century-cache-job": _command_build_century_cache_job,
        "assemble-century-cache": _command_assemble_century_cache,
        "build-century-cache": _command_build_century_cache,
        "finalize-century-cache-publication": (
            _command_finalize_century_cache_publication
        ),
        "verify-century-cache": _command_verify_century_cache,
    }
    for name, expected_handler in handlers.items():
        command = _command_parser(name)
        assert command.get_default("handler") is expected_handler

    build_destinations = {
        action.dest for action in _command_parser("build-century-cache")._actions  # type: ignore[attr-defined]
    }
    assert "plan" in build_destinations
    assert "plan_trust_lock" in build_destinations
    assert "start" not in build_destinations
    assert "end_exclusive" not in build_destinations
    assert "target" not in build_destinations

    finalization_destinations = {
        action.dest
        for action in _command_parser(
            "finalize-century-cache-publication"
        )._actions  # type: ignore[attr-defined]
    }
    assert "staging_dir" not in finalization_destinations
    assert {
        "plan",
        "plan_trust_lock",
        "output",
        "trust_lock",
        "build_evidence_dir",
    } <= finalization_destinations


def test_century_timestamp_parser_requires_an_explicit_offset() -> None:
    assert _parse_utc_timestamp("2000-01-01T01:00:00+01:00") == datetime(
        2000,
        1,
        1,
        tzinfo=UTC,
    )
    with pytest.raises(argparse.ArgumentTypeError, match="UTC offset"):
        _parse_utc_timestamp("2000-01-01T00:00:00")


def test_all_jobs_reuses_one_verified_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    jobs = (SimpleNamespace(job_id="utc-year-2000"), SimpleNamespace(job_id="utc-year-2001"))
    plan = SimpleNamespace(
        jobs=jobs,
        source_commit="a" * 40,
        engine=SimpleNamespace(ephemeris_provenance="verified-files"),
    )
    provider = object()
    calls: list[tuple[object, object]] = []
    provider_calls = 0

    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda *_args, **_kwargs: SimpleNamespace(plan=plan),
    )
    monkeypatch.setattr(
        workflow_module,
        "_require_current_source_matches_plan",
        lambda actual: calls.append(("source", actual)),
    )

    def _provider(**_kwargs: object) -> tuple[object, str]:
        nonlocal provider_calls
        provider_calls += 1
        return provider, "verified-files"

    monkeypatch.setattr(workflow_module, "_provider_and_provenance", _provider)
    monkeypatch.setattr(
        workflow_module,
        "_build_or_retain_staged_job",
        lambda **kwargs: calls.append((kwargs["job"], kwargs["provider"]))
        or kwargs["job"],
    )

    receipts = build_all_missing_century_jobs(
        plan_path="plan.json",
        plan_trust_lock_path="plan-lock.json",
        expected_plan_trust_lock_sha256="f" * 64,
        staging_directory="staged",
        ephemeris_directory="ephemeris",
        ephemeris_source_manifest_path="manifest.json",
    )

    assert receipts == jobs
    assert provider_calls == 1
    assert calls == [("source", plan), (jobs[0], provider), (jobs[1], provider)]


def test_resumed_job_rejects_source_mismatch_before_ephemeris_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = SimpleNamespace(source_commit="a" * 40)
    provider_reached = False
    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda *_args, **_kwargs: SimpleNamespace(plan=plan),
    )

    def _reject_source(_plan: object) -> None:
        raise CenturyCacheWorkflowError("source differs")

    def _provider(**_kwargs: object) -> tuple[object, object]:
        nonlocal provider_reached
        provider_reached = True
        return object(), object()

    monkeypatch.setattr(
        workflow_module,
        "_require_current_source_matches_plan",
        _reject_source,
    )
    monkeypatch.setattr(workflow_module, "_provider_and_provenance", _provider)

    with pytest.raises(CenturyCacheWorkflowError, match="source differs"):
        workflow_module.build_century_staged_job(
            plan_path="plan.json",
            plan_trust_lock_path="plan-lock.json",
            expected_plan_trust_lock_sha256="f" * 64,
            job_id="utc-year-2000",
            staging_directory="staged",
            ephemeris_directory="ephemeris",
            ephemeris_source_manifest_path="manifest.json",
        )
    assert provider_reached is False


@pytest.mark.parametrize(
    ("cache_present", "lock_present", "state"),
    [
        (False, False, "new"),
        (True, False, "published_missing_lock"),
        (False, True, "orphan_lock"),
        (True, True, "published_with_lock"),
    ],
)
def test_assembly_preflight_classifies_all_publication_path_states(
    tmp_path: Path,
    cache_present: bool,
    lock_present: bool,
    state: str,
) -> None:
    cache = tmp_path / "cache"
    lock = tmp_path / "trust-lock.json"
    if cache_present:
        cache.mkdir()
    if lock_present:
        lock.write_text("occupied", encoding="utf-8")

    assert (
        workflow_module.preflight_century_cache_publication_paths(
            cache_directory=cache,
            trust_lock_path=lock,
        )
        == state
    )


def test_build_command_preflights_before_staged_job_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    replay_reached = False

    def _replay(**_kwargs: object) -> tuple[object, ...]:
        nonlocal replay_reached
        replay_reached = True
        return ()

    monkeypatch.setattr(
        workflow_module,
        "build_all_missing_century_jobs",
        _replay,
    )
    # The command imported this name directly, so patch its defining module.
    monkeypatch.setattr(
        "hdmatch.cli.build_all_missing_century_jobs",
        _replay,
    )
    cache = tmp_path / "stranded-cache"
    cache.mkdir()
    published = object()
    monkeypatch.setattr(
        cli_module,
        "_assemble_century_cache_from_args",
        lambda _args: published,
    )
    monkeypatch.setattr(
        cli_module,
        "_published_cache_summary",
        lambda result: {"status": "pass"} if result is published else {},
    )
    args = argparse.Namespace(
        output=str(cache),
        trust_lock=str(tmp_path / "missing-lock.json"),
    )
    assert _command_build_century_cache(args) == 0
    assert replay_reached is False


def test_assembly_routes_both_published_states_to_finalization_before_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache = tmp_path / "cache"
    cache.mkdir()
    lock = tmp_path / "trust-lock.json"
    expected = object()
    finalization_calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        workflow_module,
        "finalize_century_cache_publication",
        lambda **kwargs: finalization_calls.append(kwargs) or expected,
    )
    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda _path: pytest.fail("published-state routing reached replay setup"),
    )
    kwargs = {
        "plan_path": tmp_path / "plan.json",
        "plan_trust_lock_path": tmp_path / "plan-lock.json",
        "expected_plan_trust_lock_sha256": "f" * 64,
        "staging_directory": tmp_path / "staged",
        "cache_directory": cache,
        "cache_locator": "data/century_cache/v1",
        "trust_lock_path": lock,
        "build_evidence_directory": tmp_path / "evidence",
        "ephemeris_directory": tmp_path / "ephemeris",
        "ephemeris_source_manifest_path": tmp_path / "source.json",
        "engine_validation_path": tmp_path / "engine.json",
        "parity_report_path": tmp_path / "parity.json",
        "parity_reference_source_path": tmp_path / "reference.json",
    }

    assert (
        workflow_module.assemble_and_publish_century_cache(**kwargs) is expected  # type: ignore[arg-type]
    )
    lock.write_text("occupied", encoding="utf-8")
    assert (
        workflow_module.assemble_and_publish_century_cache(**kwargs) is expected  # type: ignore[arg-type]
    )
    assert len(finalization_calls) == 2


def test_assembly_rejects_orphan_lock_before_plan_or_replay_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lock = tmp_path / "orphan-trust-lock.json"
    lock.write_text("occupied", encoding="utf-8")
    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda _path: pytest.fail("orphan-lock preflight reached plan/replay setup"),
    )

    with pytest.raises(CenturyCacheWorkflowError, match="without its cache destination"):
        workflow_module.assemble_and_publish_century_cache(
            plan_path=tmp_path / "plan.json",
            plan_trust_lock_path=tmp_path / "plan-lock.json",
            expected_plan_trust_lock_sha256="f" * 64,
            staging_directory=tmp_path / "staged",
            cache_directory=tmp_path / "missing-cache",
            cache_locator="data/century_cache/v1",
            trust_lock_path=lock,
            build_evidence_directory=tmp_path / "evidence",
            ephemeris_directory=tmp_path / "ephemeris",
            ephemeris_source_manifest_path=tmp_path / "source.json",
            engine_validation_path=tmp_path / "engine.json",
            parity_report_path=tmp_path / "parity.json",
            parity_reference_source_path=tmp_path / "reference.json",
        )


def test_new_assembly_keeps_generation_source_commit_guard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = SimpleNamespace(source_commit="9eafe5344740cdf24c4796dbcbad8fb4514045ec")
    provider_reached = False
    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda *_args, **_kwargs: SimpleNamespace(plan=plan),
    )

    def _reject_generation_source(_plan: object) -> None:
        raise CenturyCacheWorkflowError("current clean source differs")

    def _provider(**_kwargs: object) -> tuple[object, object]:
        nonlocal provider_reached
        provider_reached = True
        return object(), object()

    monkeypatch.setattr(
        workflow_module,
        "_require_current_source_matches_plan",
        _reject_generation_source,
    )
    monkeypatch.setattr(workflow_module, "_provider_and_provenance", _provider)

    with pytest.raises(CenturyCacheWorkflowError, match="current clean source differs"):
        workflow_module.assemble_and_publish_century_cache(
            plan_path=tmp_path / "plan.json",
            plan_trust_lock_path=tmp_path / "plan-lock.json",
            expected_plan_trust_lock_sha256="f" * 64,
            staging_directory=tmp_path / "staged",
            cache_directory=tmp_path / "new-cache",
            cache_locator="data/century_cache/v1",
            trust_lock_path=tmp_path / "new-lock.json",
            build_evidence_directory=tmp_path / "evidence",
            ephemeris_directory=tmp_path / "ephemeris",
            ephemeris_source_manifest_path=tmp_path / "source.json",
            engine_validation_path=tmp_path / "engine.json",
            parity_report_path=tmp_path / "parity.json",
            parity_reference_source_path=tmp_path / "reference.json",
        )
    assert provider_reached is False


def test_assembly_separates_replay_and_reconciliation_audits(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _ExpectedStop(RuntimeError):
        pass

    replay_provider = object()
    reconciliation_provider = object()
    provenance = object()
    job = object()
    plan = SimpleNamespace(
        jobs=(job,),
        engine=SimpleNamespace(ephemeris_provenance=provenance),
        design_root_time_tolerance_seconds=0.01,
    )
    providers = iter((replay_provider, reconciliation_provider))
    publisher_aborted = False
    verified_with: object | None = None

    class _Publisher:
        def abort(self) -> None:
            nonlocal publisher_aborted
            publisher_aborted = True

    class _Reconciliation:
        def __init__(self, provider: object, **_kwargs: object) -> None:
            assert provider is reconciliation_provider

        def __enter__(self) -> _Reconciliation:
            return self

        def __exit__(self, *_args: object) -> None:
            pass

        def append(self, _source: object) -> None:
            raise _ExpectedStop("stop after provider-routing assertion")

    def _verify(
        _plan: object,
        _job: object,
        provider: object,
        _staging: object,
    ) -> object:
        nonlocal verified_with
        verified_with = provider
        return object()

    monkeypatch.setattr(
        workflow_module,
        "verify_century_build_plan_against_trust_lock",
        lambda *_args, **_kwargs: SimpleNamespace(plan=plan),
    )
    monkeypatch.setattr(
        workflow_module,
        "_require_current_source_matches_plan",
        lambda _plan: None,
    )
    monkeypatch.setattr(
        workflow_module,
        "_provider_and_provenance",
        lambda **_kwargs: (next(providers), provenance),
    )
    monkeypatch.setattr(
        workflow_module,
        "load_cache_engine_provenance",
        lambda *_args: object(),
    )
    monkeypatch.setattr(
        workflow_module,
        "century_cache_stream_identity_from_plan",
        lambda *_args, **_kwargs: object(),
    )
    monkeypatch.setattr(
        workflow_module,
        "StreamingCenturyCachePublisher",
        lambda *_args, **_kwargs: _Publisher(),
    )
    monkeypatch.setattr(
        workflow_module,
        "ExactStateReconciliationStream",
        _Reconciliation,
    )
    monkeypatch.setattr(workflow_module, "verify_staged_exact_state_batch", _verify)
    monkeypatch.setattr(
        workflow_module,
        "OverlappingVerifiedExactStateBatch",
        SimpleNamespace(from_verified_staged_batch=lambda _batch: object()),
    )

    with pytest.raises(_ExpectedStop, match="provider-routing"):
        workflow_module.assemble_and_publish_century_cache(
            plan_path=tmp_path / "plan.json",
            plan_trust_lock_path=tmp_path / "plan-lock.json",
            expected_plan_trust_lock_sha256="f" * 64,
            staging_directory=tmp_path / "staged",
            cache_directory=tmp_path / "cache",
            cache_locator="data/century_cache/test",
            trust_lock_path=tmp_path / "trust-lock.json",
            build_evidence_directory=tmp_path / "evidence",
            ephemeris_directory=tmp_path / "ephemeris",
            ephemeris_source_manifest_path=tmp_path / "manifest.json",
            engine_validation_path=tmp_path / "engine.json",
            parity_report_path=tmp_path / "parity.json",
            parity_reference_source_path=tmp_path / "golden.json",
        )

    assert verified_with is replay_provider
    assert publisher_aborted is True


def test_partial_staged_job_is_never_treated_as_resumable(tmp_path: Path) -> None:
    job = SimpleNamespace(job_id="utc-year-2000")
    plan = SimpleNamespace()
    (tmp_path / "staged-utc-year-2000.parquet.zst").write_bytes(b"partial")

    with pytest.raises(CenturyCacheWorkflowError, match="partial"):
        workflow_module._retained_staged_receipt(plan, job, tmp_path)  # type: ignore[arg-type]
