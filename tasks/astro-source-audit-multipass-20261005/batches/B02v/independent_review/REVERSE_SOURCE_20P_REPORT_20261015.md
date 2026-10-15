# Original-text reverse mapping: all 20 Chapter L source pages

**2026-10-15 — HumanDesign / Lilly B02v. Status: PROVISIONAL, source-only, not accepted.**

## Original authority

William Lilly, *Christian Astrology* (1647), Wellcome b30338724, source PDF SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. B02v begins original PDF381/printed347 below `Of the house of the Thiefe, and the mark thereof` and ends PDF400/printed366 above the divider before Chapter LI. Prior B02u acceptance ends R2572. There are 2,572 previously accepted Lilly documentary units and 1,066 retained Ptolemy source units. **No new B02v source record has been accepted.**

## New reverse audit performed

The remaining six original images PDF394–399 (printed360–365) were visually read, and their printed headings, historical condition branches, alternatives, exceptions, and outcome statements were mapped to the already-existing 130 candidate records R2816–R2945, with one machine-readable page map per image:

| Original PDF | Printed page | Candidate IDs | Map |
| --- | --- | --- | --- |
| 394 | 360 | R2816–R2836 (21) | `REVERSE_SOURCE_TO_RECORD_P394_20261015.json` |
| 395 | 361 | R2837–R2857 (21) | `REVERSE_SOURCE_TO_RECORD_P395_20261015.json` |
| 396 | 362 | R2858–R2878 (21) | `REVERSE_SOURCE_TO_RECORD_P396_20261015.json` |
| 397 | 363 | R2879–R2901 (23) | `REVERSE_SOURCE_TO_RECORD_P397_20261015.json` |
| 398 | 364 | R2902–R2922 (21) | `REVERSE_SOURCE_TO_RECORD_P398_20261015.json` |
| 399 | 365 | R2923–R2945 (23) | `REVERSE_SOURCE_TO_RECORD_P399_20261015.json` |

These entries preserve historical logic and prior corrections: printed360 `truth is said of him` remains a literal unresolved referent; printed361 Part of Fortune, signs and plurality stay separate; printed362 age and stature use their respective OR/AND operators; printed363 has plural significators and unresolved aspect actor; printed364's 12-house direction table remains separate from printed365's two 12-sign direction tables; printed365's capture conditions are not overwritten by similar but distinct conditions on printed366.

**No new definite source-to-record omission or correction was admitted on these six pages at this bounded review level.** The original p360/l4 same-volume erratum still has an unresolved glyph replacement and is not conjecturally emended.

## Verified mechanical union across all 20 pages

`build_reverse_coverage_20p_20261015.py` constructed `independent_review/REVERSE_SOURCE_COVERAGE_20P_20261015.json` from the original-first page maps. It independently recomputed SHA256 for each source image and its mapping file, confirmed every mapped record ID cites that source page, and verified:

- 20/20 original PDF pages represented, PDF381–400 inclusive.
- **419 normalized editorial source anchors** in those page maps, collectively referencing **402 distinct provisional candidate IDs** R2573–R2974.
- 413 *distinct record/page appearances*; 11 IDs appear on two physical pages and are counted only once in the 402.
- **Zero candidate IDs missing from the reverse page-map union**.
- The source inventory, accepted count, and all 74 recorded textual issues remain unchanged. The source-only map test `test_reverse_20p_20261015.py` passed 6/6.

Exact machine map-manifest SHA256: `6c23f37013db7ce80991eb4329233e0277cd90e2045046147bff35c80b2dd18c`.

## What this does and does not prove

The 419 anchors are **editorially normalized summaries**, not 419 diplomatic quotations, and a single anchor can represent an original table with 12 rows. The same ChatGPT working context that edited the draft performed these mappings; it is **not** a separate independent or blind reviewer. Showing that each of 402 *existing records* has an original-page reverse anchor does **not** prove there were no additional original clauses never given a record. No predictive power, human identification, guilt, physical trait, property recovery, or historical outcome has been scientifically verified.

The original printed p360 line4 erratum remains ambiguous; several other source grammatical distinctions are intentionally retained in U01–U74 rather than fixed by speculation. No source-only canonical count is advanced, and Chapter LI (below PDF400 divider) is not included.

## Next authorized frontier

1. Publish these six maps, 20-page coverage manifest, test and this report on the **provisional HumanDesign research branch**; keep the original PDF images and all old snapshots intact.
2. A small optional review-companion ZIP builder was drafted, but execution was blocked by the laptop tool's safety checks; **no new companion ZIP or its verification receipt is claimed**. The review report itself was delivered directly to Downloads and matched byte-for-byte. Continue source-first **line-to-record omission testing** on high-risk multi-branch paragraphs and tables, ideally with a genuinely separate image reader only if it materially resolves a source question; preserve uncertainty honestly.
3. Decide/document the warranted source-only acceptance standard when actual original-clause completeness is adequately evidenced, rather than treating an assistant-added perfect-independence requirement as a permanent blocker. The parent aim is completing the historical astrology corpus, not just improving a pipeline.
4. Only then advance the accepted Lilly index with a new verified acceptance artifact, and start Chapter LI on original PDF400 **below** the divider. Keep empirical astrology validation a separate frozen lane.

**State: SOURCE_REVERSE_PAGE_COVERAGE_COMPLETE / SOURCE_TEXT_COMPLETENESS_NOT_CERTIFIED / B02v UNACCEPTED.**
