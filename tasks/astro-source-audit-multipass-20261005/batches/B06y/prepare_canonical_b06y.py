#!/usr/bin/env python3
"""Guarded append-only source admission for Lilly CXLIIII and its printed-number gap."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06y_DIGNITIES.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06y.json"):
    assert not p.exists(), f"Duplicate or partial admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
table = j(B / "REGAL_FIXED_STARS_1647_TABLE_V1.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = j(CHINESE)

assert i["records_count"] == a["previous_lilly"] == 9124
assert i["read_numbered_chapters"] == list(range(1, 145))
assert i["batches"][-1]["id"] == "B06x"
assert i["next"]["chapter"] == "CXLV"
assert i["next"]["printed_chapter_numeral"] == "CXLIIII"
assert i["next"]["pdf_page"] == 649
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B06y" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 188
assert [x["record_number"] for x in r["rules"]] == list(range(9125, 9313))
assert [x["id"] for x in r["rules"] if x["role"] == "next_navigation"] == ["R9310", "R9311"]
assert r["substantive"] == a["substantive"] == 186
assert r["rules"][-1]["role"] == "skipped_CXLV"
assert a["new_numbered_chapters"] == 1
assert a["lilly_if_published"] == 9312 and a["combined_if_published"] == 10378
assert w["body_original_pdf_frames"] == list(range(649, 656))
assert w["following_printed_CXLVI_heading_frame"] == 655
assert not w["intervening_printed_CXLV_heading_found"]
assert not limits["original_printed_CXLV_found"]
assert not limits["historical_fixed_star_table_modern_parity_passed"]
assert len(m["source_groups"]) == m["source_group_count"] == 12
assert len(table["entries"]) == 6
assert all(not x["modern_identification_verified"] for x in table["entries"])
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "REGAL_FIXED_STARS_1647_TABLE_V1.json") == a["star_table_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 30 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72
assert c["independently_validated_real_human_claims"] == c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    blob == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B06y.json"),
    (CURRENT, "CURRENT_BEFORE_B06y.md"),
    (PROGRESS, "PROGRESS_BEFORE_B06y.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B06y",
        "path": "batches/B06y/RULES.json",
        "records_count": 188,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original Lilly 1647 printed CHAP CXLIIII on dignity/preferment "
            "PDF649 middle to PDF655 upper/printed615-621. "
            "12 reversible photographed groups, 186 substantive "
            "historical source conditions plus 2 next-heading navigation "
            "R9125-R9312. Domicile/exaltation/essential reception "
            "vs lesser dignity and eighth/cadent source anomaly, "
            "fixed-regal-star +/-5degree contacts and six original "
            "source zodiac star positions without modern coordinate parity. "
            "Explicit beggar-versus-king social-class reference "
            "counterexample, divergent solar/lunar time, royal genitures "
            "and Sun/Moon/Midheaven/Ascendant/stellar alternatives "
            "including temporary rise/calamity, with glyph "
            "ambiguities and no scorable human forecasts. "
            "Original numbering jumps printed CXLIIII to CXLVI "
            "with NO separately headed CXLV in studied frames, "
            "a documented numbering anomaly not a missing source "
            "to fabricate. Zero runtime rule promotions."
        ),
    }
)
i["records_count"] = 9312
i["read_numbered_chapters"].append(145)
i["status"] = "BOOK_III_CXLIIII_DIGNITIES_NEXT_PRINTED_CXLVI_ORIGINAL_GAP"
i["next"] = {
    "pdf_page": 655,
    "printed_page": 621,
    "chapter": "CXLVI",
    "printed_chapter_numeral": "CXLVI",
    "heading": "What manner of Preferment, or its quality and cause",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Original printed CHAP CXLVI starts after divider "
        "mid original PDF655/printed621. The preceding "
        "CXLIIII ends at this seam; no separately headed "
        "CXLV appears through PDF649-655, preserve "
        "rather than invent a chapter. Study CXLVI "
        "source through its actual next printed heading."
    ),
    "research_scope": (
        "Historic causes/types of official preferment "
        "by planets partile aspecting luminaries and "
        "house positions, source Saturn hereditary/"
        "elderly vs Jupiter/Venus law/honour/virtue, "
        "Mars military, Mercury speech/learning, "
        "and source status exceptions; no person "
        "occupation or class forecast validated."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLV_source_acceptance_note"] = (
    "B06y R9125-R9312 188 source-only historical annotations, "
    "12 original source groups, original PDF649-660 SHA images "
    "and 30 independent archive tests. Exact period "
    "six-regal-star table frozen without modern parity, "
    "beggar/king source outcome-switch and original printed "
    "CXLIIII -> CXLVI numbering gap preserved. "
    "Zero real status predictions, no runtime promotion."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9312
assert i["read_numbered_chapters"] == list(range(1, 146))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original CXLIIII dignity/preferment historical source documented\n\n"
    + review
    + "\nAfter verified publication 9,312 Lilly +1,066 "
    + "Ptolemy =10,378 documentary notes, 30 source/archive "
    + "checks, zero validated people or promoted rules. "
    + "Original printed CXLV absent; next printed CXLVI.\n"
)
PROGRESS.write_text(
    "# Original Lilly through CXLIIII status and source numbering anomaly — 2026-10-18\n\n"
    "After publication 10,378 historical documentary annotations "
    "(9,312 Lilly +1,066 Ptolemy), original scanned source "
    "position PDF655/894 (~73.3% physical page order ONLY). "
    "B06y added 188 qualified source clauses, source-six-star "
    "coordinates without epoch parity and a critical beggar/"
    "king social-class-relative counterexample; printed "
    "numbering jumps CXLIIII to CXLVI. No human "
    "predictive successes or runtime model promotions. "
    "Next printed CXLVI source begins PDF655. "
    "Chinese source only BaZi46 and ZiWei26 remain "
    "separate; full physics/maths and blind tests open.\n\n---\n\n"
    + (BACK / "PROGRESS_BEFORE_B06y.md").read_text()
)
CURRENT.write_text(
    "# Lilly CXLIIII dignity/preferment original accepted; CXLVI next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B06y R9125-R9312 prepared for authenticated remote "
    "publication; then 9,312 Lilly +1,066 Ptolemy=10,378 "
    "historical source-only annotations. 30 first-edition/"
    "ZIP tests pass, original CXLV printed heading absent, "
    "period fixed-star table preserved without modern "
    "parity, social-class counterexample retained. "
    "No human ranking or status predictions validated. "
    "No production scoring rules promoted. "
    "NEXT printed CXLVI at PDF655, China source "
    "BaZi46/Zi Wei26 still separate.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06y.md").read_text()
)
receipt = {
    "batch": "B06y",
    "status": "GUARDED_ORIGINAL_CXLIIII_SOURCE_PENDING_GITHUB",
    "previous_index_git_blob": blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06y.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "star_table_sha256": sha(B / "REGAL_FIXED_STARS_1647_TABLE_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9312,
    "ptolemy_retained": 1066,
    "combined_if_published": 10378,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
