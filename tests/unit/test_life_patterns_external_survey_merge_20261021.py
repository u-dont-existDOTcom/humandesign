"""Personal survey provenance, questionnaire design and future-outcome safeguards."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-external-questionnaire-merge-20261021"
PREVIOUS = ROOT / "tasks/life-patterns-extra-natal-audit-20261018"
INSTRUMENT = TASK / "LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json"
AUDIT = TASK / "EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json"


def import_module(name: str):
    p = TASK / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), p)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MERGER = import_module("merge_owner_personal_results.py")
BUILDER = import_module("build_adaptive_survey_v3.py")


def fixture_baseline() -> dict:
    names = [
        "my-life-patterns-v3-3-role-entry.json",
        "Life-Patterns-FINAL-Primary-84-Turns-2026-10-09.json",
        "Life-Patterns-FINAL-CF003-3-Turns-2026-10-09.json",
    ]
    import hashlib

    docs = []
    for name in names:
        original = json.dumps({"schema": "SYNTHETIC", "answers": ["test only"]})
        docs.append(
            {
                "filename": name,
                "text": original,
                "sha256": hashlib.sha256(original.encode()).hexdigest(),
            }
        )
    return {
        "schema": MERGER.OLD_SCHEMA,
        "historical_original_sources": docs,
        "experience_addendum": {
            "schema": "life-patterns-experience-pilot-answers-v1",
            "responses": [{"question_id": f"EM{i:02d}", "state": "ANSWERED"} for i in range(1, 9)],
        },
    }


def fixture_external(source_hash: str = "a" * 64) -> dict:
    entries = []
    for i in range(1, 32):
        if i >= 27:
            status, marked = MERGER.PENDING, None
        elif i in [2, 3, 7, 21, 25]:
            status, marked = MERGER.MISSING, "Missing / unclear / declined"
        else:
            status, marked = MERGER.MARKED, "Synthetic option"
        entries.append(
            {
                "id": f"Q{i:02d}",
                "question": f"Q{i:02d} Synthetic question.",
                "reference_window": "Reference window: Synthetic without DOB.",
                "marked_choice": marked,
                "state": status,
                "verbatim_user_evidence_field": "Evidence or clarification (optional): ",
                "extracted_note": "Synthetic respondent note." if i == 21 else "",
            }
        )
    return {
        "schema": MERGER.ADD_SCHEMA,
        "source_odg_sha256": source_hash,
        "question_count": 31,
        "state_counts": {
            "marked_responses": 26,
            "marked_other_than_missing": 21,
            "marked_missing_or_unclear": 5,
            "future_unmarked": 5,
        },
        "responses": entries,
    }


def test_merge_losslessly_preserves_original_sources_and_unknown_future(tmp_path):
    baseline = fixture_baseline()
    external = fixture_external()
    original = tmp_path / "original.json"
    new = tmp_path / "external.json"
    output = tmp_path / "out.json"
    original.write_text(json.dumps(baseline, ensure_ascii=False))
    new.write_text(json.dumps(external, ensure_ascii=False))
    digest_before = MERGER.sha(original.read_bytes())
    receipt = MERGER.build(original, new, output, expected_source_sha="a" * 64)
    joined = json.loads(output.read_bytes())
    assert receipt["counts"] == {MERGER.MARKED: 21, MERGER.MISSING: 5, MERGER.PENDING: 5}
    assert joined["baseline"] == baseline
    assert joined["external_blinded_questionnaire_addendum"] == external
    assert joined["preceding_complete_survey_sha256"] == digest_before
    assert MERGER.sha(original.read_bytes()) == digest_before
    assert joined["preservation"]["excludes_other_participant_records"]
    assert all(
        x["marked_choice"] is None
        for x in joined["external_blinded_questionnaire_addendum"]["responses"][26:]
    )
    assert (
        joined["external_blinded_questionnaire_addendum"]["responses"][20]["extracted_note"]
        == "Synthetic respondent note."
    )
    assert output.stat().st_mode & 0o777 == 0o600
    with pytest.raises(FileExistsError):
        MERGER.build(original, new, output, expected_source_sha="a" * 64)


@pytest.mark.parametrize(
    "mutant",
    [
        "missing_source",
        "recode_missing",
        "future_marked",
        "drop_answer",
        "duplicate_id",
        "wrong_sha",
    ],
)
def test_external_answer_transformer_rejects_source_mutants(mutant):
    x = fixture_external()
    if mutant == "missing_source":
        x["responses"][0].pop("question")
    elif mutant == "recode_missing":
        x["responses"][1]["state"] = MERGER.MARKED
    elif mutant == "future_marked":
        x["responses"][26]["marked_choice"] = "No"
    elif mutant == "drop_answer":
        x["responses"].pop(9)
    elif mutant == "duplicate_id":
        x["responses"][1]["id"] = "Q01"
    elif mutant == "wrong_sha":
        x["source_odg_sha256"] = "b" * 64
    with pytest.raises(ValueError):
        MERGER.check_external_addendum(x, "a" * 64)


def test_old_source_hash_mutation_rejected():
    older = fixture_baseline()
    older["historical_original_sources"][0]["text"] += " mutation"
    with pytest.raises(ValueError):
        MERGER.audit_original_sources(older)


def test_all_thirty_one_external_items_are_reviewed_and_future_is_not_a_trait():
    review = json.loads(AUDIT.read_text())
    assert review["external_questions_reviewed"] == 31
    assert len(review["decisions"]) == 31
    assert [x["source_question_id"] for x in review["decisions"]] == [
        f"Q{i:02}" for i in range(1, 32)
    ]
    by_id = {x["source_question_id"]: x for x in review["decisions"]}
    assert all(by_id[f"Q{i:02}"]["disposition"] == "FUTURE_ONLY" for i in range(27, 32))
    assert by_id["Q21"]["disposition"] == "REJECT_FORCED_CHOICE"
    assert by_id["Q08"]["disposition"] == "REJECT_PERSONALITY_PROXY"
    assert by_id["Q24"]["disposition"] == "DEPENDENT_EVENT"
    assert by_id["Q25"]["disposition"] == "DEPENDENT_EVENT"
    assert review["source_frozen_json_available_and_verified"] is False
    assert review["participant_answers_retrospective_development_only"]


def test_original_twenty_three_questions_preserved_verbatim_with_optional_delta():
    old = json.loads((PREVIOUS / "TWENTY-THREE-OPTIONAL-QUESTIONS-v2.json").read_text())
    new = json.loads(INSTRUMENT.read_text())
    assert len(new["questions"]) == len(old["questions"]) == 23
    for original, extra in zip(old["questions"], new["questions"], strict=True):
        assert extra["id"] == original["id"]
        assert extra["question"] == original["question"]
        assert extra["optional_followup"] == original["optional_followup"]
        assert extra["answer_dimensions"] == original["answer_dimensions"]
        assert extra["already_live"] == original["already_live"] is False
        assert "CONTEXT_DEPENDENT" in extra["response_state_options"]
        assert "NO_OPPORTUNITIES" in extra["response_state_options"]
        assert extra["answer_capture"]["ability_and_opportunity_separate"]
    assert new["max_base_optional_topics_per_session"] == 5
    assert new["max_additional_conditional_probes_per_session"] == 2
    assert len(new["optional_microprobes"]) == 7
    assert new["external_future_outcome_ids_excluded"] == [f"Q{i:02}" for i in range(27, 32)]
    assert new["status"] == "DEVELOPMENT_OPT_IN_NO_LIVE_OR_CHART_SCORING"


def test_builder_matches_committed_version_exactly_and_lacks_private_answer_text():
    expected_bank = json.loads(INSTRUMENT.read_text())
    expected_audit = json.loads(AUDIT.read_text())
    bank, review = BUILDER.build()
    assert bank == expected_bank
    assert review == expected_audit
    for f in (INSTRUMENT, AUDIT, TASK / "CONDITIONAL-MICROPROBES-v1.json"):
        raw = f.read_text()
        for forbidden in (
            "SYNTHETIC RESPONDENT PRIVATE NAME",
            "ANOTHER PARTICIPANT PRIVATE ID",
            "birthplace",
            "Reference window:",
            "verbatim_user_evidence_field",
            "extracted_note",
            "/mnt/hdd/home/",
        ):
            assert forbidden not in raw
    assert not any(row.get("new_chart_score") is not None for row in review["decisions"])


def test_typical_preference_and_observed_role_keep_different_dimensions():
    bank = json.loads(INSTRUMENT.read_text())
    probes = {x["id"]: x for x in bank["optional_microprobes"]}
    lead = probes["EP-LEADERSHIP-HISTORY"]
    assert "preferred_vs_actual" in lead["dimensions"]
    assert "formal_informal_and_pay_separate" in lead["dimensions"]
    partner = probes["EP-PARTNER-PRIORITIES"]
    assert "ordering_or_ties_optional" in partner["dimensions"]
    goals = probes["EP-PROJECT-FOLLOWTHROUGH"]
    assert "started_projects_approximate_opportunities" in goals["dimensions"]
    assert "FUTURE_PENDING" in bank["evidence_state_codes"]
