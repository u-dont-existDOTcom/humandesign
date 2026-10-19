# Original Lilly 1647 versus 1659 — seven unresolved direction-rate table glyphs

2026-10-19 — Africa/Dakar UTC+0. Historical primary-source critical comparison, **not** verification of natal astrological predictions or a usable numerical ephemeris.

## Source witnesses, exact edition distinction

Original first edition: William Lilly, *Christian Astrology*, 1647, Wellcome b30338724, full 894-frame PDF SHA-256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Annual-direction equatorial-rate table printed folio 711 / PDF frame745. First-edition source scan image retained byte-exact with SHA-256 `fb75055af87141aba6acda0beaa697af48767217b8f03079453fee0c0ade4feb`.

Independent *printing* of the same text: 1659 typeset second edition, Wikimedia Commons `Christian Astrology (Lilly, 1659).djvu`, DjVu page740 / printed folio711. Full source image SHA-256 `4e7d5c7601f64109e134f77b47dce237d9832370afbadaccda9691740f4f39ac`. Its publicly available page thumbnail is roughly 1280×1875 and the small or damaged digits remain unclear. No independent second human reviewer has read and certified the photographic source.

The previous B07ad first-edition source table attempted **all 372 physical sign-degree positions** but left **seven original printed readings ambiguous**. Seven source-specific reference crops from the 1659 printing were created and individually SHA-256 witnessed. Crop rectangles and full source images are retained. A contrast-adjusted or resized crop is *not* an independent witness; the independently typeset 1659 book is a second historical edition, not another person or empirical forecast.

## Seven original 1647 readings remain unresolved

| Original sign and degree | Alternative readings of **1647** | Later 1659 scan evidence |
|---|---|---|
| Virgo 1° | 55′10″ / 55′13″ | Tentative 55′10″ |
| Virgo 18° | 53′58″ / 53′59″ | Indeterminate |
| Capricorn 9° | 66′32″ / 66′39″ | Tentative 66′32″ |
| Capricorn 15° | 65′57″ / 66′02″ | Indeterminate |
| Aquarius 5° | 62′33″ / 62′35″ | Indeterminate |
| Aquarius 6° | 62′22″ / 62′24″ | Indeterminate |
| Pisces 24° | 53′43″ / 54′43″ | Indeterminate |

**No 1647 source value was filled, replaced or silently corrected.** The two later-edition observations are *one-reader tentative hints*, not established original first-edition readings. The other five second-edition glyphs remain too unclear for this scan to choose between candidates. These values are not valid inputs for production chart/time calculations.

## Recovered pre-existing B07af draft and repaired source-to-record mapping

The 2026-10-19 00:58 local worktree already contained an unfinished `build_b07af_seven_glyph_comparison.py` and companion test, so that prior working source packet was preserved and repaired instead of duplicating it. The interrupted candidate contained two defects: entries lacked their required `degree` identity and referenced image crops which straddled or did not reliably identify the requested sign column. Both are now repaired: each entry has an exact sign/degree and refers to a photo-attested crop `evidence/1659_cell_{sign}_{degree}.png` derived from the physically separate 1659 printed edition, with a checksum. Unreliable exploratory crop variants and a redundant lower-confidence five-hint experiment were discarded *before* admission. The original full source photographic page scans and prior B07ad source data were never modified.

The accepted historical index remains **12,472 Lilly** (next source R12473, printed first CLXVI of direction-time measures), plus **1,066 Ptolemy =13,538 Western** historical records; separate Chinese V3 remains **46 BaZi +96 Zi Wei =142**. Documented source spans, internal arithmetic consistency, and actual predictive accuracy are different evidence categories. Chinese source lane remains open at ZWD-R0097 and BZI-R0047.

`SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json` captures the exact original 1647 alternatives, immutable B07ad source status, separate 1659 tentative interpretations, source crop provenance/hashes and non-promotion. Targeted `test_b07af_seven_source_glyphs.py` passes **18 focused consistency, provenance and non-promotion tests**; ZIP CRC, per-file SHA/byte and independent extraction replay are required before archival batch publication.

## Next research frontier

1. Revisit the seven faint original 1647 glyphs with higher-quality independent photographic/edition witnesses or a genuinely independent reader, without converting second-edition suggestions into first-edition source facts. Compare particularly material 1647-vs-derivative conflicts and actual 1659 table values rather than only these seven ambiguous cells.
2. Audit all historical Naibod degree/minute table rows and missing printed 27-minute label, the different printed 60-minute/one-degree carry, and the source Maginus 42′/48′ versus 13′/4′ worked remainder issue corroborated across both editions in B07ae.
3. Accept historical printed CLXVI only when its full source coverage is traceable and arithmetic-method limitations are explicit; preserve second distinct printed CLXVI for annual profections. Separately build reliable original-era astronomical engine and preregister prospective blind-human chart predictions with non-astrology baselines.
4. Continue primary Chinese Zi Wei from ZWD-R0097 and BaZi from BZI-R0047. No actual real-person predictive success or runtime model promotions are established.
