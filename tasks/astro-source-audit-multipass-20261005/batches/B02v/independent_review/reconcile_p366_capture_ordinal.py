"""One-time original printed p366 capture-list SOURCE ORDER correction.

This reassigns two *provisional* record slots so R2971 and R2972 align
with the order physically printed on original PDF400; no accepted index
or empirical observation changes. The previous entire component is frozen.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P398_400.json"
BACK=B/"recovery/producer_p398_400_before_U68_capture_order_20261015.json"
assert not BACK.exists(),"Already attempted; do not repeat."
raw=SRC.read_bytes()
j=json.loads(raw)
by={x["local_id"]:x for x in j["units"]}
a=by["P398C070"]  # provisional R2971
b=by["P398C071"]  # provisional R2972
assert a["pdf_pages"]==b["pdf_pages"]==[400]
assert a["kind"]=="other_capture_seventh_first"
assert b["kind"]=="other_capture_moon_squares_from_saturn_to_mercury"
assert a["source_statement"]=="Seventh lord in first is included as an extra capture condition."
assert b["source_statement"]=="Moon separating from Saturn conjunction and applying to Mercury square is one of the printed combinations."

a["kind"]="other_capture_moon_squares_from_saturn_to_mercury"
a["source_statement"]="Original p366 first lists the Moon separating from conjunction with Saturn and applying by square to Mercury; this appears BEFORE the seventh-lord-in-first phrase in the printed capture list."
a["preconditions"]=["Moon separates from Saturn conjunction and applies to Mercury square, original PDF400/printed366."]
a["exceptions_and_uncertainty"]=["The following 'Lord of seventh in first' is on the next printed line; punctuation does not settle whether it is an independent alternative or a further conjunct. Do not silently demand both."]
a["original_page_anchor"]="Moon Separating from a conjunction of Saturn, applying to a square of Mercury"

b["kind"]="other_capture_seventh_first"
b["source_statement"]="After the lunar Saturn-to-Mercury condition, Lilly prints 'Lord of the seventh in the first' as a further alleged capture testimony; its conjunction/alternation with the previous line remains textually unresolved."
b["preconditions"]=["Seventh-house lord situated in the ascendant/first house; sentence appears AFTER the lunar Saturn-to-Mercury clause in original PDF400."]
b["exceptions_and_uncertainty"]=["Source is an unnumbered sequence; punctuation does not prove this condition must be conjoined with the preceding lunar aspect. No actual capture or guilt is established."]
b["original_page_anchor"]="Lord of the seventh in the first"

ledger=B/"UNRESOLVED_DRAFT.json"
u=json.loads(ledger.read_text())
assert u["retained_count"]==len(u["issues"])==67
assert all(x["id"]!="U68" for x in u["issues"])
u["issues"].append({"id":"U68","status":"SOURCE_PRINTED_SEQUENCE_CORRECTION_RETAINED","description":"Original PDF400/p366 prints Moon separating from conjunction of Saturn then applying square Mercury BEFORE 'Lord of seventh in first'. Previous provisional R2971/72 were reversed. Corrected slot order: R2971 lunar application, R2972 seventh lord in first. Independence/conjunction of the two printed lines is unresolved; original producer bytes frozen."})
u["retained_count"]=len(u["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
ledger.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_pdf":400,"old_ids":{"R2971":"seventh_lord_first","R2972":"lunar_aspect"},"new_ids":{"R2971":"lunar_aspect","R2972":"seventh_lord_first"},"before_sha256":hashlib.sha256(raw).hexdigest(),"after_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"issues":len(u["issues"]),"newly_accepted":0},indent=2))
