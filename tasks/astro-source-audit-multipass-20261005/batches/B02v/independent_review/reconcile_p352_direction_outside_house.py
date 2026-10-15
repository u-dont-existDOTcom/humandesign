"""Original printed352/PDF386 marginal scope for elemental compass directions.

The printed marginal 'This is, when Goods are certainly known to be out
of the House' visually aligns with the cardinal-directions clause. This
does not automatically qualify earlier room or hidden-site conditions.
No empirical astrology inference is endorsed.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P385_387.json"
BACK=B/"recovery/producer_p385_387_before_U70_p352_20261015.json"
assert not BACK.exists(),"Already applied; compare source hashes before retry"
raw=SRC.read_bytes()
j=json.loads(raw)
rows=[x for x in j["units"] if x["local_id"]=="P385C037"]
assert len(rows)==1
r=rows[0]
assert r["pdf_pages"]==[386]
assert r["kind"]=="goods_elements_cardinal_points"
assert r["source_statement"]=="For lost goods Lilly classifies the sign as fire/east, earth/south, air/west or water/north."
r["kind"]="goods_outside_house_element_cardinal_points"
r["source_statement"]="Only where the goods are already certainly known to be OUTSIDE the house (original marginal qualification), Lilly's selected sign yields historical directional associations: fiery/east, earthy/south, airy/west or watery/north."
r["preconditions"]=["Goods certainly known to be outside the house, per the printed margin aligned with this elemental-direction paragraph.","Relevant goods/fourth-house sign has been selected; source directs fire→east, earth→south, air→west, water→north."]
r["exceptions_and_uncertainty"]=["The printed marginal restriction attaches to this elemental compass-direction clause; avoid imposing it on all neighboring interior-room rules.","Historical sign-direction system is neither verified property geolocation nor a method to investigate people."]
r["printed_margin_anchor"]="This is, when Goods are certainly known to be out of the House."
p=B/"UNRESOLVED_DRAFT.json"
u=json.loads(p.read_text())
assert u["retained_count"]==len(u["issues"])==69
assert all(x["id"]!="U70" for x in u["issues"])
u["issues"].append({"id":"U70","status":"SOURCE_MARGINAL_PRECONDITION_CORRECTION","description":"Original PDF386/printed352 elemental compass-direction sentence has marginal instruction 'This is, when Goods are certainly known to be out of the House.' Earlier R2670 omitted this gating premise. Added the outside-house qualification only to elemental-direction rule, not unrelated adjacent interior-room conditions."})
u["retained_count"]=len(u["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
p.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"record":"R2670","source_image":"PDF386 printed352","backup_sha256":hashlib.sha256(raw).hexdigest(),"source_current_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"retained_issues":len(u["issues"]),"accepted_new":0},indent=2))
