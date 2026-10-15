"""One-time correction for printed357→358 and 358→359 source seams.

R2770 sentence finishes on original PDF392. R2793 begins at end PDF392
and finishes PDF393. R2794 is an 'especially if' qualification, not
an additional required antecedent. All claims remain historical only.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
parts=[
("PRODUCER_SOURCE_DRAFT_P391_392.json","recovery/producer_p391_392_pre_U73_U74_20261015.json"),
("PRODUCER_SOURCE_DRAFT_P393_395.json","recovery/producer_p393_395_pre_U73_U74_20261015.json")
]
data=[]
for name,bname in parts:
 p=B/name
 back=B/bname
 assert not back.exists(),"Already applied, check recovery bytes"
 raw=p.read_bytes()
 data.append((p,back,raw,json.loads(raw)))
source_a,backup_a,raw_a,doc_a=data[0]
source_b,backup_b,raw_b,doc_b=data[1]
a={x["local_id"]:x for x in doc_a["units"]}
b={x["local_id"]:x for x in doc_b["units"]}
r2770=a["P391C019"]
r2793=a["P391C042"]
r2794=b["P393C001"]
assert r2770["pdf_pages"]==[391] and r2770["kind"]=="part_of_fortune_lord_to_asc_goods_moon"
assert r2793["pdf_pages"]==[392] and r2793["kind"]=="second_exaltation_recovery_continued"
assert r2794["pdf_pages"]==[393] and r2794["kind"]=="second_exaltation_extra_hope"
assert r2794["preconditions"]==["Second lord in its exaltation AND any stated extra support."]

r2770["pdf_pages"]=[391,392]
r2770["source_statement"]="The Lord of Part of Fortune applying to the first lord, second house, the Part's place or Moon belongs to a set of historical recovery testimonies; Lilly's closing 'all these signify recovery' finishes on original PDF392 after starting on PDF391."
r2770["exceptions_and_uncertainty"]=["This printed clause crosses p357→358. Do not treat page-358 'signify recovery' as a new unlinked rule or count the page turn as another observed outcome."]
r2770["original_page_anchor"]="p357 '... or to the Moon; all these' | p358 'signify recovery'"

r2793["pdf_pages"]=[392,393]
r2793["source_statement"]="The second lord in its exaltation is said to provide GREAT HOPE OF RECOVERY; the physical sentence begins at bottom printed358 and ends at top printed359. Extra favourable evidence is marked 'especially', not required for baseline hope."
r2793["preconditions"]=["Second lord in its exaltation, original PDF392/printed358 with consequent completing on PDF393/printed359."]
r2793["exceptions_and_uncertainty"]=["The following extra favourable testimony is an intensifier, not a mandatory conjunction; the historical rule is not experimentally validated."]
r2793["original_page_anchor"]="p358 'If Lord of second be in his exaltation, there is' | p359 'a great hope of recovery'"

r2794["kind"]="second_exaltation_especially_other_testimony"
r2794["source_statement"]="The p359 continuation adds that recovery hope under exalted second lord is ESPECIALLY strengthened when OTHER recovery testimony also exists. This is a qualifier to R2793, not another independent source rule nor a required antecedent for its baseline claim."
r2794["preconditions"]=["Exalted second lord provides baseline hope (printed358→359); other recovery testimony, IF PRESENT, further strengthens the author's claimed hope."]
r2794["exceptions_and_uncertainty"]=["Do not require additional testimony as an AND gate. R2793 and R2794 are two editorial units representing one physical source sentence and its modifier, not two independently observed cases."]
r2794["original_page_anchor"]="p359 'especially if there be any other testimony of the recovery'"

issues_path=B/"UNRESOLVED_DRAFT.json"
u=json.loads(issues_path.read_text())
assert len(u["issues"])==u["retained_count"]==72
assert not {x["id"] for x in u["issues"]}&{"U73","U74"}
u["issues"].extend([
{"id":"U73","status":"SOURCE_CROSS_PAGE_LOCATOR_CORRECTED","description":"Printed p357/358 source sentence for R2770 ends with 'all these' on PDF391 and 'signify recovery' on PDF392; corrected source locator [391,392], one source outcome."},
{"id":"U74","status":"SOURCE_CROSS_PAGE_AND_OPTIONAL_QUALIFIER_CORRECTED","description":"Printed p358/359 second-lord-in-exaltation clause starts PDF392 and completes 'great hope of recovery' PDF393. R2793 now cites both; R2794 separately records the printed 'especially if other testimony', NOT requiring that testimony as an AND prerequisite or counting independent outcome."}
])
u["retained_count"]=len(u["issues"])
for p,back,raw,j in data:
 back.parent.mkdir(parents=True,exist_ok=True)
 back.write_bytes(raw)
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
issues_path.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"corrected":[2770,2793,2794],"cross_pages":[[391,392],[392,393]],"issues":len(u["issues"]),"original_sha256":{p.name:hashlib.sha256(raw).hexdigest() for p,_,raw,_ in data},"accepted":False},indent=2))
