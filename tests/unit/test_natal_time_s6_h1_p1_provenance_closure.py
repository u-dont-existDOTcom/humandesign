"""Synthetic provenance checks for the bounded checkpoint-11 P1 closure."""

from __future__ import annotations

import copy
import hashlib
from typing import Any

import pytest

from tests.s6_h1_prehuman.acceptance import P, _sha256
from tests.s6_h1_prehuman.validator import ROOT, load_json

REQUIRED_RECEIPT_FIELDS = {
    "ratifying_message_author": "OWNER",
    "ratifying_message_acquisition_mode": "DIRECT_OWNER_MESSAGE",
    "ratified_policy_text_origin": "ASSISTANT_PROPOSED",
    "owner_action": "EXPLICIT_RATIFICATION",
    "receipt_capability": "OWNER_REATTESTED",
    "reattestation_scope": "EPOCH5_H1_PRIOR_EXPOSURE_AND_SEMANTIC_CONTAMINATION_POLICY_ONLY",
    "independent_source_comparison": "NOT_INDEPENDENT",
}


def _validate_synthetic_receipt(receipt: dict[str, Any]) -> None:
    for field, expected in REQUIRED_RECEIPT_FIELDS.items():
        if receipt.get(field) != expected:
            raise ValueError(f"invalid provenance field: {field}")
    if receipt["ratifying_message"]["author"] != "OWNER":
        raise ValueError("ratifying message author conflated")
    if receipt["ratified_policy"]["text_origin"] != "ASSISTANT_PROPOSED":
        raise ValueError("proposal origin conflated")
    if receipt["sequence"] != [
        "ASSISTANT_PROPOSED_P1",
        "OWNER_EXPLICITLY_RATIFIED_P1",
    ]:
        raise ValueError("proposal/ratification sequence invalid")


def test_exact_owner_message_bytes_and_assistant_relay_are_separate() -> None:
    source = load_json(P["owner_ratification"])
    exact_bytes = source["message_text_exact"].encode(source["message_encoding"])
    assert exact_bytes == bytes.fromhex(source["message_utf8_hex"])
    assert exact_bytes == b"p1 approved exactly as stated"
    assert source["message_terminator_present"] is False
    assert source["message_byte_length"] == len(exact_bytes) == 29
    assert hashlib.sha256(exact_bytes).hexdigest() == source["message_sha256"]
    assert source["assistant_relay_to_pro"] == {
        "text": "Direct owner response: P1 approved exactly as stated.",
        "classification": "ASSISTANT_RELAY_OF_DIRECT_OWNER_DECISION",
        "not_the_canonical_owner_source": True,
    }


def test_receipt_binds_exact_owner_message_and_separate_p1_proposal() -> None:
    receipt = load_json(P["owner_receipt"])
    source = load_json(P["owner_ratification"])
    _validate_synthetic_receipt(receipt)
    assert receipt["ratifying_message"]["artifact_sha256"] == _sha256(
        P["owner_ratification"]
    )
    assert receipt["ratifying_message"]["exact_message_sha256"] == source[
        "message_sha256"
    ]
    assert receipt["ratified_policy"]["sha256"] == _sha256(P["p1_proposal"])
    assert receipt["supersedes"]["sha256"] == _sha256(
        ROOT / receipt["supersedes"]["path"]
    )


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("ratifying_message_author", "ASSISTANT"),
        ("ratifying_message_acquisition_mode", "ASSISTANT_RELAY"),
        ("ratified_policy_text_origin", "OWNER_AUTHORED"),
        ("owner_action", "ORIGINAL_AUTHORSHIP"),
        ("receipt_capability", "INTEGRITY_ONLY"),
        ("independent_source_comparison", "MATCH"),
    ],
)
def test_hostile_provenance_conflation_is_rejected(field: str, invalid: str) -> None:
    mutated = copy.deepcopy(load_json(P["owner_receipt"]))
    mutated[field] = invalid
    with pytest.raises(ValueError, match=field):
        _validate_synthetic_receipt(mutated)


def test_hostile_nested_proposal_origin_conflation_is_rejected() -> None:
    mutated = copy.deepcopy(load_json(P["owner_receipt"]))
    mutated["ratified_policy"]["text_origin"] = "DIRECT_OWNER_MESSAGE"
    with pytest.raises(ValueError, match="proposal origin conflated"):
        _validate_synthetic_receipt(mutated)


def test_hostile_ratification_before_proposal_sequence_is_rejected() -> None:
    mutated = copy.deepcopy(load_json(P["owner_receipt"]))
    mutated["sequence"].reverse()
    with pytest.raises(ValueError, match="sequence invalid"):
        _validate_synthetic_receipt(mutated)


def test_historical_misclassified_sources_remain_byte_identical() -> None:
    assert _sha256(
        ROOT / "state/NATAL-TIME-OWNER-OUTCOME-SOURCE-EPOCH5-20260830.md"
    ) == "ae31f03e2d2e83373be50c451f0bf998175a64ed83811570e613112035ebd131"
    assert _sha256(
        ROOT / "state/NATAL-TIME-OWNER-SOURCE-RECEIPT-EPOCH5-V1.json"
    ) == "332c48e97802617d1867dd769a7fa9d866b2ca8e864ace2ff9db5cb36124bc98"
    receipt = load_json(P["owner_receipt"])
    assert receipt["historical_source_classification"]["actual_origin"] == (
        "ASSISTANT_INTERPRETATION"
    )
    assert receipt["historical_source_classification"]["scientifically_rejected"] is False
    assert receipt["historical_source_classification"]["corrupted"] is False


def test_policy_semantics_are_unchanged_and_limited_to_ratified_p1() -> None:
    policy = load_json(P["policy"])
    authority = load_json(P["policy_authority"])
    outcome = load_json(P["owner_outcome"])
    assert authority["semantics_artifact"]["sha256"] == _sha256(P["policy"])
    assert authority["semantics_artifact"]["semantics_changed_by_overlay"] is False
    assert len(outcome["controlling_policy_terms"]) == 5
    assert [item["id"] for item in policy["substantive_outcomes"]] == [
        "ELIGIBLE",
        "REQUIRES_BLIND_ADJUDICATION",
        "INELIGIBLE_CLEAN_H1_AUTHOR",
    ]
    assert set(policy["invalid_independent_decision_bases"]) == {
        "belief",
        "skepticism",
        "reported_accuracy",
        "reported_mismatch",
        "curiosity",
        "perceived_usefulness",
        "product_interest",
        "absence_of_known_exposure_record",
    }


def test_p1_closure_does_not_change_production_source() -> None:
    assert not any((ROOT / "src").rglob("*p1*"))
