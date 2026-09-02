from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).parents[2]
AUDIT_PATH = ROOT / "reference/audits/astrohd_rank_tiebreak_downstream_v1.json"
AUDIT_SHA256 = "c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103"


def _auditor() -> ModuleType:
    path = ROOT / "scripts/audit_astrohd_rank_tiebreak_downstream.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_rank_tiebreak_downstream", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load() -> dict[str, Any]:
    payload = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _result(comparator: str) -> dict[str, Any]:
    return _load()["comparators"]["equal_evidence_core_fit_difference"][comparator]


def test_current_and_two_research_comparators_reproduce_directed_results() -> None:
    current = _result("current")
    proposal_a = _result("rank_group_without_core_fit")
    proposal_b = _result("rank_order_without_core_fit")

    assert current["ordered_state_ids"] == ["HIGH", "LOW"]
    assert current["scientific_rank_by_state_id"] == {"HIGH": 1.0, "LOW": 2.0}
    assert proposal_a["ordered_state_ids"] == ["HIGH", "LOW"]
    assert proposal_a["scientific_rank_by_state_id"] == {"HIGH": 1.5, "LOW": 1.5}
    assert proposal_b["ordered_state_ids"] == ["LOW", "HIGH"]
    assert proposal_b["scientific_rank_by_state_id"] == {"HIGH": 1.5, "LOW": 1.5}


def test_helper_outputs_reproduce_equal_net_fixture() -> None:
    helpers = _load()["comparators"]["equal_evidence_core_fit_difference"]["helper_outputs"]

    assert helpers["current_top_net_margin"] == 0.0
    assert helpers["top_state_tie_count_by_comparator"] == {
        "current": 1,
        "rank_group_without_core_fit": 2,
        "rank_order_without_core_fit": 2,
    }
    assert helpers["percentile_by_comparator_and_state"] == {
        "current": {"HIGH": 100.0, "LOW": 50.0},
        "rank_group_without_core_fit": {"HIGH": 75.0, "LOW": 75.0},
        "rank_order_without_core_fit": {"HIGH": 75.0, "LOW": 75.0},
    }


def test_all_comparators_agree_on_preceding_field_controls() -> None:
    controls = _load()["comparators"]["non_tie_controls"]

    assert [row["control_id"] for row in controls] == [
        "different_net_rubric_bits",
        "different_meaningful_contradictions",
        "different_detailed_support",
    ]
    for control in controls:
        for comparator in (
            "current",
            "rank_group_without_core_fit",
            "rank_order_without_core_fit",
        ):
            assert control[comparator]["ordered_state_ids"] == ["PREFERRED", "OTHER"]
            assert control[comparator]["scientific_rank_by_state_id"] == {
                "OTHER": 2.0,
                "PREFERRED": 1.0,
            }
        assert control["scores"]["PREFERRED"]["core_fit"] == 0.0
        assert control["scores"]["OTHER"]["core_fit"] == 100.0


def test_ordered_sequence_consumers_match_mechanical_scan() -> None:
    consumers = _load()["ordered_sequence_consumers"]

    assert [(row["function"], row["line"], row["operation"]) for row in consumers] == [
        ("AstroHDParticipantBackend.rank", 199, "iterate_ranked_states"),
        (
            "AstroHDParticipantBackend.rank",
            220,
            "iterate_ranked_states_and_index_first_rank",
        ),
        (
            "AstroHDParticipantBackend.rank",
            232,
            "pass_ranked_states_to_top_net_margin",
        ),
        (
            "AstroHDParticipantBackend.discrimination",
            287,
            "iterate_ranked_and_index_first_rank",
        ),
        (
            "AstroHDParticipantBackend.discrimination",
            288,
            "pass_ranked_to_top_net_margin",
        ),
        (
            "AstroHDParticipantBackend._top_net_margin",
            544,
            "index_first_ranked_state",
        ),
        (
            "AstroHDParticipantBackend._top_net_margin",
            545,
            "iterate_ranked_tail_slice",
        ),
    ]


def test_historical_source_consumer_inventory_is_recorded_and_traceable() -> None:
    audit = _load()

    assert len(audit["source_locations"]) == 33
    assert len(audit["ordered_sequence_consumers"]) == 7
    assert all(row["traceability"] == "traceable" for row in audit["source_locations"])
    assert {row["token"] for row in audit["source_locations"]} >= {
        "_rank_states",
        "_evidence_tie_key",
        "_top_net_margin",
        "_RankedState",
        ".rank",
        "top_state_tie_count",
        "true_state_rank",
        "true_state_percentile",
        "percentile",
    }


def test_historical_source_hashes_and_artifact_remain_recorded_byte_identically() -> None:
    hashes = _load()["source_file_hashes"]
    recorded = {row["path"]: row["sha256"] for row in hashes}

    assert len(hashes) == 120
    assert recorded["src/hdmatch/participant/backend.py"] == (
        "80ad02402ec0ea3a094bcd2977e9843c68d296b198bcfc7e836ef71043313198"
    )
    assert recorded["src/hdmatch/search/date_aggregator.py"] == (
        "d358c0914f84d341b69ced1771c5d26a9818837ed24ae45c9808920e08c8a3ce"
    )
    assert hashlib.sha256(AUDIT_PATH.read_bytes()).hexdigest() == AUDIT_SHA256


def test_research_comparators_are_not_referenced_by_production_source() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "src/hdmatch").rglob("*.py")
    )

    assert "rank_group_without_core_fit" not in source
    assert "rank_order_without_core_fit" not in source


def test_audit_uses_synthetic_inputs_only() -> None:
    audit = _load()

    assert audit["status"] == "mechanical_downstream_audit_no_runtime_effect"
    assert audit["input_scope"] == "synthetic_candidate_and_scored_state_records_only"
    fixture = audit["comparators"]["equal_evidence_core_fit_difference"]
    assert fixture["state_start_order"] == ["LOW", "HIGH"]
    assert set(fixture["scores"]) == {"LOW", "HIGH"}


def test_historical_audit_refuses_regeneration_after_source_change(tmp_path: Path) -> None:
    auditor = _auditor()
    output = tmp_path / AUDIT_PATH.name

    with pytest.raises(
        auditor.HistoricalAuditSourceMismatch,
        match="historical audit describes pre-patch source",
    ):
        auditor.write_audit(ROOT, output=output)
    assert not output.exists()
