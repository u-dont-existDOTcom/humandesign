# C32 Hellenistic continuation — independent IAU/SOFA angle audit and eastern-root verification

**25 October 2026. PARENT OBJECTIVE OPEN:** source-faithful ancient rules across all 16 traditions are only a means to the owner's original goal of frozen falsifiable, prospective, blinded human tests against chart decoys and strong nonastrology controls. Source consistency and astronomy do **not** validate human predictions (still **0**). Preserve recorded negative cases, C30 Dorotheus Lot and all C04–C31 code/tests unchanged.

## Bootstrap / branch

Read live default `universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`, then live `humandesign/AGENTS.md`; this handoff, [C32 full research report](HELLENISTIC_SOURCE_C32_INDEPENDENT_IAU_ANGLE_AUDIT_20261025.md), and [synthetic evidence](HELLENISTIC_C32_INDEPENDENT_IAU_ANGLE_PARITY_V1.json). Accepted C31 parent SHA **`453aa04c2d227d0b43d544ffa6048f3e6c347700`**. New isolated branch `research/astro-hellenistic-c32-independent-iau-angle-audit-20261025`, worktree `/home/joel/development-worktrees/humandesign/astro-hellenistic-c32-iau-20261025`. Root `tasks/ACTIVE-TASK.json` exclusive `participant-session-v1` belongs to another branch; it was not modified. All C32 changes within `docs/astrology-research-map/`.

## New and independently verified findings

- [C32 Python module](hellenistic_c32_independent_iau_angle_audit.py) uses **optional isolated PyERFA 2.0.1.5** IAU 2006/2000A `dtf2d/utctai/taitt/utcut1/gst06a/obl06/nut06a` plus independently written ecliptic-horizon geometry, with an explicit eastern horizon root. The calculation doesn't call Swiss `houses`, `sidtime` or `julday`; these are used only in a separate comparator.
- **145 synthetic locations/times**, deterministic seed **20261025**, lat ±65°, 1960–2026, have max **0.031058 arcseconds ASC**, **0.032044 arcseconds MC** difference against Swiss `houses_ex` with the SAME **assumed DUT1=0**. Swiss house-system `P,W,E,O,R` angular values agree exactly across the sample. East horizon dot >0 for all; antipodal/western candidate east-dot negative.
- Synthetic sensitivity to **±0.9 seconds DUT1** reaches **32.94 arcseconds Asc**, **14.75 arcseconds MC**. These are sensitivity probes, not observed EOP records or bounds on a given human birth chart. No actual historical dUT1, elevation, geocentric latitude correction or independent village coordinates certified.
- An earlier private disputed Ascendant was reported ~180° opposite the Swiss reference. A private *approximate location* comparison using independent mean geometry agreed with Swiss ~17 arcseconds Asc and ~11 arcseconds MC. **Never commit exact private DOB/location/angle values, nor represent unavailable original bad source code as found.** Synthetic C32 demonstrates the corresponding east-vs-west 180° class, but not the vanished original implementation defect.
- Because `Lot=ASC+Moon−Saturn (mod360)`, a 180° ASC mistake translates the Dorothean four source-positive signs into a **disjoint** set of four antipodes. This could invalidate a human cohort test, not improve it.
- A separate IANA civil-time helper preserves **ambiguous fall DST fold** (two UTC candidates) and **nonexistent spring clock** (zero), never guessing. Tested with generic synthetic 2015 America/New_York clock inputs.
- C32 stores only *synthetic data, no human chart/outcome*, and does **not** modify the C31 body provider, C30 source, production scoring or active participant-session branch.

## Next concrete research action

The pure **geometric east/west discrepancy is now strongly diagnosed**; don't spend another dozen turns merely recomputing 180°. Progress the owner goal by using a *locked* civil-time provenance policy (IANA TZDB, historical city coordinates/folds), independent Earth-orientation source for exact UT1 at historical candidate instants, and continuous angle-enclosure proof across birth-time/coordinate uncertainty. With certified natal geometry, work separately on the **feasibility** of a blinded cohort for the Dorotheus war-campaign life-event claim: opportunity strata and actual record availability. If such a cohort is unavailable, retain the source-defined rule as development and choose another historically clear Hellenistic person-level target. No human blind evaluation started or results invented.

