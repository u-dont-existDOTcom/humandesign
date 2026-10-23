# Morinus under-the-pole AODO sign regression — research checkpoint

**Date:** 2026-10-23 UTC

**User request:** Continue the Gansten/Morinus research and send a bug report to the maintainers.

## Public bug report (confirmed submitted)

**Morinus Special Edition issue #3:** https://github.com/IngenieriaAstrologica/Morinus/issues/3

- Status at readback: OPEN.
- Published title: `Placidian under-the-pole: abs(AODO) reverses direct/converse near 0° RA (Morinus SE 8.0.0)`.
- Published issue body read back and **byte-for-byte verified** against `MAINTAINER_ISSUE.md`.
- UTC creation timestamp: 2026-10-23T23:42:45Z.
- Published body SHA-256 (excluding trailing newline): `820460dc9c6c59e5637e78f693fe6fc9c3537b01f0d83e5a10ab61cc3d1f2130`.
- Submitted through the owner's existing authenticated GitHub CLI when the ChatGPT GitHub integration could not write to the external repository (HTTP 403). No additional permission grant or credential sharing was required.

## New expanded numerical validation

The **unmodified official source** in `IngenieriaAstrologica/Morinus`, commit `020492d5fce1c7a3d6b81186cef6cf04d93fb694` (reverified as `main` head), was tested using its original `PlacidianUTPPD.toPlanet` method and `PlacidianSpeculum` classes on a deterministic matrix of **9,600 valid synthetic cases**.

Test construction: northern and southern latitudes (±8–65°), all four sky quadrants (eastern/western × above/below horizon), significator RA near 0°, near 360°, or away from both, randomized nonpolar declinations and moving RA. Conjunction-only, no Moon secondary motion, with the target's bodily latitude retained (corresponding to the specific subzodiacal/no-Bianchini code path). Seed: `202610232337`.

| Metric | Result |
|---|---:|
| Valid synthetic cases | 9,600 |
| Mismatches, unchanged source vs independently constructed signed-AODO reference | 591 |
| Mismatches where physical AODO/DO is negative | 591 / 591 |
| Mismatches for any other cause in tested domain | 0 |
| Mismatches with branch-sensitive signed-AODO **in-memory diagnostic**, no upstream file modified | 0 / 9,600 |
| Max angular discrepancy in original | 73.6826474257° |
| Max corrected residual | ~1.14 × 10⁻¹³° |

**Proposed correction is specific to the `placidianutppd.py:1668` fallback:** the source's western speculum stores `−DO` by convention whereas eastern stores `AO`. Thus use `raw` on the east side and `−raw` on the west side; do not simply delete `fabs` for all cases. Alternate `getData()` branches need separate validation.

## Actual application evidence from prior stage

The user's downloaded `Morinus_SE-8.0.0-x86_64.AppImage` was launched on a separate virtual X display with TWM on Zorin OS. Synthetic 2026-03-19 06:00 UTC, 45° N, 24° E, under-the-pole, zodiacal, significator latitude retained, both direct and converse, static Naibod:
- GUI: Sun C→ Moon **2.295°**.
- Independent signed-coordinate calculation: Sun D→ Moon **0.618706°**.
- Predicted absolute-value artifact: converse **2.297108°**.

The ~0.002° difference between GUI and independent predicted converse magnitude exceeds display rounding; binary ephemeris/build provenance and other settings remain unverified.

Earlier GUI evidence/screenshots and reproducible astronomy are separately retained at `~/Téléchargements/gansten-astro/Morinus_AppImage_GUI_Parity_20261023.zip`. The actual source-level report and comparison are committed in earlier isolated research branches.

## Unresolved limits and next steps

- This is an **engineering calculation bug finding**, not empirical validation of astrology or proof of a historical method's attribution.
- An in-memory diagnostic is not a released patch; no upstream source or the owner's production chart engines were changed.
- Extend comparisons to other aspects, zodiacal no-latitude and Bianchini options, lunar secondary motion, circumpolar charts, and precise ephemeris provenance before shipping a universal correction.
- The public upstream issue is now filed. Check maintainer feedback when requested; any maintainer-requested follow-up can use the archived reproducibility evidence.
- Do not use a named person's chart or retrospective life events to select the method.

**Root goal disposition:** The explicitly requested maintainer bug report is COMPLETE, and a wider multi-method research project remains OPEN. No owner intervention is needed for the submitted report.
