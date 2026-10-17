"""Survey-first optional experience pilot: admission, distinctions, and offline build."""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-experience-pilot-20261017"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, TASK / (name + ".py"))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROUTER = load("pilot_router")


def test_optional_pilot_is_separate_from_existing_instruments():
    bank = ROUTER.instrument()
    assert bank["status"] == "DEVELOPMENT_OPTIONAL_NOT_LIVE_NOT_SCORED"
    assert bank["scoring"]["allowed"] is False
    assert bank["scoring"]["compare_to_chart"] is False
    assert bank["scope"].startswith("Independent opt-in")
    ids = [item["id"] for item in bank["items"]]
    assert ids == ["EM01", "EM02", "EM03", "EM04", "EM05", "EM06", "EM07", "EM08"]
    assert bank["prompt_order"] == ["EM01", "EM03", "EM04", "EM08"]
    assert bank["other_prompt_order"] == ["EM02", "EM05", "EM06", "EM07"]
    assert len(set(ids)) == 8
    assert "No answer to this part" in [x[1] for x in bank["meaning_options"]]
    # Existing live guide and historical bank remain independent sources.
    assert (ROOT / bank["legacy_sources"][0]).exists()
    assert (ROOT / bank["legacy_sources"][1]).exists()
    assert (ROOT / bank["legacy_sources"][2]).exists()
    assert not any("chart" in item["question"].lower() for item in bank["items"])


def test_prior_source_only_skips_when_reference_is_present():
    blocked = ROUTER.plan_questions(consent=False, requested_optional_ids=["EM06"])
    assert blocked["queue"] == []
    assert len(blocked["not_asked"]) == 8
    initial = ROUTER.plan_questions(consent=True)
    assert initial["queue"] == ["EM01", "EM03", "EM04", "EM08"]
    assert len(initial["not_asked"]) == 4
    with_source = ROUTER.plan_questions(
        consent=True,
        requested_optional_ids=["EM02", "EM07"],
        covered_sources={
            "EM01": "previous interview Q41",
            "EM02": "  ",
            "EM07": "explicit response #8",
        },
    )
    assert with_source["queue"] == ["EM03", "EM04", "EM08", "EM02"]
    assert with_source["covered"] == {
        "EM01": "previous interview Q41",
        "EM07": "explicit response #8",
    }
    assert "EM06" in with_source["not_asked"]
    with pytest.raises(ValueError):
        ROUTER.plan_questions(consent=True, requested_optional_ids=["EM01"])
    with pytest.raises(ValueError):
        ROUTER.plan_questions(consent=True, requested_optional_ids=["EM07", "EM07"])


def test_never_unknown_skip_not_asked_are_distinct():
    response = ROUTER.normalize_answer(
        "EM03", {"state": "ANSWERED", "value": "never", "intensity": "strong"}
    )
    assert response == {"question_id": "EM03", "state": "NEVER"}
    for state in ("UNKNOWN", "SKIPPED", "NEVER"):
        normalized = ROUTER.normalize_answer("EM03", {"state": state, "intensity": "strong"})
        assert normalized == {"question_id": "EM03", "state": state}
        assert ROUTER.could_ask_followup(normalized) is False
    assert ROUTER.could_ask_followup(
        ROUTER.normalize_answer("EM03", {"state": "ANSWERED", "value": "monthly"})
    ) is True
    with pytest.raises(ValueError):
        ROUTER.normalize_answer("EM03", {"state": "NOT_ASKED"})
    with pytest.raises(ValueError):
        ROUTER.normalize_answer("EM01", {"state": "ALREADY_COVERED", "source_ref": ""})


def test_meaning_and_social_contribution_preserved_separately():
    answer = ROUTER.normalize_answer(
        "EM08",
        {"state": "ANSWERED", "values": {
            "personal_meaning": "strong",
            "perceived_contribution": "none",
        }},
    )
    assert answer["values"] == {"personal_meaning": "strong", "perceived_contribution": "none"}
    partial = ROUTER.normalize_answer(
        "EM08",
        {"state": "ANSWERED", "values": {
            "personal_meaning": "strong",
            "perceived_contribution": "not_answered",
        }},
    )
    assert partial["values"]["perceived_contribution"] == "not_answered"
    with pytest.raises(ValueError):
        ROUTER.normalize_answer(
            "EM08", {"state": "ANSWERED", "values": {"personal_meaning": "strong"}}
        )
    # A spiritual interpretation, a frequency and a follow-up are never required in the same answer.
    normalized = ROUTER.normalize_answer("EM06", {"state": "ANSWERED", "value": "once_twice"})
    assert normalized == {"question_id": "EM06", "state": "ANSWERED", "value": "once_twice"}


def test_non_behavior_domains_are_registered_without_forcing_questions():
    ledger = json.loads((TASK / "HUMAN-EXPERIENCE-DOMAIN-GAPS-v1.json").read_text())
    ids = {x["id"] for x in ledger["domains"]}
    assert len(ids) == len(ledger["domains"]) >= 25
    assert {"dream_recall_and_visions", "aesthetic_sensitivity_creative_expression",
            "family_home_roots_belonging", "play_humor_spontaneity",
            "spiritual_worldview_practices", "life_turning_points_external_events"} <= ids
    assert all(row["next"] != "this_pilot" for row in ledger["domains"][9:])
    assert "not evidence" in ledger["interpretation"]


def test_offline_html_is_reproducible_without_network_autosave_or_model_targets():
    builder = load("build_offline_pilot")
    existing = builder.OUTPUT.read_bytes()
    assert builder.build().read_bytes() == existing
    html = existing.decode("utf-8")
    assert "life-patterns-experience-pilot-answers-v1" in html
    assert "No answer to this part" in html
    assert "localStorage" not in html
    assert "XMLHttpRequest" not in html
    assert "fetch(" not in html
    assert "<script src=" not in html
    assert "http://" not in html and "https://" not in html
    assert 'type="file"' in html
    assert "anchor.download=" in html  # export is created only on a user click
    js = html.split("<script>", 1)[1].split("</script>", 1)[0]
    node = subprocess.run(["node", "--check", "-"], input=js, text=True, capture_output=True)
    assert node.returncode == 0, node.stderr
