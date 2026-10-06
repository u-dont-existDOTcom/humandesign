"""Source-definition and anti-substitution fixtures, not empirical validation."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b01b_definitions", BASE / "b01b_definitions.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def test_four_classes_and_polarities_exhaust_twelve_signs():
    groups = {"SOLSTITIAL": [], "EQUINOCTIAL": [], "SOLID": [], "BICORPOREAL": []}
    masculine = []
    for i, name in enumerate(ref.SIGNS):
        row = ref.sign_definition(name)
        assert ref.sign_definition(i) == row
        groups[row["source_class"]].append(name)
        if row["fixed_polarity"] == "MASCULINE_DIURNAL":
            masculine.append(name)
    assert groups == {
        "SOLSTITIAL": ["Cancer", "Capricorn"], "EQUINOCTIAL": ["Aries", "Libra"],
        "SOLID": ["Taurus", "Leo", "Scorpio", "Aquarius"],
        "BICORPOREAL": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    }
    assert masculine == ["Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"]


@pytest.mark.parametrize("value", [True, False, -1, 12, 360, 1.0, float("nan"), "", "Ophiuchus"])
def test_invalid_signs_are_rejected_not_wrapped(value):
    with pytest.raises(ValueError):
        ref.sign_index(value)


def test_unknown_is_not_false():
    assert ref.sign_definition(None) is None
    assert ref.ascendant_alternating_polarity("Aries", None) is None
    assert ref.quadrant_polarity(None) is None
    assert ref.seasonal_hour_minutes(None) is None
    assert ref.sign_relationship(None, "Aries")["disjunct"] is None
    assert ref.sign_relationship("Aries", None)["status"] == "UNKNOWN"


def test_reported_alternating_origin_is_not_static_polarity():
    assert ref.ascendant_alternating_polarity("Taurus", "Taurus") == "MASCULINE"
    assert ref.sign_definition("Taurus")["fixed_polarity"] == "FEMININE_NOCTURNAL"
    assert ref.ascendant_alternating_polarity("Gemini", "Taurus") == "FEMININE"
    assert ref.ascendant_alternating_polarity("Aries", "Pisces") == "FEMININE"


def test_quadrants_require_explicit_membership():
    assert ref.quadrant_polarity("ASC_TO_MC") == "MASCULINE_MATUTINAL"
    assert ref.quadrant_polarity("DSC_TO_IC") == "MASCULINE_MATUTINAL"
    assert ref.quadrant_polarity("MC_TO_DSC") == "FEMININE_EVENING"
    assert ref.quadrant_polarity("IC_TO_ASC") == "FEMININE_EVENING"
    with pytest.raises(ValueError):
        ref.quadrant_polarity("HOUSE_1_ASSUMED")


def test_all_144_ordered_sign_pairs_and_wraparound():
    for a in range(12):
        for b in range(12):
            relation = ref.sign_relationship(a, b)
            reverse = ref.sign_relationship(b, a)
            distance = min(abs(a - b), 12 - abs(a - b))
            assert relation["distance"] == distance
            assert relation["listed_aspect"] == {2:"SEXTILE",3:"QUARTILE",4:"TRINE",6:"OPPOSITION"}.get(distance)
            assert relation["disjunct"] == (distance in (1,5))
            assert relation["equal_power"] == reverse["equal_power"]
            assert relation["disjunct"] == reverse["disjunct"]
    assert ref.sign_relationship("Pisces", "Aries")["distance"] == 1


def test_same_sign_is_neither_a_fifth_listed_aspect_nor_alien():
    relation = ref.sign_relationship("Aries", "Aries")
    assert relation["same_sign"] is True
    assert relation["listed_aspect"] is None
    assert relation["disjunct"] is False
    assert relation["harmony"] is None


def test_harmony_not_derived_from_gender_parity():
    assert ref.sign_definition("Aries")["fixed_polarity"] == ref.sign_definition("Libra")["fixed_polarity"]
    assert ref.sign_relationship("Aries", "Libra")["harmony"] == "DISHARMONIOUS"
    assert ref.sign_relationship("Aries", "Gemini")["harmony"] == "HARMONIOUS"
    assert ref.sign_relationship("Aries", "Cancer")["harmony"] == "DISHARMONIOUS"


def test_five_directed_pairs_match_translator_not_modern_reflection():
    assert ref.COMMANDING_PAIRS == (("Taurus","Pisces"),("Gemini","Aquarius"),("Cancer","Capricorn"),("Leo","Sagittarius"),("Virgo","Scorpio"))
    for a,b in ref.COMMANDING_PAIRS:
        assert ref.sign_relationship(a,b)["commanding_direction"] == "A_COMMANDS_B"
        assert ref.sign_relationship(b,a)["commanding_direction"] == "B_COMMANDS_A"
    assert ref.sign_relationship("Aries","Pisces")["commanding_direction"] is None
    assert all("Aries" not in pair and "Libra" not in pair for pair in ref.COMMANDING_PAIRS)


def test_five_equal_power_pairs_remain_source_specific():
    assert ref.EQUAL_POWER_PAIRS == (("Gemini","Leo"),("Taurus","Virgo"),("Aries","Libra"),("Pisces","Scorpio"),("Aquarius","Sagittarius"))
    assert all("Cancer" not in pair and "Capricorn" not in pair for pair in ref.EQUAL_POWER_PAIRS)
    assert ref.sign_relationship("Gemini","Leo")["equal_power"] is True
    assert ref.sign_relationship("Leo","Gemini")["equal_power"] is True
    assert ref.sign_relationship("Gemini","Cancer")["equal_power"] is False


def test_seasonal_hour_is_not_necessarily_sixty_minutes():
    assert ref.seasonal_hour_minutes(900) == 75
    assert ref.seasonal_hour_minutes(900, night=True) == 45
    assert ref.seasonal_hour_minutes(720) == 60


@pytest.mark.parametrize("value", [True, 0, 1440, -1, 1441, float("nan"), float("inf"), "900"])
def test_unknown_polar_or_invalid_daylight_does_not_gain_a_new_convention(value):
    with pytest.raises(ValueError):
        ref.seasonal_hour_minutes(value)


def test_season_and_region_lookups_have_different_sequences():
    assert list(ref.SEASON_QUALITIES.values()) == ["MOIST","HOT","DRY","COLD"]
    assert list(ref.REGION_QUALITIES.values()) == ["DRY","HOT","MOIST","COLD"]


def test_all_fixed_star_groups_have_locators_and_no_unearned_coordinates():
    table = json.loads((BASE / "FIXED_STAR_TABLE.json").read_text())
    rows = table["entries"]
    assert len(rows) == table["entry_count"] == 95
    assert len({r["entry_id"] for r in rows}) == 95
    assert sum(r["source_region"] == "FIGURES_IN_ZODIAC" for r in rows) == 53
    assert sum(r["source_region"] == "FIGURES_NORTH_OF_ZODIAC" for r in rows) == 23
    assert sum(r["source_region"] == "FIGURES_SOUTH_OF_ZODIAC" for r in rows) == 19
    assert table["independent_predictions_count"] == 0
    assert table["coordinates"] is table["orbs"] is table["epoch"] is None
    for row in rows:
        assert row["source_locator"]["chapter_or_verse"] == "I.9"
        assert row["source_locator"]["pdf_english_pages"]
        assert row["relative_strength"]["numeric_weights"] is None
        lesser = row["relative_strength"]["explicitly_lesser_analogue"]
        assert lesser is None or lesser in row["planetary_analogues"]


def test_star_subgroups_and_weight_qualifiers_are_not_flattened():
    rows = json.loads((BASE / "FIXED_STAR_TABLE.json").read_text())["entries"]
    by_id = {r["entry_id"]:r for r in rows}
    spica = by_id["PT.R64.I.09.FS026"]
    assert spica["planetary_analogues"] == ["Venus","Mars"]
    assert spica["relative_strength"]["explicitly_lesser_analogue"] == "Mars"
    assert by_id["PT.R64.I.09.FS057"]["planetary_analogues"] == ["Saturn","Mars","Jupiter"]
    assert by_id["PT.R64.I.09.FS084"]["planetary_analogues"] == ["Venus"]
    assert by_id["PT.R64.I.09.FS085"]["planetary_analogues"] == ["Jupiter","Mars"]
    assert by_id["PT.R64.I.09.FS063"]["translator_annotations"][0]["kind"] == "GROUP_MEMBER_NOTE"


def test_batch_records_preserve_interpretive_gaps_and_hashes():
    rules = json.loads((BASE / "RULES.json").read_text())
    receipt = json.loads((BASE / "READING_RECEIPT.json").read_text())
    assert len(rules["records"]) == rules["records_count"] == 32
    assert len({r["id"] for r in rules["records"]}) == 32
    assert {r["source_locator"]["chapter_or_verse"] for r in rules["records"]} == {f"I.{x}" for x in range(9,17)}
    assert rules["independent_predictions_count"] == 0
    for row in rules["records"]:
        assert row["unknown_is_not_false"] is True
        assert row["source_locator"]["source_file_sha256"] == receipt["source_file_sha256"]
        assert row["interpretation_bridge"]["status"] == "UNDEFINED_FOR_PERSON_OUTCOMES"
        assert row["admission"] == "SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS"
    assert receipt["source_rules_sha256"] == hashlib.sha256((BASE / "RULES.json").read_bytes()).hexdigest()
    assert receipt["fixed_star_table_sha256"] == hashlib.sha256((BASE / "FIXED_STAR_TABLE.json").read_bytes()).hexdigest()
