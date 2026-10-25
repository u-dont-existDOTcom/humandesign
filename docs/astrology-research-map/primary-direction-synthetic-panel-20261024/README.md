# Primary directions — frozen synthetic coverage and timing robustness

Research checkpoint: 25 October 2026. This is a Western supporting subtask of the OPEN owner outcome: historically computable astrology from multiple traditions, with models frozen before prospective independent, blinded human validation and controls. No human natal records or event responses were used here.

## Historical evidence recovered

Seven original 1647 William Lilly printed pages (509–510, 651–655) from the Wellcome scan have been preserved. The separate annotated source register keeps original wording apart from later numerical interpretation. Page 652 notes that two or three degrees of birth-time/Ascendant error can shift anticipated events by years. Pages 654–655 condition manifestations on the natal strength of BOTH significator and promissor and permit no manifestation where both are weak. Lilly also permits adverse and favorable directions to coincide in one year. Page 510's forward/backward terminology relates to zodiacal ray positions in a Speculum; it does not authenticate our modern shortest-signed-arc software rule. Page 651 cites Argolus without giving a complete executable model. The full historical direct/converse method remains unresolved.

## Frozen synthetic experiment

The 96 charts were drawn from one cell each in 12 birth-month × 8 latitude strata using prespecified pseudorandom seeds, years 1910–2010, longitude/clock values and age bounds [18,65). This is not a demographically representative sample. The plan, all input tuples and runner were committed before calculating. The official Swiss files are locally hashed and SWIEPH mode checked. A single proportional-semi-arc geometry and 1 degree/year diagnostic time key were used; only software direct directions were counted. The unchanged 4 original bodily and 4 zodiacal-aspect rule families from the preceding checkpoint were examined. Contacts are not event predictions.

## Synthetic contact coverage

| Quantity | Result |
| --- | ---: |
| Charts | 96 |
| Charts without a bodily contact | 56 |
| Charts without an aspect contact | 5 |
| Charts without either | 1 |
| Bodily contacts | 47 |
| Aspect contacts | 169 |
| Total contacts | 216 |
| Mean / median / maximum contacts per chart | 2.25 / 2 / 4 |
| Mean union of one-year candidate windows, per chart | 2.179468 adult years |
| Geometry parity | 12 charts, 30 groups, 0 mismatches |

The mean age-window union occupies ~4.64% of the 47-year adult interval. This is geometric coverage, *not* probability of events, statistical power, predictive accuracy, specificity, or sensitivity. Source interpretation for some contacts requires historical dignity conditions or opportunity constraints that have NOT been implemented. Additional aspect candidates also create a multiple-testing cost. The chart-by-chart denominators, details and counts are in the accompanying JSON/CSV outputs.

## Frozen birth-time perturbation (24 synthetic charts)

A separate seeded selection of 24 charts provided 54 baseline eligible contacts. For each chart we changed the assumed UTC birth time, held geography fixed, and matched the exact rule + aspect + orientation rather than selecting whichever contact was closest to an event.

| Shift | Matched baseline branches | Median absolute timing shift | Within ±0.5 year | Within ±1 year |
| --- | ---: | ---: | ---: | ---: |
| −5 min | 54/54 | 1.253122 years | 0 | 0 |
| +5 min | 54/54 | 1.253122 years | 0 | 0 |
| −15 min | 50/54 | 3.759446 years | 0 | 0 |
| +15 min | 51/54 | 3.759388 years | 0 | 0 |

For a separate physical cross-check, Swiss Ephemeris shows a 1.25342-degree natal meridian rotation in five minutes on a sampled chart. Under the chosen diagnostic 1 degree/year convention, this independently explains the ~1.25-year sensitivity. The original planned ±0.5-year event window is therefore *not robust* to ±5-minute birth-time errors. A scale estimate of ~±2 minutes would move the derived age by ~0.5 year. That is a **conditional design estimate**, not a mandated exclusion threshold; record uncertainty intervals and propagate them instead of rectifying toward desired outcomes.

## Interpretation, reproducibility and outstanding root objective

**Verified here:** a frozen synthetic input design, strict Swiss source identity, an executable and reproducible diagnostic, 96 synthetic astronomical charts, 216 source-rule exposures, and a quantitative ±5/±15-minute sensitivity check. A separate 12-chart geometry comparison identified 30 matched contacts and no disagreements across the three geometric labels; those methods do not provide independent evidence.

**Not verified:** full historical Lilly/Argolus direction geometry, converse rules, natal-strength conditions for both participants in a direction, profections/revolutions, clinical or occupational event predictions, or any human predictive validity. The timing key is an explicitly modern diagnostic. The four aspect interpretations include conditions that are NOT implementation-frozen.

**Next substantive priority:** establish source-defined natal-strength and historical direction-sense choices where recoverable without outcome knowledge. Freeze outcome definitions, event windows, birth-time uncertainty handling, and participant/control scoring before conducting independent prospective human testing jointly across traditions. Results from known personal histories are development evidence only.
