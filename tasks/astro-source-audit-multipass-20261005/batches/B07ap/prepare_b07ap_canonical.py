#!/usr/bin/env python3
"""Guarded append-only documentary acceptance of original Lilly CLXVIII.

The physical span is covered, not expert diplomatically collated, and the
rhetorical health/morality/wealth claims are never personal predictions.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ap_CLXVIII_JUDGMENT.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ap-clxviii-judgment-20261019"
PARENT = "49b824d73d75537b2302e9facb6ddc9b5870e1e5"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for path in (LATEST, RECEIPT, RECOVERY / "LILLY_INDEX_BEFORE_B07ap.json"):
    assert not path.exists(), f"Existing/interrupted admission; reconcile {path}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
previous = j(INDEX)
chinese = j(CHINA)
notes = j(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
proof = j(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
task = j(B / "TASK_SCOPE.json")
assert task["required_branch"] == BRANCH and task["root_owner_outcome"] == "OPEN"
assert previous["records_count"] == accept["Lilly_before"] == 12671
assert previous["batches"][-1]["id"] == "B07ao"
assert sum(b["records_count"] for b in previous["batches"]) == 12671
assert previous["next"]["chapter"] == "CLXVIII"
assert previous["next"]["pdf_page"] == 760
assert previous["read_numbered_chapters"] == list(range(1, 168))
assert previous["read_headed_units_count"] == 83
assert previous["partial_numbered_chapters"] == []
assert previous["runtime_promotions"] == previous["empirical_validations"] == 0
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["runtime_promotions"] == chinese["independently_validated_real_human_claims"] == 0
assert previous["source_sha256"] == notes["original_full_Wellcome_1647_PDF_SHA256"]
assert previous["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert len(notes["rows"]) == rules["record_count"] == len(rules["rules"]) == 33
assert [r["record_number"] for r in rules["rules"]] == list(range(12672, 12705))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert notes["source_full_physical_span_1647_PDF"] == [760, 761, 762]
assert notes["source_next_CHAP_CLXIX_first_printed_PDF"] == 763
assert notes["source_chapter"] == "CLXVIII"
assert not notes["full_expert_diplomatic_comparison_completed"]
assert notes["human_predictions_validated"] == notes["runtime_promotions"] == 0
assert len(proof["full_image_sha_and_exact_bytes"]) == 8
assert accept["Lilly_if_accepted"] == 12704
assert accept["Western_if_accepted"] == 13770
assert accept["next_R"] == "R12705"
assert accept["next_source_PDF"] == 763
assert accept["next_source_printed_chapter"] == "CLXIX"
assert accept["original_CLXVIII_physical_coverage_completed"]
assert not accept["original_CLXVIII_philological_critical_edition_verified"]
assert sha(B / "RULES.json") == accept["rules_sha256"]
assert sha(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json") == accept["records_sha256"]
assert sha(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json") == accept["witness_sha256"]
assert release["CRC_passed"] and release["SHA_exact_bytes_passed"]
assert release["independent_archive_replay_passed"]
assert release["tests"] == 46
assert release["source_SHA256"] == accept["records_sha256"]
assert release["witness_SHA256"] == accept["witness_sha256"]
assert release["rules_SHA256"] == accept["rules_sha256"]
assert release["old_Western_SHA256"] == sha(INDEX)
assert release["old_Chinese_V7_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for f in (INDEX, CHINA, ROOT / T / "batches/B07ao/RULES.json"):
    rel = str(f.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(f)), rel

RECOVERY.mkdir(exist_ok=False)
for original, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ap.json"),
    (CURRENT, "CURRENT_BEFORE_B07ap.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ap.json"),
):
    (RECOVERY / name).write_bytes(original.read_bytes())

previous["batches"].append(
    {
        "id": "B07ap",
        "path": "batches/B07ap/RULES.json",
        "records_count": 33,
        "sha256": accept["rules_sha256"],
        "scope": (
            "Historical first-edition 1647 CHAP CLXVIII How to judge upon "
            "a Figure of Profections, printed726–728/PDF760–762 and "
            "physically separate next chapter CLXIX printed729/PDF763. "
            "Thirty-three bounded documentary source notes R12672–R12704 "
            "with eight first and independently typeset second 1659 edition "
            "page photographs and byte SHA witnesses. Natal vs annual "
            "year lord, radical houses, profectional dignities, two rulers "
            "and Pisces6°37 23°23 remainder example giving 284d16h28m "
            "to a June29 boundary. Old health, morality and wealth "
            "prognoses are historical rhetoric only, not verified. "
            "Source physical pages covered, NOT independently "
            "philologically or empirically validated natal astrology."
        ),
    }
)
previous["records_count"] = 12704
previous["status"] = "BOOK_III_CLXVIII_PROFECTION_JUDGMENT_PHYSICAL_SOURCE_SPAN_COVERED"
previous["read_numbered_chapters"] = previous["read_numbered_chapters"] + [168]
previous["read_headed_units_count"] = 84
previous.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXVIII",
        "chapter_heading": "How to judge upon a Figure of Profections",
        "source_unit": "original first edition distinct physical CLXVIII",
        "physical_source_start_pdf": 760,
        "accepted_through_pdf": 763,
        "end_before_new_chapter": "CLXIX",
        "next_unaccepted_pdf": 763,
        "next_record": "R12705",
        "accepted_batch": "B07ap",
        "first_edition_source_physically_covered": True,
        "complete": True,
        "full_source_critical_edition_complete": False,
        "empirical_real_human_claims_validated": 0,
        "runtime_promoted": False,
    }
)
previous["next"] = {
    "pdf_page": 763,
    "printed_page": 729,
    "chapter": "CLXIX",
    "printed_chapter_numeral": "CLXIX",
    "editorial_source_sequence_ordinal": 169,
    "heading": "Of the Profections of the Ascendant and Moon in every House",
    "include_opening_paragraph": False,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Begin substantive content below the new physical CHAP CLXIX "
        "heading on original printed729/PDF763. The title/physical "
        "separator are already documentary boundary notes in B07ap; "
        "do not double-count them as independent rules. Next source "
        "ID R12705. Source says Ascendant and Moon by twelve houses."
    ),
    "research_scope": (
        "Source-only original house-by-house Ascendant and Moon "
        "profections, contextual natal and annual predicates, "
        "conditional exceptions. Historical health, crime and "
        "morality assertions are not modern person-level predictions."
    ),
}
previous["source_CLXVIII_physical_coverage_not_empirical_verification_note"] = (
    "B07ap covers original 1647 physical CLXVIII printed726–728 "
    "with boundary to CLXIX printed729. Year ruler Jupiter/Mars "
    "example and natal/annual exceptions are documented only. "
    "No independently checked whole physical critical edition "
    "or real-human prognostic success, zero runtime promotions."
)
previous["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ap_CLXVIII_JUDGMENT.md"
assert previous["records_count"] == sum(b["records_count"] for b in previous["batches"])
assert previous["read_numbered_chapters"] == list(range(1, 169))
assert previous["empirical_validations"] == previous["runtime_promotions"] == 0
assert not previous["partial_numbered_chapters"]
INDEX.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly CLXVIII profection judgments physically covered (B07ap)\n\n"
    "**33 historical source-only annotations R12672–R12704** record "
    "Lilly's original 1647 printed726–728/PDF760–762 with "
    "separately typeset 1659 page witnesses. The source "
    "Pisces6°37 remainder 23°23 is converted by its table to "
    "284 days 16 hours 28 minutes, with Jupiter/Mars "
    "year-lord transition near June29. Context includes "
    "natal/annual house strength, profection rulers and exceptions; "
    "period health, character and monetary prognoses remain "
    "unverified rhetoric. **Lilly 12,704 + Ptolemy 1,066 "
    "=13,770 Western historical annotations**, independent "
    "Chinese V7 **154 BaZi +201 Zi Wei=355** unchanged. "
    "CLXVIII source span physically COVERED, not expert critical "
    "edition or evidence of human predictive accuracy. "
    "Next **R12705** is CLXIX substantive Ascendant/Moon "
    "profections below heading on original PDF763/printed729. "
    "No real-person validations and zero model promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier historical checkpoint preserved verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ap",
    "status": "GUARDED_CLXVIII_HISTORICAL_SOURCE_SPAN_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12671,
    "Lilly_after": 12704,
    "Ptolemy_retained": 1066,
    "Western_after": 13770,
    "Chinese_V7_retained": 355,
    "new_source_annotations": 33,
    "source_CLXVIII_physically_covered": True,
    "source_critical_edition_independent_review_complete": False,
    "next_R": "R12705",
    "next_PDF": 763,
    "next_chapter": "CLXIX",
    "prior_Western_SHA256": sha(RECOVERY / "LILLY_INDEX_BEFORE_B07ap.json"),
    "new_Western_SHA256": sha(INDEX),
    "source_SHA256": accept["records_sha256"],
    "witness_SHA256": accept["witness_sha256"],
    "rules_SHA256": accept["rules_sha256"],
    "release_archive_SHA256": release["archive_sha256"],
    "source_tests_replayed": 46,
    "Chinese_V7_SHA256": sha(CHINA),
    "real_human_prediction_validations": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
