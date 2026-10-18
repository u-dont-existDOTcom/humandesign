# First-edition Lilly annual-rate table — four complete source columns

**2026-10-18, Africa/Dakar UTC+0.** Source-only archival collation of William Lilly, *Christian Astrology* (1647), first edition, Wellcome b30338724. This does not establish a working natal birth engine, astronomical parity, or real-world predictive validity.

## Original evidence and bounded scope

Original 894-frame 1647 full scan SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. The numerical annual-direction table is original PDF745/printed folio711. The full high-resolution original page render is retained from B07y unchanged, SHA256 `fb75055af87141aba6acda0beaa697af48767217b8f03079453fee0c0ade4feb`. Eight separate contrast-enhanced crop images of the first four zodiac source columns are stored under `evidence/contrast_crops/`. These crops are derivatives of the same photograph, **not independent witnesses**. No machine OCR was used to establish these cells.

All 31 printed positions (0–30 degrees inclusive) for **Aries, Taurus, Gemini and Cancer** were manually visually read from the first edition, **124 new primary-photo source positions**, by one unblinded reader using the earlier B07x searchable transcription as a finding guide. `FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json` records the literal minute/second components for every source position and declares the occasional low/medium clarity conditions. Each row is reversible by sign, printed degree and a crop-half/source-page witness.

The source comparison against the previously frozen derivative transcription finds **one newly established conflicting value: Taurus 28° is 59′36″ in the first edition, while the derivative flattened searchable transcription says 59′56″**. The first-edition print reads Taurus 27° as **59′48″**, a nonmonotonic neighboring rate, and this remains a historical printed reading rather than a mathematically smoothed correction.

This new packet is **append-only**: the complete old B07x 372-candidate table, B07y 24-position photo correction, five prior B07y recorded discrepancies, and raw scan hashes remain preserved. The new `ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json` represents each annual-rate position with its frozen derivative candidate and, when actually observed, an explicitly separate first-edition one-reader photo value or unresolved glyph alternatives.

## Photo-evidence coverage and limits

| Evidence type | Positions |
|---|---:|
| Original table positions (12 zodiac signs ×31 positions) | 372 |
| New complete Aries/Taurus/Gemini/Cancer column photo readings | 124 |
| Earlier clear B07y photo readings, disjoint | 22 |
| **Cumulative one-reader legible first-edition positions** | **146** |
| Original-source glyphs explicitly unresolved (Capricorn15, Pisces24) | 2 |
| Remaining positions not directly photo-adjudicated | 224 |

Photo reading is *not* independent editorial interpretation. A second blind classical-text reviewer, exhaustive second-edition comparison, original celestial mathematics/epoch compatibility, and eventual untouched-human birth-chart validation are all still absent. In particular the 1647 physical source table may contain compositor/transmission errors; preserving those source values is not certifying they correctly measure annual solar right ascension.

The original numerical CLXVI text also contains contradictory Maginus worked-example residuals and Naibod table gaps. Those remain separate B07x provisional numerical method tasks. The original *CHAP CLXVI* time-measure chapter and distinct succeeding annual-profections chapter both bear the same printed numeral, so preserve an editorial distinction rather than silently renumber them.

## Verification contract and next concrete work

Focused B07z source/crop mapping and nonpromotion suite has **148 passing tests**. The portable ZIP extraction must independently pass per-file CRC/SHA256/byte verification and replay all 148 tests before archival publication. Such tests verify exact contents and mapping, not the visual truth of a glyph reading by an independent person. The Western Lilly historical accepted index stays at **12,472** (plus Ptolemy 1,066), and Chinese historical V3 at **142 (46 BaZi, 96 Zi Wei)**. Next Lilly record **R12473 remains unaccepted**, pending full original CLXVI source and computation audit.

Further work: direct 1647 source collation of the still-unread **224 positions** in remaining zodiac columns; re-examine the two unresolved glyphs; compare suspect 1659 edition cells, complete lunar Naibod 90 +59 tables with missing 27 and Maginus residual discrepancy; independently compute historical direction-to-time and birth charts against tested astronomy; continue Zi Wei ZWD-R0097/BaZi BZI-R0047; preregister real-human blinded comparison after model freeze. Source counts are not independent forecast successes.
