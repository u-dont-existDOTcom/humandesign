#!/usr/bin/env python3
"""Guarded first-edition Lilly original source accession; preserve Chinese lane."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06l_WIFE_APPEARANCE.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06l.json"):
    assert not p.exists(), f"Previous/partial source admission: {p}"

idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
archive = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapping = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
chinese = j(CHINESE)

assert idx["records_count"] == a["prior_lilly"] == 8141
assert idx["read_numbered_chapters"] == list(range(1, 135))
assert idx["batches"][-1]["id"] == "B06k"
assert idx["next"]["chapter"] == "CXXXV"
assert idx["next"]["printed_chapter_numeral"] == "CXXXIIII"
assert idx["next"]["pdf_page"] == 627
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06l" for x in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 131
assert a["lilly_if_published"] == 8272
assert a["combined_if_published"] == 9338
assert [x["record_number"] for x in r["rules"]] == list(range(8142, 8273))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8271", "R8272"]
assert a["numbered_chapters_added"] == 1
assert r["substantive"] == a["substantive"] == 129
assert len(mapping["source_groups"]) == mapping["source_group_count"] == 14
assert w["original_body_pdf_frames"] == [627, 628, 629, 630, 631]
assert w["next_printed_CXXXV_heading_frame"] == 631
assert not limits["original_glyph_categories_fully_resolved"]
assert not limits["real_person_spouse_character_moral_or_disability_claim_authorized"]
assert not limits["person_health_or_mortality_forecasts_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_appearance_accuracy_validated"]
        or x["independent_human_spouse_personality_validated"]
        or x["independent_spouse_wealth_class_validated"]
        or x["independent_marital_medical_mortality_validated"]
        or x["real_person_moral_intimate_danger_label_authorized"]
        or x["original_ptolemy_attribution_independently_verified"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == archive["accepted_rules_sha256"]
assert archive["crc_passed"] and archive["sha256_passed"] and archive["extraction_passed"]
assert archive["replayed_tests"] == 28
assert sha(archive["archive_path"]) == archive["archive_sha256"]

# The Chinese astrology addition is source-only and separate; never
# integrate its annotation records into Lilly or the retained Ptolemy count.
assert chinese["sum_source_annotations"] == 72
assert [i["accepted_source_annotations"] for i in chinese["systems"]] == [46, 26]
assert chinese["independently_validated_real_human_claims"] == 0
assert chinese["runtime_promotions"] == 0

relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06l.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06l.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06l.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06l",
        "path": "batches/B06l/RULES.json",
        "records_count": 131,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original first-edition printed CHAP CXXXIIII/"
            "editorial CXXXV, appearance, Conditions of Wife, Aphorismes "
            "of Venus position, Riches attending Wife, Signs of good Wife "
            "and ill fortune by a Wife: original PDF627 lower through "
            "PDF631 upper/printed593-597. 14 source-photo passage groups "
            "including 129 substantive historical claims/conditionals and "
            "two next numbered chapter navigation, R8142-R8272. "
            "Zodiac aesthetic fair/medium/deformed classes including "
            "unresolved signs and part glyphs; Saturn/Venus age widow "
            "and benefic counterexamples; Saturn Jupiter Mars Venus "
            "Mercury supposed personality dependent on dignity; "
            "Venus position aphorisms concerning spouse finance, "
            "sexual behavior, childlessness, rank/old age and "
            "unsupported allegations of poisoning/magic; "
            "historic alleged spouse riches/house changes and "
            "author's critical class-relative beggar/tradesman "
            "counterexample, strong seventh malefics may still "
            "denote rich spouse with trouble; severe Saturn/Mars "
            "marriage grief/death hypotheses with benefic "
            "qualifier. All are seventeenth-century stereotypes "
            "not tested personal facts. Ptolemy attribution not collated; "
            "no human marriage/wealth/body/medical accuracy "
            "and no runtime source scoring promotion."
        ),
    }
)
idx["records_count"] = 8272
idx["read_numbered_chapters"].append(135)
idx["status"] = "BOOK_III_WIFE_APPEARANCE_CHARACTER_WEALTH_NEXT_MARITAL_CONCORD"
idx["next"] = {
    "pdf_page": 631,
    "printed_page": 597,
    "chapter": "CXXXVI",
    "printed_chapter_numeral": "CXXXV",
    "heading": "Of the mutuall Love and Concord betwixt Man and Wife",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "The next separately printed CHAP CXXXV begins below "
        "a horizontal divider on original PDF631/printed597, "
        "after source CXXXIIII's extensive marriage fortunes. "
        "It continues original PDF632/printed598 and later pages; "
        "inspect original pages and following printed seam before "
        "claiming any chapter's end."
    ),
    "research_scope": (
        "Marriage love and discord allegedly from spouse-signifier "
        "planets' aspects to Moon, benefic/malefic vs friendly/hostile "
        "conditions and comparing two independently calculated "
        "nativities, including Sun/Moon same-degree contact, "
        "sexual jealousy and instability stereotypes, supporting "
        "house/sign/period conditions. Source content not "
        "verified on real human partnerships; must not infer "
        "infidelity, danger, addiction or moral traits."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXV_source_acceptance_note"] = (
    "B06l original historical R8142-R8272, 131 notes, 14 "
    "groups, eight original PDF627–634 photographic "
    "SHA/bytes and 28 archive-extracted independent "
    "documentary checks. Wife status forecast must be "
    "relative to native class per Lilly's own beggar "
    "counterexample; moral, bodily, medical, death and "
    "magic accusations remain unsupported original text. "
    "Zero human predictive validity and runtime promotions. "
    "Chinese BaZi/ZWDS source lane 72 notes separate."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8272
assert idx["read_numbered_chapters"] == list(range(1, 136))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    (
        "# Lilly original first-edition wife appearance, condition, "
        "riches and ill fortune documented\n\n"
    )
    + review
    + "\n## Original source records are not accurate-person-life evidence\n\n"
    + "After verified GitHub publication **8,272 Lilly + 1,066 "
    + "Ptolemy = 9,338 historical documentary notes**. "
    + "28 tests of photographed original source/hash/replayed "
    + "portable archive pass. No human spouse appearance, "
    + "physical or moral character, wealth/dowry or mortality "
    + "prediction validated. No runtime rule promotions. "
    + "Separate Chinese lanes 46 BaZi + 26 Zi Wei remain "
    + "source-only and are not merged into Lilly counts.\n"
)
PROGRESS.write_text(
    (
        "# Lilly 1647 original study through spouse appearance, "
        "social status and fortunes — 2026-10-17\n\n"
    )
    + "After authenticated publication **9,338 original historical "
    "source annotations** (8,272 Lilly + 1,066 Ptolemy), "
    "source photo position original PDF631/894 "
    "(**70.6% first-edition scanned page position only**). "
    "B06l adds 131 period source annotations spanning "
    "appearance, supposed temperament, spouse wealth and "
    "subjective marital outcomes, including independent "
    "qualifiers, class-relative wealth and stigmatizing "
    "source moral, medical or mortality labels all explicitly "
    "NONVALIDATED. No source rules into runtime. "
    "NEXT printed CHAP CXXXV mutual love/concord "
    "from PDF631. Chinese original parallel lanes BaZi "
    "46 and Zi Wei 26 source-only notes with 38 source "
    "mechanical tests separately published and carried "
    "into this branch; these are not added to Lilly totals. "
    "Exact historical astronomy and blind human "
    "forecasting remain independent OPEN lanes.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06l.md").read_text()
)
CURRENT.write_text(
    (
        "# Original Lilly spouse appearance, character and wealth source "
        "accepted; marital concord next\n\n"
    )
    + "2026-10-17 Africa/Dakar UTC+0. B06l historical "
    "source R8142-R8272 accepted locally; after GitHub "
    "remote verification 8,272 Lilly + 1,066 Ptolemy "
    "= 9,338 documentary historical notes. "
    "No verified human appearance, spouse character, "
    "wealth or health/mortality forecast and "
    "no promoted runtime source rule. "
    "Separate BaZi (46) and Zi Wei Dou Shu (26) "
    "historical notes integrated into this research "
    "branch but kept in distinct source index. "
    "NEXT printed CXXXV marital mutual love "
    "and concord original PDF631 onward.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06l.md").read_text()
)
receipt = {
    "batch": "B06l",
    "status": "GUARDED_CANONICAL_ORIGINAL_SOURCE_PREPARED_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06l.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": archive["archive_sha256"],
    "lilly_if_published": 8272,
    "ptolemy_retained": 1066,
    "combined_if_published": 9338,
    "separate_chinese_source_notes": 72,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
