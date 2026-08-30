"""Deterministic checks for the epoch-4 owner-outcome supervision hotfix."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"

SOURCE = STATE / "NATAL-TIME-OWNER-OUTCOME-SOURCE-EPOCH4-20260830.md"
SOURCE_RECEIPT = STATE / "NATAL-TIME-OWNER-SOURCE-RECEIPT-EPOCH4-V1.json"
OUTCOME = STATE / "NATAL-TIME-OWNER-OUTCOME-EPOCH4-V1.json"
BOOTSTRAP = STATE / "NATAL-TIME-SUPERVISION-BOOTSTRAP-RECEIPT-V1.json"
CONTRACT = STATE / "NATAL-TIME-S6-H1-CHILD-TASK-CONTRACT-V1.json"
RECONCILIATION = STATE / "NATAL-TIME-OBJECTIVE-RECONCILIATION-EPOCH4-V1.json"
VERDICT = STATE / "NATAL-TIME-RESEARCH-SUPERVISION-VERDICT-EPOCH4-V1.json"
FEEDBACK = STATE / "SUPERVISION-DESIGN-FEEDBACK-SDF-20260830-OWNER-SOURCE-INDEPENDENCE-001.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_owner_source_and_receipt_are_exactly_bound() -> None:
    receipt = _load(SOURCE_RECEIPT)
    outcome = _load(OUTCOME)
    assert receipt["source_sha256"] == _sha256(SOURCE)
    assert receipt["worker_supplied_copy_sha256"] == _sha256(SOURCE)
    assert receipt["comparison"] == "MATCH"
    assert receipt["limitations"]
    assert outcome["source"]["sha256"] == _sha256(SOURCE)
    assert outcome["source"]["receipt_id"] == receipt["receipt_id"]
    assert outcome["status"] == "ACTIVE_PARENT_OUTCOME_OPEN"


def test_bootstrap_identity_and_protocol_integrity_receipts_are_present() -> None:
    receipt = _load(BOOTSTRAP)
    source = receipt["source"]
    assert source["commit"] == "90a230e85f78063080dc627ec36a0237c3234f72"
    assert source["bootstrap_sha256"] == (
        "c8a490c33310afe8a3a238f1b66d31a58ccb133a7d942cce537f7d3e9c67d8ea"
    )
    assert all(
        protocol["integrity_verified"] and protocol["loaded_complete"]
        for protocol in receipt["askrigor_protocols"].values()
    )
    assert receipt["completion_claim"] == "WORKING"
    assert receipt["root_outcome_achieved"] is False


def test_child_contract_covers_every_owner_requirement_without_closing_parent() -> None:
    outcome = _load(OUTCOME)
    contract = _load(CONTRACT)
    required = {item["id"] for item in outcome["required_outcomes"]}
    covered = {item["owner_requirement_id"] for item in contract["required_outcome_coverage"]}
    assert required == covered == {f"RO-{index:02d}" for index in range(1, 14)}
    assert all(item["parent_task_remains_open"] for item in contract["required_outcome_coverage"])
    assert contract["completion_claim"] == "WORKING"
    assert contract["root_parent_open"] is True
    assert "root completion claim" in contract["prohibited_in_this_child"]


def test_reconciliation_keeps_alignment_planes_and_completion_claim_separate() -> None:
    reconciliation = _load(RECONCILIATION)
    assert reconciliation["taskContract"]["sha256"] == _sha256(CONTRACT)
    assert reconciliation["ownerSource"]["outcomeRecordSha256"] == _sha256(OUTCOME)
    assert reconciliation["independentSupervisorReceipt"]["sha256"] == _sha256(
        SOURCE_RECEIPT
    )
    assert reconciliation["alignment"]["workerToContract"]["status"] == "GREEN"
    assert reconciliation["alignment"]["contractToOwner"]["status"] == "PARTIAL"
    assert reconciliation["alignment"]["contractToOwner"]["unmappedOwnerRequirementIds"] == []
    assert reconciliation["completionClaim"]["type"] == "WORKING"
    assert reconciliation["completionClaim"]["proposedTerminal"] is False
    assert reconciliation["result"]["rootTerminalizationAllowed"] is False


def test_research_assurance_planes_are_independent_and_release_is_closed() -> None:
    verdict = _load(VERDICT)
    assert verdict["operationalAlignment"]["status"] == "PASS"
    assert verdict["scientificAdequacy"]["status"] == "WARN"
    assert verdict["releaseAdequacy"]["status"] == "NOT_APPLICABLE"
    assert verdict["releasePermission"]["allowed"] is False
    assert verdict["completionClaimType"] == "WORKING"
    assert verdict["workerToContractAlignment"] == "GREEN"
    assert verdict["contractToOwnerAlignment"] == "PARTIAL"


def test_supervision_design_feedback_is_routed_to_shared_scope() -> None:
    feedback = _load(FEEDBACK)
    assert feedback["feedbackId"] == "SDF-20260830-OWNER-SOURCE-INDEPENDENCE-001"
    assert feedback["blocksCurrentBoundary"] is False
    assert feedback["routing"]["sharedProScopeKey"] == (
        "supervision-architecture/20260830-90a230e"
    )
    assert feedback["routing"]["reviewPriority"] == "BATCH"
    assert feedback["routing"]["conversationUrl"] == (
        "https://chatgpt.com/c/6a937aa4-1db8-83ea-813a-350bbab44ddf"
    )
    assert feedback["status"] == "SUBMITTED_PENDING_PRO_META_REVIEW"
