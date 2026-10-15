# Lilly Chapter L — source-only acceptance readiness comparison
**2026-10-15 | Evidence-led assessment, not a new acceptance gate.**

## Owner outcome and boundaries
The owner wants a source-complete original-book audit across multiple astrology authors so important historical methods are not discovered after examining outcomes. This lane only inventories William Lilly's original historical text. **No criminal allegation, person-level observation, forecast, model weight, or scientific evidence of astrology is accepted.** The parent multi-author study is OPEN.

The 1647 Wellcome original `b30338724` SHA256 is `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. B02v is PDF381 below *Of the house of the Thiefe, and the mark thereof* through PDF400 above the Chapter LI divider. The canonical accepted index still stops at **R2572 (2,572 Lilly + 1,066 retained Ptolemy = 3,638)**. B02v proposes **402 units, R2573–R2974**, not yet accepted. If all source units are admitted unchanged, those future arithmetic totals would be Lilly 2,974 and combined 4,040.

## Verified positive source evidence
- Original page-image witness and hashed manifest: 20 B02v original content pages, plus errata PDF888. Pixel replay evidence is in `SOURCE_REPLAY_RECEIPT.json`.
- The seven producer source components reassemble into 402 consecutive candidate IDs. Exactly 49 editorial section markers, 350 historical conditional/example units and three printed tables are distinguished; the 36 table rows were separately collated at a normalized row/direction level.
- `SOURCE_ORDER_DRAFT.json` accounts for **11 dual-page locator references**: nine actual printed sentence continuations and two contextual adjacent-page citations.
- `independent_review/REVERSE_SOURCE_COVERAGE_20P_20261015.json` maps **419 editorial source anchors on all 20 original pages** to **all 402 existing candidate IDs**, with 11 record IDs occurring on two page images; source and mapping hashes and page references were checked.
- `test_reverse_20p_20261015.py` passed **6/6** on published source. Existing latest `independent_review/PROVISIONAL_SOURCE_PACKET_RECEIPT_v10_20261015.json` attests CRC, every archived SHA256, real extraction, and **88/88 source-only tests on extracted bytes**.
- The latest source ledger `UNRESOLVED_DRAFT.json` records **74** textual corrections or uncertainties. These are not 74 uncorrected defects: most are durable correction receipts, while genuine original ambiguities remain explicitly retained.

## What this evidence does NOT establish
A source-first editorial map can only demonstrate that the 402 *existing* units have image anchors. It does **not** mathematically prove no additional original sentence was omitted. The same working model context authored most maps, so these are not independent blind readings or word-for-word diplomatic transcriptions. The 1647 printed p360/l4 errata glyph cannot yet be assigned an exact textual replacement with sufficient confidence. It is explicitly preserved on **R2819**, U22 and `ERRATA_COLLATION.json`; no guessed symbol repair is licensed. Other historically ambiguous wording (e.g. R2735 bidirectional application, R2829–2830 truth referent, R2901 aspect actor) must remain marked unresolved rather than converted into firm mechanical conditions.

**Secondary text warning:** A modern keyed Book II transcript (`https://www.astrologiahumana.com/WilliamLilly-ChristianAstrology-BookII.pdf`) does not reliably preserve all original 1647 content. At printed p360, it omits the **sixth** house from an original second/sixth/seventh-house list and omits the **square** aspect in one original Moon list. Use it for navigation only, not for authoritative glyph or missing-clause adjudication. The Wellcome original images are controlling.

## Precedent and proportional acceptance threshold
The preceding **B02u** batch was accepted as documentary-only with 267 new source units, **119 retained textual uncertainties**, five first image-review windows, no post-controller final blind review, and some printed table cells not diplomatically accepted (`../B02u/ACCEPTANCE.json`, `../B02u/PUBLICATION_RECEIPT.json`). Accordingly, a *new* requirement for a perfectly independent complete second transcription or for eliminating every ambiguous glyph before accepting B02v would be an assistant-added stricter gate, not a precedent requirement. Conversely, **passing tests and matching all existing IDs alone is insufficient** to establish the owner's source-completeness aim.

## Decision-oriented next actions
1. Carry out **one finite source-first omission check on the material high-risk paragraphs**—original p355 recoveries, p357–360 conditional allegations, p365–366 captures and the original three direction tables. Look from ORIGINAL image passages for unrepresented source clauses and missing OR/AND, applications, sign positions, heading scope and marginal restrictions. Do not merely regenerate the existing 402 IDs.
2. Treat p360 erratum as retained unknown if an exact original source or genuinely different image/edition comparison cannot resolve it. Do **not** loop indefinitely on the same crop/OCR or silently emend it.
3. If no material source paragraph remains missing, prepare a documentary-only **B02v acceptance candidate** analogous to B02u with exact original scope, 402 numbered units, frozen issues, clear exceptions, verification and non-empirical status. Require an explicit readiness disposition supported by source evidence—not an extra model review solely for ceremony. Publish/merge non-force and verify canonical index only after that acceptance step genuinely succeeds.
4. After documentary admission, continue at original PDF400 **below** Chapter LI divider. The parent study remains OPEN for later Lilly and other authors. Keep all empirical/predictive work frozen and separate.

**Current disposition:** `SOURCE_BOUNDARY_AND_CANDIDATE_MAPPING_VERIFIED; DOCUMENTARY_SOURCE_ADMISSION_NOT_YET_DECIDED`. No new fail-closed control introduced.
