"""Apply this source-reading checkpoint to the known predecessor, without model edits."""
from pathlib import Path
import json

B = Path(__file__).resolve().parent
T = B.parents[1]
ROOT = T.parents[1]


def load(p):
    return json.loads(p.read_text())


def write(p, obj):
    p.write_text(json.dumps(obj, indent=2) + "\n")


def main():
    records = load(B / "RULES.json")["records"]
    section = load(T / "SECTION_DISCOVERY.json")
    spans = load(B / "READING_RECEIPT.json")["chapter_spans"]
    for row in section["sections"]:
        if row["book"] == "I" and 17 <= row["chapter"] <= 24:
            key = f"I.{row['chapter']}"
            row.update({"status": "READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE", "locator_status": "ENGLISH_SPANS_VERIFIED", "english_pdf_pages": spans[key]["english_pdf_pages"], "rule_ids": [r["id"] for r in records if r["source_locator"]["chapter_or_verse"] == key]})
    section["read_sections_count"] = sum(r["status"] == "READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE" for r in section["sections"])
    section["indexed_unread_count"] = sum(r["status"] == "INDEXED_NOT_READ" for r in section["sections"])
    assert section["read_sections_count"] == 24 and section["indexed_unread_count"] == 37
    section["body_locators_warning"] = "English Book I spans verified; all later sections remain unread. III.1 start heading checked at PDF245; table of contents locators alone are not reading."
    write(T / "SECTION_DISCOVERY.json", section)
    c = load(T / "CURRENT_PASS.json")
    c.update({"completed": "Source intake; Ptolemy English I.1-I.24; owner Rhetorius OCR incorporated and disputed continuity checked", "current": "B01c complete: English Book I foundation; wider corpus audit OPEN", "next_batch": "B01d", "next_source": "PTOLEMY1940_REPRINT1964", "next_range": "III.1-III.3, English PDF245/printed221 through end III.3 before III.4 on shared PDF265/printed241", "last_verified_unit": "I.24 end on PDF141/printed117 immediately before BOOK II", "source_rule_records": 109, "person_predictions_added": 0, "rhetorius_ocr_recheck": "RHETORIUS_OCR_RECHECK_20261006.json", "no_background_run": True, "next_actor": "Next authorized source-audit continuation, no request to re-upload books required", "counting_note": "13 current Drive files plus one owner OCR reading aid; 109 Ptolemy source records, 95 separate fixed-star groups, four targeted cross-source comparisons. None is an independent validation trial."})
    c["counts"].update({"ptolemy_read_sections": 24, "ptolemy_unread_sections": 37, "source_records": 109, "isolated_definition_tests": 85, "owner_ocr_reading_aids": 1, "ptolemy_english_foundation_books_completed": 1, "targeted_cross_source_comparisons": 4, "terms_table_cells_directly_transcribed": 120, "chaldean_cells_computed": 120})
    c["rhetorius_coverage_claim_scope"] = "Exact inspected PDF and supplement, not every copy. New OCR has text on pages with unrecognized footer labels; independently rechecked copy-specific discontinuities remain. See latest recheck."
    write(T / "CURRENT_PASS.json", c)
    p = load(T / "PASS_PLAN.json")
    p["passes"][1]["status"] = "PTOLEMY_61_INDEXED; ALL24_BOOK_I_ENGLISH_SECTIONS_READ_MAPPED"
    p["passes"][2]["status"] = "BOOK_I_COMPLETE_109_SOURCE_RECORDS; OTHER_PTOLEMY_BOOKS_UNREAD"
    p["passes"][3]["status"] = "85_SOURCE_DEFINITION_TESTS; FOUR_TARGETED_RHETORIUS_COMPARISONS; FULL_RECONCILIATION_PENDING"
    batch = next(b for b in p["batches"] if b["id"] == "B01")
    batch["next"] = c["next_range"]
    if not any(b["id"] == "B01c" for b in batch["completed_subbatches"]):
        batch["completed_subbatches"].append({"id": "B01c", "scope": "English I17-I24 and bounded notes; targeted Rhetorius comparisons", "source_records": 53, "new_predictions": 0, "tests": 36})
    write(T / "PASS_PLAN.json", p)
    state = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
    state.write_text('''# Current astrology source audit

**Parent OPEN: owner-authorized multi-pass source audit.** English Ptolemy Book I, all 24 chapters, has now been read/extracted. No person predictions or runtime-model promotion.

## Canonical recovery
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json` — current counts and exact next section.
- `tasks/astro-source-audit-multipass-20261005/PASS_PLAN.json` — source tracks and five passes.
- `tasks/astro-source-audit-multipass-20261005/SECTION_DISCOVERY.json` — 61 Ptolemy sections: 24 read, 37 unread.
- `tasks/astro-source-audit-multipass-20261005/batches/B01c/REPORT.md` — newest result and limitations.
- `tasks/astro-source-audit-multipass-20261005/batches/B01c/RULES.json`, `TERMS_TABLES.json`, `DIGNITY_DEFINITIONS.json`, `READING_RECEIPT.json`, `BOUNDED_RHETORIUS_COMPARISON.json` — exact current evidence.
- `tasks/astro-source-audit-multipass-20261005/RHETORIUS_OCR_RECHECK_20261006.json` — controlling qualification following the owner's OCR upload; read with the original intake and replacement/supplement receipts.

## Completed, do not repeat
Ptolemy B01/B01b/B01c contain 24 + 32 + 53 = 109 source records. The earlier 95 descriptive fixed-star groups remain separate. Two adopted term tables have 120 visually transcribed cells; the Chaldean day/night construction adds 120 computed cells. These are not independent predictions. There are 85 source-definition tests plus 34 prior methodology tests.

Owner OCR `RHETORIUS_HOLDEN_OWNER_OCR_20261006.txt` was hash-matched and saved beside the private books. It is the searchable prose aid; images govern ambiguous numbers, tables, and continuity checks. Never equate an unrecognized OCR footer with missing content. The exact current PDF has 198 pages, despite a 150-page preview surface. Rechecked physical transitions include printed103 to105 and112 to114 and occur in the owner OCR too. The prior 23-gap list is copy-specific, not a claim about every copy or a new complete text collation. The six-page supplement and old preview remain preserved. Reading available material does not wait for another upload.

BPHS remains the Sharma edition. Primary Directions remains an excerpt/interview. Other unavailable books do not block this source track.

## Next executable batch
**B01d: Ptolemy III.1–III.3.** Start English PDF245/printed221; read through the end of III.3 before III.4 on shared PDF265/printed241. This follows the existing plan to cover natal III/IV after foundation I. The 13 BookII mundane/general chapters remain explicitly deferred to their own pass, not forgotten. No later chapter is counted read merely because its heading was inspected.

## New implementation cautions
Egyptian/Ptolemaic term tables share global totals but differ across153/360degrees: aggregate checksum alone cannot certify a table. Chaldean rotations must keep Saturn/Mercury in a single sect-ordered group. Ptolemy reports then rejects finer twelfth-parts while Rhetorius adopts them. Triplicity roles, proper face and chariots differ by author/interpretation. Do not merge conventions without a versioned decision. Complete Greek/Latin apparatus collation, numerical angular thresholds, some term-generation details and latitude equality/zero cases remain open.

Raw books/OCR/full text stay outside Git. Preserve source/commentary/project layers and old candidate/model freezes. This is source audit, not a clean-room person experiment. No background process is running; the next authorized pass resumes the exact checkpoint.
''')
    print("CHECKPOINT: BookI24/24;Ptolemy24/61;109records;ownerOCRregistered")


if __name__ == "__main__":
    main()
