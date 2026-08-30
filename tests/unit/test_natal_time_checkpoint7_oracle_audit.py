from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import pytest

from scripts.audit_natal_time_checkpoint7_oracle import (
    CORPUS_PATH,
    LEDGER_PATH,
    MATRIX_PATH,
    MUTATION_PATH,
    REQUIRED_COVERAGE,
    OracleDiscrepancyError,
    build_discrepancy_ledger,
    validate_oracle_artifacts,
)
from tests.oracles.natal_time_v3_oracle import JsonObject

PROJECT_ROOT = Path(__file__).parents[2]


@pytest.fixture(scope="module")
def artifacts() -> dict[str, JsonObject]:
    result: dict[str, JsonObject] = {}
    for path in (CORPUS_PATH, MATRIX_PATH, MUTATION_PATH, LEDGER_PATH):
        value = json.loads((PROJECT_ROOT / path).read_bytes())
        assert isinstance(value, dict)
        result[path] = cast(JsonObject, value)
    return result


def _keys(value: object) -> set[str]:
    result: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            result.add(str(key).lower())
            result.update(_keys(child))
    elif isinstance(value, list):
        for child in value:
            result.update(_keys(child))
    return result


def test_saved_oracle_artifacts_reproduce_exactly(artifacts: dict[str, JsonObject]) -> None:
    validate_oracle_artifacts(PROJECT_ROOT, artifacts)


def test_adversarial_corpus_covers_every_required_case(
    artifacts: dict[str, JsonObject],
) -> None:
    corpus = artifacts[CORPUS_PATH]

    assert corpus["case_count"] == 41
    assert set(cast(list[str], corpus["observed_coverage_tags"])) == REQUIRED_COVERAGE
    assert corpus["contains_participant_or_live_reference_data"] is False
    assert corpus["contains_s_i_selection_procedure"] is False
    for case in cast(list[JsonObject], corpus["cases"]):
        assert "reference" not in case
        assert "selected_intervals" not in case


def test_comparison_matrix_has_complete_exact_agreement_and_zero_precommit_reads(
    artifacts: dict[str, JsonObject],
) -> None:
    matrix = artifacts[MATRIX_PATH]
    comparisons = cast(list[JsonObject], matrix["comparisons"])

    assert matrix["comparison_count"] == 41
    assert matrix["agreement_count"] == 41
    assert matrix["discrepancy_count"] == 0
    assert all(item["exact_agreement"] is True for item in comparisons)
    assert all(item["reference_loads_before_s_i_commitment"] == 0 for item in comparisons)
    probe = cast(JsonObject, matrix["t_only_inference_invariance_probe"])
    assert probe["inference_visible_bytes_unchanged"] is True
    assert probe["original_reference_loads_before_s_i_commitment"] == 0
    assert probe["changed_reference_loads_before_s_i_commitment"] == 0


def test_no_comparison_summary_contains_an_inferential_output(
    artifacts: dict[str, JsonObject],
) -> None:
    matrix = artifacts[MATRIX_PATH]
    prohibited = {
        "rank",
        "best",
        "score",
        "weight",
        "probability",
        "confidence",
        "utility",
        "threshold",
        "recommendation",
    }
    for item in cast(list[JsonObject], matrix["comparisons"]):
        for field in ("production_summary", "oracle_summary"):
            assert not (_keys(item[field]) & prohibited)


def test_every_major_guard_mutation_is_killed(artifacts: dict[str, JsonObject]) -> None:
    report = artifacts[MUTATION_PATH]
    baseline = cast(JsonObject, report["baseline"])

    assert baseline["passed"] is True
    assert report["mutation_count"] == 13
    assert report["killed_count"] == 13
    assert report["survivor_count"] == 0
    assert all(item["killed"] is True for item in cast(list[JsonObject], report["mutations"]))


def test_discrepancy_ledger_is_empty_and_injected_discrepancy_blocks(
    artifacts: dict[str, JsonObject],
) -> None:
    ledger = artifacts[LEDGER_PATH]

    assert ledger["status"] == "passed_no_discrepancies"
    assert ledger["checkpoint_completion_blocked"] is False
    assert ledger["discrepancy_count"] == 0
    injected = build_discrepancy_ledger(
        [{"case_id": "SYNTH-INJECTED-DISCREPANCY"}],
        oracle_version_sha256=cast(str, ledger["oracle_version_sha256"]),
    )
    assert injected["checkpoint_completion_blocked"] is True
    assert injected["discrepancy_count"] == 1
    with pytest.raises(OracleDiscrepancyError) as raised:
        raise OracleDiscrepancyError(injected)
    assert raised.value.ledger == injected
