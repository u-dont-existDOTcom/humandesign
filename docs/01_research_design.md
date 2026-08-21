# 01 — Research Design

## Research questions

### RQ1 — Engineering recovery
If answers are mechanically generated from a frozen HD behavioral model, can the blind decoder recover the hidden date/time/chart?

This is a software and information-recovery test. It is expected to succeed under ideal conditions if the model and decoder are internally coherent.

### RQ2 — Noise robustness
How much missingness, contextuality, response error, and measurement unreliability can the decoder tolerate before recovery fails?

### RQ3 — Human chart specificity
When real people answer the questionnaire, does their true birth-derived chart/date/time rank above matched alternatives out of sample?

This is the first stage that bears on Human Design's descriptive predictive validity.

### RQ4 — Empirical mapping
Can mappings learned from development humans predict held-out humans better than:
- the hand-coded symbolic model,
- chance/permuted charts,
- calendar/season baselines,
- demographic baselines,
- plausible mismatched HD charts?

### RQ5 — Minute rectification
Among people with reliable documented birth times, can the system recover the correct state interval within a known day at rates exceeding matched chance?

## Experimental ladder

1. Synthetic, known month/year: recover day.
2. Synthetic, known year: recover day-of-year.
3. Synthetic, known date: recover time interval.
4. Synthetic, known year: jointly recover date + time.
5. Synthetic 100-year UTC universe.
6. Human development data: post-hoc fit and iterate.
7. Human internal validation: cross-validation/nested validation.
8. Frozen prospective validation on untouched humans.
9. Documented-time minute rectification.
10. External replication.

## Development versus validation

Use three human pools:

```text
DEVELOPMENT
    Use freely for:
    - discovering questions
    - revising construct definitions
    - fitting mappings
    - estimating P(answer | chart features)
    - choosing model class
    - tuning hyperparameters
    - questionnaire shortening
    - analyzing errors

VALIDATION
    Use for:
    - model selection
    - stopping decisions
    - limited calibration
    - confirming improvements
    Do not repeatedly optimize to this set indefinitely.

FINAL TEST
    Never inspect during development.
    Reveal once for the frozen model/version.
```

If the final test motivates a redesign, that redesign becomes a new version and requires a new untouched test set.

## Important claim boundary

Post-hoc fit can establish that a model CAN describe its training humans.
Only held-out/prospective performance establishes that the same procedure generalizes.

The project must never blur these statements.
