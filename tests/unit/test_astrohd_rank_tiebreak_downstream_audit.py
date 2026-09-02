from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).parents[2]
AUDIT_PATH = ROOT / "reference/audits/astrohd_rank_tiebreak_downstream_v1.json"


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


def test_source_consumer_inventory_is_deterministic_and_traceable() -> None:
    auditor = _auditor()
    audit = _load()

    assert audit["source_locations"] == auditor._scan_locations(ROOT)
    assert audit["ordered_sequence_consumers"] == auditor._ordered_sequence_consumers(ROOT)
    assert audit["source_locations"]
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


def test_all_scanned_source_hashes_match_current_files() -> None:
    hashes = _load()["source_file_hashes"]
    expected_paths = sorted(
        path.relative_to(ROOT).as_posix() for path in (ROOT / "src/hdmatch").rglob("*.py")
    )

    assert [row["path"] for row in hashes] == expected_paths
    for row in hashes:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]


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


def test_generated_json_regenerates_byte_identically(tmp_path: Path) -> None:
    auditor = _auditor()
    output = tmp_path / AUDIT_PATH.name

    auditor.write_audit(ROOT, output=output)

    assert output.read_bytes() == AUDIT_PATH.read_bytes()
