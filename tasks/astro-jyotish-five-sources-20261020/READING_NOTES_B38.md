# B38 — Three distinct aspect systems and a shared Sun–Mercury exclusion (2026-10-21)

**Status:** Source-text and deterministic arithmetic only. No chart of any participant, no prospective human outcomes, and no change to the live model. Two new documentary source notes: `SOURCE_CANDIDATES_B38.json`. Comparison and tested code: `ASPECT_MODEL_COMPARISON_B38.json`, `comparative_aspect_methods_B38.py`, `test_comparative_aspect_methods_B38.py`. Historical source-only tally advances from **412 to 414**, NOT verified prediction successes.

## Original-source distinctions

**1. Parāśara exact planetary aspect (sphuṭa graha dṛṣṭi).** The user-provided Portuguese translation `BPHS` cp1252 **lines2305–2321** expressly distinguishes previously described sign aspects from planetary aspects computed from angular separation. Original-language digitized [BPHS Sanskrit Chapter26 verse5](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-5) introduces more exact planetary angular separation; [verses6](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-6), [7](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-7), [8](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-8), [9](https://vedicpupil.in/library/books/brihat-parashara-hora-shastra/chapter-26/verse-9) specify a **directed** zodiac longitude difference (target minus source, normalized to 0–360 degrees) with a piecewise strength in *virūpas*, capped 0–60. The formula's ordinary result is **zero for gaps between 0 and30 degrees and between 300 and360 degrees**; then rises through 1/4 at 60°, 3/4 at90°, 1/2 at120°, zero at150°, full at180°, zero at300°. This is the **general** base aspect, not the separate Mars/Jupiter/Saturn special increments in Sanskrit 26.10–12, nor final aggregated Shadbala/Drigbala.

**2. *Sārāvalī* restored Sanskrit discrete graha aspects.** Source Chapters4.32–33: 1/4 third/tenth, 1/2 fifth/ninth, 3/4 fourth/eighth, full seventh. The user-uploaded English reversed halves and quarters; B37 preserves both editions and a revised explicit-version standalone calculation. Neither includes a same-sign or adjacent-sign aspect, so the only sign positions possible to the Sun for Mercury cannot be positive in this version.

**3. Rath's Jaimini *rāśi dṛṣṭi*.** The user's PDF257–258 has the short Sanskrit original `Jaimini 1.1.2` followed by **Rath's interpretation**: movable signs view fixed except adjacent; fixed view movable except adjacent; dual signs view other dual signs. This is sign-to-sign angular relation **not** equivalent to the planetary graha or degree-weighted BPHS calculation, and the full operational enumeration is commentarial, not literal Sanskrit syllables in 1.1.2. Same-sign and immediately neighboring-sign planets do **not** qualify under this Rath version.

## Correct source-bound mathematical conclusion

The astronomical independent constraint is that Mercury remains within roughly 28° of the Sun as observed from Earth ([University of Nebraska–Lincoln](https://astro.unl.edu/naap/ssm/elongation.html)). To avoid false precision from the rounded number, the fixtures use the *conservative assumed bound 29° of ecliptic longitude separation*, still strictly below the relevant 30-degree source threshold. Under that bound:

- BPHS ordinary directed exact aspect is **0** for either positive or negative elongation.
- Restored Saravali sign graha-aspect is **0** because Sun and Mercury lie in the same or adjacent signs.
- Rath/Jaimini sign-to-sign aspect is **absent**, because same and adjacent signs do not aspect.

**Three different formulas lead to the same local no-Sun-to-Mercury conclusion, but that does NOT mean the three textual traditions are identical elsewhere.** Any alternate school, angular aspect type, house convention, or special exception remains a separate research question. Also, the relationship between great-circle maximum elongation and rigorous ecliptic longitude maximum deserves independent ephemeris/error assessment for theorem-grade precision; this is a well-declared 29° conservative model bound.

## A separate erroneous modern documentation table is not ancient Sanskrit

The modern [Saravali software `Sphuta Drishti` page](https://saravali.github.io/astrology/drishti_sputa.html)—which is **not** Kalyāṇavarman's ancient `Sārāvalī`—prints:
- `2*(150-d)` for d in 150°–180°, which yields **negative -30 at d165°**, contradicting its own [0,60] statement and the original source direction `2*(d-150)`.
- `(300-d)/2` over d270°–330°, giving a negative result above300° when the general ordinary aspect should already be zero.

These are errors in a *derived modern reference/implementation table*, not new Sanskrit school variants, not reason to silently alter uploaded sources, and not evidence against or for horoscope predictions.

## Reproducibility

The two research-only Python files calculate BPHS ordinary angle strengths, Saravali restored discrete aspects and Rath commentary Rāśi aspects **separately**. **Seven unit tests pass** on the local execution, including a dense 0.01° sweep over 0–360 that checks bounded 0–60 virūpa output and continuity at degree boundaries, independent sign controls and input validation. GitHub-read-back Git blob SHA-1 files are identical to tested local files (`39926d2f69e4ceb16af8eac3447b1e2821395470` and `3c1af50818c3310bf9405d88341b552c923f97ad`).

**Next source frontier:** Original Sanskrit BPHS 26.10–12 for special Saturn/Mars/Jupiter aspect values and how distinct variants affect the exact-degree matrix; then broader original-text and falsifiable-outcome research. Do not collapse source types or prematurely promote into the Human Design astrology engine.