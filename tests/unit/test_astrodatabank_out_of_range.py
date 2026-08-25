from __future__ import annotations

from hdmatch.human.astrodatabank_export import iter_astrodatabank_export


def test_out_of_python_range_julian_date_does_not_abort_stream(tmp_path) -> None:  # type: ignore[no-untyped-def]
    xml = """<astrodatabank_export export_format="160715">
  <adb_entry adb_id="1">
    <public_data>
      <name>Ancient</name><gender>M</gender><roddenrating>AA</roddenrating>
      <datatype sdatatype="Public Figure" />
      <bdata>
        <sbdate iyear="-5000" imonth="1" iday="1">-5000/01/01</sbdate>
        <sbtime jd_ut="-1000000">12:00</sbtime>
        <place>Unknown</place><country sctr="XX">Unknown</country>
      </bdata>
    </public_data>
    <text_data><shortbiography /><sourcenotes /></text_data>
    <research_data><categories count="0" /></research_data>
  </adb_entry>
  <adb_entry adb_id="2">
    <public_data>
      <name>Modern</name><gender>F</gender><roddenrating>AA</roddenrating>
      <datatype sdatatype="Public Figure" />
      <bdata>
        <sbdate iyear="2000" imonth="1" iday="1">2000/01/01</sbdate>
        <sbtime jd_ut="2451544.5">00:00</sbtime>
        <place>Paris</place><country sctr="FR">France</country>
      </bdata>
    </public_data>
    <text_data><shortbiography /><sourcenotes /></text_data>
    <research_data><categories count="0" /></research_data>
  </adb_entry>
</astrodatabank_export>"""
    source = tmp_path / "adb.xml"
    source.write_text(xml, encoding="utf-8")
    records = tuple(iter_astrodatabank_export(source))
    assert len(records) == 2
    assert records[0].jd_ut == -1000000.0
    assert records[0].birth_utc is None
    assert not records[0].is_primary_timed_public_record
    assert records[1].birth_utc is not None
    assert records[1].is_primary_timed_public_record
