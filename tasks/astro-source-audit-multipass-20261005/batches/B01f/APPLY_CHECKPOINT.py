#!/usr/bin/env python3
"""Advance only this source-audit checkpoint from a pinned predecessor.

No source runtime, prior batch, candidate model, or participant file is modified.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
BASE = "3fcaf407adb1807ae8db3cd5ffa683867aa7d80c"
BRANCH = "research/astro-source-audit-b01f-20261006"

def load(path: Path):
    return json.loads(path.read_text())

def put(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def main():
    assert git("branch", "--show-current") == BRANCH
    assert git("rev-parse", "HEAD") == BASE
    current = load(TASK / "CURRENT_PASS.json")
    assert current["counts"]["ptolemy_read_sections"] == 29
    assert current["counts"]["source_records"] == 164
    f = load(TASK / "batches/B01f/RULES.json")
    g = load(TASK / "batches/B01g/RULES.json")
    assert f["records_count"] == 29 and len(f["records"]) == 29
    assert g["records_count"] == 34 and len(g["records"]) == 34
    records = f["records"] + g["records"]
    chapters = {
        6: ("B01f", [279,281]), 7: ("B01f", [281,283,285]),
        8: ("B01f", [285,287,289]), 9: ("B01f", [289,291,293,295]),
        10: ("B01g", list(range(295,332,2))),
    }
    discovery = load(TASK / "SECTION_DISCOVERY.json")
    for row in discovery["sections"]:
        if row["book"] == "III" and row["chapter"] in chapters:
            assert row["status"] == "INDEXED_NOT_READ"
            batch,pages = chapters[row["chapter"]]
            ids = [r["id"] for r in records
                   if r["source_locator"]["chapter_or_verse"] == f"III.{row['chapter']}"]
            assert ids
            row.update(status="READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE",
                       locator_status="ENGLISH_SPANS_VERIFIED",rule_ids=ids,
                       english_pdf_pages=pages, source_batch=batch)
    read = sum(x["status"] == "READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE"
               for x in discovery["sections"])
    assert read == 34
    discovery["read_sections_count"] = read
    discovery["indexed_unread_count"] = 61 - read
    discovery["body_locators_warning"] = (
        "English Book I and III.1-III.10 spans verified. III.11 and III.13 "
        "boundary headings located, not counted as chapter reading. "
        "Book II, III.11-III.14 and Book IV remain unaudited.")
    put(TASK / "SECTION_DISCOVERY.json", discovery)
    next_range = ("III.11-III.12; start III.11 on English PDF331/printed307; "
                  "stop before III.13 on shared PDF357/printed333")
    c = current["counts"]
    c.update(ptolemy_read_sections=34,ptolemy_unread_sections=27,source_records=227,
             isolated_definition_tests=147,ptolemy_book_III_read_sections=10)
    current.update(
        completed="Source intake; Ptolemy English I.1-I.24 and III.1-III.10; prior Rhetorius witness/OCR qualifications retained",
        current="B01f/B01g complete: birth chapters and complete III.10 source audit with bounded directional arithmetic; parent corpus audit OPEN",
        next_batch="B01h",next_range=next_range,
        next_actor="Next authorized source-audit continuation; no new upload needed",
        last_verified_unit="III.10 closing paragraph on English PDF331/printed307 before III.11",
        source_rule_records=227, no_background_run=True,
        counting_note="227 source records; 95 earlier separate star groups; four earlier Rhetorius comparisons; none is an independent prediction or validation trial.",
        latest_reports=["batches/B01f/REPORT.md","batches/B01f/VERIFICATION.json"],
    )
    current["stop_admission"] = {
        "parent_status":"OPEN",
        "remaining_gap":"Remaining readable source chapters; full cross-author reconciliation; later compilation and evaluation.",
        "next_action":next_range,
        "authority":"Owner-approved multi-pass source audit and this continuation.",
        "executed_this_increment":"Read III.6-III.9 and continued through all III.10;63 records and39 new bounded checks.",
        "delivery_boundary":"Completed source-reading increment under the existing multi-pass pause contract; parent is not completed and no background work is claimed.",
    }
    put(TASK / "CURRENT_PASS.json", current)
    plan = load(TASK / "PASS_PLAN.json")
    states = {
        "P2":"PTOLEMY_61_INDEXED;ENGLISH_I24_AND_III10_READ_MAPPED",
        "P3":"ENGLISH_I_COMPLETE_AND_III1_III10;227_SOURCE_RECORDS;REMAINDER_OPEN",
        "P4":"147_SOURCE_REFERENCE_AND_INTEGRITY_CHECKS;FOUR_PRIOR_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING",
    }
    for row in plan["passes"]:
        if row["id"] in states: row["status"] = states[row["id"]]
    batch = next(x for x in plan["batches"] if x["id"] == "B01")
    assert not any(x["id"] in {"B01f","B01g"} for x in batch["completed_subbatches"])
    batch["next"] = next_range
    batch["completed_subbatches"].extend([
        {"id":"B01f","scope":"English III.6-III.9 and identified notes; historical source-only birth doctrines",
         "source_records":29,"new_predictions":0,"tests":0,"test_scope":"Shared39-check suite is counted under B01g."},
        {"id":"B01g","scope":"Full English III.10; Fortune convention, conditional prorogation and worked numerical examples",
         "source_records":34,"new_predictions":0,"tests":39,
         "test_scope":"Source-reference arithmetic and B01f/B01g integrity; not a complete directions engine."},
    ])
    put(TASK / "PASS_PLAN.json", plan)
    (ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md").write_text("""# Current astrology source audit

