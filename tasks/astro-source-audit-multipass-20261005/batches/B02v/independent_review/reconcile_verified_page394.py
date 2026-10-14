"""One-time visual-source correction: PDF394/printed360 conjunction and sixth house.
Freeze the original producer proposal. Does not accept any B02v units.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P393_395.json"
BACK=B/"recovery/producer_p393_395_before_20261014_p360_review.json"
assert not BACK.exists(), "Correction previously applied: do not reapply"
raw=SRC.read_bytes()
data=json.loads(raw)
assert len(data["units"])==64
by_kind={r["kind"]:r for r in data["units"]}
a=by_kind["sun_square_opposition_thief_known"]
b=by_kind["owner_self_first_second_seventh"]
assert a["source_statement"]=="Sun in square or opposition to thief's significator is said to make him known."
assert b["source_statement"]=="First lord in second, first or seventh, OR second lord in ascendant, is offered as claim owner himself did the deed."
assert a["pdf_pages"]==b["pdf_pages"]==[394]
a["kind"]="sun_conjunction_square_opposition_thief_known"
a["source_statement"]="Sun in conjunction, square or opposition to the thief significator is claimed to make the thief known."
a["preconditions"]=["Sun (☉) in conjunction (☌), square (□), or opposition (☍) to thief significator; the original p360 line4 has a same-volume errata entry."]
a["exceptions_and_uncertainty"]=["Conjunction omitted from producer paraphrase; restored from original PDF394 line and p360/l4 errata. Exact editorial role of erratum remains uncertain; no claim of real thief identification."]
b["kind"]="owner_self_second_sixth_seventh"
b["source_statement"]="Ascendant lord in the second, sixth or seventh, OR second lord in ascendant, is claimed to implicate the owner himself in the source's offender-classification list."
b["preconditions"]=["Original printed 'second, sixt or seventh': sixt denotes sixth house, NOT first house."]
b["exceptions_and_uncertainty"]=["The producer draft misread printed 'sixt' as 'first'. This historical criminal accusation rule is not valid forensic evidence."]
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
UN=B/"UNRESOLVED_DRAFT.json"
u=json.loads(UN.read_text())
issues={x["id"]:x for x in u["issues"]}
issues["U22"]["description"]="Original errata printed p360 line4 and PDF394 body both visually show Sun in conjunction; producer omitted conjunction from R2819, now corrected. Precise purpose of replacement erratum and remaining glyph alignment unresolved."
u["issues"].append({"id":"U46","description":"PDF394/printed360 says ascendant lord in second, 'sixt' (sixth), or seventh, not FIRST; earlier R2832 producer paraphrase corrected and original source preserved. This is historical text, not an offender inference.","status":"RETAINED"})
u["retained_count"]=len(u["issues"])
UN.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"old_sha256":hashlib.sha256(raw).hexdigest(),
 "new_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
 "corrected_kinds":[a["kind"],b["kind"]],
 "new_uncertainty_count":len(u["issues"]),
 "source_review":"IMAGE_FIRST_PARTIAL", "accepted":False},indent=2))
