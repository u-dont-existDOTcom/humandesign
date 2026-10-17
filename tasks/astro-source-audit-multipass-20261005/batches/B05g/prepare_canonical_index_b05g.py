#!/usr/bin/env python3
"""Guarded append-only archival acceptance of original printed CHAP CVIII.
Source annotations, not human personality validations. No runtime promotions.
"""
import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05g_PLANETARY_MANNERS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json"

H = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B05g.json"):
    assert not path.exists(), f"Previously written (fail closed): {path}"

index = json.loads(IDX.read_text())
a = json.loads((B / "ACCEPTANCE.json").read_text())
r = json.loads((B / "RULES.json").read_text())
z = json.loads((B / "SOURCE_RELEASE_RECEIPT_20261017.json").read_text())
assert index["records_count"] == a["prior_lilly"] == 6560
assert index["read_numbered_chapters"] == list(range(1, 109))
assert index["batches"][-1]["id"] == "B05f"
assert index["next"]["chapter"] == "CIX" and index["next"]["pdf_page"] == 573
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert index["source_sha256"] == "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert not any(x["id"] == "B05g" for x in index["batches"])
assert r["record_count"] == a["local_historical_annotations"] == 31
assert [x["record_number"] for x in r["rules"]] == list(range(6561, 6592))
assert H(B / "RULES.json") == a["accepted_rules_sha256"]
assert z["CRC"] and z["SHA256"] and z["extracted_tests_passed"] == 5
assert H(z["archive_path"]) == z["archive_sha256"]
assert not z["remote_published"] and a["empirical_validations"] == a["runtime_promotions"] == 0
assert all(not x["validated_personality_prediction"] and not x["runtime_model_promoted"] for x in r["rules"])
rel = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert blob == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()

BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B05g.json").write_bytes(IDX.read_bytes())
(BACK / "CURRENT_BEFORE_B05g.md").write_bytes(CUR.read_bytes())
(BACK / "PROGRESS_BEFORE_B05g.md").write_bytes(PROGRESS.read_bytes())
index["batches"].append({
    "id": "B05g",
    "path": "batches/B05g/RULES.json",
    "records_count": 31,
    "sha256": a["accepted_rules_sha256"],
    "scope": (
        "First edition printed CHAP CVIII/editorial CIX: planetary character/manners descriptions, "
        "original PDF573-577 with original PDF578 following-chapter witness. 29 substantive historical "
        "source annotations (seven planets' favorable/unfavorable manner claims; planet mixtures and "
        "conditionality) and 2 following-chapter navigation records; 8 source-passage groups. "
        "Neither planetary character, moral worth nor dangerousness validated with independent humans."
    )
})
index["records_count"] = 6591
index["read_numbered_chapters"].append(109)
index["status"] = "BOOK_III_PLANETARY_MANNERS_HISTORIC_SOURCE_COMPLETE_NEXT_WIT_UNDERSTANDING"
index["next"] = {
    "pdf_page": 577,
    "printed_page": 543,
    "chapter": "CX",
    "printed_chapter_numeral": "CIX",
    "heading": "Of the Wit or Understanding of the Native",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CIX starts original first edition PDF577/printed543 and proceeds through "
        "PDF578-580. PDF580 is misprinted page 538 after printed545 but scan/text order is continuous."
    ),
    "research_scope": (
        "Keep every astrological aptitude/learning/intellect condition and rival implication intact, "
        "without treating intelligence, cognitive disability or mental health labels as validated."
    )
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CIX_source_acceptance_note"] = (
    "31 historical records R6561-R6591; 29 planetary manners claims and 2 next chapter navigation. "
    "Physical source PDF573-578, 8 groups. Descriptions of moral conduct/traits remain unsupported by "
    "independent human testing. Zero empirical validations and zero runtime promotions."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 6591
assert index["read_numbered_chapters"] == list(range(1, 110))
IDX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
text = """# Original Lilly planetary manners — historical documentation only

2026-10-17 Africa/Dakar UTC+0. Printed CHAP CVIII/editorial CIX, source PDF573-577,
with following CHAP CIX opening at PDF577 (printed543). Source boundary through PDF578
SHA256-locked. This batch adds 31 annotations R6561-R6591 (29 source claims, 2 navigation).
The first edition lists favorable and unfavorable planetary traits and mixed signification
under varying dignities: these are **not independently demonstrated human character predictions**.
Do not classify a person's morality, violence, capability or mental health from this text.

**After authenticated publication: 6,591 Lilly + 1,066 retained Ptolemy = 7,657**
historical/documentary annotations. Source progress approximately 577/894 = 64.5% of
scanned page position; not a proportion of completed numeric transcriptions or empirical
astrology research. Zero new independent validations and zero rules added to runtime.

NEXT printed CHAP CIX/editorial CX *Of the Wit or Understanding of the Native*,
starts PDF577/printed543. Its next physical page after printed545 is marked printed538
in the original (an apparent pagination misprint). Preserve the scan order and distinguish
typographical page numbers from authoritative image sequence.
"""
LATEST.write_text(text)
PROGRESS.write_text("# Original Lilly historical source progress after planetary manners, 2026-10-17\n\n"
    "7,657 source annotations after authenticated publication (6,591 Lilly and 1,066 Ptolemy). "
    "Source frontier PDF577/894 (~64.5%, page-position only). Original printed CHAP CVIII "
    "planet-specific manners historically documented, no independent personality evidence, no "
    "new source rule in runtime. Next printed CHAP CIX, intellect, PDF577-580. Dense numerical "
    "table reconstruction and independent forward/blind testing still open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B05g.md").read_text())
CUR.write_text("# Planetary manners documentary source accepted; original intellect chapter next\n\n"
    "2026-10-17: historical annotation records R6561-R6591 prepared with guarded append-only "
    "index: 6,591 Lilly + 1,066 retained Ptolemy = 7,657 after remote publication. "
    "These are not personality validation successes. No runtime promotions. "
    "Next printed CHAP CIX/editorial CX begins original PDF577. "
    "Numerical and predictive test lanes unresolved.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B05g.md").read_text())
receipt = {
    "batch": "B05g", "status": "GUARDED_CANONICAL_PREPARED_PENDING_GITHUB",
    "old_index_git_blob_sha1": blob, "old_index_sha256": H(BACK / "INDEX_BEFORE_B05g.json"),
    "new_index_sha256": H(IDX), "latest_report_sha256": H(LATEST),
    "progress_report_sha256": H(PROGRESS), "current_sha256": H(CUR),
    "accepted_rules_sha256": a["accepted_rules_sha256"],
    "archive_sha256": z["archive_sha256"], "lilly_if_published": 6591,
    "ptolemy_retained": 1066, "combined_if_published": 7657,
    "empirical_validations": 0, "runtime_promotions": 0, "remote_published": False
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
