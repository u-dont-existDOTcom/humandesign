#!/usr/bin/env python3
"""Guard original Lilly CXLVII honor-continuity records against canonical baseline."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07a_HONOUR_DURATION.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07a.json"):
    assert not p.exists(), f"Duplicate or interrupted source admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["previous_lilly"] == 9367
assert i["read_numbered_chapters"] == list(range(1, 147))
assert i["batches"][-1]["id"] == "B06z"
assert i["next"]["chapter"] == "CXLVII"
assert i["next"]["printed_chapter_numeral"] == "CXLVII"
assert i["next"]["pdf_page"] == 656
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07a" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 77
assert [x["record_number"] for x in r["rules"]] == list(range(9368, 9445))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R9443", "R9444"]
assert r["substantive"] == a["substantive"] == 75
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 9444 and a["combined_if_published"] == 10510
assert w["body_original_pdf_frames"] == [656, 657, 658]
assert w["following_printed_CXLVIII_heading_pdf"] == 658
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert not lim["source_status_duration_model_executable"]
assert not lim["actual_person_moral_status_or_travel_safety_claim_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B07a.json"),
    (CURRENT, "CURRENT_BEFORE_B07a.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07a.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07a",
        "path": "batches/B07a/RULES.json",
        "records_count": 77,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly printed CHAP CXLVII If Dignity "
            "or Honour shall continue original PDF656 lower "
            "through PDF658 upper (printed622-624), after "
            "separate CXLVI; before printed CHAP CXLVIII "
            "Magistery/Profession lower PDF658. "
            "6 source-photo groups with 75 substantive "
            "historical clauses and two following navigation "
            "R9368–R9444. Original phase distinctions: "
            "strong Jupiter/Venus continuing rise, moderate "
            "benefics slow/obstructed, weak temporary decline; "
            "strong Saturn/Mars continuing with interruption, "
            "weak gradual wear or loss; Mercury fast early rise "
            "with intellect-mediated preservation or eventual "
            "fall. Explicit absence-of-light-contact fallback "
            "tenth occupant then tenth ruler, fixed-sign composite "
            "with friendly Sun/Moon/Jupiter/Venus aspects. "
            "Internal Speciall Aphorismes on Hyades/Hercules/"
            "Cor Scorpii/Lanx Australis, adverse directions "
            "AND revolutions vs one-trigger temporary fall, "
            "King-versus-people chart concurrence, pejorative "
            "Moon/Mars infamy claims and unresolved glyphs. "
            "No real human rank/time/reputation/morality "
            "predictive validation and zero runtime promotions."
        ),
    }
)
i["records_count"] = 9444
i["read_numbered_chapters"].append(147)
i["status"] = "BOOK_III_CXLVII_HONOUR_CONTINUITY_NEXT_CXLVIII_PROFESSION"
i["next"] = {
    "pdf_page": 658,
    "printed_page": 624,
    "chapter": "CXLVIII",
    "printed_chapter_numeral": "CXLVIII",
    "heading": "Of the Magistery, Exercitation or Profession of the Native",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLVIII begins after distinct "
        "divider original PDF658/printed624 middle "
        "following CXLVII Speciall Aphorismes on "
        "honour duration. The profession chapter "
        "continues through PDF659/printed625 onward; "
        "inspect full next numbered source boundary. "
        "Its opening defines Magistery and three "
        "profession questions, separate from honors."
    ),
    "research_scope": (
        "Historical occupation/trade/study/activity "
        "frequency and sources, career conditions "
        "Mercury/Venus/Mars, tenth-house rulership, "
        "three source questions for profession "
        "presence, kind, and livelihood. "
        "Period roles not measured modern jobs. "
        "No actual person profession accuracy tested."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLVII_honor_duration_acceptance_note"] = (
    "B07a R9368-R9444 77 original source notes, "
    "6 reversible photo groups PDF656–660 SHA "
    "and 26 extracted archive replay tests. "
    "Duration, reversal and infamy are separate "
    "historical claims, zero human prediction "
    "or runtime source promotions. Chinese 72 "
    "source notes independently indexed."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9444
assert i["read_numbered_chapters"] == list(range(1, 148))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original honor-duration and reversal source documented\n\n"
    + review
    + "\nAfter verified remote source publication **9,444 "
    + "Lilly +1,066 Ptolemy=10,510 historical annotations**. "
    + "26 first-edition image/archive replay tests, no "
    + "real human honor-duration or reputation forecast "
    + "validated and zero runtime source promotions.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 through honor-duration CXLVII — 2026-10-18\n\n"
    "After publication **10,510 historical source "
    "records** (9,444 Lilly +1,066 Ptolemy). "
    "First-edition physical source frontier "
    "PDF658/894 (**73.6% scanned page position "
    "ONLY, not scientific completion**). "
    "B07a 77 historic conditions preserves strong/"
    "moderate/weak planet timecourses, recovery "
    "vs total collapse, fixed-star triggers and "
    "the original King's/nation two-chart condition. "
    "No real human forecast and no runtime scorer. "
    "NEXT printed CXLVIII occupation/profession "
    "from PDF658 onward. Separate Chinese "
    "BaZi46/Zi Wei26 source notes remain open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07a.md").read_text()
)
CURRENT.write_text(
    "# Lilly CXLVII honor duration documented; profession chapter next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07a historical source R9368-R9444 "
    "locally admitted pending remote source verification. "
    "After verified remote 9,444 Lilly +1,066 "
    "Ptolemy =10,510 source-only annotations. "
    "26 first-edition and archive tests pass, "
    "no human reputation/rank data or source "
    "runtime rule promotions. NEXT CXLVIII "
    "profession begins original PDF658. "
    "Chinese 72 notes remain independently indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07a.md").read_text()
)
receipt = {
    "batch": "B07a",
    "status": "GUARDED_CXLVII_ORIGINAL_HONOR_DURATION_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07a.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9444,
    "ptolemy_retained": 1066,
    "combined_if_published": 10510,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
