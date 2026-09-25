from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).parents[2]
AUDIT_PATH = ROOT / "reference/audits/astrohd_cross_class_core_fit_v1.json"
AUDIT_SHA256 = "a113fb53de13f38d5053955975912a1fb194f527c57f610c82d0efc38bc32a70"

SOURCE_HASHES = {
    "mappings/mapping_library_v1.json": (
        "3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200"
    ),
    "src/hdmatch/model/dependencies.py": (
        "a49672a0edbca3ecbd121d563f7f7758b521a3cdf317c058b42ad9f137504a7d"
    ),
    "src/hdmatch/model/symbolic_score.py": (
        "fd1f216c2579aab0ba9aef74249fa5804cb7433b7eb13f452dfe1381b09f0aaa"
    ),
    "src/hdmatch/participant/backend.py": (
        "80ad02402ec0ea3a094bcd2977e9843c68d296b198bcfc7e836ef71043313198"
    ),
}


def _auditor() -> ModuleType:
    path = ROOT / "scripts/audit_astrohd_cross_class_core_fit.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_cross_class_core_fit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load() -> dict[str, Any]:
    payload = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _words(value: Any) -> set[str]:
    if isinstance(value, dict):
        values = [*value.keys(), *value.values()]
        return {word for child in values for word in _words(child)}
    if isinstance(value, list):
        return {word for child in value for word in _words(child)}
    if isinstance(value, str):
        return set(re.findall(r"[a-z]+(?:_[a-z]+)*", value.casefold()))
    return set()


def test_cross_class_cluster_set_and_classes_match_exactly() -> None:
    audit = _load()
    rows = {row["cluster_id"]: row for row in audit["dependency_clusters"]}

    assert audit["status"] == "mechanical_diagnostic_only_no_runtime_effect"
    assert audit["cross_class_dependency_cluster_ids"] == [
        "AUTHORITY_DECISION",
        "TYPE_STRATEGY_ARCHITECTURE",
    ]
    assert rows["AUTHORITY_DECISION"]["structural_classes"] == [
        "authority",
        "diagnostic_center",
    ]
    assert rows["TYPE_STRATEGY_ARCHITECTURE"]["structural_classes"] == [
        "diagnostic_center",
        "type_strategy",
    ]
    assert all(
        row["structural_class_count"] == len(row["structural_classes"]) for row in rows.values()
    )


@pytest.mark.parametrize("case_id", ["A1", "B1"])
def test_baseline_case_metrics_reproduce(case_id: str) -> None:
    case = _load()["controlled_scorer_cases"][case_id]
    score = case["score"]
    arithmetic = case["core_fit_block_arithmetic"]

    assert score["net_rubric_bits"] == pytest.approx(1.0)
    assert score["contradiction_rubric_bits"] == 0.0
    assert score["detailed_support"] == pytest.approx(50.0)
    assert score["core_fit"] == pytest.approx(66.6666666667)
    assert arithmetic["available_weight_total"] == 45.0
    assert arithmetic["earned_weight_total"] == 30.0
    assert arithmetic["core_fit"] == pytest.approx(score["core_fit"])


@pytest.mark.parametrize("case_id", ["A2", "B2"])
def test_augmented_case_metrics_reproduce(case_id: str) -> None:
    case = _load()["controlled_scorer_cases"][case_id]
    score = case["score"]
    arithmetic = case["core_fit_block_arithmetic"]

    assert score["net_rubric_bits"] == pytest.approx(1.0)
    assert score["contradiction_rubric_bits"] == 0.0
    assert score["detailed_support"] == pytest.approx(50.0)
    assert score["core_fit"] == pytest.approx(78.57142857142857)
    assert arithmetic["available_weight_total"] == 70.0
    assert arithmetic["earned_weight_total"] == 55.0
    assert arithmetic["core_fit"] == pytest.approx(score["core_fit"])
    blocks = {row["structural_class"]: row for row in arithmetic["blocks"]}
    assert blocks["diagnostic_center"] == {
        "available_weight": 25.0,
        "block_name": "diagnostic_centers",
        "confidence_total": 1.0,
        "dependency_cluster_ids": [
            "AUTHORITY_DECISION" if case_id == "A2" else "TYPE_STRATEGY_ARCHITECTURE"
        ],
        "earned_weight": 25.0,
        "fraction": 1.0,
        "structural_class": "diagnostic_center",
        "support_times_confidence_total": 1.0,
    }


@pytest.mark.parametrize("before,after", [("A1", "A2"), ("B1", "B2")])
def test_case_transition_holds_non_core_metrics_equal(before: str, after: str) -> None:
    cases = _load()["controlled_scorer_cases"]
    first = cases[before]["score"]
    second = cases[after]["score"]

    for field in (
        "net_rubric_bits",
        "contradiction_rubric_bits",
        "detailed_support",
    ):
        assert first[field] == pytest.approx(second[field])
    assert first["core_fit"] == pytest.approx(66.6666666667)
    assert second["core_fit"] == pytest.approx(78.57142857142857)


