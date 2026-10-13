"""A1/A2 independent original-image source corrections. Not outcome validation.

Preserves raw readbacks, source-reader draft, and pre-repair reference packet.
Review A1's page366 units were held at the split overlap; corresponding
actually indexed A2 clauses get corrected with their independent witness.
"""
from pathlib import Path
import json,copy,shutil,hashlib
B=Path(__file__).resolve().parent
ROOT=Path.home()/"ai-source-review"
DRAFT=B/"DRAFT_CONSOLIDATED.json"
D=json.loads(DRAFT.read_text())
assert D["unit_count"]==len(D["units"])==266
assert D["provisional_last_record"]=="R2571"
SNAP=B/"recovery"/"before_independent_A1_A2"
assert not (SNAP/"DRAFT_CONSOLIDATED.json").exists(),"Already reconciled; do not rerun"
SNAP.mkdir(parents=True,exist_ok=True)
for name in ["DRAFT_CONSOLIDATED.json","ERRATA_COLLATION.json","SOURCE_READER_A.json","SOURCE_IDENTITY.json"]:
 shutil.copy2(B/name,SNAP/name)
OUT=B/"independent_review"
OUT.mkdir(parents=True,exist_ok=True)
reviews={}
for k,expect in [("A1",36),("A2",71)]:
 stage=ROOT/f"b02u-independent-{k.lower()}-20261013"
 assert (stage/"review_codex.exit").read_text().strip()=="0"
 src=stage/"review_codex.stdout"
 a=json.loads(src.read_text())
 assert a["verdict"]=="FINDS_ERROR" and a["candidate_units_checked"]==expect
 assert a["pages_read"]==([364,365,366] if k=="A1" else [366,367,368,369])
 dest=OUT/f"OPUS_{k}_INITIAL.json"
 assert not dest.exists(),"Re-execution blocked"
 shutil.copy2(src,dest)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==hashlib.sha256(dest.read_bytes()).hexdigest()
 reviews[k]={"review_sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
  "findings":len(a["findings"]),"missing_metadata":len(a["missing_units"]),
  "source_uncertainties":len(a["uncertainties"]),
  "all_pages_in_window_read":True,"independent_first_pass":True}
srcA=json.loads((B/"SOURCE_READER_A.json").read_text())
by_raw={x["merged_from_source_split"]:x["local_id"] for x in srcA["units"]}
by_key={(x["window"],x["window_local_id"]):x for x in D["units"]}
def item(oldraw):
 key=by_raw.get(oldraw)
 assert key,("Held outside source scope: "+oldraw)
 r=by_key.get(("A",key))
 assert r,oldraw
 return r
def change(rawid,text,preconditions=None,limits=None,anchor=None,pages=None):
 r=item(rawid)
 r["source_statement"]=text
 if preconditions is not None:r["preconditions"]=preconditions
 if limits is not None:r["exceptions_and_uncertainty"]=limits
 if anchor is not None:r["source_anchor"]=anchor
 if pages is not None:
  r["pdf_pages"]=pages;r["printed_pages"]=[x-34 for x in pages]
  r["source_images"]=[f"evidence/pdf-{x}.png" for x in pages]
 r["independent_source_repair"]="FRESH_IMAGE_FIRST_A1_A2_SOURCE_RECONCILIATION"
 return r["record_number"]
change("A1005",
 "The tenth house signifies the king in Haly's example. The fourth sign refers to 'where the thing is, that is, or was taken away', preserving the original awkward alternative; no certainty that it denotes only the place from which it was taken.",
 ["Within Haly's source-mediated thief/lost-goods role descriptions."],
 ["The source does not grammatically reduce 'where it is, that is, or was taken' to one precise place; no empirical location inference.",
  "The printed p330 line6 'read or' erratum belongs to PRECEDING B02t material above the theft heading, not to this clause."],
 pages=[364,365])
change("A1014",
 "When the LORD OF THE HOUR is ALSO THE LORD OF THE SEVENTH, Lilly calls the thief-significator selection 'more radical'.",
 ["Lord of the planetary hour and lord of seventh are the SAME PLANET."],
 ["This radicality statement is separate from the following seventh-lord-in-ascendant claim; not a verified theft indicator."],
 anchor="if the Lord of the hour be Lord of the seventh")
change("A1015",
 "Lilly assigns alleged thief's complexion and condition from the SEVENTH LORD AND ITS SIGN, in the context of the preceding seventh-lord-in-ascendant suspicion example.",
 ["Seventh lord is the source's thief significator; human descriptions are conditional on house/sign and prior possible accusation."],
 ["Do not inherit the separate hour-lord-identity radicality condition as a mandatory prerequisite.",
  "No actual complexion, character or offender is established."])
