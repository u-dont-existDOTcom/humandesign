"""One-time, source-bound reconciliation of the B02p changed-item review.

The source is Lilly 1647 original PDF323-324 preserved alongside this script.
Run only on the 2026-10-12 B02p draft; all changes are source-documentary.
"""
from pathlib import Path
import json
import hashlib

BASE = Path(__file__).resolve().parent

def read(name):
    return json.loads((BASE / name).read_text())

def write(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def replace(text, old, new):
    if old in text:
        return text.replace(old, new)
    if new in text:
        return text
    raise AssertionError("Missing expected source text: " + old[:120])

d = read("RULES.json")
rules = {int(r["id"][-4:]): r for r in d["rules"]}
assert list(rules) == list(range(1770, 1794))
def add_exception(n, message):
    e = rules[n]["exceptions_and_evidence_limits"]
    if message not in e:
        e.append(message)

rules[1771]["source_statement"] = replace(
    rules[1771]["source_statement"],
    "a Saturn planetary hour are separately identified",
    "a visually h-shaped Saturn planetary-hour glyph are separately identified",
)
add_exception(1771, "The hour symbol looks like a lowercase h-form in this print; the Saturn identification is medium-high confidence, not a modernized transcription.")
rules[1772]["source_statement"] = (
    "The horoscope prints a dated inscription and sector/cusp numerals, with some visible planetary glyphs. "
    "Most planetary signs and glyph-to-degree pairings cannot be securely reconstructed from the wheel; "
    "CHART_INSCRIPTION.json preserves direct readings and explicitly provisional assignments separately."
)
add_exception(1772, "No complete planet-sign table is printed or independently reconstructed; do not infer missing signs.")
add_exception(1777, "The sentence starts on printed289/PDF323 and continues at printed290/PDF324.")
for n in (1777,1789):
    rules[n]["source_locator"]["page_images"] = ["evidence/pdf-323.png", "evidence/pdf-324.png"]
rules[1789]["source_statement"] = replace(
    rules[1789]["source_statement"],
    "July28 minus July16",
    "the source's provisionally read July28 minus July16",
)
add_exception(1789, "The printed leading numeral of the reported death day is weak; July28 is a qualified reading, not authenticated patient data.")
add_exception(1789, "This date subtraction was added by the modern editor; Lilly does not print a twelve-day subtraction or a separately timed numerical forecast derivation.")
rules[1789]["historical_evidence_class"] = "EDITORIAL_ARITHMETIC_NOT_PATIENT_EVIDENCE"
rules[1790]["source_statement"] = replace(
    rules[1790]["source_statement"],
    "and there to a square with Saturn",
    "and 'therein' to a square with Saturn",
)
rules[1791]["source_statement"] = (
    "After reporting the death, Lilly says 'and the ☽ to an ☍ of the ☉' (Moon opposing Sun), "
    "then introduces 'the ☽ that day'; the antecedent of 'that day' is unresolved between "
    "the reported July28 and the immediately preceding day."
)
add_exception(1791, "The referent of the original phrase 'that day' is not established and must not be assigned automatically to July28 or July27.")
rules[1792]["source_statement"] = (
    "In the after-death account, Lilly writes 'the ☽ that day transiting the degree of the sixt house "
    "at time of the Question, viz. 14. of ♒', and the Sun the twelfth cusp; the SIXTH-house "
    "Aquarius reading replaces an earlier erroneous first-house Virgo interpretation."
)
add_exception(1792, "The source's 'that day' could refer to the stated July28 death or the preceding day; temporal resolution is not established.")
rules[1792]["exceptions_and_evidence_limits"] = [
    replace(s, "equivalence to 14 by ordinal degree is plausible but unproved",
            "ordinal-degree interpretation or rounding to 14 is possible but not proved")
    if "equivalence to 14 by ordinal degree" in s else s
    for s in rules[1792]["exceptions_and_evidence_limits"]
]
rules[1793]["historical_evidence_class"] = "EDITORIAL_BOUNDARY_NOT_PATIENT_EVIDENCE"
add_exception(1793, "This record marks only the next chapter's textual boundary; it is not another patient, reported outcome, or prognostic success.")
write("RULES.json", d)

chart = read("CHART_INSCRIPTION.json")
assert chart["inferred_proleptic_gregorian_equivalent"] == "1645-07-26"
chart["computed_extended_gregorian_equivalent"] = chart.pop("inferred_proleptic_gregorian_equivalent")
chart["gregorian_calculation_convention"] = "Proleptic/extended Gregorian calendar arithmetic; not a source-printed date or timezone conversion."
chart["calendar_note"] = (
    "The source prints 16 Julij 1645 and the Wednesday weekday only. In contextual English Julian "
    "dating this converts by proleptic Gregorian calendar arithmetic to 26 July 1645; "
    "neither 'Julian', 'Gregorian', a city nor an offset is printed."
)
chart["source_planetary_hour_glyph_qualification"] = (
    "Visual lowercase h-form in 1647 wheel; Saturn symbol ♄ is the medium-high-confidence "
    "historical glyph reading, not a source-modernized letter sequence."
)
chart["wheel_body_readings_provisional"] = [
    {
        "sector": "upper-left",
        "visible_glyph": "☉",
        "adjacent_degree_numerals": "3 29",
        "body_assignment": "Sun glyph legible",
        "sign_reading": "UNRESOLVED_FROM_THIS_LABEL",
        "confidence": "MEDIUM; numbers adjacent in figure, no new ephemeris calculation",
    },
    {
        "sector": "left, ascending sector",
        "visible_glyph": "♂",
        "adjacent_degree_numerals": "12 30 (association provisional)",
        "body_assignment": "Mars glyph legible; source prose also places Mars in the ascendant",
        "sign_reading": "UNRESOLVED_FROM_THIS_LABEL",
        "confidence": "LOW for exact glyph-to-degree association",
    },
    {
        "sector": "left, ascending sector below Mars",
        "visible_glyph": "☽",
        "adjacent_degree_numerals": "15 43 (association provisional)",
        "body_assignment": "Moon-like glyph; source prose puts Moon near Mars",
        "sign_reading": "UNRESOLVED_FROM_THIS_LABEL",
        "confidence": "LOW for digits and association, no exact longitude inferred",
    },
    {
        "sector": "upper planetary sectors",
        "visible_glyph": "several Mercury/Venus and Saturn-like marks",
        "adjacent_degree_numerals": "UNRESOLVED; cannot securely pair",
        "body_assignment": "UNRESOLVED",
        "sign_reading": "UNRESOLVED",
        "confidence": "LOW; do not turn wheel text into a complete planetary table",
    },
]
for row in chart["wheel_labels_provisional"]:
    if row["sector"] == "sixth cusp":
        row["confidence"] = "MEDIUM: chart glyph ♒ 13 32; prose separately says 'viz. 14. of ♒'; no ordinal/rounding equivalence established"
write("CHART_INSCRIPTION.json", chart)

case = read("CASE_EVIDENCE.json")
case["source_reported_death_text"] = "The sick dyed the 28th of July following"
case["normalized_death_word"] = "died"
case["normalization_note"] = "Printed 'dyed' is normalized to 'died' only in modern summaries; verbatim source retained above."
case["source_death_date_legibility"] = (
    "The leading numeral in printed '28th' is imperfect; 28 July is a medium-high "
    "but source-qualified reading with no independently authenticated patient death record."
)
case["reported_death_inferred_julian_date_qualification"] = (
    "1645-07-28 is inferred from the qualified text '28th of July following' and contextual Julian framing; not verified outcome evidence."
)
write("CASE_EVIDENCE.json", case)

u = read("UNRESOLVED.json")
byid = {x["id"]: x for x in u["limits"]}
byid["U03"]["description"] = (
    "Printed clock 7:22 AM: and hor h-shaped Saturn glyph are distinct; no printed longitude, "
    "timezone, UT offset or verified hour calculation."
)
byid["U21"]["description"] = (
    "Chapter XLVI is a separate dated enquiry and diagram from the 8 May XLV doctor case; "
    "whether the patients are the same or different individuals cannot be decided from these passages."
)
byid["U31"]["description"] = (
    "In the retrospective sequence Mercury comes to the degree of the Sun in the QUESTION figure "
    "and therein squares Saturn, lord of sixth. The Saturn point (radical/transiting) is not specified. "
    "Do not confuse this with the distinct earlier rationalizing Sun–Saturn square."
)
byid["U32"]["description"] = (
    "Chart sixth cusp ♒ 13°32′ and prose 'viz. 14. of ♒' do not establish equivalence. "
    "An ordinal fourteenth degree and/or rounding are hypotheses, not transcribed interpretations."
)
for item in [
    {"id":"U37","description":"In the retrospective lunar opposition/transit sequence 'that day' could refer to the reported July28 death date or the preceding day; print does not settle its antecedent.","status":"RETAINED"},
    {"id":"U38","description":"The identity of the person asking the question is not established from the Chapter XLVI source pages; do not assume Lilly questioned the patient himself.","status":"RETAINED"},
    {"id":"U39","description":"The planetary-hour Saturn sign is h-shaped in the printed chart and its historical glyph attribution is medium-high, not a definitive modern glyph transcription.","status":"RETAINED"},
    {"id":"U40","description":"Provisional planet-body glyph-to-degree association in the printed horoscope is not enough to reconstruct all zodiac signs or a certified ephemeris; no positions are silently filled.","status":"RETAINED"},
]:
    if item["id"] not in byid:
        u["limits"].append(item)
u["retained_count"] = len(u["limits"])
write("UNRESOLVED.json", u)

report = (BASE/"AUDIT_REPORT.md").read_text()
report = replace(report, "a **separate** Saturn planetary-hour designation",
    "a **separate** Saturn planetary-hour designation (visually an h-shaped sign, medium-high-confidence Saturn identification)")
report = replace(report, "**16 July Julian** (equivalent to Gregorian 26 July, also a Wednesday)",
    "**16 July Julian** (equivalent to 26 July on the extended/proleptic Gregorian calendar, also a Wednesday)")
report = replace(report,
    "from the printed May 8 Chapter XLV sick-doctor case. There is no source proof that the two passages concern different patients.",
    "from the previously accepted Chapter XLV sick-doctor figure dated 8 May 1645. These are distinct questions and charts; the passages do not determine whether the two patients are identical or different.")
report = replace(report,
    "Chapter XLV's previously mistaken May 24 caption has already been explicitly corrected in its accepted packet; the present July 16 chart does not supersede or explain that first case. [PDF323; prior B02o source record; U21]",
    "Chapter XLV's previously mistaken May24 caption was corrected using **the B02o source images and correction record**, not from the present PDF323; the July16 chart neither supersedes nor explains that earlier case. [B02o/CHAPTER_XLV_DATE_CORRECTION.md; B02o/CHART_INSCRIPTION.json; R1771; U21]")
report = replace(report, "is described as especially afflicted by the **bodily presence of Mars**",
    "is described as **most afflicted** by the **corporeal presence of Mars**")
report = replace(report,
    "the Sun's asserted perfect square to Saturn, the sixth ruler in fixed signs; Mars physically at the ascendant and substantially associated with the eighth;",
    "the Sun's asserted perfect square to Saturn as sixth ruler, **both in fixed signs**; Mars physically at the ascendant, naturally adverse and **accidentally almost** ruler of the eighth;")
report = replace(report,
    "followed by virtue transferred to Jupiter as eighth lord. All four are preserved",
    "followed by virtue transferred to Jupiter as eighth lord (Mercury is the ascendant ruler, and the antecedent of 'his vertue' remains unresolved). All four are preserved")
report = replace(report, "The text then reports that the patient **died on 28 July following**.",
    "The text then reports that the patient **'dyed' on the provisionally read 28 July following** (the first date digit is weakly printed; 'died' is modernized wording).")
report = replace(report, "July 28 minus July 16 is **12 days by exclusive subtraction**",
    "The qualified July28 reading minus July16 is **12 days by exclusive subtraction**")
report = replace(report,
    "The remaining Mercury/Sun/Saturn and Moon/Sun/cusp descriptions occur **after the death statement**.",
    "The remaining passage says Mercury came to the **question-figure Sun's degree** and 'therein' squared Saturn; this is separate from Lilly's earlier Sun–Saturn rationale. It then says the Moon opposed the Sun, and the Moon **'that day'** transited the sixth cusp; the referent of 'that day' (reported July28 or preceding day) is unresolved. These Mercury/Sun/Saturn and Moon/Sun/cusp descriptions occur **after the death statement**.")
report = replace(report,
    "The unresolved ledger retains **36 explicit issues**",
    f"The unresolved ledger retains **{u['retained_count']} explicit issues**")
report = replace(report, "an ordinal fourteenth degree is possible, not proven",
    "an ordinal-fourteenth-degree reading or rounding is possible, but neither is printed or proven")
report = replace(report, "but no printed UTC offset, location or external ephemeris is established.",
    "but the printed h-shaped Saturn planetary-hour glyph, modern time standard, UTC offset, location and external ephemeris have not all been independently established.")
report = replace(report,
    "Chapter XLVII — Of the Crisis in Diseases",
    "Chapter XLVII — Of the **CRYSIS** in Diseases")
report = replace(report,
    "The wheel has provisional house-cusp labels and unresolved Venus/Mercury glyph assignments.",
    "The wheel has provisional house-cusp labels and a provisional glyph/adjacent-numerals table; most planet signs, including Venus/Mercury associations, remain unresolved.")
(BASE/"AUDIT_REPORT.md").write_text(report)

# Recreate original ledger paragraph segmentation, preserving stable C IDs.
units = [s for s in report.strip().split("\n\n")]
assert len(units)==26, f"unexpected paragraphs {len(units)}"
ledger=read("CLAIM_LEDGER.json")
assert len(ledger["units"])==26
for i,unit in enumerate(ledger["units"]):
    assert unit["id"]==f"C{i+1:02d}"
    unit["text"]=units[i]
    unit["sha256"]=hashlib.sha256(units[i].encode()).hexdigest()
# The original last ledger text includes the final trailing newline.
ledger["units"][-1]["text"] += "\n"
ledger["units"][-1]["sha256"]=hashlib.sha256(ledger["units"][-1]["text"].encode()).hexdigest()
ledger["report_sha256"]=hashlib.sha256((BASE/"AUDIT_REPORT.md").read_bytes()).hexdigest()
write("CLAIM_LEDGER.json", ledger)

print(json.dumps({"patched":"B02p narrow second-review repair","records":len(rules),"unresolved":u["retained_count"],"claim_units":len(ledger["units"]),"report_sha256":ledger["report_sha256"]},indent=2))
