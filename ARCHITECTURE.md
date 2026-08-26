# Architecture

## Goal

Implement an end-to-end research system that can:

1. calculate exact Human Design chart states across candidate birth moments;
2. encode the canonical V4.3 behavioral scoring model and current frozen target;
3. generate synthetic questionnaire cases from the frozen model;
4. recover hidden dates/times from blinded synthetic responses;
5. optimize question selection and decoding on synthetic and development data;
6. fit chart→behavior likelihoods on known human development cases;
7. freeze a model;
8. test it prospectively on untouched human cases;
9. report rank, uncertainty, stable time intervals, failures, and calibration;
10. calculate pair/connection mechanics as a separate relationship research module;
11. preserve relationship evidence separately from natal reverse-matching evidence;
12. generate independently frozen future life-state timelines for two partners and test multi-domain future concordance against random-partner null distributions;
13. test pair-specific relationship-transition hazards separately from relationship quality/mutuality outcomes.

## Core principle

The project distinguishes **model fitting** from **model validation**.

Post-hoc fitting is legitimate model development. It becomes circular only when the fitted cases are also presented as proof that the fitted model predicts unseen people.

It also distinguishes **natal reverse matching** from **relationship/connection analysis**. A relationship description may be useful or testable without being evidence that a natal candidate should receive additional V4.3 NetInformation.

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
             ┌─────────────────┼────────────────────┐
             │                 │                    │
 ┌───────────▼───────────┐ ┌──▼────────────────┐ ┌─▼──────────────────────┐
 │ Symbolic V4.3 decoder │ │ Empirical decoder │ │ Relationship analysis │
 │ frozen mappings       │ │ learned P(a|chart)│ │ pair connection state │
 │ NetInformation        │ │ on dev humans     │ │ + unknown-time ranges │
 └───────────┬───────────┘ └──┬────────────────┘ └──────────┬─────────────┘
             │                 │                              │
             └────────┬────────┘                         separate report /
                      │                                  validation track
               candidate ranker                               │
                      │                               ┌────────▼────────────┐
           adaptive question selector                 │ Future concordance  │
                      │                               │ independent timelines│
                blind prediction                      │ + null partners      │
                      │                               └────────┬─────────────┘
                prediction freeze                              │
                      │                              ┌──────────▼────────────┐
                answer-key reveal                     │ Transition / quality │
                      │                              │ separate empirical   │
                  evaluator                          │ models + hard risks  │
                                                     └───────────────────────┘
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
    relationship/
        analysis.py
        uncertain_time.py
        future_state.py
        concordance.py
        null_partners.py
        western_timing.py
        hd_timing.py
        geography.py
        risk_sets.py
        transition.py
        semimarkov.py
        quality.py
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

## Relationship module boundary

`src/hdmatch/relationship/` consumes independently calculated natal chart states. It does not modify those natal states and it does not feed the natal V4.3 scorer.

V1 implements the source-defined relationship surface:

- combined Center configuration;
- connection-chart Definition/splits;
- Electromagnetic, Dominance, Compromise, and Companionship channel classification;
- shared Gates;
- natal Type/Authority/Profile context;
- mechanically detectable Sun/Earth-to-Node alignments;
- stable versus time-dependent mechanics when a partner birth time is unknown.

V2 adds partner future-concordance research:

- independently generated/frozen future state vectors for each partner;
- secondary progressions, verified SWIEPH transits, HD life-cycle/developmental overlays, and astrocartography/relocation as separately identified layers;
- romantic, economic, home/community, work/purpose, belonging, care, and geographic domains;
- explicit collective-vs-individual specificity weighting;
- unknown-birth-time robustness across every materially distinct partner state;
- pair-specific synastry/connection timing only after both individual timelines are frozen;
- random-partner and reciprocal null distributions.

V3 separates **transition prediction** from **relationship quality** and adds hard-decoy residual testing:

- hard-match decoy partners on individual future trajectories before pair scoring;
- test progressed A→natal B, progressed B→natal A, and progressed A→progressed B as pair-specific dynamic layers;
- evaluate pair-transition signal only after individual timing has been controlled;
- develop a semi-Markov/multi-state model for formation, commitment, separation, and reunion hazards;
- develop a different Track-Q model for mutual affection, satisfaction, reciprocity, safety, conflict/repair, and benefit/harm;
- never infer that a relationship is good merely because the transition model predicts that it forms or persists.

Do not add a generic compatibility or soulmate scalar unless a separately frozen empirical relationship model is trained on development couples and tested on different, untouched couples. `SharedLifeConcordance` is an experimental future-state overlap statistic, not a soulmate probability and must be reported with its null distribution.

See:

- `docs/18_relationship_analysis.md` — static connection mechanics;
- `docs/19_partner_future_concordance.md` — future-life concordance;
- `docs/20_partner_transition_vs_quality.md` — transition-vs-quality separation and hard-decoy principle;
- `docs/21_pair_transition_semimarkov_plan.md` — empirical pair-specific semi-Markov test.

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

Relationship CLI/API adapters may be added after the pure mechanical module and tests are stable; the pure Python API is the V1 integration point.

## Time resolution

Search candidate **state intervals**, not nominal clock samples.
Report a minute only if a relevant boundary or validated finer-grained feature distinguishes it.
Otherwise return the full stable interval.

For an unknown partner birth time, apply the same rule to the partner's local civil day: enumerate exact natal state intervals, calculate the pair mechanics for every interval, merge only identical complete relationship fingerprints, and report invariants separately from time-dependent features.
