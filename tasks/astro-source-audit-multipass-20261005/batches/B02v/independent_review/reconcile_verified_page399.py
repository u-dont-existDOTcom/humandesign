"""Correct B02v producer PDF399 capture list against original printed page 365.
The prior draft duplicated NEXT page 366's separate extra-capture list and
omitted printed 365 clauses. No empirical/predictive use, no acceptance.
This is a one-time source-backed edit with exact original backup.
"""
from pathlib import Path
import json, hashlib

B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P398_400.json"
BACK=B/"recovery/producer_p398_400_before_20261014_p365_capture_review.json"
assert not BACK.exists(),"Already run; inspect original backup, never reapply."
original=SRC.read_bytes()
d=json.loads(original)
rows=d["units"]
assert len(rows)==73
by_id={r["local_id"]:r for r in rows}
edits={
"P398C039":(
"captured_first_with_retrograde",
"capture_seventh_lord_join_retrograde",
"Seventh lord joined to a retrograde planet is another claimed capture condition; this is separate from the seventh lord being in the first or joined to the first lord.",
"Printed PDF399/365: 'or a Retrograde Planet' follows 'joyned to the Lord of the first'; whether coordinated as an object of the seventh lord's joining is grammatically implied, not independently verified.",
"Historical allegation only. Do not require first-house placement in the retrograde branch without the source saying so."),
"P398C040":(
"captured_moon_seventh_to_mars_square",
"capture_moon_from_seventh_to_conj_first",
"Moon separating from the lord of the seventh and moving to conjunction with the lord of the first is offered as a capture testimony.",
"Original PDF399/365: 'or if the Moon separate from the lord of the seventh, to the conjunction of the lord of the first'.",
"Moon-in-seventh square Mars belongs to a DIFFERENT additional capture list on PDF400; it was wrongly copied here in the earlier producer draft."),
"P398C041":(
"captured_moon_saturn_mercury_sun_square",
"capture_moon_from_conj_first_toward_seventh",
"Moon separating from the conjunction of the lord of the first toward the lord of the seventh is a separate historical capture indication.",
"Original PDF399/365: 'or from the conjunction of the lord of the first to the lord of the seventh'; the exact aspect of its final contact with seventh lord is not specified.",
"The old draft erroneously imported a Moon/Saturn/Mercury/Sun square condition from next-page PDF400."),
"P398C042":(
"captured_moon_sixth_eighth_twelfth",
"capture_sun_moon_seventh_join_or_behold",
"Sun and Moon in conjunction with the lord of the seventh, or in a variant reading beholding him, are cited as historical capture indications.",
"Original PDF399/365: 'or if Sun and Moon be in conjunction with the lord of the seventh, some say, if they behold him'.",
"The source's 'some say' offers a qualified alternate aspect criterion; keep source uncertainty. Moon in sixth/eighth/twelfth is on PDF400, not this page."),
"P398C043":(
"captured_moon_saturn_square_mercury",
"capture_seventh_lord_to_combustion",
"Seventh lord going to conjunction with the Sun, described as combustion, is presented as a historical capture condition.",
"Original PDF399/365: 'or if the lord of the seventh be going to conjunction, viz. Combustion'.",
"The prior Saturn/Mercury progression is on PDF400. The source does not specify exact orbs/timing."),
"P398C044":(
"captured_moon_mars_eighth_second",
"capture_first_lord_conjunction_angles_or_infortune_seventh",
"Lilly adds an obscure condition of the ascendant lord being in conjunction in the ascendant, tenth or seventh, OR an unfortunate planet in the seventh, as further capture indicators.",
"Original PDF399/365: 'or if the lord of the ascendant be in conjunction in the ascendant, tenth or seventh, or an infortunate Planet in the seventh'.",
"The conjunction's other party is unspecified in this printed phrase; do not invent one. Moon-eighth/Mars-second is separately on PDF400.")
}
for local,(old_kind,new_kind,text,pre,unc) in edits.items():
 r=by_id[local]
 assert r["kind"]==old_kind,(local,r["kind"],old_kind)
 assert r["pdf_pages"]==[399],(local,r["pdf_pages"])
 r["kind"]=new_kind
 r["source_statement"]=text
 r["preconditions"]=[pre]
 r["exceptions_and_uncertainty"]=[unc]
 r["original_page_image_checked"]="evidence/pdf-399.png"

# Next printed page 366 is the ONLY location for the earlier mispositioned cases.
for local,pattern in {
 "P398C067":"repeated among capture rules",
 "P398C068":"repeated in the additional list",
 "P398C069":"again listed as capture sign",
}.items():
 r=by_id.get(local)
 if r and pattern in r["source_statement"]:
  r["source_statement"]=r["source_statement"].replace(pattern,"included in this separate additional capture list")

# Locate the next-page capture-list statements mechanically; do not force matching C IDs.
for r in rows:
 if r["pdf_pages"]==[400] and r["kind"] in {
 "other_capture_moon_seventh_square_mars",
 "other_capture_moon_from_saturn_mercury_sun",
 "other_capture_moon_6_8_12"}:
  old=r["source_statement"]
  r["source_statement"]=old.replace("is repeated among", "is listed among").replace("is repeated in", "is listed in").replace("is again listed", "is listed")
 
# Preserve uncertain grammatical role at p366 without inventing a positive complete rule.
for r in rows:
 if r["kind"]=="seventh_eighth_restitution_relation":
  r["exceptions_and_uncertainty"].append("PDF400/366 has an elliptical trailing clause 'or the lord of the seventh or eighth'; do not construe either ruler alone as a fully stated sufficient condition.")

BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(original)
SRC.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
ledger_path=B/"UNRESOLVED_DRAFT.json"
ledger=json.loads(ledger_path.read_text())
assert not any(x["id"]=="U50" for x in ledger["issues"])
ledger["issues"].append({
 "id":"U50",
 "description":"Original PDF399/printed365 capture paragraph was replaced in the producer extraction by conditions belonging to PDF400/printed366, duplicating next-page content and missing its distinct Moon L7→L1 application, Sun/Moon Lord7 conjunction, combustion, and angular clauses. Six relevant draft source kinds/statements corrected from original p365 image, including R2940–R2945; unqualified p365-vs-p366 'repetition' is not established.",
 "status":"SOURCE_IMAGE_CORRECTION_RETAINED"})
for issue in ledger["issues"]:
 if issue["id"]=="U35":
  issue["description"]="Original p365 and p366 both offer capture lists but with materially distinct conditions. Producer p365 accidentally reused p366 Moon/aspect conditions; corrected p365 to its own printed clauses. Repeat counts must be limited to genuine literal duplicates after source review."
ledger["retained_count"]=len(ledger["issues"])
ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_sha256":hashlib.sha256(original).hexdigest(),
"corrected_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
"corrected_page399_units":len(edits),
"source_pages":[399,400],
"ledger_count":ledger["retained_count"],
"accepted":False},indent=2))
