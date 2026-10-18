#!/usr/bin/env python3
"""Guarded append-only Lilly original CXL travel causes and attributed Haly."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06t_CAUSE_OF_TRAVEL.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06t.json"):
    assert not p.exists(), f"Duplicate or interrupted original source: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 8806
assert i["read_numbered_chapters"] == list(range(1, 141))
assert i["batches"][-1]["id"] == "B06s"
assert i["next"]["chapter"] == "CXLI"
assert i["next"]["printed_chapter_numeral"] == "CXL"
assert i["next"]["pdf_page"] == 643
assert i["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06t" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 53
assert [x["record_number"] for x in r["rules"]] == list(range(8807, 8860))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R8858", "R8859"]
assert a["lilly_if_published"] == 8859 and a["combined_if_published"] == 9925
assert a["numbered_chapters_added"] == 1
assert r["substantive"] == a["substantive"] == 51
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert w["body_pdf_frames"] == [643, 644]
assert w["following_printed_CXLI_heading_pdf"] == 644
assert not lim["haly_original_text_crosscollated"]
assert not lim["real_person_motive_faith_health_or_intimate_inference_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_person_travel_causes_validated"]
        or x["independent_trade_or_law_motive_validated"]
        or x["independent_people_or_estate_event_validated"]
        or x["independent_animal_or_parent_illness_validated"]
        or x["independent_travel_death_validated"]
        or x["historical_haly_original_independently_verified"]
        or x["private_religious_moral_health_inference_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 24 and sha(z["archive_path"]) == z["archive_sha256"]
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
(BACK / "INDEX_BEFORE_B06t.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06t.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06t.md").write_bytes(PROGRESS.read_bytes())

i["batches"].append(
    {
        "id": "B06t",
        "path": "batches/B06t/RULES.json",
        "records_count": 53,
        "sha256": a["rules_sha256"],
        "scope": (
            "William Lilly original first-edition printed CHAP CXL/"
            "editorial CXLI Cause of Travell, source PDF643–644 "
            "(printed pages609–610), ending before CHAP CXLI "
            "Of Successe in Travell, mid PDF644. 6 original "
            "photo-anchored reversible source groups, 51 "
            "substantive historic claims/conditions and two "
            "following numbered chapter navigation R8807–R8859. "
            "Travel signifier nature and natal house separately "
            "inform attributed motives: Saturn conjunct, dignity "
            "or own travel-signifier status mines, estates, "
            "commodities, older men and merchant contacts; "
            "Jupiter religion, honour, law and clerical/judicial "
            "advancement; first house curiosity and second "
            "house trade and financial gain. Internal original "
            "HALY aphorisms retained INSIDE printed CXL with "
            "ninth ruler placed first to eighth house, outcomes "
            "of journey frequency, wealth, cohabitation with "
            "women and relocation, hidden parental illness "
            "and death while traveling, children abroad, "
            "gain from enslaved people/servants and sick cattle, "
            "wife/obedience, acquiring estate and overseas travel. "
            "No ninth–twelfth rules supplied, Haly original "
            "attribution unverified and no human travel "
            "motive/religion/medical/sex/mortality "
            "accuracy or executable runtime promotions."
        ),
    }
)
i["records_count"] = 8859
i["read_numbered_chapters"].append(141)
i["status"] = "BOOK_III_CXL_CAUSES_OF_TRAVEL_HALY_NEXT_CXLI_SUCCESS"
i["next"] = {
    "pdf_page": 644,
    "printed_page": 610,
    "chapter": "CXLII",
    "printed_chapter_numeral": "CXLI",
    "heading": "Of Successe in Travell",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXLI begins after divider approximately "
        "middle original first-edition PDF644/printed610, "
        "after last Haly eighth-house aphorism. "
        "It runs through remainder of PDF644 and upper/"
        "middle PDF645/printed611, then new printed "
        "CHAP CXLII on Religion of the Native begins "
        "beneath divider later original PDF645. "
        "Verify exact boundary and never absorb "
        "religion claims into travel hazards."
    ),
    "research_scope": (
        "Period claims of favorable/unfavorable "
        "success, friendship and prosperity in travel "
        "versus dangerous travel by house, "
        "malefic strength and sign weather/animals, "
        "robbery, drowning and death. All source-only "
        "and high-stakes; no actual personal danger "
        "forecast may be inferred."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLI_source_acceptance_note"] = (
    "B06t R8807–R8859, 53 original historic annotations, "
    "four photographic pages PDF643–646 SHA/bytes "
    "and 24 independent extracted ZIP/source tests; "
    "planet/house travel causes and HALY only first "
    "through eighth house, no fabricated 9–12 "
    "branches, Haly attribution not collated. "
    "Zero real travel, economic, medical or mortality "
    "validity and no runtime promotions. Chinese "
    "source count 72 separately indexed."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 8859
assert i["read_numbered_chapters"] == list(range(1, 142))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original printed CXL travel-causes and Haly aphorisms documented\n\n"
    + review
    + "\n## Documentary source only, no personal travel-motive validity\n\n"
    + "After verified GitHub publication **8,859 Lilly + "
    + "1,066 Ptolemy =9,925 historical documentary notes**. "
    + "24 source-photo and ZIP-extracted replay tests pass. "
    + "No independent actual travel motives, religion, "
    + "profit, family/animal illness or mortality result "
    + "is validated. Zero executable scoring rules promoted.\n"
)
PROGRESS.write_text(
    "# Lilly first-edition original through Cause of Travel and Haly — 2026-10-18\n\n"
    "After verified source publication **9,925 documentary "
    "historical annotations** (8,859 Lilly +1,066 "
    "Ptolemy), original physical frame 644/894 "
    "(**72.0% scanned-page position only, not full "
    "scientific completion**). Printed CXL adds "
    "53 period source notes, planetary/house "
    "motive classification and attributed Haly "
    "ninth ruler placements first–eighth. "
    "Historical dangerous travel/death and "
    "religion/motive claims are NOT real-world "
    "human forecasts and no runtime source "
    "rules promoted. NEXT printed CXLI travel "
    "success and danger PDF644–645, then "
    "printed CXLII religion begins later PDF645. "
    "Parallel independent Chinese BaZi 46 and "
    "Zi Wei 26 source-only annotations; "
    "original astronomy/math, complete Zi Wei "
    "and BaZi charting, preregistered blind "
    "human evaluation and matched null remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06t.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly CXL travel causes/Haly historically accepted, CXLI next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B06t original source R8807–R8859 "
    "locally prepared. After authenticated remote "
    "publication Lilly 8,859 + Ptolemy 1,066 = "
    "9,925 historical source notes. "
    "24 original source/ZIP integrity replays "
    "pass; no source prediction of true human "
    "motive, belief, economic status, danger, "
    "family illness or travel death validated "
    "and zero model promotions. "
    "NEXT printed CXLI Of Successe in Travell "
    "from mid PDF644–mid PDF645. "
    "Chinese BaZi 46/ Zi Wei 26 "
    "notes indexed independently.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06t.md").read_text()
)
receipt = {
    "batch": "B06t",
    "status": "GUARDED_ORIGINAL_SOURCE_PREPARED_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06t.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8859,
    "ptolemy_retained": 1066,
    "combined_if_published": 9925,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
