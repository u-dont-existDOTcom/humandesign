# Independent Regiomontanian pole reconstruction — verified source and arithmetic

25 October 2026. **Root owner goal remains OPEN:** develop calculable, historically differentiated Western/Hellenistic/Jyotish/Chinese and other astrology systems; freeze falsifiable chart-derived predictions and independently test them in untouched forward-blind human evidence against matched controls. This is a single historical/mathematical Western subtask, **not human predictive validation**.

## Historical source hierarchy

The digitized **1667 Argoli** *Primi mobilis tabulae* original volume (`primimobilistab00argogoog`, 107-leaf excerpt, stopping at original printed p.95, from Google/Internet Archive, SHA-256 `b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d`) is preserved in `primary_1667_volume/`; three original plates are rendered in `primary_1667_pages/`.

The printed original Argoli pages **3, 7, 23** show references to Regiomontanus's rational construction, tables of rectangular/oblique ascension, position circles and pole-elevation interpolation. This supports attribution to a **family of methods**. **Do not silently call this the original 1610 Argoli text:** the 1610 original scan is located in Google Books (ID `-zhmAAAAcAAJ`); copies of 1644 in Gallica are known but have not been exhaustively collated against the *later* 1667 printing.

**Rumen Kolev**, *William Lilly and the Algorithm for His Primary Directions* (secondary modern mathematical research; `https://www.babylonianastrology.com/downloads/Lilly2.pdf`, reviewed pages 12–19), provides a modern explicit trigonometrical fictitious-pole construction and a numerical example. Those expressions are properly attributed to **Kolev's reconstruction**, not claimed as verbatim equations in Argoli's 1610 work. The secondary paper is linked but **not reproduced** here. See `PRIMARY_SOURCE_SCOPE.md` for exact source/evidence distinctions.

## New independently implemented mathematical model

`src/hdmatch/astrology/regio_pole_independent.py` computes the significator's zenith distance and Regiomontanian pole, its ascensional difference, fictitious RAMC, the promissor's adjusted ascensional difference, and the resulting forward arc. This uses an explicit **trigonometric pole/horizon path**, not the project's earlier Cartesian intersection code. Input is synthetic RA/declination/RAMC/latitude, and invalid or ambiguous meridian/horizon geometries fail explicitly.

This model deliberately omits ecliptic term and zodiacal ray projections, full Argolus/Lilly source time keys, orbital/secondary motion, radix-strength conditions, eclipse/lot cases and every human event interpretation. It does **not** overwrite the pre-existing three separate research geometry arms.

### Published secondary worked example

Kolev's rounded Jupiter-promissor to Sun-significator coordinates (53°N, RAMC 222.17357°, Sun RA 186.1673°, Sun Dec −2.6734°, Jupiter RA 261.13°, Jupiter Dec −23.151°) produce:

| Mathematical method | Computed arc |
| --- | ---: |
| **Independent Regiomontanian fictitious-pole reconstruction** | **56.61516250670422°** |
| Existing Regiomontanian Cartesian position-circle algorithm | 56.61516250670425° |
| Placidus under pole | 62.76435915356109° |
| Proportional semi-arc | 62.04313286280774° |
| Kolev's displayed rounded target | 56.615053° |

The independent Regiomontanian result differs from Kolev's rounded published number by **0.00010950670422°**, consistent with the rounding precision of input coordinates and much smaller than the divergence from the two genuinely different method families. Zenith distance and fictitious pole intermediates also match his displayed approximate values within their predeclared rounding tolerances.

## Fixed synthetic geometry comparison

The exploratory 1,200 tuples (seed 2004) were originally inspected **before** the durable precommit. They are therefore honestly labeled **DEVELOPMENT**, not independently blind. To gain additional independent arithmetic verification, seed **20261026** and 800 entirely new synthetic latitude/RAMC/RA/declination tuples were fixed in `REGIO_INDEPENDENT_PARITY_PRECOMMIT.json`, along with the complete implementation and tests, and published as commit `3e6b17e` **before first executing the new 800-case test**.

| Test panel | Synthetic geometries | Circular errors above 0.00000001° | Largest error |
| --- | ---: | ---: | ---: |
| Development (seed 2004) | 1,200 | 0 | ~1.14 × 10⁻¹³° |
| Subsequently frozen mathematical holdout (seed 20261026) | 800 | 0 | ~1.14 × 10⁻¹³° |

All four east/west × above/below quadrants are represented in each test. These are randomly generated *astronomical coordinates*, not actual birth charts. This validates agreement between two implementations of one geometry family; it does **not** create 2,000 independent predictions, verify the authentic whole Argoli 1610 system, or estimate human outcomes.

## Remaining research frontier

Full correspondence of Argoli **1610 vs. 1644 vs. 1667** editions; historic sign/term table variants; actual direct/converse practices and annual timing; promissor latitude and source-specific zodiacal aspect-ray projection; natal strength of both actors; the partly reconstructed Ascendant/MC significator treatments; independent event meanings; birth-time uncertainty; calibrated null controls; and genuinely untouched prospective human evidence are all **OPEN**. The mathematically verified model may be separately registered as a *modern Regiomontanian diagnostic arm* but must not be promoted into an authentic complete Lilly prediction rule by inference.

`POSITION_CIRCLE_PARITY_REPORT.json` contains complete input and result metadata, quadrant counts and all reproduced source values. The runner `build_regio_parity.py` is deterministic and rejects mismatched source PDF bytes/protocol. The tests are in `tests/unit/test_regio_pole_independent.py`. No real natal records, private life events, medical, financial, or legal predictions are included.
