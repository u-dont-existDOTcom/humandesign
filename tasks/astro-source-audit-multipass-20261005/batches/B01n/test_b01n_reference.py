"""Definition/arithmetic tests, not tests of astrology on human outcomes."""
from fractions import Fraction
from itertools import product
import importlib.util
import json
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b01n_reference", BASE / "b01n_reference.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
K = {"epoch_label": "synthetic externally chosen epoch", "count_policy": m.POLICY}


@pytest.mark.parametrize("planet,start,end,length", [
    ("Moon", 0, 4, 4), ("Mercury", 4, 14, 10), ("Venus", 14, 22, 8),
    ("Sun", 22, 41, 19), ("Mars", 41, 56, 15), ("Jupiter", 56, 68, 12),
    ("Saturn", 68, None, None),
])
def test_general_age_rows_are_nominal_not_native_predictions(planet, start, end, length):
    row = m.natural_age_reference(planet)
    assert (row["nominal_start_year"], row["nominal_end_year"], row["duration_years"]) == (start, end, length)
    assert row["scope"] == "GENERAL_BASELINE_NOT_INDIVIDUAL_PREDICTION"
    assert "does not supply a precise calendar boundary" in row["boundary_status"]


@pytest.mark.parametrize("origin,topics", [
    ("ASC", ["body", "journeys abroad"]), ("Fortune", ["property"]),
    ("Moon", ["affections of soul", "marriage"]), ("Sun", ["dignities", "glory"]),
    ("MC", ["actions", "friendships", "begetting children", "other conduct of life"]),
])
def test_all_five_topical_origins(origin, topics):
    assert m.topical_origin_reference(origin)["topics"] == topics


@pytest.mark.parametrize("planet,level", [
    ("Saturn", "general"), ("Jupiter", "annual"), ("Sun", "monthly"),
    ("Mars", "monthly"), ("Venus", "monthly"), ("Mercury", "monthly"), ("Moon", "daily"),
])
def test_each_emphasized_ingress_scale_not_exclusivity(planet, level):
    row = m.ingress_scale_reference(planet)
    assert row["level"] == level and row["exclusive"] is False


@pytest.mark.parametrize("start,years,expected", [
    ("Aries", 0, "Aries"), ("Aries", 1, "Taurus"), ("Pisces", 1, "Aries"),
    ("Cancer", 12, "Cancer"), ("Aquarius", 25, "Pisces"),
])
def test_annual_step_arithmetic(start, years, expected):
    r = m.annual_sign_reference(start, years, **K)
    assert r["sign"] == expected and r["steps"] == years
    assert r["sign_ruler"] == "NOT_COMPUTED_HERE"


@pytest.mark.parametrize("convention,level,elapsed,sign,remaining", [
    ("ROBBINS_MAIN", "monthly", "0", "Aries", "0"),
    ("ROBBINS_MAIN", "monthly", "27999/1000", "Aries", "27999/1000"),
    ("ROBBINS_MAIN", "monthly", "28", "Taurus", "0"),
    ("ROBBINS_MAIN", "monthly", "336", "Aries", "0"),
    ("ROBBINS_MAIN", "monthly", "365", "Taurus", "1"),
    ("ROBBINS_MAIN", "daily", "7/3", "Taurus", "0"),
    ("ROBBINS_MAIN", "daily", "233333/100000", "Aries", "233333/100000"),
    ("ROBBINS_MAIN", "daily", "28", "Aries", "0"),
    ("REPORTED_ALTERNATIVE", "monthly", "28", "Aries", "28"),
    ("REPORTED_ALTERNATIVE", "monthly", "30", "Taurus", "0"),
    ("REPORTED_ALTERNATIVE", "monthly", "360", "Aries", "0"),
    ("REPORTED_ALTERNATIVE", "daily", "7/3", "Aries", "7/3"),
    ("REPORTED_ALTERNATIVE", "daily", "5/2", "Taurus", "0"),
    ("REPORTED_ALTERNATIVE", "daily", "30", "Aries", "0"),
])
def test_rational_period_boundaries(convention, level, elapsed, sign, remaining):
    r = m.subperiod_sign_reference("Aries", elapsed, level=level, convention=convention, **K)
    assert (r["sign"], r["within_sign_days"]) == (sign, remaining)
    assert r["automatic_civil_year_normalization"] is False


def test_exact_cycle_arithmetic_and_different_witness_authority():
    main = m.subperiod_sign_reference("Pisces", Fraction(28), level="daily", convention="ROBBINS_MAIN", **K)
    alt = m.subperiod_sign_reference("Pisces", Fraction(30), level="daily", convention="REPORTED_ALTERNATIVE", **K)
    assert main["twelve_sign_days"] == "28" and alt["twelve_sign_days"] == "30"
    assert main["sign"] == alt["sign"] == "Pisces"
    assert "lacks manuscript support" in alt["authority"]


