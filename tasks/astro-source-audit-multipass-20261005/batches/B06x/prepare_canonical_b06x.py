#!/usr/bin/env python3
"""Guarded original unnumbered tenth-house source append without chapter increment."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06x_TENTH_INTRO.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06x.json"):
    assert not p.exists(), f"Duplicate or partially interrupted admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9105
assert i["read_numbered_chapters"] == list(range(1, 145))
assert i["batches"][-1]["id"] == "B06w"
assert i["next"]["chapter"] == "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES"
assert i["next"]["pdf_page"] == 649
assert i["next"]["printed_chapter_numeral"] is None
assert i["next"]["following_printed_chapter_numeral"] == "CXLIIII"
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06x" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 19
assert [x["record_number"] for x in r["rules"]] == list(range(9106, 9125))
assert [x["id"] for x in r["rules"] if x["role"] == "next_numbered_navigation"] == [
    "R9123",
    "R9124",
]
assert r["substantive"] == a["substantive"] == 17
assert a["numbered_chapters_added"] == 0
assert a["lilly_if_published"] == 9124
assert a["combined_if_published"] == 10190
assert w["unnumbered"]
assert w["body_original_pdf_frames"] == [649]
assert w["following_printed_CXLIIII_heading_pdf"] == 649
assert len(m["source_groups"]) == m["source_group_count"] == 3
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 12 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for old, name in (
    (INDEX, "INDEX_BEFORE_B06x.json"),
    (CURRENT, "CURRENT_BEFORE_B06x.md"),
    (PROGRESS, "PROGRESS_BEFORE_B06x.md"),
):
    (BACK / name).write_bytes(old.read_bytes())

i["batches"].append(
    {
        "id": "B06x",
        "path": "batches/B06x/RULES.json",
        "records_count": 19,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly substantive UNNUMBERED tenth-house "
            "intro on Honors/Preferments/Dignities, original PDF649/printed615 "
            "before separately numbered CHAP CXLIIII later same frame. "
            "3 reversible source groups, 17 historical qualified "
            "clauses and 2 next-chapter navigation R9106-R9124. "
            "Author source hierarchy: luminaries especially Sun, "
            "planets within half orb aspecting lights; secondly "
            "lord of Midheaven, third planets in Midheaven, fourth "
            "first/second-magnitude regal stars near tenth or first cusp. "
            "Original orb sizes and fixed-star cusp distances unspecified. "
            "No verified human status/preferment or social rank "
            "predictions, no production runtime promotions. "
            "Chinese source study independently indexed."
        ),
    }
)
i["records_count"] = 9124
i["status"] = "BOOK_III_UNNUMBERED_TENTH_HOUSE_NEXT_CXLIIII_DIGNITIES"
i["next"] = {
    "pdf_page": 649,
    "printed_page": 615,
    "chapter": "CXLV",
    "printed_chapter_numeral": "CXLIIII",
    "heading": "Whether the Native shall have Dignity or Preferments, or None at all",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLIIII starts beneath horizontal "
        "divider around the middle of original PDF649/printed615, "
        "after UNNUMBERED tenth-house summary in upper same page. "
        "Continues through original PDF650 and onward. Inspect "
        "the next separately printed numbered seam before "
        "acceptance; keep source fixed-star star positions and "
        "class-relative beggar/king example together."
    ),
    "research_scope": (
        "Historical alleged honor, rank, official preferment "
        "and social esteem by dignity, angularity, house ruler "
        "and fixed-star contact with explicit class-relative "
        "limitations. No validated real career forecast."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["unnumbered_tenth_source_acceptance_note"] = (
    "B06x historic R9106-R9124, 19 archival claims, "
    "original PDF649-651 SHA photos, 12 extracted "
    "ZIP replays. Four source-priority classes "
    "preserved and numbered chapter count unchanged."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9124
assert i["read_numbered_chapters"] == list(range(1, 145))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original unnumbered tenth-house source accepted\n\n"
    + review
    + "\nHistorical source record, not career forecasting. "
    + "9,124 Lilly +1,066 Ptolemy =10,190 documentary notes "
    + "after remote publication; 12 source/ZIP checks, zero "
    + "real status predictions and zero promoted rules.\n"
)
PROGRESS.write_text(
    "# Lilly first edition through unnumbered tenth-house honors — 2026-10-18\n\n"
    "After source publication 10,190 historical annotations "
    "(9,124 Lilly +1,066 Ptolemy), original PDF649/894 "
    "(72.6% physical scan position only). B06x adds 19 "
    "records preserving the four priority classes "
    "and specific orb/magnitude conditions; no actual "
    "career/rank accuracy and no runtime model change. "
    "The unnumbered source does not increment chapter count. "
    "NEXT original printed CXLIIII on status PDF649 onward; "
    "Chinese BaZi 46 and Zi Wei 26 notes separate.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06x.md").read_text()
)
CURRENT.write_text(
    "# Lilly tenth-house unnumbered introduction complete; numbered CXLIIII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B06x source R9106-R9124 prepared for remote source publication. "
    "After verified publication 9,124 Lilly +1,066 Ptolemy "
    "=10,190 archival historic notes. No real honor/career "
    "predictions validated or scoring rule promotions. "
    "12 archive-replayed integrity tests PASS. "
    "Original numbered chapter count unchanged. "
    "NEXT printed CXLIIII later PDF649; Chinese source "
    "notes remain 46 BaZi and 26 Zi Wei.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06x.md").read_text()
)
receipt = {
    "batch": "B06x",
    "status": "GUARDED_UNNUMBERED_TENTH_SOURCE_PREPARED_PENDING_REMOTE",
    "previous_index_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06x.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9124,
    "ptolemy_retained": 1066,
    "combined_if_published": 10190,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
