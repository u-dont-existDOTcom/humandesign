# B02v source-image review progress — 2026-10-14 (UTC+0)

**Status: PARTIAL, UNACCEPTED.** Parent multi-author astrology text study remains OPEN. This note describes source fidelity, not claims about genuine theft, suspects, identities, places, or predictive validity. Source-only tests do not certify documentary completeness.

## Baseline and scope

Accepted predecessor: B02u, R2572, 2,572 Lilly plus 1,066 Ptolemy = 3,638 documentary units. New B02v source scope: original 1647 William Lilly PDF381/printed347 **below** `Of the house of the Thiefe, and the mark thereof` through PDF400/printed366 **above** Chapter LI divider. Exactly 20 original-page images (PDF381–400) plus same-volume errata PDF888 are locally preserved. Scan declared SHA256: `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. The existing independent original-to-raster RGB replay receipt is separate from semantic review.

402 producer draft units in seven page components, candidate R2573–R2974, were already present locally. 402 units remain **provisional**; none accepted. Candidate totals 2,974 Lilly/4,040 combined must not be reported as accepted.

## Actual source-image work in this continuation

Read the original page images at PDF381, 382, 383, 384, 385, 394, 398, 399 and 400 and original errata PDF888; compare the source text's relevant headings, glyphs, conjunctive/disjunctive clauses, table cells and page boundaries with the producer paraphrases. The original scan is authoritative. This is a **partial image-first review and selective source-to-record collation**, not a completed full 402-record review, not a separately instantiated blinded evaluator, and not an original historical incident check.

Four confirmed material corrections:
1. **PDF381/printed347 — proposed R2576.** House marker is printed Sun `☉`, not unspecified “fortune-like glyph”; Moon `☽` separately indicates the door. Local producer kind changed to `sun_as_thief_house_marker`. Original producer bytes retained under `recovery/producer_p381_384_before_20261014_sun_review.json`; SHA256 `0157b9b0c1855f49cf24f462b9aac1f9e613548bb41211911e3911df350dfd5a`.
2. **PDF381/printed347 — proposed R2577.** The oriental-sign condition concerns Sun `☉`, not a fortune-like point. Corrected kind `sun_oriental_house_east` with explicit subject.
3. **PDF394/printed360 — proposed R2819.** Source prints Sun in **conjunction, square OR opposition** to thief significator; producer omitted conjunction. Corrected kind `sun_conjunction_square_opposition_thief_known`. The same-volume printed erratum p360/l4 is related, but no uncertain additional glyph emendment was made.
4. **PDF394/printed360 — proposed R2832.** Original words are “second, sixt or seventh”; `sixt` means **sixth**, not first. Corrected kind `owner_self_second_sixth_seventh`. Before-correction SHA256 of the producer PDF393–395 component: `176c99f0c9c36309ae6b311a4d2510c3819bd58484bf7f0e64ad895aed4b6561`; original frozen in `recovery/producer_p393_395_before_20261014_p360_review.json`.

Visually located the erratum's likely body passage on PDF394 under “Whether the Thief shall be knowne or not,” setting `ERRATA_COLLATION.json` `body_line_located=true` while **retaining `read_word_or_glyph_verified=false`** until the exact erratum-body replacement is reconciled. Original PDF398/printed364 house-direction table has twelve printed house rows. PDF399/printed365 contains two distinct twelve-sign direction tables; their different source-defined directions remain distinct, not retrospectively harmonized. The original PDF400 horizontal rule separates the last Chapter L clauses from the first Chapter LI passage. No Chapter LI body was admitted.

## Local source-only engineering performed

- Two source draft JSONs corrected, with exact original bytes frozen first. Five remaining producer source components preserved, not re-extracted.
- `assemble_source_draft.py` rerun successfully after corrections; `RULES_DRAFT.json`, `COUNTS.json`, and `SECTION_COVERAGE_DRAFT.json` rebuilt from all seven source components. Candidate count still 402, no canonical change.
- Existing `test_b02v_staging.py` initially failed 1 assertion/2 missing-schema keys against newly assembled candidate metadata. The three stale expectations were aligned to the current UNACCEPTED schema and evidence state, with original test SHA256 `debf23618cd0460ae5a65bbaf9e0dc1f37c37845a23a324b8f56c8b174c88e88` preserved in `recovery/test_b02v_staging_before_20261014_schema_align.py`.
- `python3 test_b02v_staging.py`: **18/18** source-provenance staging checks PASS (after schema alignment).
- `python3 independent_review/test_reconciled_draft.py`: **11/11** focused checks PASS.
- Pending source uncertainties now **46** including a corrected “sixt” misreading. Neither suite performs independent line-by-line full-source adjudication, original empirical validation, release acceptance, archive extract/replay, or owner-machine delivery.

## Exact remaining gate

Source review of all PDF381–400 text against all 402 draft claims **remains incomplete**; independently and comprehensively validate the house/zodiac tables, cross-page conditions, nearby headings, planet/sign aspect operators, and printed p360/l4 erratum. Preserve all confirmed differences and original files. Then run source-bound integration/regression/claim-ledger validation, build a manifest-hashed ZIP, actually extract and replay source tests, nonforce publish to source and canonical research branches with remote readback, and verify OS Downloads delivery hashes. Only then change accepted record count, announce full Chapter L source-read completion, and proceed Chapter LI below PDF400 divider. No user decision is outstanding.