@pytest.mark.parametrize("bad", [1.5, True, None, float("nan"), -1, "-1/3", "x", "1/0"])
def test_reject_inexact_invalid_or_negative_elapsed(bad):
    with pytest.raises((ValueError, TypeError)):
        m.subperiod_sign_reference("Aries", bad, level="daily", convention="ROBBINS_MAIN", **K)


@pytest.mark.parametrize("overrides", [
    {"epoch_label": ""}, {"count_policy": "AUTO"}, {"convention": "HYBRID"},
    {"level": "annual"}, {"start_sign": "Unknown"},
])
def test_explicit_count_contract_required(overrides):
    args = {"start_sign": "Aries", "elapsed_days": 0, "level": "monthly", "convention": "ROBBINS_MAIN", **K}
    args.update(overrides)
    with pytest.raises(ValueError):
        m.subperiod_sign_reference(**args)


@pytest.mark.parametrize("bad", [True, 1.5, -1, "1"])
def test_annual_completed_steps_are_explicit_nonnegative_integers(bad):
    with pytest.raises(ValueError):
        m.annual_sign_reference("Aries", bad, **K)


def test_initial_contacts_have_priority_and_terms_remain_separate():
    r = m.reconcile_general_lords(at_degree_or_aspect=["Venus", "Mars", "Venus"],
                                  nearest_preceding=["Saturn"], term_lords=["Jupiter"])
    assert r["encounter_lords"] == ["Venus", "Mars"]
    assert r["term_co_rulers"] == ["Jupiter"] and r["route"] == "AT_DEGREE_OR_ASPECT"
    assert r["term_share_weight"] == "UNSPECIFIED_BY_PASSAGE"


@pytest.mark.parametrize("direct,preceding,expected,selected", [
    (None, ["Saturn"], "UNKNOWN_INITIAL_CONTACT", None),
    ([], None, "UNKNOWN_PRECEDING_CONTACT", None),
    ([], ["Saturn", "Jupiter"], "REFERENCE_CARRIERS_SELECTED", ["Saturn", "Jupiter"]),
    ([], [], "NO_SUPPLIED_QUALIFIED_CARRIER", []),
    (["Sun"], None, "REFERENCE_CARRIERS_SELECTED", ["Sun"]),
])
def test_known_absence_not_unknown_enables_preceding_fallback(direct, preceding, expected, selected):
    r = m.reconcile_general_lords(at_degree_or_aspect=direct, nearest_preceding=preceding, term_lords=None)
    assert r["status"] == expected and r["encounter_lords"] == selected
    assert r["term_status"] == "UNKNOWN" and r["prediction"] is None


@pytest.mark.parametrize("bad", ["Venus", ["Neptune"], {"Mars"}, [1]])
def test_invalid_carrier_evidence_rejected(bad):
    with pytest.raises((TypeError, ValueError)):
        m.reconcile_general_lords(at_degree_or_aspect=bad, nearest_preceding=[], term_lords=[])


@pytest.mark.parametrize("origin,measure", [
    ("ASC", "LOCAL_ASCENSION_TIMES"), ("MC", "CULMINATION_TIMES"),
    ("Sun", "ANGULAR_POSITION_PROPORTION"), ("Moon", "ANGULAR_POSITION_PROPORTION"),
    ("Fortune", "ANGULAR_POSITION_PROPORTION"),
])
def test_direction_units_follow_origin_not_zodiacal_difference(origin, measure):
    r = m.equivalent_years_reference(origin, "46", supplied_measure=measure, geometry_qualified=True)
    assert r["years"] == "46" and r["event_date"] is None
    with pytest.raises(ValueError):
        m.equivalent_years_reference(origin, "60", supplied_measure="ECLIPTIC_LONGITUDE_DEGREES", geometry_qualified=True)


@pytest.mark.parametrize("qualified,status", [(None, "UNKNOWN_GEOMETRY"), (False, "UNQUALIFIED")])
def test_uncomputed_geometry_cannot_become_years(qualified, status):
    r = m.equivalent_years_reference("ASC", 46, supplied_measure="LOCAL_ASCENSION_TIMES", geometry_qualified=qualified)
    assert r["status"] == status and r["years"] is None


