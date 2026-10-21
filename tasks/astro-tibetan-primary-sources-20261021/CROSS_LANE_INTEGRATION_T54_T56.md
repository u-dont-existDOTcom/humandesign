# Tibetan astrology T54–T56: civil-date algorithms and experimentally explicit birth-time policy

**Research date:** 21 October 2026. **Parent owner task remains OPEN.** This is documentary/source mathematics and software parity research for the Tibetan part of the HumanDesign comparative astrology project. It does not establish traditional astrology's predictive ability. No human questionnaire, known participant life event, response key or private birth data was used.

## Accepted baseline and changes

Accepted previous Tibetan lane: `research/astro-tibetan-t51-cornu-janson-math-20261021` at `4110a30342f05dd58a4167634370db52b1baa436`, 488 historical source annotations (TIB-R0001–0488). This pass adds **12** genuine source/math annotations in `batches/T54/JANSON_TRUE_DATE_12_SOURCE_NOTES_V1.json` (TIB-R0489–0500), bringing the cumulative documentary-source total to **500**. Batches T55 and T56 have **zero** new source-annotation count: they are respectively a source-labeled project hypothesis and a computational sensitivity measurement.

All changes are isolated in the Tibetan task folder. The prior accepted 488 annotated records, the Western Lilly/Ptolemy source lane, Chinese BaZi/Zi Wei, Indian Jyotish, existing human participants, and production model/scoring engines remain unchanged.

## T54: independently written exact rational date engine

File: `batches/T54/tibetan_true_dates.py`.

Source: Svante Janson (2014), *Tibetan calendar mathematics* (arXiv:1401.6285v1), §§5–9 and Appendix A.2, with explicit rational constants and independently re-derived code. (This derives traditional model dates, not observed contemporary astronomical conjunctions.)

- Implements `true_date` from mean lunar date, mean solar longitude, lunar anomaly, and linearly interpolated Moon/Sun correction tables; Python `Fraction` avoids floating-point changes at exactly integral date boundaries.
- Explicitly supports **Phugpa 806/1927/1987** and **Tsurphu 1732/1852** epoch policies. Their month-index/leap-month rules, constants and version identities stay distinct. No default policy is silently substituted.
- Computes one-based Tibetan year/month, leap-month instance, lunar-day/tithi, skipped lunar-day labels, the *first* leap/extra instance of duplicated day labels, and Gregorian-day-label/JDN conversion both directions. **Losar** is the calendar day following lunar day 30 of previous Tibetan year's regular 12th month, including a leap first month.
- Requires an explicit lunar-anomaly policy: Janson's commonly used `a2=1/28` versus the Dharmashri/Henning mathematically exact `a2=3781/105840`. The two sources/algorithms are preserved, not selected based on a participant's chart.
- Conventional **Gregorian date labels are NOT identical to UTC instants**; Janson's JD is the theoretical local calendar day ordinal. This module does **not** automatically infer what Tibetan day a person occupied at a given UTC birth instant or a physical sunrise in a particular city. That is a separate policy below.

Source semantics are bounded: traditional mean/true solar and lunar values are **historical model coordinates**, not guaranteed modern Swiss/JPL or observational ephemeris positions. Matching calendar arithmetic is not a scientific prediction test.

### Verification: original source and two separately authored implementations

**All receipts checked and saved** under `batches/T54/`. No external project's copyrighted source code was committed; both references advertise MIT licenses, but that is not an endorsement of empirical astrology.

1. **Internal/source specification:** `verify_t54_true_dates.py` reproduces **ten published Phugpa Losar dates** (1950, 1951, 1984, 1985, 2000, 2023–2027), checks all five supported epochs agree *within their own tradition*, and checks **12 full Tibetan years** (six source years × Phugpa/Tsurphu) for uninterrupted civil-day JDN continuity, valid skipped and duplicated labels, leap-month numbering, round-trips and explicit rejection of invalid policies. It chains the earlier T51–T53 source verification.
2. **Independent pinned Python reference:** `dorjeduck/tibcal` (MIT, exact upstream Git SHA **01591b5bf03d038b864c4138fde3cc4285ca8001**), written independently from Janson's formulas, was retrieved and inspected. `compare_t54_independent_tibcal.py` checked **4,386 individual civil dates** over 1950, 1984, 1985, 2000, 2024, 2026 across **Phugpa and Tsurphu**. **0 differences**, including leap-month, skipped and repeated-day cases. Receipt: `DIFFERENTIAL_PYTHON_RECEIPT_V1.json`.
3. **Independent pinned JavaScript reference:** `hnw/date-tibetan` (MIT, source SHA **7651b8b579c8332442198cc0d9ca14d0b0e8b3a8**) was separately fetched. Production package dependency installed only in a temporary clone with `npm ci --omit=dev --ignore-scripts --no-audit --no-fund`. `compare_t54_independent_javascript.py` checked **all 2,193 Gregorian dates in those same six years for the Phugpa tradition**. **0 differences**. Receipt: `DIFFERENTIAL_JAVASCRIPT_RECEIPT_V1.json`. This is a second implementation/language cross-check, not another 2,193 *different* dates. Combined evidence is not 6,579 unique dates; the JS subset overlaps the Python comparisons.
4. Janson's Phugpa Losar benchmarks reproduced include 1984-03-03, 1985-02-20, 2000-02-06, 2024-02-10 and 2026-02-18; Tibetan New Year can occur on leap month 1 as in 2000. The day 1985-02-19 belongs to the still-running Tibetan Wood Mouse year, not 1985's Wood Ox year.

