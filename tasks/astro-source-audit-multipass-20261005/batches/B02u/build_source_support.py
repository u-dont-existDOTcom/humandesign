"""Rebuild B02u source-only reference units, provenance, and pending gaps.

Original 1647 page images are controlling. This does not accept source
interpretation, alter the empirical prediction engine, or advance Git index.
"""
from pathlib import Path
import collections,hashlib,json,re
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
BASE="tasks/astro-source-audit-multipass-20261005"
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def load(path):return json.loads(path.read_text())
def save(name,data):(B/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
D=load(B/"DRAFT_CONSOLIDATED.json")
I=load(ROOT/BASE/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json")
assert I["records_count"]==2305 and I["batches"][-1]["id"]=="B02t"
assert I["next"]["chapter"]=="L" and I["next"]["pdf_page"]==364
assert D["batch"]=="B02u" and D["original_pdf_sha256"]==SRC
units=D["units"]
assert len(units)==D["unit_count"]
assert [x["record_number"] for x in units]==list(range(2306,2306+len(units)))
assert all(x["runtime_status"]=="REFERENCE_ONLY_NOT_PROMOTED" for x in units)
assert all(x["original_human_cases_verified"]==0 and x["source_claim_not_predictive_validation"] for x in units)
man=load(B/"SOURCE_IMAGE_MANIFEST.json")
rep=load(B/"SOURCE_REPLAY_RECEIPT.json")
assert rep["all_rgb_identical"] and rep["images_pixel_replayed"]==20
assert man["full_original_1647_sha256"]==SRC
assert {x["source_pdf_page"] for x in man["original_images"]}==set(range(364,382))|{888,400}
for x in man["original_images"]:
    p=B/x["relative_path"]
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==x["sha256"]
save("RETAINED_LILLY_INDEX_BEFORE.json",I)
out=[]
for unit in units:
    pages=unit["pdf_pages"]
    assert pages and all(364<=p<=381 for p in pages)
    rec={
      "id":unit["id"],"record_number":unit["record_number"],"batch":"B02u",
      "source_id":"LILLY1647_WELLCOME_B30338724","book":"II","chapter":"L",
      "phase":"THIEF_SOURCE_BODY_PARTIAL_CHAPTER",
      "source_pdf_full_sha256":SRC,
      "source_locator":{"pdf_pages":pages,"printed_pages":[p-34 for p in pages],
                        "page_images":unit["source_images"],
                        "source_anchor":unit["source_anchor"],
                        "source_anchor_diplomatic_verified":False,
                        "source_statement_is_verbatim":False,
                        "source_reader_window":unit["window"],
                        "source_reader_local_id":unit["window_local_id"]},
      "source_record_kind":unit["source_kind"],
      "source_section":unit["section_heading"],
      "source_statement":unit["source_statement"],
      "source_statement_type":"IMAGE_READER_NORMALIZED_PARAPHRASE_NOT_VERBATIM",
      "preconditions":unit["preconditions"] if unit["preconditions"] else ["Section-heading record only; no prediction precondition."],
      "exceptions_and_evidence_limits":unit["exceptions_and_uncertainty"] if unit["exceptions_and_uncertainty"] else ["Source is an unverified early-modern assertion; no empirical evidence supplied."],
      "review_fidelity_status":unit.get("independent_source_repair","CANDIDATE_PENDING_FINAL_SOURCE_RECONCILIATION"),
      "source_review_inserted":bool(unit.get("source_review_inserted",False) or unit.get("source_order_after") is not None),
      "source_order_after":unit.get("source_order_after"),
      "dependency_group":unit["section_heading"] or "Unheaded continuation",
      "case_evidence_countable":False,
      "independently_authenticated_human_case":False,
      "prospective_frozen_prediction":False,
      "verified_crime_identification":False,
      "clinical_medical_or_criminal_use_authorized":False,
      "runtime_status":"REFERENCE_ONLY_NOT_PROMOTED"
    }
    assert all((B/f).is_file() for f in rec["source_locator"]["page_images"])
    out.append(rec)
data={"batch":"B02u","status":"DRAFT_DOCUMENTARY_REVIEW_INCOMPLETE",
      "numbered_book_chapter":"II.L", "first_source_page":364,"last_source_page":381,
      "source_end":"BEFORE separate Of the house of the Thiefe and mark thereof heading on PDF381",
      "whole_chapter_l_complete":False,
      "record_count":len(out),"first_record":"R2306",
      "last_record":f"R{2305+len(out)}",
      "previous_accepted_lilly_records":2305,
      "independently_authenticated_people_or_crimes":0,
      "empirical_predictive_validation":False,
      "original_table_rows_diplomatically_transcribed":False,
      "rules":out}
save("RULES.json",data)
# Reference ID order is append-only; physical source-reading order inserts later recovered clauses.
source_order=[r["record_number"] for r in out if not r.get("source_review_inserted")]
for r in out:
    if r.get("source_review_inserted"):
        anchor=next(x.get("source_order_after") for x in units if x["record_number"]==r["record_number"])
        assert anchor in source_order
        source_order.insert(source_order.index(anchor)+1,r["record_number"])
assert len(source_order)==len(out) and set(source_order)==set(x["record_number"] for x in out)
save("SOURCE_ORDER.json",{"batch":"B02u","source_order_record_ids":source_order,
 "source_order_is_not_prognostic_ranking":True,
 "source_review_insertions":[r["record_number"] for r in out if r.get("source_review_inserted")]})
by=collections.defaultdict(list)
for x in units:
    by[min(x["pdf_pages"])].append(x)
coverage=[]
for page in range(364,382):
    a=by[page]
    headings=[x["section_heading"] for x in a if x["source_kind"]=="heading"]
    for x in a:
        if x["source_kind"]=="source_table" and x["section_heading"] not in headings:headings.append(x["section_heading"])
    coverage.append({"pdf_page":page,"printed_page":page-34,
                     "new_unit_start_count":len(a),
                     "first_record":f"R{min(x['record_number'] for x in a)}" if a else None,
                     "last_record":f"R{max(x['record_number'] for x in a)}" if a else None,
                     "headings_and_tables":list(dict.fromkeys(headings)),
                     "boundary_note":"LAST IN-SCOPE 'Which way the Thief is gone'; house/door heading is NEXT source phase" if page==381 else None})
assert all(x["new_unit_start_count"]>0 for x in coverage)
save("SECTION_COVERAGE_DETAILED.json",{
 "original_source_sha256":SRC,
 "source_begin":"PDF364 printed330 BELOW Of a Thief and Theft heading, no B02t fugitive overlap",
 "source_end":"PDF381 printed347 BEFORE Of the house of the Thiefe heading",
 "physical_body_source_pages":18,
 "window_page_overlaps":[369,373,377],
 "original_body_next_heading_separately_preserved":"NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json",
 "whole_chapter_l_complete":False,
 "source_pages":coverage,
 "overlap_audit":"READER_OVERLAP_AUDIT.json",
 "overlap_manual_resolution":"OVERLAP_ADJUDICATION.json"
})
core=[
 ("K01","Single full original 1647 copy only; no independent manuscript or edition collated."),
 ("K02","The p381 house-of-thief / door material follows AFTER the declared B02u phase stop, starts next source batch on same physical page; original page image already preserved."),
 ("K03","Full Lilly Chapter L continues beyond p381 through original PDF400, and the accepted index must remain PARTIAL after B02u."),
 ("K04","Three original page overlaps 369/373/377 require semantic de-duplication; count once, preserve excluded source-reader draft units."),
 ("K05","Printed p339 six zodiac classifications are represented separately after original-source review, not independently observed six cases."),
 ("K06","The old text alleges thief identity, gender, social roles, guilt, clothing and names without verifiable evidence; never identify a real criminal or give legal enforcement advice."),
 ("K07","The printed name table on PDF375 has companion glyphs and blank slots; extracted page/table units are not certified individual diplomatic transcriptions of every cell."),
 ("K08","Original printing, same-volume errata and later handwritten marks are separate witnesses; damaged p3?7 locator is not confidently p337."),
 ("K09","Original ancient authority attributions are Lilly-mediated; underlying Al-Kindi/other external sources not independently collated."),
 ("K10","No original individual suspect charts, birth data, crime records, successful predictions or calibrated probability evidence are supplied."),
 ("K11","Different rules for ascendant ruler, seventh ruler, Moon and hour ruler cannot be freely substituted between source subheadings."),
 ("K12","Source may contain contradictory fixed/immovable and multiple-thief sign classifications; retain rather than silently harmonize."),
 ("K13","Historical positions, distance/house/furlong scales and directions lack modern calibrated map or ephemeris validation."),
 ("K14","Source name/gender/race/occupation appearances are period stereotype assertions, not real-world attribute inferencing."),
 ("K15","No participant data, synthetic target, blinded forecast, working HumanDesign model or prior source IDs are altered by source-documentary intake."),
 ("K16","Original reviewer B/C/D checked page spans but the merged overlap logic and C006 six-row disaggregation are controller changes, not newly independent observational evidence."),
 ("K17","Two new clean-context source readers disagree over p332 jest-condition aspect glyph (opposition vs conjunction). It is source-qualified rather than silently assigned a single operator."),
 ("K18","Later handwritten numerals, margin 7th-House marks and the p335 'Planet' caret are not authenticated original Lilly print."),
 ("K19","P331 exact separate: hour lord identical to seventh lord gives radicality; seventh lord in ascendant under suspicion is a different allegation, not automatically a crime."),
 ("K20","An asserted hope of DISCOVERY is not a guaranteed RECOVERY; the source's 'scant be had again' is opposite the earlier bad paraphrase 'soon returned'.")
]
issues=[{"id":n,"source":"CONTROLLER","description":s,"status":"RETAINED"} for n,s in core]
aud=load(B/"READER_OVERLAP_AUDIT.json")
for i,z in enumerate(aud["raw_reader_uncertainties"],1):
    issues.append({"id":f"R{i:03d}","source":"SOURCE_READER_"+z["window"],
                   "description":str(z.get("finding",""))[:1300],
                   "status":"RETAINED_DRAFT_ORIGINAL_SOURCE_UNCERTAINTY"})
for win in ("B","C","D","A1","A2"):
    p=B/"independent_review"/f"OPUS_{win}_INITIAL.json"
    if p.exists():
        q=load(p)
        for i,z in enumerate(q.get("source_ambiguities",q.get("uncertainties",[])),1):
            issues.append({"id":f"{win}{i:03d}","source":f"INDEPENDENT_READER_{win}",
                           "description":z.get("description",z.get("issue","")),"pdf_page":z.get("pdf_page"),
                           "status":"RETAINED_REVIEWER_SOURCE_UNCERTAINTY"})
save("UNRESOLVED.json",{
 "batch":"B02u","status":"INITIAL_INDEPENDENT_READERS_COMPLETE_CORRECTIONS_DOCUMENTED",
 "retained_count":len(issues),"issues":issues,
 "accepted_human_or_legal_findings":0
})
save("COUNTS.json",{
 "batch":"B02u","status":"NOT_ACCEPTED",
 "lilly_previous_accepted":2305,"retained_ptolemy":1066,
 "candidate_source_documentary_units":len(out),
 "lilly_total_if_accepted":2305+len(out),
 "combined_total_if_accepted":3371+len(out),
 "source_physical_pages":18,"context_original_images":2,
 "all_original_images":len(man["original_images"]),
 "reviewed_BCD_initial":all((B/"independent_review"/f"OPUS_{x}_INITIAL.json").is_file() for x in "BCD"),
 "remaining_A1_A2_reviews":"COMPLETE_FIRST_PASS_CORRECTED_GLYPH_DISAGREEMENT_RETAINED",
 "held_duplicate_or_overlap_source_units":D["overlap_units_held_for_fidelity_review"],
 "original_evidence_cases":0,"independent_verifications":0,
 "whole_chapter_l_complete":False,"runtime_promotions":0,
 "source_kinds":dict(collections.Counter(x["source_record_kind"] for x in out))
})
save("TABLE_WITNESS_REGISTER.json",{
 "batch":"B02u","source_only":True,
 "table_witnesses":[
  {"pdf_page":374,"printed_page":340,"subject":"planetary colors and compound colors",
   "evidence_file":"evidence/pdf-374.png","diplomatic_all_cells_checked":False},
  {"pdf_page":375,"printed_page":341,"subject":"Men's and women's name-to-planet combination tables",
   "evidence_file":"evidence/pdf-375.png","diplomatic_all_cells_checked":False}
 ],
 "admission":"Original images and named source-table units may be accepted as source witnesses; no machine-accurate name assignment or untested prediction algorithm may be inferred without separate full-cell original-source collation."
})
print(json.dumps({"candidate":len(out),"lilly_if_accepted":2305+len(out),
                  "combined_if_accepted":3371+len(out),
                  "pages":18,"issues":len(issues),"tables":2,
                  "all_chapter_complete":False}))
