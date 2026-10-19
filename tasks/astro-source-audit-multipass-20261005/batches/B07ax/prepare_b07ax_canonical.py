#!/usr/bin/env python3
"""Guarded append-only historical-source Merchant Nativity chapter admission.

The source text and one-reader physical 1647/1659 photos are documentary
evidence, not independently blinded actual-human predictions or astronomical
epoch chart validation. Preserve Mercury 20 arcminute original print error.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ax_MERCHANT.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07ax-merchant-nativity-opening-20261019"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    result = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    directory = (
        Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    )
    if (
        directory is not None
        and directory.is_dir()
        and directory.resolve() != Path.home().resolve()
    ):
        return directory
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07ax.json"):
    assert not f.exists(), f"Potential interrupted earlier index admission: {f}"
assert git("branch", "--show-current") == BRANCH
old = j(INDEX)
chinese = j(CHINA)
photos = j(B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json")
antiscion = j(B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json")
candidate = j(B / "MERCHANT_NATIVITY_SOURCE_CANDIDATES_V1.json")
rules = j(B / "RULES.json")
notes = j(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert old["records_count"] == accept["prior_Lilly"] == 12870
assert old["batches"][-1]["id"] == "B07aw"
assert old["read_numbered_chapters"] == list(range(1, 175))
assert old["read_headed_units_count"] == 90
assert not old["partial_numbered_chapters"]
assert old["next"]["chapter"] == "CLXXV" and old["next"]["pdf_page"] == 776
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == photos["original_1647_Wellcome_full_scan_sha256"]
assert old["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["independently_validated_real_human_claims"] == 0
assert chinese["runtime_promotions"] == 0
assert candidate["entry_count"] == notes["new_source_only_documentary_records"] == 30
assert len(rules["rules"]) == rules["record_count"] == 30
assert [r["record_number"] for r in rules["rules"]] == list(range(12871, 12901))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert notes["source_human_outcomes_validated"] == notes["runtime_astrology_promotions"] == 0
assert antiscion["original_minus_formula_arcminutes"] == -20
assert antiscion["all_other_6_antiscions_arithmetically_match"]
assert antiscion["actual_person_outcomes_predicted_and_verified"] == 0
assert accept["Lilly_after_if_admitted"] == 12900
assert accept["Western_after_if_admitted"] == 13966
assert accept["next_historical_R"] == "R12901"
assert accept["next_original_PDF_frame"] == 779
assert accept["next_original_printed_folio"] == 745
assert accept["next_original_physically_distinct_chapter"] == "CLXXVI"
assert accept["source_printed_Mercury_antiscion_26_06_vs_arithmetic_26_26"]
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["source_notes_SHA256"] == sha(
    B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json"
)
assert accept["photo_witness_SHA256"] == sha(
    B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json"
)
assert accept["source_antiscion_critical_diagnostic_SHA256"] == sha(
    B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"
)
assert release["CRC_passed"] and release["member_SHA256_and_exact_bytes_passed"]
assert release["independent_ZIP_extraction_test_replay_passed"]
assert release["source_tests_replayed"] == 47
assert release["source_notes_SHA256"] == accept["source_notes_SHA256"]
assert release["rules_SHA256"] == accept["rules_SHA256"]
assert (
    release["mercury_diagnostic_SHA256"] == (accept["source_antiscion_critical_diagnostic_SHA256"])
)
assert release["old_Lilly_index_SHA256"] == sha(INDEX)
assert release["Chinese_V7_index_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
assert len(photos["original_source_photographic_witnesses"]) == 10

for file in (
    INDEX,
    CHINA,
    TASK / "batches/B07aw/RULES.json",
    TASK / "batches/B07ax/ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json",
    TASK / "batches/B07ax/MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json",
):
    relative = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + relative) == git("hash-object", str(file)), relative

BACK.mkdir(exist_ok=False)
for path, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07ax.json"),
    (CURRENT, "CURRENT_BEFORE_B07ax.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07ax.json"),
):
    (BACK / name).write_bytes(path.read_bytes())

old["batches"].append(
    {
        "id": "B07ax",
        "path": "batches/B07ax/RULES.json",
        "records_count": 30,
        "sha256": accept["rules_SHA256"],
        "scope": (
            "Original 1647 source first printed CLXXV English Merchant Nativity "
            "chapter on folios742-745 PDF776-779 with 1659 physically "
            "independently typeset source photo comparator. 30 historical "
            "source annotations R12871–R12900: source chart, birth-time text, "
            "temperament 7hot/6moist/6cold/7dry and Lilly's own admission "
            "of knowing the merchant, historic planetary dignity sums and "
            "Mercury antiscion printed Pisces26°06 (analytic Pisces26°26) "
            "20-arcminute original printing discrepancy preserved; six other "
            "antiscions arithmetically match. Next printed CLXXVI Manners "
            "starts on same original folio745. Known-person descriptive "
            "historical example is NOT prospective human forecast accuracy; "
            "true calendar/ephemeris and independent critical edition unverified."
        ),
    }
)
old["records_count"] = 12900
old["status"] = (
    "BOOK_III_ORIGINAL_CLXXV_MERCHANT_NATIVITY_DOCUMENTARY_SOURCE_COVERED_NEXT_MANNERS_CLXXVI"
)
old["read_numbered_chapters"] = old["read_numbered_chapters"] + [175]
old["read_headed_units_count"] = 91
old["next"] = {
    "pdf_page": 779,
    "printed_page": 745,
    "chapter": "CLXXVI",
    "printed_chapter_numeral": "CLXXVI",
    "editorial_source_sequence_ordinal": 176,
    "heading": "Of the Manners of the Native.",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647 first physical CHAP CLXXVI starts below original "
        "Merchant Natality fortitudes scores on printed folio745/PDF779. "
        "Next historical R12901. B07ax source correctly preserved original "
        "printed Mercury antiscion Pisces26°06 versus mathematical "
        "solstitial reflection Pisces26°26 and did not convert a familiar "
        "retrospective merchant into a blinded human forecast."
    ),
    "research_scope": (
        "Original 1647 manners of native source following historical "
        "merchant case, two editions, explicit age/place/planet conditions, "
        "and no real-person outcome or actual astronomical chart validation."
    ),
}
old["chapter_CLXXV_source_coverage_not_expert_critical_complete"] = (
    "B07ax source-only 30 annotations from original Merchant Nativity "
    "chapter p742–745; original natal ephemeris, 1616 time/calendar and "
    "merchant biography unverified. Lilly says native was already known. "
    "Both 1647 and 1659 preserve Mercury solstitial antiscion 26°06′ Pisces "
    "vs calculated 26°26′, cause unknown. Original 1647 and 1659 one reader; "
    "not independent human predictive evidence."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07ax_MERCHANT.md"
assert old["records_count"] == sum(b["records_count"] for b in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 176))
assert not old["partial_numbered_chapters"]
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly CLXXV Merchant Nativity historical source accepted (B07ax)\n\n"
    "**30 historical documentary annotations R12871–R12900** from actual "
    "first printed 1647 and separately typeset 1659 Merchant nativity folios "
    "742–745. Original known merchant birth-chart date text 19 September1616 "
    "2h24m39 P.M. at latitude53 requires independent calendar/ephemeris "
    "validation. Original hot7/moist6/cold6/dry7 temperament columns and "
    "eight planetary dignity sums preserved; Lilly expressly knew merchant. "
    "The printed Mercury antiscion **Pisces26°06′** in both editions conflicts "
    "with mathematical reflection **Pisces26°26′** by 20′; printed historical "
    "value is not silently rewritten. **Lilly 12,900 + Ptolemy 1,066 = "
    "13,966 Western historical source notes**; separate Chinese V7 "
    "**154 BaZi+201 Zi Wei=355** unchanged. Physically distinct next "
    "CHAP **CLXXVI Of the Manners of the Native** begins original printed "
    "745/PDF779, next **R12901**. No actual prospective human forecast "
    "success and no runtime model promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted documentary source checkpoint preserved\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07ax",
    "status": "MERCHANT_NATIVITY_HISTORICAL_SOURCE_PREPARED_REMOTE_PUBLICATION_PENDING",
    "Lilly_before": 12870,
    "Lilly_after": 12900,
    "Ptolemy_retained": 1066,
    "Western_after": 13966,
    "Chinese_V7_retained": 355,
    "new_original_source_records": 30,
    "original_date_and_ephemeris_mathematics_validated": False,
    "Mercury_26_06_print_vs_26_26_arithmetic_retained": True,
    "next_R": "R12901",
    "next_original_pdf_frame": 779,
    "next_original_printed_folio": 745,
    "next_printed_chapter": "CLXXVI",
    "prior_Western_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07ax.json"),
    "new_Western_index_SHA256": sha(INDEX),
    "source_notes_SHA256": accept["source_notes_SHA256"],
    "source_edition_photo_witness_SHA256": accept["photo_witness_SHA256"],
    "source_antiscion_diagnostic_SHA256": (accept["source_antiscion_critical_diagnostic_SHA256"]),
    "rules_SHA256": accept["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "focused_portable_test_replays": 47,
    "Chinese_V7_SHA256": sha(CHINA),
    "independent_actual_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
