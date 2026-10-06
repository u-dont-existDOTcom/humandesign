"""Source structure/lookup and geometry checks, not predictive validation."""
from __future__ import annotations
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
H = HERE.parent / "B01h"
spec = importlib.util.spec_from_file_location("b01i_reference_under_test", HERE / "b01i_reference.py")
assert spec and spec.loader
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def load(path):
    return json.loads(path.read_text())


def test_all_five_singles_and_ten_pairs_exist_with_both_branches():
    t = ref.read_profile_table()
    expected = {frozenset([p]) for p in ref.PLANETS} | {
        frozenset(p) for p in itertools.combinations(ref.PLANETS, 2)
    }
    actual = [frozenset(p["planets"]) for p in t["profiles"]]
    assert set(actual) == expected
    assert len(actual) == len(set(actual)) == 15
    assert t["branch_count"] == 30
    for p in t["profiles"]:
        assert set(p["placement_branches"]) == {"HONOURABLE", "CONTRARY"}
        assert all(b["descriptors"] for b in p["placement_branches"].values())
        assert p["modern_trait_mapping"] is None
        assert p["default_weights"] is None


@pytest.mark.parametrize("planets", [(p,) for p in ref.PLANETS] + list(itertools.combinations(ref.PLANETS, 2)))
def test_every_profile_is_order_invariant_and_source_only(planets):
    a = ref.profile_reference(planets, topical_qualified=True, placement="HONOURABLE")
    b = ref.profile_reference(tuple(reversed(planets)), topical_qualified=True, placement="HONOURABLE")
    assert a == b
    assert a["is_prediction"] is False
    assert a["status"] == "SOURCE_REFERENCE_ONLY"
    assert a["qualification_origin"] == "CALLER_ASSERTION_NOT_VERIFIED_BY_THIS_HELPER"


@pytest.mark.parametrize("placement", [None, "MIXED", "UNRESOLVED"])
def test_unknown_or_mixed_placement_does_not_choose_a_favourable_branch(placement):
    r = ref.profile_reference(["Jupiter"], topical_qualified=True, placement=placement)
    assert r["status"] == "UNRESOLVED" and "description" not in r


@pytest.mark.parametrize("qualified,status", [(None, "UNRESOLVED"), (False, "NOT_APPLICABLE")])
def test_unknown_qualification_is_not_the_same_as_failed_qualification(qualified, status):
    r = ref.profile_reference(["Saturn"], topical_qualified=qualified, placement="CONTRARY")
    assert r["status"] == status and "description" not in r


def test_three_planets_not_synthesized_by_adding_pair_bundles():
    r = ref.profile_reference(["Saturn", "Mars", "Mercury"], topical_qualified=True, placement="HONOURABLE")
    assert r["status"] == "UNRESOLVED"


@pytest.mark.parametrize("planets", [[], ["Sun"], ["Moon"], ["Saturn", "Saturn"], [None]])
def test_invalid_table_ruler_requests_rejected(planets):
    with pytest.raises(ValueError):
        ref.profile_reference(planets, topical_qualified=True, placement="HONOURABLE")


def test_string_request_and_numeric_qualification_rejected():
    with pytest.raises(TypeError):
        ref.profile_reference("Mars", topical_qualified=True, placement="HONOURABLE")
    with pytest.raises(TypeError):
        ref.profile_reference(["Mars"], topical_qualified=1, placement="HONOURABLE")
    with pytest.raises(ValueError):
        ref.profile_reference(["Mars"], topical_qualified=True, placement="good person")


def test_honourable_malefic_bundle_not_rewritten_as_moral_goodness():
    r = ref.profile_reference(["Saturn", "Mars"], topical_qualified=True, placement="HONOURABLE")
    text = " ".join(r["description"]["descriptors"])
    assert "successful" in text and "tyrannical" in text and "deceitful" in text
    assert "neither good nor bad" in text and "evil through and through" in text


def test_contrary_benefic_bundles_retain_express_positive_qualifications():
    r = ref.profile_reference(["Jupiter", "Venus"], topical_qualified=True, placement="CONTRARY")
    text = " ".join(r["description"]["descriptors"])
    assert all(s in text for s in ["trustworthy", "not rascally", "gracious", "approachable"])
    r = ref.profile_reference(["Jupiter", "Mercury"], topical_qualified=True, placement="CONTRARY")
    text = " ".join(r["description"]["descriptors"])
    assert all(s in text for s in ["good memory", "teaching", "pure desires"])


