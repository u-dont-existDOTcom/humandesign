#!/usr/bin/env python3
"""Guarded append of Lilly 1647 CXLVI causes of preferment historical text."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06z_PREFERMENT_CAUSES.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06z.json"):
    assert not p.exists(), f"Duplicate or incomplete source admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9312
assert i["read_numbered_chapters"] == list(range(1, 146))
assert i["batches"][-1]["id"] == "B06y"
assert i["next"]["chapter"] == "CXLVI"
assert i["next"]["printed_chapter_numeral"] == "CXLVI"
assert i["next"]["pdf_page"] == 655
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06z" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 55
assert [x["record_number"] for x in r["rules"]] == list(range(9313, 9368))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R9366", "R9367"]
assert r["substantive"] == a["substantive"] == 53
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 9367 and a["combined_if_published"] == 10433
assert w["body_original_pdf_frames"] == [655, 656]
assert w["following_printed_CXLVII_heading_pdf"] == 656
assert len(m["source_groups"]) == m["source_group_count"] == 4
assert not lim["printed_CXLV_text_observed"]
assert not lim["real_person_recommendation_or_moral_classification_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 20 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B06z.json"),
    (CURRENT, "CURRENT_BEFORE_B06z.md"),
    (PROGRESS, "PROGRESS_BEFORE_B06z.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B06z",
        "path": "batches/B06z/RULES.json",
        "records_count": 55,
        "sha256": a["rules_sha256"],
        "scope": (
            "Lilly Christian Astrology original first edition 1647 "
            "printed CHAP CXLVI How the Kind/Quality/Cause of "
            "Preferment, original PDF655 middle through PDF656 "
            "middle (printed621–622), after original skipped "
            "printed CHAP CXLV, before distinct CHAP CXLVII "
            "If Honour shall continue later PDF656. Four "
            "reversible source/photo groups and 53 substantive "
            "historical annotations + two next-chapter "
            "navigation R9313–R9367. Eligibility of planets "
            "partile-aspecting better fortified luminary, "
            "Saturn inheritance and elders, Jupiter/Venus "
            "virtues/lawful people, Mars military expedition "
            "and Mercury education/oratory/merchants. "
            "Natal house of planet modifies alleged causes "
            "(first own industry, second riches). Source "
            "conditional fallback if no light-aspecting "
            "planet -> strongest tenth occupant -> if empty "
            "lord of tenth with natal house, plus an "
            "alternative astrologers' luminary-dispositor "
            "or tenth-ruler partile method with no validated "
            "priority. No actual human career prediction, "
            "person-level moral inference or runtime promotions."
        ),
    }
)
i["records_count"] = 9367
i["read_numbered_chapters"].append(146)
i["status"] = "BOOK_III_CXLVI_PREFERMENT_CAUSES_NEXT_CXLVII_CONTINUATION"
i["next"] = {
    "pdf_page": 656,
    "printed_page": 622,
    "chapter": "CXLVII",
    "printed_chapter_numeral": "CXLVII",
    "heading": "If the Dignity or Honour shall continue",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLVII starts after divider in "
        "lower original PDF656/printed622 following "
        "CXLVI causes, runs through PDF657/printed623 "
        "and PDF658/printed624 upper, including "
        "internal Speciall Aphorismes. Next printed "
        "CXLVIII Of Magistery/Profession starts "
        "later PDF658. Verify exact seam before "
        "accepting CXLVII."
    ),
    "research_scope": (
        "Historical persistence, increasing/decreasing "
        "reputation, sudden loss/temporary interruptions, "
        "luminary partile contacts, tenth-house occupancy, "
        "tenth ruler signs/aspects and internal fixed-star "
        "aphorisms; no real person's career prognosis."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLVI_cause_source_acceptance_note"] = (
    "B06z historic R9313–R9367, 55 annotations, "
    "PDF655–658 source SHA and 20 extracted "
    "archive tests, verified multi-step source "
    "fallback and separate alternative author method. "
    "Original printed CXLV omission preserved, "
    "Chinese 72 source records independent. "
    "No human status accuracy and no runtime rules."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9367
assert i["read_numbered_chapters"] == list(range(1, 147))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly CXLVI causes of preferment historically documented\n\n"
    + review
    + "\nAfter verified GitHub publication **9,367 Lilly + "
    + "1,066 Ptolemy =10,433 historical source notes**. "
    + "Twenty source-photo and portable archive integrity "
    + "checks pass, no independently tested human career "
    + "causes and zero promoted runtime models.\n"
)
PROGRESS.write_text(
    "# Lilly original first-edition through causes of preferment — 2026-10-18\n\n"
    "Following remote verification **10,433 historical "
    "source annotations** (9,367 Lilly +1,066 Ptolemy), "
    "original book scanned-frame frontier PDF656/894 "
    "(**73.4% physical page-position only**, NOT "
    "research completion). New CXLVI adds 55 "
    "source-only notes on planetary and house "
    "possible causes of preferment plus alternative "
    "eligibility/fallback methods. Zero actual "
    "human occupational/rank accuracy and no runtime "
    "model promotion. NEXT printed CXLVII "
    "persistence of honors starts PDF656, ends "
    "before printed CXLVIII on PDF658. "
    "Chinese BaZi46/Zi Wei26 source notes separate.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06z.md").read_text()
)
CURRENT.write_text(
    "# Lilly original CXLVI types/causes of preferment documented; CXLVII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B06z "
    "R9313–R9367 prepared; after verified "
    "remote readback 9,367 Lilly +1,066 "
    "Ptolemy =10,433 archival source notes. "
    "20 image/source/portable ZIP tests PASS. "
    "No human career or financial status "
    "prediction validated, no model promotions. "
    "NEXT printed CXLVII honor duration from "
    "lower PDF656; Chinese source-only BaZi46/"
    "Zi Wei26 independently preserved.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06z.md").read_text()
)
receipt = {
    "batch": "B06z",
    "status": "GUARDED_CXLVI_ORIGINAL_SOURCE_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06z.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9367,
    "ptolemy_retained": 1066,
    "combined_if_published": 10433,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
