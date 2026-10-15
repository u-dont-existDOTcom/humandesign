"""One-time original printed p355/PDF389 textual-direction correction.

This preserves both application directions printed in source rather than
silently harmonizing them. These are untested historical astrology claims.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P388_390.json"
BACK=B/"recovery/producer_p388_390_before_U66_p355_20261015.json"
assert not BACK.exists(), "One-time U66 patch was already attempted."
raw=SRC.read_bytes()
j=json.loads(raw)
hit=[r for r in j["units"] if r["local_id"]=="P388C042"]
assert len(hit)==1
r=hit[0]
assert r["pdf_pages"]==[389] and r["kind"]=="sun_and_moon_application_with_waning"
assert r["source_statement"]=="Source adds a more complicated branch involving Sun applying to its own lord and the Moon diminished in light, with the Moon's term lord and relevant house lords also applying."

r["kind"]="sun_house_ruler_application_bidirectional_textual_ambiguity"
r["source_statement"]="The original recovery passage first states Sun applying to the lord of its house, with Moon diminished in light; its following 'I meane' clarification instead describes the specified house/term lords applying TO the Sun. Preserve both printed application directions and the apparent inconsistency rather than converting either into one executable rule."
r["preconditions"]=[
 "Initial wording: Sun applies to lord of its house AND Moon is diminished in light.",
 "Following 'I meane' states lord of 'his House', Moon-term ruler and Sun-house ruler apply TO Sun; pronoun and conjunction/alternative grouping are not unequivocal."
]
r["exceptions_and_uncertainty"]=[
 "Original PDF389/printed355 seems to reverse the directed aspect in its clarification. No edition/erratum-authorized repair has established which direction is intended.",
 "The original grouping among Moon's decreasing light, house rulers, term ruler and their applications is nested and ambiguous. Historical recovery claim, no independently witnessed property return."
]
r["source_image_anchor"]="or if the Sun doe apply unto the Lord of his House ... I meane if ... doe apply to the Sun"
u_path=B/"UNRESOLVED_DRAFT.json"
u=json.loads(u_path.read_text())
assert len(u["issues"])==u["retained_count"]==65
assert not any(x["id"]=="U66" for x in u["issues"])
u["issues"].append({
 "id":"U66",
 "status":"SOURCE_TEXT_APPLICATION_DIRECTION_CONTRADICTION_RETAINED",
 "description":"Original PDF389/printed355 Sun-recovery clause first says Sun applies to own house-lord, then its 'I meane' clarification says house/term lords apply TO Sun. Earlier R2735 retained only first direction and indefinite 'also applying'. Both directions preserved; exact rule and nested Moon diminished qualifier unresolved."
})
u["retained_count"]=len(u["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
u_path.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({
 "updated_record":"R2735","source":"PDF389 printed355",
 "before_sha256":hashlib.sha256(raw).hexdigest(),
 "after_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
 "issue_count":len(u["issues"]),"accepted":False
},indent=2))
