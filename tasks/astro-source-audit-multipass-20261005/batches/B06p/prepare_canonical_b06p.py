#!/usr/bin/env python3
"""Guarded original 1647 UNNUMBERED fifth-house source archival admission."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06p_CHILDREN_INTRO.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06p.json"):
    assert not path.exists(), f"Duplicate or partially interrupted admission: {path}"
idx = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
c = j(CHINESE)

assert idx["records_count"] == a["prior_lilly"] == 8496
assert idx["read_numbered_chapters"] == list(range(1, 139))
assert idx["batches"][-1]["id"] == "B06o"
assert idx["next"]["chapter"] == "UNNUMBERED_FIFTH_HOUSE_CHILDREN"
assert idx["next"]["pdf_page"] == 636
assert idx["next"]["printed_chapter_numeral"] is None
assert idx["next"]["following_printed_chapter_numeral"] == "CXXXVIII"
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(item["id"] == "B06p" for item in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 106
assert [x["record_number"] for x in r["rules"]] == list(range(8497, 8603))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8601", "R8602"]
assert r["substantive"] == a["substantive"] == 104
assert a["new_numbered_chapters"] == 0
assert a["lilly_if_published"] == 8602
assert a["combined_if_published"] == 9668
assert r["first_ed_printed_chapter_number"] is None
assert w["unnumbered"]
assert w["body_pdf_frames"] == [636, 637, 638]
assert w["following_printed_CXXXVIII_heading_frame"] == 638
assert len(mapdata["source_groups"]) == mapdata["source_groups_count"] == 8
assert not limits["original_glyphs_fully_resolved"]
assert not limits["medical_or_child_death_predictions_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_human_fertility_accuracy_validated"]
        or x["independent_human_child_count_validated"]
        or x["independent_real_child_health_or_death_validated"]
        or x["human_parent_child_morality_claim_authorized"]
        or x["person_level_medical_fertility_advice_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 31 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in c["systems"]] == [46, 26]
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06p.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06p.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06p.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06p",
        "path": "batches/B06p/RULES.json",
        "records_count": 106,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly 1647 first edition UNNUMBERED "
            "substantive fifth-house and children introduction, original "
            "PDF636 middle to PDF638 middle/printed602-604. Before next "
            "printed CHAP CXXXVIII on How many Children Native may have. "
            "Eight photo-anchored reversible source groups, 104 substantive "
            "historical clauses and two next numbered chapter navigation "
            "R8497–R8602. Original fifth > eleventh > first house "
            "priority and positive or negative fifth testimony override "
            "contrary eleventh; fallback Lord Fifth if houses empty, "
            "majority witnesses unweighted. Traditional fruitful Jupiter "
            "Venus Moon North Node vs barren Saturn Mars Sun South Node, "
            "Mercury originally indifferent/convertible by aspects, "
            "dignity and Oriental/Occidental condition; planets/signs "
            "mixed fertile and barren yield intermediate testimony. "
            "Period aphorisms attributed Alubater Schoner Origanus "
            "without independent collation; combinations Moon/Mercury, "
            "benefic fifth, ascendant and angularity. "
            "Alternative claims of many/few/no children, mortality, "
            "abortion, infertility, health and child morality are "
            "unvalidated and never appropriate individual forecasts. "
            "Unknown glyphs and retrospective Jupiter-fifth anecdote "
            "preserved as source limits. ZERO human predictive "
            "validations or runtime source promotions."
        ),
    }
)
idx["records_count"] = 8602
# The fifth-house text has NO separately printed chapter heading.
assert idx["read_numbered_chapters"] == list(range(1, 139))
idx["status"] = "BOOK_III_UNNUMBERED_CHILDREN_FIFTH_HOUSE_NEXT_PRINTED_CHILD_COUNT"
idx["next"] = {
    "pdf_page": 638,
    "printed_page": 604,
    "chapter": "CXXXIX",
    "printed_chapter_numeral": "CXXXVIII",
    "heading": "How many Children the Native may have",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Next separately printed CHAP CXXXVIII starts after "
        "divider in lower original PDF638/printed604 "
        "following UNNUMBERED fifth-house/children introduction. "
        "It continues PDF639 and later; original PDF636–639 "
        "photographs preserved. Check true next printed "
        "chapter boundary before extracting complete section."
    ),
    "research_scope": (
        "Historical methods of number of children allegedly from "
        "fifth ruler, natal fifth/eleventh/first house positions, "
        "partile applications, planet fecundity and strength, "
        "various female/male and birth/mortality stereotypes. "
        "Separate exact child count, live births, pregnancies, "
        "loss, infant mortality and fertility, all unverified "
        "and not medical forecasts."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["unnumbered_fifth_house_source_acceptance_note"] = (
    "B06p original unnumbered source R8497–R8602, 106 historic "
    "annotations, 8 groups, original PDF636–639 photo SHA and "
    "31 full extracted archive replay tests. Fifth-over-eleventh "
    "priority, Mercury convertible, mixed sign results and "
    "unverified child death/infertility outcomes preserved. "
    "No human reproductive validity, medical claims or runtime "
    "promotion; Chinese BaZi+Zi Wei source counts separate 72."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 8602
assert idx["read_numbered_chapters"] == list(range(1, 139))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly original unnumbered fifth-house/children source documented\n\n"
    + review
    + "\n## Historical documents only, never child mortality or fertility forecasts\n\n"
    + "Following authenticated publication **8,602 Lilly + 1,066 "
    + "Ptolemy = 9,668 documentary historical source notes**. "
    + "31 first-edition source/ZIP extraction tests pass; no "
    + "human conception, live births, child survival or "
    + "medical outcome prediction validated. No model promotions. "
    + "Separate Chinese source-only lanes still 46 BaZi/26 Zi Wei.\n"
)
PROGRESS.write_text(
    "# Lilly historical source through unnumbered fifth-house children — 2026-10-17\n\n"
    "After authenticated remote publication **9,668 historical "
    "notes** (8,602 Lilly + 1,066 Ptolemy); original first-edition "
    "source frontier PDF638/894 (**71.4% scanned physical page "
    "position ONLY, not entire science completion**). "
    "UNNUMBERED fifth-house introduction has 106 source notes "
    "and explicitly fifth over eleventh conflicting-testimony "
    "precedence, Mercury-dependent fertility category and "
    "old unsupported child morbidity, mortality, miscarriage "
    "and parent-life claims. All genuine clinical/personal "
    "predictions 0, runtime rules 0. Numbered chapter counter "
    "UNCHANGED. NEXT printed CHAP CXXXVIII child counts from "
    "lower PDF638. Chinese BaZi 46 and Zi Wei 26 historical "
    "source annotations remain independent with 38 scoped "
    "mechanics tests; neither historical tradition's human "
    "prediction accuracy independently validated.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06p.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly unnumbered fifth-house/children source accepted; child count next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06p source R8497–R8602 "
    "accepted locally. After verified GitHub readback 8,602 "
    "Lilly + 1,066 Ptolemy = 9,668 historic source notes. "
    "31 original-photo/replayed archive integrity tests pass; "
    "no independent real fertility/child health accuracy, "
    "zero runtime scoring promotions. The UNNUMBERED section "
    "did not change numbered chapter count. NEXT original "
    "printed CXXXVIII child count on PDF638. "
    "Chinese source BaZi 46 / Zi Wei 26 notes separately indexed.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06p.md").read_text()
)
receipt = {
    "batch": "B06p",
    "status": "GUARDED_UNNUMBERED_CHILD_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06p.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8602,
    "ptolemy_retained": 1066,
    "combined_if_published": 9668,
    "numbered_chapters_added": 0,
    "separate_chinese_source_notes": 72,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
