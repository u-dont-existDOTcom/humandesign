"""Create exact-source support, table geometry and self-contained first-pass limits for B02q.

Do not invoke to change historical source records or previously accepted index.
The 30 x 16 grid is an EDITORIAL COMPUTED RECONSTRUCTION of geometry,
NOT a diplomatic transcription of 480 original cells. The PDF328 image wins.
"""
from pathlib import Path
import json,hashlib
from collections import Counter
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
SRC_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def read(n):return json.loads((B/n).read_text())
def H(raw):return hashlib.sha256(raw).hexdigest()
def save(n,obj):(B/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
R=read("RULES.json")
assert R["first_record"]==1794 and R["last_record"]==1851 and R["record_count"]==58
assert all(r["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for r in R["rules"])
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert I["records_count"]==1793 and I["batches"][-1]["id"]=="B02p" and I["next"]["chapter"]=="XLVII"
save("RETAINED_LILLY_INDEX_BEFORE.json",I)
save("SOURCE_IDENTITY.json",{
 "source_id":"LILLY1647_WELLCOME_B30338724",
 "author":"William Lilly","work":"Christian Astrology","year":1647,"copy":"Wellcome b30338724 original 894-page scan",
 "archive_original_pdf":"https://archive.org/download/b30338724/b30338724.pdf",
 "source_full_pdf_bytes":141842963,"source_full_pdf_sha256":SRC_SHA,"page_count":894,
 "admitted_pdf_pages":[324,325,326,327,328,329,330],"admitted_printed_pages":[290,291,292,293,294,295,296],
 "start":"Original PDF324/printed290 below divider, Chapter XLVII CRYSIS",
 "stop":"Original PDF330/printed296 above divider, before XLVIII servant freedom",
 "errata_page":888,"source_original_verification":"Full archive downloaded to owner-authorized out-of-Git local cache; complete file SHA256 verified before page rendering",
 "lilly_prior_record_count":1793,
 "one_original_table":True,"new_original_horoscopes":0,"reused_prior_horoscope_as_hypothetical_onset_only":True,
 "independently_authenticated_outcomes":0,"clinical_or_predictive_validation":False
})
images=[]
for page in [324,325,326,327,328,329,330,888]:
 p=B/"evidence"/(f"pdf-{page}.png" if page!=888 else "errata-888.png")
 assert p.is_file(),p
 images.append({"path":str(p.relative_to(B)),"pdf_page":page,"printed_page":page-34 if page!=888 else None,
   "bytes":p.stat().st_size,"sha256":H(p.read_bytes()),"render":"pdftoppm -f PAGE -l PAGE -scale-to-y 1800 -png, from exact source PDF SHA256",
   "primary_visual_witness":True})
save("SOURCE_IMAGE_MANIFEST.json",{
 "batch":"B02q","source_pdf_sha256":SRC_SHA,"source_pdf_pages":7,"included_original_errata_page":888,
 "renders_are_secondary_visualizations_of_exact_hash_verified_original":True,
 "raster_pixel_replay_required_before_acceptance":True,
 "included":images
})
coverage=[
(324,"Chapter heading below previous XLVI divider and opening sentence crossing page turn",1794,1795),
(325,"Meaning and two polarities of crisis; critical/decretory/chrysmal days",1795,1798),
(325,"Timing hierarchy: onset, first urine presentation, first doctor's requested consultation",1799,1801),
(325,"Galen, Hippocrates, Avicenna definitions, non-local motion and malignant exceptions",1802,1807),
(325,"Minority inferior-cause view and lunar counterargument crossing to next leaf",1808,1809),
(326,"Lunar causal explanation, onset degree and rectified fallback",1810,1812),
(326,"Critical-day table input types, hypothetically reused July16 figure, rounding 15°42′ Virgo→16 Virgo",1813,1816),
(326,"First indicative Libra8°30, benevolent/malevolent configurations, first half-crisis Scorpio1° crossing leaf",1817,1819),
(327,"Second indicative Scorpio23°30, true crisis Sagittarius16, aspects and continued zodiac cycle",1820,1823),
(327,"Independent observation of 6th/7th/8th cusp transits",1824,1824),
(328,"Entire source 30x16 numerical lookup table; separate geometrical reconstruction",1825,1826),
(329,"First-quartile benefic caveat, medical restoration claim, infortune adverse",1827,1829),
(329,"Calendar 7/14/21 rejected as fixed; lunar true speed requires computation",1830,1831),
(329,"Four moon-in-sign temperament rows",1832,1835),
(329,"Three conditional water-Moon purging rows, planets Jupiter/Venus/Mars-or-Sun",1836,1838),
(329,"Saturn retentive and six-item planetary faculty table",1839,1845),
(329,"Four elemental-sign to humour rows",1846,1849),
(329,"Larger illness treatise deferred to Master Booker, continues next leaf",1850,1850),
(330,"Master Booker closing clause; next XLVIII servant freedom begins BELOW divider",1850,1851),
(888,"Original-volume errata for printed p291 line7 and p295 line34, separate collation",None,None)]
save("SECTION_COVERAGE.json",{
 "batch":"B02q","status":"SOURCE_READ_FIRST_PASS_REVIEW_PENDING",
 "start_pdf_page":324,"end_pdf_page":330,"exact_start":"below horizontal divider PDF324","exact_end":"above horizontal divider PDF330",
 "all_seven_original_pages_in_packet":True,"table_page":328,
 "sections":[{"pdf_page":p,"printed_page":p-34 if p!=888 else None,"scope":scope,"first_record":f"R{first}" if first else None,"last_record":f"R{last}" if last else None} for p,scope,first,last in coverage],
 "not_accepted_in_this_batch":"XLVI retrospective patient ending above PDF324 divider, XLVIII servant question below PDF330 divider"
})
save("ERRATA_COLLATION.json",{
 "volume_errata_pdf_page":888,"status":"PRINTED_ERRATA_ADMITTED_BODY_LINE_ALIGNMENT_NOT_PROVEN",
 "entries":[
  {"target_printed_page":291,"target_pdf_page":325,"printed_errata_text":"p 291 l 7 r do","read_token":"do","body_target_line_matched":False,
    "consequence":"No silent source text edit; original witness remains unchanged; verify print line counting before assigning correction."},
  {"target_printed_page":295,"target_pdf_page":329,"printed_errata_text":"p 295 l 34 r atram","read_token":"atram","body_target_line_matched":False,
    "consequence":"Preserve token atram and author's Earth/black-melancholy context; original morphology/target line remain copy-qualified."}
 ],
 "other_errata_in_printed_290_to_296":"No other entry identified in the full original errata list; this is a same-volume selective list, not a guarantee against mistakes.",
 "source_body_not_overwritten":True
})
signs=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
def cell(row,col):
 arcminutes=(30+60*row+1350*col)%(360*60)
 sign=signs[arcminutes//(30*60)]
 dm=arcminutes%(30*60)
 return {"column_index_1based":col+1,"sign":sign,"degree":dm//60,"minutes":dm%60,"longitude_arcminutes":arcminutes}
grid=[[cell(row,col) for col in range(16)] for row in range(30)]
samples=[
(0,0,"Aries",0,30),(0,1,"Aries",23,0),(0,2,"Taurus",15,30),
(8,7,"Virgo",16,0),(8,8,"Libra",8,30),(8,9,"Scorpio",1,0),
(8,10,"Scorpio",23,30),(8,11,"Sagittarius",16,0),
(29,0,"Aries",29,30)]
for row,col,sign,degree,minute in samples:
 got=grid[row][col]
 assert (got["sign"],got["degree"],got["minutes"])==(sign,degree,minute),got
save("TABLE_GEOMETRY.json",{
 "witness":"Original 1647 page printed294/PDF328; image evidence/pdf-328.png",
 "chart_input":"Zodiac sign and degree of Moon at illness onset or qualified fallback, rounded to nearest printed table row as author illustrates",
 "reconstruction_status":"EDITORIAL_MATHEMATICAL_MODEL_NOT_DILPOMATIC_TRANSCRIPTION",
 "original_source_cell_verification_scope":"Selected physical source cells and author's four worked positions only; all 480 generated coordinates unverified against possible printer anomalies",
 "printed_rows":30,"printed_columns":16,"derived_coordinate_cells":480,
 "columns_step_from_previous_arcminutes":1350,
 "row_zero_col_zero":"Aries 0 degrees 30 minutes",
 "generated_formula":"zodiac_longitude_arcminutes = (30 + 60*zero_based_row + 1350*zero_based_column) mod 21600",
 "table_data":grid,
 "source_examples_checked":[{"row_zero_based":r,"column_zero_based":c,"sign":s,"degree":d,"minute":m,
   "source":"Printed page294 grid" if r in (0,29) else "Author's worked demonstration on printed292-293 plus page294 table"}
   for r,c,s,d,m in samples],
 "event_labels_author_explicit":"first indicative at Libra8°30; first half-crisis/semisquare Scorpio1; second indicative Scorpio23°30; true crisis/quarter Sagittarius16; opposition/full crisis in the general method",
 "not_calendar_days":True,"not_validated_astronomical_ephemeris":True,"no_patient_data":True
})
limits=[
("U01","1647 Wellcome copy only; no collation of independent original editions or manuscripts."),
("U02","Source terms CRYSIS, decretory, chrysmal, humour and faculty belong to 1647 usage; not modern clinical constructs."),
("U03","Galen's alleged sudden-motion definition not collated with Galen's Greek/Latin primary text."),
("U04","Hippocrates acute-disease/poisonous-disease exception is source-mediated and not independently checked."),
("U05","Avicenna in Canticis reference is Lilly's attribution; underlying source is not examined."),
("U06","Original volume's p291 l7 'r do' erratum is legible; exact source body token/line convention remains unproved."),
("U07","Original volume p295 l34 'r atram' erratum is legible; body-word alignment remains unproved."),
("U08","Illness onset moment has no independent chronological verification in historical example."),
("U09","Urine first-presentation or first doctor consultation times are fallbacks and expressly less certain."),
("U10","Lunar longitude, chart houses/aspects and alleged event timings were not calculated against modern independent historical ephemerides."),
("U11","The printed 16 July 1645 horoscope is reused as an IF/suppose example, not a new chart, patient or outcome."),
("U12","The 15°42′ Virgo Moon position and 16° Virgo table entry differ by 18 arcminutes due to the author's rounding."),
("U13","The table's all-cell 30x16 geometry model is editorial; image preserved, 480 cells not individually diplomatically transcribed."),
("U14","The source may contain printer mistakes or numerals/ambiguous zodiac glyphs outside the selected table cell readbacks."),
("U15","Semiquadrate, crisis and indicative labels are printed schematic notions; extension to all phase positions is interpretation."),
("U16","Moon's motion can vary; no exact clock dates follow from table positions without an independently verified ephemeris."),
("U17","Conditional benefic judgement specifically says 'if the party be ordained for life'; may make claims unfalsifiable."),
("U18","Claims about favourable/aspect-based cure and easier medicine are source authorial claims, not trials or treatment guidance."),
("U19","The 'inferior causes' alternative is acknowledged but neither it nor lunar causation is experimentally assessed."),
("U20","Humoral, temperamental, purging and sign association claims have no source-supported modern clinical efficacy."),
("U21","Printed signs in the purging brace/table must not be silently converted into a general therapeutic algorithm."),
("U22","First, sixth, seventh, eighth chart house crossings require another chart/house-system specification absent from table."),
("U23","Aphorisms in previous chapters and the 1645 July illness case are neither rerun nor counted as new independent support here."),
("U24","The printer's word 'atr(a/u)m' in body and same-volume erratum 'atram' are kept as separate witnesses."),
("U25","The author does not provide observed patient cohorts, denominators, blind forecast logs or reproducible outcomes."),
("U26","No source content here validates astronomical astrology, medical diagnostics, or any prospective life prediction."),
("U27","The following servant-freedom material starts below PDF330 divider and is excluded."),
("U28","The previous XLVI patient-transit narrative ends above PDF324 divider and is excluded."),
("U29","Galen/Hippocrates/Avicenna distinctions can influence disease concept but are not independent empirical evidence."),
("U30","Phrase 'ordained for life' may refer to providential fate, not a measurable frozen criterion."),
("U31","The earlier question-wheel Moon-like glyph/degree might indicate 15°43′ while Chapter XLVII prose reads 15°42′ Virgo; source pairing and exact minute are not proven. The rounded 16° input is invariant to this one-minute distinction.")
]
save("UNRESOLVED.json",{
 "retained_count":len(limits),"limits":[{"id":k,"description":s,"status":"RETAINED"} for k,s in limits]
})
count=len(R["rules"])
save("COUNTS.json",{
 "batch":"B02q","lilly_before":1793,"new_documentary_records":count,"lilly_after_if_accepted":1793+count,
 "retained_ptolemy":1066,"combined_if_accepted":1793+count+1066,
 "first_record":"R1794","last_record":f"R{1793+count}",
 "source_pages":7,"printed_table_count":1,"derived_table_cells_not_observed_cases":480,
 "new_historical_patient_cases":0,"new_original_patient_charts":0,
 "reuses_unvalidated_previous_july_horoscope_as_hypothetical":True,
 "independently_verified_patient_outcomes":0,"preregistered_predictions":0,
 "clinical_or_predictive_validation":False,"runtime_promotion":False,
 "source_record_kind_counts":dict(Counter(r["source_record_kind"] for r in R["rules"]))
})
print(json.dumps({"batch":"B02q","records":count,"lilly_candidate":1793+count,
  "images":len(images),"sections":len(coverage),"unresolved":len(limits),"generated_table_cells":len(grid)*len(grid[0])}))
