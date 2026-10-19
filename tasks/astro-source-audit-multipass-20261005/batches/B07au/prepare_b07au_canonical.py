#!/usr/bin/env python3
"""Guarded append-only close of original Lilly CLXXII physical source chapter."""

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
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07au_CLXXII_END.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07au-clxxii-revolution-configurations-20261019"
PARENT = "398ac7345f150a73cde40228131795e849d23bb4"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for file in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07au.json"):
    assert not file.exists(), f"Possible prior/incomplete update {file}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT
old = j(INDEX)
china = j(CHINA)
source = j(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json")
rules = j(B / "RULES.json")
a = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
assert old["records_count"] == a["Lilly_before"] == 12788
assert old["batches"][-1]["id"] == "B07at"
assert sum(x["records_count"] for x in old["batches"]) == 12788
assert old["read_numbered_chapters"] == list(range(1, 172))
assert old["read_headed_units_count"] == 87
assert len(old["partial_numbered_chapters"]) == 1
assert old["partial_numbered_chapters"][0]["printed_chapter"] == "CLXXII"
assert old["partial_numbered_chapters"][0]["complete"] is False
assert old["next"]["pdf_page"] == 770 and old["next"]["chapter"] == "CLXXII"
assert old["empirical_validations"] == old["runtime_promotions"] == 0
assert old["source_sha256"] == source["original_full_first_edition_PDF_SHA256"]
assert china["sum_source_annotations"] == a["Chinese_V7_retained"] == 355
assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
assert len(source["records"]) == rules["record_count"] == 15
assert [r["record_number"] for r in rules["rules"]] == list(range(12789, 12804))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert source["source_CLXXII_physically_covered_through_original_pdf_771"]
assert source["separate_source_next_CLXXIII_heading_starts_pdf_772"]
assert not source["critical_source_edition_expert_collation_complete"]
assert source["independent_real_human_prediction_validations"] == source["runtime_promotions"] == 0
assert a["Lilly_if_accepted"] == 12803 and a["Western_if_accepted"] == 13869
assert a["next_original_R"] == "R12804"
assert a["next_original_pdf"] == 772 and a["next_chapter"] == "CLXXIII"
assert (
    sha(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json") == a["new_source_SHA256"]
)
assert sha(B / "RULES.json") == a["rules_SHA256"]
assert release["CRC_passed"] and release["all_members_SHA256_and_exact_bytes_passed"]
assert release["independent_archive_extraction_replayed_tests"] == 25
assert release["source_SHA256"] == a["new_source_SHA256"]
assert release["rules_SHA256"] == a["rules_SHA256"]
assert release["prior_Lilly_index_SHA256"] == sha(INDEX)
assert release["Chinese_V7_SHA256"] == sha(CHINA)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]
for file in (
    INDEX,
    CHINA,
    ROOT / TASK / "batches/B07at/RULES.json",
    ROOT / TASK / "batches/B07au/ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07au.json"),
    (CURRENT, "CURRENT_BEFORE_B07au.md"),
    (CHINA, "CHINESE_V7_BEFORE_B07au.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

old["batches"].append(
    {
        "id": "B07au",
        "path": "batches/B07au/RULES.json",
        "records_count": 15,
        "sha256": a["rules_SHA256"],
        "scope": (
            "Original first Lilly CLXXII source ending in 1647 printed736–737/"
            "PDF770–771, with distinct following CLXXIII chapter heading "
            "printed738/PDF772; 1659 separately typeset same folios preserved. "
            "Fifteen historical source-only notes R12789–R12803 on solar-return "
            "versus natal chart, annual ascendant and lord strength/combustion, "
            "Moon mitigation, natal 6th/12th/7th context, year-lord malefic "
            "contact and conditional cross-chart discord. Historic health, "
            "marriage, crime and money assertions NOT independently validated. "
            "1646 natal solar-return calculation/calendar/ephemeris parity "
            "and human actual-person prediction accuracy still unverified."
        ),
    }
)
old["records_count"] = 12803
old["status"] = "BOOK_III_CLXXII_SOLAR_REVOLUTION_PHYSICALLY_COVERED_NEXT_CLXXIII_PLANETARY_RETURNS"
part = old["partial_numbered_chapters"].pop()
assert part["accepted_through_pdf"] == 769 and part["next_record"] == "R12789"
part["accepted_through_pdf"] = 771
part["last_physical_boundary_source_pdf"] = 772
part["physical_source_span_covered"] = True
part["complete"] = True
part["closed_by_batch"] = "B07au"
part["source_full_original_expert_critical_edition_verified"] = False
part["solar_return_old_epoch_ephemeris_and_meridian_parity_verified"] = False
part["independent_real_person_predictions_validated"] = 0
part["runtime_model_promoted"] = False
old.setdefault("completed_original_source_units_with_uncertainty", []).append(part)
old["read_numbered_chapters"].append(172)
old["read_headed_units_count"] = 88
old["next"] = {
    "pdf_page": 772,
    "printed_page": 738,
    "chapter": "CLXXIII",
    "printed_chapter_numeral": "CLXXIII",
    "editorial_source_sequence_ordinal": 173,
    "heading": (
        "Of the Returne of the Planets to their owne Places, "
        "and to the places of other Planets in the Radix"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Next CLXXIII starts below an original physical heading at "
        "printed738/PDF772 after CLXXII closes at printed737/PDF771. "
        "Saturn section begins on same page and Jupiter section "
        "continues on original PDF773/printed739. Both original "
        "1647 and independent 1659 photos already saved in B07au "
        "source evidence but NO substantive Saturn/Jupiter rules "
        "were accepted as CLXXIII yet. Next historical R12804."
    ),
    "research_scope": (
        "Document historical planetary-return-to-radix positions by "
        "planet with natal-context conditions from actual first and "
        "separately typeset second original printed editions, without "
        "turning health, relationship, morality or death assertions "
        "into verified person-level facts."
    ),
}
old["physical_CLXXII_source_coverage_and_limits"] = (
    "B07at–B07au cover original first printed CLXXII folios734–737 "
    "and record CLXXIII next heading at printed738. First-and-second "
    "1647/1659 source photos preserved, but historical 1646 return "
    "astronomy/calendar and natal chart parity, expert critical "
    "edition and actual human predictions are NOT verified."
)
old["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07au_CLXXII_END.md"
assert old["records_count"] == sum(r["records_count"] for r in old["batches"])
assert old["read_numbered_chapters"] == list(range(1, 173))
assert old["partial_numbered_chapters"] == []
assert old["empirical_validations"] == old["runtime_promotions"] == 0
INDEX.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly CLXXII solar revolution chapter physically covered (B07au)\n\n"
    "**15 historical documentary notes R12789–R12803** on the 1647 "
    "CLXXII ending through printed737/PDF771, plus the distinct "
    "**CLXXIII planetary return** physical heading at "
    "printed738/PDF772. Annual-versus-natal ascendant/lord "
    "configurations, contextual Moon mitigation and old house/"
    "malefic claims are preserved as historical text only. "
    "**Lilly 12,803+Ptolemy1,066=13,869 Western historical notes**; "
    "Chinese V7 **154 BaZi+201 Zi Wei=355** unchanged. "
    "Original CLXXII physically covered but old-epoch solar "
    "return engine, expert edition accuracy and actual human "
    "predictions unverified. Next **R12804 CLXXIII** original "
    "PDF772/printed738 planetary returns. Zero actual-person "
    "predictive validations and zero runtime promotions.\n\n"
)
CURRENT.write_text(
    summary
    + "## Earlier accepted source checkpoint retained verbatim\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
receipt = {
    "batch": "B07au",
    "status": "GUARDED_ORIGINAL_CLXXII_END_SOURCE_INDEX_PREPARED_REMOTE_PENDING",
    "Lilly_before": 12788,
    "Lilly_after": 12803,
    "Ptolemy_retained": 1066,
    "Western_after": 13869,
    "Chinese_V7_retained": 355,
    "new_source_only_records": 15,
    "source_CLXXII_physical_coverage": True,
    "source_1646_natal_ephemeris_parity": False,
    "next_R": "R12804",
    "next_pdf": 772,
    "next_chapter": "CLXXIII",
    "prior_Lilly_index_SHA256": sha(BACK / "LILLY_INDEX_BEFORE_B07au.json"),
    "new_Lilly_index_SHA256": sha(INDEX),
    "source_doc_SHA256": a["new_source_SHA256"],
    "rules_SHA256": a["rules_SHA256"],
    "archive_SHA256": release["archive_sha256"],
    "portable_tests_replayed": 25,
    "Chinese_V7_SHA256": sha(CHINA),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2))
