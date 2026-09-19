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
FINAL = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor_final.py"
DIRECT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_direct_choice.py"


def _load(path: Path, name: str) -> ModuleType:
    scripts = str(SCRIPTS)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _patched() -> tuple[ModuleType, str, str]:
    base = _load(BASE, "lp_direct_base")
    portable = _load(PORTABLE, "lp_direct_portable")
    plain = _load(PLAIN, "lp_direct_plain")
    provenance = _load(PROVENANCE, "lp_direct_provenance")
    final = _load(FINAL, "lp_direct_final")
    direct = _load(DIRECT, "lp_direct_choice")
    original = final.patch_html_for_final_auditor(
        provenance.patch_html_for_nonredundant_provenance(
            plain.patch_html_for_plain_human_ui(
                portable.patch_html_for_portable_sha256(base._load_html_template())
            )
        )
    )
    patched = direct.patch_html_for_direct_behavior_choice(original)
    return direct, original, patched


def _function(html: str, name: str) -> str:
    start = html.index(f"function {name}(")
    candidates = [
        html.find("\nfunction ", start + 1),
        html.find("\nconst attestQs=", start + 1),
        html.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return html[start:end]


def test_direct_choice_preserves_embedded_handoff() -> None:
    direct, original, patched = _patched()
    assert direct._embedded_fragment(patched) == direct._embedded_fragment(original)


def test_behavior_choices_are_visible_before_machine_state() -> None:
    _, _, patched = _patched()
    states = _function(patched, "renderStates")
    assert "Which behavior or behaviors does the exact source clearly show?" in states
    assert "plainBehavior" in states
    assert "Doesn't apply to this story" in states
    assert "Not enough information" in states
    assert "Enough information to code" not in states
    assert "Can this unit be coded for the question above?" not in states


def test_machine_observed_state_is_derived_from_direct_behavior_selection() -> None:
    _, _, patched = _patched()
    read_form = _function(patched, "readForm")
    assert 'base.state=vals.length?"observed":fallback' in read_form
    assert 'input[name="stateFallback"]:checked' in read_form
    assert 'vals.length===1?"single"' in read_form


def test_partial_fit_is_not_forced_into_generic_fourth_state() -> None:
    _, _, patched = _patched()
    states = _function(patched, "renderStates")
    assert "Some pieces may fit" in states
    assert "too incomplete or unclear to choose a behavior reliably" in states
    assert "Partially" not in states


def test_conditional_extras_remain_after_direct_behavior_choice() -> None:
    _, _, patched = _patched()
    observed = _function(patched, "renderObserved")
    assert "selected.size>1" in observed
    assert "Does the story say they happened in a particular order?" in observed
    assert "seriesFields(r)" in observed
    assert "Extra check for the “did not act” behavior you selected" in observed
    assert "Describe the behavior that is not listed above" in observed


def test_validation_copy_is_actionable_for_no_primary_choice() -> None:
    _, _, patched = _patched()
    validate = _function(patched, "validate")
    assert "Select at least one behavior" in validate
    assert "Doesn't apply to this story / Not enough information" in validate