change("A1017",
 "The printed marginal comment says Lilly prefers the seventh lord as the more rational and 'consentanious' (consonant/agreement with reason) significator.",
 ["Source author's methodological preference among alternative possible thief significators."],
 ["The historical word is 'consentanious', NOT 'conscientious'; do not ascribe a moral-diligence trait to the planet."])
change("A1022",
 "When first lord draws toward seventh lord, draws toward hour lord, OR occupies seventh, the author says the thief may be taken soon afterward OR there is hope of DISCOVERY OF THE THING LOST.",
 ["Each directed application or first-lord seventh-house placement is a separate alternative."],
 ["Discovery is not equivalent to recovery/return of goods, and the source claims no independently observed thief."])
# Source photo copied by all original readers, OCR glyph disputed as conjunction vs opposition:
# A1 specifically calls it opposition; source-image ALTO shows 'cP' (navigation only).
# The contradictory A2 reader independently said conjunction. Record variant as
# open, not as a falsely settled diplomatic transcription.
change("A2009",
 "With MOON ruling ASCENDANT in FOURTH, second lord in SEVENTH or in SIGN OF EIGHTH, the author says an aspect to the SECOND HOUSE which one reader decodes as OPPOSITION (another source reader: CONJUNCTION), plus sextile/trine to MOON, indicates a thing taken away in jest, not outright stolen.",
 ["Moon rules ascendant and is in fourth; the second lord occupies seventh or sign of eighth.",
  "Printed aspect glyph to the SECOND HOUSE is physically disputed between independent readers (A1 ☍ opposition; A2 ☌ conjunction); sextile/trine to Moon is separate."],
 ["Do not replace SECOND HOUSE with second-house lord or other planet. The aspect-glyph reading is explicitly UNRESOLVED rather than force-corrected.",
  "Author describes a historical hypothetical, not observed person or act."])
change("A2010",
 "If Moon rules ascendant AND is IN ASCENDANT, 'not farre remote', Sun as second lord IN THE TENTH WITH SEVENTH LORD, and seventh lord SQUARES Moon, author says the goods were stolen.",
 ["Moon is first lord and in first, near unspecified reference point.",
  "SUN lord of second IN TENTH with seventh lord (NOT third and no invented sextile).",
  "Seventh lord squares Moon."],
 ["Original phrase 'not farre remote' has no metric; report as unverified claimed theft."])
change("A2014",
 "With MOON in fifth and Capricorn ruling hour, VENUS as second lord IN THE TENTH IN SIGN OF TENTH, and Moon in OPPOSITION to seventh lord, Lilly says goods were lost while travelling or left in a visited place.",
 ["Moon in fifth, Capricorn and lady of hour.",
  "Venus rules second, placed in tenth AND tenth sign.",
  "Moon OPPOSITE seventh lord, not conjunction."],
 ["No real trip or place is verified."])
change("A2016",
 "If MOON as hour ruler IN FOURTH is in OPPOSITION to seventh lord, and second lord IN TWELFTH SEXTILES seventh lord, author claims goods taken in jest.",
 ["Moon rules the hour and is in fourth; Moon opposes lord of seventh.",
  "Second lord occupies twelfth and sextiles seventh lord."],
 ["Two different directed relationships, not a lunar conjunction; historical source conjecture only."])
change("A2018",
 "If second lord last separated from lord of Moon's house, the author says goods were stolen in jest BUT WILL SCANT BE HAD AGAIN (scarcely recovered), not quickly returned.",
 ["Second lord has last separated from Moon's domicile ruler."],
 ["Source's 'scant' is the opposite of 'soon'; do not invert the expected result."])
change("A2001",
 "Continuation of printed p331–332: the ASCENDANT represents QUERENT, and 'his Lord' stands for the one WHO LOST THE GOODS and for the place from whence goods were taken.",
 ["The antecedent of 'his Lord' is on PDF365 after 'the querent, and'."],
 ["This joins the original physical page turn instead of inventing an unattached new subject. Some printed syntax remains elliptical."],
 pages=[365,366])
