"""Create authority, provenance, coverage and open-limit packet for Lilly B02r.

Never automatically accept or publish the candidate. The original pages are
authoritative over the provider's pre-existing ALTO navigational text.
"""
from pathlib import Path
import json,hashlib,collections
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def save(n,d):(B/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def h(path):return hashlib.sha256(path.read_bytes()).hexdigest()
I=json.loads(INDEX.read_text());r=rd("RULES.json")
assert I["records_count"]==1851 and I["batches"][-1]["id"]=="B02q"
assert I["next"]["chapter"]=="XLVIII" and I["next"]["pdf_page"]==330
assert len(r["rules"])==69 and r["record_count"]==69
assert r["general_horary_aphorism_units"]==43
assert [v["aphorism_number"] for v in r["rules"] if "aphorism_number" in v]==list(range(1,44))
assert all(v["source_full_pdf_sha256"]==SOURCE_SHA for v in r["rules"])
save("RETAINED_LILLY_INDEX_BEFORE.json",I)
save("SOURCE_IDENTITY.json",{
 "source_id":"LILLY1647_WELLCOME_B30338724","author":"William Lilly",
 "work":"Christian Astrology","publication_year":1647,"full_pdf_pages":894,
 "source_full_pdf_sha256":SOURCE_SHA,"source_bytes":141842963,
 "original_pdf_url":"https://archive.org/download/b30338724/b30338724.pdf",
 "admitted_content_pages":list(range(330,337)),
 "next_boundary_page":337,"original_errata_page":888,
 "printed_content_pages":list(range(296,303)),
 "start":"Original PDF330 printed296 below divider beginning XLVIII",
 "section_transition":"Original PDF331 printed297 Finis Sexæ Domus then unnumbered Seventh House significations, separate general 43 aphorisms begin original PDF332 printed298",
 "stop":"Original PDF336 printed302 above horizontal divider for XLIX Of Marriage",
 "distinct_original_patient_horoscopes":0,
 "independently_verified_predictions":0,
 "runtime_promotion":False
})
images=[]
for p in list(range(330,338))+[888]:
 name="errata-888.png" if p==888 else f"pdf-{p}.png"
 path=B/"evidence"/name;assert path.is_file(),path
 images.append({"path":f"evidence/{name}","pdf_page":p,"printed_page":p-34 if p!=888 else None,
                "bytes":path.stat().st_size,"sha256":h(path),"from_full_original_pdf_sha256":SOURCE_SHA,
                "source_region":"CONTENT" if p<=336 else "NEXT_BOUNDARY" if p==337 else "ERRATA"})
save("SOURCE_IMAGE_MANIFEST.json",{
 "batch":"B02r","source_sha256":SOURCE_SHA,"raster_generator":"pdftoppm -f 330 -l 337 -scale-to-y 1700 -png, original PDF full SHA checked",
 "previous_render_reused_errata888":"B02q exact verified same-volume page raster",
 "original_pages_included":list(range(330,338)), "original_errata_page":888,"images":images
})
coverage=[
 (330,"XLVIII heading below XLVII divider; servant first-house lord/Moon; master tenth-house lord; perfection, exactness, separation, Moon and Sun fallback; determinate query; departure rules; begins angular opposition",1852,1865),
 (331,"XLVIII angular/direct/retrograde/impediment completion, Finis Sextae Domus; seventh-house topic introduction; 43 aphorisms announced",1865,1875),
 (332,"New unnumbered horary aphorism heading, numbers 1–8 in full",1876,1883),
 (333,"Numbers 9–19 and number20 begins",1884,1895),
 (334,"Aphorism20 continuation through 28; aphorism29 begins",1895,1904),
 (335,"Number29 continuation and complete numbers30–39",1904,1914),
 (336,"Complete numbers40–43; Chapter XLIX new marriage heading below divider",1915,1920),
 (337,"Only next-chapter continuation witnessed, not admitted into B02r rules",None,None),
 (888,"Same-volume errata selective list inspected; no legible item refers to printed296–302",None,None)
]
save("SECTION_COVERAGE.json",{
 "start":"original PDF330 lower below horizontal divider after CRYSIS",
 "end":"original PDF336 above horizontal divider before XLIX",
 "partitions":[{"pdf_page":p,"printed_page":p-34 if p!=888 else None,"description":s,
                "approx_first_record":f"R{a}" if a else None,"approx_last_record":f"R{z}" if z else None} for p,s,a,z in coverage],
 "numbered_aphorisms_source_range":[1,43],"chapter_xlviii_complete":True,
 "seventh_intro_complete":True,"horary_43_complete":True,"xlix_body_excluded":True,
 "earlier_physician_43_is_distinct":True
})
save("ERRATA_COLLATION.json",{
 "errata_source_page":888,"scope":"Original same-volume errata inspected for printed pages296–302 only",
 "matching_entries":[],"observation":"No printed-page296–302 entry visibly present in the volume's selective errata. The list includes adjacent page295 and later page305; a lack of listed corrections is not proof that wording is faultless.",
 "absence_scope":"ONLY this original selective printed errata list, not all editions or handwritten notes",
 "pdf888_in_packet":True
})
limits=[
("U01","Only one 1647 printed copy collated; no independent author autograph/manuscript or alternate edition checked."),
("U02","The society's 1647 legal/social servant/master framework is historical testimony, not modern employment or human-rights advice."),
("U03","The source uses 'conjunction' broadly 'by body or aspect'; conjunction terminology is not silently modernized."),
("U04","The distinction between 'determinate and not absolute' questions and paired examples of particular-versus-ever freedom has ambiguous wording."),
("U05","The first Sun fallback depends on failure of two Moon/ascendant-lord comparisons, not an unconditional Sun criterion."),
("U06","The directional condition of angular planet direct versus retrograde is source-local and conditional on earlier presence/conjunction."),
("U07","The phrase few minutes separated has no universal measured threshold, no ephemeris implementation here."),
("U08","'Entr ing combustion' must remain distinct from already combust Sun aspects; printed typography and start moment unspecified."),
("U09","The heading Seventh House after Finis Sexæ Domus is a new source section despite no new numbered chapter."),
("U10","The forty-three general horary aphorisms differ from the previously indexed forty-three physician aphorisms of Lilly XLIV."),
("U11","Aphorism1 'one nature or Triplicity' does not provide a modern reproducible exact-hour construction."),
("U12","Aphorism2 few/late ascending degrees does not state an exact numerical cutoff."),
("U13","Aphorism3 node-like glyph in tenth may be copy-specific; identify on source image rather than infer from typography."),
("U14","Aphorism5 Moon strength and 'virtue transmission' are 1647 doctrine, not observed mechanism."),
("U15","Aphorism6 cold and heat refer to virtue/operation rather than physical thermodynamic temperature."),
("U16","Aphorism9 void-of-course Moon exceptions are Cancer Taurus Sagittarius Pisces; exact OCR node/sign glyphs require visual read."),
("U17","Aphorism16 'do so when Fortunes are Significators' is elliptic; cannot safely synthesize a fully symmetric calculation."),
("U18","Aphorism20 dignified Saturn/Mars near angles is an explicit exception to a generally malefic-class prediction."),
("U19","Aphorism26 under-beams is within 12 degrees of Sun; cazimi source threshold sixteen arcminutes. Endpoint inclusive ambiguity."),
("U20","Aphorism27 source distinguishes oriental Saturn/Jupiter/Mars from Venus/Mercury reversal of timing."),
("U21","Aphorism28 common-sign probable-but-not-concluded is not a calibrated prediction probability."),
("U22","Aphorism29 states Head or Tail Dragon may harm, not a default north-node positive reading."),
("U23","Aphorism30 'eclipse at hand' requires a separate historic eclipse ephemeris not supplied."),
("U24","Aphorism32 Mercury-in-Sagittarius/Pisces example is source-specific; 'opposite own house' may not imply all signs are uniformly opposite."),
("U25","Aphorism35 Moon conjunct Sun/combustion magnitude is author assertion not independent medical or predictive evidence."),
("U26","Aphorism36 the grouping of both-significators' multiple negative conditions is syntactically uncertain."),
("U27","Aphorism39 circle/fortune glyph read as Part-of-Fortune-like with source-qualified identity."),
("U28","Aphorism40 seventh-house malefic natal-significator exception requires independently known birth-chart role and must be retained."),
("U29","Aphorism41 woman death/deceased men's debts are distinct source claims without verification."),
("U30","Aphorism42 printed Jupiter-and-Venus phrase may enumerate Fortune planets, not require simultaneous co-location."),
("U31","Aphorism43 printed Dragon Tail glyph identification is image-dependent; no verified modern risk prediction."),
("U32","Original handwritten margins of surviving scan are not presumed 1647-authorial."),
("U33","43 source rules are not 43 patients, forecast trials or tested successes."),
("U34","No selective printed erratum for pp296–302 is not proof absence of other printer errors."),
("U35","No comparison to historical Swiss-ephemeris positions, independent interpretations, or untouched human experiments has been performed."),
]
save("UNRESOLVED.json",{
 "batch":"B02r","retained_count":len(limits),
 "limits":[{"id":id,"description":desc,"status":"RETAINED"} for id,desc in limits]
})
counts={
 "batch":"B02r","lilly_before":1851,"new_documentary_records":69,"lilly_after_if_accepted":1920,
 "ptolemy_retained":1066,"combined_if_accepted":2986,
 "source_chapter_xlviii_records":19,"source_seventh_bridge_records":6,
 "general_horary_aphorisms":43,"next_heading_boundary_records":1,
 "previous_physician_aphorisms_already_in_index":43,"new_original_horoscopes":0,
 "new_historical_cases":0,"independently_verified_outcomes":0,"blinded_predictions":0,
 "source_pages":7,"boundary_only_pages":1,"source_errata_pages":1,
 "clinical_or_predictive_validation":False,"runtime_promotion":False,
 "record_group_counts":dict(collections.Counter(x["dependency_group"] for x in r["rules"]))
}
save("COUNTS.json",counts)
print(json.dumps({"images":len(images),"records":r["record_count"],"last":"R1920",
                  "lilly_after":counts["lilly_after_if_accepted"],
                  "combined_after":counts["combined_if_accepted"],
                  "unresolved":len(limits),"sections":len(coverage)}))
