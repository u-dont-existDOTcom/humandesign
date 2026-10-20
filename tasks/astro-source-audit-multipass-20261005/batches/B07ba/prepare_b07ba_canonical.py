#!/usr/bin/env python3
"""Guarded original CLXXVIII Brethren documentary, no real-person forecast claim."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07ba_BRETHREN.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH = "research/astro-b07ba-clxxviii-brethren-source-20261020"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()


def downloads():
    x = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(x.stdout.strip()) if x.returncode == 0 and x.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


for p in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ba.json"):
    assert not p.exists(), f"Prior/interrupted source acceptance: {p}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
chinese = j(CHINA)
source = j(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
scope = j(B / "TASK_SCOPE.json")
assert scope["required_branch"] == BRANCH and scope["root_outcome"] == "OPEN"
assert old["records_count"] == accept["prior_Lilly"] == 12969
assert old["batches"][-1]["id"] == "B07az"
assert old["next"]["pdf_page"] == 785 and old["next"]["chapter"] == "CLXXVIII"
assert old["read_numbered_chapters"] == list(range(1, 178))
assert old["read_headed_units_count"] == 93
assert not old["partial_numbered_chapters"]
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == source["full_original_1647_Wellcome_pdf_SHA256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert rules["record_count"] == source["record_count"] == 22
assert [r["record_number"] for r in rules["rules"]] == list(range(12970, 12992))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert source["source_strict_ptolemy_interpretation_predicts_few_siblings"]
assert source["source_author_reports_sibling_count_brothers"] == 7
assert source["source_author_reports_sibling_count_sisters"] == 1
assert source["reported_sibling_count_independent_validation_count"] == 0
assert source["source_explicitly_warns_exact_sibling_counts_difficult"]
assert accept["Lilly_after_if_accepted"] == 12991
assert accept["Western_after_if_accepted"] == 14057
assert accept["next_R"] == "R12992" and accept["next_original_pdf"] == 786
assert accept["next_original_physically_distinct_chapter"] == "CLXXIX"
assert accept["source_notes_sha256"] == sha(
    B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"
)
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert release["CRC_passed"] and release["member_SHA256_and_exact_bytes_passed"]
assert release["independent_archive_extraction_34_tests_passed"]
assert release["source_SHA256"] == accept["source_notes_sha256"]
assert release["rules_SHA256"] == accept["rules_sha256"]
assert release["old_Western_index_SHA256"] == sha(INDEX)
assert release["Chinese_V7_index_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_SHA256"]
for p in (
    INDEX,
    CHINA,
    T / "batches/B07az/RULES.json",
    T / "batches/B07az/ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json",
):
    rel = str(p.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(p)), rel

BACK.mkdir(exist_ok=False)
for p, n in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ba.json"),
    (CURRENT, "CURRENT_BEFORE_B07ba.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ba.json"),
):
    (BACK / n).write_bytes(p.read_bytes())
old["batches"].append(
    {
        "id": "B07ba",
        "path": "batches/B07ba/RULES.json",
        "records_count": 22,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Source-only original first 1647 CLXXVIII Of Brethren printed751–752 "
            "PDF785–786, compared with separate 1659 typeset same folios. "
            "22 historical annotations R12970–R12991. Author first says strict "
            "Ptolemaic third-house doctrine suggests few siblings, then reports "
            "seven brothers and one sister for a known merchant and provides "
            "flexible Jupiter/Mars/Mercury/Venus/Sun source explanation, "
            "explicitly conceding exact count is difficult. Reports and "
            "source conjectures about sibling mortality, relations, and uncle "
            "estate disputes are not independent human outcome evidence. "
            "Original CLXXVIII physically ends p752 before distinct CLXXIX "
            "Of Parents; old epoch natal engine and expert critical collation "
            "unverified, zero human predictive successes or runtime promotion."
        ),
    }
)
old["records_count"] = 12991
old["status"] = "ORIGINAL_LILLY_CLXXVIII_BRETHREN_PHYSICALLY_COVERED_NEXT_PARENTS"
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [178]
old["read_headed_units_count"] = 94
old.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXVIII",
        "editorial_ordinal": 178,
        "chapter_heading": "Of Brethren",
        "physical_source_start_pdf": 785,
        "accepted_through_pdf": 786,
        "printed_folios": [751, 752],
        "source_batch": "B07ba",
        "historical_start": "R12970",
        "historical_end": "R12991",
        "complete": True,
        "physical_source_span_covered": True,
        "independent_expert_source_critical_edition_complete": False,
        "author_known_sibling_count_brothers": 7,
        "author_known_sibling_count_sisters": 1,
        "independent_human_sibling_counts_verified": 0,
        "source_initial_strict_ptolemy_interpretation_few_versus_known_seven": True,
        "human_prospective_predictions_validated": 0,
        "runtime_model_promoted": False,
    }
)
old["next"] = {
    "pdf_page": 786,
    "printed_page": 752,
    "chapter": "CLXXIX",
    "printed_chapter_numeral": "CLXXIX",
    "editorial_source_sequence_ordinal": 179,
    "heading": "Of PARENTS",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original first 1647 printed p752/PDF786 below fourth-house "
        "divider starts distinct CLXXIX Of Parents. Next historic source "
        "R12992. Do not repeat preceding CLXXVIII unity passage."
    ),
    "research_scope": (
        "Source-only claims of parental appearance/condition, natal "
        "derived chart from child and Ptolemy method, historical case "
        "conditions, not verified human health/family prediction."
    ),
}
old["chapter_CLXXVIII_known_count_posthoc_source_warning"] = (
    "B07ba original 1647/1659 chapter states few siblings under a "
    "strict Ptolemaic indicator, then reports already known 7 brothers "
    "and 1 sister and reinterprets additional factors. The source "
    "itself warns it is difficult to judge exact number. Do not count "
    "reported siblings as independent validation, the later "
    "reconciliation as preregistered matching, or health/mortality/"
    "estate conjectures as proved individual events."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07ba_BRETHREN.md"
assert old["records_count"] == sum(x["records_count"] for x in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 179))
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = (
    "# Original Lilly CLXXVIII sibling-count evidence preserved (B07ba)\n\n"
    "**22 historical documentary source notes R12970–R12991** from "
    "1647 printed751–752 and separately typeset 1659 originals, "
    "cover the full CLXXVIII *Of Brethren*. Strict Ptolemy reasoning "
    "would imply few siblings, yet author already knew his merchant "
    "had **seven brothers and one sister** and adjusted the chart "
    "explanation accordingly; source also calls exact sibling number "
    "difficult. These reported counts are NOT independently verified "
    "or a blinded prediction. Claimed sickness, early mortality, "
    "family discord and uncle-estate disputes remain untested. "
    "**12,991 Lilly+1,066 Ptolemy=14,057 Western historical notes**, "
    "Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. Next "
    "**R12992**, original PDF786/printed752 **CLXXIX Of Parents** "
    "below physical divider. Zero prospective human validations, "
    "no runtime astrology rules promoted.\n\n"
)
CURRENT.write_text(
    summary + "## Earlier accepted source checkpoint\n\n" + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "RECOVERY_CHECKPOINT_20261020.md").read_text(encoding="utf-8"), encoding="utf-8"
)
receipt = {
    "batch": "B07ba",
    "status": "GUARDED_BRETHREN_SOURCE_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12969,
    "Lilly_after": 12991,
    "Ptolemy_retained": 1066,
    "Western_after": 14057,
    "Chinese_V7_retained": 355,
    "new_historical_source_notes": 22,
    "historical_author_reported_seven_brothers_one_sister": True,
    "historical_author_not_blinded": True,
    "independent_sibling_count_corrob": False,
    "next_R": "R12992",
    "next_original_pdf": 786,
    "next_chapter": "CLXXIX",
    "original_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ba.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "source_notes_sha256": accept["source_notes_sha256"],
    "rules_sha256": accept["rules_sha256"],
    "archive_sha256": release["archive_SHA256"],
    "portable_test_replays": 34,
    "Chinese_V7_SHA256": sha(CHINA),
    "independent_prospective_real_human_predictions": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
