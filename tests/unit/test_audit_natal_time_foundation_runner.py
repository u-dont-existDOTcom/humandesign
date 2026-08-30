from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from scripts.audit_natal_time_foundation import build_audit

from hdmatch.util import sha256_json

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
