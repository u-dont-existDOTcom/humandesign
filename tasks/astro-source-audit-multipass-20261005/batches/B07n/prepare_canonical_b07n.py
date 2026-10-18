#!/usr/bin/env python3
"""Guarded original Lilly printed CLVII direction strength source index append."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07n_DIRECTION_STRENGTH.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07n.json"):
    assert not p.exists(), f"Duplicate or incomplete source admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
guard = j(B / "DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10595
assert i["read_numbered_chapters"] == list(range(1, 156))
assert i["batches"][-1]["id"] == "B07m"
assert i["next"]["chapter"] == "CLVII"
assert i["next"]["printed_chapter_numeral"] == "CLVII"
assert i["next"]["pdf_page"] == 688
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(batch["id"] == "B07n" for batch in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 62
assert [x["record_number"] for x in r["rules"]] == list(range(10596, 10658))
assert [x["id"] for x in r["rules"] if x["role"] == "next_navigation"] == ["R10656", "R10657"]
assert r["substantive"] == a["substantive"] == 60
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 10657
assert a["combined_if_published"] == 11723
assert w["body_original_pdf_frames"] == [688, 689, 690]
assert w["next_printed_CLVIII_heading_frame"] == 690
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert not guard["numeric_effect_duration_rule_present"]
assert not guard["original_direction_and_annual_methods_mathematically_verified"]
assert not lim["numeric_event_duration_equation_present"]
assert not lim["source_high_stakes_person_level_predictions_authorized"]
assert guard["independent_human_impact_or_duration_tests"] == 0
assert guard["executable_runtime_rules_promoted"] == 0
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json") == a["guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 25 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
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
    (INDEX, "INDEX_BEFORE_B07n.json"),
    (CURRENT, "CURRENT_BEFORE_B07n.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07n.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07n",
        "path": "batches/B07n/RULES.json",
        "records_count": 62,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly first-edition printed "
            "CHAP CLVII How long Effects of Direction "
            "shall last, original PDF688/printed654 "
            "after divider, PDF689/printed655 and "
            "TOP PDF690/printed656 before printed CLVIII "
            "starts below separate divider PDF690. "
            "Six reversible original photograph groups, "
            "60 substantive historic conditions and "
            "two next-CLVIII navigation R10596–R10657. "
            "Dual natal Significator and Promittor "
            "strength/dignity and angularity, strong "
            "both full, one strong/other weak moderate "
            "but asymmetric causal interpretation, "
            "both weak small or NULL effects, "
            "malefic Promittor in own dignity "
            "supposed mitigation. Good and bad directions "
            "same year can both operate, conflicting "
            "health topic invokes additional annual "
            "profections/revolutions and final natal "
            "Promittor strength arbitration, illustrated "
            "by entirely UNVERIFIED fever/evaded illness. "
            "No independent numerical duration algorithm "
            "despite title, no mathematical direction/"
            "annual parity or human event outcomes; "
            "no executable runtime rule promotions."
        ),
    }
)
i["records_count"] = 10657
i["read_numbered_chapters"].append(156)
i["status"] = "BOOK_III_CLVII_DIRECTION_MAGNITUDE_NEXT_CLVIII_FIVE_HYLEGIACAL"
i["next"] = {
    "pdf_page": 690,
    "printed_page": 656,
    "chapter": "CLVIII",
    "printed_chapter_numeral": "CLVIII",
    "heading": (
        "The Effects of the five Hylegiacall Places, "
        "viz. the Ascendant, Mid-heaven, Sun, Moon and "
        "Part of Fortune directed to their Promittors"
    ),
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CLVIII starts after original "
        "CLVII last sentence and distinct divider "
        "at TOP original first-edition PDF690/"
        "printed656. Unlike the previous directions "
        "taxonomy of TEN directed objects, this "
        "header explicitly lists FIVE Hylegiacal "
        "places (Asc, MC, Sun, Moon, Part Fortune). "
        "It runs into following original scanned "
        "pages; inspect full next physical printed "
        "chapter boundary before declaring complete."
    ),
    "research_scope": (
        "Original ancient horoscopic aspect-specific "
        "claims for five named Hylegiacal places "
        "and their Promittors. May contain extensive "
        "period health, mortality, conduct, relationships "
        "and economic claims. Source-only; no person "
        "clinical or safety forecast, exact original "
        "longitude/orb/directions math required "
        "before any blind calculation."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLVII_strength_source_acceptance_note"] = (
    "B07n historical R10596–R10657, "
    "62 source-only clauses, six photo groups "
    "original PDF688–690 SHA/bytes and 25 "
    "standalone ZIP test replays. "
    "Strong/weak Significator vs Promittor "
    "conditions, completely weak no-effect "
    "and malefic dignity mitigation; contradictory "
    "good/bad directions sometimes coexist "
    "with annual profection/revolution arbitrary "
    "fallback. Title asks duration but no "
    "numeric time table source. "
    "No real human or medical validity "
    "and zero runtime promotions. "
    "Chinese 72 historical notes separate."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10657
assert i["read_numbered_chapters"] == list(range(1, 157))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly printed CLVII duration and strength historically documented\n\n"
    + review
    + "\nAfter verified GitHub publication "
    + "10,657 Lilly +1,066 Ptolemy=11,723 "
    + "historical source annotations. "
    + "25 photo/ZIP source tests pass, no "
    + "independent person event date, "
    + "magnitude, clinical or moral "
    + "accuracy or production runtime promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly through printed CLVII effect strength — 2026-10-18\n\n"
    "After verified publication **11,723 historical "
    "documentary source notes** (10,657 Lilly "
    "+1,066 Ptolemy), original PDF690/894 "
    "(~77.2% physical scan position only, "
    "NOT total science/model completion). "
    "B07n adds 62 original source statements "
    "on natal Significator/Promittor strength, "
    "relative effect and conflicting same-year "
    "directions. Original permits zero-effect "
    "under very weak indicators, and uses annual "
    "Profections/Revolutions to resolve health "
    "disagreements. No medical event, date "
    "or duration human validation and no "
    "runtime source promotion. NEXT printed "
    "CLVIII five Hylegiacall Places PDF690 "
    "onward. Chinese separate BaZi46 ZiWei26 "
    "historical-only intake.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07n.md").read_text()
)
CURRENT.write_text(
    "# Lilly CLVII directions effect strength source accepted; CLVIII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07n historical R10596–R10657 prepared "
    "for authenticated remote publication, "
    "after push 10,657 Lilly+1,066 Ptolemy "
    "=11,723 archival documentary notes. "
    "25 original-photo/standalone ZIP tests "
    "pass, no human predictive date, duration "
    "or actual clinical outcome validations "
    "and no runtime source rules promoted. "
    "NEXT printed CLVIII historical five "
    "Hylegiacal Places from PDF690 onward. "
    "Chinese source intake 72 separate.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B07n.md").read_text()
)
receipt = {
    "batch": "B07n",
    "status": "GUARDED_ORIGINAL_CLVII_DIRECTION_STRENGTH_PENDING_REMOTE",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B07n.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "source_duration_guard_sha256": sha(B / "DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10657,
    "ptolemy_retained": 1066,
    "combined_if_published": 11723,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
