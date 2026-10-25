# C32 — IAU 2006 independent Ascendant and Midheaven parity; 180° horizon incident isolated

**2026-10-25. OWNER OUTCOME STILL OPEN:** historical Hellenistic astrology is one of 16 source traditions in `humandesign`; source algorithms must become independently frozen, falsifiable, prospective predictions against untouched consenting human data with matched decoys and negative cases. The C30 Dorotheus *Lot of Expedition* is a development candidate, not evidence of predictive validity. **0 human predictive validations, 0 production scorer changes, root participant-session lock untouched.**

## Main result: a genuinely different astronomical implementation agrees with Swiss

The C31 research module `hellenistic_c31_expedition_chart_bridge.py` checked a five-point Meeus-style **mean** sidereal geometry against Swiss, agreeing to 0.324' Asc and 0.206' MC but still lacked nutation and independent modern Earth-rotation modeling. C32 now adds **SOFA/ERFA's IAU 2006 precession plus IAU 2000A nutation**, accessed through **PyERFA 2.0.1.5**, as a genuinely separate sidereal-time implementation and a separately coded eastern-horizon/ecliptic intersection. There is **no call to Swiss `houses_ex`, `sidtime` or `julday` inside the ERFA angle calculation**. Swiss `houses_ex` is invoked *only for the comparison target*.

For each UTC test instant:
1. SOFA's `dtf2d → utctai → taitt` constructs UTC, TAI and TT time scales; `utcut1` forms UT1 with **explicitly assumed UT1−UTC=0 seconds** (NOT observed historical EOP).
2. `gst06a` computes Greenwich apparent sidereal time using IAU 2006/2000A; `obl06 + nut06a.Δε` gives true ecliptic obliquity.
3. The independent observer-horizon/ecliptic intersection resolves **the eastern rising root** by a positive dot product with the local east vector, and the upper meridian/ecliptic intersection gives MC. The entire root-selection process is independent of Swiss's internal house-cusp code.
4. Swiss `houses_ex(jd_ut, latitude, east_positive_longitude, hsys=P, flags=0)` provides comparison Asc/MC. Distinct Swiss house-system choices `P,W,E,O,R` are independently checked for invariant Asc/MC.

