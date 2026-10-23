# Morinus SE × Gansten — source-level primary-directions parity

**Date:** 2026-10-23 UTC
**State:** Research-only calculation parity; full Morinus GUI/Swiss Ephemeris application NOT run; no source-to-prediction promotion.
**Owner purpose:** Continue the verified Gansten primary-direction audit in the empirical astrology project without replacing existing Ptolemy/Lilly source interpretation or fitting to known lives.

## Which program and why

**Morinus Special Edition (Morinus SE)**, public code at https://github.com/IngenieriaAstrologica/Morinus. Source commit independently pinned: \`020492d5fce1c7a3d6b81186cef6cf04d93fb694\`.

The developer's documentation explicitly supports **Placidian proportional semi-arcs, Placidian under-the-pole, and Regiomontanian position circles**. This makes it a useful comparison against Gansten's deliberately distinct historical geometries. Use the exact source build and explicit geometry/latitude/converse/time-key configuration; generic "Morinus" output is not a method definition.

## What was executed

On a Zorin Linux research scratch directory, the pinned official GitHub repository was cloned. The verifier **executed the original unchanged AST bodies** of:
- \`placidiansapd.py::PlacidianSAPD.toPlanet\` and \`PlacidianSAPD.getvars\`
- \`placidianutppd.py::PlacidianUTPPD.toPlanet\`
- \`regiomontanpd.py::RegiomontanPD.toPlanet\`
- \`primdirs.py::PrimDirs.getDiff\`

The verifier also executed the original \`placspec.py::PlacidianSpeculum\` and \`regiospec.py::RegiomontanianSpeculum\`. Nonessential application/GUI/ephemeris dependencies were replaced with minimal stubs; this is **not a complete launched Morinus application**, and source-level precision cannot certify the full GUI run. Synthetic inputs are RA/declination and local RAMC in degrees, and an exact one-point conjunction is compared with fixed-point latitude retained. Lunar secondary motion and other forecast-selection rules are off.

The independent comparator is the **previous research packet's** \`geometry_reference.py\`; its SHA-256 and all Morinus source hashes are recorded in \`MORINUS_PARITY.json\`. The two engines have different algebraic forms, including a Cartesian plane-intersection solver for Regiomontanus. The Morinus code was not modified or copied into the research repository.

## Original Gansten synthetic example

Inputs: geographical latitude +45°, RAMC 0°, fixed/significator RA 50° declination +15°, moving/promissor RA 80° declination −10°.

| Geometry | Prior independent research | Executed Morinus source | Difference |
|---|---:|---:|---:|
| Proportional semi-arc | 42.17434402835047° | 42.17434402835047° | 0° |
| Placidean under-pole | 42.20081504892782° | 42.20081504892782° | 0° |
| Regiomontanian position circle | 46.449117851278395° | 46.449117851278395° | 0° |

Also source-derived: speculum POH 25.5610956166°, signed AO/DO 42.6369460857°, Regiomontanian pole 32.7692698549°, Regiomontanian W 40.0680651914°.

## Deterministic broad grid

**Scope:** northern latitudes 10–65°, fixed point in the **eastern, above-horizon** quadrant, declinations selected to admit ordinary rising/setting, independent moving RA/declination, no real births, direct one-point conjunction, no secondary motion. Random seeds \`20261023\` (n=1,200) and \`19870502\` (fresh n=2,400).

| Comparison | Matches | Different |
|---|---:|---:|
| Morinus semi-arc vs independent proportional model | 3,600 | 0 |
| Morinus Regiomontanus vs independent Cartesian position-circle solver | 3,600 | 0 |
| Morinus under-the-pole vs independent under-pole branch | 3,564 | **36** |

The 36 mismatches were **not rounded numerical noise**; one original sample showed an arc difference of 63.2548679169°. This is a mathematical discrepancy measured under a precisely limited configuration, **not an observed prediction error or evidence about astrology's usefulness**.

## Root cause found in Morinus source

\`Morinus/placidianutppd.py\`, pinned commit, **line 1668**:
\`aodosig = math.fabs(plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO])\`

The original Placidian speculum stores an *eastern* oblique-ascension value \`RA − AD_at_pole\`, which can validly be **negative near the RA 0° boundary**. The under-pole routine then converts that negative coordinate to its absolute value, moving the reference to the wrong angular side.

For every one of the 36 mismatches, \`AODO < 0\` in the **eastern** branch and the observed arc displacement equals \`2 × abs(AODO)\`, to within \(5.3\times10^{-14}\) degrees in the fresh sample.

For a diagnostic only, replacing the absolute-value interpretation with the **signed original coordinate** recovers the independent output in all 3,600 cases. This is **not yet a validated upstream patch**: western-branch signed encoding and ecliptic aspect constructions must be preserved when designing any correction. Never simply delete the \`fabs\` globally without more tests.

The other two geometry routines agreed across the tested domain even in the 36 seam cases. Thus the finding is **specific to the exercised Placidian under-pole path**, not a claim that all Morinus primary directions are wrong.

## Reproduction and files

- \`compare_morinus_source.py\` — unchanged source methods and speculum classes with controlled dependency stubs, base example, first 1,200-case grid.
- \`diagnose_aodo.py\` — independently seeded second 2,400-case grid, root-cause classification and counterfactual.
- \`geometry_reference.py\` — prior independent research reference, unchanged.
- \`MORINUS_PARITY.json\` — source hashes, exact synthetic comparison, 1,200-case records and unmatched cases.
- \`MORINUS_AODO_DIAGNOSIS.json\` — seed/count breakdown, numerical reproduction and six representative seam failures.
- No Morinus binaries, copyrighted book pages, real human data, or secrets included.

To replay: clone the same upstream git commit beside these scripts into a sibling \`Morinus/\` directory, then use \`python3 compare_morinus_source.py\` (expected **nonzero** because 11 uncorrected Morinus discrepancies are intentionally retained) followed by \`python3 diagnose_aodo.py\` (**zero** when the predicted sign-boundary pattern is confirmed). No installation of wxPython is needed for the isolated source-method replay.

## Follow-up and stop conditions

1. Retain this as a *source-method parity finding*, separate from historical attribution and empirical evidence.
2. For eventual real software verification, run an **identified, unmodified Morinus GUI/engine build** with precisely declared natal inputs and program settings, and verify exported direction arcs/ages, especially seam cases. **NOT DONE here.**
3. Extend tests to western, lower-meridian, southern-hemisphere, different aspects, ecliptic projections, converse modes, and time keys. Preserve errors/unknowns; do not let a preset silently change the method.
4. Keep the existing Gansten/Lilly/Ptolemy source registry and all production/blinded predictive models unchanged; software agreement is not historical fidelity or evidence of real event prediction.
5. Do not publish a bug report to Morinus upstream without separate external-publication authority.

**Root-owner outcome:** OPEN (mathematically independent software check advanced; full application and historical-method coverage remain unverified).
