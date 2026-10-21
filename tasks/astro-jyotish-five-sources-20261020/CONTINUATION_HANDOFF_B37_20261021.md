# HumanDesign five-book Jyotish reader — B37 continuation (2026-10-21)

**ROOT TASK OPEN.** Repo `u-dont-existDOTcom/humandesign`, isolated branch `research/astro-jyotish-five-sources-reader-20261020`, draft PR #136. **412** historical source-only annotations; **zero** independent human predictive successes, **zero** production rules. Other readers, survey and participant files unchanged. No copyrighted full books in public GitHub.

## New since B35

**B36 (+2 source notes):** `SOURCE_CANDIDATES_B36.json`, `READING_NOTES_B36.md`, `SIX_EXALTATION_SKY_SUPPORT_B36.json`, `six_exaltation_support_B36.py`. Sanskrit `Sārāvalī` **35.169** (English 35.168/PDF105) puts Sun THIRD from Mercury, impossible for a whole-sign zodiac because Sun/Mercury require ≥30° difference while Mercury maximum solar elongation ~28°. Sanskrit **35.80** (English 35.79/PDF100) says **Mercury–Jupiter–Venus** in fourth aspected by Sun, while uploaded English wrongly names **Saturn**; under sign graha-dṛṣṭi the Sun cannot aspect Mercury because the first allowable aspect is third-house. This is conditional on source-defined aspects, not on all possible modern aspect schemes.

B36 nonproduction **Moshier Lahiri sidereal** 00UTC search (astronomical years −2999 to +2999, **2,191,090** proleptic Gregorian midnights), optimized outer-planet guards reproducing the earlier 400-year full check, finds **17,355** Jupiter Cancer + Saturn Libra days, **1,153** also Mars Capricorn, **77** additionally Sun Aries, and **0** additionally Venus Pisces; thus **0 sampled** complete six exaltations (omitting Mercury). **NOT** a proof this sky configuration is impossible in all time or sub-day intervals; historical Moshier and source-ayanamsha choices are not canonical pinned SWIEPH.

**B37 (+3 source notes):** `SOURCE_CANDIDATES_B37.json`, `ASPECT_STRENGTH_TRANSLATION_AUDIT_B37.json`, `READING_NOTES_B37.md` identify a consequential **English translation inversion** in Saravali 4.32–33: uploaded English says 1/2 aspect fourth/eighth and 3/4 fifth/ninth; actual Sanskrit and Jataka Parijata II.30 plus Portuguese Parashara line2311 say **1/2 fifth/ninth and 3/4 fourth/eighth**. The source-supported *eligible aspect houses* did NOT change, so B36 impossibility of Sun-to-Mercury sign aspects remains conditional but intact.

**B36 code supersession now explicit:** `solar_graha_aspect_B36.py` and `test_solar_graha_aspect_B36.py` rewritten to require a named `english_uploaded` vs `sanskrit_restored` version; no default and **6/6 local tests passed**. GitHub blobs verified exactly equal locally tested files. `six_exaltation_support_B36.py` is likewise byte-identical to locally tested coarse-to-fine Moshier scan.

## Exact next tasks

Compare original Parashara planet-aspect longitude interpolation (Portuguese CP1252 lines2319–2343) to sign graha-dṛṣṭi and Jaimini rāśi-dṛṣṭi; preserve source-specific semantics and any new numerical translation defects. Then resume unexamined verse-level material from five books rather than recomputing already accepted B01–B37 batches. Do not fit known biographies, retroactively choose source readings, count copied passages as independent successes, or merge parallel reader work. Reader remains open.
