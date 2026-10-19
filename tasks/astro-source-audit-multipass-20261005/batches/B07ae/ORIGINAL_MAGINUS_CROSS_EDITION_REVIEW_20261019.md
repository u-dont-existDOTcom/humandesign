# Lilly's 1647 Maginus worked-example arithmetic: actual 1659 independent printing

2026-10-19, Africa/Dakar UTC+0. This is a strictly historical literary and **exact-arithmetic** check of William Lilly's *Christian Astrology* (first edition 1647; independently typeset second edition 1659). It does not validate astrology's predictive accuracy, modern birth-time or star positions, health/mortality, or social-personality claims.

## Distinct first and second edition source images

First-edition 1647 Wellcome original b30338724 full 894-frame PDF SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Original first-edition printed folio712 (PDF frame746) was newly rendered using Poppler scale-to-3200, image SHA256 `a3a4955f3fa0ff446d95a730857f4add250ca876604289985fbaa9d30d813986` and stored `evidence/first_edition_1647_printed712_pdf746.jpg`.

A **genuinely separate 1659 typeset printed edition** was accessed through Wikimedia Commons `File:Christian Astrology (Lilly, 1659).djvu`. Original facsimile leaves preserved in this batch:

- 1659 printed folio709 / DjVu page738, Ptolemy example and Maginus introduction; SHA256 `55509e5690b849096d2a87bad2b79c30997ee5ce5c386b6e71aa05ea7e251918`.
- 1659 printed folio710 / DjVu page739, Maginus solar right-ascension source passage; SHA256 `6d10cc1de22a6e05f1dd43fee2f5db4bd6463e7d0be146a23418bf114a0d5`.
- 1659 printed folio712 / DjVu page741, same two original Maginus numeric worked examples; SHA256 `ee4fbe098258b57439cae727e2ac34eea9b703addb6d75a24d8494c2fffe2579`.

These are independent *printed witnesses to the same historical text*, not a second human researcher or an independent prospective prediction cohort.

## Reproduced historic numerical inconsistency

Lilly's example uses a simplified annual equatorial arc of **54 arcminutes per nominal year**. A separate direction-rate zodiac table on printed711 contains **54′25″** for Libra7°; do not silently replace the example's 54′ by that greater-precision rate.

| Worked instance | Target angular arc | Printed complete years + attained arc | Remaining by exact subtraction | Printed remainder used | Printed fractional year result |
|---|---|---|---|---|---|
| Ascendant → Mars terms | 11°55′ | 13 years, 11°42′ | **13′** | **42′** | 284 days |
| Ascendant → Mars opposition | 19°52′ | 22 years, 19°48′ | **4′** | **48′** | 324 days |

The first and second edition pages both actually print the numbers 42 and 48 in the fractional calculation. These appear to be the *arcminute parts of the already accumulated arcs* (11°42′ and 19°48′), not the actual remainder to the stated targets. Keeping Lilly's 54′/365-nominal-days rate, using the printed amounts versus the mathematical remainder changes the partial-year contribution by **10585/54 days ≈196.02 days** for the Mars-terms example, and **8030/27 days ≈297.41 days** for Mars opposition. The printed day values are internally compatible (within rounding to a day) with 42′ and 48′ respectively; the *target subtraction* appears inconsistent.

**Epistemic status:** an independently typeset 1659 second edition repeats the original 1647 worked-example numbers; this supports a persistent transmitted arithmetic discrepancy rather than a one-off modern OCR fault. It does *not* conclusively establish author-versus-compositor cause, specify a corrected natal forecast algorithm, or validate any real-world timing. Historic source words/inputs, arithmetic reconstruction and human empirical outcomes must remain separate.

## Relation to other open source work

The Ptolemy historical arc-to-age example with a 360-day annual approximation and the Naibod historical 365-day lookup worked cases remain distinct from Maginus's 54′ rate. Full 1647 paper annual-rate table source **372 of372 positions visually attempted by one reader: 365 legible, seven unresolved**, in B07ad. The original Naibod tables have **90 historical degree rows and 59 visibly numbered minute rows**, with a missing original row label27 and persistent printed discrepancies; those are not corrected by this Maginus finding. Original CLXVI directions-time chapter begins PDF742; a *second different chapter also printed CLXVI* on annual profections begins PDF749, original printed numeral duplicated.

**Historical accepted index unchanged:** 12,472 Lilly +1,066 Ptolemy=13,538 Western source annotations; parallel Chinese V3=142 (46 BaZi+96 Zi Wei). Next not-yet-accepted Lilly historical source entry R12473. No runtime astrological model promotion and **zero independently validated actual human forecasts**.

Source machine record `MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json` uses exact rational arithmetic, explicitly labels source photographs, printed numbers, target subtraction and nominal day deltas. `test_b07ae_maginus_editions.py` verifies original image SHA, old index stability, bounded input, original printed case numbers, exact target/residual computation, dates and no-promotion flags; suite **26 focused tests**, independently extracted archive replay required before asserting source batch acceptance.

Next source-critical task: compare original 1647/1659 printing on all seven unresolved annual-rate glyphs and printed anomalies, with independent source review where meaningful, while preserving original source. Complete Naibod numbers, the full CLXVI reversible source map and precise astronomical/chart-time mechanics. Continue original Zi Wei ZWD-R0097 and BaZi BZI-R0047 lanes and after model freeze consider blinded human prospective testing against decoys and failures.
