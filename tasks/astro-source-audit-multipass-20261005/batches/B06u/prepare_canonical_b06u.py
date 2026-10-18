#!/usr/bin/env python3
"""Guarded first-edition Lilly CXLI travel hazards and regions source admission."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06u_TRAVEL_SUCCESS.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for path in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06u.json"):
    assert not path.exists(), f"Duplicate or incomplete original-source admission: {path}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
mapdata = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 8859
assert i["read_numbered_chapters"] == list(range(1, 142))
assert i["batches"][-1]["id"] == "B06t"
assert i["next"]["chapter"] == "CXLII"
assert i["next"]["printed_chapter_numeral"] == "CXLI"
assert i["next"]["pdf_page"] == 644
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06u" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 76
assert [x["record_number"] for x in r["rules"]] == list(range(8860, 8936))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8934", "R8935"]
assert r["substantive"] == a["substantive"] == 74
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 8935 and a["combined_if_published"] == 10001
assert w["body_pdf_frames"] == [644, 645]
assert w["following_printed_CXLII_heading_frame"] == 645
assert len(mapdata["source_groups"]) == mapdata["source_group_count"] == 6
assert not limits["original_node_heraldic_glyphs_fully_verified"]
assert not limits["geographical_zodiac_country_table_p93_verified"]
assert not limits["person_travel_safety_or_criminality_forecasts_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["real_travel_success_or_profit_validated"]
        or x["real_travel_hazard_crime_or_death_validated"]
        or x["real_favorable_country_location_validated"]
        or x["historical_p93_country_table_verified"]
        or x["person_level_travel_medical_or_safety_advice_authorized"]
        or x["real_person_criminality_or_religion_inference_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in chinese["systems"]] == [46, 26]
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

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
(BACK / "INDEX_BEFORE_B06u.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06u.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06u.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B06u",
        "path": "batches/B06u/RULES.json",
        "records_count": 76,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original 1647 first-edition printed "
            "CHAP CXLI/editorial CXLII Of Successe in Travell "
            "mid PDF644/printed610 through PDF645/printed611, "
            "before independently numbered CHAP CXLII "
            "religion of the native, later PDF645. "
            "Six source-photo reversible groups, 74 substantive "
            "historical claims and two following printed heading "
            "navigation R8860–R8935. Travel signifier strength, "
            "benefic aspect and domicile allegedly safe/prosperous "
            "friendships and honors relative to class; weak "
            "malefic signifiers allegedly difficulty, imprisonment, "
            "betrayal, thieves, soldiers and poverty. Distinct "
            "source zodiac hazard categories: moist showers/"
            "water/isolation, Saturn fixed EXCEPT Scorpio "
            "fall/wind, movable lightning and sudden air, "
            "humane theft, bestial animals/earthquakes/collapse, "
            "Scorpio flux/poison, compounded watery malefic "
            "violent fixed stars drowning, Saturn/ninth ruler "
            "twelfth death versus ninth ruler in Saturn house robbery. "
            "Internal fortunate REGION subsection maps "
            "natal houses 1/10/11/2 and Jupiter/Venus vs "
            "unfavorable 7/6/8/4 and malefic signs; "
            "some source glyphs unresolved and earlier "
            "Part I printed page93 geography table not "
            "collated. No real human travel success/safety/"
            "crime/health or destination predictions and "
            "zero source runtime scoring promotions."
        ),
    }
)
i["records_count"] = 8935
i["read_numbered_chapters"].append(142)
i["status"] = "BOOK_III_CXLI_TRAVEL_SUCCESS_HAZARDS_NEXT_CXLII_RELIGION"
i["next"] = {
    "pdf_page": 645,
    "printed_page": 611,
    "chapter": "CXLIII",
    "printed_chapter_numeral": "CXLII",
    "heading": "Of the Religion of the Native",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLII begins after horizontal divider "
        "lower original first-edition PDF645/printed611, "
        "continues original PDF646/printed612 and "
        "PDF647/printed613, including internal "
        "Aphorismes shewing inclinations to PIETY "
        "and Aphorismes signifying IMPIETY. "
        "Separate numbered CHAP CXLIII Of DREAMES "
        "starts after divider lower PDF647. "
        "Verify exact source and glyphs before admission."
    ),
    "research_scope": (
        "Period Christian attitudes to 'piety' and "
        "religious constancy/changing convictions, "
        "source Jupiter/benefic vs Saturn/Mars "
        "conditions and explicit Lilly caveat "
        "that stars DO NOT force religious belief "
        "or make persons religious. Historic "
        "sectarian labels and religious identity "
        "are not actual individual predictions."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLII_source_acceptance_note"] = (
    "B06u original R8860–R8935, 76 historic "
    "source clauses with original PDF644–648 "
    "SHA/bytes and 26 independently extracted "
    "ZIP tests. Explicit Saturn-fixed Scorpio "
    "exception and compound watery drowning "
    "conditions; no original country/zodiac "
    "table page93 collation and node glyphs "
    "unresolved; zero human danger or travel "
    "geo-validity and no runtime promotions. "
    "Chinese 72 records separately indexed."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 8935
assert i["read_numbered_chapters"] == list(range(1, 143))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original CXLI travel success, danger and regions documented\n\n"
    + review
    + "\n## Historical source, not travel risk guidance or forecast\n\n"
    + "After authenticated GitHub publication **8,935 Lilly "
    + "+1,066 Ptolemy =10,001 historical documentary notes**. "
    + "26 original photo and extracted ZIP source tests pass. "
    + "No actual safe journeys, robbery, drowning, illness, "
    + "country choice or travel fortunes verified "
    + "from natal data. Zero production source rules promoted.\n"
)
PROGRESS.write_text(
    "# Lilly first edition through printed CXLI travel safety and fortunes — 2026-10-18\n\n"
    "After authenticated publication **10,001 original "
    "documentary historical notes** (8,935 Lilly "
    "+1,066 Ptolemy), source frontier first-edition "
    "PDF645/894 (**72.1% physical scanned position "
    "ONLY, not predictive or research completion**). "
    "B06u adds 76 historic conditions on travel "
    "success, hazards and claimed fortunate regions, "
    "with source exceptions and period geographic "
    "lookup at printed page93 still unresolved. "
    "No independent human travel danger or fortune "
    "results validated; no executable source "
    "rule promotions. NEXT printed CXLII on "
    "religion of native, PDF645–647; source "
    "explicitly denies stellar compulsion of faith. "
    "Parallel separate BaZi 46 and Zi Wei 26 "
    "source-only notes remain open; exact "
    "astrological and blinded studies not complete.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06u.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CXLI travel success documented; CXLII religion next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B06u source R8860–R8935 accepted locally, "
    "after remote verification 8,935 Lilly "
    "+1,066 Ptolemy =10,001 historical notes. "
    "26 source and ZIP extraction integrity "
    "tests pass; no real human risk or "
    "religion inference authorized and zero "
    "runtime model promotions. "
    "Next printed CXLII religion starts "
    "lower original PDF645; following CXLIII "
    "dreams starts lower PDF647. "
    "Chinese independent BaZi 46 and "
    "Zi Wei 26 notes separately preserved.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06u.md").read_text()
)
receipt = {
    "batch": "B06u",
    "status": "GUARDED_TRAVEL_SUCCESS_HISTORICAL_SOURCE_PREPARED_PENDING_GITHUB",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06u.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8935,
    "ptolemy_retained": 1066,
    "combined_if_published": 10001,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
