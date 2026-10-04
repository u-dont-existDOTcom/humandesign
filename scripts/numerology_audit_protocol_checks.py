#!/usr/bin/env python3
"""Small audit-control proofs; not a numerology reading or human-study engine."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

BASE = "reference/research/numerology_v2_20261004/"
EFFECTIVE = "reference/research/numerology_method_registry_v2_1_20261004.json"


def primary_cell_score(cells: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Score only independently observation-complete cells, with no abstentions.

    Cells need unique arm-independent keys. Complete cells require binary outcome
    and decision. Incomplete cells are reported, never credited as primary hits.
    The caller must separately ensure identical cell keys across compared arms.
    """
    rows = list(cells)
    keys = [r["key"] for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate primary cell keys")
    eligible = [r for r in rows if r.get("observation_complete") is True]
    if not eligible:
        raise ValueError("No observation-complete primary cells")
    counts = dict(TP=0, FP=0, FN=0, TN=0)
    for row in eligible:
        y, pred = row.get("outcome"), row.get("decision")
        if type(y) is not int or y not in (0, 1):
            raise ValueError("Complete cells need independently coded binary outcomes")
        if type(pred) is not int or pred not in (0, 1):
            raise ValueError("Arm not admitted: primary binary coverage is incomplete")
        counts["TP" if pred == y == 1 else "TN" if pred == y == 0 else "FP" if pred else "FN"] += 1
    n = len(eligible)
    errors = counts["FP"] + counts["FN"]
    return {**counts, "N_eligible": n, "eligible_keys": sorted(r["key"] for r in eligible),
            "unassessed_cells": len(rows) - n, "error": errors / n,
            "utility": -errors, "symmetric_score": n - 2 * errors}


def compare_primary_cells(left: list[dict], right: list[dict]) -> tuple[dict, dict]:
    a, b = primary_cell_score(left), primary_cell_score(right)
    if a["eligible_keys"] != b["eligible_keys"]:
        raise ValueError("Primary arms do not share the identical eligible cell set")
    return a, b


def both_timing_anchors_pass(calendar_pass: bool, birthday_age_pass: bool) -> bool:
    if type(calendar_pass) is not bool or type(birthday_age_pass) is not bool:
        raise ValueError("Both separately evaluated anchor decisions are required")
    return calendar_pass and birthday_age_pass


def validate_reconciled_contract(data: dict) -> list[str]:
    c = data.get("constraints", {})
    expected = {
        "primary_objective": "minimize_(FP+FN)/N_eligible",
        "companion_utility": "-(FP+FN)",
        "threshold_objective": "primary_equal_cost_error",
        "primary_observation_complete_windows_only": True,
        "completeness_rule_independent_of_event_found": True,
        "same_primary_cells_for_all_arms": True,
        "events_in_incomplete_windows_get_primary_credit": False,
        "primary_requires_full_binary_coverage": True,
        "abstention_primary_disposition": "ARM_NOT_ADMITTED_NO_PRIMARY_SCORE",
        "selective_comparisons_same_cell_set": True,
        "nonscorable_assigned_by": "frozen_arm_agnostic_translator",
        "scorable_residue_assessment_required": True,
        "primary_timing_anchors": ["calendar", "birthday_age"],
        "primary_timing_claim_requires_both_anchors": True,
        "timing_anchors_are_independent_replications": False,
        "external_horoscope_overlay_scope": "RELEVANT_TO_OVERALL_FULL_AUTHOR_ARMS",
        "horoscope_adapter_required_for": ["CAMPBELL_YOUR_DAYS_V1", "JAVANE_BUNKER_DIVINE_TRIANGLE_V1"],
        "numerology_only_subset_admitted_as_full_arm": False,
        "owner_aware_audit_documents_allowed_in_reader_context": False,
        "branch_selection_blind_to_development_outcomes": True,
        "trivial_controls_required": ["constant_negative", "development_base_rate"],
    }
    errors = []
    for key, value in expected.items():
        same = c.get(key) is value if isinstance(value, bool) else c.get(key) == value
        if not same:
            errors.append("RECONCILED_CONTROL_VIOLATION: " + key)
    if "true_positive_reward" in c:
        errors.append("ASYMMETRIC_REWARD_REINTRODUCED")
    ablation = data.get("relationship_ablation", {})
    if ablation.get("label") != "WWYB_DELTA_ABLATION" or ablation.get("relationship_only") is not False or ablation.get("affected_endpoints") != ["period_personality", "relationships"]:
        errors.append("CHEIRO_DELTA_SCOPE_UNDERSTATED")
    return errors


def validate_effective_overlay(root: Path) -> list[str]:
    errors = []
    try:
        registry = json.loads((root / EFFECTIVE).read_text())
        if registry.get("errata_id") != "NUMEROLOGY_AUDIT_ERRATA_V2_1_20261004" or registry.get("method_rule_changes") != []:
            errors.append("EFFECTIVE_AUDIT_OVERLAY_SCOPE_CHANGED")
        for name, digest in registry["mandatory_files_sha256"].items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
                errors.append("EFFECTIVE_OVERLAY_HASH_MISMATCH: " + name)
        overrides = json.loads((root / BASE / "source_audit_overrides_v2_1.json").read_text())
        status = overrides["overrides"]["J-A07"]["effective_status"]
        if status != "WITHDRAWN_AUDIT_ERROR":
            errors.append("DOYLE_AUDIT_ERROR_REINTRODUCED")
    except (OSError, KeyError, ValueError, TypeError) as exc:
        errors.append("EFFECTIVE_AUDIT_OVERLAY_INVALID: " + str(exc)[:160])
    return errors
