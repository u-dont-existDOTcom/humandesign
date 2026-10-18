#!/usr/bin/env python3
"""Guarded canonical first-edition source admission: CLV historical captivity only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07j_CAPTIVITY.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07j.json"):
    assert not p.exists(), f"Duplicate or incomplete source append: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapping = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
ch = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10146
assert i["read_numbered_chapters"] == list(range(1, 154))
assert i["batches"][-1]["id"] == "B07i"
assert i["next"]["chapter"] == "CLV"
assert i["next"]["printed_chapter_numeral"] == "CLV"
assert i["next"]["pdf_page"] == 676
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07j" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 100
assert [x["record_number"] for x in r["rules"]] == list(range(10147, 10247))
assert [x["id"] for x in r["rules"] if x["role"] == "next_navigation"] == ["R10245", "R10246"]
assert r["substantive"] == a["substantive"] == 98
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 10246 and a["combined_if_published"] == 11312
assert w["body_pdf_frames"] == [676, 677]
assert w["following_printed_CLVI_heading_frame"] == 678
assert len(mapping["source_groups"]) == mapping["source_group_count"] == 8
assert not limits["fully_executable_captivity_risk_method"]
assert not limits["actual_person_criminality_captivity_medical_or_mortality_inference_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 24 and sha(z["archive_path"]) == z["archive_sha256"]
assert ch["sum_source_annotations"] == 72
assert ch["independently_validated_real_human_claims"] == ch["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B07j.json"),
    (CURRENT, "CURRENT_BEFORE_B07j.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07j.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07j",
        "path": "batches/B07j/RULES.json",
        "records_count": 100,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 first-edition printed CHAP CLV "
            "Of Captivity or Imprisonment from PDF676 lower/"
            "printed642 to PDF677 bottom/printed643, "
            "before separate printed CLVI Death "
            "whether Violent or Natural at TOP PDF678. "
            "Eight reversible first-edition photo groups, "
            "98 substantive historical conditions "
            "plus 2 next navigation R10147–R10246. "
            "Period hierarchy first Sun/Moon, second "
            "Saturn/Mars, third 7th/12th house occupants. "
            "Many alternative compound seventh/twelfth "
            "ruler, light malefic square/opposition/"
            "conjunction and retrograde/combustion "
            "conditions, angularity, source-sign lists, "
            "rare protective benefic reception/exceptions. "
            "Historic class-specific imprisonment by King "
            "or unfounded mortal danger claims. "
            "A separate final source discusses supposed "
            "LONG versus SHORT imprisonment from "
            "malefic twelfth and benefic aspects. "
            "No actual human legal arrest, imprisonment "
            "length, criminality or mortality validity, "
            "source glyphs not fully verified and zero "
            "executable runtime scoring promotion."
        ),
    }
)
i["records_count"] = 10246
i["read_numbered_chapters"].append(154)
i["status"] = "BOOK_III_CLV_IMPRISONMENT_SOURCE_NEXT_CLVI_DEATH"
i["next"] = {
    "pdf_page": 678,
    "printed_page": 644,
    "chapter": "CLVI",
    "printed_chapter_numeral": "CLVI",
    "heading": "Of Death, whether Violent or Natural",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Separate first edition printed CHAP CLVI "
        "begins at TOP PDF678/printed644, "
        "with internal headings 'Arguments of a "
        "Violent Death', 'The manner or kind of "
        "a violent death' and 'Of the quality of "
        "a violent Death'. It extends PDF679, "
        "PDF680 onward; inspect all pages through "
        "next true separately printed chapter "
        "before accepting. Do not merge with "
        "prior printed CLV custody."
    ),
    "research_scope": (
        "Historically asserted violent vs natural "
        "death, old zodiac star and house "
        "associations, purported manner/cause "
        "and class-related moralizing. All "
        "high-stakes mortality and criminality "
        "claims documentary only, not real-person "
        "diagnosis or forecasting."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLV_captivity_historical_acceptance_note"] = (
    "B07j original R10147–R10246, 100 source-only "
    "photographed annotations PDF676–679 with "
    "24 independent ZIP-extracted integrity "
    "test replays. Period confinement, "
    "royal punishment, legal risk and duration "
    "are unrelated high-stakes alternatives "
    "without any actual persons validated. "
    "Chinese 72 source notes remain separate, "
    "no model runtime promotion."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10246
assert i["read_numbered_chapters"] == list(range(1, 155))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly 1647 original printed CLV captivity source documented\n\n"
    + review
    + "\nFollowing GitHub verification 10,246 Lilly "
    + "+1,066 Ptolemy=11,312 historic documentation "
    + "records, 24 original source/archive checks; "
    + "zero human legal or safety validity and "
    + "no runtime model promotions.\n"
)
PROGRESS.write_text(
    "# Original Lilly first edition through CLV Captivity — 2026-10-18\n\n"
    "After authenticated source publication **11,312 "
    "historical documentary annotations** (10,246 Lilly "
    "+1,066 Ptolemy). First-edition physical scan "
    "frontier PDF678/894 (**75.8% scanned frame "
    "position ONLY; NOT scientific completion**). "
    "B07j adds 100 historical conditions with "
    "multiple and sometimes conflicting hypotheses "
    "about custody and length of imprisonment. "
    "No real person custody/criminal or medical "
    "forecast validated, zero model promotions. "
    "NEXT printed CLVI on violent/natural death "
    "from PDF678 onward. Chinese source BaZi46/"
    "ZiWei26 separate and not yet human-tested.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07j.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CLV prison/captivity source; CLVI death next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B07j R10147–R10246 "
    "locally accepted, GitHub remote readback pending. "
    "After remote verification 10,246 Lilly +1,066 "
    "Ptolemy=11,312 historical source annotations, "
    "24 source-photo/ZIP independent tests pass. "
    "No human captivity, judicial, illness or violent "
    "death predictions validated and zero promoted "
    "runtime rules. NEXT separate printed CLVI on "
    "death at PDF678. Chinese BaZi46/Zi Wei26 "
    "source-only historical records remain separate.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07j.md").read_text()
)
receipt = {
    "batch": "B07j",
    "status": "GUARDED_CLV_ORIGINAL_CAPTIVITY_SOURCE_PENDING_REMOTE",
    "prior_index_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07j.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10246,
    "ptolemy_retained": 1066,
    "combined_if_published": 11312,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
