from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
BASE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2.py"
PORTABLE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_portable.py"
PLAIN = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain.py"
PROVENANCE = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain_provenance.py"
FINAL_V2 = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor_final.py"
V5 = SCRIPTS / "build_life_patterns_human_calibration_ui_v5.py"
FINAL_V5 = SCRIPTS / "build_life_patterns_human_calibration_ui_v5_final.py"
V2_TEST = ROOT / "tests" / "unit" / "test_life_patterns_human_calibration_ui_v2.py"


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


def _patched() -> tuple[ModuleType, ModuleType, str, str]:
    base = _load(BASE, "lp_v5f_base")
    portable = _load(PORTABLE, "lp_v5f_portable")
    plain = _load(PLAIN, "lp_v5f_plain")
    provenance = _load(PROVENANCE, "lp_v5f_provenance")
    final_v2 = _load(FINAL_V2, "lp_v5f_final_v2")
    v5 = _load(V5, "lp_v5f_v5")
    final_v5 = _load(FINAL_V5, "lp_v5f_final")
    html = base._load_html_template()
    html = portable.patch_html_for_portable_sha256(html)
    html = plain.patch_html_for_plain_human_ui(html)
    html = provenance.patch_html_for_nonredundant_provenance(html)
    html = final_v2.patch_html_for_final_auditor(html)
    v5_html = v5.patch_html_for_v5_auditor(html, v5.load_public_v5_semantics())
    final_html = final_v5.patch_html_for_v5_final_fallbacks(v5_html)
    return v5, final_v5, v5_html, final_html


def test_final_v5_uses_exact_fallback_labels_without_touching_private_embedding() -> None:
    v5, _, prior, final = _patched()
    assert v5._embedded_fragment(final) == v5._embedded_fragment(prior)
    assert "Doesn't apply to this story" in final
    assert "Not enough information" in final
    assert "No — does not fit" not in final
    assert ">Can't tell<" not in final
    assert "non-mention is not enough" in final


def test_final_v5_keeps_v5_export_and_human_first_controls() -> None:
    _, _, _, final = _patched()
    assert "Final V5 response export" in final
    assert "episode_responses.completed.v5.jsonl" in final
    assert "Which exact quote supports each selected claim?" in final
    assert "Does the exact source establish their chronology?" in final
    assert "data-v5-hybrid-positive" in final


def test_final_v5_runtime_builder_keeps_private_handoff_embedded_and_offline(tmp_path: Path) -> None:
    helper = _load(V2_TEST, "lp_v5f_v2_test_helper")
    final_v5 = _load(FINAL_V5, "lp_v5f_runtime")
    handoff = tmp_path / "private.zip"
    output = tmp_path / "v5-final.html"
    helper._write_synthetic_handoff(handoff)
    receipt = final_v5.build_final_human_calibration_ui_v5(handoff, output)
    html = output.read_text(encoding="utf-8")
    assert receipt["schema_version"] == "life-patterns-human-calibration-ui-final-build-receipt-v5"
    assert receipt["embedded_private_handoff_unchanged"] is True
    assert receipt["network_requests_required"] is False
    assert receipt["owner_usability_review_required_before_collection"] is True
    assert receipt["not_applicable_label"] == "Doesn't apply to this story"
    assert receipt["insufficient_label"] == "Not enough information"
    assert "PRIVATE-SYNTHETIC-EPISODE" not in html
    assert "PRIVATE-SYNTHETIC-SERIES" not in html
