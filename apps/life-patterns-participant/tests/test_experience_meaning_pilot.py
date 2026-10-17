"""Optional survey dimensions and existing Custom GPT release separation."""

import importlib.util
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / "tasks/life-patterns-early-review-and-experience-20261017"


def test_experience_meaning_questions_are_optional_and_unscored():
    module = json.loads((TASK / "EXPERIENCE-MEANING-PILOT-v0.json").read_text())
    assert module["status"] == "EXPLORATORY_NOT_LIVE_NOT_ASTROLOGY_SCORED"
    items = module["items"]
    assert len(items) == 8
    assert len({item["id"] for item in items}) == 8
    assert len({item["name"] for item in items}) == 8
    assert len(module["minimal_pilot_path"]["default_optional_prompt_ids"]) == 4
    assert module["minimal_pilot_path"]["skip_if_existing_source_answers_equivalent"]
    assert "never" in module["anchoring"]["frequency_options"]
    assert "none" in module["anchoring"]["intensity_options"]
    assert "No astro/HD rules" in module["protocol"]["scoring"]


def test_guidance_and_meaning_measure_distinct_responses():
    module = json.loads((TASK / "EXPERIENCE-MEANING-PILOT-v0.json").read_text())
    domains = {item["name"]: item["targets"] for item in module["items"]}
    assert "interpretation" in domains["perceived_guidance"]
    assert "later_appraisal" in domains["meaningful_coincidences"]
    assert "personal_presence" in domains["personal_social_meaning"]
    assert "perceived_social_impact" in domains["personal_social_meaning"]
    assert "search_for_meaning" in domains["personal_social_meaning"]


def test_early_portal_update_does_not_change_other_gpt_knowledge():
    source = TASK / "build_gpt_early_review.py"
    spec = importlib.util.spec_from_file_location("early_gpter", source)
    assert spec is not None and spec.loader is not None
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    parts = builder.contents()
    manifest = json.loads(parts["UPDATE-MANIFEST.json"])
    assert manifest["action_version"] == "1.8.0"
    assert manifest["knowledge_files"] == 8
    assert manifest["instructions_strict_characters"] <= 8000
    assert manifest["same_existing_gpt_and_bearer"]
    assert not manifest["private_data_in_package"]
    assert builder.OUT.read_bytes() == builder.serialize(parts)
    with zipfile.ZipFile(builder.BASE) as prior:
        for key, contents in parts.items():
            if key.startswith("knowledge/") and key != builder.GUIDE:
                assert contents == prior.read(key)


def test_chart_topic_inventory_is_source_bound_and_not_rebranded_as_prediction():
    inventory = json.loads((TASK / "CHART-DOMAIN-V7-RECONCILIATION-v0.json").read_text())
    bank = json.loads(
        (ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json").read_text()
    )
    pilot = json.loads((TASK / "EXPERIENCE-MEANING-PILOT-v0.json").read_text())
    source_ids = {ref["id"] for ref in inventory["source_conventions"]}
    pilot_ids = {item["id"] for item in pilot["items"]}
    survey_families = set(bank["families"])
    statuses = {
        "absent",
        "proxy_only",
        "partial",
        "direct",
        "not_suitable_for_routine_personality_survey",
    }
    assert inventory["interpretation_policy"]["chart_domain_claim"].startswith(
        "Historical chart convention"
    )
    assert len(inventory["matrix"]) >= 20
    assert len({item["id"] for item in inventory["matrix"]}) == len(inventory["matrix"])
    assert inventory["survey_version"] == bank["version"]
    for item in inventory["matrix"]:
        assert item["survey_status"] in statuses
        assert set(item["families"]).issubset(survey_families)
        assert set(item["pilot_item_ids"]).issubset(pilot_ids)
        assert set(item["claim_sources"]).issubset(source_ids)
        assert item["measurement"]
    assert not any(
        item["survey_status"] == "direct" and item["id"].startswith("awe")
        for item in inventory["matrix"]
    )
