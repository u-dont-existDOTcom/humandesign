# Swiss Ephemeris Moshier third numerical witness — BaZi JieQi audit
21 October 2026. DEVELOPMENT-ONLY original-calendar engineering. No personal birth data, no horoscope validation, no model promotion.

## Fixed source authority and exact question

The prior Chinese source-only registry V30 (BaZi230 + Zi Wei1059 =1289 historical documentary annotations, NOT validated predictions) is unchanged. Prior separately accepted two-library synthetic fixture has SHA256 `bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e` and exactly 480 ordinary synthetic date/hour cases plus 36 deliberately term-boundary clocks across six original solar-term days. It compared `sxtwl 2.0.7` and `lunar-python 1.4.8` and retained 4/36 nonunanimous exact-term clocks despite correcting the 8/480 naive date-only GanZhi mismatches.

This THIRD comparison holds all prior sample clocks and Chinese stem/branch outputs immutable and computes the geocentric apparent tropical ecliptic longitude of the Sun relative to the moving equinox using the independently installed `pysweph 2.10.3.6` wrapper of Swiss Ephemeris 2.10.03, with explicitly requested and returned `FLG_MOSEPH | FLG_SPEED` numeric flags **260**. Neither SWIEPH planetary .se1 files nor JPL DE kernels were requested or used. We subtract eight hours from the strictly fictional fixed UTC+8 reference clock before converting to a Julian Day in UT, then find the longitude crossings for targets 315°, 285°, 315°, 255°, 135°, 255° for the six previously prespecified exact source dates. `swe.calc_ut` handles ΔT internally under its declared ephemeris model. The converter treats UTC civil clock as UT; it does not separately verify UT1−UTC, historical civil offsets, apparent versus true solar birthplace time, Chinese traditional ephemerides or independent observatory term announcements.

The Swiss Ephemeris documentation confirms that an omitted true-position, sidereal, heliocentric, topocentric, equatorial or nutation-suppression flag means default **apparent geocentric tropical ecliptic** longitude of date. Moshier is a semi-analytic approximation, not a JPL kernel; the vendor notes planetary positions differ from JPL below roughly one arcsecond, so a submillisecond **root solver numeric residual** is emphatically NOT one-millisecond real astronomical accuracy. The 1912/1965 term seconds depend on historical ΔT conventions. Exact original references: https://www.astro.com/swisseph/swephprg.htm ; https://www.astro.com/swisseph/swisseph.htm . These are provider descriptions, not independent observation confirmation.

## Results (model crossing instants, fictional UTC+8)

| Term reference day | sxtwl source term | Moshier longitude target | lunar-python first new-pillars second | Moshier minus sxtwl |
|---|---|---|---|---:|
| 2023-02-04 | 10:42:20.856 | 10:42:32.522 | 10:42:33 | +11.666 s |
| 2026-01-05 | 16:22:53.353 | 16:23:09.285 | 16:23:10 | +15.933 s |
| 2026-02-04 | 04:01:51.393 | 04:02:08.050 | 04:02:08 | +16.658 s |
| 1912-12-07 | 18:58:53.093 | 18:58:53.431 | 18:58:53 | +0.338 s |
| 2057-08-07 | 07:33:09.603 | 07:34:11.131 | 07:34:00 | +61.528 s |
| 1965-12-07 | 15:45:32.080 | 15:45:31.899 | 15:45:32 | −0.181 s |

At **5 of 6 source term dates** the lunar-python first altered GanZhi second lies within 1 second of the Moshier numerical longitude crossing, while the 2057-08-07 day differs by ~11.131 seconds (lunar-python crosses earlier). This is conditional correspondence between software implementations, not independent proof they compute the historically correct Chinese JieQi instant.

Across the **original 36 deliberate clocks**, the third witness agrees with both calendar-library GanZhi states in 31; **five require abstention**:
- 2023-02-04 10:42:21; sxtwl already switches but lunar-python and Moshier still pre-term.
- 2026-01-05 16:22:54; sxtwl already switches but lunar-python and Moshier still pre-term.
- 2026-02-04 04:01:52; sxtwl already switches but lunar-python and Moshier still pre-term (year and month).
- 2057-08-07 07:33:10; sxtwl already switches, lunar-python and Moshier still pre-term.
- **New negative** 2057-08-07 07:34:09; sxtwl and lunar-python both report the new month, but the Moshier solar longitude is still **below 135°**; the model crossing is ~07:34:11.131. Two agreeing libraries are therefore NOT enough for a source-correctness claim. The two-library previous report saw only four nonunanimity cases; the fifth is independently detected from the third numerical solar-term model.

All original disagreements are retained with flags, actual reported year/month GanZhi values, relative target-longitude angular difference in arcseconds, solver tolerance, and named source method in `BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json` (SHA256 **48d9b068797c4ef2209761c4d94532d035e26205b48c8f3cfb250c61722d06b1**). This is a selected boundary challenge set. **5/36 is NOT a population error rate** nor a real-world birth calculation success or any prediction about humans.

## Implications and remaining independent gate

Software Moshier precision/coordinate mode, UT1−UTC, ΔT, time scale, precession/nutation, and contemporary Chinese solar-term conventions can shift the apparent crossing. This comparison does not establish either implementation's absolute one-second accuracy. A fourth comparison against original observatory published term moments or a pinned independent high-accuracy JPL/Swiss-kernel ephemeris with correct flags and timescales would help adjudicate the remaining 2057 disagreement. Until then, **ABSTAIN** when term time is uncertain, not a favorable-cherry-picked chart. The broader birthsite IANA/true-solar, lunar calendar, certified old Chinese written source, calibrated human questionnaire, decoy baseline and prospective human blinding remain separate unfinished work.

The archived third witness uses owner temporary binary `swisseph.cpython-312-x86_64-linux-gnu.so`, SHA256 `2b3234b6678dfa5666c98e898c16ee7e8c6c8457100e293c24ce679cd4387764`, pysweph version 2.10.3.6, and pinned status checks. Compiled vendor libraries are not redistributed with project evidence. No new historical source annotation accepted; Chinese V30 remains 1289 annotations.

**Real-person blinded human predictive validations: 0. Production astrology rule promotions: 0.**
