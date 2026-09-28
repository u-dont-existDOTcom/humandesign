import csv
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from participant.domain import export_record, import_record, new_state
from test_participant import authority

ROOT = Path(__file__).resolve().parents[3]
VOICE = ROOT / "reference/custom_gpt/life_patterns_voice_interviewer_v2.md"
ANALYZER_PATH = ROOT / "apps/life-patterns-participant/scripts/analyze_collection_modes.py"
CODEX_PROBE = ROOT / "apps/life-patterns-participant/scripts/codex_dev_probe.py"


def load_script(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ANALYZER = load_script(ANALYZER_PATH, "collection_mode_analyzer")


def synthetic_record(mode: str, answer: str) -> dict:
    instrument = authority()
    state = new_state("instrument-test", "openai-gpt-56-sol", "xhigh")
    state.update(
        session_id="synthetic",
        revision=0,
        consent=True,
        phase="ready",
    )
    imported = {
        "turns": [
            {
                "question_text": "Synthetic question?",
                "answer_text": answer,
                "conditions": ["synthetic condition"],
            }
        ]
    }
    state["phase"] = "consent"
    state["consent"] = None
    import_record(
        state,
        imported,
        "edited_response_record",
        instrument,
        mode,
    )
    state["consent"] = True
    state["phase"] = "ready"
    state["calls"] = [
        {
            "provider": "synthetic",
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "request_chars": 400,
        }
    ]
    return export_record(state, instrument)


def test_voice_interviewer_fits_builder_budget_and_has_accuracy_guards():
    text = VOICE.read_text(encoding="utf-8")
    strict_count = len(text) + text.count("\n")
    assert strict_count < 8000
    required = (
        "long spoken answers are fine",
        "Do not claim access to\nthe original audio or perfect transcription",
        "bank is a menu, not a quota",
        "Put only their exact transcript words in quotation marks",
        "Say they never mentioned something only after checking the complete conversation",
        "neither defend your prior\n  reading nor adopt a new claim they did not say",
        "ChatGPT account-data\nExport",
        "collection_mode",
    )
    for phrase in required:
        assert phrase in text


@pytest.mark.parametrize(
    "mode",
    ["railway_text", "chatgpt_voice", "chatgpt_text", "mixed", "unknown"],
)
def test_collection_mode_is_preserved_in_import_and_export(mode):
    record = synthetic_record(mode, "A synthetic answer.")
    assert record["collection_mode"] == mode
    assert record["source_records"][0]["source_mode"] == mode


def test_unknown_collection_mode_is_rejected():
    instrument = authority()
    state = new_state("instrument-test", "m", "x")
    with pytest.raises(ValueError):
        import_record(
            state,
            {"turns": [{"answer_text": "synthetic"}]},
            "edited_response_record",
            instrument,
            "guessed_voice",
        )


def test_collection_mode_analyzer_reports_richness_and_cost_fields(tmp_path):
    voice = synthetic_record(
        "chatgpt_voice",
        "This is a somewhat longer synthetic spoken-style answer with several words.",
    )
    typed = synthetic_record("railway_text", "Short synthetic answer.")
    rows = [
        ANALYZER.summarize(tmp_path / "voice.json", voice),
        ANALYZER.summarize(tmp_path / "typed.json", typed),
    ]
    assert rows[0]["collection_mode"] == "chatgpt_voice"
    assert rows[1]["collection_mode"] == "railway_text"
    assert rows[0]["participant_words_total"] > rows[1]["participant_words_total"]
    grouped = ANALYZER.aggregate(rows)
    assert grouped["chatgpt_voice"]["sessions"] == 1
    assert grouped["railway_text"]["sessions"] == 1


def test_collection_mode_analyzer_cli_writes_csv_and_json(tmp_path):
    inputs = []
    for name, mode in (("voice", "chatgpt_voice"), ("typed", "railway_text")):
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(synthetic_record(mode, f"{name} answer")), encoding="utf-8")
        inputs.append(path)
    csv_path = tmp_path / "comparison.csv"
    json_path = tmp_path / "comparison.json"
    subprocess.run(
        [
            "python3",
            str(ANALYZER_PATH),
            *map(str, inputs),
            "--csv",
            str(csv_path),
            "--json",
            str(json_path),
            "--input-usd-per-million",
            "1.0",
            "--output-usd-per-million",
            "2.0",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    report = json.loads(json_path.read_text())
    assert len(rows) == 2
    assert set(report["by_collection_mode"]) == {"chatgpt_voice", "railway_text"}
    assert all("estimated_model_usd" in row for row in rows)


def test_codex_probe_dry_run_does_not_invoke_model(tmp_path):
    context = tmp_path / "context.json"
    output = tmp_path / "output.json"
    context.write_text(
        json.dumps(
            {
                "turns": [],
                "pending_turn_ids": [],
                "import_bulk_review": False,
                "review_only": False,
                "existing_evidence": [],
                "candidate_routes": [],
                "candidate_evidence_guide": [],
            }
        )
    )
    result = subprocess.run(
        [
            sys.executable,
            str(CODEX_PROBE),
            "--stage",
            "plan",
            "--context",
            str(context),
            "--output",
            str(output),
            "--dry-run",
        ],
        env=dict(
            os.environ,
            PYTHONPATH=str(ROOT / "apps/life-patterns-participant"),
        ),
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = json.loads(result.stdout)
    assert receipt["paid_api"] is False
    assert receipt["production_backend"] is False
    assert receipt["prompt_chars"] > receipt["context_chars"]
    assert not output.exists()


def test_voice_manifest_hashes_and_budget():
    import hashlib

    manifest = json.loads(
        (ROOT / "reference/custom_gpt/life_patterns_voice_gpt_manifest_v2.json").read_text()
    )
    instructions = ROOT / manifest["instructions"]["path"]
    assert (
        hashlib.sha256(instructions.read_bytes()).hexdigest() == manifest["instructions"]["sha256"]
    )
    assert manifest["instructions"]["strict_linebreak_count"] < 8000
    for item in manifest["knowledge_files"]:
        source = ROOT / item["path"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == item["sha256"]
    assert manifest["birth_or_chart_material_in_bundle"] is False


def test_record_collection_mode_is_used_when_import_mode_unknown():
    instrument = authority()
    state = new_state("instrument-test", "m", "x")
    import_record(
        state,
        {
            "collection_mode": "chatgpt_voice",
            "turns": [{"question_text": "Q", "answer_text": "A"}],
        },
        "prior_json",
        instrument,
        "unknown",
    )
    assert state["collection_mode"] == "chatgpt_voice"
    assert state["source_records"][0]["source_mode"] == "chatgpt_voice"


def test_runtime_semantic_prompts_carry_core_accuracy_checks():
    from participant.engine import PLANNER, REVIEWER

    joined = PLANNER + "\n" + REVIEWER
    for phrase in (
        "exact source",
        "motive",
        "backstory",
        "absence of mention",
        "participant corrections",
        "coverage quota",
    ):
        assert phrase.lower() in joined.lower()
    assert "source_quotes must be exact contiguous substrings" in PLANNER
    assert "compact global admission authority" in REVIEWER


def test_voice_interviewer_records_retrospective_preference():
    text = VOICE.read_text(encoding="utf-8")
    assert "earlier-life comparison questions are welcome" in text
    assert "retrospective_questions_welcome" in text


def test_nested_collection_preferences_survive_reimport():
    instrument = authority()
    state = new_state("instrument-test", "m", "x")
    import_record(
        state,
        {
            "collection_mode": "chatgpt_voice",
            "collection_preferences": {"retrospective_questions_welcome": True},
            "turns": [{"question_text": "Q", "answer_text": "A"}],
        },
        "prior_json",
        instrument,
        "unknown",
    )
    assert state["collection_mode"] == "chatgpt_voice"
    assert state["collection_preferences"]["retrospective_questions_welcome"] is True


def test_chatgpt_evidence_is_preserved_as_source_but_not_admitted_on_import():
    instrument = authority()
    state = new_state("instrument-test", "m", "x")
    import_record(
        state,
        {
            "collection_mode": "chatgpt_voice",
            "source_fidelity": "model_export_of_visible_chat_not_independently_verified",
            "evidence_authority": "chatgpt_collector_unverified",
            "turns": [{"question_text": "Q", "answer_text": "A"}],
            "neutral_evidence": [{"evidence_id": "collector-e1", "observation": "unverified"}],
        },
        "prior_json",
        instrument,
        "unknown",
    )
    assert state["evidence"] == []
    source = state["source_records"][0]
    assert source["upstream_evidence_authority"] == "chatgpt_collector_unverified"
    assert source["upstream_evidence_admitted"] is False
    assert source["source_fidelity"] == "model_export_of_visible_chat_not_independently_verified"


def test_analyzer_separates_collector_and_railway_evidence_authority(tmp_path):
    collector = {
        "collection_mode": "chatgpt_voice",
        "evidence_authority": "chatgpt_collector_unverified",
        "turns": [{"turn_source": "import-1", "answer_text": "Synthetic voice answer"}],
        "neutral_evidence": [
            {
                "evidence_id": "u1",
                "candidate_facet_ids": ["D01.approach"],
                "review_status": "collector_only",
                "conditions": [],
            }
        ],
    }
    row = ANALYZER.summarize(tmp_path / "collector.json", collector)
    assert row["collector_unverified_evidence_items"] == 1
    assert row["railway_admitted_evidence_items"] is None

    railway = synthetic_record("chatgpt_voice", "Synthetic imported answer")
    railway["neutral_evidence"] = [
        {
            "evidence_id": "r1",
            "candidate_facet_ids": ["D01.approach"],
            "review_status": "independent_semantic_admission_passed",
            "conditions": [],
        }
    ]
    row = ANALYZER.summarize(tmp_path / "railway.json", railway)
    assert row["evidence_authority"] == "railway_independent_semantic_admission"
    assert row["railway_admitted_evidence_items"] == 1
    assert row["collector_unverified_evidence_items"] is None
