from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.development_human_attestation_v2 import (
    DevelopmentHumanAuditorAttestationV2,
    build_human_auditor_attestation_receipt_v2,
    canonical_human_auditor_attestation_v2_bytes,
    human_auditor_attestation_receipt_v2_integrity_errors,
    load_and_validate_human_auditor_attestation_v2,
)

NOW = datetime(2026, 9, 8, 20, 30, tzinfo=UTC)


def _attestation(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "schema_version": "life-patterns-human-auditor-attestation-v2",
        "auditor_id": "private-auditor-001",
        "independent_of_participant": True,
        "participant_or_theory_exposed_owner": False,
        "target_theory_blind": True,
        "llm_outputs_available_before_first_pass": False,
        "automated_consensus_available_before_first_pass": False,
        "target_model_outputs_available": False,
        "birth_or_chart_data_available": False,
        "automated_coder_used_for_first_pass": False,
        "human_facing_offline_ui_used": True,
        "first_pass_completed_at_utc": NOW.isoformat(),
        "auditor_notes": "Private note must not enter the public receipt.",
    }
    values.update(overrides)
    return values


def _raw(**overrides: object) -> bytes:
    return json.dumps(_attestation(**overrides), sort_keys=True).encode("utf-8")


def test_eligible_attestation_is_accepted_and_receipt_hides_identity_and_notes() -> None:
    raw = _raw()
    attestation = load_and_validate_human_auditor_attestation_v2(raw)
    receipt = build_human_auditor_attestation_receipt_v2(raw)

    assert attestation.auditor_id == "private-auditor-001"
    assert receipt.receipt_id.startswith("LPHA2-")
    assert receipt.payload.attestation_sha256 == hashlib.sha256(raw).hexdigest()
    assert receipt.payload.auditor_id_sha256 == hashlib.sha256(
        b"private-auditor-001"
    ).hexdigest()
    assert receipt.payload.contains_auditor_identity is False
    assert receipt.payload.contains_auditor_notes is False
    rendered = receipt.model_dump_json()
    assert "private-auditor-001" not in rendered
    assert "Private note" not in rendered
    assert human_auditor_attestation_receipt_v2_integrity_errors(receipt) == ()


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("independent_of_participant", False),
        ("participant_or_theory_exposed_owner", True),
        ("target_theory_blind", False),
        ("llm_outputs_available_before_first_pass", True),
        ("automated_consensus_available_before_first_pass", True),
        ("target_model_outputs_available", True),
        ("birth_or_chart_data_available", True),
        ("automated_coder_used_for_first_pass", True),
        ("human_facing_offline_ui_used", False),
    ],
)
def test_ineligible_or_contaminated_declarations_fail_closed(
    field: str,
    bad_value: object,
) -> None:
    with pytest.raises(ValidationError):
        load_and_validate_human_auditor_attestation_v2(_raw(**{field: bad_value}))


def test_naive_completion_time_fails_closed() -> None:
    with pytest.raises(ValidationError, match="timezone-aware"):
        load_and_validate_human_auditor_attestation_v2(
            _raw(first_pass_completed_at_utc="2026-09-08T20:30:00")
        )


def test_canonical_helper_does_not_replace_raw_byte_hash_authority() -> None:
    raw = _raw()
    attestation = DevelopmentHumanAuditorAttestationV2.model_validate_json(raw)
    canonical = canonical_human_auditor_attestation_v2_bytes(attestation)
    receipt = build_human_auditor_attestation_receipt_v2(raw)

    assert receipt.payload.attestation_sha256 == hashlib.sha256(raw).hexdigest()
    assert canonical != raw
