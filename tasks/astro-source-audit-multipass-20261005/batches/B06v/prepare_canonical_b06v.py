#!/usr/bin/env python3
"""Guarded historical source accession, Lilly printed CXLII."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06v_RELIGION.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06v.json"):
    assert not p.exists(), f"Previous source admission: {p}"
i = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
guard = read(B / "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = read(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 8935
assert i["read_numbered_chapters"] == list(range(1, 143))
assert i["batches"][-1]["id"] == "B06u"
assert i["next"]["chapter"] == "CXLIII"
assert i["next"]["printed_chapter_numeral"] == "CXLII"
assert i["next"]["pdf_page"] == 645
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert r["record_count"] == a["new_historical_annotations"] == 104
assert [x["record_number"] for x in r["rules"]] == list(range(8936, 9040))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R9038", "R9039"]
assert a["numbered_chapters_added"] == 1
assert w["body_original_pdf_frames"] == [645, 646, 647]
assert w["next_printed_CXLIII_heading_frame"] == 647
assert len(m["source_groups"]) == m["source_group_count"] == 7
assert guard["strict_source_scope"]["denies_stars_enforce_faith"]
assert guard["strict_source_scope"]["denies_stars_cause_religion_or_irreligion"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json") == a["causal_guard_sha256"]
assert (
    z["replayed_tests"] == 29 and z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
)
assert sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72 and chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for before, name in (
    (INDEX, "INDEX_BEFORE_B06v.json"),
    (CURRENT, "CURRENT_BEFORE_B06v.md"),
    (PROGRESS, "PROGRESS_BEFORE_B06v.md"),
):
    (BACK / name).write_bytes(before.read_bytes())

i["batches"].append(
    {
        "id": "B06v",
        "path": "batches/B06v/RULES.json",
        "records_count": 104,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 first-edition printed CXLII, source PDF645-647; "
            "seven reversible groups, 102 historical conditions and two "
            "next-chapter navigation, R8936-R9039. Historic Christian piety "
            "and impiety rubrics, multiple explicit Saturn/benefic exceptions, "
            "and Lilly's crucial stated rejection of stellar causation of faith. "
            "Separate causal scope and image/record details retained in B06v. "
            "No person-level religion, moral or divinatory classification "
            "established and zero runtime promotions."
        ),
    }
)
i["records_count"] = 9039
i["read_numbered_chapters"].append(143)
i["status"] = "BOOK_III_CXLII_HISTORICAL_RELIGION_NEXT_CXLIII_DREAMS"
i["next"] = {
    "pdf_page": 647,
    "printed_page": 613,
    "chapter": "CXLIV",
    "printed_chapter_numeral": "CXLIII",
    "heading": "Of Dreames",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CXLIII on Dreams begins below divider on original "
        "PDF647/printed613. Continues PDF648 and later; establish "
        "next numbered heading before complete extraction."
    ),
    "research_scope": (
        "Historical dream quality/content and alleged prophecy from "
        "ninth-house planets, categories, dignity and aspects. "
        "No actual dream-event prediction validation."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLIII_source_acceptance_note"] = (
    "B06v original R8936-R9039, 104 source notes, "
    "PDF645-649 SHA images and 29 independent archive tests; "
    "source explicit denial of celestial religious causation; "
    "zero human prediction and runtime promotions."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9039
assert i["read_numbered_chapters"] == list(range(1, 144))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original Lilly CXLII religion and noncausation documented\n\n"
    + review
    + "\n## Archival source status\n\n"
    + "After verified remote publication 9,039 Lilly and "
    + "1,066 Ptolemy = 10,105 documentary historical records. "
    + "29 photo/ZIP integrity tests pass. Source explicitly "
    + "denies stellar causation of belief. No actual "
    + "human belief/values accuracy validated and "
    + "zero scoring model promotions.\n"
)
PROGRESS.write_text(
    "# Lilly original historical source through religion — 2026-10-18\n\n"
    "After remote verification 10,105 historical "
    "documentary source notes (9,039 Lilly + 1,066 Ptolemy). "
    "Original first-edition physical scan PDF647/894 "
    "(72.4% page position, NOT scientific completion). "
    "B06v adds 104 source notes across seven passage groups "
    "and a separate author causal-scope guard. Lilly "
    "says stars cannot force or cause religion, "
    "while proposing natural inclination/persistence "
    "as a symbolic historical judgment. "
    "No individual beliefs or behaviors validated. "
    "Next printed CXLIII Dreams from PDF647. "
    "Chinese BaZi 46 and Zi Wei 26 source-only "
    "notes kept separately indexed, full computational "
    "and blind human validations OPEN.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06v.md").read_text()
)
CURRENT.write_text(
    "# Lilly printed CXLII historical religion complete, CXLIII dreams next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. "
    "B06v source R8936–R9039 prepared for authenticated "
    "publication; after remote readback 9,039 Lilly "
    "+ 1,066 Ptolemy = 10,105 source notes. "
    "Author explicitly rejects stellar causation of religion. "
    "No person religion or moral classification validated, "
    "no executable source rules promoted. "
    "29 source and ZIP replay integrity tests pass. "
    "NEXT CXLIII Dreams on original PDF647. "
    "Independent Chinese source 72 notes unchanged.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B06v.md").read_text()
)
receipt = {
    "batch": "B06v",
    "status": "GUARDED_HISTORICAL_SOURCE_PREPARED_PENDING_REMOTE",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06v.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "causal_guard_sha256": sha(B / "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9039,
    "ptolemy_retained": 1066,
    "combined_if_published": 10105,
    "separate_chinese_source_notes": 72,
    "numbered_chapters_added": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