Canonical original standards and documentation: [IAU/SOFA current software](https://www.iausofa.org/current-software) (IAU 2006/2000A model distinction), [IAU/SOFA tools for Earth attitude](https://www.iausofa.org/cookbooks), [USNO sidereal-time and UT1/TT notes](https://aa.usno.navy.mil/faq/GAST), and [Swiss Ephemeris original angle/house programming documentation](https://www.astro.com/ftp/swisseph/doc/swisseph.htm).

## Fully reproducible public *synthetic* parity receipt

`hellenistic_c32_independent_iau_angle_audit.py` generates 5 fixed C31 synthetic points plus **140 deterministic new synthetic cases** using seed **20261025**. Dates span **1960–2026**, observer latitudes **±65°** and longitudes **±179°**. None are selected from people, observations or owner biography. Full event list and mathematical results: [C32 public synthetic receipt](HELLENISTIC_C32_INDEPENDENT_IAU_ANGLE_PARITY_V1.json). Source code and receipt are stored in Git; the privately known incident's DOB/location are explicitly **not** included.

| Verified measurement (145 synthetic cases) | Result |
|---|---:|
| ERFA IAU 2006/2000A vs Swiss maximum Ascendant difference | **0.031058 arcseconds** |
| ERFA IAU 2006/2000A vs Swiss maximum Midheaven difference | **0.032044 arcseconds** |
| Swiss `P,W,E,O,R` house-system variation in Asc/MC | **0 arcseconds** |
| Eastern-root east-vector dot product, minimum | **+0.5182** (all on correct horizon side) |
| Max Asc shift with artificial UT1−UTC perturbation of ±0.9 s | **32.94 arcseconds** |
| Max MC shift with artificial UT1−UTC perturbation of ±0.9 s | **14.75 arcseconds** |

The **0.03-arcsecond numerical parity** applies to the same assumed UT1, observer geodetic coordinates and convention within this declared sample. The *±0.9-second* exercise is a sensitivity demonstration, **not** a source of observed historical DUT1 or a universal uncertainty bound. Therefore it must **not** be combined with the tiny parity residual to declare a future person's Ascendant accurate to 0.03 arcseconds.

The independent C32 code and receipt also save the exact PyERFA compiled-extension binary SHA, Swiss extension SHA and version strings so the software provenance can be reconstructed. PyERFA was installed to a **temporary isolated path**, not into `humandesign`'s production requirements, packages or runtime. C31's pinned `sepl_18.se1` and `semo_18.se1` strict Moon/Saturn evidence remains separate and intact; Swiss house geometry itself does not prove provenance of planetary ephemeris files.

## Known earlier 180° Ascendant incident — status rather than overclaim

A previously reported alternative angle calculation produced an Ascendant **approximately 180° away from the Swiss result**. A private, read-only sanity comparison using the same historical case with an approximately reconstructed observer coordinate agrees with Swiss to about **17 arcseconds for Asc** and **11 arcseconds for MC**, using a *different Meeus mean-geometry method*. The incorrect alternative lies approximately at the opposite/western horizon root. **No personal birth instant, site coordinates, name or chart position is included in C32 public files.** The old alternative implementation, its exact coordinate-input receipt and its original raw computation are **not** preserved here; the exact coding mistake therefore cannot be independently reproduced or attributed conclusively to a particular line.

C32 **demonstrates** an exact 180° east/west mathematical error mechanism on every one of its 145 synthetic horizon constructions: the antipodal ecliptic crossing has **negative** east-vector dot product (setting, not rising). The independently computed rising point always has positive east-vector dot product. That is a compelling diagnostic class for the historical disagreement but **not** proof of the absent previous program's source code defect.

This matters for the C30 Lot-of-Expedition indicator: adding 180° to the Ascendant adds 180° to the calculated lot. Its four asserted sign exposures **Aries, Scorpio, Capricorn and Aquarius** have **no overlap** with their 180° antipodes **Libra, Taurus, Cancer and Leo**. A wrong horizon root therefore selects a *disjoint positive-exposure group*, which could silently invalidate any statistical test. Regression safeguards prevent that silent promotion.

## Civil-time folds/gaps — exercised, not overfitted

The new `resolve_civil_time_without_guessing` checks both `fold=0` and `fold=1` against an IANA timezone and performs UTC↔local roundtrips. On generic **2015 America/New_York** synthetic local clocks, 01:30 on the November fallback day generates **two distinct UTC instants**, whereas 02:30 on the spring-forward day generates **zero** valid local instants. A normal winter time produces one UTC instant. It does not guess a birth timezone, silently choose a fold, or adjust nonexistent civil times. The exact historical local-clock/birthplace provenance for any real participant still requires separate independent proof and a locked TZDB version.

## Admission, remaining issues and practical next phase

**Completed:** direct independent IAU 2006/2000A vs Swiss numerical parity on 145 synthetic cases; east/west horizon sign resolved and sensitivity measured; five independent Swiss house divisions yield the same geometric angles; synthetic DST fold/gap handling; regression tests and machine-readable full receipt.

**Still open:** historical DUT1/EOP data for actual cohorts, exact historical IANA local time and birthplace geodetic coordinates, the missing original old-algorithm receipt, thorough extremes/high-latitude and crossing-boundary parity, and rigorous continuous uncertainty envelopes for actual chart inputs. Most importantly, the modern war-campaign observable needs a feasible untreated cohort, records, sufficient outcome prevalence and a preregistered source-defined score and strong nonastrology comparison.

The active root project `participant-session-v1` explicitly excludes using uncertified angles in strong confirmatory claims; **C32 does not change that guard**. No new owner requirements were added and no paid services, private human records, calculated future military advice or horoscope interpretation entered the source research.

**C32 deliverables:** `hellenistic_c32_independent_iau_angle_audit.py`, `HELLENISTIC_C32_INDEPENDENT_IAU_ANGLE_PARITY_V1.json`, `test_hellenistic_c32_independent_iau_angles.py`, `HELLENISTIC_CONTINUATION_C32_20261025.md`. The dataset is generic deterministic synthetic data (no photographs, scanned books or proprietary binaries committed).


## Follow-up C32 observed-EOP pass — replaced a hypothetical clock assumption with actual recorded values

After the strictly `DUT1=0` synthetic parity, I retrieved **IERS 20 C04 daily Earth-orientation samples** via [the public Simple Space Data mirror](https://www.simplespacedata.org/eop/iers/c04_20u24/latest/EOP_C04_one_file_1962-now.txt), linking to the [official IERS product catalogue](https://data.iers.org/eop.php) and [IERS C04 metadata](https://datacenter.iers.org/versionMetadata.php?filename=latestVersionMeta%2F254_EOP_C04_20u24.62-NOW254.txt). The direct hpiers host timed out from the authorized local machine; the mirror succeeded. **The actual file header says `IERS 20 C04` (not `20u24`)** even though the mirror URL path contains `c04_20u24`; these are not assumed identical edition identities. This exact **5,176,575-byte** source file is pinned SHA-256 **`ed3ee86f9a6470a0f6c33e080991745069cf1a7a0899bf6fa9122d10bbd89181`**, 23,634 consecutive daily 0h-UTC records **1962-01-01 through 2026-09-15**. Raw original data is not committed; the accompanying locally delivered research ZIP contains the pinned raw file and the public Git receipt includes the exact paired daily source records required to independently reproduce every used interpolation.

**Method:** [C32 observed EOP module](hellenistic_c32_iers_observed_eop.py) parses and hashes the complete daily IERS series and takes each same synthetic timestamp from the C32 145-case audit. Because `UT1−UTC` jumps at leap seconds, it **does not directly interpolate that discontinuous column**. It subtracts the SOFA/ERFA `TAI−UTC` value for each adjacent 0h day, linearly interpolates the continuous `UT1−TAI` quantity, then restores `TAI−UTC` at the queried instant. A dedicated test checks **2016-12-31 → 2017-01-01** and rejects the approximately 0.5-second fake step that naive `UT1−UTC` interpolation would introduce at midday.

The same observed `DUT1` is supplied independently to ERFA's `utcut1` and to Swiss `houses_ex` through a Julian date shifted by `DUT1/86400` days. Their numerical angle outputs are compared without inspecting or tuning any real birth chart, event or outcome.

| Observed-IERS result | Verified synthetic-only measurement |
|---|---:|
| Synthetic cases with both adjacent daily EOP rows | **140 of 145** |
| Five samples unavailable | **1960–1961**, before official 1962 record start |
| ERFA vs Swiss maximum Asc residual using recorded DUT1 | **0.031135 arcseconds** |
| ERFA vs Swiss maximum MC residual using recorded DUT1 | **0.031873 arcseconds** |
| Largest actual recorded-EOP shift from naive DUT1=0 in Asc | **17.393 arcseconds** |
| Largest actual recorded-EOP shift from naive DUT1=0 in MC | **10.404 arcseconds** |

This is materially stronger evidence for *time-scale handling* than merely varying DUT1 by an arbitrary ±0.9 seconds: the comparison now uses IERS-recorded (mirrored, version-pinned) UT1 samples. It **still does not use polar-motion x/y, celestial-pole dX/dY corrections, geocentric versus geodetic latitude adjustments, subdaily observed EOP interpolation, or exact original human-location/timezone provenance**. The interpolation is a documented approximation between daily observations; formal daily UT1 uncertainties are preserved in the receipt, not converted into unwarranted exact angle claims.

Full self-contained [synthetic observed-EOP receipt](HELLENISTIC_C32_OBSERVED_IERS_EOP_SENSITIVITY_V1.json), with each case's two tabulated daily records and leap-TAI conversion terms: SHA-256 **`62b840585b63514144bf84c03f33981cbab0aafbab85f722dd74db0cd3a9c130`**. No real-person natal inputs or human outcomes in the dataset.

**Net admission:** independent angle mathematics and time-scale source parity are substantially supported for this restricted synthetic domain; the previously reported 180° discrepancy is an east/west horizon-choice error class, but the original incorrect third-party code is not available for direct defect tracing. Confirmatory birth-chart prediction remains blocked on independently provenance-checked time and geolocation, proper EOP/geometry boundaries and genuinely prospective human outcome validation.


## Final C32 test and reproducibility receipt

- Complete source-only historical/engineering suite: `PYTHONPATH=/tmp/c32-independent-erfa C32_IERS_C04_PINNED_FILE=/tmp/c32-eop-c04-mirror.txt /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py'` — **329/329 passed**, exit zero (**308 inherited C31; 21 new C32**).
- Focused C32 IAU and observed-IERS checks: `test_hellenistic_c32_*.py` — **21/21 passed**, includes exact public synthetic replay and original pinned EOP raw-source hash and leap-second proof.
- The raw version-pinned IERS 20 C04 source is 5,176,575 bytes, source SHA-256 `ed3ee86f9a6470a0f6c33e080991745069cf1a7a0899bf6fa9122d10bbd89181`, deliberately **not committed** as a changing third-party bulk resource; the complete same source bytes are in the owner-local ZIP for exact replay, and the public study receipt stores every used source-day pair.
- Independently regenerated DUT1=0 synthetic receipt source SHA-256 `332faa955f755adfd9f703c82695eb6c46d5adb1d7463095068e2fb77a72e1ff`. Observed-IERS corrected self-contained receipt source SHA-256 `62b840585b63514144bf84c03f33981cbab0aafbab85f722dd74db0cd3a9c130`.
- In an environment lacking PyERFA or the exact raw IERS archive, optional live replay checks deliberately skip, while versioned receipt/semantic/source invariants still run. This prevents claiming a clean-checkout reconstruction was executed without its required published inputs.
- This is **not** a preregistered study or a successful prediction of any person; real-human validation count remains **0**, and the root exclusive participant task and production scorer remain unchanged.
