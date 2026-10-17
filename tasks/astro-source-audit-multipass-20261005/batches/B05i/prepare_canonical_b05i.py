#!/usr/bin/env python3
"""Guarded, append-only historical archive admission for first-edition stature."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
IDX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05i_STATURE.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (RECOVERY / "INDEX_BEFORE_B05i.json", LATEST, RECEIPT):
    assert not path.exists(), f"Already prepared: {path}"

index = j(IDX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
z = j(B / "RELEASE_RECEIPT_20261017.json")
assert index["records_count"] == a["previous_lilly"] == 6644
assert index["batches"][-1]["id"] == "B05h"
assert index["read_numbered_chapters"] == list(range(1, 111))
assert index["next"]["chapter"] == "CXI" and index["next"]["pdf_page"] == 580
assert index["source_sha256"] == "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert index["empirical_validations"] == index["runtime_promotions"] == 0
assert not any(x["id"] == "B05i" for x in index["batches"])
assert r["record_count"] == a["new_historical_source_annotations"] == 27
assert [x["record_number"] for x in r["rules"]] == list(range(6645, 6672))
assert a["lilly_if_published"] == 6671 and a["historical_combined_if_published"] == 7737
assert r["empirical_validations"] == r["runtime_promotions"] == 0
assert z["crc_passed"] and z["all_hashes_passed"] and z["extraction_passed"]
assert z["replayed_tests_passed"] == 12 and sha(z["archive_path"]) == z["archive_sha256"]
assert sha(B / "RULES.json") == a["rules_sha256"] == z["rules_sha256"]

idx_rel = str(IDX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", idx_rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + idx_rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(IDX)], cwd=ROOT, text=True).strip()
)

RECOVERY.mkdir(exist_ok=True)
(RECOVERY / "INDEX_BEFORE_B05i.json").write_bytes(IDX.read_bytes())
(RECOVERY / "CURRENT_BEFORE_B05i.md").write_bytes(CURRENT.read_bytes())
(RECOVERY / "PROGRESS_BEFORE_B05i.md").write_bytes(PROGRESS.read_bytes())

index["batches"].append(
    {
        "id": "B05i",
        "path": "batches/B05i/RULES.json",
        "records_count": 27,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original printed CHAP CX/editorial CXI: stature and form of body, PDF580-581, "
            "next heading PDF581 and following witness PDF582. 24 historical observations "
            "and 3 navigation records: partile Ascendant-ruler aspects with strongest-planet "
            "tie-breaker, 5 planets x oriental/occidental table, Mercury dispositor and sign "
            "overrides, luminary analogy, 5 proportion sources. Original folios appear "
            "as 538/539 despite continuous pages; PDF582 shows 548. All alleged stature "
            "relationships are historical, not validated actual height predictions."
        ),
    }
)
index["records_count"] = 6671
index["read_numbered_chapters"].append(111)
index["status"] = "BOOK_III_STATURE_HISTORICAL_SOURCE_COMPLETE_NEXT_FACE_HAIR_SIGN"
index["next"] = {
    "pdf_page": 581,
    "printed_page_as_seen": 539,
    "sequential_printed_page_expected": 547,
    "chapter": "CXII",
    "printed_chapter_numeral": "CXI",
    "heading": "Nature of the Signes; Colour of the Face and Haire",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXI starts PDF581 below source divider; original folio appears "
        "539 after PDF580 folio538, although these follow printed545 in uninterrupted "
        "text. PDF582 folio548 resumes expected physical order."
    ),
    "research_scope": (
        "Historical sign/face/hair claims and country/climate caveats; strictly no "
        "modern race/ethnicity/health or biometric inference based on these stereotypes."
    ),
}
index["current_state"] = str(LATEST.relative_to(ROOT))
index["chapter_CXI_source_acceptance_note"] = (
    "R6645-R6671: 27 source records, 24 chapter claims and 3 following-chapter "
    "navigation. Source frames 580-582 hash-authenticated, archive replay 12 tests, "
    "zero independent height/physical outcome confirmations and no runtime promotion."
)
assert index["records_count"] == sum(x["records_count"] for x in index["batches"]) == 6671
assert index["read_numbered_chapters"] == list(range(1, 112))
IDX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
audit = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original first-edition Stature source accepted — historical only\n\n"
    + audit
    + "\n## Repository validation boundary\n\n"
    + "**R6645–R6671 historical source annotations**, 24 substantive and 3 navigation. "
    + "After authenticated GitHub publication: **6,671 Lilly + 1,066 Ptolemy = 7,737** "
    + "source/documentary records. Neither real human heights, facial form, ancestry nor "
    + "medical outcomes were tested. The source is not a validated height/physical "
    + "description predictor. **Zero empirical validations, zero runtime promotions.**\n"
)
PROGRESS.write_text(
    "# First-edition Lilly historical study through Stature, 2026-10-17\n\n"
    "After authenticated publication **7,737** source annotations (6,671 Lilly + "
    "1,066 Ptolemy). First-edition source frontier PDF581/894 (~65.0% by scan "
    "position; NOT numerical transcription or completed evidence). Stature and "
    "body-form chapter preserved with 27 historical-only annotations. PDF581 "
    "includes the start of next original printed CHAP CXI on sign, facial colour "
    "and hair; must retain period caveats and never presume predictive validity "
    "or ethnic classification. All independent validation and model runtime "
    "promotion in this source lane remain at zero.\n\n---\n\n"
    + (RECOVERY / "PROGRESS_BEFORE_B05i.md").read_text()
)
CURRENT.write_text(
    "# First-edition Lilly Stature original historical source accepted\n\n"
    "2026-10-17 Africa/Dakar UTC+0: records R6645–R6671 incorporated in "
    "historical-only source index, 6,671 Lilly + 1,066 retained Ptolemy = 7,737 "
    "after verified remote publication. Source frontier PDF581/894 scan position; "
    "no real-person height or health validation, no clinical/biometric assumptions, "
    "no runtime promotions. Following CHAP CXI nature of signs, face and hair starts "
    "mid original PDF581 (misprinted folio 539).\n\n---\n\n"
    + (RECOVERY / "CURRENT_BEFORE_B05i.md").read_text()
)
rec = {
    "batch": "B05i",
    "status": "GUARDED_CANONICAL_PREPARED_PENDING_REMOTE",
    "previous_git_blob": blob,
    "previous_index_sha256": sha(RECOVERY / "INDEX_BEFORE_B05i.json"),
    "new_index_sha256": sha(IDX),
    "current_sha256": sha(CURRENT),
    "latest_review_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 6671,
    "ptolemy": 1066,
    "combined_if_published": 7737,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
