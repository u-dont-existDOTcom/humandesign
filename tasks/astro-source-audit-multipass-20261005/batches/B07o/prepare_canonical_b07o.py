#!/usr/bin/env python3
"""Guarded original Lilly CLVIII Ascendant-Saturn historical source append."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07o_ASC_SATURN.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07o.json"):
    assert not path.exists(), f"Duplicate/incomplete source index admission: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
guard = j(B / "CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
ch = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10657
assert i["read_numbered_chapters"] == list(range(1, 157))
assert i["batches"][-1]["id"] == "B07n"
assert i["next"]["chapter"] == "CLVIII"
assert i["next"]["printed_chapter_numeral"] == "CLVIII"
assert i["next"]["pdf_page"] == 690
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07o" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 75
assert [x["record_number"] for x in r["rules"]] == list(range(10658, 10733))
assert [x["id"] for x in r["rules"] if x["role"] == "next_navigation"] == ["R10731", "R10732"]
assert r["substantive"] == a["substantive"] == 73
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 10732
assert a["combined_if_published"] == 11798
assert w["body_original_pdf_frames"] == [690, 691]
assert w["following_printed_CLIX_heading_pdf"] == 691
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert not limits["source_directions_and_fixed_stars_computationally_verified"]
assert not limits["individual_mortality_or_clinical_claim_authorized"]
assert not guard["original_anareta_selection_verified"]
assert not guard["mathematical_aspects_or_stellar_parity_verified"]
assert guard["real_human_medical_accuracy_validated"] == 0
assert guard["real_human_mortality_predictions_validated"] == 0
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json") == a["guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 25 and sha(z["archive_path"]) == z["archive_sha256"]
assert ch["sum_source_annotations"] == 72
assert ch["independently_validated_real_human_claims"] == ch["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for file, name in (
    (INDEX, "INDEX_BEFORE_B07o.json"),
    (CURRENT, "CURRENT_BEFORE_B07o.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07o.md"),
):
    (BACK / name).write_bytes(file.read_bytes())

i["batches"].append(
    {
        "id": "B07o",
        "path": "batches/B07o/RULES.json",
        "records_count": 75,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 William Lilly first edition printed "
            "CLVIII five HYLEGIACALL PLACES heading but actual "
            "source only Ascendant-to-Saturn direction body, "
            "sextile/trine, square/opposition/terms "
            "PDF690/printed656 through PDF691/printed657 "
            "above next distinct printed CLIX Ascendant-to-Jupiter. "
            "Six original photo reversible source groups, "
            "73 substantive historical clauses and two CLIX "
            "navigation R10658-R10732. Antiquarian humoral/"
            "psychological/age/sex diagnoses from Saturn body, "
            "water danger only with watery sign and violent stars; "
            "Saturn sextile/trine contrary favorable "
            "rural/reputation/property/legacy/family types, "
            "large social-class-dependent alternative lists. "
            "Adverse square/opposition/terms claim old disease, "
            "reputation loss and pejorative morals; "
            "high-stakes death language requires EXTRA "
            "malevolent Promittor concurrence OR Saturn Anareta. "
            "All old illness/criminality/clinical safety "
            "claims quarantined with no human validity "
            "and ZERO runtime scoring rule promotion."
        ),
    }
)
i["records_count"] = 10732
i["read_numbered_chapters"].append(157)
i["status"] = "BOOK_III_CLVIII_ASC_SATURN_NEXT_CLIX_ASC_JUPITER_DIRECTIONS"
i["next"] = {
    "pdf_page": 691,
    "printed_page": 657,
    "chapter": "CLIX",
    "printed_chapter_numeral": "CLIX",
    "heading": "The Ascendant directed to the Body of Jupiter, and his Aspects",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original separately printed CLIX begins after "
        "a horizontal divider in lower original PDF691/"
        "printed657, following short CLVIII Ascendant-"
        "to-Saturn source. CLIX continues through "
        "original PDF692–701 and ends before printed "
        "CHAP CLX `Directions of the Mid-heaven to "
        "PROMITTORS` begins in original PDF702/"
        "printed668, as visually checked with "
        "first-edition source photos. Inspect "
        "all intervening original source content "
        "for every separate hylegiacal and aspect "
        "subheading before complete extraction."
    ),
    "research_scope": (
        "Multiple old Ascendant directed to Jupiter "
        "and other planets/aspects/terms, event types "
        "ranging from social fortune to periods of "
        "health/marriage/travel/property and adverse "
        "human conditions. Several dozen compound "
        "source alternatives require precise "
        "original glyph/angle/ephemeris review; "
        "no actual person outcomes or medical "
        "forecasts authorized."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLVIII_original_source_acceptance_note"] = (
    "B07o original R10658–R10732, "
    "75 historic source notes, six "
    "reversible original photo groups "
    "PDF690–692 SHA/bytes and 25 "
    "portable ZIP test replays. "
    "CLVIII is a SHORT Saturn-specific "
    "chapter despite five-place general "
    "heading. Ancient diseases/moralities "
    "not real clinical predictions; "
    "source mortality claims additionally "
    "require adverse Promittor agreement "
    "or Saturn Anareta. No real people "
    "or runtime models; Chinese 72 source "
    "notes independent."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10732
assert i["read_numbered_chapters"] == list(range(1, 158))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original printed CLVIII Ascendant-to-Saturn historically documented\n\n"
    + review
    + "\nAfter GitHub verified publication "
    + "10,732 Lilly +1,066 Ptolemy =11,798 "
    + "first-edition historical source notes, "
    + "25 photo/ZIP source checks pass. "
    + "Zero independent actual person illness, "
    + "mortality/social accuracy or production "
    + "runtime source promotions.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 through printed CLVIII Saturn directions — 2026-10-18\n\n"
    "After verified source publication **11,798 "
    "historic documentary annotations** "
    "(10,732 Lilly +1,066 Ptolemy), "
    "physical first-edition scan frontier "
    "PDF691/894 (~77.3% physical page "
    "position ONLY, not full empirical project "
    "completion). B07o adds 75 history-only "
    "Ascendant-to-Saturn old body/sextile/"
    "trine/square/opposition/terms rules with "
    "high-stakes requirements and source "
    "exceptions. NO human illness, safety, "
    "life-event or moral forecasts validated "
    "and NO executable runtime rule promotions. "
    "NEXT printed CLIX Ascendant-to-Jupiter "
    "and multiple other aspects, original "
    "PDF691–702, then printed CLX from PDF702. "
    "Chinese original BaZi46/ ZiWei26 "
    "historical notes indexed independently.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07o.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CLVIII Ascendant to Saturn source complete; CLIX next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07o historic R10658–R10732 "
    "locally accepted and pending "
    "GitHub remote publication. "
    "After verified remote 10,732 Lilly "
    "+1,066 Ptolemy=11,798 archival "
    "source-only notes, 25 source/ZIP "
    "integrity tests PASS. No real human "
    "medical/religion/moral or death "
    "predictions and no runtime model "
    "promotions. NEXT long CLIX "
    "Ascendant-directed planets/aspects "
    "PDF691 onward, printed CLX at PDF702. "
    "Chinese 72 separate source-only notes.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07o.md").read_text()
)
receipt = {
    "batch": "B07o",
    "status": "GUARDED_ORIGINAL_CLVIII_ASC_SATURN_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07o.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "nonpromotion_guard_sha256": sha(B / "CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10732,
    "ptolemy_retained": 1066,
    "combined_if_published": 11798,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
