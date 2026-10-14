"""One-time source-witness correction: PDF381/printed347 Sun vs Moon.
Preserves byte-identical producer proposal before any mutation. Does not accept B02v.
"""
from pathlib import Path
import json, hashlib

B = Path(__file__).resolve().parents[1]
rec = B / "recovery"
source = B / "PRODUCER_SOURCE_DRAFT_P381_384.json"
backup = rec / "producer_p381_384_before_20261014_sun_review.json"
assert not backup.exists(), "Already corrected; do not reapply. Inspect recovery."
raw = source.read_bytes()
data = json.loads(raw)
assert len(data["units"]) == 61
a,b = data["units"][3:5]
assert a["kind"] == "fortune_like_house_marker", a
assert b["kind"] == "fortune_oriental_house_east", b
assert a["normalized_historical_statement"] == "The printed circular fortune-like glyph's zodiacal place is assigned to the thief's house, while the Moon's place is assigned to the house door."
assert b["normalized_historical_statement"] == "If the printed house-marker glyph is in an oriental sign, Lilly claims the house lies eastward from the master or property loser."

a["kind"] = "sun_as_thief_house_marker"
a["normalized_historical_statement"] = "Lilly assigns the Sun's (☉) place to the house the thief is in, and the Moon's (☽) place to the door of that house."
a["preconditions"] = ["Original PDF381/printed347 explicitly gives the place of Sun for the thief's house and the place of Moon for its door."]
a["exceptions_and_uncertainty"] = ["Image-first visual correction: the Sun glyph has an interior dot, not a Part-of-Fortune cross; this historical locational assertion has no verified outcome."]
a["source_glyph_visual_review"] = "Sun ☉, Moon ☽ — original PDF381/printed347; source image authoritative"
b["kind"] = "sun_oriental_house_east"
b["normalized_historical_statement"] = "If Sun (☉) is in an oriental sign, Lilly places the house in the eastern part relative to the master or the one who lost the goods."
b["preconditions"] = ["Sun, rather than an unspecified fortune-like point, is in an oriental sign."]
b["source_glyph_visual_review"] = "Original PDF381/printed347 prints Sun ☉ before 'Orientall Signe'."
assert all(r["pdf_pages"] == [381] for r in [a,b])

er = B / "ERRATA_COLLATION.json"
err = json.loads(er.read_text())
e = err["candidate_in_scope"][0]
assert e["printed_page"] == 360 and e["original_pdf_page"] == 394 and e["body_line_located"] is False
e["body_line_located"] = True
e["body_passage_anchor"] = "PDF394/printed360, 'Most Planets in cadents, he shall be knowne' followed by Sun/aspect glyphs, under 'Whether the Thief shall be knowne or not'."
e["read_word_or_glyph_verified"] = False
e["action"] = "Body line now visually located; exact substitution after the printed errata 'p 360 l 4 r' remains ambiguous, and no glyph has been emended."

un = B / "UNRESOLVED_DRAFT.json"
unresolved = json.loads(un.read_text())
issues = {i["id"]:i for i in unresolved["issues"]}
assert "U05" in issues and "U22" in issues
issues["U05"]["description"] = "Image-first p347 review distinguishes the Sun (☉) location of thief's house from Moon (☽) door of that house; the earlier 'fortune-like glyph' producer gloss was corrected, with original bytes retained. PDF387/printed353 separately describes entry placement."
issues["U22"]["description"] = "Original printed p360 line4 erratum has been visually located at PDF394's 'Most Planets in cadents' clause about knowledge of thief; exact replacement aspect glyph remains unclear. No silent emendation."

rec.mkdir(exist_ok=True)
backup.write_bytes(raw)
source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
er.write_text(json.dumps(err,ensure_ascii=False,indent=2)+"\n")
un.write_text(json.dumps(unresolved,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_sha256":hashlib.sha256(raw).hexdigest(),
 "corrected_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
 "source_units_preserved":len(data["units"]),
 "corrected_source_kinds":[a["kind"],b["kind"]],
 "erratum_body_line_located":True,"erratum_exact_glyph_still_unresolved":True,
 "b02v_accepted":False},indent=2))
