# Morinus SE 8 AppImage — independent GUI verification checkpoint

**Date:** 2026-10-23 UTC. **Status:** Source-method parity + actual GUI test complete in specified synthetic domains. **Predictive validation: none.**

## Where to begin
Read `APPIMAGE_GUI_VERIFICATION.md` first, then `MATH_VERIFICATION.json`. `reproduce_gui_math.py` plus `geometry_reference.py` replicate the independent Swiss Ephemeris and directional-geometry calculations (a compatible `swisseph` package is required).

## Findings
- An actual AppImage downloaded by the owner, `Morinus_SE-8.0.0-x86_64.AppImage`, SHA256 `926e79b5d5494a045557ca66e3f35b2d91e9629427ffdbe959b9d9771306f4e3`, was launched in an isolated X11 GUI. The owner desktop remained untouched.
- Normal 2000-01-01T12:00Z synthetic chart: Sun→MC 0.821° in GUI versus independent 0.821314°; Uranus-square-Moon: semi-arc 1.070° (independent 1.070941°), under-pole 1.075° (independent 1.075065°), Regiomontanus 0.993° (independent 0.993477°).
- Targeted 2026-03-19T06:00Z, 45°N 24°E chart, UTP, Zodiacal, latitude of significator retained, direct+converse: independent **Sun DIRECT Moon 0.618706°**; AppImage **Sun CONVERSE Moon 2.295°**. Separate diagnostic with absolute-valued AODO predicts converse 2.297108°. Consistent with signed oblique-ascension bug at 0° crossing; exact binary-to-source commit identity is not established.
- With a proper private window manager, the target combined GUI run was successful. Crashes in an earlier environment without a window manager do not establish an intrinsic AppImage fault.
- Standalone executable programs and source files (including the AppImage) are not committed here.

## Owner artifact / screenshots

A checked ZIP including all GUI screenshots, the math script, checks and source/edition caveats is saved directly to the owner's laptop:
`~/Téléchargements/gansten-astro/Morinus_AppImage_GUI_Parity_20261023.zip`
- ZIP SHA-256: `dad96a472d0a07950d2025de0bd4058dc8c7a63c4e321c25496cfde8ad06f52f`
- CRC/member SHA checks: pass, 13 members including `MANIFEST.json`.
- A separate `.sha256` sibling was written for local verification.

## Scope boundary and next action

The owner's immediate request to **use the downloaded AppImage** is satisfied. Do not relabel the broader astrology research as empirically validated. Remaining optional engineering: verify exact compiled source/build and ephemeris, extend branch tests across western/southern/lower quadrants and other options, and consider a source patch and controlled upstream bug report only under explicit external-publication permission. Work remains isolated on this research branch; production chart models and other source lanes were not modified.
