from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from hdmatch.util import sha256_json
from scripts.audit_natal_time_api_trace import build_trace
from scripts.audit_natal_time_foundation import build_audit

PROJECT_ROOT = Path(__file__).parents[2]


def test_foundation_audit_is_synthetic_complete_and_self_hashing() -> None:
    audit = build_audit(PROJECT_ROOT, "synthetic-audit-commit")
    fixtures = audit["fixtures"]
    assert isinstance(fixtures, list)

    assert audit["synthetic_only"] is True
    assert [item["name"] for item in fixtures] == [
        "ordinary",
        "leap_day",
        "dst_gap",
        "dst_fold",
        "historical_offset",
    ]
    assert all(item["ranking_present"] is False for item in fixtures)
    assert all(item["weights_present"] is False for item in fixtures)
    assert all(item["probability_present"] is False for item in fixtures)
    assert all(item["relationship_evidence_included"] is False for item in fixtures)
    unhashed = deepcopy(audit)
    expected = unhashed.pop("audit_sha256")
    assert expected == sha256_json(unhashed)


def test_weekday_lock_trace_is_synthetic_ordered_and_self_hashing() -> None:
    trace = build_trace("synthetic-trace-commit")
    sequence = trace["sequence"]
    assert isinstance(sequence, list)

    assert trace["synthetic_only"] is True
    assert sequence[0]["event"] == "client_submits_date_and_independent_weekday_memory"
    assert sequence[0]["assertions"]["implied_weekday_absent_from_lock_response"] is True
    assert sequence[1]["event"] == "client_requests_assessment_after_server_lock"
    assert sequence[1]["assertions"]["implied_weekday_revealed_after_lock"] is True
    unhashed = deepcopy(trace)
    expected = unhashed.pop("trace_sha256")
    assert expected == sha256_json(unhashed)
