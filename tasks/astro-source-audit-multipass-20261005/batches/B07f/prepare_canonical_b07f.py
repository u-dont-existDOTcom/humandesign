#!/usr/bin/env python3
"""Guarded first-edition original CLI two-chart concord source append-only."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07f_TWO_NATIVITY_CONCORD.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07f.json"):
    assert not p.exists(), f"Duplicate or partial source admission: {p}"

i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
lim = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
guard = j(B / "DYAD_HISTORICAL_VALIDATION_GUARD_V1.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["previous_lilly"] == 9926
assert i["read_numbered_chapters"] == list(range(1, 151))
assert i["batches"][-1]["id"] == "B07e"
assert i["next"]["chapter"] == "CLI"
assert i["next"]["printed_chapter_numeral"] == "CLI"
assert i["next"]["pdf_page"] == 671
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07f" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 93
assert [x["record_number"] for x in r["rules"]] == list(range(9927, 10020))
assert [
    x["id"]
    for x in r["rules"]
    if x["role"] in ("next_unnumbered_navigation", "later_numbered_navigation")
] == ["R10016", "R10017", "R10018", "R10019"]
assert r["substantive"] == a["substantive"] == 89
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 10019
assert a["combined_if_published"] == 11085
assert w["original_body_pdf_frames"] == [671, 672, 673]
assert w["next_unnumbered_twelfth_house_pdf"] == 673
assert w["following_printed_CLIII_pdf"] == 674
assert not w["original_intervening_CLII_heading_found"]
assert not lim["original_planet_friendship_glyphs_fully_verified"]
assert not lim["real_person_relationship_risk_or_moral_inferences_authorized"]
assert not guard["original_glyphs_fully_cross_collated"]
assert len(m["source_groups"]) == m["source_group_count"] == 8
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "DYAD_HISTORICAL_VALIDATION_GUARD_V1.json") == a["dyad_guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 26 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for path, name in (
    (INDEX, "INDEX_BEFORE_B07f.json"),
    (CURRENT, "CURRENT_BEFORE_B07f.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07f.md"),
):
    (BACK / name).write_bytes(path.read_bytes())

i["batches"].append(
    {
        "id": "B07f",
        "path": "batches/B07f/RULES.json",
        "records_count": 93,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 Lilly printed CHAP CLI on paired Nativities "
            "and friendship concord starts middle original PDF671/"
            "printed637, continues PDF672 and ends upper PDF673/"
            "printed639 before a separate UNNUMBERED 12th-house "
            "Of Enemies source starts lower SAME original PDF673; "
            "printed CLIII enemy quality begins PDF674, no separate "
            "CLII heading observed between. Eight reversible original "
            "photo passage groups, 89 substantive historical "
            "conditions and 4 future navigation R9927–R10019. "
            "Comparison expressly requires TWO independently "
            "computed Ascendants and occupants, both Ascendant "
            "rulers and reception/aspects, old nonreciprocal "
            "natural planetary friendship tables, four asserted "
            "lord-concord routes, cross-chart light/benefic/"
            "malefic planet placement swaps, opposite/mixed "
            "malefic rivalry, old moralizing planetary motives, "
            "best same-sign source, asymmetric which-person-loves-"
            "more source and supposed negative 6th/8th/12th "
            "house alignment. Historical source only, some glyphs "
            "unverified; zero independently validated human "
            "dyads, no actual safety/morality character claims "
            "and no executable runtime scoring promotions."
        ),
    }
)
i["records_count"] = 10019
i["read_numbered_chapters"].append(151)
i["status"] = "BOOK_III_CLI_PAIRWISE_CONCORD_NEXT_UNNUMBERED_TWELFTH_ENEMIES"
i["next"] = {
    "pdf_page": 673,
    "printed_page": 639,
    "chapter": "UNNUMBERED_TWELFTH_HOUSE_ENEMIES",
    "printed_chapter_numeral": None,
    "heading": "Of the twelfth House. Of Enemies",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "following_printed_chapter_numeral": "CLIII",
    "following_original_pdf_page": 674,
    "position": (
        "Original SUBSTANTIVE UNNUMBERED twelfth-house "
        "Of Enemies section begins beneath divider lower "
        "original PDF673/printed639, after CHAP CLI on "
        "two-nativity mutual concord. It runs through "
        "TOP original PDF674/printed640 before another "
        "divider introducing separate printed CHAP CLIII "
        "What manner of Enemies/their Quality. "
        "No separately headed original CLII has been "
        "found between printed CLI and CLIII. "
        "Retain exact original numbering; do not "
        "count unnumbered enemies as printed CLII."
    ),
    "research_scope": (
        "Historically claimed number or prevalence "
        "of enemies by seventh/twelfth occupants, "
        "malefics, lights in opposition, lords "
        "seventh/twelfth and ascendant, with "
        "benefic/nodal variants. Keep enemy count "
        "separate from identity/type/strength and "
        "any actual real-person danger or accusations."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CLI_source_acceptance_note"] = (
    "B07f R9927–R10019, 93 original first edition "
    "source-only annotations, eight reversible "
    "photo groups PDF671–675 SHA/bytes, "
    "26 ZIP-extracted source integrity replays. "
    "Original pairwise method requires 2 charts, "
    "natural planetary friendship can be "
    "NONRECIPROCAL, directional affection separate "
    "from duration and conflict, printed CLII "
    "heading not found and following unnumbered "
    "twelfth house from PDF673 preserved. "
    "Zero real human relationship accuracy or "
    "runtime rule promotion; Chinese 72 separate."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 10019
assert i["read_numbered_chapters"] == list(range(1, 152))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly CLI two-nativity mutual concord historically documented\n\n"
    + review
    + "\nAfter GitHub verified publication 10,019 Lilly "
    + "+1,066 Ptolemy =11,085 historical source records. "
    + "26 first-edition source and ZIP archive replays pass, "
    + "no real dyadic compatibility/conflict/person "
    + "prediction or production rules validated.\n"
)
PROGRESS.write_text(
    "# Original Lilly first edition through two-nativity CLI — 2026-10-18\n\n"
    "After authenticated publication **11,085 historic source "
    "annotations** (10,019 Lilly +1,066 Ptolemy), "
    "original first-edition physical scan frontier "
    "PDF673/894 (**75.3% scanned page position ONLY, "
    "not full source or predictive science completion**). "
    "B07f adds 93 historic clauses for two-nativity "
    "concord/discord, natural asymmetrical planet "
    "affinity, same Ascendant and ruler, four reception/"
    "aspect routes and directional affection. "
    "No real paired participant has been scored "
    "and no source runtime rules promoted. "
    "NEXT UNNUMBERED twelfth-house enemies introduction "
    "PDF673–674; printed CLIII enemies quality later "
    "PDF674; historical CLII printed heading absent. "
    "Chinese BaZi46, Zi Wei26 separately indexed.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B07f.md").read_text()
)
CURRENT.write_text(
    "# Lilly printed CLI on two natal charts documented; enemies introduction next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B07f historical records R9927–R10019 "
    "prepared and pending verified GitHub remote. "
    "After publication 10,019 Lilly +1,066 "
    "Ptolemy =11,085 original source notes. "
    "26 image/archive integrity checks pass; "
    "no actual relationship/morality/danger "
    "accuracy or runtime model promotions. "
    "NEXT unnumbered twelfth-house `Of Enemies` "
    "from PDF673 to PDF674 (then numbered CLIII). "
    "Chinese BaZi46/ZiWei26 separate historic notes.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07f.md").read_text()
)
receipt = {
    "batch": "B07f",
    "status": "GUARDED_CLI_TWO_NATIVITY_HISTORICAL_SOURCE_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07f.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "dyad_guard_sha256": sha(B / "DYAD_HISTORICAL_VALIDATION_GUARD_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 10019,
    "ptolemy_retained": 1066,
    "combined_if_published": 11085,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
