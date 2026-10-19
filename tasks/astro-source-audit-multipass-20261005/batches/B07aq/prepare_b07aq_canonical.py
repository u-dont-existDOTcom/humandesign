#!/usr/bin/env python3
"""Guarded original 1647/1659 CLXIX source-only history admission.

Documentary restoration of a missing secondary transcription paragraph is
not a prediction of actual friends, prosperity, health or human life events.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aq_11TH_HOUSE.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07aq-clxix-ascendant-moon-20261019"
PARENT = "74aa345d114278e0b678ed526fc23be609d32d07"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    p = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, RECOVERY / "LILLY_INDEX_BEFORE_B07aq.json"):
    assert not f.exists(), f"Earlier admission or interrupted state; reconcile: {f}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
old = j(INDEX)
chi = j(CHINA)
source = j(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json")
proof = j(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["root_owner_outcome"] == "OPEN"
assert old["records_count"] == accept["Lilly_before"] == 12704
assert old["batches"][-1]["id"] == "B07ap"
assert sum(v["records_count"] for v in old["batches"]) == 12704
assert old["next"]["chapter"] == "CLXIX" and old["next"]["pdf_page"] == 763
assert old["read_numbered_chapters"] == list(range(1, 169))
assert old["read_headed_units_count"] == 84
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert chi["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chi["independently_validated_real_human_claims"] == chi["runtime_promotions"] == 0
assert old["source_sha256"] == source["original_1647_full_pdf_SHA256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert source["new_documentary_source_notes"] == len(source["source_rows"]) == 21
assert rules["record_count"] == len(rules["rules"]) == 21
assert [r["record_number"] for r in rules["rules"]] == list(range(12705, 12726))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert sum(x["profection_house_number"] is not None for x in source["source_rows"]) == 12
assert source["source_original_1647_and_1659_both_contain_11th"]
assert source["secondary_modern_html_transcription_omits_house11"]
assert proof["original_first_and_second_printings_agree_eleventh_present"]
assert proof["modern_secondary_11th_omitted"]
assert not source["full_independent_expert_critical_edition_verified"]
assert source["actual_human_predictive_validations"] == source["runtime_promotions"] == 0
assert accept["Lilly_if_accepted"] == 12725
assert accept["Western_if_accepted"] == 13791
assert accept["next_R"] == "R12726" and accept["next_original_pdf_frame"] == 765
assert accept["next_chapter"] == "CLXX"
assert accept["source_notes_sha256"] == sha(
    B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json"
)
assert accept["source_witness_sha256"] == sha(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json")
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert release["CRC_passed"] and release["all_members_SHA256_and_exact_bytes_passed"]
assert release["independent_archive_test_replay_passed"]
assert release["source_tests_replayed"] == 35
assert release["source_notes_sha256"] == accept["source_notes_sha256"]
assert release["source_photo_witness_sha256"] == accept["source_witness_sha256"]
assert release["rules_sha256"] == accept["rules_sha256"]
assert release["prior_Western_index_SHA256"] == sha(INDEX)
assert release["prior_Chinese_V7_index_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07ap/RULES.json",
    ROOT / TASK / "batches/B07ap/evidence/1647_original-763.jpg",
):
    relative = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(f)), relative

RECOVERY.mkdir(exist_ok=False)
for p, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07aq.json"),
    (CURRENT, "CURRENT_BEFORE_B07aq.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07aq.json"),
):
    (RECOVERY / name).write_bytes(p.read_bytes())

old["batches"].append(
    {
        "id": "B07aq",
        "path": "batches/B07aq/RULES.json",
        "records_count": 21,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Original first 1647 CLXIX Ascendant/Moon profections physical "
            "printed729–730/PDF763–764, with new distinct CLXX p731/PDF765. "
            "21 source-only historical annotations R12705–R12725 cover all "
            "twelve source house descriptions, explicit age/Hyleg/radical "
            "and natal exception predicates, older Arabic translation caveat "
            "and annual year-lord context. Crucial original 11th-house "
            "friends/time-stewardship/prosperity paragraph PRESENT in BOTH "
            "original 1647 first and separately typeset 1659 second "
            "printings, OMITTED from modern searchable secondary HTML. "
            "Six original SHA-pinned photographs and derivative excerpt "
            "receipt preserved. Claims about health, death, finances or "
            "personal character are historical rhetoric only, not "
            "validated individual observations or engine rules."
        ),
    }
)
old["records_count"] = 12725
old["status"] = "BOOK_III_CLXIX_ALL_TWELVE_PROFECTION_HOUSES_SOURCE_COVERED_11TH_RESTORED"
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [169]
old["read_headed_units_count"] = 85
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXIX",
        "chapter_heading": "Of the Profections of the Ascendant and Moon in every House",
        "source_unit": "original physical CLXIX, first and second separately typeset editions",
        "physical_source_start_pdf": 763,
        "accepted_through_pdf": 765,
        "next_unaccepted_pdf": 765,
        "next_record": "R12726",
        "accepted_batch": "B07aq",
        "first_edition_source_physically_covered": True,
        "source_all_twelve_houses_present_in_original": True,
        "modern_derivative_missing_11th": True,
        "complete": True,
        "full_source_critical_edition_complete": False,
        "empirical_real_human_claims_validated": 0,
        "runtime_promoted": False,
    }
)
old["next"] = {
    "pdf_page": 765,
    "printed_page": 731,
    "chapter": "CLXX",
    "printed_chapter_numeral": "CLXX",
    "editorial_source_sequence_ordinal": 170,
    "heading": "Of the Profection of Mid-heaven and the Sunne, and their Significations",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Substantive next CHAP CLXX original printed731/PDF765 Mid-heaven "
        "and Sun house-by-house profection descriptions. The new heading "
        "was already source-indexed as B07aq last boundary note, "
        "do not duplicate it. Next historical record R12726."
    ),
    "research_scope": (
        "Original historical conditional Midheaven and Sun profection "
        "judgments for all houses, actual original 1647 vs 1659 "
        "edition distinctions and missing secondary-transcription "
        "provisions. No medical, money, criminality or real-person "
        "predictive accuracy is established."
    ),
}
old["CLXIX_source_transcription_11th_missing_repair_note"] = (
    "Both original independent 1647 and 1659 printings visibly include "
    "a complete 11th-house paragraph about friends, cheerfulness, "
    "well-used time and private fortune; the secondary HTML excerpt "
    "omits it between 10th and 12th. B07aq supplies SHA-pinned six "
    "source photographs and a single-reader cleaned source transcription. "
    "Historical text does not establish real-life predictive validity."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07aq_11TH_HOUSE.md"
assert sum(x["records_count"] for x in old["batches"]) == 12725
assert old["read_numbered_chapters"] == list(range(1, 170))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly 1647 CLXIX original eleven-house omission repaired (B07aq)\n\n"
    "**21 original historical source-only annotations R12705–R12725** "
    "document Ascendant/Moon profections through **all twelve houses**, "
    "printed729–730/PDF763–764 first 1647 edition and actual "
    "separately typeset 1659 second edition. The modern searchable "
    "secondary transcription SKIPS house **eleven**: both original "
    "books include a distinct paragraph on cheerfulness, friends, "
    "husbanding time and private fortune. Historic source text, "
    "not verified real-person predictive effects. Conditions on "
    "age, corroboration, Hyleg direction and natal house strength "
    "remain separately documented. **Lilly 12,725 + Ptolemy 1,066 "
    "=13,791 Western historical annotations**, independent Chinese "
    "V7 **154 BaZi +201 Zi Wei=355** unchanged. "
    "Next original **R12726** is new CLXX Sun/Midheaven "
    "profections printed731/PDF765; the title is already counted "
    "once as a physical source boundary. Empirical human validation "
    "zero, runtime promotions zero.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted historical checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07aq",
    "status": "GUARDED_ORIGINAL_CLXIX_MISSING_11TH_RESTORED_REMOTE_PENDING",
    "Lilly_before": 12704,
    "Lilly_after": 12725,
    "Ptolemy_retained": 1066,
    "Western_after": 13791,
    "Chinese_V7_retained": 355,
    "new_historical_source_only_annotations": 21,
    "source_original_all_twelve_houses": True,
    "source_1647_1659_11th_present_secondary_missing": True,
    "source_full_independent_critical_edition_complete": False,
    "next_R": "R12726",
    "next_original_pdf": 765,
    "next_chapter": "CLXX",
    "prior_Western_index_sha256": sha(RECOVERY / "LILLY_INDEX_BEFORE_B07aq.json"),
    "new_Western_index_sha256": sha(INDEX),
    "notes_sha256": accept["source_notes_sha256"],
    "proof_sha256": accept["source_witness_sha256"],
    "rules_sha256": accept["rules_sha256"],
    "archive_sha256": release["archive_sha256"],
    "portable_source_tests_replayed": 35,
    "Chinese_V7_index_sha256": sha(CHINA),
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
