# Wave 4 development evaluation

This directory contains the mechanical development-only runner for the frozen
v1b empirical-astrology model.

Run from the repository root with the empirical dependencies installed:

```bash
python experiments/empirical_astrology/wave4/run_wave4.py
```

The runner reads the frozen model artifacts and
`input_manifest.json`. It does not discover or open owner-known outcomes. The
manifest contains no eligible human development dataset, so the runner emits
explicit `NOT_EVALUATED` empirical rows, explicit
`NOT_APPLICABLE_NO_INCLUDED_FEATURE` astrology-ablation rows, and engineering
fixture checks only.

Engineering fixture metrics test code paths. They are not human observations,
effect estimates, null evidence, power evidence, or prospective validation.
