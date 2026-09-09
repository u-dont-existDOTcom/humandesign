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
    base = _load(BASE_SCRIPT, "life_patterns_ui_v2_provenance_base_test")
    portable = _load(PORTABLE_SCRIPT, "life_patterns_ui_v2_provenance_portable_test")
    plain = _load(PLAIN_SCRIPT, "life_patterns_ui_v2_provenance_plain_test")
    provenance = _load(PROVENANCE_SCRIPT, "life_patterns_ui_v2_provenance_test")
    original = portable.patch_html_for_portable_sha256(base._load_html_template())
    plain_html = plain.patch_html_for_plain_human_ui(original)
    patched = provenance.patch_html_for_nonredundant_provenance(plain_html)
    return provenance, plain_html, patched


def test_single_source_observed_unit_auto_binds_provenance_without_second_question() -> None:
    _, _, patched = _patched_template()

    assert 'segments.length===1' in patched
    assert 'type="checkbox" hidden data-source="support"' in patched
    assert "No extra citation decision is needed" in patched
    assert "Use this quote as evidence for the behavior I selected" not in patched


def test_multiple_sources_keep_only_useful_provenance_choice() -> None:
    _, _, patched = _patched_template()

    assert "Which quote(s) show the behavior you selected?" in patched
    assert "This is only source bookkeeping" in patched
    assert 'data-source="support"' in patched
    assert "with several, choose only the quote(s) you relied on" in patched


def test_counterevidence_is_optional_secondary_exception_control() -> None:
    _, _, patched = _patched_template()

    assert "Optional: does any quote contain an exception or conflicting detail?" in patched
    assert "Most units need nothing here" in patched
    assert 'data-source="counter"' in patched
    assert "This quote qualifies or goes against my selected behavior" not in patched


def test_no_or_cant_tell_require_no_source_citation() -> None:
    _, _, patched = _patched_template()

    assert "No behavioral value or source citation is needed." in patched
    assert "No behavioral value or source citation is needed; use an uncertainty flag" in patched


def test_provenance_layer_preserves_embedded_handoff_and_response_contract() -> None:
    provenance, plain_html, patched = _patched_template()

    assert provenance._embedded_fragment(patched) == provenance._embedded_fragment(plain_html)
    for literal in (
        '"observed"',
        '"insufficient"',
        '"not_applicable"',
        "episode_responses.completed.jsonl",
        "series_responses.completed.jsonl",
        "auditor_attestation.completed.json",
    ):
        assert literal in patched
