#!/usr/bin/env python3
"""Guarded original Lilly women's-marriage source accession, not a forecast."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B06o_WOMENS_MARRIAGE.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261017.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06o.json"):
    assert not p.exists(), f"Duplicate or interrupted source acceptance: {p}"
idx = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261017.json")
c = read(CHINESE)

assert idx["records_count"] == a["prior_lilly"] == 8397
assert idx["read_numbered_chapters"] == list(range(1, 138))
assert idx["batches"][-1]["id"] == "B06n"
assert idx["next"]["chapter"] == "CXXXVIII"
assert idx["next"]["printed_chapter_numeral"] == "CXXXVII"
assert idx["next"]["pdf_page"] == 634
assert idx["source_sha256"] == ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
assert idx["empirical_validations"] == idx["runtime_promotions"] == 0
assert not any(x["id"] == "B06o" for x in idx["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 99
assert [x["record_number"] for x in r["rules"]] == list(range(8398, 8497))
assert [x["id"] for x in r["rules"] if x["role"] == "next_section_navigation"] == ["R8495", "R8496"]
assert r["substantive"] == a["substantive"] == 97
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 8496
assert a["combined_if_published"] == 9562
assert w["body_original_pdf_frames"] == [634, 635, 636]
assert w["following_unnumbered_fifth_house_start_frame"] == 636
assert w["following_printed_CXXXVIII_heading_frame"] == 638
assert len(m["source_groups"]) == m["source_group_count"] == 7
assert not limits["original_source_glyphs_fully_resolved"]
assert not limits["sex_gender_partner_morality_predictions_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_legal_marriage_occurrence_validated"]
        or x["independent_marriage_ages_or_number_validated"]
        or x["independent_husband_origin_wealth_traits_validated"]
        or x["independent_marital_concord_validated"]
        or x["real_partner_identity_gender_sexual_conduct_claim_authorized"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert [x["accepted_source_annotations"] for x in c["systems"]] == [46, 26]
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

relative = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=ROOT).returncode == 0
before = subprocess.check_output(
    ["git", "rev-parse", "HEAD:" + relative], cwd=ROOT, text=True
).strip()
assert (
    before
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
(BACK / "INDEX_BEFORE_B06o.json").write_bytes(INDEX.read_bytes())
(BACK / "CURRENT_BEFORE_B06o.md").write_bytes(CURRENT.read_bytes())
(BACK / "PROGRESS_BEFORE_B06o.md").write_bytes(PROGRESS.read_bytes())

idx["batches"].append(
    {
        "id": "B06o",
        "path": "batches/B06o/RULES.json",
        "records_count": 99,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original William Lilly 1647 first edition printed CHAP CXXXVII/"
            "editorial CXXXVIII, Of the Marriage of Women, original PDF634 "
            "middle to PDF636 middle (printed 600–602), ending before "
            "separate UNNUMBERED fifth-house/children introduction "
            "after double rule on PDF636. 7 reversible source groups "
            "with 97 substantive period claims and 2 next-section "
            "navigation R8398–R8496. Historical women-marriage Sun/Mars "
            "primary factors rather than male Venus/Moon, but "
            "source exceptions return to Sun AND Moon masculine signs "
            "or Venus seventh and Venus dispositor for specific "
            "number/desire rules; no global automatic substitution. "
            "Positive versus barren weak marriages, separate subjective "
            "desire, ease versus difficulty, special directions of "
            "Midheaven/Sun and Oriental/Occidental qualitative age "
            "OR spouse-age alternatives; multiple conflicting husband "
            "counts from one/many-formed signs, matutine aspects, "
            "common signs, Venus or Sun corporal same-sign planets "
            "and Sun applying to dignity-holders NOT inverse. "
            "Origin allegedly stranger via peregrine signifiers and "
            "unresolved third-house glyph; husband's appearance/"
            "character and unverified author confidence. Lilly "
            "explicitly dissents from ancient husband-wealth method, "
            "instead judges eighth house/lord and occupants. "
            "Mutual reception, sextile/trine and 6/8/12 negative "
            "house claims of agreement are period rhetoric only. "
            "No actual person marriage, sex-life, husband condition, "
            "wealth or marital concord forecasts validated or promoted."
        ),
    }
)
idx["records_count"] = 8496
idx["read_numbered_chapters"].append(138)
idx["status"] = "BOOK_III_WOMENS_MARRIAGE_NEXT_UNNUMBERED_CHILDREN_FIFTH_HOUSE"
idx["next"] = {
    "pdf_page": 636,
    "printed_page": 602,
    "chapter": "UNNUMBERED_FIFTH_HOUSE_CHILDREN",
    "heading": "The fift House and its proper Judgments. Viz. Of Children",
    "printed_chapter_numeral": None,
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "The substantive UNNUMBERED fifth-house/children "
        "introduction starts after a double divider around "
        "middle original first-edition PDF636/printed602. "
        "It continues original PDF637/printed603 and "
        "upper/middle PDF638/printed604; separate numbered "
        "printed CHAP CXXXVIII on HOW MANY Children starts "
        "after divider lower PDF638. Do not increment the "
        "numbered chapter counter for this unnumbered "
        "introduction and do not swallow the next CXXXVIII."
    ),
    "following_printed_chapter_numeral": "CXXXVIII",
    "following_original_pdf_page": 638,
    "research_scope": (
        "Historical fifth/eleventh/first house and ruler, "
        "fruitful/barren planets/signs, fifth overriding "
        "eleventh, Moon/Mercury, benefics/malefics, source "
        "qualifiers for alleged childbearing, childlessness, "
        "stillbirth and child mortality. Period hypotheses "
        "only: NO actual fertility/health/death prediction "
        "or medical advice. Preserve every fifth-house "
        "priority exception and astronomical glyph uncertainty."
    ),
}
idx["current_state"] = str(LATEST.relative_to(ROOT))
idx["chapter_CXXXVIII_source_acceptance_note"] = (
    "B06o source R8398–R8496, 99 historic notes, "
    "original PDF634–638 SHA/bytes and 26 archived "
    "replayed documentary tests. Women's historical "
    "Sun/Mars marriage model with explicitly retained "
    "Moon/Venus counterexamples, many outcome switches "
    "and author eighth-house husband wealth alternative. "
    "Next immediate unnumbered fifth-house section "
    "PDF636, next numbered CXXXVIII only PDF638. "
    "Zero human prediction or runtime promotion; "
    "Chinese BaZi/Zi Wei 72 notes independently indexed."
)
assert idx["records_count"] == sum(b["records_count"] for b in idx["batches"]) == 8496
assert idx["read_numbered_chapters"] == list(range(1, 139))
INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261017.md").read_text()
LATEST.write_text(
    "# Lilly 1647 original women's-marriage chapter historically documented\n\n"
    + review
    + "\n## Documentary record not personal relationship science\n\n"
    + "After authenticated GitHub publication **8,496 Lilly "
    + "+ 1,066 Ptolemy = 9,562 historical source annotations**. "
    + "Twenty-six first-edition photo/archive-replayed tests pass. "
    + "No independent real marriage age/count, husband traits, "
    + "sexual conduct or wealth forecasts established. "
    + "Separate Chinese BaZi and Zi Wei preserved; "
    + "zero runtime source promotions.\n"
)
PROGRESS.write_text(
    "# Lilly original women marriage through printed CXXXVII — 2026-10-17\n\n"
    "After verified remote publication **9,562 historical "
    "records** (8,496 Lilly + 1,066 Ptolemy); "
    "original book PDF636/894 (**71.1% physical "
    "scanned-page position only, not scientific "
    "completion**). B06o adds 99 historical source "
    "claims including qualified sex-coded marriage "
    "Sun/Mars rules, preserved Venus/Moon exceptions, "
    "age-of-spouse versus wedding-time alternate "
    "predictions, several incompatible spouse-count "
    "methods, author eighth-house husband wealth "
    "contrary to earlier writers, and claimed "
    "concord. No real couple predictions validated; "
    "no scorer/runtime rules promoted. NEXT "
    "unnumbered fifth-house children introduction "
    "PDF636-638, then printed CXXXVIII on number "
    "of children begins late PDF638. Parallel "
    "Chinese BaZi 46 and Zi Wei 26 historical "
    "source notes remain independent and still "
    "need full chart engines/untouched human tests.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06o.md").read_text()
)
CURRENT.write_text(
    "# Original Lilly women marriage source documented; unnumbered children next\n\n"
    "2026-10-17 Africa/Dakar UTC+0. Source batch "
    "B06o R8398–R8496 prepared. After verified "
    "GitHub remote 8,496 Lilly + 1,066 Ptolemy "
    "= 9,562 historical source notes. "
    "Twenty-six original source tests and portable "
    "ZIP replay pass. No actual person marriage "
    "predictions and zero production scoring "
    "promotions. Next UNNUMBERED fifth-house "
    "children section starts original PDF636, "
    "numbered CXXXVIII only at PDF638. "
    "Chinese BaZi 46 and Zi Wei 26 "
    "source-only notes retained separately.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06o.md").read_text()
)
receipt = {
    "batch": "B06o",
    "status": "GUARDED_SOURCE_ACCEPTANCE_PREPARED_PENDING_REMOTE",
    "previous_index_git_blob": before,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06o.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 8496,
    "ptolemy_retained": 1066,
    "combined_if_published": 9562,
    "separate_chinese_source_notes": 72,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
