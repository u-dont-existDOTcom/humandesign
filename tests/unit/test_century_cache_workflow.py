from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from hdmatch.century_cache import workflow as workflow_module
from hdmatch.century_cache.workflow import (
    CenturyCacheWorkflowError,
    build_all_missing_century_jobs,
)
from hdmatch.cli import (
    _command_assemble_century_cache,
    _command_build_century_cache,
    _command_build_century_cache_job,
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
        "verify-century-cache": _command_verify_century_cache,
    }
    for name, expected_handler in handlers.items():
        command = _command_parser(name)
        assert command.get_default("handler") is expected_handler

    build_destinations = {
        action.dest for action in _command_parser("build-century-cache")._actions  # type: ignore[attr-defined]
    }
    assert "plan" in build_destinations
    assert "start" not in build_destinations
    assert "end_exclusive" not in build_destinations
    assert "target" not in build_destinations


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

    monkeypatch.setattr(workflow_module, "load_century_build_plan", lambda _path: plan)
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
    monkeypatch.setattr(workflow_module, "load_century_build_plan", lambda _path: plan)

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
            job_id="utc-year-2000",
            staging_directory="staged",
            ephemeris_directory="ephemeris",
            ephemeris_source_manifest_path="manifest.json",
        )
    assert provider_reached is False


def test_partial_staged_job_is_never_treated_as_resumable(tmp_path: Path) -> None:
    job = SimpleNamespace(job_id="utc-year-2000")
    plan = SimpleNamespace()
    (tmp_path / "staged-utc-year-2000.parquet.zst").write_bytes(b"partial")

    with pytest.raises(CenturyCacheWorkflowError, match="partial"):
        workflow_module._retained_staged_receipt(plan, job, tmp_path)  # type: ignore[arg-type]
