from pathlib import Path
import json
root = Path(__file__).resolve().parent
t4 = json.loads((root/"batches/T04/WHITE_BERYL_60_PROFILES_V1.json").read_text())
t5 = json.loads((root/"batches/T05/WHITE_BERYL_NATAL_CONDITIONAL_21_SOURCE_NOTES.json").read_text())
notes = t5["source_notes"]
assert len(notes) == t5["note_count"] == 21
assert [x["id"] for x in notes] == [f"TIB-R{i:04d}" for i in range(92,113)]
assert {x["id"] for x in notes}.isdisjoint({x["source_note_id"] for x in t4["profiles"]})
assert t5["source_pdf_sha256"] == t4["source_pdf_sha256"]
assert t5["human_predictions_tested"] == 0
assert all(x["empirical_human_validation"] is False and x["runtime_promoted"] is False for x in notes)
assert all(156 <= x["anchor"]["pdf_page_1based"] <= 163 for x in notes)
trigrams = [x["kind"] for x in notes if x["kind"].endswith("-natal-trigram")]
assert trigrams == [f"{v}-natal-trigram" for v in ("Li","Khon","Dva","Khen","Kham","Gin","Zin","Zon")]
by_kind = {x["kind"]: x for x in notes}
assert "mother_natal_trigram_or_mewa" in by_kind["five-maternal-grades"]["required_inputs"]
assert "father_natal_year_animal" in by_kind["three-paternal-year-sector-wheels"]["required_inputs"]
assert "exact elemental lookup" in ' '.join(t5["known_gaps"]).lower() or "lookup tables" in ' '.join(t5["known_gaps"]).lower()
print("T05 SOURCE-ONLY PASS: 21 contiguous notes, eight natal trigrams, no human validation")
