"""Original printed366 noncapture clauses: retain seventh lord aspect operator.

The opening clause explicitly requires lord7 ASPECTING a Fortune.
The eleventh/third benefic placement subclauses inherit this aspect
rather than being pure house-placement rules. Original p400 scan governs.
"""
from pathlib import Path
import hashlib,json

B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P398_400.json"
FROZEN=B/"recovery/producer_p398_400_pre_U65_20261015.json"
assert not FROZEN.exists(),"Already corrected: do not rerun"
raw=SRC.read_bytes()
doc=json.loads(raw)
by={x["local_id"]:x for x in doc["units"]}
a=by["P398C047"];b=by["P398C048"]
assert (a["kind"],b["kind"])==("not_taken_jupiter_venus_eleven_friends","not_taken_jupiter_venus_third_strangers")
assert a["pdf_pages"]==b["pdf_pages"]==[400]
assert a["source_statement"]=="If the Fortune involved is Jupiter or Venus in eleventh, escape is attributed to friends."
assert b["source_statement"]=="If Jupiter/Venus occupies third instead, the author attributes escape to strangers."

a["kind"]="not_taken_lord7_aspects_venus_jupiter_eleven_friends"
a["source_statement"]="If the seventh lord aspects Jupiter OR Venus placed in the ELEVENTH, the author attributes the alleged person's escape to friends. The aspect is a precondition, not house placement alone."
a["preconditions"]=["Original printed p366: 'if in aspect to ♃ or ♀ in the eleventh, he escapes by friends'; the previous clause supplies lord of seventh as aspecting subject."]
a["exceptions_and_uncertainty"]=["This is an attributed historical noncapture explanation, not established help from actual friends."]
a["printed_anchor"]="if in aspect to Jupiter or Venus in the eleventh, he escapes by friends"

b["kind"]="not_taken_lord7_aspects_benefic_third_strangers"
b["source_statement"]="In the same seventh-lord/benefic aspect context, the source says 'if in the third, by strangers'; the third-house position modifies the preceding Jupiter/Venus condition, but the precise elliptical grammatical subject is not restated."
b["preconditions"]=["Source p366 third-house 'if in the third, by strangers' follows seventh lord aspecting Jupiter/Venus in eleventh; preserve the inherited aspect condition and conditional framing."]
b["exceptions_and_uncertainty"]=["Do not reinterpret this as an unrelated planet's placement in the third sufficient on its own; original subject is elliptical and remains qualified. No real stranger assistance is demonstrated."]
b["printed_anchor"]="if in the third, by strangers"

u_path=B/"UNRESOLVED_DRAFT.json"
u=json.loads(u_path.read_text())
assert len(u["issues"])==u["retained_count"]==64
assert all(x["id"]!="U65" for x in u["issues"])
u["issues"].append({"id":"U65","status":"SOURCE_PRECONDITION_AND_ELLIPSIS_CORRECTION_RETAINED","description":"Original PDF400/printed366 escape-by-friends/strangers clauses inherit seventh-lord ASPECT to Jupiter/Venus from preceding sentence. Earlier R2948–R2949 reduced this to planet in eleventh/third with no aspect. R2949's elliptical 'if in third' subject remains explicitly uncertain."})
u["retained_count"]=len(u["issues"])
FROZEN.parent.mkdir(parents=True,exist_ok=True)
FROZEN.write_bytes(raw)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
u_path.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"changes":[2948,2949],"original_sha256":hashlib.sha256(raw).hexdigest(),"current_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issues":u["retained_count"],"accepted":False},indent=2))
