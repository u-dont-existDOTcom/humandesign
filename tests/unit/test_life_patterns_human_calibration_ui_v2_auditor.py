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
AUDITOR_SCRIPT = SCRIPTS / "build_life_patterns_human_calibration_ui_v2_auditor.py"


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
    base = _load(BASE_SCRIPT, "lp_ui_auditor_base")
    portable = _load(PORTABLE_SCRIPT, "lp_ui_auditor_portable")
    plain = _load(PLAIN_SCRIPT, "lp_ui_auditor_plain")
    provenance = _load(PROVENANCE_SCRIPT, "lp_ui_auditor_provenance")
    auditor = _load(AUDITOR_SCRIPT, "lp_ui_auditor_final")
    original = provenance.patch_html_for_nonredundant_provenance(
        plain.patch_html_for_plain_human_ui(
            portable.patch_html_for_portable_sha256(base._load_html_template())
        )
    )
    patched = auditor.patch_html_for_auditor(original)
    return auditor, original, patched


def _function(html: str, name: str) -> str:
    start = html.index(f"function {name}(")
    candidates = [
        html.find("\nfunction ", start + 1),
        html.find("\nconst attestQs=", start + 1),
        html.find("\n</script>", start + 1),
    ]
    end = min(value for value in candidates if value >= 0)
    return html[start:end]


def test_embedded_handoff_and_response_contract_are_unchanged() -> None:
    auditor, original, patched = _patched()
    assert auditor._embedded_fragment(patched) == auditor._embedded_fragment(original)
    for literal in (
        '"observed"',
        '"insufficient"',
        '"not_applicable"',
        "episode_responses.completed.jsonl",
        "series_responses.completed.jsonl",
        "auditor_attestation.completed.json",
    ):
        assert literal in patched


def test_single_behavior_has_no_relation_task_and_multiple_behavior_question_is_forward() -> None:
    _, _, patched = _patched()
    observed = _function(patched, "renderObserved")
    read_form = _function(patched, "readForm")

    assert 'selected.size>1' in observed
    assert "Does the story say they happened in a particular order?" in observed
    assert "Yes — the story gives an order" in observed
    assert "Put the selected behaviors in the order they happened" in observed
    assert "If more than one behavior is selected, how do they relate?" not in observed
    assert 'vals.length===1?"single"' in read_form


def test_order_list_uses_plain_behavior_wording_not_internal_codes() -> None:
    _, _, patched = _patched()
    ordered = _function(patched, "renderOrdered")
    assert "plainBehavior" in ordered
    assert "orderlabel" in ordered
    assert "${esc(v)}</span>" not in ordered
    assert ".value code{display:none!important}" in patched


def test_optional_auxiliary_data_entry_is_removed_from_normal_human_flow() -> None:
    _, _, patched = _patched()
    observed = _function(patched, "renderObserved")
    read_form = _function(patched, "readForm")

    assert "#advancedContext{display:none!important}" in patched
    assert "episodeInfluence(u,r)" not in observed
    assert "Optional: does any quote contain an exception or conflicting detail?" not in observed
    assert 'base.counterevidence_source_segment_ids=[]' in read_form
    assert 'base.influence_relation="none_reported"' in read_form
    assert 'base.context_qualifiers=[]' in read_form
    assert 'base.missingness_flags=[]' in read_form


def test_one_quote_is_automatic_and_multiple_quote_choice_shows_quote_text() -> None:
    _, _, patched = _patched()
    sources = _function(patched, "renderSources")

    assert 'segments.length===1' in sources
    assert 'class="machineonly"' in sources
    assert "Which quote(s) did you use for this Yes answer?" in sources
    assert "quotesnippet" in sources
    assert "quoteText(s)" in sources
    assert "does any quote contain an exception" not in sources


def test_errors_are_actions_a_human_can_take_not_schema_messages() -> None:
    _, _, patched = _patched()
    validate = _function(patched, "validate")
    save = _function(patched, "saveUnit")

    assert "Choose at least one behavior from the list." in validate
    assert "Tell us whether the story gives a clear order" not in validate
    assert "Say whether the story gives a clear order." in validate
    assert "all four extra checks must be Yes" in validate
    assert "Observed requires a value relation" not in validate
    assert "frozen registry" not in validate
    assert "One thing needs fixing before this can be saved" in save


def test_series_ui_asks_required_human_questions_and_derives_machine_basis() -> None:
    _, _, patched = _patched()
    series = _function(patched, "seriesFields")
    read_form = _function(patched, "readForm")

    assert "How often does the narrator say this behavior happens?" in series
    assert "Does the narrator report exceptions or limits?" in series
    assert "Optional count/rate" not in series
    assert '"bounded_rate_or_count_self_report"' in read_form
    assert '"generalized_self_report"' in read_form
    assert "recurrence_scope_description=null" in read_form
