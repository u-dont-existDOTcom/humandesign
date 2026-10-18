#!/usr/bin/env python3
"""Guarded, append-only 1647 Lilly printed dreams source admission."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B06w_DREAMS.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B06w.json"):
    assert not p.exists(), f"Previously applied archive: {p}"
i = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
c = read(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9039
assert i["read_numbered_chapters"] == list(range(1, 144))
assert i["batches"][-1]["id"] == "B06v"
assert i["next"]["chapter"] == "CXLIV"
assert i["next"]["printed_chapter_numeral"] == "CXLIII"
assert i["next"]["pdf_page"] == 647
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(b["id"] == "B06w" for b in i["batches"])
assert r["record_count"] == a["new_historical_records"] == 66
assert [x["record_number"] for x in r["rules"]] == list(range(9040, 9106))
assert [x["id"] for x in r["rules"] if x["role"] == "next_section_navigation"] == ["R9104", "R9105"]
assert r["substantive"] == a["substantive"] == 64
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 9105
assert a["combined_if_published"] == 10171
assert w["body_original_pdf_frames"] == [647, 648]
assert w["following_unnumbered_tenth_house_pdf"] == 649
assert w["following_printed_CXLIIII_heading_pdf"] == 649
assert len(m["source_groups"]) == m["source_group_count"] == 7
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(
    not (
        x["independent_dream_content_prediction_validated"]
        or x["independent_dream_prophecy_accuracy_validated"]
        or x["independent_sleep_psychological_diagnosis_validated"]
        or x["human_spiritual_or_nightmare_classification_authorized"]
        or x["dream_to_real_event_causation_verified"]
        or x["runtime_model_promoted"]
    )
    for x in r["rules"]
)
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 21 and sha(z["archive_path"]) == z["archive_sha256"]
assert c["sum_source_annotations"] == 72 and c["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B06w.json"),
    (CURRENT, "CURRENT_BEFORE_B06w.md"),
    (PROGRESS, "PROGRESS_BEFORE_B06w.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B06w",
        "path": "batches/B06w/RULES.json",
        "records_count": 66,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original first-edition 1647 printed CHAP CXLIII Of Dreames, "
            "PDF647 lower through PDF648 bottom/printed613-614. "
            "Seven reversible original photo source groups, "
            "64 substantive historical dream claims and two following "
            "navigation R9040-R9105. Jupiter/Venus strong ninth "
            "alleged corresponding dreams, malefic ninth alleged false "
            "dreams, weak benefics allow ambiguous sometimes true/"
            "sometimes false; empty ninth fallback to cusp/lord. "
            "Content themes historically attributed to Saturn/Jupiter/"
            "Mars/Sun/Venus/Mercury/Moon and Saturn+Moon frightening "
            "case. Dream content, psychological interpretation and "
            "future event verification are entirely different targets. "
            "No source claims validated on independently observed "
            "humans, no production predictions or runtime promotions. "
            "Next immediate original source UNNUMBERED tenth-house "
            "honours introduction PDF649, then numbered CXLIIII."
        ),
    }
)
i["records_count"] = 9105
i["read_numbered_chapters"].append(144)
i["status"] = "BOOK_III_CXLIII_DREAMS_NEXT_UNNUMBERED_TENTH_HOUSE"
i["next"] = {
    "pdf_page": 649,
    "printed_page": 615,
    "chapter": "UNNUMBERED_TENTH_HOUSE_HONOURS_DIGNITIES",
    "printed_chapter_numeral": None,
    "heading": "The tenth House, and the Judgments thereunto appertaining",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "following_printed_chapter_numeral": "CXLIIII",
    "following_original_pdf_page": 649,
    "position": (
        "The original unnumbered tenth-house introduction "
        "starts upper PDF649/printed615 after dreams end on "
        "PDF648. It lists the sources for honours/dignities, "
        "then separately numbered CHAP CXLIIII begins on "
        "the SAME PDF649, below horizontal divider. "
        "Accept the unnumbered source separately first."
    ),
    "research_scope": (
        "Original historical hierarchy of Sun and luminaries, "
        "lord of Midheaven, tenth-house occupant planets, "
        "and first/second-magnitude regal stars near first/"
        "tenth cusps. No actual social rank or professional "
        "status predictions validated."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CXLIV_source_acceptance_note"] = (
    "B06w original R9040-R9105, 66 historic records, "
    "PDF647-651 images SHA and 21 archive-replayed "
    "documentary tests. Dream truth vs dream content "
    "explicitly distinguished; no actual future-event "
    "validation, sleep diagnosis or runtime promotions."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9105
assert i["read_numbered_chapters"] == list(range(1, 145))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly original printed dream chapter historically documented\n\n"
    + review
    + "\n## Historical documentation, no predictive success\n\n"
    + "After authenticated GitHub publication "
    + "9,105 Lilly + 1,066 Ptolemy = 10,171 "
    + "source-only historical records; 21 photo/archive "
    + "tests pass. No human dream accuracy, prophecy, "
    + "sleep or psychology validation and no runtime rules.\n"
)
PROGRESS.write_text(
    "# Original Lilly study through printed CHAP CXLIII Dreams — 2026-10-18\n\n"
    "After authenticated publication 10,171 historical "
    "source annotations (9,105 Lilly +1,066 Ptolemy); "
    "original PDF648/894 (72.5% source page position "
    "ONLY, not scientific completion). B06w documents "
    "66 historical dream-source clauses, truth/falsehood "
    "conditions and separate dream content categories. "
    "No real dream or future-event validation or runtime "
    "rule promotions. NEXT unnumbered tenth-house honours "
    "introduction on PDF649, followed by numbered CXLIIII "
    "on same page. Chinese 46 BaZi/26 Zi Wei source notes "
    "remain separate; complete chart engines and "
    "blind humans still open.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B06w.md").read_text()
)
CURRENT.write_text(
    "# Lilly original dream source documented; tenth-house intro next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B06w historical "
    "R9040-R9105 complete, remote acceptance pending. "
    "After GitHub verification 9,105 Lilly +1,066 "
    "Ptolemy=10,171 source-only documents. "
    "No independently validated dream prediction "
    "or executable scorer; all 21 source/archive tests pass. "
    "Next UNNUMBERED tenth-house status on original PDF649; "
    "separate Chinese studies retained.\n\n---\n\n" + (BACK / "CURRENT_BEFORE_B06w.md").read_text()
)
receipt = {
    "batch": "B06w",
    "status": "GUARDED_DREAMS_SOURCE_PREPARED_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "previous_index_sha256": sha(BACK / "INDEX_BEFORE_B06w.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9105,
    "ptolemy_retained": 1066,
    "combined_if_published": 10171,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
