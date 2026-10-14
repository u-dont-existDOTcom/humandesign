"""One-time image-first correction: p358 'second'/'Ascendant' referents.
Preserve source literal objects rather than assuming second/first LORDS.
No acceptance or empirical inference.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P391_392.json"
BACK=B/"recovery/producer_p391_392_before_20261014_p358_review.json"
assert not BACK.exists(), "Already corrected"
raw=SRC.read_bytes()
d=json.loads(raw)
target=[x for x in d["units"] if x["kind"]=="first_second_direct_contact"]
assert len(target)==1
r=target[0]
assert r["pdf_pages"]==[392] and r["source_statement"]=="First lord applying to second lord or second lord applying to first is a source recovery signal."
r["kind"]="first_lord_to_second_second_lord_to_asc_textual"
r["source_statement"]="Lilly says if the lord of the ascendant applies to 'the second', or the lord of the second applies to 'the Ascendant', the goods are recovered. The original objects are not explicitly called the second and first house LORDS, respectively."
r["preconditions"]=["Original PDF392/printed358 uses 'Lord of the Ascendant apply to the second, or the Lord of the second to the Ascendant'; preserve directional applications without replacing the literal objects."]
r["exceptions_and_uncertainty"]=["The phrase may describe contacts with house cusps or planetary rulers; no definite lord1↔lord2 aspect is certified from this clause alone. The next clause separately uses eighth-house lord and second-house lord."]
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
un=B/"UNRESOLVED_DRAFT.json"
u=json.loads(un.read_text())
assert all(x["id"]!="U47" for x in u["issues"])
u["issues"].append({"id":"U47","description":"Original PDF392/printed358 says first lord applies to 'the second' OR second lord to 'the Ascendant'. Producer assumed these were aspects between first and second house lords; replaced with literal source-object wording and retained cusp-versus-lord ambiguity.","status":"RETAINED"})
u["retained_count"]=len(u["issues"])
un.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_sha256":hashlib.sha256(raw).hexdigest(),
 "new_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
 "corrected_kind":r["kind"],"retained_issues":len(u["issues"]),
 "source_image":"PDF392/printed358","accepted":False},indent=2))
