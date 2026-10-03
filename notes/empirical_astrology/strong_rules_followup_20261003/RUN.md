# Run and inspect this packet

The delivered archive preserves the repository directory layout under notes/empirical_astrology/. Start with REPORT.md in strong_rules_followup_20261003/.

## Inspect without rerunning

- results/results.json: full model search, baselines, folds and choices.
- results/fitting_audit.json: fixed depth-four held-out and shuffled-label diagnostic.
- results/exact_year_pairs.csv: exact-year rematching used in the second arm.
- ../murderer_birth_pattern_pilot_20261003/paired_cohort.csv: unchanged input.
- reviewer_report.md and review_reconciliation.json: review and dispositions.
- baseline_replay.json: unchanged earlier baseline replay.

## Reproduce in an existing scientific Python environment

Recorded versions: Python 3.12 runtime; numpy 2.5.2; scipy 1.18.0; scikit-learn 1.9.0; pyswisseph reports 20230604; python-dateutil is also required. The original baseline additionally uses pandas. This packet does not install packages or reproduce the entire environment automatically; different library versions can alter fitted models.

From the archive root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python notes/empirical_astrology/strong_rules_followup_20261003/search_rules.py   --input notes/empirical_astrology/murderer_birth_pattern_pilot_20261003/paired_cohort.csv   --out reproduced_results --repeats 3 --calendar-draws 3
```

The script checks the exact source input blob and fails on a substituted cohort. The saved result is the original execution, not a re-created summary. Do not modify or overwrite it. fitting_audit.py writes to its local results directory; use a separate copy of the archive for rerunning that diagnostic.

These tools evaluate this historical cohort only. They are not a deployment or an individual criminal-risk service. Full traditional natal rules and verified birth-name numerology are outside this experiment.
