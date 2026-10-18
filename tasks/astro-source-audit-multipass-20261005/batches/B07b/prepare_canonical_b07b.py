#!/usr/bin/env python3
"""Guarded source index admission for original 1647 Lilly vocational Magistery."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07b_PROFESSION.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07b.json"):
    assert not p.exists(), f"Duplicate or incomplete source admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9444
assert i["read_numbered_chapters"] == list(range(1, 148))
assert i["batches"][-1]["id"] == "B07a"
assert i["next"]["chapter"] == "CXLVIII"
assert i["next"]["printed_chapter_numeral"] == "CXLVIII"
assert i["next"]["pdf_page"] == 658
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07b" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 82
assert [x["record_number"] for x in r["rules"]] == list(range(9445, 9527))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R9525", "R9526"]
assert r["substantive"] == a["substantive"] == 80
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 9526 and a["combined_if_published"] == 10592
assert w["body_original_pdf_frames"] == [658, 659, 660]
assert w["following_printed_CXLIX_heading_pdf"] == 660
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert not lim["original_profession_selection_algorithm_complete"]
assert not lim["ptolemy_profession_rules_crosscollated"]
assert not lim["actual_person_professional_moral_labels_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
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
for old, name in (
    (INDEX, "INDEX_BEFORE_B07b.json"),
    (CURRENT, "CURRENT_BEFORE_B07b.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07b.md"),
):
    (BACK / name).write_bytes(old.read_bytes())

i["batches"].append(
    {
        "id": "B07b",
        "path": "batches/B07b/RULES.json",
        "records_count": 82,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 first edition printed "
            "CHAP CXLVIII Magistery/Exercitation/Profession, "
            "PDF658 middle to PDF660 upper (printed624–626). "
            "Six image-anchored source groups: 80 substantive "
            "period clauses and 2 next CXLIX navigation "
            "R9445–R9526. Historical magistery defined "
            "as main lifetime study, delight, occupation, "
            "livelihood, esteem and time use; three distinct "
            "questions: presence, type, fortune/fame. "
            "Mars body/strength, Venus delight, Mercury mind; "
            "eligible candidates tenth/first/seventh, dignified "
            "and not combust/under beams, fallback to one "
            "of three ruling MC with dignity, then closest "
            "partile Moon aspects prioritizing strength, "
            "aspect and sinister orientation; ambiguous "
            "Moon half-orb fallback excluding malefic "
            "conjunction/square/opposition, last solar "
            "antecedence selection, lower-tier alleged "
            "no/ignoble negligent vocation stereotypes. "
            "Separate Ptolemy-attributed two-way morning "
            "Sun-riser and MC ruler/occupant with Moon, "
            "both routes preferred but one permitted, "
            "not independently cross-collated. "
            "No tested human jobs or runtime promotions."
        ),
    }
)
i["records_count"] = 9526
i["read_numbered_chapters"].append(148)
i["status"] = "BOOK_III_CXLVIII_VOCATION_SOURCE_NEXT_CXLIX_PROFESSIONAL_APHORISMS"
i["next"] = {
    "pdf_page": 660,
    "printed_page": 626,
    "chapter": "CXLIX",
    "printed_chapter_numeral": "CXLIX",
    "heading": (
        "Severall experimented Aphorismes concerning the Native's Magistery, Trade or Profession"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLIX begins after a divider "
        "mid original PDF660/printed626, following "
        "CXLVIII's Ptolemy-attributed profession "
        "significator method. It continues PDF661 "
        "onwards with unnumbered Mercury/Venus/Mars "
        "and source mixture subsections; inspect "
        "original PDF661–677 and true next "
        "printed chapter boundary. Treat vocation "
        "occupation catalogue separate from "
        "CXLVIII existence/kind/fortune questions."
    ),
    "research_scope": (
        "Detailed historical profession categories by "
        "Mercury Venus Mars single/combined with "
        "Jupiter Saturn and luminaries, positive "
        "vs malefic aspects, signs/houses/orbs, "
        "old social class/moral stereotypes, "
        "magic/divination claims, and trade "
        "counts. No actual modern occupational "
        "prediction validated, source only."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLVIII_profession_source_acceptance_note"] = (
    "B07b R9445–R9526 82 source only records, "
    "six original image groups PDF658–662 "
    "SHA/bytes, 26 extracted ZIP source tests. "
    "Separate three target questions, competing "
    "professional signifier tiers and "
    "unverified alternative Ptolemy source. "
    "Zero actual human vocation or "
    "runtime model promotions; Chinese 72 "
    "source notes independently indexed."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9526
assert i["read_numbered_chapters"] == list(range(1, 149))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original printed CXLVIII vocation/profession source documented\n\n"
    + review
    + "\nAfter authenticated GitHub publication **9,526 Lilly "
    + "+ 1,066 Ptolemy =10,592 historical source records**. "
    + "All 26 first-edition original photo/ZIP source checks "
    + "pass. No human vocation/fame/wealth predictions "
    + "or executable runtime source promotions validated.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 source through CXLVIII profession — 2026-10-18\n\n"
    "After verified source publication **10,592 documentary "
    "historical records** (9,526 Lilly +1,066 Ptolemy), "
    "source first-edition PDF660/894 (**73.8% physical "
    "scanned frame position only**, NOT full research/"
    "predictive validation). B07b adds 82 qualified "
    "historic source statements on vocation existence, "
    "type and fame/income, conditionally eligible "
    "Mars/Venus/Mercury, lunar aspect/MC fallbacks "
    "and distinct Ptolemy original-unverified method. "
    "Zero real human scores or runtime promotions. "
    "NEXT printed CXLIX experimental profession "
    "aphorisms from PDF660 onwards. Separate Chinese "
    "BaZi46/ ZiWei26 remain source-only.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07b.md").read_text()
)
CURRENT.write_text(
    "# Lilly CXLVIII Magistery profession source documented; CXLIX next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07b source R9445–R9526 locally complete, "
    "pending remote publication. After verified "
    "readback, 9,526 Lilly +1,066 Ptolemy "
    "=10,592 archival source records, "
    "26 image and independent ZIP-replay tests pass. "
    "No human occupation ranking, moral/financial "
    "accuracy or promoted source runtime rules. "
    "Next printed CXLIX from PDF660; Chinese "
    "46 BaZi +26 Zi Wei still separately indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07b.md").read_text()
)
receipt = {
    "batch": "B07b",
    "status": "GUARDED_CXLVIII_HISTORICAL_PROFESSION_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B07b.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9526,
    "ptolemy_retained": 1066,
    "combined_if_published": 10592,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
