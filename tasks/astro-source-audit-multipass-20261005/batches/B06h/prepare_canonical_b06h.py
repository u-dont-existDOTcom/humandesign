#!/usr/bin/env python3
"""Guarded append of unnumbered seventh-house historical marriage source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06h_SEVENTH_MARRIAGE.md"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06h.json"):
    assert not p.exists(), f"Previous or interrupted source admission: {p}"
idx = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
witness = read(B / "ORIGINAL_SOURCE_WITNESS.json")

assert idx["records_count"] == a["previous_lilly"] == 7877
assert idx["read_numbered_chapters"] == list(range(1, 132))
assert idx["batches"][-1]["id"] == "B06g"
assert idx["next"]["chapter"] == "UNNUMBERED_SEVENTH_HOUSE_MARRIAGE"
assert idx["next"]["pdf_page"] == 621
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06h" for x in idx["batches"])
assert a["new_historical_records"] == r["record_count"] == 66
assert a["lilly_if_published"] == 7943 and a["combined_if_published"] == 9009
assert [x["record_number"] for x in r["rules"]] == list(range(7878, 7944))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R7942", "R7943"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert a["new_numbered_chapters"] == 0
assert witness["seventh_house_intro_is_unnumbered"]
assert witness["following_printed_CXXXI_heading_frame"] == 623
assert not limits["sex_life_character_or_partner_claim_authorized"]
assert all(
    not (
        x["independent_human_marriage_outcome_validated"]
        or x["real_partner_character_or_sexual_behavior_validated"]
        or x["person_level_moral_or_intimate_claim_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 21 and sha(z["archive_path"]) == z["archive_sha256"]

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)

BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06h.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06h.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06h.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06h",
        "path": "batches/B06h/RULES.json",
        "records_count": 66,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly unnumbered seventh-house "
            "Of Marriage and first of Mens Marriages, original "
            "PDF621–623 upper, separate printed CXXXI starts "
            "mid PDF623. Eight passage groups, 64 substantive "
            "source statements and 2 numbered chapter navigation, "
            "R7878–R7943. Men's Venus/Moon, seventh house lord "
            "and occupants, claimed wife's quality/dowry, "
            "barren signs Virgo/Gemini/Leo and 6/9/12 houses "
            "plus expressly non-cadent eighth. Strong Saturn "
            "with debilitated marriage significators may allegedly "
            "oppose marriage, but favorable Venus/Moon strength "
            "overrules Saturn and Moon–Saturn harsh aspect "
            "without many other corroborating indicators is "
            "explicitly insufficient for permanent singleness. "
            "Other period stereotypes about affairs, chastity "
            "and sexual potency, and positive prolific-sign "
            "seventh lord/reception conditions retained as "
            "historical source only. No actual human marriage "
            "or intimate conduct validity, zero scoring promotions."
        ),
    }
)
idx["records_count"] = 7943
# The source is explicitly unnumbered.
assert idx["read_numbered_chapters"] == list(range(1, 132))
idx["status"] = "BOOK_III_UNNUMBERED_SEVENTH_HOUSE_MARRIAGE_SOURCE_NEXT_EASE_OF_WIFE"
idx["next"] = {
    "pdf_page": 623,
    "printed_page": 589,
    "chapter": "CXXXII",
    "printed_chapter_numeral": "CXXXI",
    "heading": "Whether the Native shall obtaine his Wife with ease, or much difficulty",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CXXXI begins below horizontal divider "
        "middle original first-edition PDF623/printed589. "
        "It covers ease of obtaining a wife and continues "
        "with an independently headed 'The time of Marriage' "
        "subsection across following original pages. "
        "Do not confuse the time-of-marriage section "
        "with this earlier unnumbered marriage yes/no source. "
        "Verify true end and next numbered chapter boundary."
    ),
    "research_scope": (
        "Historically asserted marriage ease/difficulty "
        "from greater part benefic/weak signs and "
        "Saturn/Mars exceptions; further original date/"
        "age/timing source may involve directions and "
        "solar/lunar arcs, requiring exact mathematical "
        "scope and independent chronology evidence. "
        "No person-level relationship forecasts validated."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["unnumbered_seventh_house_acceptance_note"] = (
    "B06h original 1647 source R7878-R7943, "
    "66 source clauses including two explicit "
    "Saturn versus Venus/Moon exceptions and "
    "a no-sufficient-evidence Moon/Saturn case. "
    "Original PDF621–625 SHA and 21 standalone "
    "archive-replayed integrity tests; zero "
    "marriage/sexual human predictions and "
    "no runtime scoring rules."
)
assert idx["records_count"] == sum(x["records_count"] for x in idx["batches"]) == 7943
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly first-edition unnumbered seventh-house marriage historically accepted\n\n"
    + review
    + "\n## Source-only, not verified human marriage predictions\n\n"
    + "After verified publication **7,943 Lilly + 1,066 "
    + "Ptolemy = 9,009 historical annotations**. "
    + "21 source integrity/replayed archival tests pass. "
    + "No human marriage, intimate conduct or "
    + "sexual-health predictions have been validated. "
    + "No executable original source rules promoted.\n"
)
PROGRESS.write_text(
    "# Lilly original source through unnumbered seventh-house marriage — 2026-10-17\n\n"
    "After authenticated publication **9,009 historical "
    "source annotations** (7,943 Lilly + 1,066 Ptolemy), "
    "original first-edition source frontier PDF623/894 "
    "(**69.7% scanned page position only**, not program "
    "completion). The unnumbered seventh-house "
    "male marriage introduction adds 66 historic "
    "annotated assertions including opposing Saturn "
    "and Venus/Moon configurations, explicit "
    "insufficiency of lone Moon-Saturn adverse contact, "
    "fecundity/reception and historical moral stereotypes. "
    "Next separately printed CXXXI on ease of obtaining "
    "wife starts middle PDF623. No independent "
    "marriage predictions and no promoted source rules. "
    "Numeric data and blind human tests remain OPEN.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06h.md").read_text()
)
CURRENT.write_text(
    "# Lilly unnumbered seventh-house marriage study accepted, CXXXI next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. B06h "
    "R7878–R7943, 66 historic source notes "
    "prepared. After verified GitHub readback "
    "7,943 Lilly plus 1,066 Ptolemy = "
    "9,009 original documentary records. "
    "Unnumbered section did not increment "
    "numbered-chapter count. No verified "
    "relationship or private sexual-life "
    "forecasts, no runtime source promotions. "
    "NEXT printed CXXXI original PDF623.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06h.md").read_text()
)
receipt = {
    "batch": "B06h",
    "status": "GUARDED_CANONICAL_UNNUMBERED_SOURCE_PREPARED_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B06h.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 7943,
    "ptolemy_retained": 1066,
    "combined_if_published": 9009,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
