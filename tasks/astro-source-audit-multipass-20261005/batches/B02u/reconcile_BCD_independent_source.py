"""Repair only B/C/D independently image-reviewed source claims, not empirical outcomes.

A1/A2 remain separately under review. The 1647 page381 house/door section lies
BEYOND the frozen B02u phase boundary and must be extracted next without omission.
Never rewrite the raw reader JSON or independent reviewer results.
"""
from pathlib import Path
import copy,hashlib,json,shutil
B=Path(__file__).resolve().parent
raw=Path.home()/"ai-source-review"
P=B/"DRAFT_CONSOLIDATED.json"
D=json.loads(P.read_text())
assert D["unit_count"]==len(D["units"])==266
assert D["provisional_first_record"]=="R2306" and D["provisional_last_record"]=="R2571"
snap=B/"recovery"/"before_independent_BCD"
assert not (snap/"DRAFT_CONSOLIDATED.json").exists(),"Already executed, reconcile current bytes"
snap.mkdir(parents=True,exist_ok=True)
for f in ["DRAFT_CONSOLIDATED.json","ERRATA_COLLATION.json","READER_OVERLAP_AUDIT.json"]:
 shutil.copy2(B/f,snap/f)
I=B/"independent_review"
I.mkdir(parents=True,exist_ok=True)
D["source_review_history"]={
 "B":"Fresh image-first independent source review, initial verdict FINDS_ERROR.",
 "C":"Fresh image-first independent source review, initial verdict FINDS_ERROR.",
 "D":"Fresh image-first independent source review, initial verdict FINDS_ERROR.",
 "later_final_blind_review_of_these_corrections":False,
 "scope_note":"Window D's full-page reader request extended beyond this PHASE'S previously frozen heading-boundary scope at PDF381."
}
for k in "bcd":
 stage=raw/f"b02u-independent-{k}-20261013"
 assert (stage/"review_codex.exit").read_text().strip()=="0"
 incoming=stage/"review_codex.stdout"
 info=json.loads(incoming.read_text())
 assert info["status"]=="FINDS_ERROR" and info["all_claims_checked"]
 name=f"OPUS_{k.upper()}_INITIAL.json"
 if not (I/name).exists():shutil.copy2(incoming,I/name)
 assert hashlib.sha256((I/name).read_bytes()).digest()==hashlib.sha256(incoming.read_bytes()).digest()
def unit(w,local):
 hits=[u for u in D["units"] if u["window"]==w and u["window_local_id"]==local]
 assert len(hits)==1,(w,local,hits)
 return hits[0]
def overwrite(w,k,statement,pre=None,ex=None):
 x=unit(w,k)
 x["source_statement"]=statement
 if pre is not None:x["preconditions"]=pre
 if ex is not None:x["exceptions_and_uncertainty"]=[ex]
 x["independent_source_repair"]="ORIGINAL_IMAGE_ADJUDICATED_NOT_PREDICTIVE_VALIDATION"
 return x["record_number"]
changes={}
changes["B015"]=overwrite("B","B015",
  "The author says a proposed future theft occurs when Moon, AS LORD OF SEVENTH, transfers virtue to a planet in SECOND, ELEVENTH OR FIFTH; after 'or fift' the print adds that she has neither sextile nor trine to the house cusps.",
  ["Moon rules seventh; destination planet is in second, eleventh OR fifth.",
   "The no-sextile/no-trine to cusps condition is explicitly printed but its reach across all three placements is uncertain."],
  "Printed 'or fift' is legible. The subsequent 'having her selfe neither' may limit all placement alternatives or only the last; do not impose a fixed Boolean rule.")
changes["B016"]=overwrite("B","B016",
  "The printed other future-theft clause has a planet in the SEVENTH giving virtue to another planet in SECOND or ELEVENTH, followed by 'and have no' sextile/trine to the SEVENTH planet; the actor of 'have no' is NOT securely supplied.",
  ["Donor planet occupies seventh and gives virtue to second- or eleventh-house recipient.",
   "Additional negative aspect to the seventh planet, subject unresolved in original syntax."],
  "Do not write an aspect from the seventh planet to itself or force its receiver to be the subject.")
changes["C029"]=overwrite("C","C029",
  "Lilly claims a NAME OF MORE SYLLABLES such as Richard or William when SATURN ♄ OR VENUS ♀ is the relevant significator.",
  ["Saturn ♄ OR Venus ♀ acting as name significator, with manuscript glyph on p340 originally unclear."],
  "Second glyph read as Venus in fresh independent page image inspection; slight open-head ink distortion remains, not actual name evidence.")
