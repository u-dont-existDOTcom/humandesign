#!/usr/bin/env python3
"""Guarded original Lilly Friends source append from exact accepted B07bg snapshot."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA_V7 = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261021_B07bh_FRIENDS.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"


def rd(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


for f in (LATEST, RECEIPT, BACK / "LILLY_INDEX_BEFORE_B07bh.json"):
    assert not f.exists(), f"Duplicate or unfinished prior admission: {f}"

i = rd(INDEX)
a = rd(B / "ACCEPTANCE.json")
s = rd(B / "SOURCE_FIRST_AUTHORING_20261021.json")
r = rd(B / "RULES.json")
w = rd(B / "ORIGINAL_SOURCE_WITNESS_20261021.json")
m = rd(B / "SOURCE_TO_RECORD_MAP.json")
limits = rd(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = rd(B / "SOURCE_RELEASE_RECEIPT_20261021.json")
chinese = rd(CHINA_V7)

assert i["source_id"] == "LILLY1647_WELLCOME_B30338724"
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["records_count"] == a["Lilly_before"] == 13236
assert i["read_numbered_chapters"] == list(range(1, 185))
assert i["read_headed_units_count"] == 100
assert i["batches"][-1]["id"] == "B07bg"
assert i["completed_original_source_units_with_uncertainty"][-1]["source_batch"] == "B07bg"
assert i["next"]["chapter"] == "CLXXXIII"
assert i["next"]["printed_chapter_numeral"] == "CLXXXIII"
assert i["next"]["editorial_source_sequence_ordinal"] == 185
assert i["next"]["pdf_page"] == 796
assert i["next"]["printed_page"] == 762
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(batch["id"] == "B07bh" for batch in i["batches"])

assert r["record_count"] == a["new_historical_source_only_annotations"] == 35
assert [x["record_number"] for x in r["rules"]] == list(range(13237, 13272))
assert a["Lilly_after_if_accepted"] == 13271
assert a["Western_after_if_accepted"] == 14337
assert a["numbered_editorial_chapters_increment"] == 1
assert r["editorial_ordinal"] == 185 and r["printed_chapter"] == "CLXXXIII"
assert s["known_merchant"]
assert not s["independent_real_merchant_friendship_or_business_records_obtained"]
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert len(w["photos"]) == a["source_photo_count"] == 5
assert w["two_printings_agree_on_printed_Friends_CLXXXIII"]
assert w["two_printings_agree_on_next_CLXXXIV"]
assert not limits["actual_merchant_friendship_or_trade_outcome_verified"]
assert all(not x["independent_human_blind_forecast_tested"] for x in r["rules"])
assert all(not x["runtime_astrological_rule_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"]
assert sha(B / "SOURCE_FIRST_AUTHORING_20261021.json") == a["source_first_sha256"]
assert sha(B / "ORIGINAL_SOURCE_WITNESS_20261021.json") == a["witness_sha256"]
assert z["zip_CRC_check_passed"]
assert z["all_members_exact_SHA_and_bytes_check_passed"]
assert z["independent_cold_source_tests_green"] == 18
assert sha(z["archive_path_on_owner_machine"]) == z["archive_sha256"]

prior_source = TASK / "batches/B07bg"
prior_receipt = rd(prior_source / "CANONICAL_PREPARE_RECEIPT_20261020.json")
assert sha(INDEX) == prior_receipt["new_index_sha256"]
assert sha(CHINA_V7) == prior_receipt["Chinese_V7_sha256"]
assert chinese["sum_source_annotations"] == 355
assert chinese["independently_validated_real_human_claims"] == 0
assert chinese["runtime_promotions"] == 0

relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative],
    cwd=ROOT,
    text=True,
).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
old_index_sha = sha(INDEX)

BACK.mkdir(exist_ok=True)
for previous, name in (
    (INDEX, "LILLY_INDEX_BEFORE_B07bh.json"),
    (CHINA_V7, "CHINESE_V7_BEFORE_B07bh.json"),
    (CURRENT, "CURRENT_BEFORE_B07bh.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07bh.md"),
):
    (BACK / name).write_bytes(previous.read_bytes())

i["batches"].append(
    {
        "id": "B07bh",
        "path": "batches/B07bh/RULES.json",
        "records_count": 35,
        "sha256": sha(B / "RULES.json"),
        "scope": (
            "Original Lilly 1647/1659 first and second edition, "
            "old known-merchant 11th-house Of Friends, "
            "original p762 lower through p763 upper, "
            "original Wellcome PDF796–797, "
            "literal printed CHAP CLXXXIII (repeated earlier "
            "Travels numeral and backwards after Honours CLXXXIIII), "
            "editorial ordinal185. Six source-photo groups, "
            "32 substantive old source clauses and three future "
            "navigation R13237–R13271, both original printings "
            "p762-763 SHA/bytes. Sagittarius bicorporeal 11th "
            "cusp, Moon opposite 11th and ruling 7th, historic "
            "Moon-type sailors and working-class exclusions, "
            "hypothesized adverse business partnership, "
            "Jupiter in Sagittarius Jovian and Venice/Venusian "
            "ambiguous positive contacts versus Mercury "
            "peregrine/combust, Mars trine 11th and Leo-"
            "qualified officials/medicine/mint/iron-tool "
            "professions. Social, legal, medical and economic "
            "class categories are historical stereotypes "
            "not real friendship or merchant outcomes. "
            "Next printed p763 CLXXXIV imprisonment then "
            "independent CLXXXV death; zero human predictive "
            "accuracy and zero runtime scoring promotions."
        ),
    }
)
i["records_count"] = 13271
i["read_numbered_chapters"].append(185)
i["read_headed_units_count"] += 1
i["completed_original_source_units_with_uncertainty"].append(
    {
        "printed_chapter": "CLXXXIII",
        "editorial_ordinal": 185,
        "heading": "Of Friends",
        "original_source_start_pdf": 796,
        "accepted_through_original_pdf": 797,
        "printed_folios": [762, 763],
        "source_batch": "B07bh",
        "historical_start": "R13237",
        "historical_end": "R13271",
        "physical_source_span_covered": True,
        "complete": True,
        "original_printings_two_edition_page_SHA_and_bytes_verified": True,
        "source_merchant_known_before_astrologer_wrote_example": True,
        "source_1647_1659_original_printed_numeral_CLXXXIII_duplicate": True,
        "expert_blinded_diplomatic_edition_all_astrological_glyphs_finished": False,
        "actual_known_merchant_friends_or_trade_profit_verified": False,
        "human_predictive_accuracy_validations": 0,
        "runtime_astrological_promotions": 0,
    }
)
i["status"] = "BOOK_III_MERCHANT_FRIENDS_SOURCE_ORDINAL185_NEXT_IMPRISONMENT"
i["next"] = {
    "pdf_page": 797,
    "printed_page": 763,
    "chapter": "CLXXXIV",
    "printed_chapter_numeral": "CLXXXIV",
    "editorial_source_sequence_ordinal": 186,
    "heading": "Of Imprisonment",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original 1647/1659 printed p763 (1647 PDF797) "
        "has an independent twelfth-house Judgement "
        "upon the twelfth house / CHAP CLXXXIV "
        "Of Imprisonment below divider after Friends, "
        "and then a separate eighth-house CHAP CLXXXV "
        "Of Death its quality farther down the SAME page. "
        "Do NOT import either into B07bh. The original "
        "imprisonment source is brief and ends before "
        "the later death-heading divider."
    ),
    "research_scope": (
        "Author's already-known merchant example for "
        "imprisonment/restraint of liberty; old Jupiter "
        "in 12th, lights and malefic-aspect exclusions, "
        "earlier page643 aphorisms and general fate exception. "
        "Historical source only, not legal or life-safety forecasts."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLXXXIII_duplicate_friends_known_merchant_note"] = (
    "B07bh 35 original source-only clauses R13237-R13271, "
    "both first1647 and second1659 photos p762–763 "
    "sha/byte audited, printed numeral CLXXXIII repeats "
    "earlier Travels and regresses after Honours CLXXXIIII. "
    "Known merchant; no historical partner outcome or "
    "real human success. Separate next CLXXXIV imprisonment "
    "and CLXXXV mortality on original p763. "
    "Independent later Chinese V14 796 source notes are "
    "not merged with older Western inherited Chinese V7."
)
assert i["records_count"] == sum(batch["records_count"] for batch in i["batches"]) == 13271
assert i["read_numbered_chapters"] == list(range(1, 186))
assert i["read_headed_units_count"] == 101
INDEX.write_text(json.dumps(i, indent=2, ensure_ascii=False) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261021.md").read_text()
LATEST.write_text(
    "# Original Lilly 1647 and 1659 merchant Friends — historical documentary evidence\n\n"
    + review
    + "\n**Accepted only after remote verification:** "
    + "13,271 Lilly + 1,066 Ptolemy =14,337 Western "
    + "original source annotations, 18 photo/ZIP source tests "
    + "pass, no actual verified merchant friendships or "
    + "real human predictions and zero runtime model promotions.\n"
)
PROGRESS.write_text(
    "# Parallel research reconciled; Lilly merchant Friends original source — 2026-10-21\n\n"
    "After authenticated remote publication **14,337 Western "
    "historical source annotations** (13,271 Lilly +1,066 "
    "Ptolemy) at original first-edition PDF797/894 "
    "(~89.2% PHYSICAL scan-page position ONLY, not "
    "completed research or predictive truth). B07bh "
    "35 historical source notes on a known merchant's "
    "supposed friends, Moon-partner risks, Jupiter/Venus "
    "and Mars source alternatives from both 1647/1659. "
    "Old literal friends CLXXXIII repeated after "
    "Honours CLXXXIIII; editorial ordinal185. "
    "No actual association, economic result, human "
    "behavioral prediction or runtime source promotion. "
    "Other accepted Chinese V14 source has 796 source "
    "records (BaZi210+ZiWei586) on an INDEPENDENT "
    "branch, not merged; existing independent computational "
    "and literature study branches also not merged. "
    "NEXT original p763 CHAP CLXXXIV Imprisonment, "
    "then CHAP CLXXXV Death.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07bh.md").read_text()
)
CURRENT.write_text(
    "# Lilly Friends merchant source documented after cross-chat reconciliation\n\n"
    "2026-10-21 Africa/Dakar UTC+0. B07bh "
    "source R13237–R13271 prepared for remote acceptance. "
    "After verified push 13,271 Lilly+1,066 Ptolemy "
    "=14,337 source annotations. First 1647 and "
    "second 1659 independent original photos agree "
    "on old numbered source seam p762–763; original "
    "printed CLXXXIII Friends is editorial185 and "
    "must not be normalized. 18 photo/ZIP extracted "
    "source tests, zero independent real-person "
    "friendship or commerce outcome accuracy "
    "and no scoring rule promotions. "
    "Chinese V14 796 historical notes remain in "
    "parallel accepted original source branch, "
    "not combined at file level. NEXT source printed "
    "CLXXXIV Imprisonment p763, then CLXXXV death.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07bh.md").read_text()
)
receipt = {
    "batch": "B07bh",
    "status": "GUARDED_1647_1659_MERCHANT_FRIENDS_SOURCE_PENDING_REMOTE_GITHUB",
    "prior_index_git_blob": old_blob,
    "old_index_sha256": old_index_sha,
    "new_index_sha256": sha(INDEX),
    "rules_sha256": sha(B / "RULES.json"),
    "source_first_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261021.json"),
    "witness_sha256": sha(B / "ORIGINAL_SOURCE_WITNESS_20261021.json"),
    "source_review_sha256": sha(B / "ORIGINAL_SOURCE_REVIEW_20261021.md"),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "portable_archive_sha256": z["archive_sha256"],
    "Chinese_V7_SHA256_unchanged": sha(CHINA_V7),
    "Chinese_V14_separate_accepted_source_notes": 796,
    "Lilly_before": 13236,
    "Lilly_after": 13271,
    "Ptolemy_retained": 1066,
    "Western_after": 14337,
    "numbered_editorial_chapters_increment": 1,
    "read_headed_units_increment": 1,
    "next_R": "R13272",
    "next_original_printed_folio": 763,
    "next_literal_printed_chapter": "CLXXXIV",
    "source_focused_cold_tests_passed": 18,
    "real_human_blind_predictive_validations": 0,
    "runtime_astrological_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
