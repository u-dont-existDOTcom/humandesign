from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
BASE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2.py"
PORTABLE_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_portable.py"
PLAIN_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_plain.py"


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


def _patched_template() -> tuple[ModuleType, str, str]:
    base = _load(BASE_SCRIPT, "life_patterns_ui_v2_plain_base_test")
    portable = _load(PORTABLE_SCRIPT, "life_patterns_ui_v2_plain_portable_test")
    plain = _load(PLAIN_SCRIPT, "life_patterns_ui_v2_plain_test")
    original = portable.patch_html_for_portable_sha256(base._load_html_template())
    patched = plain.patch_html_for_plain_human_ui(original)
    return plain, original, patched


def test_plain_layer_covers_all_observables_and_clarifies_help_direction() -> None:
    plain, _, patched = _patched_template()

    assert set(plain.PLAIN_OBSERVABLES) == {f"NBM-R{i:02d}" for i in range(1, 23)}
    assert "This is about the narrator receiving or seeking help" in patched
    assert "The narrator offering help to someone else does not count as R16" in patched
    assert "Question for this unit" in patched
    assert "Yes — clearly shown" in patched
    assert "No — does not fit" in patched
    assert "Can't tell" in patched


def test_plain_layer_removes_ambiguous_source_and_influence_copy() -> None:
    _, _, patched = _patched_template()

    assert " Supporting</label>" not in patched
    assert "Narrator influence / precedence" not in patched
    assert "Use this quote as evidence for the behavior I selected" in patched
    assert "This quote qualifies or goes against my selected behavior" in patched
    assert "Optional: does the narrator explicitly say something influenced the behavior you selected?" in patched
    assert "Do not record a causal statement about some other action in the story" in patched


def test_plain_layer_preserves_embedded_handoff_placeholder_and_response_contract() -> None:
    plain, original, patched = _patched_template()

    assert plain._embedded_fragment(patched) == plain._embedded_fragment(original)
    assert patched.count("__EMBEDDED__") == original.count("__EMBEDDED__") == 1
    assert patched.count("__OUTER__") == original.count("__OUTER__") == 1
    for literal in (
        '"observed"',
        '"insufficient"',
        '"not_applicable"',
        "life-patterns-development-episode-annotation-response-v1",
        "life-patterns-development-series-annotation-response-v2",
        "episode_responses.completed.jsonl",
        "series_responses.completed.jsonl",
        "auditor_attestation.completed.json",
    ):
        assert literal in patched


def test_plain_layer_collapses_advanced_material_instead_of_removing_it() -> None:
    _, _, patched = _patched_template()

    assert "Formal definition and coding rules (open only if needed)" in patched
    assert "Optional uncertainty / context notes" in patched
    assert "Extra check required for a “did not act” code" in patched
    assert "Did the narrator know about the relevant option / request / problem?" in patched
    assert "Was there a real opportunity or response window?" in patched
    assert "Was the action realistically possible?" in patched


def test_plain_layer_fails_closed_on_template_drift() -> None:
    plain = _load(PLAIN_SCRIPT, "life_patterns_ui_v2_plain_drift_test")

    with pytest.raises(ValueError, match="influence constant"):
        plain.patch_html_for_plain_human_ui("<html>template drift</html>")
