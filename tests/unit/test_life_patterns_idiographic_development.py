"""Prospective response scaffolds, historical-facet scope and private local pilot."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-idiographic-20261010"
ATLAS = ROOT / "tasks/survey-recovery-autonomy-20261009"


def read(filename):
    return json.loads((TASK / filename).read_text())


def test_development_v3_is_pinned_to_v1_v2_and_completely_unscored():
    current = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
    previous = ROOT / "tasks/question-feedback-loop-20261008/tendency-first-v2-development.json"
    v1, v2 = json.loads(current.read_text()), json.loads(previous.read_text())
    v3 = read("tendency-first-v3-scaffold-development.json")
    assert v3["status"] == "RESEARCH_CANDIDATE_NOT_ACTIVE_NOT_VALIDATED"
    assert (
        v3["source_integrity"]["active_v1_sha256"]
        == hashlib.sha256(current.read_bytes()).hexdigest()
    )
    assert (
        v3["source_integrity"]["previous_v2_sha256"]
        == hashlib.sha256(previous.read_bytes()).hexdigest()
    )
    assert v3["parent_policy_version"] == v2["version"]
    assert len(v3["questions"]) == len(v2["questions"]) == len(v1["questions"]) == 25
    old = {q["id"]: q for q in v2["questions"]}
    new = {q["id"]: q for q in v3["questions"]}
    assert set(old) == set(new)
    changed = {k for k in old if old[k]["question"] != new[k]["question"]}
    assert changed == {"TF1-A0"}
    for key, row in new.items():
        assert row["source_route_id"] == old[key]["source_route_id"]
        assert row["planning_targets"] == []
        assert 2 <= len(row["example_answer_paths"]) <= 4
        assert len(set(row["example_answer_paths"])) == len(row["example_answer_paths"])
        assert row["examples_display_by_default"] is True
        assert row["automatic_chart_scoring"] is False
        assert row["answer_format"] == "free_text_or_examples_multi_select_with_other_skip_unsure"
    assert v3["response_scaffolding_policy"]["options_never_forced"] is True
    assert v3["response_scaffolding_policy"]["multi_select_allowed"] is True
    assert any(
        "Other" in option for option in v3["response_scaffolding_policy"]["response_options"]
    )


def test_a0_scaffolding_disambiguates_solitude_time_making_from_company_tradeoff():
    v3 = read("tendency-first-v3-scaffold-development.json")
    rows = {q["id"]: q for q in v3["questions"]}
    a0 = rows["TF1-A0"]
    assert a0["question"] == "How much do you enjoy spending time alone?"
    assert "intrinsic_enjoyment_of_solitude" in a0["measured_dimensions"]
    followups = a0["follow_up_only_if_not_already_answered"]
    assert len(followups) == 2
    assert "arrange time alone" in followups[0]["question"]
    assert "friend invites" in followups[1]["question"]
    assert "not_inferred_from_solitude_enjoyment" in followups[1]["measures"]
    recognition = rows["TF1-STATUS"]
    assert recognition["scoped_measured_dimension"] == "intrinsic_subjective_value_of_recognition"
    assert recognition["exclude_historical_joint_facet_without_new_admission"] == [
        "D19.status_ownership"
    ]
    assert all("laptop" not in x.lower() for x in recognition["example_answer_paths"])


def test_idiographic_inventory_is_voluntary_and_not_a_birth_difficulty_score():
    module = read("unusual-behavior-inventory-v0.json")
    assert module["can_record_zero"] is True
    assert module["initial_batch_size"] == 3
    assert "10–20" in module["target_list_size_if_willing"]
    assert "quota" in module["target_list_size_if_willing"]
    assert (
        "not" in module["birth_predictiveness_hypothesis"].lower()
        or "test" in module["birth_predictiveness_hypothesis"].lower()
    )
    assert module["evaluation_design"]["no_unproven_birth_difficulty_inference"] is True
    assert module["evaluation_design"]["birth_data_hidden_from_interviewer"] is True
    assert module["data_schema_per_item"]["objective_prevalence_verified"] == "false_by_default"
    assert module["data_schema_per_item"]["chart_prediction_admitted"] == "false_by_default"
    assert any("Can't think" in x for x in module["participant_control"])
    assert "unsafe" in module["example_safety"].lower()


def test_source_facet_split_preserves_original_and_atlas_has_no_laptop_ownership_in_active_status():
    source = ROOT / "tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json"
    old = json.loads(source.read_text())
    original = next(x for x in old if x["facet_id"] == "D19.status_ownership")
    assert set(original["question_routes"]) == {"STATUS", "OWNERSHIP"}
    split = read("scoped_recognition_ownership_and_solitude-v0.json")
    assert split["frozen_source"]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert len(split["separate_prospective_dimensions"]) == 2
    assert set(split["separate_prospective_dimensions"][0]["route_ids"]) == {"TF1-STATUS"}
    rows = json.loads((ATLAS / "question-atlas.json").read_text())["questions"]
    scoped = [r for r in rows if r["id"] == "TF1-STATUS"]
    assert len(scoped) == 2
    assert all(r["frozen_v7_facet_examples"] == [] for r in scoped)
    assert all("laptop" in r["source_scope_note"].lower() for r in scoped)
    historical = next(r for r in rows if r["id"] == "STATUS" and r["version"] == "historical_v7")
    assert historical["frozen_v7_facet_examples"][0]["facet_id"] == "D19.status_ownership"
    assert "laptop" in historical["frozen_v7_facet_examples"][0]["narrow_supported_reading"].lower()
    v2_a0 = next(r for r in rows if r["id"] == "TF1-A0" and r["version"] == "proposed_tf1_v2")
    assert "TEXT SAME AS CURRENT V1" in v2_a0["status"]


def test_offline_pilot_has_25_choice_routes_no_remote_transmission_and_valid_js(tmp_path):
    path = TASK / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html"
    page = path.read_text()
    assert 'id="pilot-data"' in page
    assert '<textarea id="other"' in page
    assert '<textarea id="behavior"' in page
    assert 'id="skip"' in page and 'id="unsure"' in page
    assert "No data are transmitted" in page or "does not upload" in page
    assert "fetch(" not in page and "XMLHttpRequest" not in page
    assert "URL.createObjectURL" in page
    assert "TF1-STATUS" in page and "TF1-A0" in page
    scripts = re.findall(r"<script(?: [^>]*)?>(.*?)</script>", page, flags=re.S)
    assert len(scripts) == 2
    script = tmp_path / "pilot.js"
    script.write_text(scripts[-1])
    subprocess.run(["node", "--check", str(script)], check=True, capture_output=True)


def test_delivery_is_reversible_and_idempotent(tmp_path):
    import importlib.util

    script = TASK / "deliver_owner_pilot.py"
    spec = importlib.util.spec_from_file_location("idiographic_delivery", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    guide = tmp_path / "Life-Patterns-Researcher-Guide.html"
    guide.write_text("<html><body><p>Existing guide content</p></body></html>")
    atlas = tmp_path / "existing-atlas.html"
    atlas.write_text("Previous atlas")
    first = module.deliver(tmp_path, existing_atlas_path=atlas)
    second = module.deliver(tmp_path, existing_atlas_path=atlas)
    assert first["landing_changed"] is True
    assert second["landing_changed"] is False
    assert first["current_atlas_updated"] is True
    assert second["current_atlas_updated"] is False
    assert first["question_pilot_hashes_match"] is True
    assert first["atlas_hash_matches"] is True
    assert "Existing guide content" in guide.read_text()
    assert guide.read_text().count("LIFE_PATTERNS_V3_OFFLINE_PILOT.html") == 1
    assert (
        tmp_path / "All-Questions-Previous-Generated-2026-10-10.html"
    ).read_text() == "Previous atlas"
