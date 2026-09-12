from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

from hdmatch.evaluation.development_evidence_v5 import DevelopmentEpisodeAnnotationResponseV5
from hdmatch.evaluation.facet_relation_v5 import observable_response_v5_errors

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
BASE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2.py"
PORTABLE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_portable.py"
PLAIN = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain.py"
PROVENANCE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain_provenance.py"
FINAL = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor_final.py"
V5 = SCRIPTS / "build_life_patterns_human_calibration_ui_v5.py"
V2_TEST = ROOT / "tests" / "unit" / "test_life_patterns_human_calibration_ui_v2.py"
CONTRACT = ROOT / "state" / "LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json"


def _load(path: Path, name: str) -> ModuleType:
    scripts_value = str(SCRIPTS)
    if scripts_value not in sys.path:
        sys.path.insert(0, scripts_value)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _patched() -> tuple[ModuleType, str, str]:
    base = _load(BASE, "lp_v5_base")
    portable = _load(PORTABLE, "lp_v5_portable")
    plain = _load(PLAIN, "lp_v5_plain")
    provenance = _load(PROVENANCE, "lp_v5_provenance")
    final = _load(FINAL, "lp_v5_final")
    v5 = _load(V5, "lp_v5_builder")
    html = base._load_html_template()
    html = portable.patch_html_for_portable_sha256(html)
    html = plain.patch_html_for_plain_human_ui(html)
    html = provenance.patch_html_for_nonredundant_provenance(html)
    final_html = final.patch_html_for_final_auditor(html)
    patched = v5.patch_html_for_v5_auditor(final_html, v5.load_public_v5_semantics())
    return v5, final_html, patched


def _helpers(html: str) -> str:
    start = html.index("// V5_EXPORT_HELPERS_START")
    end = html.index("// V5_EXPORT_HELPERS_END") + len("// V5_EXPORT_HELPERS_END")
    return html[start:end]


