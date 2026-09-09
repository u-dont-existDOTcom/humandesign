from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
BASE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2.py"
PORTABLE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_portable.py"
PLAIN_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain.py"
PROVENANCE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain_provenance.py"
FINAL_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor_final.py"
STATE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor_state_labels.py"


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
    base = _load(BASE_SCRIPT, "lp_state_labels_base")
    portable = _load(PORTABLE_SCRIPT, "lp_state_labels_portable")
    plain = _load(PLAIN_SCRIPT, "lp_state_labels_plain")
    provenance = _load(PROVENANCE_SCRIPT, "lp_state_labels_provenance")
    final = _load(FINAL_SCRIPT, "lp_state_labels_final")
    states = _load(STATE_SCRIPT, "lp_state_labels")
    original = final.patch_html_for_final_auditor(
        provenance.patch_html_for_nonredundant_provenance(
            plain.patch_html_for_plain_human_ui(
                portable.patch_html_for_portable_sha256(base._load_html_template())
            )
        )
    )
    patched = states.patch_html_for_evidence_state_clarity(original)
    return states, original, patched


def _function(html: str, name: str) -> str:
    start = html.index(f"function {name}(")
    candidates = [
        html.find("\nfunction ", start + 1),
        html.find("\nconst attestQs=", start + 1),
        html.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return html[start:end]


def test_states_are_presented_as_coding_conditions_not_fit_scale() -> None:
    _, _, patched = _patched()
    states = _function(patched, "renderStates")

    assert "Can this unit be coded for the question above?" in states
    assert "Enough information to code" in states
    assert "Doesn't apply" in states
    assert "Not enough information" in states
    assert "This is not a fit scale" in states
    assert "If it partly fits" in states
    assert "Yes — clearly shown" not in states
    assert "No — does not fit" not in states
    assert "Can't tell" not in states


def test_partial_evidence_is_explained_as_insufficient_when_not_codeable() -> None:
    _, _, patched = _patched()
    semantics = _function(patched, "updateStateSemantics")

    assert "only part of the needed information is present" in semantics
    assert "too unclear to choose a behavior reliably" in semantics


def test_state_label_patch_preserves_embedded_handoff_and_contract_literals() -> None:
    states, original, patched = _patched()

    assert states._embedded_fragment(patched) == states._embedded_fragment(original)
    for literal in (
        '"observed"',
        '"insufficient"',
        '"not_applicable"',
        "episode_responses.completed.jsonl",
        "series_responses.completed.jsonl",
        "auditor_attestation.completed.json",
    ):
        assert literal in patched


def test_validation_copy_uses_same_human_state_meanings() -> None:
    _, _, patched = _patched()
    validate = _function(patched, "validate")

    assert "Choose Enough information to code, Doesn't apply, or Not enough information." in validate
    assert "Choose Yes, No, or Can't tell." not in validate