The two independent packages compare mathematical **calendar conventions**, not source witnesses for Tibetan classical interpretation, actual planetary observations, or participants' future lives.

## T55: optional born-at-UTC clock policy and author worked chart

Source/candidate: Janson §6 Remark 6, Henning Chapter I pp10–11 and Cornu's 1950 Paris example. Janson describes a theoretical traditional mean daybreak, about **05:00 local mean solar time**, and specifically does **not** require measured sunrise. Project inference (not yet demonstrated traditional historical universality): **`project_extension_05_LMT_dawn`** applies that time convention to an independently supplied birthplace longitude, after the political civil timezone has already been resolved to an aware UTC instant.

File: `batches/T55/natal_mean_dawn_candidate.py`; explicit UTC datetime, degrees east of Greenwich, calendar branch, epoch and anomaly policy. The result records local mean solar clock without a misleading +00:00 timezone suffix; gives theoretical dawn day label, Tibetan year/month/tithi/double hour, four animal+element pairs, natal mewa and year forces. Fails closed for naive datetimes, nonzero local offset without upstream UTC normalization, non-numeric/invalid longitude, unspecified policy, unsupported epochs.

**Published Cornu example reproduced independently:** 1950-11-15 **17:00 Paris political civil time** (`Europe/Paris` historical UTC+1) → 16:00 UTC → 16:09:24.528 mean solar clock at longitude 2.3522°E. Phugpa/Janson year 1950 month10 day6 and traditional Monkey double-hour produce **Iron Tiger (year), Water Ox (month), Wood Ox (lunar day), Fire Monkey (hour)**. Natal central mewa=5, day mewa=3, year life/body Wood, power Iron, fortune Iron, spirit Water. This is a precise reconstruction of an author's **worked chart**, not accuracy against that person's actual behavior.

Boundary tests: mean-solar 04:59 vs 05:00 on 2026-02-18 produce previous vs new Tibetan day and at Losar year; longitude changes the offset. The **location extrapolation is tagged an assistant research hypothesis**, not a source-proven canonical practice for Pennsylvania, Paris, Senegal or the rest of the world. A location-specific source convention must be frozen before any human test; no client or user identity used.

## T56: variant sensitivity

To prevent false consensus when two scholarly lunar-anomaly increments differ, `batches/T56/compare_anomaly_policies.py` compared *both Janson-style mathematical methods* on exactly 65 Tibetan years, 1987–2051, both Phugpa and Tsurphu. Results:

| Traditional calendar | Tithi-end calendar-day comparisons | End-day-number differences | Losar date differences |
|---|---:|---:|---:|
| Phugpa | 24,120 | **6** | **0** |
| Tsurphu | 24,120 | **5** | **0** |

These are **tithi-end JDN differences**, not counted distinct birthdates, people, or successful predictions. Full examples and exact policy wording are recorded in `batches/T56/ANOMALY_POLICY_SENSITIVITY_1987_2051.json`. All 11 differences shift the assigned tithi ending by one calendar day. Though infrequent, this is enough to change classifications for certain births, so register the choice before outcome scoring.

## Cross-lane merge constraints

Tibetan *Jungtsi* year/month/day animals and five-force elemental relationships share inputs and history with Chinese BaZi and Tibetan-derived numerology. The lunar mansion/almanac parts overlap Indian Jyotish astronomy. Mathematical agreement of inherited formulae across books is **not independent evidence of personality or life-event predictions**. The explicit Janson model's `true_date` is also not a physical ephemeris; do not treat its sunrise/daybreak and solar longitude as Swiss ephemeris corroboration.

Recommended future arms once the source rules and exact birth conversions are frozen: Tibetan-only birth features vs matched birth-year/chart decoys; the Tibetan *increment* over fixed Chinese BaZi/Jyotish/Western predictions; non-astrology age/cohort and behavioral baselines. Marriage/parents/household/consultation/ritual/mortality/afterlife statements require separate input and evidence classes, never improvised natal survey items. Keep real human predictive hits/misses and negative controls, and distinguish source algebra accuracy from forecast accuracy.

## Incomplete root work and next executable source frontier

T54–T56 complete source-grounded traditional civil-date conversion and the **optional** theoretical mean-daybreak research policy for chart construction. Not done: physical astronomical ephemeris parity, original Tibetan manuscript reading, all Cornu/Henning/Erlewine/Janson sections, lunar mansion/yoga/karana computation, independent verification of location-specific historical application, birth-time data-quality policy for human cohorts, and any *real* frozen/blinded human prediction.

**Next source ID TIB-R0501**, after 500 current historical annotations. Read and implement Janson §10's lunar mansion/yoga/karana almanac components (source-formula derived, physically approximate), check independent **lscalendars/tibcalendar** or other versioned implementations, and finish outstanding Henning/Cornu/Erlewine and original Tibetan witness reading. Keep previously accepted 500 IDs unchanged. No need for human approval for reversible source reading and local tests; DO NOT collect participants, claim medical/mortality guidance, spend money or publish external results without appropriate separate authority.
