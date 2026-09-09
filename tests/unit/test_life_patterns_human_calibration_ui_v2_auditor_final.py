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
    base = _load(BASE_SCRIPT, "lp_final_auditor_base")
    portable = _load(PORTABLE_SCRIPT, "lp_final_auditor_portable")
    plain = _load(PLAIN_SCRIPT, "lp_final_auditor_plain")
    provenance = _load(PROVENANCE_SCRIPT, "lp_final_auditor_provenance")
    final = _load(FINAL_SCRIPT, "lp_final_auditor")
    original = provenance.patch_html_for_nonredundant_provenance(
        plain.patch_html_for_plain_human_ui(
            portable.patch_html_for_portable_sha256(base._load_html_template())
        )
    )
    patched = final.patch_html_for_final_auditor(original)
    return final, original, patched


def _function(html: str, name: str) -> str:
    start = html.index(f"function {name}(")
    candidates = [
        html.find("\nfunction ", start + 1),
        html.find("\nconst attestQs=", start + 1),
        html.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return html[start:end]


def test_final_auditor_preserves_embedded_handoff() -> None:
    final, original, patched = _patched()
    assert final._embedded_fragment(patched) == final._embedded_fragment(original)
    assert "episode_responses.completed.jsonl" in patched
    assert "series_responses.completed.jsonl" in patched
    assert "auditor_attestation.completed.json" in patched


def test_single_behavior_relation_is_automatic_and_multiple_relation_is_conditional() -> None:
    _, _, patched = _patched()
    observed = _function(patched, "renderObserved")
    read_form = _function(patched, "readForm")
    assert "Does the story say they happened in a particular order?" in observed
    assert "Yes — the story gives an order" in observed
    assert "Put the selected behaviors in the order they happened" in observed
    assert 'selected.size>1' in observed
    assert 'vals.length===1?"single"' in read_form
    assert "If more than one behavior is selected, how do they relate?" not in observed


def test_ordering_shows_plain_behavior_labels_not_codes() -> None:
    _, _, patched = _patched()
    ordered = _function(patched, "renderOrdered")
    assert "plainBehavior" in ordered
    assert "orderlabel" in ordered
    assert ".value code{display:none!important}" in patched


def test_optional_auxiliary_fields_are_not_human_tasks() -> None:
    _, _, patched = _patched()
    observed = _function(patched, "renderObserved")
    read_form = _function(patched, "readForm")
    assert "#advancedContext{display:none!important}" in patched
    assert "episodeInfluence(u,r)" not in observed
    assert "does any quote contain an exception" not in observed
    assert 'base.counterevidence_source_segment_ids=[]' in read_form
    assert 'base.influence_relation="none_reported"' in read_form
    assert 'base.context_qualifiers=[]' in read_form
    assert 'base.missingness_flags=[]' in read_form


def test_source_provenance_is_automatic_for_one_quote_and_readable_for_many() -> None:
    _, _, patched = _patched()
    sources = _function(patched, "renderSources")
    assert 'segments.length===1' in sources
    assert 'class="machineonly"' in sources
    assert "Which quote(s) did you use for this Yes answer?" in sources
    assert "quotesnippet" in sources
    assert "quoteText(s)" in sources
    assert "Use this quote as evidence for the behavior I selected" not in sources


def test_validation_copy_tells_human_what_to_do() -> None:
    _, _, patched = _patched()
    validate = _function(patched, "validate")
    save = _function(patched, "saveUnit")
    assert "Choose at least one behavior from the list." in validate
    assert "Say whether the story gives a clear order." in validate
    assert "all four extra checks must be Yes" in validate
    assert "Observed requires a value relation" not in validate
    assert "frozen registry" not in validate
    assert "One thing needs fixing before this can be saved" in save


def test_series_machine_basis_is_derived_instead_of_asked_as_optional_work() -> None:
    _, _, patched = _patched()
    series = _function(patched, "seriesFields")
    read_form = _function(patched, "readForm")
    assert "How often does the narrator say this behavior happens?" in series
    assert "Does the narrator report exceptions or limits?" in series
    assert "Optional count/rate" not in series
    assert '"bounded_rate_or_count_self_report"' in read_form
    assert '"generalized_self_report"' in read_form
    assert "recurrence_scope_description=null" in read_form
