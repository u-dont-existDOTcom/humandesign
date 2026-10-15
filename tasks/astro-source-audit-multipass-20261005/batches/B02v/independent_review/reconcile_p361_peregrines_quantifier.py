"""Original p361/PDF395: do not add a planetary-number threshold.

The printed 'Many Thieves, if peregrine Planets be in angles' does not
state that TWO OR MORE peregrine planets must be angular.
Historical claimed number of persons is not a measured fact.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P393_395.json"
BACK=B/"recovery/producer_p393_395_pre_U64_20261015.json"
assert not BACK.exists(),"This original-source correction was already attempted"
before=SRC.read_bytes()
j=json.loads(before)
r=[x for x in j["units"] if x["local_id"]=="P393C062"]
assert len(r)==1
r=r[0]
assert r["pdf_pages"]==[395] and r["kind"]=="many_thieves_peregrines_angular"
assert r["source_statement"]=="Many peregrine planets in angles are said to indicate multiple thieves."
r["kind"]="many_thieves_peregrine_planets_angular_unspecified_count"
r["source_statement"]="Under Lilly's 'Many Thieves' heading, peregrine planet(s) in angular houses are presented as a historical plurality-of-alleged-offenders indication; the source gives no minimum COUNT of peregrine planets."
r["preconditions"]=["Printed p361: 'Many Thieves, if peregrine Planets be in angles.' Source uses a plural generic 'Planets' without a cardinality threshold such as two or more."]
r["exceptions_and_uncertainty"]=["Do not convert plural planets into an explicitly quantified multiple-planet Boolean threshold. 'Many' modifies the alleged thieves, not the count of qualifying planets. No documented criminal outcome is provided."]
r["original_page_anchor"]="Many Thieves, if peregrine Planets be in angles."
ledger_path=B/"UNRESOLVED_DRAFT.json"
ledger=json.loads(ledger_path.read_text())
assert ledger["retained_count"]==63 and len(ledger["issues"])==63
assert all(x["id"]!="U64" for x in ledger["issues"])
ledger["issues"].append({"id":"U64","status":"SOURCE_BOOLEAN_THRESHOLD_CORRECTION_RETAINED","description":"Original p361 R2855 'Many Thieves, if peregrine Planets be in angles.' Producer had required multiple peregrine planets; number of peregrine planets not explicitly stated, only the supposed multiplicity of thieves. Removed unjustified cardinality threshold."})
ledger["retained_count"]=len(ledger["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(before)
SRC.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"corrected":"R2855","source":"PDF395/printed361","old_sha256":hashlib.sha256(before).hexdigest(),"current_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issue_count":ledger["retained_count"],"accepted_additions":0},indent=2))
