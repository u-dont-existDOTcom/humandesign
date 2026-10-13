"""One-time source-bound repair: p318 Mistress/Sweetheart application omitted from candidate."""
from pathlib import Path
import json,shutil,copy
B=Path(__file__).resolve().parent
saved=B/"recovery"/"scope_insert_originals"
if (saved/"RULES.json").exists():raise SystemExit("Already applied, inspect state")
saved.mkdir(parents=True,exist_ok=True)
names=["RULES.json","RULES_SOURCE_ORDER.json","UNRESOLVED.json","COUNTS.json",
       "AUDIT_REPORT.md","README.md","CONTINUE_HANDOFF.md","SOURCE_FIRST_NOTES.md",
       "WORKING_CHECKPOINT.md","ERRATA_COLLATION.json",
       "test_b02s_source_structure.py","test_b02s_original_review_regressions.py"]
for n in names:shutil.copy2(B/n,saved/n)
def load(n):return json.loads((B/n).read_text())
def save(n,v):(B/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n")
d=load("RULES.json")
assert d["record_count"]==len(d["rules"])==216
assert [r["record_number"] for r in d["rules"]]==list(range(1921,2137))
v=copy.deepcopy(next(x for x in d["rules"] if x["record_number"]==2095))
v.update(id="LI.1647.II.XLIX.R2137",record_number=2137,
         source_record_kind="mistress_sweetheart_scope_parallel",
         source_statement="In the estranged-partner inquiry, Lilly expressly states that the same question also concerns doubts about a mistress or sweetheart, not solely a married wife or husband.",
         preconditions=["This extends the immediately preceding inquiry about an absent or estranged partner; preserve its seventh-house signification and original question context."],
         exceptions_and_evidence_limits=["Scope extension is historical authorial text, not a second actual couple or outcome.",
                                         "No assumption that reconciliation is safe, desired or consensual."],
         source_review_inserted=True,source_order_after_draft=2095)
d["rules"].append(v)
d.update(record_count=217,last_record="R2137",added_missed_original_units=30,
         status="CORRECTED_SOURCE_ONLY_PENDING_FINAL_ACCEPTANCE")
save("RULES.json",d)
order=load("RULES_SOURCE_ORDER.json")
assert len(order["ids"])==216 and 2137 not in order["ids"]
order["ids"].insert(order["ids"].index(2095)+1,2137)
save("RULES_SOURCE_ORDER.json",order)
c=load("COUNTS.json")
assert c["records"]==216 and c["lilly_if_accepted"]==2136
c.update(records=217,lilly_if_accepted=2137,combined_if_accepted=3203)
save("COUNTS.json",c)
u=load("UNRESOLVED.json")
assert len(u["limits"])==u["retained_count"]==64
limits=[
("U65","Printed p318 explicitly extends the estranged-partner question to mistress or sweetheart; it is now R2137 but not an independent person or verified result."),
("U66","Two informed changed-item reviewer passes after two partial-window fresh image reviews caught material errors; the controller's final repairs were not given a third fresh blind evaluation."),
("U67","p305 erratum deleting a conjunction has a body match one line different by one count; p306 already seems to print undertaken; p307 handwriting cannot independently prove the original printed form."),
("U68","p312 read-it-is-no-good erratum's exact replacement span is uncertain; p315 south-node body mark is blotted and later marginal handwriting is not original print.")
]
for id,desc in limits:u["limits"].append({"id":id,"description":desc,"status":"RETAINED"})
u["retained_count"]=len(u["limits"])
save("UNRESOLVED.json",u)
e=load("ERRATA_COLLATION.json")
assert e["count"]==len(e["entries"])==6
desc=[
"Original p305 conjunction glyph found in the clause; modern body count is line23 while source erratum says22. Erratum says delete conjunction; preserve both source witnesses.",
"Original p306 body appears already to read undertaken; do not invent an earlier different word for the erratum.",
"p307 source glyph partly obscured and handwritten correction later; erratum instructs reading for Sun and Mars.",
"p312 source clause includes not to trust; erratum says read it is no good, but precise body replacement span is not proven.",
"p315 Dragon Tail mark blotted; later handwriting separate; rely on explicit erratum.",
"p315 seventh printed in abbreviation and body location substantially matches; no body page rewrite."
]
for row,s in zip(e["entries"],desc):row["body_match"]=s
e["source_reconciliation"]="Source original body separate from same-volume printed errata and later handwritten marginalia."
save("ERRATA_COLLATION.json",e)
print(json.dumps({"new_records":217,"new_limits":u["retained_count"],"next_if_accepted":"R2138"}))