def _node_envelope(html: str, unit: dict[str, object], response: dict[str, object]) -> dict[str, object]:
    script = (
        _helpers(html)
        + "\nconst unit="
        + json.dumps(unit, separators=(",", ":"))
        + ";\nconst response="
        + json.dumps(response, separators=(",", ":"))
        + ";\nprocess.stdout.write(JSON.stringify(v5BuildEnvelope(unit,response)));\n"
    )
    completed = subprocess.run(
        ["node", "-e", script],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    value = json.loads(completed.stdout)
    assert isinstance(value, dict)
    return value


def _episode_unit(observable_id: str, allowed_values: list[str]) -> dict[str, object]:
    return {
        "key": f"episode:test:{observable_id}",
        "kind": "episode",
        "task": {
            "task_id": "LPDT-00000000000000000001",
            "corpus_id": "LPDC-00000000000000000001",
            "corpus_sha256": "1" * 64,
            "episode_id": "EP-001",
            "exact_source_segments": [
                {"segment_id": "SEG-1", "exact_text": "Synthetic exact source."}
            ],
        },
        "obs": {"observable_id": observable_id, "allowed_values": allowed_values},
        "resolved": {"subcodes": []},
        "ext": {"non_action_values": [], "other_specified_value": "OS"},
    }


def test_v5_patch_preserves_private_embedding_and_replaces_global_relation_task() -> None:
    v5, prior, patched = _patched()
    assert v5._embedded_fragment(patched) == v5._embedded_fragment(prior)
    assert "Which behavior does the exact source show?" in patched
    assert "Choices are separated by behavioral dimension" in patched
    assert "Does the exact source establish their chronology?" in patched
    assert "If more than one behavior is selected, how do they relate?" not in patched
    assert "Partially" not in patched
    assert "record IDs, stage IDs" not in patched


def test_v5_hybrid_ui_separates_affirmative_and_absence_components() -> None:
    _, _, patched = _patched()
    assert "data-v5-hybrid-positive" in patched
    assert "Separate absence claim" in patched
    assert "affirmative fact is retained but the combined value is not asserted" in patched
    assert "acceptance or selection of an existing option or designated default" in patched
    assert (
        "no additional alternative search during the named feasible preselection search opportunity"
        in patched
    )
    assert "silence or missing detail" in patched.lower()


def test_v5_ui_uses_claim_specific_provenance_only_when_multiple_sources_need_it() -> None:
    _, _, patched = _patched()
    assert "Which exact quote supports each selected claim?" in patched
    assert "data-v5-source-key" in patched
    assert "if(segments.length<=1||!claims.length)" in patched
    assert "source_record_id:s.segment_id" in patched


def test_v5_final_export_is_versioned_and_keeps_attestation_boundary() -> None:
    _, _, patched = _patched()
    assert "Final V5 response export" in patched
    assert "episode_responses.completed.v5.jsonl" in patched
    assert "series_responses.completed.v5.jsonl" in patched
    assert "auditor attestation" in patched.lower()
    assert "auditor_attestation.completed.json" in patched
    assert "connect-src 'none'" in patched


def test_public_v5_semantics_bind_exact_review_and_hybrid_set() -> None:
    v5, _, _ = _patched()
    public = v5.load_public_v5_semantics()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert public["accepted_review_commit"] == "ce04642146c41a7d5d94f85360572c78de887682"
    assert set(public["hybrid_value_components"]) == set(contract["hybrid_value_components"])
    assert set(contract["hybrid_value_components"]) <= set(public["absence_specs"])
    assert public["target_theory_information_used"] is False


def test_browser_export_builds_validator_clean_pure_absence_graph() -> None:
    _, _, patched = _patched()
    unit = _episode_unit("NBM-R14", ["R14-a", "R14-i"])
    response: dict[str, object] = {
        "state": "observed",
        "coded_values": ["R14-i"],
        "v5_hybrid_components": {},
        "v5_absence_gates": {
            "R14-i": {
                "awareness": "established",
                "opportunity": "established",
                "feasibility": "established",
                "established_nonoccurrence": "established",
            }
        },
        "v5_facet_stage": {},
        "v5_claim_sources": {"absence:R14-i": ["SEG-1"]},
    }
    raw = _node_envelope(patched, unit, response)
    envelope = DevelopmentEpisodeAnnotationResponseV5.model_validate(raw)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert envelope.response_graph.state == "observed"
    assert envelope.response_graph.value_assertions[0].value_id == "R14-i"
    assert envelope.response_graph.component_assertions[0].component_role == "absence"
    assert observable_response_v5_errors(
        envelope.response_graph,
        contract=contract,
        valid_source_record_ids={"SEG-1"},
    ) == ()


def test_browser_export_retains_hybrid_affirmative_when_absence_is_insufficient() -> None:
    _, _, patched = _patched()
    unit = _episode_unit("NBM-R05", ["R05-O2"])
    response: dict[str, object] = {
        "state": "observed",
        "coded_values": [],
        "v5_hybrid_components": {
            "R05-O2": {
                "affirmative_selected": True,
                "absence_gate": {
                    "awareness": "established",
                    "opportunity": "unclear",
                    "feasibility": "established",
                    "established_nonoccurrence": "unclear",
                },
            }
        },
        "v5_absence_gates": {},
        "v5_facet_stage": {},
        "v5_claim_sources": {
            "hybrid-positive:R05-O2": ["SEG-1"],
            "hybrid-absence:R05-O2": ["SEG-1"],
        },
    }
    raw = _node_envelope(patched, unit, response)
    envelope = DevelopmentEpisodeAnnotationResponseV5.model_validate(raw)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    graph = envelope.response_graph
    assert graph.state == "insufficient"
    assert graph.value_assertions == ()
    assert [row.component_role for row in graph.component_assertions] == ["affirmative", "absence"]
    assert graph.component_assertions[0].state == "observed"
    assert graph.component_assertions[1].state == "insufficient"
    assert graph.absence_conditions[0].qualified_assertion_id is None
    assert observable_response_v5_errors(
        graph,
        contract=contract,
        valid_source_record_ids={"SEG-1"},
    ) == ()


def test_v5_builder_reuses_verified_private_handoff_without_plaintext_leak(tmp_path: Path) -> None:
    helper = _load(V2_TEST, "lp_v5_v2_test_helper")
    v5 = _load(V5, "lp_v5_runtime_builder")
    handoff = tmp_path / "synthetic-private-handoff.zip"
    output = tmp_path / "synthetic-v5-ui.html"
    helper._write_synthetic_handoff(handoff)
    receipt = v5.build_human_calibration_ui_v5(handoff, output)
    html = output.read_text(encoding="utf-8")
    assert receipt["schema_version"] == "life-patterns-human-calibration-ui-build-receipt-v5"
    assert receipt["embedded_private_handoff_unchanged"] is True
    assert receipt["network_requests_required"] is False
    assert receipt["owner_usability_review_required_before_collection"] is True
    assert "PRIVATE-SYNTHETIC-EPISODE" not in html
    assert "PRIVATE-SYNTHETIC-SERIES" not in html
    assert "Final V5 response export" in html
