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
FINAL = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_final.py"


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
    base = _load(BASE, "lp_final_base")
    portable = _load(PORTABLE, "lp_final_portable")
    plain = _load(PLAIN, "lp_final_plain")
    provenance = _load(PROVENANCE, "lp_final_provenance")
    final = _load(FINAL, "lp_final")
    html = base._load_html_template()
    html = portable.patch_html_for_portable_sha256(html)
    html = plain.patch_html_for_plain_human_ui(html)
    prior = provenance.patch_html_for_nonredundant_provenance(html)
    patched = final.patch_html_for_final_human_ui(prior)
    return final, prior, patched


def test_relation_control_is_hidden_for_single_value_and_only_asks_when_multiple() -> None:
    _, _, patched = _patched()

    assert "If more than one behavior is selected, how do they relate?" not in patched
    assert 'const relationHidden=selected.size<=1?" hidden":""' in patched
    assert 'id="relationRow"' in patched
    assert 'option value="single" hidden' in patched
    assert "You selected more than one behavior. Did they happen in a known order?" in patched
    assert "Yes — they happened in this order" in patched
    assert "No / the order is not established" in patched


def test_relation_control_reacts_to_value_count_without_new_measurement_semantics() -> None:
    _, _, patched = _patched()

    assert 'if(vals.length===1){vr.value="single";row.classList.add("hidden")}' in patched
    assert 'else if(vals.length>1){if(vr.value==="single")vr.value="";row.classList.remove("hidden")}' in patched
    assert 'const rel=$("valueRelation")?.value||(vals.length===1?"single":null);' in patched


def test_source_segment_ids_remain_machine_values_but_are_not_human_labels() -> None:
    _, _, patched = _patched()

    assert 'value="${esc(s.segment_id)}"' in patched
    assert 'class="quotelabel"' in patched
    assert 'class="quotesnippet"' in patched
    assert '<b>${esc(s.segment_id)}</b>' not in patched
    assert '${esc(s.segment_id)}</label>' not in patched


def test_internal_behavior_codes_are_hidden_from_human_view() -> None:
    _, _, patched = _patched()

    assert ".value code{display:none!important}" in patched
    assert "requires extra evidence check" in patched
    assert "no-action rule" not in patched


def test_final_layer_preserves_embedded_private_handoff_exactly() -> None:
    final, prior, patched = _patched()

    assert final._embedded_fragment(patched) == final._embedded_fragment(prior)
    for literal in (
        '"observed"',
        '"insufficient"',
        '"not_applicable"',
        "episode_responses.completed.jsonl",
        "series_responses.completed.jsonl",
        "auditor_attestation.completed.json",
    ):
        assert literal in patched
