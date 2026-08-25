from __future__ import annotations

from hdmatch.human.astrodatabank_export import iter_astrodatabank_export


def test_parser_exposes_country_and_archive_source_provenance(tmp_path) -> None:  # type: ignore[no-untyped-def]
    xml = """<astrodatabank_export export_format="160715">
  <adb_entry adb_id="33">
    <public_data>
      <name>Charcot, Jean-Martin</name><gender>M</gender><roddenrating>AA</roddenrating>
      <datatype sdatatype="Public Figure" />
      <bdata>
        <sbdate iyear="1825" imonth="11" iday="29">1825/11/29</sbdate>
        <sbtime jd_ut="2387960.285185">19:00</sbtime>
        <place slati="48n52" slong="2e20">Paris</place>
        <country sctr="FR">France</country>
      </bdata>
      <scollector>Geslain</scollector>
      <seditor>LMR sco</seditor>
      <sbiographer>lmr</sbiographer>
    </public_data>
    <text_data>
      <shortbiography>French neurologist.</shortbiography>
      <sourcenotes>Birth certificate in Didier Geslain archive. Same data in Gauquelin.</sourcenotes>
    </text_data>
    <research_data><categories count="0" /></research_data>
  </adb_entry>
</astrodatabank_export>"""
    source = tmp_path / "adb.xml"
    source.write_text(xml, encoding="utf-8")
    record = next(iter_astrodatabank_export(source))
    assert record.birth_year == 1825
    assert record.birthplace == "Paris"
    assert record.country == "France"
    assert record.country_code == "FR"
    assert record.collector == "Geslain"
    assert record.editor == "LMR sco"
    assert record.biographer == "lmr"
    assert "Didier Geslain" in record.source_notes
    assert "Gauquelin" in record.source_notes
