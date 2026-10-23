## Summary

In **Morinus Special Edition 8.0.0** (Linux x86_64 AppImage), Placidian **under-the-pole** directions can flip a small **direct** arc into a different **converse** arc when the significator's oblique ascension/descension is negative near the 0° RA boundary. I reproduced this in the running GUI using a synthetic chart and traced it to a sign conversion in the current source.

## Reproduce in the GUI

1. Create a synthetic Gregorian radix chart: **2026-03-19 06:00:00 UTC**, longitude **24° E**, latitude **45° N**, GMT offset 0.
2. In **Options → Primary Directions**, choose **Placidian (under the pole)**, **Zodiacal**, *use significator's latitude*, **Bianchini unchecked**; leave Moon secondary motion unchecked.
3. In **Options → Primary Keys**, choose static **Naibod**.
4. Open **Tables → Primary Directions**, ages **0–25**, select **Both** (direct and converse). Inspect the conjunction of the **Sun promissor** to the **Moon significator** (other enabled promissors/aspects do not matter to this particular contact).

**Observed:** the AppImage lists **Sun C→ Moon**, arc **2.295°**, date **2028-07-16**.

**Expected geometrically:** **Sun D→ Moon**, arc about **0.619°**. An independent calculation with Swiss Ephemeris 2.10.03 (Moshier, geocentric equatorial coordinates) produced:
- Moon RA `0.2547313748°`, declination `+2.2736895919°`
- Sun RA `358.7543717847°`; RAMC `290.8037360606°`
- Signed significator oblique ascension at its pole: `−1.4579065310°`
- Correct directed arc `+0.6187055618°`
- If the negative significator coordinate is instead absolute-valued: arc `−2.2971075003°`, very close to the **2.295° converse** result in the GUI. The ~0.002° difference should be checked against the AppImage's exact ephemeris/coordinate settings; it is larger than display rounding.

## Likely source-level cause

In the current `main` source commit `020492d5fce1c7a3d6b81186cef6cf04d93fb694`, [`placidianutppd.py` line 1668](https://github.com/IngenieriaAstrologica/Morinus/blob/020492d5fce1c7a3d6b81186cef6cf04d93fb694/placidianutppd.py#L1668):

```python
aodosig = math.fabs(plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO])
```

The speculum stores eastern `AO = RA − AD_at_pole`, which legitimately becomes negative near RA 0°. Its western `AODO` value, by contrast, stores the **negative** of `DO = RA + AD_at_pole` as an encoding convention. A blanket absolute value handles many ordinary western cases, but incorrectly flips the physical coordinate wherever `AO` or `DO` itself is negative.

**Potential narrowly scoped correction for the speculum fallback path** (needs regression testing in the full app):

```python
stored = plsig.speculums[primdirs.PrimDirs.PLACSPECULUM][planets.Planet.AODO]
aodosig = stored if sigeastern else -stored
```

Please **do not merely remove `fabs` globally**; western values use a different stored sign convention. The `getData()` recomputation branch already provides a signed coordinate, and needs to remain distinct.

## Extended numerical verification

I executed the **unchanged** `PlacidianUTPPD.toPlanet` method and original `PlacidianSpeculum` class (AST-loaded directly from the pinned Morinus source) against an independent signed-coordinate semi-arc/under-pole oracle on **9,600 valid synthetic conjunction cases**: all four celestial quadrants × north/south geographic latitudes × RA near 0°, near 360°, and away from the seam; deterministic seed `202610232337`.

- Unmodified Morinus source: **591 / 9,600 discrepancies**, including both hemispheres and all four quadrants; maximum angular discrepancy `73.682647°`.
- In every one of the 591 cases, the physical oblique-ascension/descension coordinate is **negative**. No other cases disagree within `1e-7°`.
- **In-memory diagnostic only** replacing that single AST expression with the hemisphere/side-aware signed interpretation: **0 / 9,600 discrepancies**, maximum residual `1.14e-13°`.

The 9,600-case test is restricted to synthetic equatorial positions, conjunctions, ordinary semi-arcs and valid under-pole crossing domains. It does **not** validate other aspect constructions, Bianchini handling, Moon secondary motion, all ephemeris modes, historical accuracy or astrology's predictive value. No upstream source code was modified by these tests.

## Build context

User-downloaded binary: `Morinus_SE-8.0.0-x86_64.AppImage` (SHA-256 `926e79b5d5494a045557ca66e3f35b2d91e9629427ffdbe959b9d9771306f4e3`); Linux x86_64, tested in an isolated X11 virtual display with TWM. The exact binary-to-source commit correspondence is not independently verified. The GUI contact was reproduced after initializing a clean application instance with a window manager; no natal/private birth data was used.

I can provide the exact synthetic test harness, per-quadrant JSON matrix, and GUI screenshots if useful. This report is about reproducible computational geometry, not event prediction.