@pytest.mark.parametrize("node,expected", [(0,[0,90,180,270]), (350,[350,80,170,260]), (-10,[350,80,170,260]), (720,[0,90,180,270])])
def test_nodal_quadratures_wrap_without_selecting_a_proximity_orb(node, expected):
    r=ref.nodal_quadrature_points(node)
    assert list(r.values()) == expected
    assert all(0 <= v < 360 for v in r.values())


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan"), True, "12"])
def test_invalid_geometric_inputs_fail(value):
    with pytest.raises((TypeError, ValueError)):
        ref.nodal_quadrature_points(value)


def test_body_table_preserves_unstated_qualities_and_venus_analogy():
    t = load(H/"BODY_REFERENCE_TABLES.json")
    rows = {r["row_id"]:r for r in t["planet_phase_descriptions"]}
    assert len(rows) == 9
    assert rows["BODY_JUPITER_SETTING"]["explicit_temperamental_qualities"] == ["moist"]
    assert rows["BODY_MARS_SETTING"]["explicit_temperamental_qualities"] == ["dry"]
    assert rows["BODY_VENUS_ANALOGY"]["explicit_temperamental_qualities"] == []
    body = {r["planet"]:r["source_correspondences"] for r in t["planetary_body_correspondences"]}
    assert "right ear" in body["Saturn"] and "left ear" in body["Mars"]
    assert "liver" in body["Venus"] and "lungs" in body["Jupiter"]
    assert len(t["eye_passage_star_clusters"]["items"]) == 6


def test_all_record_ids_and_source_locators_have_declared_integrity():
    allrows = load(H/"RULES.json")["records"] + load(HERE/"RULES.json")["records"]
    assert len(allrows) == 106
    assert [int(r["id"].split(".R")[-1]) for r in allrows] == list(range(228,334))
    assert len({r["id"] for r in allrows}) == 106
    for r in allrows:
        l = r["source_locator"]
        assert l["source_file_sha256"] == "10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec"
        assert l["printed_support_pages"] == [p-24 for p in l["pdf_support_pages"]]
        assert r["unknown_is_not_false"] is True
        assert r["admission"] == "SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS"
        assert l["passage_anchor"] and r["antecedents"]


def test_reading_receipts_and_coverage_match_actual_saved_rules():
    coverage = load(H/"SECTION_COVERAGE.json")
    assert {c["chapter"] for c in coverage["chapters"]} == {"III.11","III.12","III.13","III.14"}
    for d in [H,HERE]:
        data=load(d/"RULES.json"); r=load(d/"READING_RECEIPT.json")
        assert r["rules_sha256"] == hashlib.sha256((d/"RULES.json").read_bytes()).hexdigest()
        assert data["records_count"] == r["records_added"] == len(data["records"])
        assert r["new_ocr_calls"] == 0 and r["independent_validation_cases"] == 0
        ids=[rid for s in r["chapter_spans"] for rid in s["record_ids"]]
        assert ids == [x["id"] for x in data["records"]]


def test_all_profile_branches_link_to_actual_rules_and_local_json_targets():
    rules=load(HERE/"RULES.json")["records"]
    ids={r["id"] for r in rules}
    for p in ref.read_profile_table()["profiles"]:
        assert all(branch["rule_id"] in ids for branch in p["placement_branches"].values())
    for d in [H,HERE]:
        for r in load(d/"RULES.json")["records"]:
            for s in r.get("table_refs",[]):
                path,ptr=s.split("#",1); v=load(d/path)
                for part in ptr.strip("/").split("/"):
                    v=v[int(part)] if isinstance(v,list) else v[part]
                assert v is not None


def test_no_silent_resolution_of_motion_dignity_or_identity_bridge():
    h=load(H/"UNRESOLVED_INTERPRETATIONS.json")["items"]
    i=load(HERE/"UNRESOLVED_INTERPRETATIONS.json")["items"]
    alltext=json.dumps(h+i)
    assert "positive-speed" in alltext
    assert "Bouch" in alltext and "commentary" in alltext
    assert "modern identity" in alltext
    assert ref.read_profile_table()["sign_mode_bundles"][0]["membership_status"].startswith("UNRESOLVED")
