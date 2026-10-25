# Source scope — Argoli, Regiomontanus, and Lilly

Research date: 2026-10-25. The owner's overarching astrology objective remains **OPEN**: compare historically differentiated, independently frozen chart-based predictions against untouched human events and proper controls. This mathematical source audit is supporting evidence only.

## Physical primary source

Andrea Argoli, *Primi mobilis tabulae*, a public-domain later edition (1667, Padua), digitized from an Internet Archive/Google Books original; PDF identifier `primimobilistab00argogoog`. A 107-image excerpt, ending at original printed p.95 before the binding back cover, is preserved byte-for-byte in `primary_1667_volume/`. Its SHA-256 is `b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d`. Three rendered plates have independent hashes under `primary_1667_pages/`.

- Original printed p.3 (PDF physical page 14): Argoli discusses the 'rational' method of Johann Regiomontanus, position circles, oblique/rect ascensions and polar latitudes. That establishes the historical *family* of methods he is discussing.
- Original printed p.7 (PDF physical page 18): original tables of rectangular and oblique ascensions, position-circle/pole-elevation computation. This source supports a table-based pole framework.
- Original printed p.23 (PDF physical page 34): worked interpolation in oblique ascension for elevations of the pole around 44° and 45° with degree/minute arithmetic.

A distinct original 1610 Rome printing was located in Google Books (ID `-zhmAAAAcAAJ`), and 1644 Gallica copies were identified, but we have **not** verified full numerical table equivalence with the 1667 printing. Claiming full 1610/1644 source exactness from this later surviving scan would be unwarranted.

## Mathematical reconstruction

Rumen Kolev, *William Lilly and the Algorithm for His Primary Directions*, modern secondary mathematical paper (PDF `https://www.babylonianastrology.com/downloads/Lilly2.pdf`, inspected pp.12–19), reconstructs an explicit fictitious-pole Regiomontanian method and gives a rounded Sun/Jupiter example. These formulas are **Kolev's modern expression of an earlier method**, not a verbatim Latin transcription from Argoli's 1610 tables.

Our new module `src/hdmatch/astrology/regio_pole_independent.py` implements that mathematical route via significator zenith distance, pole, ascensional differences and fictitious horizon. It does **not** call or copy the existing Cartesian position-circle function. Direct comparison is therefore meaningful for arithmetic parity, but it still shares the same conceptual geometry and is **not independent empirical astrology evidence**. The existing Placidus-under-pole and proportional semi-arc arms remain distinct and must not be relabeled 'Argoli'.

The protocol explicitly marks the prior 1200 seeded exploratory coordinate comparisons as DEVELOPMENT. A separately fixed 800-case set with seed 20261026 is a later mathematics holdout to be executed only after the protocol/code/test commit. Neither set contains real natal charts or behavioral outcomes.

## Unresolved historical and experimental conditions

Complete earlier-edition table collation, planetary ecliptic latitude, zodiacal ray promissors, lunar motion, full direct/converse conventions, compound natal strength, term variants, source-specific timing keys, event meanings, and historical author's prognosis conditions remain OPEN. A matching mathematical arc alone establishes no predictive accuracy or historical source uniqueness. The forward-blind human test has not begun.
