# File-backed Swiss Ephemeris 2.10 / BaZi JieQi fourth model check — 2026-10-21

## Method and evidence type

This is an **astronomical software source comparison on 36 wholly fictional fixed UTC+8 reference clocks**, not a real person's horoscope, original printed BaZi authenticity or behavioral prediction. The preceding project sources remain unchanged: the accepted Chinese historical text V30 index records **230 BaZi +1059 ZiWei =1289 documentary notes**; the accepted 480 random +36 boundary two-library parity fixture and the third Moshier source report are frozen on previous separate branches. Neither the existing 73,049-day lunar-date scan nor 312 synthetic Iztro chart test was rerun.

A local **Swiss Ephemeris compressed planetary file `sepl_18.se1`** already existed in the owner's authorized `/home/joel/humandesign/data/ephemeris`, SHA256 `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66` (484061 bytes). The repo's source manifest documents `aloistr/swisseph` commit `3fd0f956d73898b91cc4f67cf18b21af656d1342`. The Moon file `semo_18.se1` SHA `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7` is also source pinned but not counted as additional independent Sun evidence. No compiled library or compressed ephemeris file was modified or redistributed.

Using already source-pinned `pysweph 2.10.3.6` binary SHA `2b3234b6678dfa5666c98e898c16ee7e8c6c8457100e293c24ce679cd4387764`, each calculation explicitly requested **`FLG_SWIEPH | FLG_SPEED` (258)** and checked actual returned flags **258**; failed flags cause an exception instead of Moshier fallback. Swiss Ephemeris Moshier from the previous study returned **260** and did not read the file-backed planetary kernel. These are **two different numerical backends within the same Swiss Ephemeris software family**, not wholly independent observational sources.

Both calculate the **apparent geocentric tropical ecliptic Sun longitude of date** using Julian day in UT, with fixed reference UTC+8 shifted eight hours backward. Internal ΔT, equinox, precession, nutation and historical or future UT1−UTC conventions are not independently verified here. A millisecond numerical bisection residual does **not** establish millisecond astronomical accuracy or historical Chinese ephemeris equivalence.

## Results: same six preselected source solar-term target crossings

| Date | Moshier to SWIEPH change | lunar-python first new month/year pillar minus SWIEPH |
|---|---:|---:|
| 2023-02-04 | +0.640513 seconds | −0.163007 seconds |
| 2026-01-05 | +0.470568 seconds | +0.243651 seconds |
| 2026-02-04 | +0.171877 seconds | −0.222468 seconds |
| 1912-12-07 | −0.403617 seconds | −0.027604 seconds |
| 2057-08-07 | −0.540088 seconds | **−10.591710 seconds** |
| 1965-12-07 | +0.730636 seconds | −0.629827 seconds |

Within these six selected dates, SWIEPH and Moshier numerical Sun-longitude crossings are within 0.8 s. At **five of six**, the independently implemented lunar-python first altered-pillar second is also within 1 s of SWIEPH. At **2057-08-07**, file-backed SWIEPH crosses the 135° apparent solar-longitude target around **07:34:10.591 (fictional reference UTC+8)**, while lunar-python first changes month at **07:34:00** and sxtwl changes near **07:33:09.603**. This 2057 example is an independently reproducible **software disagreement**, not a certified human chart error rate; exact printed BaZi Chinese conventions and external observatory truth still require adjudication.

All **36** previously selected synthetic clocks were checked again without adding favorable test cases. **31 of 36** have compatible GanZhi year/month from both calendar libraries and pre/post numerical solar-term status from both Moshier and SWIEPH. The same **five** remain NONUNANIMOUS, **not** 5/36 randomly sampled real birth errors. The extra case remains at **2057-08-07 07:34:09**, when both calendar libraries have already assigned the next month but the SWIEPH Sun longitude remains **below 135°**, so both SWIEPH and Moshier show *preterm*. This falsifies the simplistic claim that two agreeing calendar libraries necessarily identify the same exact astronomical JieQi instant.

The source report `BAZI_FOURTH_SWIEPH_6_TERMS_36_FICTIONAL_CLOCKS_V1.json` SHA256 **7826f65e9dbff6142064a356c55c61a0ba659d423490bb59775dd0f563dd7e0d** preserves the six root times, every original 36 clock, explicit source-named year/month outputs, solar longitude residuals, actual flags258 and all five abstentions; the original accepted third and two-source fixture hashes are unchanged.

## Interpretive and methodological constraints

The older `sxtwl` calendrical day-only year/month API must not be treated as an exact-term second; the first two-source study corrected date-only month/year assignments using `getJieQiJD`, but differences from independent ephemeris remained. SWIEPH uses compressed DE-derived planetary source files and can improve precision over Moshier; both share the Swiss Ephemeris code and astronomical convention assumptions. Neither is a separately authenticated ancient Chinese almanac, independent modern observatory timing bulletin, or proof of human personality correlations.

**Next discriminating action:** independently compare the fixed UTC+8 2057-08-07 exact apparent 135° crossing against a documented original **JPL SPK/DE440 kernel or Hong Kong Observatory solar-term timestamp**, with precise time scale conversion and independently verified astronomical/geographic conventions. If this is unavailable or the two sources disagree, retain a narrow abstention window instead of choosing a preferred prediction. More broadly integrate established IANA birthsite/timezone and true-solar policy bridge (already on other branches) with the verified year/month Four-Pillar logic on synthetic examples before making *any* real-person interpretation. Original personality questionnaires, calibration, decoy/source prediction freeze and prospective untouched consenting real humans remain untested.

**Actual real-person forward/reverse blinded predictions validated: ZERO. Astrology runtime rule promotions: ZERO.**