# Source A1 reviewer identified a second standalone house-placement inference
# previously bundled in R2319, so add exactly one source-documentary unit.
original=item("A1014")
new=copy.deepcopy(original)
new_id=2306+len(D["units"])
assert new_id==2572
new.update(
 id=f"LI.1647.II.L.B02u.R{new_id}",record_number=new_id,
 window_local_id="A014_SPLIT_SEVENTH_ASC",
 preliminary_key="A.A014.SPLIT",
 source_kind="source_conditional",
 source_anchor="but if the Lord of the seventh be in the ascendant",
 section_heading="Of the SIGNIFICATOR of the Thiefe.",
 source_statement="Separately from the hour/seventh lord radicality rule, the source says seventh LORD IN ASCENDANT MAY denote querent as alleged thief ONLY when question concerns querent's FIDELITY or the querent is chiefly suspected.",
 preconditions=["Seventh-house lord actually occupies ascendant.",
                "Inquiry is specifically about fidelity or the querent is greatest suspected person; no universal accusation."],
 exceptions_and_uncertainty=["Requires original suspicion restriction; does NOT require hour-lord identity with seventh lord.",
                            "An early-modern symbolic accusation without any real criminal evidence."],
 source_order_after=original["record_number"],
 raw_source_reader_draft="SOURCE_READER_A.json",
 source_status="AUTHORIAL_SOURCE_WITNESS_NOT_VALIDATED",
 independent_source_repair="A1_SOURCE_SEMICOLON_SPLIT"
)
D["units"].append(new)
assert len(D["units"])==267
D["unit_count"]=267
D["provisional_last_record"]="R2572"
D["conditional_cumulative_lilly_if_accepted"]=2572
D["conditional_combined_if_accepted"]=3638
D["status"]="ORIGINAL_SOURCE_CORRECTED_A1_A2_BCD_PENDING_FINAL_SOURCE_ADMISSION"
D.setdefault("source_review_history",{})["A1"]=reviews["A1"]
D["source_review_history"]["A2"]=reviews["A2"]
D["source_fidelity_review_completed_windows"]=["A1","A2","B","C","D"]
(B/"DRAFT_CONSOLIDATED.json").write_text(json.dumps(D,ensure_ascii=False,indent=2)+"\n")
margins={
 "scope":"Original PDF365–369 later manuscript annotations, NOT 1647 printed rules",
 "witness":"original raster evidence/pdf-365.png through evidence/pdf-369.png",
 "items":[
  {"pdf_page":365,"description":"Upper margin handwritten 7 and smaller ambiguous mark followed by House; unknown hand/date."},
  {"pdf_page":365,"description":"Later handwritten numeral 1 beside Significator of the Thiefe heading."},
  {"pdf_page":365,"description":"Later handwritten numeral 2 beside Significator of the thing stolen heading."},
  {"pdf_page":365,"description":"Later handwritten numeral 3 beside Of THEFTS heading."},
  {"pdf_page":367,"description":"Upper margin handwritten 7th House; separate from printed running title. The footer includes ORIGINAL PRINTED signature Kk 3 and catchword 'aforesaid,'."},
  {"pdf_page":368,"description":"Handwritten references apparently 5/6/7/8/30/31 above or near stolen heading, some digits ambiguous; additional mark 4 by heading."},
  {"pdf_page":369,"description":"Later handwritten 7th House at upper right and hand-added section numerals 5/6/7/8 adjacent to source PRINTED headings; NOT printed source numbering."},
  {"pdf_page":369,"description":"Handwritten small 'a' above the marked Planet word and a caret below it; uncertain whether it implements same-volume errata, not independently original printing."}
 ],
 "source_only":True,"not_new_aphorisms_or_human_cases":True
}
(B/"ORIGINAL_MARGINALIA_REGISTER.json").write_text(json.dumps(margins,ensure_ascii=False,indent=2)+"\n")
review={
 "review_windows":["A1","A2"],
 "first_pass_independent":True,
 "first_pass_verdicts":["FINDS_ERROR","FINDS_ERROR"],
 "source_input_copy_verified":True,
 "finding_counts":{"A1":8,"A2":6},
 "record_changes":[2310,2319,2320,2322,2327,2330,2338,2339,2343,2345,2347,2572],
 "source_glyph_conflict_R2338":"Independent readers disagree (A1 opposition, A2 conjunction). Marked unresolved; no hidden deterministic claim.",
 "new_source_units":1,
 "marginalia_only_findings_are_not_new_lilly_rules":True,
 "reviewed_intermediate_source_not_accepted":True,
 "empirical_or_criminal_validity":False
}
(B/"A1_A2_RECONCILIATION.json").write_text(json.dumps(review,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"A1_A2_REVIEW_COMPLETE":True,"repaired_source_units":11,
                  "new_source_units":1,"draft_count":267,"last_id":"R2572",
                  "glyph_dispute_left_open":True,"source_image_marginalia":8}))
