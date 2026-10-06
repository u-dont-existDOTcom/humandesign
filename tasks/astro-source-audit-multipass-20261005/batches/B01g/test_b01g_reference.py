from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("b01g_reference", HERE / "b01g_reference.py")
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)
DATA = json.loads((HERE / "DIRECTION_REFERENCE.json").read_text())
F = HERE.parent / "B01f"

@pytest.mark.parametrize("row", DATA["rounded_examples"], ids=lambda r: r["case"])
def test_four_main_text_examples(row):
    assert m.directed_example_interval(
        row["initial_signed_distance"], row["target_signed_ordinary_hours"],
        row["horary_magnitude"]) == row["expected_interval"]

def test_note_precision_rising_replay():
    h = m.sexagesimal(17, 6, 30)
    initial = m.sexagesimal(147, 44)
    assert m.directed_example_interval(initial, 6, h) == pytest.approx(m.sexagesimal(45, 5))

def test_note_precision_setting_replay():
    h = m.sexagesimal(17, 6, 30)
    gemini_ra = m.sexagesimal(147, 44) - 90
    initial = gemini_ra - 90
    assert m.directed_example_interval(initial, -6, h) == pytest.approx(m.sexagesimal(70, 23))

def test_wrong_ocr_digit_does_not_match_note_result():
    wrong = m.directed_example_interval(m.sexagesimal(147, 14), 6, m.sexagesimal(17, 6, 30))
    assert wrong != pytest.approx(m.sexagesimal(45, 5))

@pytest.mark.parametrize("start,end,h,result",
                         [(58,70,3,64),(58,70,2,62),(70,58,2,66),(58,70,0,58),(58,70,6,70)])
def test_source_interpolation_and_endpoints(start,end,h,result):
    assert m.quadrant_interpolation(start,end,h) == result

def test_interpolation_endpoint_reversal_preserves_same_position():
    for h in (0,1,2,3,4,5,6):
        assert m.quadrant_interpolation(58,70,h) == m.quadrant_interpolation(70,58,6-h)

def test_signed_distance_is_not_silently_absolutized():
    assert m.directed_example_interval(-10, 1, 17) == -27

@pytest.mark.parametrize("sect", ["DAY","NIGHT"])
def test_main_text_fortune_both_sects(sect):
    assert m.fortune_main_text(350,20,40,sect=sect) == 10

def test_fortune_relation_and_rotation_invariant():
    for a,s,moon in [(1,2,3),(359,1,180),(20,220,35),(0,0,0),(270,300,10)]:
        f=m.fortune_main_text(a,s,moon,sect="DAY")
        assert (f-moon)%360 == (a-s)%360
        assert m.fortune_main_text(a,s,moon,sect="NIGHT") == f
        assert m.fortune_main_text(a+360,s-360,moon+720,sect="DAY") == f

def test_fortune_has_no_undeclared_sect():
    with pytest.raises(ValueError):
        m.fortune_main_text(0,0,0,sect="UNKNOWN")

@pytest.mark.parametrize("semiarc,expected",[(90,15),(102,17),(78,13)])
def test_ordinary_hour_uses_supplied_semiarc(semiarc,expected):
    assert m.ordinary_hour_magnitude(semiarc) == expected

@pytest.mark.parametrize("body,offset,expected",
                         [("JUPITER",0,True),("JUPITER",12,True),("JUPITER",12.001,False),
                          ("VENUS",8,True),("VENUS",8.001,False),("VENUS",359,False)])
def test_source_ray_limits_are_directional(body,offset,expected):
    assert m.protective_ray_distance_only(100,100+offset,body) is expected

def test_ray_window_wrap():
    assert m.protective_ray_distance_only(358,6,"VENUS")
    assert not m.protective_ray_distance_only(6,358,"VENUS")

def test_no_unspecified_benefic_limit():
    with pytest.raises(ValueError):
        m.protective_ray_distance_only(1,2,"MERCURY")

def test_cardanus_example_longitude_and_latitude():
    assert m.cardanus_opposition_example(10,3,190,-3)
    assert not m.cardanus_opposition_example(10,3,190,3)
    assert not m.cardanus_opposition_example(10,3,189,-3)

@pytest.mark.parametrize("value",[float("nan"),float("inf"),-float("inf")])
def test_nonfinite_rejected(value):
    with pytest.raises(ValueError):
        m.fortune_main_text(value,0,0,sect="DAY")

@pytest.mark.parametrize("value",["17",True])
def test_nonnumeric_and_bool_rejected(value):
    with pytest.raises(TypeError):
        m.ordinary_hour_magnitude(value)

def test_invalid_fields_and_ranges():
    for args in [(1,60,0),(1,0,60),(-1,0,0)]:
        with pytest.raises(ValueError): m.sexagesimal(*args)
    for arc in (0,180,-10):
        with pytest.raises(ValueError): m.ordinary_hour_magnitude(arc)
    for h in (-0.1,6.1):
        with pytest.raises(ValueError): m.quadrant_interpolation(58,70,h)
    with pytest.raises(ValueError): m.directed_example_interval(1,7,17)
    with pytest.raises(ValueError): m.directed_example_interval(1,1,0)
    with pytest.raises(ValueError): m.cardanus_opposition_example(10,91,190,-3)

def test_exact_record_sequence_and_scope():
    f=json.loads((F/"RULES.json").read_text())
    g=json.loads((HERE/"RULES.json").read_text())
    assert len(f["records"])==f["records_count"]==29
    assert len(g["records"])==g["records_count"]==34
    records=f["records"]+g["records"]
    assert [int(x["id"].rsplit("R",1)[1]) for x in records]==list(range(165,228))
    assert len({x["id"] for x in records})==63
    assert {x["source_locator"]["chapter_or_verse"] for x in records}=={"III.6","III.7","III.8","III.9","III.10"}
    for x in records:
        assert x["source_locator"]["source_file_sha256"]=="10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec"
        assert x["admission"]=="SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS"
        assert x["unknown_is_not_false"]
        assert x["source_locator"]["printed_support_pages"]==[p-24 for p in x["source_locator"]["pdf_support_pages"]]

def test_source_tables_keep_scope_and_precision_tracks():
    t=json.loads((F/"BIRTH_DOCTRINE_TABLES.json").read_text())
    assert len(t["named_triple_arrangements"])==4
    assert all(sum(x["source_claim"].values())==3 for x in t["named_triple_arrangements"])
    assert "Mercury specifically feminized" in t["named_triple_arrangements"][1]["conditions"]
    assert DATA["note_precision_track"]["do_not_replace_main_rounded_examples"]
    assert DATA["fortune"]["same_for_day_and_night"]
    assert not DATA["full_direction_engine_implemented"]
    assert tuple(DATA["prorogative_regions"]["priority"])==m.PROROGATIVE_PRIORITY

def test_receipt_page_ranges_do_not_claim_next_chapter():
    f=json.loads((F/"READING_RECEIPT.json").read_text())
    g=json.loads((HERE/"READING_RECEIPT.json").read_text())
    assert set(f["chapter_spans"])=={"III.6","III.7","III.8","III.9"}
    assert set(g["chapter_spans"])=={"III.10"}
    assert "before III.11" in g["end_boundary"]
    assert g["independent_greek_translation"] is False
    assert f["new_ocr_calls"]==g["new_ocr_calls"]==0
