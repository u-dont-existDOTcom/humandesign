# 07 — Acceptance Tests

## Engine acceptance
- Historical DST conversions match independent authoritative timezone data.
- Design moment solves the exact 88° solar-arc criterion within declared tolerance.
- Golden charts match at least one independent HD implementation for random dates and every finalist.
- Boundary enumeration finds all known gate/line transitions in stress tests.
- Adjacent stable intervals reconstruct continuously with no gaps/overlaps.

## Blinding acceptance
- Decoder test container cannot read answer key path.
- Public blind file passes leakage scan.
- Prediction hash changes when prediction content changes.
- Evaluator refuses reveal if no freeze record exists.
- Evaluation uses the frozen prediction file only.

## Synthetic oracle acceptance
Known-month oracle benchmark:
- top-1 recovery should approach the theoretical identifiability ceiling.
- every failure is classified:
  - structurally indistinguishable,
  - missing mapping,
  - search bug,
  - scoring bug,
  - aggregation ambiguity.

Do not set “100%” as a blind requirement if several candidate birth states are mathematically identical under the model; ties are legitimate.

## Noise benchmark acceptance
Report performance as a curve by:
- missingness,
- answer-flip rate,
- reliability,
- number of independent clusters restored.

## Human-development acceptance
- all splits are person-level;
- development records may be fit post-hoc;
- final test records are inaccessible to fitting pipeline;
- baseline models run automatically;
- permutation/null test implemented.

## Minute claim acceptance
A result cannot be labeled exact-minute unless:
- true chart state changes at relevant boundaries;
- scoring/questionnaire actually discriminates those states;
- independent chart-engine validation agrees;
- interval width is reported.

## Reproducibility
Same commit + config + seed + input must produce the same:
- synthetic blind file,
- prediction ranking,
- metrics,
within documented numerical tolerances.
