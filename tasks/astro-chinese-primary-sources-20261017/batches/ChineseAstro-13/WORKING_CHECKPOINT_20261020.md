# ChineseAstro-13 – exact local birth time projection and explicitly labeled convention boundaries

Working checkpoint. Previous independently accepted source/engineering baseline branch `research/astro-chinese-iztro-external-chart-parity-20261020`, exact sha 6f4a75febc1624e44b54d724422804a05f31fd12. Source annotation counts unchanged: Lilly13,044+Ptolemy1,066+BaZi210+ZiWei220=14,540; human prediction validations zero.

Problem: Existing Chinese 14-star engine accepts a calendar reference Gregorian date / Chinese lunar month-day and separate hour branch. That is NOT real person natal timestamp handling, especially across DST, ambiguous/nonexistent wall times, geography, pre-standardized historical time and daylight-saving changes. Current task is a bounded, strictly source-labeling civil-time bridge using Python `zoneinfo` and two independent Chinese date converters. Design decisions:
- Require full local wall time seconds and explicit user-provided IANA TZ ID (no guessed birth city or timezone).
- Strict DST fold disambiguation; reject nonexistent spring-gap local times; preserve UTC instant and local zone provenance.
- Expose BOTH plausible Chinese-calendar Gregorian date choices: (A) date of same UTC instant in Asia/Hong_Kong; (B) original birth site's civil date looked up in HKO-derived Chinese calendar. Neither is asserted universally correct for cross-geography or ancient periods.
- Hour basis explicit: recorded civil clock OR local mean solar time calculated from UTC + 4 minutes per east-longitude degree; apparent solar time requires equation-of-time astronomy and is currently UNIMPLEMENTED. Local mean solar is NOT apparent/true solar.
- Require explicit birth-longitude for solar time (east-positive); no auto-geocoding; UTC offset/DST kept separate from longitude conversion. Late Zi-at-23 zodiac day rollover versus midnight must be explicitly chosen; only midnight initially supported.
- Lunar New Year stem-year convention only; Li Chun must fail closed, not silently substitute.
- Calendar interpreter depends on pinned lunar-python v1.4.8 + sxtwl v2.0.7 and their 1901-2100 audit. Any conflict (2057 30-day mismatch) fails closed.
- No real owner or third-party personal birth records in tracked test corpus, no real human predictions, no runtime promotion.

Existing-work basis:
- IANA Python zoneinfo + PEP 495 fold https://peps.python.org/pep-0495/
- US Naval Observatory Equation of Time https://aa.usno.navy.mil/faq/eqtime (mean vs apparent separate)
- Official HKO lunar calendar data https://www.hko.gov.hk/en/gts/time/conversion.htm and HKO public date API only from 2023 onward.
- An external iztro 2.6.0 312 synthetic chart cross-implementation comparison is already frozen. Do not rerun unchanged vendor suite.

## Implemented and verified

Bounded source module `ziwei/explicit_natal_time.py` plus `tests/test_ziwei_explicit_natal_time.py`: all required IANA named-zone, DST fold disambiguation, missing local time, UTC source, daylight offset, two reference calendar-day policies, late-Zi explicit only-midnight gate, local longitude mean-solar time and precision guard, and exact 14-principal-star projection under explicit leap/CNY rules. Modern end-to-end path to 14 stars is now possible *only* after exact user-supplied clock, timezone, longitude (when mean solar), calendar reference-day policy and birth-hour/day convention. Source traditional domains and actual person forecast validity unproven.

**Historically significant correction discovered during testing:** `Asia/Hong_Kong` wall clock included summer time UTC+9 during periods 1941–1979 (official https://www.hko.gov.hk/en/gts/time/Summertime.htm). That is **not equivalent** to modern official UTC+8 Chinese calendar reference day. The first prototype implicitly used `Asia/Hong_Kong` for the lunar day date, which could shift births around midnight by one day. Replaced with fixed UTC+8 standard reference; still preserve `Asia/Hong_Kong` as actual local birth clock when explicitly supplied, with independently recorded TZDB SHA. On 1965-07-01 00:30 historic HKT+DST, old local date July1 but source reference Gregorian date June30. New focused source tests cover both different 14-star placements. This finding does not establish the correct year/calendar for all early historical Chinese or foreign locales.

Synthetic DST edge cases: New York 2026 spring missing 02:30 (reject), autumn repeated 01:30 fold 0/1 differing UTC by one hour (require fold), Samoa deleted local date 2011-12-30 (reject). New York longitude -74 mean solar hour vs 2026 daylight saving civil clock changes Wei to Wu for a precisely selected synthetic time. We reject apparent/true solar time, 23:00 Zi-day variants and time uncertainty until source/astronomical resolution.

Independent Node ECMAScript Intl and Python IANA `zoneinfo` 12 case projections (HK 1965, HK 1979, NY 2026, Samoa 2011, Dakar 2026 etc.) matched 12/12. Freeze original hash and ICU/Node/tzdb versions; software agreement may share an original tzdb source and does not independently prove historical clock facts. 24 source and boundary tests green including Gregorian day differences, intentional lunar-year/leap and clock hour branch chart differences. Source-variant preservation and no human predictions.

## Next
- Independent astronomical apparent solar time with equation of time and true historic documentation; distinguish modern NOAA approximation from independently verified ephemeris. Preserve any close-to-branch-boundary uncertainty.
- Historical Chinese official lunar standard evolution, especially pre-1949 Beijing meridian, versus modern UTC+8, and region/multi-calendar lineage variants; do not silently treat 1901–2100 software consensus as ancient correctness.
- Li Chun year and JieQi monthly BaZi solar term parity, 23-hour late Zi / early Zi conventions, exact time uncertainty propagation in predicted chart states.
- Independently source-collate Lilly CLXXXI next R13045, BaZi next BZI-R0211 and Zi Wei Life-palace next ZWD-R0221 on separate guarded append branches.
- Freeze chart-to-survey predictions, prereg real-blind human matched-decoy and non-astrology comparisons and report failures.

## Verification and durable status at closeout

Source-only new IANA/date/longitude engine: **24/24** focused synthetic fail-closed regression tests green. Across all inherited source-HKO-iztro Zi Wei paths plus new time tests, **90/90 affected tests passed**. Post-lint normalization re-tested the changed new module and 24/24 remained green. Static Ruff checks pass on three new Python files; JS original Node Intl comparator passes `node --check`. Separate 12/12 Intl/zoneinfo offline projection record SHA verified. Test-efficiency observer recorded invocation durations without wasteful rerun of the unchanged full 73,049-day or 312 vendor oracle batch.

IANA zone raw binary hash is attached to resolved clock output when backed by the host timezone filesystem; this does not prove the historical clock-law source exactness or original-era natal calendar conventions. The reproducible source records and negative test cases are sufficient to resume without old chat. Exact new source code and handoff committed to branch `research/astro-chinese-13-timezones-localmean-20261020` after verified remote push.

Next: original Chinese 14 stars still not a complete natal chart: historical lunar standards, JieQi/solar LiChun, equation of time (apparent/true solar), Zi23, chart-time uncertainty and all minor stars. Then preregister birth-supplied blinded human forward/reverse validations versus matched decoys and non-astrology baselines. Both old and new human validation counts remain zero.
