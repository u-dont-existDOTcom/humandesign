from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest

from hdmatch.natal_time.evaluation_contract import (
    VerificationError,
    validate_no_prohibited_fields,
    verify_receipt,
    verify_receipt_self_hash,
)
from hdmatch.util import sha256_json
from scripts.build_natal_time_synthetic_evaluation_verifier import (
    FixturePair,
    GeneratedBundle,
    build_bundle,
)
from tests.oracles.natal_time_v3_oracle import (
    JsonObject,
    evaluate_preconstructed_fixture,
    independent_sha256_json,
    validate_receipt_guard,
)

PROJECT_ROOT = Path(__file__).parents[2]
ORACLE_PATH = PROJECT_ROOT / "tests/oracles/natal_time_v3_oracle.py"


@pytest.fixture(scope="module")
def bundle() -> GeneratedBundle:
    return build_bundle(PROJECT_ROOT)


@dataclass
class _CountingLoader:
    value: JsonObject
    calls: int = 0

    def __call__(self) -> JsonObject:
        self.calls += 1
        return deepcopy(self.value)


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


def _pairs_and_receipts(
    bundle: GeneratedBundle,
) -> tuple[dict[str, FixturePair], dict[str, JsonObject]]:
    pairs = {
        cast(str, pair.inference_visible["fixture_id"]): pair
        for pair in bundle.fixture_pairs
    }
    receipts = {
        cast(str, receipt["fixture_id"]): receipt for receipt in bundle.receipts
    }
    return pairs, receipts


def test_oracle_has_no_production_or_builder_import() -> None:
    tree = ast.parse(ORACLE_PATH.read_bytes(), filename=str(ORACLE_PATH))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.add(node.module)

    assert not any(name.startswith("hdmatch") for name in imported)
    assert not any(name.startswith("scripts") for name in imported)
    assert "evaluation_contract" not in ORACLE_PATH.read_text(encoding="utf-8")
    assert "build_bundle" not in ORACLE_PATH.read_text(encoding="utf-8")


def test_independent_oracle_agrees_with_all_production_fixture_results(
    bundle: GeneratedBundle,
) -> None:
    for pair, receipt in zip(bundle.fixture_pairs, bundle.receipts, strict=True):
        loader = _CountingLoader(pair.evaluator_reference)
        oracle = evaluate_preconstructed_fixture(pair.inference_visible, loader)
        assert oracle.fixture_id == receipt["fixture_id"]
        assert oracle.summary == _production_summary(receipt)
        assert oracle.access_trace["reference_loads_before_s_i_commitment"] == 0
        assert oracle.access_trace["reference_load_count"] == loader.calls
        assert loader.calls in {0, 1}


def test_reordered_disconnected_output_has_identical_commitment_and_metrics(
    bundle: GeneratedBundle,
) -> None:
    pairs, receipts = _pairs_and_receipts(bundle)
    first = receipts["SYNTH-FIXTURE-DISCONNECTED-SAME-DATE"]
    reordered = receipts["SYNTH-FIXTURE-DISCONNECTED-REORDERED"]

    assert first["s_i_commitment_sha256"] == reordered["s_i_commitment_sha256"]
    assert first["metrics"] == reordered["metrics"]
    for fixture_id in (
        "SYNTH-FIXTURE-DISCONNECTED-SAME-DATE",
        "SYNTH-FIXTURE-DISCONNECTED-REORDERED",
    ):
        pair = pairs[fixture_id]
        result = evaluate_preconstructed_fixture(
            pair.inference_visible, lambda pair=pair: deepcopy(pair.evaluator_reference)
        )
        assert result.summary["s_i_commitment_sha256"] == first["s_i_commitment_sha256"]


def test_repeated_state_counts_diverge_independently(bundle: GeneratedBundle) -> None:
    pairs, receipts = _pairs_and_receipts(bundle)
    pair = pairs["SYNTH-FIXTURE-REPEATED-STATE"]
    result = evaluate_preconstructed_fixture(
        pair.inference_visible, lambda: deepcopy(pair.evaluator_reference)
    )
    metrics = cast(JsonObject, result.summary["metrics"])

    assert metrics == receipts["SYNTH-FIXTURE-REPEATED-STATE"]["metrics"]
    assert cast(JsonObject, metrics["canonical_interval_count_retained"])["fraction"] == "1/3"
    assert cast(JsonObject, metrics["unique_state_identity_count_retained"])["fraction"] == (
        "1/4"
    )


def test_changing_only_t_leaves_precommit_bytes_and_access_unchanged(
    bundle: GeneratedBundle,
) -> None:
    pairs, _receipts = _pairs_and_receipts(bundle)
    pair = pairs["SYNTH-FIXTURE-FULL-C"]
    original_visible = independent_sha256_json(pair.inference_visible)
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

    assert independent_sha256_json(pair.inference_visible) == original_visible
    assert original.access_trace["reference_loads_before_s_i_commitment"] == 0
    assert changed.access_trace["reference_loads_before_s_i_commitment"] == 0


@pytest.mark.parametrize(
    "field",
    ["score", "probability", "confidence", "threshold", "recommendation"],
)
def test_rehashed_forbidden_receipt_fields_fail_both_guards(
    bundle: GeneratedBundle, field: str
) -> None:
    _pairs, receipts = _pairs_and_receipts(bundle)
    mutant = deepcopy(receipts["SYNTH-FIXTURE-FULL-C"])
    mutant[field] = 1
    unhashed = dict(mutant)
    unhashed.pop("receipt_sha256")
    mutant["receipt_sha256"] = sha256_json(unhashed)

    assert verify_receipt_self_hash(mutant)
    with pytest.raises(
        VerificationError, match="prohibited_inferential_or_scalar_output_field"
    ):
        validate_no_prohibited_fields(mutant)
    assert verify_receipt(mutant) is False
    assert validate_receipt_guard(mutant) == (
        False,
        "prohibited_inferential_or_scalar_output_field",
    )


def test_rehashed_nested_forbidden_field_fails_both_guards(
    bundle: GeneratedBundle,
) -> None:
    _pairs, receipts = _pairs_and_receipts(bundle)
    mutant = deepcopy(receipts["SYNTH-FIXTURE-FULL-C"])
    metrics = cast(JsonObject, mutant["metrics"])
    intersection = cast(JsonObject, metrics["reference_intersection"])
    intersection["nested_probability"] = "0/1"
    mutant["metrics_sha256"] = sha256_json(metrics)
    unhashed = dict(mutant)
    unhashed.pop("receipt_sha256")
    mutant["receipt_sha256"] = sha256_json(unhashed)

    assert verify_receipt_self_hash(mutant)
    with pytest.raises(
        VerificationError, match="prohibited_inferential_or_scalar_output_field"
    ):
        validate_no_prohibited_fields(mutant)
    assert verify_receipt(mutant) is False
    assert validate_receipt_guard(mutant) == (
        False,
        "prohibited_inferential_or_scalar_output_field",
    )
