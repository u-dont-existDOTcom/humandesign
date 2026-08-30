"""Build checkpoint-7 independent-oracle comparison and mutation artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.evaluation_contract import (
    VerificationError,
    validate_no_prohibited_fields,
    verify_receipt,
    verify_receipt_self_hash,
)
from hdmatch.util import canonical_json_bytes, sha256_json
from scripts.build_natal_time_synthetic_evaluation_verifier import build_bundle
from tests.oracles.natal_time_v3_oracle import (
    JsonObject,
    evaluate_preconstructed_fixture,
    independent_sha256_json,
    validate_receipt_guard,
)

V3_CONTRACT_SHA256 = "75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe"
ORACLE_PATH = "tests/oracles/natal_time_v3_oracle.py"
PRODUCTION_PATH = "src/hdmatch/natal_time/evaluation_contract.py"
BUILDER_PATH = "scripts/build_natal_time_synthetic_evaluation_verifier.py"

CORPUS_PATH = "state/NATAL-TIME-CHECKPOINT7-ORACLE-ADVERSARIAL-CORPUS.json"
MATRIX_PATH = "state/NATAL-TIME-CHECKPOINT7-ORACLE-COMPARISON-MATRIX.json"
MUTATION_PATH = "state/NATAL-TIME-CHECKPOINT7-ORACLE-MUTATION-REPORT.json"
LEDGER_PATH = "state/NATAL-TIME-CHECKPOINT7-ORACLE-DISCREPANCY-LEDGER.json"

REQUIRED_COVERAGE = frozenset(
    {
        "full_c_i",
        "single_interval_s_i",
        "disconnected_first_third_same_date",
        "reordered_equivalent_s_i",
        "duplicate_interval",
        "partial_interval",
        "manufactured_gap_spanning_interval",
        "foreign_interval",
        "repeated_nonadjacent_same_state",
        "multiple_candidate_dates",
        "t_i_contained_one_interval",
        "t_i_spans_included_intervals",
        "partial_reference_before_domain",
        "partial_reference_after_domain",
        "partial_reference_both_ends",
        "endpoint_only_contact",
        "wholly_incompatible_reference_date",
        "abstention",
        "empty_non_abstention",
        "documentary_source_conflict",
        "precommit_t_i_access_attempt",
        "post_access_s_i_mutation",
        "cross_role_connected_component",
        "nested_forbidden_field_insertion",
        "rehashed_scalar_score_insertion",
        "rehashed_probability_insertion",
        "rehashed_confidence_insertion",
        "rehashed_threshold_insertion",
        "rehashed_recommendation_insertion",
    }
)

COVERAGE_BY_FIXTURE: dict[str, tuple[str, ...]] = {
    "SYNTH-FIXTURE-FULL-C": ("full_c_i", "t_i_contained_one_interval"),
    "SYNTH-FIXTURE-BOUNDARY-TOUCH": (
        "single_interval_s_i",
        "endpoint_only_contact",
    ),
    "SYNTH-FIXTURE-REPEATED-STATE": ("repeated_nonadjacent_same_state",),
    "SYNTH-FIXTURE-MULTIPLE-DATES": ("multiple_candidate_dates",),
    "SYNTH-FIXTURE-PARTIAL-REFERENCE-ONE-MICROSECOND": (
        "partial_reference_before_domain",
    ),
    "SYNTH-FIXTURE-REFERENCE-CONTAINED-ACROSS-ADJACENT": (
        "t_i_spans_included_intervals",
    ),
    "SYNTH-FIXTURE-REFERENCE-EXTENDS-AFTER-DOMAIN": (
        "partial_reference_after_domain",
    ),
    "SYNTH-FIXTURE-REFERENCE-EXTENDS-BOTH-DOMAIN-ENDS": (
        "partial_reference_both_ends",
    ),
    "SYNTH-FIXTURE-MULTIDATE-EXCLUDED-DATE": (
        "wholly_incompatible_reference_date",
    ),
    "SYNTH-FIXTURE-SOURCE-CONFLICT": ("documentary_source_conflict",),
    "SYNTH-FIXTURE-ABSTENTION": ("abstention",),
    "SYNTH-FIXTURE-EMPTY-NON-ABSTENTION": ("empty_non_abstention",),
    "SYNTH-FIXTURE-PARTIAL-INTERVAL": ("partial_interval",),
    "SYNTH-FIXTURE-DUPLICATE-INTERVAL": ("duplicate_interval",),
    "SYNTH-FIXTURE-FOREIGN-INTERVAL": ("foreign_interval",),
    "SYNTH-FIXTURE-MANUFACTURED-INTERVAL": (
        "manufactured_gap_spanning_interval",
    ),
    "SYNTH-FIXTURE-EARLY-REFERENCE-ACCESS": ("precommit_t_i_access_attempt",),
    "SYNTH-FIXTURE-EARLY-REFERENCE-RAW-BYTE": ("precommit_t_i_access_attempt",),
    "SYNTH-FIXTURE-EARLY-REFERENCE-DIGEST": ("precommit_t_i_access_attempt",),
    "SYNTH-FIXTURE-EARLY-REFERENCE-METADATA": ("precommit_t_i_access_attempt",),
    "SYNTH-FIXTURE-EARLY-REFERENCE-ALTERNATE-LOADER": (
        "precommit_t_i_access_attempt",
    ),
    "SYNTH-FIXTURE-POST-REFERENCE-OUTPUT-MUTATION": (
        "post_access_s_i_mutation",
    ),
    "SYNTH-FIXTURE-CROSS-ROLE-COMPONENT": ("cross_role_connected_component",),
    "SYNTH-FIXTURE-DISCONNECTED-SAME-DATE": (
        "disconnected_first_third_same_date",
    ),
    "SYNTH-FIXTURE-DISCONNECTED-REORDERED": ("reordered_equivalent_s_i",),
    "SYNTH-FIXTURE-DISCONNECTED-DUPLICATE": ("duplicate_interval",),
}

RECEIPT_MUTATIONS = (
    (
        "ORACLE-RECEIPT-NESTED-FORBIDDEN",
        "nested_probability",
        "nested_forbidden_field_insertion",
    ),
    ("ORACLE-RECEIPT-SCORE", "score", "rehashed_scalar_score_insertion"),
    ("ORACLE-RECEIPT-PROBABILITY", "probability", "rehashed_probability_insertion"),
    ("ORACLE-RECEIPT-CONFIDENCE", "confidence", "rehashed_confidence_insertion"),
    ("ORACLE-RECEIPT-THRESHOLD", "threshold", "rehashed_threshold_insertion"),
    (
        "ORACLE-RECEIPT-RECOMMENDATION",
        "recommendation",
        "rehashed_recommendation_insertion",
    ),
)

MUTATION_OPERATORS: tuple[dict[str, object], ...] = (
    {
        "mutation_id": "guard-duplicate-selection",
        "category": "metric_membership",
        "replacements": (
            (
                "if len(selected_payloads) != len(set(selected_payloads)):",
                "if False:",
                1,
            ),
            ("if len(selected_ids) != len(set(selected_ids)):", "if False:", 1),
        ),
    },
    {
        "mutation_id": "guard-empty-nonabstention",
        "category": "metric_abstention",
        "replacements": (("if not output.selected_intervals:", "if False:", 1),),
    },
    {
        "mutation_id": "guard-whole-interval-membership",
        "category": "metric_membership",
        "replacements": (("if selected != frozen:", "if False:", 1),),
    },
    {
        "mutation_id": "guard-manufactured-boundary-code",
        "category": "metric_membership",
        "replacements": (
            (
                'self._invalidate("manufactured_interval_not_allowed")',
                'self._invalidate("foreign_or_manufactured_interval")',
                1,
            ),
        ),
    },
    {
        "mutation_id": "guard-cross-role-component",
        "category": "access_contamination",
        "replacements": (
            (
                "if any(len(roles) > 1 for roles in roles_by_component.values()):",
                "if False:",
                2,
            ),
        ),
    },
    {
        "mutation_id": "guard-contaminated-component",
        "category": "access_contamination",
        "replacements": (("if contamination_status != \"clean\":", "if False:", 1),),
    },
    {
        "mutation_id": "guard-precommit-reference-access",
        "category": "access_order",
        "replacements": (
            (
                "if self.phase is not SessionPhase.OUTPUT_COMMITTED:",
                "if False:",
                1,
            ),
        ),
    },
    {
        "mutation_id": "guard-postaccess-s-i-mutation",
        "category": "access_order",
        "replacements": (
            (
                "if self.phase is SessionPhase.REFERENCE_EXPOSED:",
                "if False:",
                2,
            ),
        ),
    },
    {
        "mutation_id": "guard-reference-domain-classification",
        "category": "metric_reference_domain",
        "replacements": (
            ("if overlap_width == reference_width:", "if overlap_width > 0:", 1),
        ),
    },
    {
        "mutation_id": "guard-half-open-intersection",
        "category": "metric_reference_intersection",
        "replacements": (
            (
                "return max(left_start, right_start) < min(left_end, right_end)",
                "return max(left_start, right_start) <= min(left_end, right_end)",
                1,
            ),
        ),
    },
    {
        "mutation_id": "guard-prohibited-output-schema",
        "category": "schema",
        "replacements": (
            (
                "if any(fragment in lowered for fragment in PROHIBITED_OUTPUT_FRAGMENTS):",
                "if False:",
                1,
            ),
        ),
    },
    {
        "mutation_id": "guard-postaccess-t-i-integrity",
        "category": "access_order",
        "replacements": (("if cached != self._opened_payload_digest:", "if False:", 1),),
    },
    {
        "mutation_id": "guard-fraction-calculation",
        "category": "metric_fraction",
        "replacements": (
            (
                "fraction = Fraction(numerator, denominator)",
                "fraction = Fraction(0, 1)",
                1,
            ),
        ),
    },
)


class OracleAuditError(ValueError):
    """Raised when an oracle audit artifact cannot be reproduced."""


class OracleDiscrepancyError(OracleAuditError):
    """Raised with a fail-closed discrepancy ledger when comparison disagrees."""

    def __init__(self, ledger: JsonObject) -> None:
        super().__init__("independent oracle discrepancy blocks checkpoint completion")
        self.ledger = ledger


def _git_text(root: Path, arguments: Sequence[str]) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _git_file(root: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=root, check=True, capture_output=True
    )
    return result.stdout


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _self_hashed(payload: JsonObject, field: str) -> JsonObject:
    result = deepcopy(payload)
    result[field] = sha256_json(result)
    return result


def _validate_self_hash(payload: Mapping[str, object], field: str) -> None:
    unhashed = dict(payload)
    embedded = unhashed.pop(field, None)
    if embedded != sha256_json(unhashed):
        raise OracleAuditError(f"self-hash mismatch: {field}")


def _production_summary(receipt: JsonObject) -> JsonObject:
    kind = cast(str, receipt["receipt_kind"])
    common: JsonObject = {
        "receipt_kind": kind,
        "inference_or_selection_performed": receipt["inference_or_selection_performed"],
    }
    if kind == "fail_closed_rejection":
        common["violation_codes"] = receipt["violation_codes"]
        return common
    common["s_i_commitment_sha256"] = receipt["s_i_commitment_sha256"]
    if kind == "reference_domain_diagnostic":
        common.update(
            {
                "valid_reference_evaluation_receipt": receipt[
                    "valid_reference_evaluation_receipt"
                ],
                "reference_domain_status": receipt["reference_domain_status"],
                "reference_intersection": receipt["reference_intersection"],
                "documentary_reference_width": receipt[
                    "documentary_reference_width"
                ],
            }
        )
        return common
    common.update(
        {
            "evaluation_eligible": receipt["evaluation_eligible"],
            "metrics": receipt["metrics"],
        }
    )
    return common


def _oracle_version(root: Path, source_commit: str) -> JsonObject:
    oracle_source = (root / ORACLE_PATH).read_bytes()
    if oracle_source != _git_file(root, source_commit, ORACLE_PATH):
        raise OracleAuditError("loaded oracle differs from the declared source commit")
    tree = ast.parse(oracle_source, filename=ORACLE_PATH)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.add(node.module)
    if any(name.startswith(("hdmatch", "scripts")) for name in imported):
        raise OracleAuditError("independent oracle imports a production module")
    packet: JsonObject = {
        "schema_version": "natal-time-v3-independent-oracle-version-v1",
        "source_commit": source_commit,
        "source_tree_oid": _git_text(root, ("rev-parse", f"{source_commit}^{{tree}}")),
        "oracle_path": ORACLE_PATH,
        "oracle_source_sha256": _sha256(oracle_source),
        "operative_v3_contract_sha256": V3_CONTRACT_SHA256,
        "standard_library_only": True,
        "production_imports": [],
        "constructs_or_chooses_s_i": False,
    }
    packet["oracle_version_sha256"] = sha256_json(packet)
    return packet


def _base_comparisons(
    root: Path, oracle_version_sha256: str
) -> tuple[list[JsonObject], list[JsonObject]]:
    bundle = build_bundle(root)
    cases: list[JsonObject] = []
    comparisons: list[JsonObject] = []
    for pair, receipt in zip(bundle.fixture_pairs, bundle.receipts, strict=True):
        loads = 0

        def load_reference(pair_value: object = pair) -> Mapping[str, object]:
            nonlocal loads
            loads += 1
            pair_typed = cast(Any, pair_value)
            return cast(Mapping[str, object], deepcopy(pair_typed.evaluator_reference))

        oracle = evaluate_preconstructed_fixture(pair.inference_visible, load_reference)
        production = _production_summary(receipt)
        coverage = list(COVERAGE_BY_FIXTURE.get(oracle.fixture_id, ()))
        cases.append(
            {
                "case_id": oracle.fixture_id,
                "case_kind": "committed_separated_fixture",
                "source_fixture_id": oracle.fixture_id,
                "coverage_tags": coverage,
            }
        )
        comparisons.append(
            {
                "case_id": oracle.fixture_id,
                "case_kind": "committed_separated_fixture",
                "coverage_tags": coverage,
                "production_summary": production,
                "production_summary_sha256": sha256_json(production),
                "oracle_summary": oracle.summary,
                "oracle_summary_sha256": independent_sha256_json(oracle.summary),
                "oracle_version_sha256": oracle_version_sha256,
                "reference_load_count": loads,
                "reference_loads_before_s_i_commitment": oracle.access_trace[
                    "reference_loads_before_s_i_commitment"
                ],
                "exact_agreement": oracle.summary == production,
            }
        )
    return cases, comparisons


def _mutated_receipt(
    base: JsonObject, mutation_kind: str, field: str
) -> JsonObject:
    mutant = deepcopy(base)
    if mutation_kind == "nested_probability":
        metrics = cast(JsonObject, mutant["metrics"])
        intersection = cast(JsonObject, metrics["reference_intersection"])
        intersection["nested_probability"] = "0/1"
        mutant["metrics_sha256"] = sha256_json(metrics)
    else:
        mutant[field] = 1
    unhashed = dict(mutant)
    unhashed.pop("receipt_sha256", None)
    mutant["receipt_sha256"] = sha256_json(unhashed)
    return mutant


def _receipt_guard_comparisons(
    root: Path, oracle_version_sha256: str
) -> tuple[list[JsonObject], list[JsonObject]]:
    bundle = build_bundle(root)
    receipts = {
        cast(str, item["fixture_id"]): item for item in bundle.receipts
    }
    base = receipts["SYNTH-FIXTURE-FULL-C"]
    cases: list[JsonObject] = []
    comparisons: list[JsonObject] = []
    for case_id, field, coverage in RECEIPT_MUTATIONS:
        mutant = _mutated_receipt(base, field, field)
        if not verify_receipt_self_hash(mutant):
            raise OracleAuditError(f"production mutant is not self-hashed: {case_id}")
        production_code: str | None = None
        try:
            validate_no_prohibited_fields(mutant)
        except VerificationError as exc:
            production_code = exc.code
        production_accepted = verify_receipt(mutant)
        oracle_accepted, oracle_code = validate_receipt_guard(mutant)
        production_summary: JsonObject = {
            "accepted": production_accepted,
            "controlled_code": production_code,
            "self_hash_valid": True,
        }
        oracle_summary: JsonObject = {
            "accepted": oracle_accepted,
            "controlled_code": oracle_code,
            "self_hash_valid": True,
        }
        cases.append(
            {
                "case_id": case_id,
                "case_kind": "rehashed_postcommit_schema_mutant",
                "source_fixture_id": "SYNTH-FIXTURE-FULL-C",
                "mutation": {
                    "operation": "insert_and_rehash",
                    "field": field,
                    "nested": field == "nested_probability",
                },
                "coverage_tags": [coverage],
            }
        )
        comparisons.append(
            {
                "case_id": case_id,
                "case_kind": "rehashed_postcommit_schema_mutant",
                "coverage_tags": [coverage],
                "production_summary": production_summary,
                "production_summary_sha256": sha256_json(production_summary),
                "oracle_summary": oracle_summary,
                "oracle_summary_sha256": independent_sha256_json(oracle_summary),
                "oracle_version_sha256": oracle_version_sha256,
                "reference_load_count": 0,
                "reference_loads_before_s_i_commitment": 0,
                "exact_agreement": oracle_summary == production_summary,
            }
        )
    return cases, comparisons


def _t_only_invariance_probe(root: Path) -> JsonObject:
    bundle = build_bundle(root)
    pair = next(
        item
        for item in bundle.fixture_pairs
        if item.inference_visible["fixture_id"] == "SYNTH-FIXTURE-FULL-C"
    )
    inference_before = canonical_json_bytes(pair.inference_visible)
    changed_reference = deepcopy(pair.evaluator_reference)
    reference = cast(JsonObject, changed_reference["reference"])
    sources = cast(list[JsonObject], reference["sources"])
    sources[0]["end_utc"] = "2099-01-01T02:00:00.000001Z"
    original = evaluate_preconstructed_fixture(
        pair.inference_visible, lambda: deepcopy(pair.evaluator_reference)
    )
    changed = evaluate_preconstructed_fixture(
        pair.inference_visible, lambda: deepcopy(changed_reference)
    )
    inference_after = canonical_json_bytes(pair.inference_visible)
    if inference_before != inference_after:
        raise OracleAuditError("T-only mutation changed inference-visible bytes")
    if (
        original.access_trace["reference_loads_before_s_i_commitment"] != 0
        or changed.access_trace["reference_loads_before_s_i_commitment"] != 0
    ):
        raise OracleAuditError("T-only invariance probe read a reference before S_i commitment")
    return {
        "fixture_id": "SYNTH-FIXTURE-FULL-C",
        "mutation": "evaluator-only synthetic T_i end changed by one microsecond",
        "inference_visible_bytes_sha256_before": _sha256(inference_before),
        "inference_visible_bytes_sha256_after": _sha256(inference_after),
        "inference_visible_bytes_unchanged": True,
        "original_reference_loads_before_s_i_commitment": 0,
        "changed_reference_loads_before_s_i_commitment": 0,
        "oracle_summary_changed_only_after_authorized_reference_load": (
            original.summary != changed.summary
        ),
    }


def build_discrepancy_ledger(
    discrepancies: Sequence[Mapping[str, object]], *, oracle_version_sha256: str
) -> JsonObject:
    status = "blocked_discrepancies_present" if discrepancies else "passed_no_discrepancies"
    return _self_hashed(
        {
            "schema_version": "natal-time-v3-independent-oracle-discrepancy-ledger-v1",
            "synthetic_only": True,
            "oracle_version_sha256": oracle_version_sha256,
            "status": status,
            "checkpoint_completion_blocked": bool(discrepancies),
            "discrepancy_count": len(discrepancies),
            "entries": [dict(item) for item in discrepancies],
        },
        "ledger_sha256",
    )


def _apply_replacements(source: str, replacements: object) -> str:
    result = source
    for raw in cast(Sequence[tuple[str, str, int]], replacements):
        old, new, expected_count = raw
        available = result.count(old)
        if available < expected_count:
            raise OracleAuditError(
                f"mutation target count changed: {old!r} has {available}, needs {expected_count}"
            )
        result = result.replace(old, new, expected_count)
    return result


def _run_mutation_suite(
    root: Path, *, mutated_source: str | None
) -> tuple[int, str, str]:
    command = (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/unit/test_natal_time_synthetic_evaluation_contract.py",
        "--tb=short",
        "--maxfail=1",
    )
    environment = os.environ.copy()
    if mutated_source is None:
        environment["PYTHONPATH"] = f"{root / 'src'}:{root}"
        result = subprocess.run(
            command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="natal-oracle-mutant-") as directory:
            temporary = Path(directory)
            overlay = temporary / "src" / "hdmatch"
            shutil.copytree(root / "src" / "hdmatch", overlay)
            target = temporary / "src" / "hdmatch" / "natal_time" / "evaluation_contract.py"
            target.write_text(mutated_source, encoding="utf-8")
            environment["PYTHONPATH"] = f"{temporary / 'src'}:{root / 'src'}:{root}"
            result = subprocess.run(
                command,
                cwd=root,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )
    combined = result.stdout + result.stderr
    return (result.returncode, _sha256(combined.encode("utf-8")), " ".join(command))


def _mutation_report(
    root: Path, source_commit: str, oracle_version_sha256: str
) -> JsonObject:
    production_source = (root / PRODUCTION_PATH).read_text(encoding="utf-8")
    if production_source.encode("utf-8") != _git_file(root, source_commit, PRODUCTION_PATH):
        raise OracleAuditError("production evaluator differs from oracle audit source commit")
    baseline_code, baseline_output_sha, command = _run_mutation_suite(
        root, mutated_source=None
    )
    if baseline_code != 0:
        raise OracleAuditError("mutation baseline test suite is not green")
    records: list[JsonObject] = []
    for operator in MUTATION_OPERATORS:
        mutated = _apply_replacements(production_source, operator["replacements"])
        return_code, output_sha, mutant_command = _run_mutation_suite(
            root, mutated_source=mutated
        )
        records.append(
            {
                "mutation_id": operator["mutation_id"],
                "category": operator["category"],
                "target_path": PRODUCTION_PATH,
                "replacement_count": sum(
                    item[2]
                    for item in cast(Sequence[tuple[str, str, int]], operator["replacements"])
                ),
                "test_command": mutant_command,
                "return_code": return_code,
                "output_sha256": output_sha,
                "killed": return_code != 0,
            }
        )
    survivors = [item["mutation_id"] for item in records if not item["killed"]]
    if survivors:
        raise OracleAuditError(f"major-guard mutation survivors: {survivors}")
    return _self_hashed(
        {
            "schema_version": "natal-time-v3-independent-oracle-mutation-report-v1",
            "synthetic_only": True,
            "source_commit": source_commit,
            "oracle_version_sha256": oracle_version_sha256,
            "production_target_path": PRODUCTION_PATH,
            "baseline": {
                "test_command": command,
                "return_code": baseline_code,
                "output_sha256": baseline_output_sha,
                "passed": True,
            },
            "mutation_count": len(records),
            "killed_count": len(records),
            "survivor_count": 0,
            "mutations": records,
        },
        "mutation_report_sha256",
    )


def build_oracle_artifacts(
    repository_root: Path, source_commit: str
) -> dict[str, JsonObject]:
    root = repository_root.resolve(strict=True)
    if len(source_commit) != 40 or _git_text(root, ("rev-parse", source_commit)) != source_commit:
        raise OracleAuditError("oracle source commit is not an exact commit")
    for bound_path in (PRODUCTION_PATH, BUILDER_PATH):
        if (root / bound_path).read_bytes() != _git_file(root, source_commit, bound_path):
            raise OracleAuditError(
                f"loaded production comparison surface differs from source: {bound_path}"
            )
    version = _oracle_version(root, source_commit)
    version_sha = cast(str, version["oracle_version_sha256"])
    fixture_cases, fixture_comparisons = _base_comparisons(root, version_sha)
    mutant_cases, mutant_comparisons = _receipt_guard_comparisons(root, version_sha)
    cases = [*fixture_cases, *mutant_cases]
    comparisons = [*fixture_comparisons, *mutant_comparisons]
    coverage = sorted(
        {
            tag
            for item in cases
            for tag in cast(list[str], item["coverage_tags"])
        }
    )
    missing = sorted(REQUIRED_COVERAGE - set(coverage))
    if missing:
        raise OracleAuditError(f"adversarial corpus coverage missing: {missing}")
    corpus = _self_hashed(
        {
            "schema_version": "natal-time-v3-independent-oracle-adversarial-corpus-v1",
            "synthetic_only": True,
            "source_commit": source_commit,
            "oracle_version": version,
            "case_count": len(cases),
            "required_coverage_tags": sorted(REQUIRED_COVERAGE),
            "observed_coverage_tags": coverage,
            "cases": cases,
            "contains_participant_or_live_reference_data": False,
            "contains_s_i_selection_procedure": False,
        },
        "corpus_sha256",
    )
    discrepancies = [
        {
            "case_id": item["case_id"],
            "production_summary_sha256": item["production_summary_sha256"],
            "oracle_summary_sha256": item["oracle_summary_sha256"],
        }
        for item in comparisons
        if not item["exact_agreement"]
        or item["reference_loads_before_s_i_commitment"] != 0
    ]
    ledger = build_discrepancy_ledger(discrepancies, oracle_version_sha256=version_sha)
    if discrepancies:
        raise OracleDiscrepancyError(ledger)
    bundle = build_bundle(root)
    evaluator_version = cast(JsonObject, bundle.evaluator_schema["evaluator_version"])
    matrix = _self_hashed(
        {
            "schema_version": "natal-time-v3-independent-oracle-comparison-matrix-v1",
            "synthetic_only": True,
            "source_commit": source_commit,
            "oracle_version_sha256": version_sha,
            "production_evaluator_version_sha256": evaluator_version[
                "evaluator_version_sha256"
            ],
            "production_evaluator_source_sha256": _sha256(
                (root / PRODUCTION_PATH).read_bytes()
            ),
            "production_builder_source_sha256": _sha256((root / BUILDER_PATH).read_bytes()),
            "corpus_sha256": corpus["corpus_sha256"],
            "comparison_count": len(comparisons),
            "agreement_count": len(comparisons),
            "discrepancy_count": 0,
            "comparisons": comparisons,
            "t_only_inference_invariance_probe": _t_only_invariance_probe(root),
            "no_scalar_or_inferential_output": True,
            "inference_or_selection_performed": False,
        },
        "matrix_sha256",
    )
    mutation = _mutation_report(root, source_commit, version_sha)
    return {
        CORPUS_PATH: corpus,
        MATRIX_PATH: matrix,
        MUTATION_PATH: mutation,
        LEDGER_PATH: ledger,
    }


def validate_oracle_artifacts(root: Path, artifacts: Mapping[str, JsonObject]) -> None:
    corpus = artifacts[CORPUS_PATH]
    _validate_self_hash(corpus, "corpus_sha256")
    _validate_self_hash(artifacts[MATRIX_PATH], "matrix_sha256")
    _validate_self_hash(artifacts[MUTATION_PATH], "mutation_report_sha256")
    _validate_self_hash(artifacts[LEDGER_PATH], "ledger_sha256")
    source_commit = cast(str, corpus["source_commit"])
    rebuilt = build_oracle_artifacts(root, source_commit)
    if rebuilt != artifacts:
        raise OracleAuditError("checkpoint-7 oracle artifacts do not reproduce exactly")


def _load_artifacts(root: Path) -> dict[str, JsonObject]:
    result: dict[str, JsonObject] = {}
    for path in (CORPUS_PATH, MATRIX_PATH, MUTATION_PATH, LEDGER_PATH):
        payload = json.loads((root / path).read_bytes())
        if not isinstance(payload, dict):
            raise OracleAuditError(f"saved oracle artifact is not an object: {path}")
        result[path] = cast(JsonObject, payload)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--source-commit")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    if args.validate_only:
        artifacts = _load_artifacts(root)
        validate_oracle_artifacts(root, artifacts)
        print("CHECKPOINT7_INDEPENDENT_ORACLE_ARTIFACTS_OK")
        return 0
    source_commit = args.source_commit or _git_text(root, ("rev-parse", "HEAD^{commit}"))
    artifacts = build_oracle_artifacts(root, source_commit)
    for path, payload in artifacts.items():
        write_new_bytes(root / path, canonical_json_bytes(payload) + b"\n")
    corpus = artifacts[CORPUS_PATH]
    matrix = artifacts[MATRIX_PATH]
    mutation = artifacts[MUTATION_PATH]
    version = cast(JsonObject, corpus["oracle_version"])
    print(f"ORACLE_VERSION_SHA256:{version['oracle_version_sha256']}")
    print(f"ORACLE_MATRIX_SHA256:{matrix['matrix_sha256']}")
    print(f"ORACLE_MUTATION_REPORT_SHA256:{mutation['mutation_report_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
