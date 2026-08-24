from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.human.astrodatabank_export import (
    iter_astrodatabank_export,
    julian_day_ut_to_datetime,
)


def test_julian_day_ut_matches_documented_adb_example() -> None:
    # The export documentation's example is 1906-10-30 09:00 at h1e,
    # hence approximately 08:00 UTC.  The XML JD is rounded to 6 decimals.
    actual = julian_day_ut_to_datetime(2417513.833333)
    expected = datetime(1906, 10, 30, 8, 0, tzinfo=UTC)
    assert abs((actual - expected).total_seconds()) < 0.1


def test_julian_day_ut_rejects_nonfinite() -> None:
    with pytest.raises(ValueError, match="finite"):
        julian_day_ut_to_datetime(float("nan"))


def test_streaming_parser_extracts_birth_biography_and_categories(tmp_path) -> None:  # type: ignore[no-untyped-def]
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<astrodatabank_export export_format="160715">
  <adb_entry adb_id="1019">
    <timestamp itst="0">2016-01-01T00:00:00Z</timestamp>
    <public_data>
      <name>Fegelein, Hermann</name>
      <sflname>Hermann Fegelein</sflname>
      <gender csex="m">M</gender>
      <roddenrating rrc="1">AA</roddenrating>
      <datatype sdatatype="Public Figure" dtc="1" sdatasource="BC/BR in hand" dsc="1" />
      <bdata>
        <sbdate ccalendar="g" iyear="1906" imonth="10" iday="30">1906/10/30</sbdate>
        <sbtime sbtime_ampm="09:00 AM" ctimetype="s" stimetype="standard time"
          stmerid="h1e" jd_ut="2417513.833333" sznabbr="MET">09:00</sbtime>
        <place slati="49n18" slong="10e35">Ansbach</place>
        <country sctr="GER">Germany</country>
      </bdata>
    </public_data>
    <text_data>
      <shortbiography>German public figure with a busy career.</shortbiography>
    </text_data>
    <research_data>
      <categories count="2">
        <category cat_id="85" adb_id="1019" catnotes="Energetic">
          Traits : Personality : Active
        </category>
        <category cat_id="399" adb_id="1019">Vocation : Military</category>
      </categories>
    </research_data>
  </adb_entry>
</astrodatabank_export>
"""
    path = tmp_path / "adb.xml"
    path.write_text(xml, encoding="utf-8")
    records = list(iter_astrodatabank_export(path))
    assert len(records) == 1
    record = records[0]
    assert record.adb_id == 1019
    assert record.name == "Fegelein, Hermann"
    assert record.gender == "M"
    assert record.rodden_rating == "AA"
    assert record.data_type == "Public Figure"
    assert record.is_primary_timed_public_record is True
    assert record.birth_utc is not None
    assert abs(
        (record.birth_utc - datetime(1906, 10, 30, 8, 0, tzinfo=UTC)).total_seconds()
    ) < 0.1
    assert record.short_biography == "German public figure with a busy career."
    assert tuple(item.cat_id for item in record.categories) == (85, 399)
    assert record.categories[0].notes == "Energetic"


def test_alternative_birth_data_is_conservatively_ineligible(tmp_path) -> None:  # type: ignore[no-untyped-def]
    xml = """<astrodatabank_export export_format="160715">
  <adb_entry adb_id="2">
    <public_data>
      <name>Case, Alternative</name><gender>F</gender><roddenrating>A</roddenrating>
      <datatype sdatatype="Public Figure" />
      <bdata><sbtime jd_ut="2451545.0">12:00</sbtime></bdata>
      <bdata_alt><event_type event_id="4001">Misc.: Alternative birth time</event_type></bdata_alt>
    </public_data>
    <text_data><shortbiography>Example.</shortbiography></text_data>
    <research_data><categories count="0" /></research_data>
  </adb_entry>
</astrodatabank_export>"""
    path = tmp_path / "adb.xml"
    path.write_text(xml, encoding="utf-8")
    record = next(iter_astrodatabank_export(path))
    assert record.has_alternative_birth_data is True
    assert record.is_primary_timed_public_record is False


def test_untimed_record_is_not_primary_eligible(tmp_path) -> None:  # type: ignore[no-untyped-def]
    xml = """<astrodatabank_export export_format="160715">
  <adb_entry adb_id="3"><public_data><name>Case, Untimed</name><gender>M</gender>
  <roddenrating>AA</roddenrating><datatype sdatatype="Public Figure" />
  <bdata><sbtime>12:00</sbtime></bdata></public_data></adb_entry>
</astrodatabank_export>"""
    path = tmp_path / "adb.xml"
    path.write_text(xml, encoding="utf-8")
    record = next(iter_astrodatabank_export(path))
    assert record.birth_utc is None
    assert record.is_primary_timed_public_record is False
