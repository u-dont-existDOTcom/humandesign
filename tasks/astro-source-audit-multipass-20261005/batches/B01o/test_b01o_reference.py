"""Bounded reference/data checks, not evidence for population or natal prediction."""
import importlib.util
import json
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b01o_reference", HERE / "b01o_reference.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R = json.loads((HERE / "RULES.json").read_text())
T = json.loads((HERE / "GENERAL_CONTEXT_TABLES.json").read_text())
K = json.loads((HERE / "RECORD_KEY_MAP.json").read_text())


def test_sequential_unique_records_and_count():
    assert R["records_count"] == len(R["records"]) == 37
    assert len({x["id"] for x in R["records"]}) == 37
    assert [int(x["id"].split("R")[-1]) for x in R["records"]] == list(range(709, 746))
    assert len(set(K.values())) == 37
    assert R["independent_predictions_count"] == 0


def test_every_record_has_source_pages_attribution_and_explicit_scope():
    allowed = {141, 143, 145, 147, 149, 151}
    for row in R["records"]:
        loc = row["source_locator"]
        assert loc["pdf_support_pages"] and set(loc["pdf_support_pages"]) <= allowed
        assert loc["printed_support_pages"] == [p - 24 for p in loc["pdf_support_pages"]]
        assert loc["source_file_sha256"] == "10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec"
        assert loc["passage_anchor"] and loc["attribution_layer"]
        assert row["antecedents"] and row["consequent"]
        assert row["unknown_is_not_false"] is True
        assert row["admission"] == "SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS"
        assert row["interpretation_bridge"]["status"].startswith("UNDEFINED")


@pytest.mark.parametrize("term,context,text", [
    ("climes", "II.1_NOTE1", "latitude"),
    ("proper regions", "II.1_NOTE2", "I.17"),
    ("transits", "II.1_NOTE3", "through the zodiac"),
    ("parallels", "II.2_NOTE5", "north or south"),
    ("angles", "II.2_NOTE5", "east or west"),
])
def test_context_bound_definitions(term, context, text):
    d = m.definition(term, context)
    assert text in d["meaning"]
    assert m.source_record(d["source_record"])["source_locator"]["attribution_layer"] == "ROBBINS_EXPLANATORY_NOTE"


@pytest.mark.parametrize("term,context", [("angles", "III.10"), ("parallels", "MODERN_DECLINATION"), ("houses", "II.1_NOTE2"), ("climes", "II.2_NOTE5")])
def test_no_silent_cross_context_substitution(term, context):
    with pytest.raises(KeyError):
        m.definition(term, context)


@pytest.mark.parametrize("bad", [None, 0, True, "", " "])
def test_bad_definition_inputs(bad):
    with pytest.raises(ValueError):
        m.definition(bad, "II.1_NOTE1")
    with pytest.raises(ValueError):
        m.definition("climes", bad)


def test_spatial_and_circumstance_are_not_one_axis():
    d = m.general_inquiry_axes()
    assert d["axes_are_separate"] is True
    assert d["spatial"]["adopted"] == ["whole countries", "cities"]
    assert d["spatial"]["reported_variant"]["second_part"] == "both countries and cities"
    assert d["circumstance"]["greater_more_periodic"]["examples"] == ["wars", "famines", "pestilences", "earthquakes", "deluges"]
    assert "crops" in d["circumstance"]["lesser_more_occasional"]["examples"]


def test_five_glossary_rows_and_six_retained_historical_portraits():
    assert len(T["glossary"]) == 5
    assert len(T["historical_region_portraits"]) == 6
    for row in T["historical_region_portraits"]:
        assert row["individual_use_admitted"] is False
        assert m.source_record(row["source_record"])["output_type"] == "HISTORICAL_GROUP_CLAIM"
        assert row["source_universality_qualification"] == K["not_each"]
    assert T["no_individual_or_group_prediction_implemented"] is True


def test_main_text_and_commentator_are_not_merged():
    r = m.source_record(K["southern_middle"])
    a = m.source_record(K["named_middle"])
    assert r["source_locator"]["attribution_layer"] == "PTOLEMY_AS_TRANSLATED_BY_ROBBINS"
    assert a["source_locator"]["attribution_layer"] == "ANONYMOUS_AS_REPORTED_BY_ROBBINS"
    assert a["consequent"]["reported_identification"] == ["Egyptians", "Chaldaeans"]
    assert "probably" in m.source_record(K["posidonius"])["consequent"]["claim"]
    assert m.source_record(K["frank_variant"])["consequent"]["reported_alternatives"] == ["freedom of speech", "felicitous expression"]


def test_local_modifiers_and_nonuniversal_scope_survive():
    assert T["local_modifiers"]["geographical"] == ["situation", "height", "lowness", "adjacency"]
    assert len(T["local_modifiers"]["examples"]) == 3
    assert m.source_record(K["not_each"])["consequent"]["scope"] == "Generally present, but not in every individual."
    assert "No frequency" in m.source_record(K["not_each"])["modifiers"][0]


def test_deep_copy_return_values():
    d = m.definition("climes", "II.1_NOTE1"); d["meaning"] = "changed"
    assert m.definition("climes", "II.1_NOTE1")["meaning"] != "changed"
    d = m.general_inquiry_axes(); d["spatial"]["adopted"].clear()
    assert len(m.general_inquiry_axes()["spatial"]["adopted"]) == 2
    r = m.source_record(K["south"]); r["consequent"].clear()
    assert m.source_record(K["south"])["consequent"]


def test_unknown_record_is_not_an_empty_negative_result():
    with pytest.raises(KeyError):
        m.source_record("PT.R64.II.3.R999")
    with pytest.raises(ValueError):
        m.source_record(None)


def test_coverage_is_exact_once_even_on_shared_page145():
    c = json.loads((HERE / "SECTION_COVERAGE.json").read_text())
    assert [s["chapter"] for s in c["sections"]] == ["II.1", "II.2"]
    ids = [i for s in c["sections"] for i in s["record_ids"]]
    assert set(ids) == set(K.values()) and len(ids) == len(set(ids)) == 37
    assert [len(s["record_ids"]) for s in c["sections"]] == [16, 21]
    assert c["prior_bookI_end_not_recounted"] is True
    q = json.loads((HERE / "SOURCE_PAGE_QC.json").read_text())
    assert [p["pdf_page"] for p in q["pages"]] == [141, 143, 145, 147, 149, 151]
    assert q["new_ocr_calls"] == 0


def test_unresolved_links_are_resolvable():
    u = json.loads((HERE / "UNRESOLVED_INTERPRETATIONS.json").read_text())
    ids = {x["id"] for x in u["issues"]}
    assert len(ids) == u["count"] == 11
    for r in R["records"]:
        assert set(r["ambiguities"]) <= ids
    for row in T["glossary"] + T["historical_region_portraits"]:
        assert row["source_record"] in set(K.values())


def test_next_range_includes_shared_page185_without_counting_it_read():
    n = json.loads((HERE / "NEXT_HEADINGS.json").read_text())
    assert n["start"]["pdf_page"] == 153
    assert n["end"]["pdf_page"] == 185
    assert "before II.4" in n["end"]["boundary"]
    assert n["status"] == "HEADINGS_LOCATED_NOT_CHAPTER_READ"
