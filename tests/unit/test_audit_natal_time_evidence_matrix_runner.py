from __future__ import annotations

from copy import deepcopy

from hdmatch.util import sha256_json
from scripts.audit_natal_time_evidence_matrix import build_matrix


def test_evidence_matrix_is_complete_synthetic_and_self_hashing() -> None:
    matrix = build_matrix("synthetic-matrix-commit")
    cases = matrix["cases"]
    assert isinstance(cases, list)

    assert matrix["synthetic_only"] is True
    assert matrix["case_count"] == 12
    assert {item["case_id"] for item in cases} == {
        "documentary_weekday_unavailable",
        "documentary_weekday_concordant",
        "documentary_weekday_conflict",
        "memory_weekday_unavailable",
        "memory_weekday_concordant",
        "memory_weekday_conflict",
        "conflicting_documentary_sources",
        "explicit_unordered_candidate_set",
        "correction_supersession",
        "attempted_original_date_omission",
        "attempted_relationship_evidence_injection",
        "attempted_in_place_mutation",
    }
    assert all(len(item["evidence_lineage_sha256"]) == 64 for item in cases)
    assert all(isinstance(item["operative_dates"], list) for item in cases)
    rejected = [item for item in cases if not item["attempt_accepted"]]
    assert len(rejected) == 3
    assert all(item["attempted_payload_sha256"] for item in rejected)

    unhashed = deepcopy(matrix)
    expected = unhashed.pop("matrix_sha256")
    assert expected == sha256_json(unhashed)
