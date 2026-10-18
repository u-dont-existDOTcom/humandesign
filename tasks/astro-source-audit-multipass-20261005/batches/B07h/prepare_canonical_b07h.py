#!/usr/bin/env python3
"""Guard append-only 1647 printed CLIII enemy-type source, no real-world danger claims."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07h_ENEMY_QUALITY.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07h.json"):
    assert not p.exists(), f"Duplicate or incomplete source acceptance: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
ch = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 10042
assert i["read_numbered_chapters"] == list(range(1, 152))
assert i["batches"][-1]["id"] == "B07g"
assert i["next"]["chapter"] == "CLIII"
assert i["next"]["printed_chapter_numeral"] == "CLIII"
assert i["next"]["pdf_page"] == 674
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07h" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 40
assert [x["record_number"] for x in r["rules"]] == list(range(10043, 10083))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == [
    "R10081",
    "R10082",
]
assert r["substantive"] == a["substantive"] == 38
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 10082 and a["combined_if_published"] == 11148
assert w["body_pdf_frames"] == [674, 675]
assert w["following_printed_CLIIII_heading_pdf"] == 675
assert len(m["source_groups"]) == m["source_group_count"] == 4
assert not limits["real_person_enmity_danger_inference_authorized"]
assert not limits["source_planet_fortitude_weights_and_glyphs_fully_verified"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 17 and sha(z["archive_path"]) == z["archive_sha256"]
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
    (INDEX, "INDEX_BEFORE_B07h.json"),
    (CURRENT, "CURRENT_BEFORE_B07h.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07h.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07h",
        "path": "batches/B07h/RULES.json",
        "records_count": 40,
        "sha256": a["rules_sha256"],
        "scope": (
            "Lilly Christian Astrology original 1647 first-edition "
            "printed CHAP CLIII on Enemies' Quality from original "
            "PDF674 middle to PDF675 upper (printed640–641), "
            "following unnumbered twelfth-house enemy COUNT source "
            "and before separately printed CLIIII on alleged "
            "winning or losing conflicts, same PDF675. "
            "Four reversible source-photo groups, 38 substantive "
            "qualified historical conditions and two next printed "
            "heading navigation R10043–R10082. "
            "Seventh occupants/luminary opposition supposedly "
            "open hostility, twelfth hidden hostility; eleventh "
            "lord seventh allows friends turning unfriendly via "
            "historical Directions, twelfth lord Ascendant "
            "contrary source friendly case. Enemy alleged social "
            "power supposedly determined from planet nature, "
            "house angularity/succedent/cadency and essential "
            "dignity, with counterintuitive BENefics denoting "
            "powerful enemies and malefics lower-class adversaries. "
            "No real individual's hidden intentions, crime, "
            "character, threat or adversary power inferred "
            "or validated; no runtime promotions."
        ),
    }
)
i["records_count"] = 10082
i["read_numbered_chapters"].append(152)
i["status"] = "BOOK_III_CLIII_ENEMIES_QUALITY_NEXT_CLIIII_ADVERSARY_OUTCOMES"
i["next"] = {
    "pdf_page": 675,
    "printed_page": 641,
    "chapter": "CLIIII",
    "printed_chapter_numeral": "CLIIII",
    "heading": "Whether the Native shall overcome, or be overcome by his Adversaries",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CLIIII starts after a separate "
        "divider mid PDF675/printed641, following "
        "CLIII on class/power of enemies. "
        "It continues upper PDF676/printed642, "
        "ending before printed CHAP CLV "
        "Of Captivity or Imprisonment beginning "
        "after another divider same PDF676. "
        "Inspect exact original glyphs and "
        "avoid real-world personal safety claims."
    ),
    "research_scope": (
        "Historical 7th/10th and 12th/10th lord "
        "reciprocal positions, Sun/Moon/Mars dignities, "
        "period claims of victory, injury, death, "
        "sickness or imprisonment; all high-stakes "
        "historic source only and not real-person "
        "medical or violent-risk forecasts."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLIII_enemies_quality_acceptance_note"] = (
    "B07h R10043–R10082, 40 photo-anchored source "
    "records original PDF674–677 SHA/bytes, "
    "17 extracted ZIP tests, open-versus-hidden "
    "enemy stereotypes and old benefic-powerful "
    "paradox preserved without human predictions. "
    "Chinese 72 source notes independent, "
    "runtime promotions zero."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10082
assert i["read_numbered_chapters"] == list(range(1, 153))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original 1647 Lilly CLIII enemy social quality documented\n\n"
    + review
    + "\nAfter remote publication 10,082 Lilly +1,066 "
    + "Ptolemy=11,148 historical source notes. 17 photo/"
    + "ZIP integrity tests pass; no validated personal "
    + "danger/character predictions or runtime rules.\n"
)
PROGRESS.write_text(
    "# Original Lilly 1647 through CLIII enemy quality — 2026-10-18\n\n"
    "After authenticated source publication **11,148 historical "
    "notes** (10,082 Lilly +1,066 Ptolemy), original "
    "first-edition scan frontier PDF675/894 "
    "(**75.5% physical page position only, NOT full "
    "research/scientific completion**). B07h adds "
    "40 historic open/covert enemy type and relative "
    "power/source-dignity claims, including "
    "original benefic-powerful exception. "
    "Zero verified real person hostility, safety "
    "or character predictions, no runtime promotion. "
    "NEXT printed CLIIII on whether native overcomes "
    "adversaries begins PDF675 then printed CLV "
    "captivity from PDF676. Chinese BaZi46/Zi Wei26 "
    "remain original-source only and separate.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07h.md").read_text()
)
CURRENT.write_text(
    "# Lilly first-edition CLIII enemies quality documented; CLIIII next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B07h source "
    "R10043–R10082 accepted locally pending remote "
    "verification. After verified GitHub publication "
    "10,082 Lilly +1,066 Ptolemy=11,148 "
    "historical notes; 17 source/ZIP replays PASS, "
    "no real person enemy assessment or runtime "
    "promotions. NEXT printed CLIIII on conflicts "
    "from PDF675; following printed CLV captivity "
    "starts PDF676. Chinese 72 source notes separate.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07h.md").read_text()
)
receipt = {
    "batch": "B07h",
    "status": "GUARDED_PRINTED_CLIII_ENEMY_QUALITY_PENDING_REMOTE",
    "previous_index_git_blob": blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07h.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10082,
    "ptolemy_retained": 1066,
    "combined_if_published": 11148,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
