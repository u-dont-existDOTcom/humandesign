"""Build the root reader's source records, without changing earlier batches."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = "LILLY1647_WELLCOME_B30338724"
SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


records = []


def add(chapter, section, pages, title, assertion, anchor, kind="rule",
        conditions=(), exceptions=(), uncertainty=(), calculation=None, case=None):
    record = {
        "id": f"C{len(records)+1:03d}", "chapter": chapter,
        "section": section, "pdf_pages": pages,
        "printed_pages": [p - 34 for p in pages], "title": title,
        "anchor": anchor,
        "anchor_type": "normalized locating phrase, not a diplomatic quotation",
        "kind": kind, "conditions": list(conditions),
        "condition_logic": {"all": list(conditions)},
        "assertion": assertion, "exceptions": list(exceptions),
        "uncertainty": list(uncertainty),
        "scope": "historical horary source only",
        "evidence_class": "retrospective_author_narrative" if case else "source_method",
        "case_id": case,
        "independent_evidence_unit": False,
        "calculation": calculation,
    }
    records.append(record)
    return record["id"]


CASE1 = "LILLY_II_XLII_1635_CHILDREN"
CASE2 = "LILLY_II_XLIII_1645_BIRTH"

add("XLII", "first_figure", [272], "Lifetime children enquiry and dated figure",
    "The question asks whether the querent should ever have children. The figure records 11 June 1635, Thursday, 2:30 P.M., with Jupiter as the astrological hour ruler.",
    "If the Querent should ever have Children?; Die Jupiter 11 Iune 1635", "illustration",
    uncertainty=["C11"], case=CASE1)
add("XLII", "negative_judgment", [272, 273], "Barren and indifferent sign testimonies",
    "Lilly calls the Virgo Ascendant barren, the Capricorn fifth sign indifferent for this question, the Moon's sign barren, and Saturn in Sagittarius and Mercury in Gemini rather barren than fruitful.",
    "The ascendant is here Virgo a barren Signe; a Signe of indifferency",
    conditions=["Interpreting the printed 1635 figure"], case=CASE1)
add("XLII", "negative_judgment", [273], "Afflictions and shared fifth/sixth ruler",
    "Saturn is retrograde; Moon in Mars's terms squares Saturn; Mercury in Saturn's terms is with Mars and goes to Saturn opposition; Saturn rules both fifth and sixth; the South Node occupies the Ascendant. Lilly treats these as adverse testimonies.",
    "Saturn Lord of the fift house is Retrograde; who is Lord of the sixt, as well as of the fift",
    conditions=["Interpreting the printed 1635 figure"], uncertainty=["C07"], case=CASE1)
add("XLII", "negative_judgment", [273], "Past nonconception and lifelong negative judgment",
    "On the listed testimonies Lilly says the querent had not conceived and would never conceive, describing her as naturally barren; first/tenth/fourth affliction makes him infer the impediment was longstanding and would continue.",
    "neither had been ever yet conceived; the first, tenth and fourth houses",
    conditions=["Lilly found the preceding negative configuration"],
    uncertainty=["C01"], case=CASE1)
add("XLII", "counterfactual_qualification", [273], "Jupiter contact would soften the categorical negative",
    "Lilly would have been less categorical had Jupiter fortunated the fifth cusp, aspected the Ascendant ruler or Saturn, or had reception existed between Saturn and Jupiter or between Jupiter and Mercury.",
    "Had I found Jupiter either fortunating the cusp of the fift house",
    exceptions=["These are stated counterfactual alternatives; not an assertion that they occurred."], case=CASE1)
records[-1]["condition_logic"] = {"any": ["Jupiter fortunates fifth cusp", "Jupiter aspects Mercury", "Jupiter aspects Saturn", "reception Saturn/Jupiter", "reception Jupiter/Mercury"]}
add("XLII", "counterfactual_qualification", [273], "Reception-qualified collection would soften judgment",
    "Collection of light from Mercury to Saturn, with the collecting planet receiving Saturn or Mercury, would also have made Lilly less categorical.",
    "any collection of light from Mercury to Saturn; received Saturn or Mercury",
    conditions=["A planet collects light from Mercury to Saturn", "That collector receives Saturn or Mercury"],
    exceptions=["Counterfactual in this worked narrative; not an observed successful exception."], case=CASE1)
add("XLII", "negative_judgment", [273], "No promising testimony in the author's assessment",
    "Lilly says he found no promising testimony and therefore judged against conception or children; this is his assessment of this figure, not this audit's independent exhaustive chart evaluation.",
    "when I found no one promising testimony", "author_report",
    uncertainty=["C01", "C07"], case=CASE1)
add("XLII", "reported_health", [273], "Reported illness and source-body attribution",
    "The account describes the querent as sickly, with wind and colic in belly/small guts and head pain; Lilly links these to Moon–Saturn, Mercury–Saturn/Mars and the South Node, and cites the Mercury-in-Gemini body table on printed119.",
    "very sickly, and extreamly afflicted with the Wind and Cholick", "author_report",
    uncertainty=["C02"], case=CASE1)
marks = [
    ("navel", "One mole close by the navel; the sentence does not explicitly assign a separate astrological cause to this first item."),
    ("right_ankle", "One on the right ankle, assigned to Aquarius on the sixth cusp."),
    ("right_knee_inner_thigh", "One toward the right knee on the inner side of the thigh, assigned to Saturn, lord of sixth, in Sagittarius."),
    ("genital_region", "One in or near the genital member, assigned to Moon in Virgo."),
    ("right_arm", "A scar or mole on the outside of the right arm, assigned to Mercury, Ascendant ruler, in Gemini."),
]
for label, assertion in marks:
    add("XLII", "reported_marks", [273], "Reported bodily mark: " + label,
        assertion, "Shee affirmed, that the Moles of her Body did correspond", "author_report",
        uncertainty=["C02"], case=CASE1)
add("XLII", "nativity_check", [274], "Consult nativity for a categorical negative",
    "For a question so categorical in the negative, enquire birth time, cast the nativity, compare radix with question and use discretion.",
    "When you find a Question that is so peremptory in the negative", "method",
    conditions=["A strongly negative horary judgment of this kind"], uncertainty=["C03"])
add("XLII", "nativity_check", [274], "Natal barrenness takes precedence in the stated comparison",
    "Lilly states that if the radix affirms barrenness, no promising horary question can contradict that signification.",
    "if the Radix affirme Barrennesse", "qualification",
    conditions=["The radix affirms barrenness"], uncertainty=["C03"])
add("XLII", "first_question_similarity", [274], "First-question Ascendant resemblance claim",
    "Lilly says that in a person's first question he usually finds the same Ascendant triplicity as the nativity, and often the same sign and degree; he attributes this to his experience.",
    "I meane in their first Question; found by experience", "author_report",
    uncertainty=["C04"])
add("XLII", "first_question_similarity", [274], "Gemini–Libra–Aquarius illustration",
    "Gemini rising in a nativity, with Libra or Aquarius rising in a horary question, illustrates the same-triplicity claim.",
    "for if Gemini ascend in the Nativity", "illustration",
    exceptions=["Illustration, not another enumerated observation."], uncertainty=["C04"])
add("XLIII", "second_figure", [274], "Child-sex and delivery-time enquiry",
    "The second figure asks whether the child is male or female and when delivery will occur, dated 7 April 1645 at 2:15 P.M. Its central labels place Moon beside both day and hour.",
    "If one were with Child of a Male or Female; 7 Apri 1645", "illustration",
    uncertainty=["C05", "C08", "C11"], case=CASE2)
add("XLIII", "sex_testimony_method", [275], "Plurality of proper-significator testimonies",
    "Lilly says he used the plurality of masculine or feminine testimonies of the proper significators to resolve this example.",
    "considered onely the plurality of testimonies", "method",
    uncertainty=["C09"], case=CASE2)

votes = [
    ("F1", "female", "Ascendant sign Virgo is feminine", ["ascendant_sign"]),
    ("F2", "female", "Fifth-house sign Capricorn is feminine", ["fifth_sign"]),
    ("F3", "female", "Moon is in a feminine sign", ["Moon", "Capricorn"]),
    ("F4", "female", "Mercury, Ascendant ruler, is with Venus, a feminine planet", ["Mercury", "Venus", "ascendant_ruler"]),
    ("M1", "male", "Mercury, Ascendant ruler, is in a masculine sign", ["Mercury", "Aries", "ascendant_ruler"]),
    ("M2", "male", "Saturn, fifth ruler, is a masculine planet", ["Saturn", "fifth_ruler"]),
    ("M3", "male", "Saturn, fifth ruler, is in a masculine sign", ["Saturn", "Aries", "fifth_ruler"]),
    ("M4", "male", "Moon is in a masculine house", ["Moon", "house_convention"]),
    ("M5", "male", "Saturn is in a masculine house", ["Saturn", "house_convention"]),
    ("M6", "male", "Jupiter, lord of the hour, is masculine", ["Jupiter", "hour_lord"]),
    ("M7", "male", "Jupiter is in a masculine sign", ["Jupiter", "Gemini", "hour_lord_chain"]),
    ("M8", "male", "Mercury applies to Mars's square, and Mars is masculine", ["Mercury", "Mars", "aspect_chain"]),
]
for label, direction, assertion, dependencies in votes:
    rid = add("XLIII", "sex_testimony_table", [275], "Printed sex testimony " + label,
        assertion + ".", "Arguments of a Girle / Significations of a Male Child", "illustration",
        uncertainty=["C05"] if label in ["M6", "M7"] else (["C10"] if label in ["M4", "M5"] else ["C09"]),
        case=CASE2)
    records[-1]["testimony_direction"] = direction
    records[-1]["dependencies"] = dependencies
    records[-1]["testimony_id"] = label
add("XLIII", "sex_result", [275], "Eight-to-four conclusion and reported male birth",
    "The printed tally is eight male testimonies and four female. Lilly says he therefore judged a male child, adding that it proved so.",
    "eight testimonies; but four; and so it proved", "author_report",
    uncertainty=["C05", "C09"], calculation="printed_table_count", case=CASE2)
add("XLIII", "delivery_method", [276], "Movable signs tempered by slow Saturn",
    "The movable fifth sign Capricorn and Aries containing the first/fifth rulers suggest a short time, but Lilly gives much weight to slow, ponderous Saturn and to Moon in the sign of the fifth.",
    "because Saturn Lord of the fift is a ponderous Planet", "method",
    uncertainty=["C12"], case=CASE2)
add("XLIII", "delivery_arithmetic", [276], "Moon–Saturn square distance",
    "The table gives Saturn 24°37′ Aries and Moon 9°50′ Capricorn, both cardinal signs; the remaining distance of Moon to Saturn's square is 14°47′.",
    "Locus Saturn in 24 37 Aries; Locus Moon in 9 50 Capricorn", "illustration",
    calculation="moon_to_saturn_square_static", case=CASE2)
add("XLIII", "delivery_arithmetic", [276], "Mercury–Saturn conjunction distance",
    "The second table gives Saturn 24°37′ Aries and Mercury 11°00′ Aries; their difference is 13°37′.",
    "Saturn 24 37 Aries; Mercury 11 00 Aries; Distance13", "illustration",
    uncertainty=["C08"], calculation="mercury_to_saturn_conjunction_static", case=CASE2)
add("XLIII", "delivery_arithmetic", [276], "Difference of distances and local degree-to-week rule",
    "The two distances differ by 1°10′. Lilly assigns one week to every degree and judges delivery about fourteen weeks after the question.",
    "one degree and ten minutes; for every degree one week", "method",
    uncertainty=["C12"], calculation="two_distances_and_local_scale", case=CASE2)
add("XLIII", "delivery_result", [276], "Reported delivery on 11 July",
    "Lilly reports delivery on 11 July following the 7 April question.",
    "she was delivered the eleventh of July following", "author_report",
    uncertainty=["C11", "C12"], calculation="same_calendar_date_interval_only", case=CASE2)
add("XLIII", "reported_birth_transits", [276], "Mars and Mercury transits reported at delivery",
    "The narrative says Mars transited the question's Ascendant degree, and Mercury the opposite place of the question Moon, described as the tenth degree of Cancer.",
    "Mars transited the degree ascending; the opposite place of the Moon", "author_report",
    uncertainty=["C11", "C13"], case=CASE2)
add("XLIII", "reported_birth_transits", [276], "Reported exact Sun square and Moon–Mercury conjunction",
    "The narrative gives Sun 27°48′ Cancer on that day and calls this a perfect square to its figure position; it also reports Moon in Cancer conjunct Mercury. The figure itself reads Sun 27°52′.",
    "Sun the same day is in 27.48 Cancer; in perfect square", "author_report",
    uncertainty=["C06", "C11", "C13"], case=CASE2)


def coord(label, sign, degree, minute, basis="printed", **extra):
    return {"label": label, "sign": sign, "degree": degree, "minute": minute,
            "sign_basis": basis, **extra}


def cusps(rows):
    return [coord(f"cusp{i}", *row) for i, row in enumerate(rows, 1)]


fig1 = {
    "id": CASE1, "source_pdf_page": 272, "printed_page": 238,
    "date_text": "11 Iune 1635", "time_text": "2:30 P.M.",
    "day_lord_printed": "Jupiter", "hour_lord_printed": "Jupiter",
    "calendar": "SOURCE_UNSPECIFIED_NO_UTC_CONVERSION",
    "cusps": cusps([
        ("Virgo",3,46), ("Virgo",24,33), ("Libra",19,20),
        ("Scorpio",25,0), ("Capricorn",7,40), ("Aquarius",10,30),
        ("Pisces",3,46), ("Pisces",24,33), ("Aries",19,10),
        ("Taurus",25,0), ("Cancer",7,40), ("Leo",10,30)]),
    "points": [
        coord("Sun","Cancer",0,31,"diagram_position_inference", note="No immediately adjacent solar sign; retained as declared inference for arithmetic, not independent astronomical verification."),
        coord("Moon","Virgo",29,53,"diagram_and_narrative"),
        coord("Mercury","Gemini",24,45,"printed_shared_brace"),
        coord("Venus","Taurus",20,45,"diagram_position_inference"),
        coord("Mars","Gemini",18,30,"printed_shared_brace"),
        coord("Jupiter","Leo",5,0,"diagram_position_inference", note="Assumed Leo from figure placement; Part-of-Children replay is conditional on this reading."),
        coord("Saturn","Sagittarius",20,24,"printed_shared_brace", retrograde=True),
        coord("SouthNode","Virgo",4,40,"diagram_position_inference"),
        coord("NorthNode","Pisces",4,40,"diagram_position_inference"),
        coord("Fortune","Sagittarius",3,8,"printed_shared_brace"),
        coord("PartOfChildren","Libra",20,16,"diagram_position_inference", note="Entry gives20:16 in the third sector; sign is not printed beside the Part label.")
    ],
    "known_printed_discrepancy": "Third/ninth cusp minutes differ by10′; neither is repaired.",
}
fig2 = {
    "id": CASE2, "source_pdf_page": 274, "printed_page": 240,
    "date_text": "7 Apri 1645", "time_text": "2:15 P.M.",
    "day_lord_printed": "Moon", "hour_lord_printed": "Moon",
    "hour_lord_in_testimony_table": "Jupiter",
    "calendar": "SOURCE_UNSPECIFIED_NO_UTC_CONVERSION",
    "cusps": cusps([
        ("Virgo",8,50), ("Virgo",29,50), ("Libra",25,20),
        ("Sagittarius",2,20), ("Capricorn",14,1), ("Aquarius",15,50),
        ("Pisces",8,50), ("Pisces",29,50), ("Aries",25,20),
        ("Gemini",2,20), ("Cancer",14,1), ("Leo",15,50)]),
    "points": [
        coord("Sun","Aries",27,52,"diagram_and_narrative_context", alternative_source_value={"pdf_page":276,"sign":"Cancer","degree":27,"minute":48,"role":"reported birth-day square, not question-chart replacement"}),
        coord("Moon","Capricorn",9,50,"diagram_and_printed242_table"),
        coord("Mercury","Aries",11,None,"diagram_and_printed242_table", minute_note="Diagram omits minutes; printed242 arithmetic table explicitly supplies00.", arithmetic_table_value={"pdf_page":276,"sign":"Aries","degree":11,"minute":0}),
        coord("Venus","Aries",5,36,"diagram_position_inference"),
        coord("Mars","Cancer",13,20,"diagram_plus_square_testimony_inference", note="Cancer follows the stated Mercury–Mars square; sign not printed directly with the Mars value."),
        coord("Jupiter","Gemini",15,20,"diagram_position_inference"),
        coord("Saturn","Aries",24,37,"diagram_and_printed242_table"),
        coord("NorthNode","Leo",24,11,"diagram_position_inference"),
        coord("SouthNode","Aquarius",24,11,"diagram_position_inference"),
        coord("Fortune","Taurus",20,48,"printed_adjacent_sign")
    ],
}

issues = [
    ("C01","evidence_limit",[272,273],"No lifetime endpoint for the negative case","Past nonconception and lifelong nonconception are the author's judgment; no independently verified history or lifetime follow-up is given in the admitted case."),
    ("C02","evidence_limit",[273],"Symptoms and five marks belong to one retrospective case","The mole/scar confirmation and symptoms are narrated by Lilly, with no separate blinded elicitation or independent case denominator. They do not establish clinical validity."),
    ("C03","implementation_limit",[274],"Natal override needs its own source-complete natal procedure","The precedence statement is explicit; this horary span does not supply a complete natal barrenness algorithm or the1635 querent's nativity."),
    ("C04","evidence_limit",[274],"First-question resemblance lacks counts","Usually/often is not accompanied by a denominator, comparison distribution or independently checkable series; the Gemini example is illustrative."),
    ("C05","source_conflict",[274,275],"Moon-versus-Jupiter hour ruler","The figure's day/hour brace shows Moon; the table counts Jupiter as hour ruler and separately its masculine sign. Retain both without choosing a repair. A coherent two-row hour-chain substitution is an analyst sensitivity calculation, not Lilly's alternative judgment."),
    ("C06","source_conflict",[274,276],"Four-minute solar mismatch","Question figure Sun 27°52′ differs from the27°48′ used for the later perfect-square claim. Exact geometry gives a4′ mismatch; no change is made to the source."),
    ("C07","input_and_calculation_limit",[272,273],"1635 chart is transcribed, not independently recomputed","Several signs are inferred from diagram placement. Printed third/ninth cusps retain Libra19°20′ and Aries19°10′. Terms, application and source judgment are not ephemeris-validated by a static replay."),
    ("C08","input_qualification",[274,276],"Mercury minutes come from the later table","The figure gives Mercury 11 degrees with no minutes. The later calculation prints11°00′; preserve the missing figure field and explicit second witness rather than silently zero-filling."),
    ("C09","dependence_and_model_limit",[275],"Twelve testimonies are not independent evidence","The table reuses Mercury, Saturn, Moon, Jupiter, sign and house roles. Its8:4 plurality is a literal table count, not calibrated probability or an independent-observation denominator."),
    ("C10","interpretation_limit",[274,275],"House-gender votes and cusp virtue","Moon and Saturn lie in geometric sectors4 and8 but within5° before cusps5 and9. The earlier cusp-virtue rule is a plausible qualification, not an explicitly stated resolution here. Preserve geometry, source votes and inference separately."),
    ("C11","calendar_and_ephemeris_limit",[272,274,276],"Unspecified time/calendar and unverified historical transits","The source labels dates and P.M. times but these pages do not state modern timezone, exact observation location, Gregorian conversion or birth-hour inputs. Same-calendar date subtraction is distinct from an ephemeris calculation."),
    ("C12","implementation_and_evidence_limit",[276],"About fourteen weeks is not a frozen exact target","The local one-week-per-degree rule is explicit, but the averaging/rounding/selection rule and prior tolerance for about are not. Do not optimize a conversion against the known11 July report."),
    ("C13","evidence_limit",[276],"Reported birth-day transits are retrospective support","Mars/Ascendant, Mercury/Moon, Sun square and Moon/Mercury statements appear after the reported birth date, without separate advance freezes or external corroboration; they are not four new predictions.")
]

write("ROOT_CANDIDATE_RULES.json", {"reader":"root", "records":records})
write("ROOT_UNRESOLVED.json", {"issues":[{"id":i,"type":t,"pdf_pages":p,"title":title,"detail":detail,"status":"OPEN"} for i,t,p,title,detail in issues]})
write("WORKED_NUMERIC_TABLES.json", {"source_id":SOURCE,"source_sha256":SHA,"figures":[fig1,fig2],"coordinate_entry_count":45,
    "testimonies":[{"id":i,"direction":d,"source_statement":s,"dependencies":deps,"pdf_page":275} for i,d,s,deps in votes],
    "delivery_table":{"source_pdf_page":276,"saturn":["Aries",24,37],"moon":["Capricorn",9,50],"mercury":["Aries",11,0],"printed_moon_distance":[14,47],"printed_mercury_distance":[13,37],"printed_difference":[1,10],"source_scale":"one week per degree in this example","source_judgment":"about fourteen weeks"},
    "scope":"Source values and explicitly labeled inferences; no historical ephemeris or predictive validation."})
write("HISTORICAL_CASES.json", {"case_count":2,"dated_enquiries":2,"printed_charts":2,"cases":[
    {"id":CASE1,"source_pdf_pages":[272,273,274],"date_label":"11 June1635","question":"Whether querent should ever have children","known_inputs":"A question about children; no independently documented reproductive history or natal chart supplied in these pages.","judgments":["past nonconception","lifelong nonconception","longstanding and continuing impediment"],"reported_features":["illness/symptoms","five bodily-mark locations"],"reported_predictive_endpoint":"No lifetime outcome supplied in admitted pages","independently_verified":False,"bodily_mark_count":5,"dependent_record_ids":[r['id'] for r in records if r['case_id']==CASE1]},
    {"id":CASE2,"source_pdf_pages":[274,275,276],"date_label":"7 April1645","question":"Male/female child and delivery time","known_inputs":"The question is already framed around being with child; pregnancy is not a newly discovered endpoint in this worked example.","judgments":["male child by 8:4 tally","delivery about 14 weeks"],"reported_outcomes":["male birth: and so it proved","delivery 11 July following"],"birth_time":"Not supplied","retrospective_support":["Mars transit Ascendant","Mercury opposite question Moon","Sun square question Sun","Moon conjunct Mercury"],"independently_verified":False,"dependent_record_ids":[r['id'] for r in records if r['case_id']==CASE2]}
],"unquantified_experience_claims":"Maternal safety, infant survival, parent-child reconciliation and first-question Ascendant resemblance are retained in source records, not converted into a counted case series.","scope":"Two narrated enquiries, not two independently validated predictions; distinct endpoints remain separate."})
print(json.dumps({"root_records":len(records),"root_issues":len(issues),"coordinate_entries":45,"testimony_rows":len(votes)}))
