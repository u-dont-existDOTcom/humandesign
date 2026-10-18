# Lilly's direction-time numerical source: cross-edition and table-wide provisional audit

**Source study updated 2026-10-18, Africa/Dakar (UTC+0).** Parent research task remains OPEN. This audit expands the pending B07x numerical method packet; it does **not** accept CLXVI into the Lilly canonical registry and does **not** establish any human astrological forecast accuracy.

## First-edition authority and independent second-edition print witness

The authoritative source is William Lilly's original *Christian Astrology* **1647**, Wellcome b30338724, original full 894-frame PDF SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`; chapter printed folios 708–715, PDF742–749, old Naibod **degree table** on PDF747/printed713 and **minute table** on PDF748/printed714. Source image bytes and hashes are in `ORIGINAL_SOURCE_WINDOW_V1.json`.

A genuinely separate **1659 second-edition typeset print** was located: `File:Christian Astrology (Lilly, 1659).djvu` on Wikimedia Commons, page 742 (printed713 Naibod degree table) and page 743 (printed714 Naibod minute table). Its actual scans were downloaded and archived as `evidence/second_edition_1659/1659_djvu_scan_742.jpg` and `...743.jpg`, with independently recorded SHA-256 hashes. The digital derivative on pdfcoffee.com is used only as a convenient machine-readable *secondary transcription aid*. Its exact table-section SHA256s are frozen in `NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json`; the 1647 original photo always takes precedence.

## Original Naibod table results

- **90** numerically indexed degree rows were populated from the modern searchable text and checked against selected original printed rows. Critical correction of derivative representation: **degree inputs 69–90 map to printed year entries 70–91** (the original and 1659 printings carry an extra completed year at the 365-day rollover). The flattened modern text wrongly treats printed years as 69–90; **22 affected year fields** remain separately preserved under `secondary_transcript_years`.
- Only **59 minute labels** are present in the 1647 *and* 1659 printed tables: the label **27 is skipped**, and label28 takes 166d18h; labels29 and30 take 172d23h and 179d3h. This omission is a real printed feature, not a dropped JSON row. The data cannot safely be completed by silently inserting interpolation under "source values."
- 1647 minute1 day glyph is ambiguous to a reader (**5 or 6**), but the 1659 printing and the derivative transcription read **6d4h**. The primary first-edition row retains the visual uncertainty rather than silently replacing it.
- Minute8 is **44d10h** in both printed editions even though surrounding arithmetic suggests approximately 49d10h. This is a strong persistent printing/transmission anomaly; an inferred correction has **not** been written into the source table.
- **Minute44 differs across editions**: 1647 and the derivative transcription give **271d8h**, while the 1659 typeset photo reads **271d18h**. Original and later values remain separate. This may be an editorial change/erratum, not proof of predictive validity.
- Minute60 is **374d14h** in both editions; printed degree1 equals **1 year, 5 days, 8 hours**, equivalent to 370d8h under the chapter's 365-day carry. The two printed table representations of equal arcs differ by **4 days, 6 hours**. No automatic normalization or interpolation is admitted.
- Degree80 prints **24 hours**, not zero; exact transcribed unit is preserved even though it could be normalized arithmetically. The two original worked Naibod examples, 11°55′ → **12y33d14h** and 19°52′ → **20y57d21h**, still replay against their original selected rows.

`NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json` contains the source identities, edition-specific values, direct image hashes and 12 comparison notes. `NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json` gives all 90 degree and 59 visible minute rows with explicit ambiguity/correction statuses. These candidate rows are **not** a complete critical transcription or a scientifically validated direction-date calculation.

## All 372 annual-rate table cells: provisional text reconstruction, not false validation

Original PDF745/printed711 contains an annual measure table with **31 degree rows (0 through 30 inclusive) ×12 signs =372 pairs of equatorial angular-rate minutes/seconds**, 744 numeric fields. Machine-readable derivative text contains precisely these 744 numeric fields but **scrambles sign-column order**. A naïve split treats the seventh text block as Libra: this gives **64′47″** at Libra 7°, inconsistent with the first-edition printed 54′25″ worked case. Verified original photo data require this explicit reversible mapping from zodiac sign to flattened numeric block:

`Aries=9, Taurus=0, Gemini=1, Cancer=2, Leo=3, Virgo=4, Libra=10, Scorpio=5, Sagittarius=6, Capricorn=7, Aquarius=8, Pisces=11`.

The builder `build_annual_measure_372_provisional.py` reconstructs **372 candidate cells**, retaining the exact derivative text block for each and **without arithmetic correction**. Only **12 cells have direct original PDF745 photo checks** so far (11 clear degree-zero sign entries plus the critical Libra 7° 54′25″). Leo 0° is deliberately excluded from the confirmed count: the derivative gives **59′24″**, but the original photographed glyph may read **59′34″**; the conflict remains flagged. Candidate cells with abrupt changes in adjacent rate are flagged for manual review, and the other **360 cells remain derivative-only/unverified**. The rate unit is a *total number of equatorial arcminutes per year*, so 60′–66′ are valid amounts (not invalid sexagesimal component values).

The complete source dataset `ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json` records cell-level tentative rates, source-block mapping, 12 photo attestations, source anomalies and **zero runtime promotions**. The 372 is a **coverage inventory**, not the number of fully verified original cells, and certainly not a human-evaluation sample.

## Outstanding scientific/engineering work

1. Visually compare **all 372 candidate cells** with original 1647 PDF745, resolving explicit ambiguous glyphs by at least one independent human/editorial review and 1659 edition where relevant.
2. Audit remaining primary 1659 printed Naibod rows against photo rather than trust the derivative text. Preserve 1647 readings when editions disagree. Compare corrected printed tables to deterministic minute/degree calculations and identify what the year carry/rate convention actually is.
3. Resolve Maginus's two worked-example residual arithmetic mismatches from PDF746 with an independent first/second-edition comparison before treating them as reliable algorithm instructions.
4. Finish the full printed CLXVI's reverse source map and independent archive replay. Only then consider a guarded historical-source index increment. Next distinct chapter *annual profections* also prints **CHAP CLXVI** on original PDF749; preserve duplicated numeral and its separate editorial identity.
5. Calculate genuine birth-chart era, 1647 ecliptic/oblique ascension, latitude and time conversion with reliable independent astronomical parity before designing **prospective blinded human accuracy tests** with matched decoys. Historical source text, computational reproduction, and actual-world forecasting are different evidence planes.

No high-stakes health, death, sexuality, legal, morality or socioeconomic conclusions about real people may be drawn from this 17th-century text.