def test_global_dependency_collapse_has_one_relevant_contribution() -> None:
    cases = _load()["controlled_scorer_cases"]
    expected = {
        "A2": {
            "cluster": "AUTHORITY_DECISION",
            "raw_count": 2,
            "winner": "MAP-AUTH-EMOTIONAL-D03",
        },
        "B2": {
            "cluster": "TYPE_STRATEGY_ARCHITECTURE",
            "raw_count": 3,
            "winner": "MAP-TYPE-GENERATOR-S02",
        },
    }
    for case_id, values in expected.items():
        collapse = cases[case_id]["global_dependency_collapse"]
        assert collapse["dependency_cluster_id"] == values["cluster"]
        assert collapse["raw_contribution_count"] == values["raw_count"]
        assert collapse["collapsed_contribution_count"] == 1
        assert collapse["winning_mapping_id"] == values["winner"]
        assert collapse["winning_support"] == 1.0
        assert collapse["winning_evidence_rubric_bits"] == 1.0
        assert collapse["resulting_evidence_rubric_bits"] == 1.0


def test_ranking_case_orders_high_ahead_only_on_core_fit() -> None:
    ranking = _load()["ranking_case"]
    low = ranking["scores"]["LOW"]
    high = ranking["scores"]["HIGH"]

    assert ranking["only_differing_score_field"] == "core_fit"
    assert ranking["held_equal_fields"] == [
        "net_rubric_bits",
        "evidence_rubric_bits",
        "contradiction_rubric_bits",
        "meaningful_contradictions",
        "detailed_support",
    ]
    for field in ranking["held_equal_fields"]:
        assert low[field] == high[field]
    assert low["core_fit"] == pytest.approx(66.66666666666667)
    assert high["core_fit"] == pytest.approx(78.57142857142857)
    assert ranking["ordered_state_ids"] == ["HIGH", "LOW"]
    assert ranking["better_scientific_rank_state_id"] == "HIGH"
    assert ranking["scientific_rank_by_state_id"] == {"HIGH": 1.0, "LOW": 2.0}


def test_historical_source_hashes_remain_recorded_byte_identically() -> None:
    source_rows = _load()["source"]
    recorded = {row["path"]: row["sha256"] for row in source_rows.values()}

    assert recorded == SOURCE_HASHES
    assert _sha256(AUDIT_PATH) == AUDIT_SHA256


def test_directed_mapping_facts_and_source_behavior_are_mechanical() -> None:
    audit = _load()

    assert audit["source_behavior"] == {
        "core_fit_support_basis": "mapping_directness_when_mapping_support_is_nonzero",
        "ordinary_evidence_support_basis": "structural_salience_times_mapping_directness",
    }
    assert audit["directed_mapping_facts"] == [
        {
            "dependency_cluster": "AUTHORITY_DECISION",
            "mapping_id": "MAP-AUTH-EMOTIONAL-D03",
            "question_ids": ["D03"],
            "structural_class": "authority",
        },
        {
            "dependency_cluster": "TYPE_STRATEGY_ARCHITECTURE",
            "mapping_id": "MAP-CENTER-SACRAL-DEFINED-C08",
            "question_ids": ["C08"],
            "structural_class": "diagnostic_center",
        },
        {
            "dependency_cluster": "AUTHORITY_DECISION",
            "mapping_id": "MAP-CENTER-SOLARPLEXUS-DEFINED-C02",
            "question_ids": ["C02"],
            "structural_class": "diagnostic_center",
        },
        {
            "dependency_cluster": "TYPE_STRATEGY_ARCHITECTURE",
            "mapping_id": "MAP-TYPE-GENERATOR-S02",
            "question_ids": ["S02"],
            "structural_class": "type_strategy",
        },
    ]


def test_artifact_has_no_prohibited_interpretive_terms() -> None:
    prohibited = {
        "bug",
        "bias",
        "correct",
        "incorrect",
        "defect",
        "fix",
        "recommended",
        "blocker",
        "owner_decision",
    }

    assert prohibited.isdisjoint(_words(_load()))


def test_historical_audit_refuses_regeneration_after_source_change(tmp_path: Path) -> None:
    auditor = _auditor()
    output = tmp_path / AUDIT_PATH.name

    with pytest.raises(
        auditor.HistoricalAuditSourceMismatch,
        match="historical audit describes pre-patch source",
    ):
        auditor.write_audit(ROOT, output=output)
    assert not output.exists()
