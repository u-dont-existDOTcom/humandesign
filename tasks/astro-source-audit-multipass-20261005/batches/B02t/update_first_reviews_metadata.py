"""Reconcile provisional B02t phase1 support after BOTH source review findings.

Only safe after finalized original-review A+B source edits. Prior accepted index
remains 2137 and is NEVER modified here.
"""
import copy,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
def save(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
D=rd("PHASE1_RULES_DRAFT.json")
R=D["rules"]
assert len(R)==D["record_count"]==162
assert [x["record_number"] for x in R]==list(range(2138,2300))
assert (B/"independent_review/OPUS_A_INITIAL.md").is_file()
assert (B/"independent_review/OPUS_B_INITIAL.md").is_file()
C=rd("COUNTS.json")
assert C["lilly_before"]==2137 and C["draft_source_units"]==129
C.update(draft_source_units=162,candidate_lilly_after=2299,
         candidate_combined_after=3365,original_initial_units=129,
         new_fidelity_review_units=33,
         source_first_review_material_findings="A 7 major+15 moderate, B 9 high+18 medium",
         initial_independent_source_review_windows=2,
         all_chapter_l_complete=False)
save("COUNTS.json",C)
S=rd("SECTION_COVERAGE.json")
S["status"]="CORRECTED_DRAFT_AFTER_TWO_IMAGE_FIRST_REVIEWS_ACCEPTANCE_NOT_YET_GRANTED"
S["phase1_start"]="PDF353 printed319 BELOW XLIX/L divider"
S["phase1_end"]="PDF364 printed330 ABOVE 'Of a Thief and Theft' heading"
S["full_lilly_chapter_l_complete"]=False
S["records_count_after_review"]=162
for x in S["pages"]:
 pg=x["pdf_page"]
 nums=[r["record_number"] for r in R if pg in r["source_locator"]["pdf_pages"]]
 assert nums
 x.update(source_records=len(nums),first_record=f"R{min(nums)}",last_record=f"R{max(nums)}")
# Physical witness PDF364 is shared context for phase2; body after theft divider excluded.
S["phase2_overlap_page"]=364
S["phase2_starts_below_of_a_thief_and_theft_heading"]=True
save("SECTION_COVERAGE.json",S)
E=rd("ERRATA_COLLATION.json")
assert E["count"]==len(E["entries"])==2
e=E["entries"][1]
assert e["printed_page"]==330
e.update(original_erratum="p 330 l 6 r or",replacement="or",body_target_proved=True,
         body_target_line="PDF364/printed330: 'three dayes; [f]or according to probability' at line 6 as counted by original errata",
         body_word_ambiguity="Printed first letter blotted, 'for' is plausible; correction to 'or' unequivocal in original same-volume errata. Do not overwrite original print.",
         consequence="With 'or', three-day NEWS is an alternative to return, under source distance qualifier rather than merely an explanation.")
E["entries"][0]["note"]="Original p324 line10 'read the' is present on printed same-volume errata; exact body replacement token remains unresolved; no silent emendation."
E["reviewer_original_source_status"]="A/B independent windows source fidelity diagnostic; authorial source image unchanged; errata original p330 'or' not 'for'"
save("ERRATA_COLLATION.json",E)
U=rd("UNRESOLVED.json")
assert U["retained_count"]==len(U["issues"])==30
issues=[
 "The 8th house FROM THE MOON for beast death (p322) must not be substituted with radical 8th, which is only later fallback. Source repeats eighth-house variants differently on p324.",
 "The original 'moon house lord' vs 'moon' location/significator subjects have several unclear antecedents; do not impose a single generic lost-goods indicator.",
 "The p323/p324 Capricorn glyph differs: LAST FACE Capricorn versus LAST MOIETY Capricorn, both retained separately without repair.",
 "Original p322 stolen-beast and general 'Whether thing missing be stolne' headings are distinct from PDF364 later 'Of a Thief and Theft'; phase1 does not admit post-heading thief mechanics.",
 "Cattle-restored source p325 lists second, FIFTH or eleventh, not sixth; printed 'they' subject may refer to fortunes or animals, exact grammar ambiguous.",
 "Sixth lord watery + angular, succedent and cadent location clauses differ; only cadent branch uses wet meadows/watering-place details.",
 "Original printed p328-329 Moon first-lord->seventh predicts news, seventh->first predicts regret/entreaty; no inversion permitted.",
 "Original p330 1647 erratum says read 'OR', changing explanatory vs alternative news/return logic; body glyph blotted and original remains unchanged.",
 "Original p327 animal custody Saturn in four houses (including eighth) may conflict with ascendant lord in eighth probable animal death; separate premises and planets, no outcome verified.",
 "An historical HUNDRED is a district or locality, not a fixed modern distance; historical houses/furlongs not converted to miles.",
 "The first reviewer could read the sign glyphs ♎, ♒, ♈, ♑, ♊, ♍, ♐, ♓ in the high-resolution copy; later glyph identification not guessed elsewhere.",
 "Some printed margin labels restrict parts of p320 to strayed CATTLE and p324 parts to immovable goods versus strayed beasts; scope switching remains source-specific.",
 "The broad compound original source accounts include editor-created summaries and atomic sub-rules; overlapping source records are not independent factual observations or prediction successes.",
 "B reviewer found additional original headings missing; section records are editorial metadata, not distinct experimental evidence.",
 "Original p328 Sun is querent secondary significator while Moon is fugitive NATURAL signifier in following subsection, not another querent.",
 "The 1647 'pound' is cattle enclosure and the owner may be forced to pay a custodian; these descriptions do not establish criminal guilt, person safety, animal health or lawful custody.",
 "The source's favourable restitution rule distinguishes a finder WOULD FAIN restore, actual WILL restore, and Moon in first RESTORED WITH TROUBLE; clauses not merged.",
 "Review A & B were image-first isolated evaluations but their subwindows overlap at PDF359; overlapping page reviewed twice does not increase original primary source count.",
 "Source reviewer A staged original images under source_images/, while canonical Git keeps evidence/ paths; stage-path absence is not a repository defect.",
 "The author invokes judicial-astrology directions for missing humans and alleged thieves without verified social or geographic outcomes; do not promote as modern law-enforcement advice."
]
for i,s in enumerate(issues,31):U["issues"].append({"id":f"U{i:02d}","description":s,"status":"RETAINED"})
assert len(U["issues"])==50
U["retained_count"]=50
U["review_initial_outcomes"]={"A":"FINDS_ERROR, 7 major, 15 moderate","B":"FINDS_ERROR, 9 high, 18 medium"}
save("UNRESOLVED.json",U)
assert sum(v["record_number"] in set(range(2138,2300)) for v in R)==162
print(json.dumps({"candidate_records":len(R),"accepted_lilly_unchanged":C["lilly_before"],
                  "if_admitted_lilly":C["candidate_lilly_after"],
                  "if_admitted_combined":C["candidate_combined_after"],
                  "unresolved":U["retained_count"],"errata330":E["entries"][1]["replacement"]}))
