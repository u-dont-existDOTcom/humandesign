"""One-time original-image correction on Lilly printed p366 (PDF400).
The last capture condition uses opposition ☍, not conjunction ☌.
Preserve the exact before-edit source as a separately hashed document.
These historical source claims do not establish guilt, recovery or capture.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[1]
source=B/"PRODUCER_SOURCE_DRAFT_P398_400.json"
prior=B/"recovery/producer_p398_400_before_20261014_p366_opposition_fix.json"
assert not prior.exists(),"Do not rerun one-time source migration"
original=source.read_bytes()
doc=json.loads(original)
hit=[r for r in doc["units"] if r["local_id"]=="P398C072"]
assert len(hit)==1
r=hit[0]
assert r["pdf_pages"]==[400]
assert r["kind"]=="other_capture_moon_eighth_mars_second"
assert r["source_statement"]=="Moon in eighth and conjunction to Mars in second closes the compact capture list."
assert r["preconditions"]==["Moon eighth, Mars second, conjunction as printed."]
r["kind"]="other_capture_moon_eighth_opposition_mars_second"
r["source_statement"]="The printed final capture-list clause places the Moon in the eighth house IN OPPOSITION (☍) to Mars in the second house; it does not prescribe conjunction."
r["preconditions"]=["Original PDF400/printed366 at the last line above Chapter LI: Moon in eighth, opposition (☍) to Mars in second. This is a historical author's statement only."]
r["exceptions_and_uncertainty"]=["The prior producer misread the opposition ☍ glyph as conjunction ☌ and inferred a false geometry conflict. No observed outcome or independent astrological validity follows."]
r["original_page_anchor"]="☽ In the eight, in ☍ to ♂ in the second."
prior.parent.mkdir(parents=True,exist_ok=True)
prior.write_bytes(original)
source.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
ledger_file=B/"UNRESOLVED_DRAFT.json"
issues=json.loads(ledger_file.read_text())
assert issues["retained_count"]==54
assert all(x["id"]!="U55" for x in issues["issues"])
issues["issues"].append({
    "id":"U55",
    "status":"SOURCE_IMAGE_CORRECTION_RETAINED",
    "description":"Original Lilly PDF400/printed366 last capture rule immediately above Chapter LI says Moon in eighth in OPPOSITION ☍ to Mars in second, NOT conjunction. Corrected R2973 / P398C072; removed spurious geometry-inconsistency gloss, froze original source bytes."
})
issues["retained_count"]=len(issues["issues"])
ledger_file.write_text(json.dumps(issues,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"record":"R2973","old_source_sha256":hashlib.sha256(original).hexdigest(),"new_source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"retained_source_issues":len(issues["issues"]),"admitted_to_canonical":False},indent=2))
