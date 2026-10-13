"""Close five genuinely separate ORIGINAL-IMAGE source-fidelity reviews for B02u.

All reviewers examined earlier source-reader candidates. Controller corrections
are traceable and not misrepresented as a final sixth blind evaluation.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
P=B/"independent_review"/"FINAL_RECONCILIATION.json"
assert not P.exists(),"Already written; inspect rather than overwrite"
def rd(n):return json.loads((B/n).read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
R=rd("RULES.json")
C=rd("COUNTS.json")
U=rd("UNRESOLVED.json")
T=rd("TEST_RUN_SUMMARY.json")
A=rd("A1_A2_RECONCILIATION.json")
assert R["record_count"]==267 and C["candidate_source_documentary_units"]==267
assert R["last_record"]=="R2572" and C["lilly_total_if_accepted"]==2572
assert U["retained_count"]==len(U["issues"])==119
assert T["successful"] and T["tests_run"]==T["distinct_test_count"]==314
reviews=[]
for w,expected in [("A1",36),("A2",71),("B",88),("C",74),("D",65)]:
 p=B/"independent_review"/f"OPUS_{w}_INITIAL.json"
 assert p.is_file(),p
 d=json.loads(p.read_text())
 assert d.get("verdict",d.get("status"))=="FINDS_ERROR"
 assert d["candidate_units_checked"]==expected
 assert d.get("errata_read",d.get("errata_image_read"))==True
 assert len(d.get("findings",[]))>=2
 reviews.append({
  "window":w,"reported_model":"gpt-6.1-sol via Codex CLI (filenames OPUS inherited historical convention)",
  "review_file":f"independent_review/OPUS_{w}_INITIAL.json",
  "sha256":H(p),"initial_verdict":"FINDS_ERROR",
  "original_reading_coverage":d.get("pages_read",d.get("original_pages_read")),
  "candidate_units_checked":expected,"findings_count":len(d.get("findings",[])),
  "missing_units_not_necessarily_all_indexed":len(d.get("missing_units",d.get("missing_source_units",[]))),
  "source_ambiguities":len(d.get("uncertainties",d.get("source_ambiguities",[])))
 })
assert all(reviews)
changes=rd("DRAFT_CONSOLIDATED.json")["source_review_history"]
assert "A1" in changes and "A2" in changes and all(w in changes for w in "BCD")
r2338=next(x for x in R["rules"] if x["record_number"]==2338)
assert "OPPOSITION" in r2338["source_statement"] and "CONJUNCTION" in r2338["source_statement"]
assert "UNRESOLVED" in " ".join(r2338["exceptions_and_evidence_limits"]).upper()
boundary=rd("NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json")
assert "BEFORE" in boundary["phase_current_stop"]
assert len(boundary["unextracted_next_phase_sections_pdf381"])>=5
summary={
 "batch":"B02u","review_kind":"FIVE_FRESH_SOURCE_IMAGE_FIRST_INPUT_READER_EVALUATIONS",
 "final_disposition":"DOCUMENTARY_SOURCE_FIDELITY_CONTROLLER_RECONCILED_WITH_RETAINED_AMBIGUITIES",
 "primary_source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "original_body_pdf_pages":list(range(364,382)),
 "original_errata_pdf_page":888,
 "five_original_image_review_windows":reviews,
 "number_of_independent_review_windows":5,
 "all_five_initial_evaluators_found_issues":True,
 "source_evaluator_inputs_earlier_candidate_drafts":True,
 "initial_source_model_drafts_independently_evaluated":True,
 "controller_source_correspondence_repaired":True,
 "post_final_controller_change_new_blind_model_review":False,
 "originally_applicable_ancient_author_texts_independently_collated":False,
 "corrected_source_units_count":267,
 "newly_separated_source_statement_R2572":True,
 "maintain_physical_source_order":"SOURCE_ORDER.json",
 "semantic_overlap_audited":"READER_OVERLAP_AUDIT.json + OVERLAP_ADJUDICATION.json + SPLIT_A_OVERLAP_AUDIT.json",
 "material_corrections":[
  {"pdf_page":365,"record_numbers":[2319,2572],
   "problem":"Hour lord equals seventh lord gives radicality; seventh lord in ascendant is a separate suspicion-restricted claim; previously collapsed."},
  {"pdf_page":365,"record_numbers":[2322,2327],
   "problem":"'consentanious' is not 'conscientious'; hope of discovering goods is not guaranteed recovery."},
  {"pdf_page":366,"record_numbers":[2338],
   "problem":"Original aspect to SECOND HOUSE remains disputed between reader A1 opposition and A2 conjunction; unresolved, not an operative rule."},
  {"pdf_page":366,"record_numbers":[2339],
   "problem":"Sun as second lord in TENTH with seventh lord, not third; no invented sextile."},
  {"pdf_page":367,"record_numbers":[2343,2345,2347],
   "problem":"Venus sign TENTH, Moon OPPOSITION rather than conjunction; 'scant be had again' opposite prior 'soon' reading."},
  {"pdf_page":369,"record_numbers":[2392,2393],
   "problem":"Future-theft Moon virtue includes fifth house, and negative aspect grammatical subject is unresolved."},
  {"pdf_page":373,"record_numbers":[],
   "problem":"Six separate original zodiac-sign classification rows restored from independent overlapping source reader."},
  {"pdf_page":374,"record_numbers":[2475],
   "problem":"Name-syllable rule's second planet Venus, not unidentified glyph."},
  {"pdf_page":376,"record_numbers":[2499],
   "problem":"Conjunction not sextile in a return rule; retrograde plural subject ambiguous."},
  {"pdf_page":377,"record_numbers":[2511],
   "problem":"'Within power of loser or someone of his house' plus optional financial recovery, not mere household membership."},
  {"pdf_page":378,"record_numbers":[2523],
   "problem":"Neighbor option and 'by such a one OR his means' restored."},
  {"pdf_page":380,"record_numbers":[2551,2552],
   "problem":"Sometimes-qualified printed marginal willing return distinct from thief-home-before-querent body."},
  {"pdf_page":381,"record_numbers":[],
   "problem":"House/door subsections identified by D outside B02u's exact heading stop; all retained as required next phase, not erased."}
 ],
 "source_witness_disagreements":[
  {"pdf_page":366,"record_number":2338,"status":"UNRESOLVED_OPPOSITION_VS_CONJUNCTION_ASPECT_GLYPH_SECOND_HOUSE"},
  {"printed_page_locator":"3?7","status":"ERRATA_REFERENCE_UNDETERMINED_307_OR_337"}
 ],
 "source_image_pixel_replay":"SOURCE_REPLAY_RECEIPT.json",
 "source_records_not_human_cases":True,
 "clinically_or_criminally_validated":False,
 "empirical_prediction_verified":False,
 "produced_live_operational_rules":False,
 "full_lilly_chapter_L_completed":False,
 "original_uncertainties_retained":119,
 "focused_source_checks_before_this_ledger":314,
 "acceptance_meaning":"A source-only reference corpus with provenance and explicit disputed readings. It does not attest every table cell has been separately diplomatic-transcribed or every historical condition is objectively correct."
}
P.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"reviews":len(reviews),"review_findings":sum(x["findings_count"] for x in reviews),
"retained_issues":119,"reference_units":267,"source_phase_complete":True,
"full_chapter_L_complete":False}))
