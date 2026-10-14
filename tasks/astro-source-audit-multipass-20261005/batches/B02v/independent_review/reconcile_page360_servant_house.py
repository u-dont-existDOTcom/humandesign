"""Source-image correction: printed p360 servant rule uses SIXTH house.

Historical documentary paraphrase only. No finding of real guilt or suspects.
The original producer file is backed up byte-for-byte before modification.
"""
from pathlib import Path
import hashlib, json

B = Path(__file__).resolve().parents[1]
source = B / "PRODUCER_SOURCE_DRAFT_P393_395.json"
backup = B / "recovery/producer_p393_395_before_20261014_servant_sixth_review.json"
assert not backup.exists(), "Correction already attempted: inspect backup"
original = source.read_bytes()
draft = json.loads(original)
matches = [r for r in draft["units"] if r["kind"] == "first_luminaries_servant"]
assert len(matches) == 1
r = matches[0]
assert r["pdf_pages"] == [394]
assert r["source_statement"] == "Sun or Moon in first is associated in this list with a servant."
assert r["preconditions"] == ["Either Sun or Moon in ascendant."]
r["kind"] = "sixth_luminaries_servant"
r["source_statement"] = "In Lilly's historical offender-role list, Sun OR Moon in the SIXTH house denotes a servant (not the first house)."
r["preconditions"] = ["Sun OR Moon physically in the SIXTH house in the p360 'Who did the Deed or Theft' subsection."]
r["exceptions_and_uncertainty"] = ["Original PDF394/printed360 says 'in the sixt, a Servant'; the earlier producer 'first' was a source-transcription error. This is not forensic evidence."]
r["original_page_anchor"] = "in the sixt, a Servant"
backup.parent.mkdir(parents=True, exist_ok=True)
backup.write_bytes(original)
source.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n")
issues_file = B / "UNRESOLVED_DRAFT.json"
issues = json.loads(issues_file.read_text())
assert issues["retained_count"] == 52
assert all(entry["id"] != "U53" for entry in issues["issues"])
issues["issues"].append({
    "id": "U53",
    "status": "SOURCE_IMAGE_CORRECTION_RETAINED",
    "description": "Original PDF394/printed360 'Who did the Deed or Theft': Sun OR Moon 'in the sixt, a Servant'. Former draft R2835 erroneously identified first/ascendant; corrected to SIXTH, with before-edit producer JSON preserved. Historical allegation only."
})
issues["retained_count"] = len(issues["issues"])
issues_file.write_text(json.dumps(issues, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({
    "record": 2835, "source_page": 394, "old_kind": "first_luminaries_servant",
    "new_kind": r["kind"], "before_sha256": hashlib.sha256(original).hexdigest(),
    "after_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "uncertainties": issues["retained_count"], "source_accepted": False
}, indent=2))
