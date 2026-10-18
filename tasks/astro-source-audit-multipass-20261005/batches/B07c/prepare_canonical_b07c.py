#!/usr/bin/env python3
"""Guarded append-only original Lilly CXLIX occupation source; friends next."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07c_PROFESSION_APHORISMS.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07c.json"):
    assert not p.exists(), f"Duplicate or partial original-source admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapping = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
validation = j(B / "PROFESSION_VALIDATION_REQUIREMENTS_V1.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9526
assert i["read_numbered_chapters"] == list(range(1, 149))
assert i["batches"][-1]["id"] == "B07b"
assert i["next"]["chapter"] == "CXLIX"
assert i["next"]["printed_chapter_numeral"] == "CXLIX"
assert i["next"]["pdf_page"] == 660
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(b["id"] == "B07c" for b in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 251
assert [x["record_number"] for x in r["rules"]] == list(range(9527, 9778))
assert [x["id"] for x in r["rules"] if x["role"].startswith("navigation_")] == [
    "R9775",
    "R9776",
    "R9777",
]
assert r["substantive"] == a["substantive"] == 248
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 9777 and a["combined_if_published"] == 10843
assert w["body_pdf_frames"] == list(range(660, 669))
assert w["following_unnumbered_eleventh_heading_frame"] == 668
assert w["following_numbered_CL_heading_frame"] == 670
assert len(mapping["source_groups"]) == mapping["source_group_count"] == 14
assert not limits["original_albubater_attribution_independently_collated"]
assert not limits["modern_occupation_mapping_and_baselines_defined"]
assert not limits["actual_person_crime_morality_religion_or_spiritual_inference_authorized"]
assert validation["explicit_nonpromotion"]
assert not validation["calibrated_probabilistic_model"]
assert validation["real_human_occupation_validation"] == 0
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "PROFESSION_VALIDATION_REQUIREMENTS_V1.json") == a["scope_guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 33 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
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
    (INDEX, "INDEX_BEFORE_B07c.json"),
    (CURRENT, "CURRENT_BEFORE_B07c.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07c.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07c",
        "path": "batches/B07c/RULES.json",
        "records_count": 251,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly 1647 Christian Astrology "
            "printed CHAP CXLIX 'Severall experimented Aphorismes' "
            "for Magistery, Trades and Profession from lower "
            "PDF660/printed626 through upper PDF668/printed634, "
            "ending BEFORE a separate substantive unnumbered "
            "eleventh-house Friendship source on SAME PDF668. "
            "Fourteen original reversible photo-source groups, "
            "248 substantive historical clauses, 3 next-source "
            "navigation R9527-R9777. Mercury alone/joined Saturn "
            "Mars Jupiter Sun Moon, Venus alone and combinations "
            "Saturn Jupiter Sun/cazimi, Mars alone strong/moderate/"
            "weak/night birth, Mars with Saturn Jupiter Sun Moon, "
            "Mercury+Venus/Mercury+Mars/Mars+Venus, success/fame "
            "vs profession-type source, zodiac movable/fixed "
            "EXCEPT Scorpio, humane/quad/water/earth, and elemental "
            "trade lists attributed to uncollated Albubater. "
            "Many mutually incompatible occupations and "
            "unverified period crime/morality/occult accusations "
            "explicitly not real person labels. Modern occupational "
            "mapping, original glyph parity and independent birth-"
            "verified human tests OPEN. Next unnumbered 11th-house "
            "friends PDF668-669, then printed CHAP CL PDF670. "
            "Zero actual human predictive validation and "
            "zero model runtime promotions."
        ),
    }
)
i["records_count"] = 9777
i["read_numbered_chapters"].append(149)
i["status"] = "BOOK_III_CXLIX_PROFESSION_APHORISMS_NEXT_UNNUMBERED_ELEVENTH"
i["next"] = {
    "pdf_page": 668,
    "printed_page": 634,
    "chapter": "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS",
    "printed_chapter_numeral": None,
    "heading": "Judgments appertaining unto the eleventh House. Of Friends, &c.",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "following_printed_chapter_numeral": "CL",
    "following_original_pdf_page": 670,
    "position": (
        "A substantive UNNUMBERED eleventh-house "
        "friendship introduction begins after divider "
        "mid/lower original PDF668/printed634, "
        "following the final trade sign aphorisms of "
        "CXLIX. Continues PDF669/printed635 "
        "including internal 'Speciall Rules concerning "
        "Friends'. Distinct numbered CHAP CL "
        "Quality of Friends begins original PDF670/"
        "printed636. Do NOT increment printed "
        "chapter count for the unnumbered intro."
    ),
    "research_scope": (
        "Historical judgments about friends by eleventh "
        "house occupants and aspects, first-house planets, "
        "lord eleventh and planetary strengths, benefic/"
        "malefic configurations, friendship count and "
        "loyalty/support, and special rules. Do not "
        "infer actual person's interpersonal trust, "
        "morality, criminality or relationships."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLIX_occupational_historical_acceptance_note"] = (
    "B07c historic R9527-R9777, 251 source annotations, "
    "14 reversible groups original PDF660-670 photos with "
    "source SHA/byte witnesses and 33 extracted archive "
    "integrity replays. Old occupational lists highly "
    "non-specific and sometimes criminally stigmatizing; "
    "separate primary work, income, skill, time use and "
    "fame targets before any blind test. "
    "Chinese 72 historical notes separate. "
    "Zero actual human accuracy and zero runtime promotions."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9777
assert i["read_numbered_chapters"] == list(range(1, 150))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly CXLIX historical occupation aphorisms documented\n\n"
    + review
    + "\nAfter GitHub remote verified publication "
    + "**9,777 Lilly + 1,066 Ptolemy = 10,843 historical "
    + "source annotations**, 33 source/photo/ZIP tests pass; "
    + "no real person jobs, professional income, morality or "
    + "alleged occult abilities validated, no runtime rules.\n"
)
PROGRESS.write_text(
    "# Lilly original 1647 through printed CXLIX profession aphorisms — 2026-10-18\n\n"
    "After verified source publication **10,843 "
    "documentary historical annotations** (9,777 Lilly "
    "+1,066 Ptolemy). First-edition scanned source "
    "frontier PDF668/894 (**74.7% physical scanned "
    "page position ONLY, not project completion**). "
    "B07c adds 251 historic source claims across 14 "
    "passages on Mars/Venus/Mercury, mixed signifiers, "
    "strength/malefic exceptions, dozens of old professional "
    "alternatives, source career success and elemental "
    "trade taxonomies attributed to unverified Albubater. "
    "No independently verified human profession accuracy "
    "and no promoted source rules. NEXT substantive "
    "UNNUMBERED eleventh-house friendship introduction "
    "PDF668–669, printed CL quality of friends begins "
    "PDF670. Chinese BaZi46, Zi Wei26 remain separate; "
    "full chart engines and blind human testing open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07c.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CXLIX old professional aphorisms documented; friends next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07c original source R9527–R9777 "
    "accepted locally and pending GitHub verification, "
    "after remote source acceptance 9,777 Lilly "
    "+1,066 Ptolemy =10,843 historical notes. "
    "33 first-edition images/source and portable "
    "ZIP replay checks pass, no independently "
    "verified real human occupation or runtime "
    "promotions. Next unnumbered eleventh-house "
    "friendship intro PDF668–669, then separately "
    "printed CHAP CL on PDF670. Chinese BaZi46/"
    "Zi Wei26 historic notes separately preserved.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07c.md").read_text()
)
receipt = {
    "batch": "B07c",
    "status": "GUARDED_ORIGINAL_CXLIX_PROFESSION_HISTORICAL_PENDING_REMOTE",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B07c.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "profession_validation_scope_sha256": sha(B / "PROFESSION_VALIDATION_REQUIREMENTS_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9777,
    "ptolemy_retained": 1066,
    "combined_if_published": 10843,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
