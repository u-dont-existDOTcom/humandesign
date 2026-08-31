"""Tests for the immutable participant candidate-universe binding."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from hdmatch.participant.backend import (
    AstroHDParticipantBackend,
    FrozenRuntimeMismatchError,
    _candidate_universe_sha256,
)
from hdmatch.participant.models import RankScope


@dataclass(frozen=True)
class _State:
    state_id: str
    start_utc: datetime
    end_utc: datetime
    chart_features_hash: str


def _states() -> tuple[_State, ...]:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    middle = start + timedelta(hours=12)
    end = start + timedelta(days=1)
    return (
        _State("STATE-A", start, middle, "a" * 64),
        _State("STATE-B", middle, end, "b" * 64),
    )


def _digest(states: tuple[_State, ...], timezone_name: str = "UTC") -> str:
    return _candidate_universe_sha256(  # type: ignore[arg-type]
        states,
        ranking_scope=RankScope.KNOWN_BIRTH_MONTH,
        engine_fingerprint="c" * 64,
        timezone_name=timezone_name,
    )


def test_candidate_universe_digest_is_deterministic() -> None:
    states = _states()
    assert _digest(states) == _digest(states)
    assert len(_digest(states)) == 64


def test_candidate_universe_digest_changes_when_partition_changes() -> None:
    first, second = _states()
    changed = (
        first,
        _State(
            second.state_id,
            second.start_utc,
            second.end_utc + timedelta(seconds=1),
            second.chart_features_hash,
        ),
    )
    assert _digest(changed) != _digest(_states())


def test_candidate_universe_digest_binds_order_and_timezone() -> None:
    states = _states()
    assert _digest(tuple(reversed(states))) != _digest(states)
    assert _digest(states, "Africa/Dakar") != _digest(states, "UTC")


@pytest.mark.parametrize(
    ("frozen_field", "replacement", "message"),
    [
        ("code_commit", "other-commit", "source commit"),
        ("engine_fingerprint", "other-engine", "chart engine"),
        ("model_version", "other-model", "model version"),
        ("model_sha256", "1" * 64, "model bytes"),
        ("mapping_sha256", "2" * 64, "mapping bytes"),
        ("question_bank_version", "other-bank", "question bank version"),
        ("question_bank_sha256", "3" * 64, "question bank bytes"),
    ],
)
def test_runtime_bundle_drift_fails_closed(
    frozen_field: str,
    replacement: str,
    message: str,
) -> None:
    backend = object.__new__(AstroHDParticipantBackend)
    backend.code_commit = "a" * 40
    backend.chart_engine = SimpleNamespace(fingerprint="engine")  # type: ignore[assignment]
    backend.model = SimpleNamespace(  # type: ignore[assignment]
        library=SimpleNamespace(model_version="model-v1"),
        model_sha256="4" * 64,
        mapping_sha256="5" * 64,
        question_bank_sha256="6" * 64,
    )
    backend.question_bank = SimpleNamespace(version="bank-v1")  # type: ignore[assignment]
    fields = {
        "code_commit": backend.code_commit,
        "engine_fingerprint": backend.chart_engine.fingerprint,
        "model_version": backend.model.library.model_version,
        "model_sha256": backend.model.model_sha256,
        "mapping_sha256": backend.model.mapping_sha256,
        "question_bank_version": backend.question_bank.version,
        "question_bank_sha256": backend.model.question_bank_sha256,
    }
    fields[frozen_field] = replacement

    with pytest.raises(FrozenRuntimeMismatchError, match=message):
        backend.assert_freeze_compatible(SimpleNamespace(**fields))  # type: ignore[arg-type]
