"""Schema/source/target-blinding tests for an UNSCORED prospective bridge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-richer-mapping-20261010"
ACTIVE = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
V2 = ROOT / "tasks/question-feedback-loop-20261008/tendency-first-v2-development.json"


def load(name: str) -> dict:
    return json.loads((TASK / name).read_text())


def test_each_current_question_has_observable_contract_and_retains_original_source():
    bridge = load("question_to_chart_hypotheses_v0.json")
    current = json.loads(ACTIVE.read_text())
    q = {x["id"]: x for x in current["questions"]}
    rows = bridge["current_question_contracts"]
    assert len(rows) == len(q) == 25
    assert len({x["question_id"] for x in rows}) == 25
    assert set(x["question_id"] for x in rows) == set(q)
    assert bridge["input_versions"]["active_v1"] == current["version"]
    assert (
        bridge["input_versions"]["active_v1_sha256"]
        == hashlib.sha256(ACTIVE.read_bytes()).hexdigest()
    )
    assert (
        bridge["input_versions"]["existing_proposed_v2_sha256"]
        == hashlib.sha256(V2.read_bytes()).hexdigest()
    )
    for row in rows:
        original = q[row["question_id"]]
        assert row["original_question"] == original["question"]
        assert row["source_route_id"] == original["source_route_id"]
        assert (
            row["original_question_sha256"]
            == hashlib.sha256(original["question"].encode()).hexdigest()
        )
        assert all(
            row[key]
            for key in (
                "measured_construct",
                "discriminating_contrast",
                "important_confounders",
                "defect_or_limit",
            )
        )
        assert original["planning_targets"] == []  # interviewer never receives target key
        assert row["participant_blinding"].startswith("Keep chart hypotheses")


def test_theory_hypotheses_are_complete_but_unscored_and_source_bound():
    data = load("question_to_chart_hypotheses_v0.json")
    codebook = load("source_to_target_evidence_codebook_v0.json")
    assert data["status"] == "DRAFT_UNSCORED_NOT_LIVE_NOT_VALIDATED"
    assert data["score_status"] == "NOT_ADMITTED_FOR_ANY_BIRTH_RANKING"
    assert len(data["theory_hypotheses"]) == 12
    assert len(data["supplement_question_candidates"]) == 4
    assert (
        codebook["theory_bridge_sha256"]
        == hashlib.sha256((TASK / "question_to_chart_hypotheses_v0.json").read_bytes()).hexdigest()
    )
    hypothesis_ids = {x["hypothesis_id"] for x in data["theory_hypotheses"]}
    assert len(hypothesis_ids) == len(data["theory_hypotheses"])
    assert hypothesis_ids == {x["hypothesis_id"] for x in codebook["hypotheses"]}
    for h in data["theory_hypotheses"]:
        assert h["theory_source_url"].startswith("https://jovianarchive.com/")
        assert h["chart_predicate"]["feature"] in {"type", "authority", "center", "channel"}
        assert h["scoring_status"] == "UNSCORED_PROSPECTIVE_DRAFT"
        assert "NOT_HUMAN_VALIDATED" in h["epistemic_status"]
    for evidence in codebook["hypotheses"]:
        assert evidence["unknown_is_valid"] is True
        assert evidence["chart_feature_absence_does_not_imply_opposite"] is True
        assert evidence["score_weight"] is None and evidence["probability"] is None
        assert all(
            evidence[k]
            for k in (
                "positive_evidence_if_multiple_situations",
                "possible_counterevidence_not_automatic_inverse",
                "must_abstain_if",
            )
        )


def test_no_bogus_trait_to_chart_links_or_live_question_activation():
    data = load("question_to_chart_hypotheses_v0.json")
    q = {r["question_id"]: r for r in data["current_question_contracts"]}
    linked = {key for key, value in q.items() if value["hypothesis_ids_behind_blind_wall"]}
    assert len(linked) == 10
    assert len(q) - len(linked) == 15
    assert q["TF1-M01"]["target_link_status"] == "question_near_claim_still_unscored"
    assert (
        sum(
            r["target_link_status"] == "needs_new_evidence_then_theory_link_trial"
            for r in q.values()
        )
        == 9
    )
    # Invitation/recognition of a specific contribution is NOT liking praise.
    assert q["TF1-STATUS"]["hypothesis_ids_behind_blind_wall"] == []
    # Changing group habits alone does not establish stable identity.
    assert q["TF1-G10"]["hypothesis_ids_behind_blind_wall"] == []
    # Persuasion success cannot automatically count as 'insight translation'.
    assert q["TF1-G05"]["hypothesis_ids_behind_blind_wall"] == []
    assert q["TF1-G17"]["draft_revised_question"] != q["TF1-G17"]["original_question"]
    assert q["TF1-D0"]["draft_revised_question"] != q["TF1-D0"]["original_question"]
    targets = {"HD-AUTH-SPLENIC", "HD-AUTH-EMOTIONAL"}
    extras = data["supplement_question_candidates"]
    assert targets <= {h for row in extras for h in row["hypothesis_ids"]}
    for item in extras:
        assert item["status"] == "NOT_ASKED_NOT_ACTIVE_NOT_SCORED"
        assert not any(
            token in item["candidate_question"].lower()
            for token in (
                "splenic",
                "projector",
                "solar plexus",
                "channel ",
                "human design",
                "astrology",
            )
        )


def test_owner_audit_is_rendered_without_person_specific_birth_or_target_data():
    page = (TASK / "RESEARCHER_MAPPING_AUDIT.html").read_text()
    audit = (TASK / "RICHER_MAPPING_AND_QUESTION_DEFECT_AUDIT.md").read_text()
    assert page.count('class="question"') == 25
    assert "not a live questionnaire" in page.lower()
    assert (
        "source feature" not in json.loads(ACTIVE.read_text())["questions"][0]["question"].lower()
    )
    assert all(x in audit for x in ("TF1-G17", "TF1-D0", "TF1-G06", "TF1-G23", "TF1-STATUS"))
    assert "new independent birth-data cohort" in audit
    assert "<script>alert" not in page
    assert len(page) > 30000
    assert "probability" in (TASK / "source_to_target_evidence_codebook_v0.json").read_text()


def test_astrohd_bridge_is_preserved_as_a_separate_six_rule_baseline():
    baseline = ROOT / "reference/research/astrohd_v15_behavioral_bridge.json"
    old = json.loads(baseline.read_text())
    new = load("ASTROHD_SIX_RULE_BASELINE_AND_EXPANSION_BOUNDARY.json")
    assert new["frozen_baseline_sha256"] == hashlib.sha256(baseline.read_bytes()).hexdigest()
    assert len(new["original_six_clauses_unchanged"]) == len(old["rules"]) == 6
    assert new["domain_count_original"] == len(old["domains"]) == 5
    assert new["new_astro_claims"] == []
    assert new["status"] == "DEVELOPMENT_RESEARCH_PROTOCOL_ONLY_NOT_A_NEW_MODEL"
    for a, b in zip(new["original_six_clauses_unchanged"], old["rules"], strict=True):
        assert a["original_rule_id"] == b["rule_id"]
        assert a["original_behavioral_domains"] == b["domain_ids"]
        assert not a["changed_in_this_version"]
    assert "do not invent" in new["warning"].lower() or "development" in new["warning"].lower()


def test_owner_local_guide_link_installs_without_changing_other_links(tmp_path):
    import sys

    path = str(TASK)
    sys.path.insert(0, path)
    from deliver_researcher_audit import install

    main = tmp_path / "Life-Patterns-Researcher-Guide.html"
    main.write_text('<html><body><a href="old-questions.html">Old guide</a></body></html>')
    first = install(tmp_path)
    second = install(tmp_path)
    assert first["index_updated"] is True
    assert second["index_updated"] is False
    assert first["delivered_files"] == 6
    assert all(
        x.is_file() for x in (tmp_path / "Life-Patterns-Richer-Mapping-2026-10-10").iterdir()
    )
    page = main.read_text()
    assert "old-questions.html" in page
    assert page.count("RESEARCHER_MAPPING_AUDIT.html") == 1
