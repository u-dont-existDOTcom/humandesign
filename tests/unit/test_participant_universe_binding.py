"""Tests for the immutable participant candidate-universe binding."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from hdmatch.participant.backend import _candidate_universe_sha256
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
