# T54 — reproducible traditional Tibetan civil-date mathematics

Research status **SOURCE CALCULATION PARITY, NOT HUMAN PREDICTION VALIDATION**.

Original parent research goal remains OPEN: source-study Tibet alongside Lilly/Ptolemy, Jyotish and BaZi/Zi Wei, then independently frozen prospective blinded human tests vs decoys and non-astrology baselines.

## What works

`tibetan_true_dates.py` implements Svante Janson's *Tibetan calendar mathematics* (2014) equations 5.2–5.9, 7.1–7.24, 8.1, Appendix A.2. It uses Python standard library `Fraction` exact arithmetic and supports:

- Phugpa epochs **806/1927/1987** and Tsurphu epochs **1732/1852**, with explicit per-call choice.
- Mean date/Sun/Moon anomaly and tabulated interpolated corrections, keeping **rounded lunar anomaly** versus **Dharmashri/Henning exact increment** as explicit alternative policies.
- True tithi/lunar-day ending time as a fractional Julian day number, and the integer JDN for the traditional calendar day.
- Correct leap-month instances, skipped and doubled lunar-day labels, first versus second occurrence, Gregorian day-label ↔ Tibetan day-label conversions.
- Losar calculated from the last day of regular month 12 the preceding Tibetan year (Janson Section 8), without assuming Gregorian year and Tibetan year are identical before New Year.

**Unimplemented/forbidden inference:** arbitrary UTC birth instant to Tibetan calendar day; local mean dawn/observer coordinates; time zone; actual astronomical sunrise; physically accurate observed lunar longitude; Jyotish/natal interpretive predictions; original Tibetan text collation. Source Janson Remark 6 models theoretical local mean dawn (~05:00 LMT), not an astronomically measured sunrise. Civil date-label conversion must not be silently presented as timestamp-based horoscope.

## Independent verification receipts

- `verify_t54_true_dates.py` is an original offline test: 10 published Janson Phugpa Losar dates and **twelve full source-built Tibetan years** across Phugpa/Tsurphu; every resolved civil date covers an uninterrupted JDN, all skipped/repeated labels use explicit flags, correct epoch agreement and round-trip behavior. Also rejects unsupported epochs and missing anomaly policies.
- `compare_t54_independent_tibcal.py` (optional external reference) compares **4,386** individual dates across six Gregorian years and both traditions with independently authored **dorjeduck/tibcal** Python implementation pinned to GitHub **01591b5bf03d038b864c4138fde3cc4285ca8001**. Result **0 mismatches**. The external MIT source is NOT copied into HumanDesign.
- `compare_t54_independent_javascript.py` (optional independent second reference) checks **2,193** Phugpa civil dates against **hnw/date-tibetan** JavaScript implementation pinned to **7651b8b579c8332442198cc0d9ca14d0b0e8b3a8**. Installed only the external module's production dependency with `npm ci --omit=dev --ignore-scripts` into an external temporary clone. Result **0 mismatches**. This is independent code/source-language corroboration of **Janson-defined calendar date labels**, not of astrology or historical observations.
- `DIFFERENTIAL_PYTHON_RECEIPT_V1.json` and `DIFFERENTIAL_JAVASCRIPT_RECEIPT_V1.json` capture exact SHA, total counts, years and zero disagreement. `JANSON_TRUE_DATE_12_SOURCE_NOTES_V1.json` adds historical math annotations R0489–R0500 (12), nonduplicate from T01–T53, **cumulative 500**.

## Provenance and license

Janson's scholarly mathematical formulas (not the external implementations' source) informed our fresh MIT-licensed Python implementation, with separate expressions and method boundaries. References:

- Source: https://arxiv.org/html/1401.6285v1 (sections 6–9, Appendix A.2).
- Independent MIT Python comparator: https://github.com/dorjeduck/tibcal (pinned SHA above).
- Independent MIT JavaScript comparator: https://github.com/hnw/date-tibetan (pinned SHA above).
- Existing earlier T53 partial year/month/day symbolic module is **retained unchanged** until a cross-module integration review. Janson's exact mathematical dates do not imply psychometric specificity, life-event predictive accuracy or clinical suitability.

## Next priority

Record the exact mean-dawn/UTC observer convention separately before using birth timestamps, and test any such convention with independent source examples. Extend Janson's solar/lunar mansion and yoga almanac components with evidence-labeled source variants; continue Henning/Cornu/Erlewine readings and original Tibetan manuscript collation. Only frozen calculated human tests can support actual predictive claims.
