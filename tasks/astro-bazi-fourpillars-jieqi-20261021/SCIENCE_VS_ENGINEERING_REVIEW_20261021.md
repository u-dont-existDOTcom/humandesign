# BaZi Four-Pillar year/month/day/hour JieQi source engineering audit — 2026-10-21

## What was actually measured

This experiment compares **two independent software libraries**, not astrology’s claimed effects in people and not independent validation of the historical Chinese original. Previous Zi Wei source-only V30 accepted **BaZi230 + ZiWei1059 = 1289 documentary Chinese annotations** in a separate historical text lane. This engineering branch leaves that index **unchanged**, pinned exactly SHA256 `6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de`.

External software versions are `sxtwl==2.0.7` and `lunar-python==1.4.8`, both previously independently used for Chinese lunar date comparison. The exact library source files, including extension-binary **hashes and byte counts, but not the binary files themselves**, are recorded in the committed result fixture. The libraries are two separate computational implementations, **not two independent ancient text editions** or proof of astronomical correctness.

Tests concern fictional **whole-second Gregorian reference-clock timestamps evaluated as UTC+08:00**. No real person's DOB/place/location appears. No historical IANA timezone, daylight time, leap-second, local apparent or mean solar time, China versus birthplace reference-calendar resolution, lunar New Year versus Li Chun policy inference, or full source-specific chart interpretation is performed. Year: solar **Li Chun**; month: **Jie** solar terms; day: midnight with `lunar-python EightChar sect2`; hour: fixed local-reference two-hour branch; all choices are declared rather than claimed universally traditional.

## 480 deterministic synthetic dates

Random seed `20261021`, 40 calendar date/hour draws for each of 12 nonprivate example years: 1901, 1912, 1937, 1965, 1985, 2000, 2023, 2025, 2026, 2036, 2057, 2090, with minute30 second0. All **480 full year/month/day/hour stem-branch outputs** retained in `BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json`; source fixture SHA256 **bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e**.

Naively using `sxtwl.fromSolar(y,m,d).getYearGZ(False)` and `getMonthGZ()` as the exact-birth year/month disagrees with `lunar-python EightChar` in **8/480**. All eight were dates when a solar-term transition happened after the sampled birth time. The source `sxtwl` date-level GanZhi returns the *post-transition day's* year/month from the start of that civil date rather than preserving the precise second of transition. This is **not evidence the library is generally wrong**: `sxtwl.getJieQiJD()` supplies a precise, albeit independently unverified, transition timestamp.

When `sxtwl` source year/month are taken from the **previous day only if the fictional clock is strictly before that precise day’s JieQi**, all **480/480** software year/month/day/hour outputs agree with the second independently pinned implementation. This is a *comparison adapter*, not yet a certified historical natal computation or user-selected calendar policy.

## Precision counterexamples: six dated solar-term crossings, 36 synthetic samples

For these six deliberately nonrandom solar-term transition dates, preserve original `sxtwl.JD2DD(getJieQiJD())` timestamp, and use a **binary search of the lunar-python Four-Pillar outputs to the first second of the changed month/year**. Test samples 10 minutes, 60 seconds and 1 second before and after the sxtwl timestamp (6 clocks per date; 36 total):

| Original solar-term date | Difference: lunar-python switch versus sxtwl term | Disagreeing sample |
|---|---:|---|
| 2023-02-04 | +12.143829 seconds | 10:42:21 |
| 2026-01-05 | +16.647186 seconds | 16:22:54 |
| 2026-02-04 | +16.607216 seconds | 04:01:52 |
| 1912-12-07 | −0.093262 seconds | none sampled |
| 2057-08-07 | +50.396576 seconds | 07:33:10 |
| 1965-12-07 | −0.080078 seconds | none sampled |

Of 36 deliberately chosen **precise-source boundary** samples, **32/36 agree and 4/36 disagree**. All four disagreeing records and the independent full four-pillar outputs remain in the fixture; software must return `ABSTAIN_DIFFERENT_GANZHI_WITNESSES`, NEVER silently average, round to whichever is more favorable, or report a deterministic historical chart. For example, at the **fictional fixed UTC+8 reference clock 2026-02-04 04:01:52**, `sxtwl` gives year 丙午/month 庚寅, while `lunar-python` gives year 乙巳/month 己丑, with identical day 己酉/hour 丙寅. This is a chart-feature disagreement, not a human prediction.

The +12s, +17s and +50s boundary offsets may arise from different astronomical ephemerides, calculation approximations, rounded table conventions, or bugs. **This work does not establish which library’s exact solar-term second is astronomically correct.** Those offsets should not be generalized from these six deliberately chosen dates to arbitrary centuries, longitudes, ephemerides or historical calendar systems. The existing lunar-date 2057 disagreement (Sep–Oct) is a separate documented issue; this new 2057-08-07 **GanZhi term time** discrepancy must not be conflated with it.

## Honest readiness and acceptance

This is a reproducible **engineering result**: original library versions/source hashes, complete fictional test inputs/results, a transparent dual-output abstention interface, deterministic source switch detection, focused tests including package-version-mutation and witness corruption, and a cold-replay portable archive. It is **not** an authoritative Chinese horoscope calculator for real foreign birth data, not verification of early Chinese woodblocks, and not scientifically valid behavior/life predictions.

Already-existing independent work includes source-limited Zi Wei fourteen-main-star charts, Chinese lunar date agreement tests, civil birthplace timezone/IANA conversions with policy ambiguities, and a purely synthetic score/readiness protocol. Do not repeat those accepted studies. The actual blockers for untouched humans remain the fully anchored birth-input/timezone/calendar policies, complete selected chart-feature computation, source-conditioned psychosocial question mapping, scoring/calibration, prespecified chart decoys and nonastrological baselines, and consent plus pre-response version/prediction freeze. **Zero** source or engineering records can be counted as human predictive successes; no user/third-party biography should be included in this public repo.

**Human blinded chart-to-response validations: 0; production astrology promotions: 0.**
