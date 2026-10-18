#!/usr/bin/env python3
"""Guarded append of original Lilly CLIIII adversity outcomes source only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07i_ADVERSARY_OUTCOMES.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07i.json"):
    assert not p.exists(), f"Duplicate or partially applied admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapping = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
ch = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10082
assert i["read_numbered_chapters"] == list(range(1, 153))
assert i["batches"][-1]["id"] == "B07h"
assert i["next"]["chapter"] == "CLIIII"
assert i["next"]["printed_chapter_numeral"] == "CLIIII"
assert i["next"]["pdf_page"] == 675
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07i" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 64
assert [x["record_number"] for x in r["rules"]] == list(range(10083, 10147))
assert [x["id"] for x in r["rules"] if x["role"] == "next_navigation"] == ["R10145", "R10146"]
assert r["substantive"] == a["substantive"] == 62
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 10146
assert a["combined_if_published"] == 11212
assert w["body_pdf_frames"] == [675, 676]
assert w["following_printed_CLV_heading_frame"] == 676
assert len(mapping["source_groups"]) == mapping["source_group_count"] == 6
assert not limits["actual_person_risk_or_moral_inference_authorized"]
assert not limits["adversary_victory_decision_rule_executable"]
assert not limits["any_real_person_enemy_or_safety_prediction_validated"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not row["runtime_model_promoted"] for row in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 20 and sha(z["archive_path"]) == z["archive_sha256"]
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
for src, name in (
    (INDEX, "INDEX_BEFORE_B07i.json"),
    (CURRENT, "CURRENT_BEFORE_B07i.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07i.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07i",
        "path": "batches/B07i/RULES.json",
        "records_count": 64,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly Christian Astrology first edition 1647 "
            "printed CHAP CLIIII Whether the Native shall overcome "
            "or be overcome by Adversaries; original PDF675 mid "
            "through PDF676 upper printed641–642, before separately "
            "printed CLV Of Captivity or Imprisonment starts "
            "same PDF676. 6 source-photo reversible groups, "
            "62 substantive historic propositions and two "
            "following chapter navigation R10083–R10146. "
            "Seventh/tenth and twelfth/tenth ruler reciprocal "
            "positions, weak retrograde twelfth lord in sixth, "
            "day/night luminary in Mars dignities or house "
            "reception (not eighth), strongest Mars near chosen "
            "light, twelfth Saturn+Mars potent or weak with "
            "alleged enemies' death vs member debility, "
            "twelfth/sixth malefic split allegedly death, "
            "lifelong illness OR imprisonment, alternative "
            "benefic twelfth ruler source no-harm claims, "
            "Gemini/Sagittarius/Aquarius rising or malefic "
            "Leo/Sagittarius twelfth horse fall claims, "
            "and internal 'Whose Friendship Native must avoid' "
            "period injunction with two-chart adverse aspects. "
            "Extremely high-stakes and unvalidated historical "
            "rhetoric only; no real human adversary, medical, "
            "legal, accident or relationship safety forecasts "
            "and no production runtime rule promotions."
        ),
    }
)
i["records_count"] = 10146
i["read_numbered_chapters"].append(153)
i["status"] = "BOOK_III_CLIIII_ADVERSARY_OUTCOMES_NEXT_CLV_CAPTIVITY"
i["next"] = {
    "pdf_page": 676,
    "printed_page": 642,
    "chapter": "CLV",
    "printed_chapter_numeral": "CLV",
    "heading": "Of Captivity or Imprisonment",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CLV Of Captivity or Imprisonment "
        "starts after divider in middle/lower original "
        "PDF676/printed642 following CLIIII adversary "
        "victory/defeat cases. It continues original "
        "PDF677/printed643 and later; inspect actual "
        "next printed heading, full original numeric "
        "conditions and page seam before source acceptance."
    ),
    "research_scope": (
        "Period natal claims concerning confinement "
        "and captivity, seventh/twelfth planets, "
        "Saturn/Mars/light conditions and time duration. "
        "Distinguish actual incarceration, detention, "
        "legal outcome, time-to-release, alleged injuries "
        "and abstract restriction. ZERO validated human "
        "legal, health, injury, safety predictions."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLIIII_adversary_historical_acceptance_note"] = (
    "B07i historic R10083–R10146, 64 photo-anchored "
    "source-only records PDF675–677 SHA+bytes, 20 ZIP "
    "archive-extracted independent replay tests. "
    "Old contradictory threats include death, "
    "imprisonment, illness and horse fall, and "
    "friend avoidance rhetoric. Do not warn or "
    "diagnose any real person from natal source. "
    "Zero empirical validations/promotions, Chinese "
    "72 source-only records separate."
)
assert i["records_count"] == sum(row["records_count"] for row in i["batches"]) == 10146
assert i["read_numbered_chapters"] == list(range(1, 154))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original CLIIII adversary victory/defeat historical source\n\n"
    + review
    + "\nAfter verified publication 10,146 Lilly +1,066 Ptolemy "
    + "=11,212 documentary historic annotations, 20 original "
    + "photo/portable archive tests pass. No verified real "
    + "human violence, injury, mortality, relationship or "
    + "legal prognosis and no model runtime promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly first edition through CLIIII adversary cases — 2026-10-18\n\n"
    "After authenticated publication **11,212 historic source "
    "annotations** (10,146 Lilly +1,066 Ptolemy). "
    "First-edition physical source frontier PDF676/894 "
    "(**75.6% scanned physical page order ONLY, not "
    "predictive or mathematical study completion**). "
    "B07i adds 64 historical propositions on asserted "
    "overcoming of adversaries, and problematic unproven "
    "death/illness/prison/accident/relationship warnings. "
    "No actual person prediction validity or source "
    "runtime promotions. NEXT printed CLV captivity "
    "starts PDF676 after divider, continues PDF677 "
    "onward. Chinese BaZi46/ZiWei26 historical source "
    "records separately indexed.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07i.md").read_text()
)
CURRENT.write_text(
    "# Lilly CLIIII original adversary outcomes documented; captivity next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B07i source "
    "R10083–R10146 locally documented, remote "
    "publication pending. After verified remote "
    "source readback 10,146 Lilly +1,066 Ptolemy "
    "=11,212 historical annotations. All 20 "
    "image/independent ZIP archive tests pass. "
    "Zero actual human adversary/harm/medical/legal "
    "outcomes or promoted runtime rules. NEXT "
    "printed CLV captivity from PDF676. "
    "Chinese 46 BaZi +26 Zi Wei source-only "
    "annotations separate.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B07i.md").read_text()
)
receipt = {
    "batch": "B07i",
    "status": "GUARDED_CLIIII_ORIGINAL_HISTORIC_SOURCE_PENDING_REMOTE",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B07i.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10146,
    "ptolemy_retained": 1066,
    "combined_if_published": 11212,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
