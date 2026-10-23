# Morinus SE 8.0.0 AppImage — GUI verification of Gansten primary directions

**Date:** 2026-10-23 UTC. **Scope:** actual downloaded Linux AppImage, isolated Xvfb GUI on the user's authorized Zorin laptop; only invented test charts. NOT a predictive-astrology validation, historical-source proof, or universal software audit.

## Tested binary and environment

- Original user-downloaded executable (left unchanged): `Morinus_SE-8.0.0-x86_64.AppImage`
- **SHA-256:** `926e79b5d5494a045557ca66e3f35b2d91e9629427ffdbe959b9d9771306f4e3`
- Linux, isolated X11 virtual display :86 and separate temporary HOME; TWM window manager added for final seam test. The owner's ordinary desktop and Morinus instance were not controlled.
- Comparison astronomy: locally available Swiss Ephemeris Python binary 2.10.03 with `FLG_MOSEPH` requested and confirmed in returned flags on independent Sun-RA test. This does **not** prove which ephemeris flags or files the downloaded AppImage actually used.
- Earlier source-method audit: separate `IngenieriaAstrologica/Morinus` GitHub checkout at `020492d5fce1c7a3d6b81186cef6cf04d93fb694`. The AppImage's exact correspondence to that source commit was **not** verified.

## GUI test 1 — three historical direction geometries

Disposable chart: **2000-01-01 12:00:00 UTC**, latitude **45° N**, longitude **0° E**, Gregorian, radix. The GUI computed primary-direction lists successfully with the **Naibod static time key**. For method parity on Uranus-square-Moon: **zodiacal**, both promissor and significator latitude projected to the ecliptic, and other aspects enabled; lunar secondary motion unchecked. GUI values are displayed to three decimals; the source formulas carry more precision.

| Directed event | Method | Actual AppImage GUI arc | Independent reference arc |
|---|---|---:|---:|
| Sun body to Midheaven | Semi-arc, UTP and Regiomontanus | 0.821° | 0.8213138100° (Swiss RA−RAMC) |
| Uranus square Moon | Proportional semi-arc | 1.070° | 1.0709410726° |
| Uranus square Moon | Placidean under-the-pole | 1.075° | 1.0750653720° |
| Uranus square Moon | Regiomontanus | 0.993° | 0.9934768727° |

The semi-arc screenshot displays `1.070`, which differs from the independent rounded-to-three-decimals result `1.071` by about `0.001°`; do not call this exact precision parity. The other results match within the display resolution. The Sun–MC direction matches when rounded to three decimals.

## GUI test 2 — targeted RA/oblique-ascension 0° seam case

Disposable chart: **2026-03-19 06:00:00 UTC**, latitude **45° N**, longitude **24° E**, Gregorian. Method: **Placidean under-the-pole**, Zodiacal, **retain the significator's bodily latitude**, direct AND converse, range ages **0–25**, Naibod key, lunar secondary motion unchecked.

A separately computed Moon-significator position has RA `0.2547313748°`, declination `+2.2736895919°` and correctly **signed** eastern oblique-ascension `−1.4579065310°`; the moving Sun RA is `358.7543717847°`. The independently computed under-the-pole Sun→Moon direction:

- Correct signed-coordinate **direct** arc: `+0.6187055618°`.
- Absolute-value transformation erroneously changes the angular displacement to `−2.2971075003°`, interpreted as **converse 2.297°**.

**Actual AppImage GUI:** displays an un-aspected **Sun C→ Moon** contact at **2.295°**, dated 2028-07-16 under Naibod; the early sorted displayed list has **no corresponding Sun D→ Moon 0.619°**. The 0.002° disagreement between predicted and displayed converse magnitudes exceeds simple 3-decimal rounding; the binary's exact ephemeris/co-ordinate inputs need separate verification. The **direction reversal and approximate displaced magnitude match** the source-level `math.fabs` diagnosis.

This is substantially stronger evidence for an **under-the-pole calculation/sign-handling problem in the tested AppImage configuration** than source reading alone. However the result remains one controlled graphical seam case, not proof all versions, all quadrants, other geometry families or real-chart results are affected.

## Other GUI/runtime observations

- Before a private window manager was configured, closing result windows via X11 automation triggered one GTK segmentation fault and one GObject protection fault. **These are not established program faults in an ordinary desktop setup.** With TWM and a fresh AppImage process, the targeted **both-direction** list completed and remained open.
- In the earlier no-WM run, opening the program's ordinary Positions table produced a Python `TypeError` in `positionswnd.py` line 514. It was not reproduced with TWM and does not establish a primary-directions defect.
- No user birth data, chart-based event fitting, production changes or external bug publication.

## Evidence archive and next engineering work

Screenshots and independent reproducer accompany this report. The user's actual AppImage is not included. Source repository from previous work remains unmodified.

Follow-up engineering (not completed): check exact binary-versus-source provenance and ephemeris mode; reproduce across western, southern and lower-horizon quadrants; compare sign wrap of both traditional converse and other aspect constructions; determine a branch-safe fix without blanket removal of `fabs`; then consider asking the user about an external upstream issue, if appropriate. Keep any prospective human test separately preregistered and blinded.

**Outcome reached this turn:** yes, the user's downloaded AppImage was run and tested through the actual GUI, including the targeted sign-boundary case. The app's derived forecast ages are not evidence that astrology predicts events.