def test_three_valued_condition_table_all_243_combinations():
    # One exhaustive logic test, not 243 independent research observations.
    def logical_and(vals):
        return False if any(v is False for v in vals) else (None if any(v is None for v in vals) else True)
    for vals in product([True, False, None], repeat=5):
        r = m.aspect_context_reference(**dict(zip(
            ["natal_harmonious", "ingress_favorable", "natal_inharmonious", "opposite_sect", "hard_transit_relation"], vals)))
        assert r["favorable_clause"] is logical_and(vals[:2])
        assert r["adverse_clause"] is logical_and(vals[2:])
        assert r["actual_event_inferred"] is False


def test_conflicting_qualified_testimony_not_arbitrarily_overridden():
    r = m.aspect_context_reference(natal_harmonious=True, ingress_favorable=True,
        natal_inharmonious=True, opposite_sect=True, hard_transit_relation=True)
    assert r["status"] == "COMPETING_SUPPLIED_TESTIMONY_NO_PRECEDENCE"


def test_hard_aspect_exclusion_is_not_positive_prediction():
    r = m.aspect_context_reference(natal_harmonious=False, ingress_favorable=False,
        natal_inharmonious=True, opposite_sect=True, hard_transit_relation=False)
    assert r["status"] == "NEITHER_CLAUSE_TRIGGERED_NOT_OPPOSITE_PREDICTION"


@pytest.mark.parametrize("same,natal,status", [
    (True, True, "SOURCE_INTENSIFICATION_PLUS_ORIGINAL_RULERSHIP"),
    (True, False, "SOURCE_INTENSIFICATION"),
    (True, None, "SOURCE_INTENSIFICATION_NATAL_ROLE_UNRESOLVED"),
    (False, True, "NOT_TRIGGERED_NOT_WEAK_EVENT_PREDICTION"),
    (None, True, "UNKNOWN_ROLE_COINCIDENCE"),
])
def test_repeated_planet_roles_not_independent_votes(same, natal, status):
    r = m.role_coincidence_reference(same_time_and_ingress_lord=same, original_natal_ruler=natal)
    assert r["status"] == status and r["numeric_weight"] is None
    assert r["independent_confirmations_added"] == 0
    assert r["valence"] == "NOT_DETERMINED_BY_COINCIDENCE"


def test_non_boolean_qualifiers_rejected():
    with pytest.raises(TypeError):
        m.role_coincidence_reference(same_time_and_ingress_lord=1, original_natal_ruler=True)


def test_outputs_are_copies_and_invalid_reference_keys_fail():
    first = m.natural_age_reference("Mars")
    first["qualities"].clear()
    assert m.natural_age_reference("Mars")["qualities"]
    t = m.topical_origin_reference("Moon")
    t["topics"].clear()
    assert m.topical_origin_reference("Moon")["topics"]
    for func in [m.natural_age_reference, m.topical_origin_reference, m.ingress_scale_reference]:
        with pytest.raises(ValueError):
            func("not-in-source")


def test_source_records_complete_unique_and_in_scope():
    data = json.loads((BASE / "RULES.json").read_text())
    assert data["records_count"] == len(data["records"]) == 78
    ids = [r["id"] for r in data["records"]]
    assert ids == [f"PT.R64.IV.10.R{i}" for i in range(631, 709)]
    for row in data["records"]:
        assert row["source_locator"]["chapter_or_verse"] == "IV.10"
        assert all(461 <= p <= 483 for p in row["source_locator"]["pdf_support_pages"])
        assert row["unknown_is_not_false"] is True
        assert "NOT_ADMITTED" in row["admission"]
    coverage = json.loads((BASE / "SECTION_COVERAGE.json").read_text())
    assert coverage["sections"][0]["record_ids"] == ids
    assert {i for s in coverage["segments"] for i in s["record_ids"]} == set(ids)


def test_table_source_links_and_all_ambiguity_links_resolve():
    data = json.loads((BASE / "RULES.json").read_text())
    ids = {r["id"] for r in data["records"]}
    for name in ["natural_ages", "topical_origins", "emphasized_ingress_scales"]:
        assert all(row["source_record"] in ids for row in m.TABLES[name])
    issues = json.loads((BASE / "UNRESOLVED_INTERPRETATIONS.json").read_text())
    known = {r["id"] for r in issues["items"]}
    assert len(known) == issues["count"] == 22
    for row in data["records"]:
        assert set(row["ambiguities"]) <= known


def test_both_endings_and_three_comparisons_remain_separate():
    assert [r["key"] for r in m.TABLES["ending_witnesses"]] == ["PARISINUS_2425", "MADPROC_CAM"]
    c = json.loads((BASE / "CROSS_SOURCE_COMPARISONS.json").read_text())
    assert [r["id"] for r in c["comparisons"]] == ["C18", "C19", "C20"]
    assert all(r["independent_empirical_confirmation"] is False for r in c["comparisons"])
