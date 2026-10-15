"""One-time primary-image clause completeness correction, PDF391/printed357.

The printed paragraph explicitly offers the LORD OF MOON'S HOUSE
applying to the Moon as another recovery-time testimony. Historical
source-text capture only, not an observed outcome or validated forecast.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P391_392.json"
BACK=B/"recovery/producer_p391_392_before_U75_moon_domicile_20261015.json"
assert not BACK.exists(),"Already applied: inspect backup"
raw=SRC.read_bytes()
doc=json.loads(raw)
rows=[r for r in doc["units"] if r["local_id"]=="P391C018"]
assert len(rows)==1
r=rows[0]
assert r["kind"]=="part_of_fortune_asc_moon" and r["pdf_pages"]==[391]
assert r["source_statement"]=="The printed Part-of-Fortune-like symbol is examined for testimony with ascendant lord or Moon; mutual application is a recovery hope."
r["kind"]="part_fortune_and_moon_domicile_alternative_timing"
r["source_statement"]="Lilly says to inspect the printed Part-of-Fortune-like glyph for testimony with ascendant lord OR Moon, and their applications to each other as a hopeful timing sign of recovery; he adds a separate alternative, the lord of the Moon's domicile applying to the Moon, which the prior paraphrase omitted."
r["preconditions"]=[
 "Original PDF391/printed357: Part glyph has testimony with the lord of the ascendant OR Moon; source then discusses application among those referents.",
 "OR original distinct branch: lord of the Moon's own house applies TO the Moon."
]
r["exceptions_and_uncertainty"]=[
 "The phrase 'when any of them apply to each other' does not resolve every planetary source/target pair; retain without inventing simultaneous conjunction or exact precedence.",
 "Author promises 'time of the recovery in hope'; this is a historical prediction, not an independently verified object recovery. Part glyph/natural-house calculus has its own source limits."
]
r["original_page_anchor"]="or the Lord of the house of the ☽ to the ☽, there is the time of the recovery in hope"
ledgerpath=B/"UNRESOLVED_DRAFT.json"
u=json.loads(ledgerpath.read_text())
assert len(u["issues"])==u["retained_count"]==74
assert not any(i["id"]=="U75" for i in u["issues"])
u["issues"].append({"id":"U75","status":"SOURCE_OMITTED_ALTERNATIVE_REPAIRED","description":"Original PDF391/printed357 R2769 explicitly offers Moon-domicile lord applying to Moon as an alternative recovery-time testimony, in addition to Part-of-Fortune glyph with lord1/Moon mutual application. Earlier paraphrase omitted this clause and reduced timing to mere recovery hope. Restored alternative and kept referent grammar uncertain."})
u["retained_count"]=len(u["issues"])
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
ledgerpath.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"source_pdf":391,"record_id":2769,"before_sha256":hashlib.sha256(raw).hexdigest(),"after_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),"source_issue_count":len(u["issues"]),"accepted":False},indent=2))