changes["C053"]=overwrite("C","C053",
  "MOON IN NINTH in CONJUNCTION ☌, SQUARE □ OR OPPOSITION ☍ to SATURN ♄ or MARS ♂ is said to bring back the thief, 'without fail if they be Retrograde'.",
  ["Moon must occupy ninth house.",
   "Source's first aspect is conjunction, NOT sextile, followed by square/opposition.",
   "Named Mars/Saturn bodies and the ambiguous plural retrograde qualifier."],
  "Original glyph is conjunction with ascending stroke; cannot insert application/separation, and the antecedent of 'they' is uncertain.")
changes["D005"]=overwrite("D","D005",
  "With SEVENTH LORD in SECOND, after masculine/feminine sign alternatives, the source says the subject is 'within the power of the Loser, or some of his house', and 'may be recovered by money'.",
  ["Seventh ruler in second, following house/sign-specific person categories."],
  "Do not turn power of loser or of one of his house into merely household membership. The subject of 'it' and source of recovery by money remain uncertain.")
changes["D017"]=overwrite("D","D017",
  "When SEVENTH LORD is in ELEVENTH, the author alleges a friend, one known by service, someone of a churchman's household, OR A NEIGHBOUR as a possible class; also somebody of the querent's MOTHER'S HOUSEHOLD, and says recovery may be achieved 'by such a one OR his meanes'.",
  ["Seventh ruler physically in eleventh; each source household, neighbor, service or maternal-household alternative remains source-qualified."],
  "Whether neighbor is independent or shares the preceding household syntax is ambiguous. 'By such a one or his means' includes both actor and agency.")
x=unit("D","D045")
x["exceptions_and_uncertainty"]=[
 "Source body says seventh lord in ascendant points to supposed thief arriving home before the querent, adds 'probatum est'; this is author's claim of demonstration.",
 "Adjacent printed margin's 'sometimes' explicitly introduces a DIFFERENT willing-goods-return claim. Its reach to this body clause is NOT established."
]
x["independent_source_repair"]="MARGINAL_SCOPE_RESTRICTED"
x=unit("D","D046")
x["source_statement"]="In PRINTED MARGIN the author says SOMETIMES when seventh lord is in the ascendant a supposed thief RETURNS THE GOODS HOME WILLINGLY; this differs from the body claim the thief comes home before querent."
x["exceptions_and_uncertainty"]=["Original margin says 'It sometimes holds true'; not an unconditional qualification of the neighboring body.", "Neither predicts an actual identified person's conduct."]
x["independent_source_repair"]="DISTINCT_MARGINAL_ASSERTION"
D["status"]="SOURCE_REPAIRED_B_C_D_A_WINDOWS_PENDING"
D["source_fidelity_review_completed_windows"]=["B","C","D"]
D["review_repair_map"]=changes
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+"\n")
e=json.loads((B/"ERRATA_COLLATION.json").read_text())
for entry in e["original_printed_errata_entries"]:
 if entry.get("printed_page")==337 and str(entry.get("line"))=="28":
  entry["printed_page_locator_original"]="p 3?7 (middle digit damaged)"
  entry["printed_page"]=None
  entry["possible_printed_page_readings"]=[307,337]
  entry["body_target_matched"]=False
  entry["admission"]="UNCERTAIN_PAGINATION_NO_ASSIGNMENT_TO_B02u_SOURCE_BODY"
  entry["body_context"]="Printed page locator not reliably read, perhaps 307 outside this chapter; do not ascribe to lunar age body p337."
e["reconciliation_note"]="Independent source review B reads faint p3?7, not proved p337. No silent source body emendation."
(B/"ERRATA_COLLATION.json").write_text(json.dumps(e,ensure_ascii=False,indent=2)+"\n")
scope={
 "phase_current_stop":"BEFORE separate Of the house of the Thiefe, and the mark thereof on original PDF381.",
 "reviewer_D_F01":"Reviewer was asked to read entire original PDF381 and correctly noticed the later source sections. The controlling original work checkpoint excludes them from THIS bounded phase; they must be first units of next phase. Review conclusion does not prove the material nonexistent.",
 "unextracted_next_phase_sections_pdf381":[
 "Of the house of the Thiefe, and the mark thereof",
 "Thief-significator sign/quarter and house/object directions",
 "Sun signification of house, Moon of door",
 "East, west, north, south and intermediate angular placements",
 "Of the Door of the house: Moon angular/succedent/cadent rule continuing original PDF382"
 ],
 "verifier_required":"Next phase must start at original PDF381 WITH these sections and include PDF382 continuation without omission.",
 "safety":"Do not report full chapter L complete or use source claims for real suspects.",
 "original_images":["evidence/pdf-381.png","evidence/next-chapter-boundary-pdf-400.png"]
}
(B/"NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json").write_text(json.dumps(scope,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"reviewed_windows":["B","C","D"],"corrected_core_units":len(changes)+2,
 "draft_count":len(D["units"]),"last":D["provisional_last_record"],
 "erratum_locator":"p3?7 uncertain","next_phase_footprint":"PDF381 heading onward"}))