## Reproducibility

```sh
# From worktree root, with separate optional PyERFA installation:
PYTHONPATH=/tmp/c32-independent-erfa /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c32_*.py' -v
PYTHONPATH=/tmp/c32-independent-erfa /home/joel/humandesign/.venv/bin/python docs/astrology-research-map/hellenistic_c32_independent_iau_angle_audit.py > /tmp/c32-replay.json
# Compare /tmp/c32-replay.json against the checked-in receipt after confirming dependencies.
```

PyERFA installed **only in temporary researcher directory** `/tmp/c32-independent-erfa` (not a production dependency or committed wheel). Full original IAU model information: https://www.iausofa.org/current-software and https://www.iausofa.org/cookbooks; civil/GAST reference: https://aa.usno.navy.mil/faq/GAST. The original private case and source code of earlier incorrect alternative are not committed. Exact C32 focused/full test totals and accepted Git commit are appended to report/index after final verification.

**Root objective remains OPEN.** No certification of real human military outcomes or high-stakes military, medical or personal recommendations.


## New C32 observed IERS time-scale receipt — same isolated branch

Beyond the earlier hypothetical `DUT1=0` parity, recovered IERS **20 C04** daily Earth-orientation values via a **public Simple Space Data mirror** with the raw data SHA `ed3ee86f9a6470a0f6c33e080991745069cf1a7a0899bf6fa9122d10bbd89181`; the mirror URL contains `c04_20u24` but the actual source header says `20 C04` — preserve this version distinction. Original file 5,176,575 bytes, 23,634 day0 records, 1962-01-01 to 2026-09-15. **140/145** original C32 synthetic cases have observed DUT1 coverage (five 1960–1961 not covered). Record both daily 0h UTC source records within each case in [C32 observed EOP receipt](HELLENISTIC_C32_OBSERVED_IERS_EOP_SENSITIVITY_V1.json).

`hellenistic_c32_iers_observed_eop.py` reconstructs DUT1 by interpolating **UT1−TAI rather than discontinuous UT1−UTC** across leap seconds, uses ERFA `dat` to restore TAI−UTC, and supplies the observed DUT1 both to ERFA `utcut1` and Swiss house JD `+DUT1/86400`. Verified max ERFA-Swiss error **0.031135 arcsec Asc**, **0.031873 arcsec MC**; observed DUT1 shifts from default zero reach **17.393 arcsec Asc**, **10.404 arcsec MC**. A leap-second regression at 2016-12-31 ensures a 0.5-second false interpolation is NOT introduced. Two additional research files: [source code](hellenistic_c32_iers_observed_eop.py) and [regressions](test_hellenistic_c32_iers_observed_eop.py). Raw IERS file is *not committed in public Git*; it is bundled with the owner-local ZIP and receipt embeds all sampled two-day source values. `C32_IERS_C04_PINNED_FILE` can point to the exact raw file; missing raw -> optional source-replay tests skip, not a false historical-model failure.

**No change to root task lock or person chart.** Actual historical EOP solves one portion of the old angle provenance barrier, but polar-motion correction, time-zone provenance, full interval proof and original incorrect third-party source code remain unresolved. Do not promote a human-prediction claim from numeric chart parity alone. Parent root scientific goal remains open.


## Verified publication-ready C32 checkpoint

With exact optional `pyerfa==2.0.1.5` isolated in `/tmp/c32-independent-erfa` and the SHA256-pinned IERS 20 C04 archive, **21/21 C32** and **329/329 all Hellenistic source/engineering tests passed** (exit0). The IERS file's mirror URL name is *not* a guarantee of matching 20u24 source version: header actually says 20 C04. The project Git receipt embeds full source-day values for 140 sample points, raw source is included in owner-local ZIP. Root scientifically untouched-human outcome is still **OPEN**, and `participant-session-v1` lock is unchanged.
