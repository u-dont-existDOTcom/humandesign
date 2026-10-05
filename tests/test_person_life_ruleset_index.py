import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "reference" / "research" / "CURRENT_PERSON_LIFE_RULESET_INDEX_V1.json"


def test_person_life_ruleset_index_is_mandatory_and_complete():
    data = json.loads(INDEX.read_text())
    assert data["status"] == "CURRENT_ROUTING_INDEX"
    assert data["activation_contract"]["required_before_substantive_reasoning"] is True
    assert data["activation_contract"]["no_silent_omission"] is True
    assert set(data["activation_contract"]["required_dispositions"]) == {
        "APPLIED", "NOT_APPLICABLE", "UNAVAILABLE", "SUPERSEDED"
    }

    ids = {row["family_id"] for row in data["families"]}
    assert {
        "source_grounded_astrology_v14_full_library",
        "astrohd_v14_six_rule_owner_fitted_signature",
        "numerology_source_audit_v2_1",
        "numerology_name_layers",
        "merged_timing_candidates",
        "timing_model_controls",
        "human_design_v4_3_core",
        "cf003_planetary_dominance",
        "relationship_pair_analysis",
    } <= ids
    assert data["catalog"] == "reference/research/CURRENT_PERSON_LIFE_RULESET_CATALOG_V1.json"
    assert data["astrology_deep_analysis_protocol"] == "reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json"
    assert all(row["must_consider"] is True for row in data["families"])


def test_same_branch_authority_paths_exist():
    data = json.loads(INDEX.read_text())
    for row in data["families"]:
        authority = row["authority"]
        if authority["ref"] != "same_commit_as_index":
            assert authority.get("commit")
            assert authority.get("primary_path")
            continue
        for key, value in authority.items():
            if key.endswith("_path") or key == "primary_path":
                assert (ROOT / value).exists(), f"missing {row['family_id']} authority path: {value}"


def test_agents_bootstrap_requires_person_life_index():
    agents = (ROOT / "AGENTS.md").read_text()
    assert "## Person-life ruleset activation" in agents
    assert "CURRENT_PERSON_LIFE_RULESET_INDEX_V1.json" in agents
    assert "CURRENT_PERSON_LIFE_RULESET_CATALOG_V1.json" in agents
    assert "ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json" in agents
    assert "Do not silently omit an older retained ruleset" in agents
