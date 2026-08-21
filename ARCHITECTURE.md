# Architecture

## Goal

Implement an end-to-end research system that can:

1. calculate exact Human Design chart states across candidate birth moments;
2. encode the existing V4/V3.2 behavioral scoring model;
3. generate synthetic questionnaire cases from the frozen model;
4. recover hidden dates/times from blinded synthetic responses;
5. optimize question selection and decoding on synthetic and development data;
6. fit chart→behavior likelihoods on known human development cases;
7. freeze a model;
8. test it prospectively on untouched human cases;
9. report rank, uncertainty, stable time intervals, failures, and calibration.

## Core principle

The project distinguishes **model fitting** from **model validation**.

Post-hoc fitting is legitimate model development. It becomes circular only when the fitted cases are also presented as proof that the fitted model predicts unseen people.

## System components

```text
                    ┌──────────────────────┐
                    │ Exact chart engine   │
                    │ UTC / design / gates │
                    │ boundaries / states  │
                    └──────────┬───────────┘
                               │
                 chart features / state intervals
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
 ┌───────────▼───────────┐             ┌─────────▼─────────┐
 │ Symbolic V4 decoder   │             │ Empirical decoder │
 │ frozen mappings       │             │ learned P(a|chart)│
 │ rubric bits           │             │ on dev humans     │
 └───────────┬───────────┘             └─────────┬─────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               │
                        candidate ranker
                               │
                    adaptive question selector
                               │
                         blind prediction
                               │
                         prediction freeze
                               │
                         answer-key reveal
                               │
                           evaluator
```

## Packages Codex should implement

```text
src/hdmatch/
    cli.py
    config.py
    schemas/
    chart/
        ephemeris.py
        timezone.py
        design_moment.py
        rave_mandala.py
        bodygraph.py
        boundaries.py
        validation.py
    model/
        observations.py
        mapping_library.py
        symbolic_score.py
        empirical_score.py
        dependencies.py
        reliability.py
    questionnaire/
        bank.py
        response.py
        adaptive.py
    synthetic/
        generator.py
        noise.py
        sealing.py
    search/
        candidate_universe.py
        interval_ranker.py
        date_aggregator.py
        minute_rectifier.py
    experiments/
        manifest.py
        freeze.py
        blind_run.py
        reveal.py
        splits.py
    evaluation/
        metrics.py
        permutation.py
        calibration.py
        ablation.py
        robustness.py
    api/
        app.py

tests/
    unit/
    integration/
    golden/
    blind_e2e/
```

## CLI target

```bash
hdmatch validate-engine
hdmatch compile-model
hdmatch generate-synthetic --config configs/synth_month.yaml
hdmatch recover --blind-file blind_cases.json --model symbolic
hdmatch freeze-predictions run_dir/
hdmatch reveal --run run_dir/ --key /outside/project/answer_key.enc
hdmatch evaluate --run run_dir/
hdmatch fit-human --dataset dev_humans.parquet
hdmatch validate-human --model frozen_model/ --dataset validation_humans.parquet
hdmatch test-human --model frozen_model/ --dataset untouched_test_humans.parquet
hdmatch optimize-questionnaire --development-set ...
hdmatch report --run ...
```

## Time resolution

Search candidate **state intervals**, not nominal clock samples.
Report a minute only if a relevant boundary or validated finer-grained feature distinguishes it.
Otherwise return the full stable interval.
