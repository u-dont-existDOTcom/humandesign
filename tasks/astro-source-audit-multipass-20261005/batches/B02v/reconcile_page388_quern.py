"""One-time image-first source repair: PDF388/printed354 reads 'Furnace or Quern'.
Quern is a hand grain mill, not an oven. Unaccepted editorial source only.
"""
from pathlib import Path
import json
import hashlib
B = Path(__file__).resolve().parent
src = B / "PRODUCER_SOURCE_DRAFT_P388_390.json"
backup = B / "recovery" / "producer_p388_390_before_20261014_quern_review.json"
assert not backup.exists(), "This one-time correction has already been applied"
raw = src.read_bytes()
doc = json.loads(raw)
found = [u for u in doc["units"] if u["kind"] == "tenth_moon_underground_oven"]
assert len(found) == 1
u = found[0]
assert u["pdf_pages"] == [388]
assert u["source_statement"] == "Moon in tenth is associated with an underground door/opening or a necessary household device such as a furnace or oven."
u["kind"] = "tenth_moon_underground_quern"
u["source_statement"] = "For the Moon in the tenth, Lilly places the entryway near a door under the ground or another frequently used household feature, giving a furnace or a quern (hand grain mill) as examples."
u["preconditions"] = ["Moon in tenth in this printed house-entry subsection."]
u["exceptions_and_uncertainty"] = ["Original PDF388/printed354 reads 'as a Furnace or Querne, or such like'; earlier editorial 'oven' was incorrect. Do not merge this with other Moon-based location sections."]
u["original_page_anchor"] = "as a Furnace or Querne, or such like"
backup.parent.mkdir(exist_ok=True)
backup.write_bytes(raw)
src.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
ledger_path = B / "UNRESOLVED_DRAFT.json"
ledger = json.loads(ledger_path.read_text())
assert all(i["id"] != "U51" for i in ledger["issues"])
ledger["issues"].append({
    "id":"U51", "status":"SOURCE_IMAGE_CORRECTION_RETAINED",
    "description":"Original PDF388/printed354 says 'as a Furnace or Querne' under Moon in tenth; earlier R2699 producer paraphrase substituted 'oven'. Corrected to quern/grain mill, with before-edit bytes frozen."
})
ledger["retained_count"]=len(ledger["issues"])
ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"corrected_record":"R2699","source_image":"PDF388/printed354","before_sha256":hashlib.sha256(raw).hexdigest(),"after_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"retained_issues":len(ledger["issues"]),"source_accepted":False},indent=2))