**Parent OPEN: owner-authorized multi-pass source audit.** English Ptolemy Book I (24/24) and III.1-III.10 are read/extracted. No personal predictions, fitted-model changes or runtime promotion.

## Canonical recovery
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json` — exact next section/counts.
- `tasks/astro-source-audit-multipass-20261005/PASS_PLAN.json` — five passes and all source tracks.
- `tasks/astro-source-audit-multipass-20261005/SECTION_DISCOVERY.json` — 61 Ptolemy sections:34 read,27 unread.
- `tasks/astro-source-audit-multipass-20261005/batches/B01f/REPORT.md` — integrated B01f/B01g report.
- `tasks/astro-source-audit-multipass-20261005/batches/B01f/VERIFICATION.json` — actual integration tests and source/protected-content verification.
- Task `batches/B01f/RULES.json`, `BIRTH_DOCTRINE_TABLES.json`, `READING_RECEIPT.json`, `UNRESOLVED_INTERPRETATIONS.json` — historical birth doctrines.
- Task `batches/B01g/RULES.json`, `DIRECTION_REFERENCE.json`, `ARITHMETIC_REPLAY.json`, `READING_RECEIPT.json`, `UNRESOLVED_INTERPRETATIONS.json` — full III.10 source audit and bounded arithmetic.
- `tasks/astro-source-audit-multipass-20261005/RHETORIUS_OCR_RECHECK_20261006.json` — controlling copy-specific qualification; original witness/supplement receipts preserved.

## Completed; do not repeat
B01/B01b/B01c/B01d/B01e/B01f/B01g contain24+32+53+27+28+29+34=227 source records.95 earlier fixed-star groups are separate. Egyptian/Ptolemaic terms have120 directly transcribed cells and the Chaldean reconstruction120 computed cells. Four earlier Rhetorius comparisons are not a full Rhetorius audit.147 source-reference/integrity checks plus34 methodology checks are expected; the latest verification records the actual run. None measures predictive validity.

Owner Rhetorius OCR remains the private search aid. Images govern ambiguous numbers and continuity; an unreadable footer is not missing content. The replacement is198 physical PDF pages despite the150-page preview. The23-gap count concerns the inspected copy plus six-page supplement. The owner acknowledges the gaps: do not reopen that debate or demand another upload. Available material remains usable. BPHS remains Sharma; Primary Directions remains an excerpt/interview; unavailable books do not block other tracks.

## Next executable batch
**B01h: English III.11-III.12.** Start at III.11 heading onPDF331/printed307; end beforeIII.13 onPDF357/printed333. Headings verified, chapters not yet audited. Preserve historical physical/medical descriptions as source material, not diagnoses. BookII's13 mundane/general chapters remain deferred; BookIV is unread.

## New source implementation cautions
III.6-III.9 retain multifactor preconditions, subject changes, non-sufficient adverse patterns and rescue/rearing alternatives. No modern identity/medical classifier is admitted. Cardanus's latitude explanation of the isosceles opposition is commentary, not an undisputed Ptolemaic definition.

III.10 separates spatial eligibility, significator selection, direction method, encounter timing and outcome. Adopted Robbins main text uses Fortune=(ASC+Moon-Sun)mod360 both by day and night; other transmitted wording remains separately identified. Equal60-degree ecliptic intervals yield rounded46/58/70/64 equinoctial times at different temporal positions. Ordinary hours are seasonal. The exact PDF321 note reads147;44, not OCR147;14; finer-note replay gives45;05 and70;23, kept apart from rounded main examples. Interpolation is explicitly approximate. Jupiter12/Venus8 are conditional following-ray limits, not generic aspect orbs. Latitude mismatch concerns bodily encounters. Under-beams exclusion affects help and harm. III.10's final past-event candidate selection is development, not independent validation. IV.10 ingress/time-division dependencies remain pending.

## Earlier cautions retained
Topical place precedes ruler selection. III.2 has five forms with phase OR aspect one category. Rectification lacks resolved epoch/closeness/inversion conventions. Quality, magnitude and general timing are distinct. Equally strong rulers can blend or act successively. No original familiarity means no great influence, not literally no effect. Weak positive longevity testimony does not establish its opposite. Sibling locus remains textually ambiguous; do not replace with a generic third house. Rejection of unexplained Lots is qualified by Fortune usage. Terms tables have equal totals but differ on153/360degrees. Chaldean rotation keeps Saturn/Mercury together. Ptolemy rejects twelfth-parts whereas Rhetorius adopts them. Triplicities, proper face and chariots remain author-specific. Greek/apparatus collation and unspecified numerical conventions remain open.

Raw books, full text and source images stay outside Git. Preserve all prior batches, personal freezes and retained astrology/numerology candidates. This is source audit, not independent personal blinding. No unattended process is promised after delivery; resume the first unfinished unit.
""")
    print("CHECKPOINT_UPDATED:34/61 sections;227 records;B01h next")

if __name__ == "__main__":
    main()
