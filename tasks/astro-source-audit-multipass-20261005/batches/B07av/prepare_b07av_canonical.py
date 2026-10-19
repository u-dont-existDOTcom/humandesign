#!/usr/bin/env python3
"""Append-only Lilly CLXXIII historical source acceptance, not model validation.

Required: photo and original/second-edition variant witnesses, 106 tests from
independently extracted ZIP, exact hashes and no canonical prior mutations.
Only source chapter PHYSICAL COVERAGE is completed; original astrological
natal engine, expert critical text edition and human forecasting remain OPEN.
"""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07av_RADIX_RETURNS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH = "research/astro-b07av-clxxiii-radix-returns-20261019"
PARENT_SHA = "77d1a3848ca4aa20e1d7e5492ce7e635eb69b578"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def downloads():
    result = subprocess.run(
        ["xdg-user-dir", "DOWNLOAD"],
        capture_output=True,
        text=True,
    )
    p = Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


for file in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07av.json"):
    assert not file.exists(), f"Preexisting/interrupted canonical batch: {file}"
assert git("branch", "--show-current") == BRANCH
assert git("rev-parse", "HEAD") == PARENT_SHA
before = j(INDEX)
chinese = j(CHINESE)
matrix = j(B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json")
source = j(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
release = j(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json")
roman = j(B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json")
photos = j(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json")
task = j(B / "TASK_SCOPE.json")

assert task["active_branch"] == BRANCH
assert task["outcome"] == "OPEN"
assert before["records_count"] == accept["Lilly_before"] == 12803
assert before["batches"][-1]["id"] == "B07au"
assert before["next"]["pdf_page"] == 772
assert before["next"]["chapter"] == "CLXXIII"
assert before["read_numbered_chapters"] == list(range(1, 173))
assert before["read_headed_units_count"] == 88
assert before["partial_numbered_chapters"] == []
assert before["empirical_validations"] == before["runtime_promotions"] == 0
assert chinese["sum_source_annotations"] == accept["Chinese_V7_retained"] == 355
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0
assert before["source_sha256"] == source["original_full_1647_source_pdf_sha256"]
assert before["ptolemy_registry"] == "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json"
assert accept["Ptolemy_retained"] == 1066
assert len(source["rows"]) == len(matrix["records"]) == len(rules["rules"]) == 42
assert [r["record_number"] for r in rules["rules"]] == list(range(12804, 12846))
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert all(not r["independent_real_event_prediction_validated"] for r in rules["rules"])
assert rules["physical_CLXXIII_text_covered"]
assert not source["complete_expert_critical_edition_collation"]
assert rules["independently_blinded_human_predicted_results"] == rules["runtime_promotions"] == 0
assert source["source_clause_matrix_sha256"] == sha(
    B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json"
)
assert source["original_photo_checkpoint_sha256"] == sha(
    B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json"
)
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["source_full_doc_sha256"] == sha(
    B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json"
)
assert accept["source_photographic_manifest_sha256"] == sha(
    B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json"
)
assert accept["Lilly_if_admitted"] == 12845
assert accept["Western_historical_if_admitted"] == 13911
assert accept["next_R"] == "R12846"
assert accept["next_original_pdf_frame"] == 775
assert accept["next_original_printed_folio"] == 741
assert accept["next_1647_literal_chapter_numeral"] == "CLXXIIII"
assert accept["next_1659_literal_chapter_numeral"] == "CLXXIV"
assert accept["next_editorial_source_chapter_ordinal"] == 174
assert roman["source_original_first_1647_literal_printed_heading"] == "CHAP. CLXXIIII."
assert roman["source_second_1659_literal_printed_heading"] == "CHAP. CLXXIV."
assert len(photos["photo_witnesses"]) == 8
assert release["CRC_passed"] and release["member_SHA256_bytes_verified"]
assert release["independent_extracted_archive_tests_passed"]
assert release["preflight_tests_replayed"] == 52
assert release["source_tests_replayed"] == 54
assert release["archive_test_replays_total"] == 106
assert release["previous_Western_index_sha256"] == sha(INDEX)
assert release["Chinese_V7_sha256"] == sha(CHINESE)
assert release["rules_sha256"] == accept["rules_sha256"]
assert release["source_witness_sha256"] == accept["source_full_doc_sha256"]
assert (
    release["original_source_photo_manifest_sha256"]
    == accept["source_photographic_manifest_sha256"]
)
assert sha(downloads() / release["filename"]) == release["archive_sha256"]

for file in (
    INDEX,
    CHINESE,
    ROOT / TASK / "batches/B07au/RULES.json",
    ROOT / TASK / "batches/B07au/ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json",
    B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json",
    B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json",
    B / "RULES.json",
):
    rel = str(file.relative_to(ROOT))
    assert git("rev-parse", "HEAD:" + rel) == git("hash-object", str(file)), rel

BACK.mkdir(exist_ok=False)
for file, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07av.json"),
    (CURRENT, "CURRENT_BEFORE_B07av.md"),
    (CHINESE, "CHINESE_V7_BEFORE_B07av.json"),
):
    (BACK / name).write_bytes(file.read_bytes())

before["batches"].append(
    {
        "id": "B07av",
        "path": "batches/B07av/RULES.json",
        "records_count": 42,
        "sha256": accept["rules_sha256"],
        "scope": (
            "First edition 1647 Lilly original CLXXIII physical source "
            "planetary annual Revolution return to natal radix, original "
            "printed738–741/PDF772–775, versus separately typeset original "
            "1659 same folios/DjVu767–770. Exactly 42 historical source "
            "clauses R12804–R12845: six returning planets Saturn, Jupiter, "
            "Mars, Venus, Mercury, Moon each at seven natal planet positions, "
            "including conditional natal dignities, combustion and marriage "
            "preconditions. Aged medical, moral, criminal, sexual and social "
            "claims remain source rhetoric, not empirical predictions. "
            "The next distinct original 1647 transit chapter printed741 "
            "uses literal CLXXIIII, versus 1659 CLXXIV (editorial ordinal174); "
            "the original Roman edition discrepancy is preserved with photo "
            "cropped hashes. One unblinded reader; no expert critical edition, "
            "genuine natal ephemeris method or human outcomes validated."
        ),
    }
)
before["records_count"] = 12845
before["status"] = "BOOK_III_CLXXIII_PLANETARY_RADIX_RETURN_SOURCE_COVERED_NEXT_TRANSIT_CLXXIIII"
before.setdefault("completed_original_source_units_with_uncertainty", []).append(
    {
        "printed_chapter": "CLXXIII",
        "original_first_edition_book_year": 1647,
        "editorial_sequence_ordinal": 173,
        "chapter_heading": (
            "Of the Returne of the Planets to their owne Places, and "
            "to the places of other Planets in the RADIX."
        ),
        "source_original_printed_start_folio": 738,
        "source_original_printed_end_folio": 741,
        "source_original_PDF_begin": 772,
        "source_original_PDF_end": 775,
        "source_historical_record_start": "R12804",
        "source_historical_record_end": "R12845",
        "source_batch": "B07av",
        "physical_source_pages_covered": True,
        "complete": True,
        "independent_original_philological_expert_verified": False,
        "original_1647_natal_planetary_return_engine_verified": False,
        "independent_actual_human_prediction_validations": 0,
        "runtime_model_promoted": False,
    }
)
before["read_numbered_chapters"].append(173)
before["read_headed_units_count"] = 89
before["next"] = {
    "pdf_page": 775,
    "printed_page": 741,
    "chapter": "CLXXIIII",
    "printed_chapter_numeral": "CLXXIIII",
    "second_edition_1659_printed_chapter_numeral": "CLXXIV",
    "editorial_source_sequence_ordinal": 174,
    "heading": "Of the TRANSIT of the Planets.",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Begin below the physical divider after the Moon returning to "
        "its natal place on original 1647 printed741/PDF775. "
        "First edition next chapter literally CHAP. CLXXIIII; "
        "independently typeset second 1659 original prints CLXXIV. "
        "Both editions show Of the TRANSIT of the Planets. "
        "Next source record R12846. Continue original transits "
        "by body, houses and aspects with historical event-claim caution."
    ),
    "research_scope": (
        "Source-document how ephemeris transits touch natal house cusps, "
        "planetary positions and angular aspects, original 1647/1659 "
        "edition differences, and age/duration qualifiers. "
        "No modern medical, legal or personal astrology predictions."
    ),
}
before["CLXXIII_source_acceptance_scope_note"] = (
    "B07av original physical CLXXIII covered with 42 independently "
    "source-located, conditional ordered returning-planet to radix "
    "planet clauses from original two printings; one unblinded "
    "reader not independent text-critical proof. No actual-event "
    "prediction validated. New original next chapter prints "
    "CLXXIIII in 1647 and CLXXIV in 1659. Original first-edition "
    "literal chapter numeral preserved with distinct editorial174."
)
before["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261019_B07av_RADIX_RETURNS.md"
assert before["read_numbered_chapters"] == list(range(1, 174))
assert before["read_headed_units_count"] == 89
assert before["records_count"] == sum(r["records_count"] for r in before["batches"])
assert before["empirical_validations"] == before["runtime_promotions"] == 0
INDEX.write_text(json.dumps(before, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = (
    "# Original Lilly CLXXIII planet returns to natal Radix covered (B07av)\n\n"
    "**42 historical source-only annotations R12804–R12845** represent "
    "six annual-return planets×seven radix planet positions in original "
    "1647 printed738–741/PDF772–775 and separately typeset 1659 prints. "
    "Historical conditional clauses and moral/medical claims are "
    "documented, NOT real-human prediction evidence. First 1647 original "
    "next transit heading prints **CHAP. CLXXIIII.** while 1659 prints "
    "**CHAP. CLXXIV.**, editorial sequence ordinal174; preserve this "
    "literal edition difference. **12,845 Lilly +1,066 Ptolemy =13,911 "
    "Western historical notes**, Chinese V7 **154 BaZi +201 Zi Wei=355** "
    "unchanged. Next **R12846 original PDF775/printed741**, the new "
    "chapter *Of the TRANSIT of the Planets.* Actual natal astronomical "
    "engine, independent historical textual second-reader, and "
    "genuinely blinded human predictive validation remain OPEN. "
    "**Zero predictive validations, zero runtime promotions.**\n\n"
)
CURRENT.write_text(
    summary
    + "## Previous accepted historical checkpoint retained\n\n"
    + CURRENT.read_text(encoding="utf-8"),
    encoding="utf-8",
)
LATEST.write_text(
    summary + (B / "ORIGINAL_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8",
)
rec = {
    "batch": "B07av",
    "status": "CLXXIII_ORIGINAL_1647_1659_SOURCE_ACCEPTED_PREP_REMOTE_PENDING",
    "Lilly_before": 12803,
    "Lilly_after": 12845,
    "Ptolemy_retained": 1066,
    "Western_after": 13911,
    "Chinese_V7_retained": 355,
    "new_historical_documentary_notes": 42,
    "first_CLXXIII_physical_source_covered": True,
    "expert_diplomatic_critical_collation_completed": False,
    "original_1647_next_chapter_literal": "CLXXIIII",
    "separate_1659_next_chapter_literal": "CLXXIV",
    "next_R": "R12846",
    "next_original_PDF": 775,
    "old_Western_index_sha256": sha(BACK / "LILLY_INDEX_BEFORE_B07av.json"),
    "new_Western_index_sha256": sha(INDEX),
    "source_witness_sha256": accept["source_full_doc_sha256"],
    "source_matrix_sha256": accept["source_original_candidate_matrix_sha256"],
    "rules_sha256": accept["rules_sha256"],
    "portable_archive_sha256": release["archive_sha256"],
    "portable_test_replays": 106,
    "Chinese_V7_sha256": sha(CHINESE),
    "independent_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
RECEIPT.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rec, indent=2))
