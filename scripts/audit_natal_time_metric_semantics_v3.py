"""Audit the checkpoint-5 metric/reference-domain v3 contract.

This audit validates policy artifacts only.  It does not select ``S_i``, run an
evaluator, read participant data, or calculate a reference-accuracy result.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from hdmatch.util import canonical_json_bytes, sha256_file, sha256_json

PROJECT_ROOT = Path(__file__).parents[1]
V1_PATH = Path("state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json")
V2_PATH = Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json")
V3_PATH = Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json")
AUDIT_PATH = Path("state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3-AUDIT.json")
V1_CONTRACT_SHA256 = "c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9"
V2_CONTRACT_SHA256 = "067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e"
V3_CONTRACT_SHA256 = "75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe"
V1_FILE_SHA256 = "dc76792218c32ccca392ecdfb2cd706f3f3df6112df2a15a40310bd99be0ed04"
V2_FILE_SHA256 = "a1244378acbb7c0cf5a3f6464c7d1186dda9c70dac300357e28f9d530cb5adfd"

REFERENCE_EDGE_IDS = {
    "reference-contained-in-one-interval",
    "reference-contained-across-adjacent-intervals",
    "reference-extends-before-domain",
    "reference-extends-after-domain",
    "reference-extends-across-both-domain-ends",
    "reference-wholly-outside-domain",
    "reference-endpoint-only-contact",
    "reference-multidate-included-date",
    "reference-multidate-excluded-date",
}
SUBSET_EDGE_IDS = {
    "s-i-disconnected-first-and-third-same-date",
    "s-i-disconnected-reordered",
    "s-i-disconnected-duplicate",
    "s-i-manufactured-spanning-window",
}


class ContractAuditError(ValueError):
    """Raised when the v3 contract or preserved predecessors fail closed."""


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        raise ContractAuditError(f"invalid contract JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ContractAuditError(f"contract is not a JSON object: {path}")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractAuditError(message)


def _verify_contract_hash(payload: dict[str, Any], expected: str) -> None:
    unhashed = deepcopy(payload)
    embedded = unhashed.pop("contract_sha256", None)
    _require(embedded == expected, "contract embedded digest changed")
    _require(sha256_json(unhashed) == expected, "contract canonical digest mismatch")


def validate_v3_contract(repository_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    """Validate exact preservation, supersession, and required v3 semantics."""

    root = repository_root.resolve(strict=True)
    v1_path = root / V1_PATH
    v2_path = root / V2_PATH
    v3_path = root / V3_PATH
    _require(sha256_file(v1_path) == V1_FILE_SHA256, "preserved v1 bytes changed")
    _require(sha256_file(v2_path) == V2_FILE_SHA256, "preserved v2 bytes changed")
    v1 = _load_object(v1_path)
    v2 = _load_object(v2_path)
    v3 = _load_object(v3_path)
    _verify_contract_hash(v1, V1_CONTRACT_SHA256)
    _verify_contract_hash(v2, V2_CONTRACT_SHA256)
    _verify_contract_hash(v3, V3_CONTRACT_SHA256)

    supersession = v3.get("supersession")
    _require(isinstance(supersession, dict), "v3 lacks supersession object")
    supersession = cast(dict[str, Any], supersession)
    _require(
        supersession.get("preserved_v1", {}).get("file_sha256") == V1_FILE_SHA256,
        "v3 does not bind preserved v1 bytes",
    )
    _require(
        supersession.get("preserved_v2", {}).get("file_sha256") == V2_FILE_SHA256,
        "v3 does not bind preserved v2 bytes",
    )

    sets = v3.get("set_semantics_v3")
    _require(isinstance(sets, dict), "v3 lacks set semantics")
    sets = cast(dict[str, Any], sets)
    c_i = cast(dict[str, Any], sets.get("C_i", {}))
    s_i = cast(dict[str, Any], sets.get("S_i_candidate_subset", {}))
    d_i = cast(dict[str, Any], sets.get("D_i", {}))
    _require(
        "gap-free, non-overlapping partition" in c_i.get("partition_requirement", ""),
        "C_i within-domain partition requirement is missing",
    )
    _require(
        "not to the geometry of a selected S_i" in c_i.get("partition_scope", ""),
        "C_i partition is not separated from S_i geometry",
    )
    _require(
        "any nonempty unordered subset" in s_i.get("definition", ""),
        "S_i is not an arbitrary nonempty unordered exact subset",
    )
    _require(
        "nonadjacent intervals on the same civil date" in s_i.get("allowed_geometry", ""),
        "disconnected same-date S_i is not expressly allowed",
    )
    _require(
        "are not validity conditions" in s_i.get("adjacency_rule", ""),
        "S_i adjacency or contiguity remains a validity condition",
    )
    _require(
        "does not require S_i" in s_i.get("distinct_from_C_i_partition", ""),
        "C_i completeness is conflated with S_i adjacency",
    )
    _require(d_i.get("formula") == "D_i = union_{I in C_i} I", "D_i is not the exact union of C_i")
    _require(
        "not the convex hull" in d_i.get("no_convex_hull_rule", ""),
        "D_i could fill candidate-domain gaps",
    )

    compatibility = v3.get("reference_domain_compatibility_v3")
    _require(isinstance(compatibility, dict), "v3 lacks reference-domain semantics")
    compatibility = cast(dict[str, Any], compatibility)
    states = compatibility.get("states")
    _require(isinstance(states, list), "reference-domain states are not a list")
    states = cast(list[Any], states)
    by_status = {item.get("status"): item for item in states if isinstance(item, dict)}
    _require(
        set(by_status)
        == {
            "reference_domain_compatible",
            "reference_domain_partially_incompatible",
            "reference_domain_incompatible",
        },
        "reference-domain state set changed",
    )
    _require(
        "T_i is a subset of D_i" in by_status["reference_domain_compatible"]["condition"],
        "full compatibility is not exact subset containment",
    )
    _require(
        by_status["reference_domain_partially_incompatible"]["reference_intersection_applicability"]
        == "not_applicable_reference_domain_partially_incompatible",
        "partial incompatibility lacks typed N/A intersection",
    )
    _require(
        by_status["reference_domain_incompatible"]["reference_intersection_applicability"]
        == "not_applicable_reference_domain_incompatible",
        "complete incompatibility lacks typed N/A intersection",
    )
    _require(
        by_status["reference_domain_compatible"]["valid_reference_evaluation_receipt_allowed"]
        is True,
        "compatible reference cannot issue a valid receipt",
    )
    for status in (
        "reference_domain_partially_incompatible",
        "reference_domain_incompatible",
    ):
        _require(
            by_status[status]["valid_reference_evaluation_receipt_allowed"] is False,
            f"{status} can issue a valid reference receipt",
        )
    _require(
        "neither credit nor error"
        in compatibility.get("partial_or_complete_incompatibility_rule", ""),
        "incompatibility disposition is not neutral",
    )
    _require(
        "Never clip T_i" in compatibility.get("immutability_rule", ""),
        "reference or candidate mutation is not prohibited",
    )

    cases = v3.get("acceptance_edge_cases")
    _require(isinstance(cases, list), "v3 edge cases are not a list")
    cases = cast(list[Any], cases)
    by_id = {item.get("id"): item for item in cases if isinstance(item, dict)}
    _require(
        set(by_id) == REFERENCE_EDGE_IDS | SUBSET_EDGE_IDS,
        "v3 acceptance edge-case coverage changed",
    )
    allowed_reference_receipts = {
        case_id
        for case_id in REFERENCE_EDGE_IDS
        if by_id[case_id]["valid_reference_evaluation_receipt_allowed"] is True
    }
    _require(
        allowed_reference_receipts
        == {
            "reference-contained-in-one-interval",
            "reference-contained-across-adjacent-intervals",
            "reference-multidate-included-date",
        },
        "reference edge cases authorize the wrong valid receipts",
    )
    _require(
        v3.get("implementation_boundary", {}).get("metric_evaluator_modified_by_this_contract")
        is False,
        "v3 contract improperly modifies evaluator execution",
    )
    _require(
        all(v3.get("forbidden_semantics", {}).values()),
        "a v3 forbidden semantic is not fail closed",
    )
    return v3


def build_audit_report(repository_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    """Build a deterministic machine-readable contract audit receipt."""

    contract = validate_v3_contract(repository_root)
    payload: dict[str, Any] = {
        "schema_version": "natal-time-preinference-metric-semantics-v3-audit-v1",
        "status": "passed_contract_only_no_evaluator_execution",
        "synthetic_only": True,
        "human_records_accessed": 0,
        "v1_file_sha256": V1_FILE_SHA256,
        "v1_contract_sha256": V1_CONTRACT_SHA256,
        "v2_file_sha256": V2_FILE_SHA256,
        "v2_contract_sha256": V2_CONTRACT_SHA256,
        "v3_file_sha256": sha256_file(repository_root / V3_PATH),
        "v3_contract_sha256": contract["contract_sha256"],
        "checks": [
            "preserved_v1_v2_exact_bytes",
            "canonical_v1_v2_v3_contract_hashes",
            "C_i_partition_distinct_from_S_i_adjacency",
            "disconnected_same_date_S_i_allowed",
            "D_i_exact_union_without_gap_filling",
            "three_way_reference_domain_classification",
            "typed_NA_for_partial_and_complete_incompatibility",
            "no_reference_clipping_or_C_i_T_i_mutation",
            "all_checkpoint5_subset_and_reference_edge_cases",
            "no_evaluator_or_S_i_selector_implemented",
        ],
        "acceptance_edge_case_ids": sorted(REFERENCE_EDGE_IDS | SUBSET_EDGE_IDS),
        "valid_reference_receipt_edge_case_ids": [
            "reference-contained-across-adjacent-intervals",
            "reference-contained-in-one-interval",
            "reference-multidate-included-date",
        ],
    }
    payload["audit_sha256"] = sha256_json(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = build_audit_report(args.repository_root)
    if args.check:
        committed = _load_object(args.repository_root / AUDIT_PATH)
        if committed != report:
            raise ContractAuditError("committed v3 audit artifact does not reproduce")
    print(canonical_json_bytes(report).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
