# HD Reverse-Matching Research Harness

This repository contains a typed Python harness for blinded Human Design birth-moment reverse-matching research. Human Design is treated as an experimental symbolic hypothesis. Synthetic recovery validates engineering coherence only; it does not validate Human Design in humans.

## Environment

Required: Python 3.11 or newer. The tested development runtime is Python 3.12.

```bash
bash scripts/bootstrap.sh
source .venv/bin/activate
```

Swiss Ephemeris is an optional engine dependency with AGPL/professional dual licensing. Exact production runs must point to declared local ephemeris files and will fail rather than silently use Moshier. See `docs/PRIOR_WORK_SCAN.md`.

## Verification

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check src tests scripts
.venv/bin/mypy src/hdmatch
```

The task-specific milestone gate is:

```bash
.venv/bin/python scripts/task_acceptance.py
```

Ordinary green tests do not by themselves prove that the requested benchmark artifacts exist.

## Blind workflow

The CLI exposes separate commands for generation, recovery, prediction freeze, and reveal/evaluation. Keep the answer-key encryption key outside this repository and outside the decoder workspace. The default known-month configuration is the bounded 75-case Model A engineering smoke; the deferred 1,000-case configuration is not an acceptance default.

```bash
hdmatch generate-blind \
  --config configs/synth_month.yaml \
  --run-dir run_artifacts/model_a_smoke \
  --ephemeris /path/to/declared-swiss-files

hdmatch recover \
  --run-dir run_artifacts/model_a_smoke \
  --ephemeris /path/to/declared-swiss-files \
  --cache-dir run_artifacts/candidate_cache

hdmatch freeze --run-dir run_artifacts/model_a_smoke

hdmatch reveal-evaluate --run-dir run_artifacts/model_a_smoke
```

Generation creates or uses an owner-only AES key under `/tmp/hdmatch-secrets` by default. Recovery accepts no key or answer-key path. Reveal fails unless the prediction freeze and all bound hashes verify. Exact ephemeris files and their hashes must be supplied for every chart run.

The completed smoke report is in `reports/model_a_smoke_75/`. It retains all 41 non-Top-1 cases and explains the residual failure classification.

## Synthetic noise-tier comparison

The bounded noise smoke uses four 25-case configs:
`synth_month_oracle_noise_smoke.yaml`, `synth_month_low_smoke.yaml`,
`synth_month_medium_smoke.yaml`, and `synth_month_adversarial_smoke.yaml`.
Generate the four runs with the same external secret seed so they conceal the same
birth moments, then run the normal recover → freeze → reveal/evaluate sequence for
each directory. Do not compare an interrupted or unrevealed run.

After all four canonical `evaluation.json` files exist, aggregate them without
opening an answer key:

```bash
hdmatch compare-noise-tiers \
  --oracle-run-dir run_artifacts/noise_oracle \
  --low-run-dir run_artifacts/noise_low \
  --medium-run-dir run_artifacts/noise_medium \
  --adversarial-run-dir run_artifacts/noise_adversarial \
  --output run_artifacts/noise_comparison.json
```

This command reads only each run's public `blind_cases.json`, `run.manifest.json`,
and post-reveal `evaluation.json`. It verifies their hashes, frozen model and noise
settings, candidate-universe binding, case denominator, aggregation rule, and
revealed target consistency. The report preserves every tier, failure, and
unevaluable case and shows Top-1/3/5 and MRR degradation from oracle. It is an
engineering robustness result, not human validation.

## Model A and Model B

`MODEL-A-CORE-V1` is the unchanged coarse architecture model. `MODEL-B-DETAILED-V1` is a separate composite artifact containing all source-supported detailed mechanics: 36 complete channels, separate Personality/Design Sun–Earth gate and line representations, Definition, mechanics-only repeated gates and Nodes, a deliberately empty unresolved prominent-activation allowlist, hanging-gate candidates, dependency controls, and the conditional-prevalence framework.

Rebuild either frozen artifact with:

```bash
hdmatch compile-model --model MODEL-A-CORE-V1
hdmatch compile-model --model MODEL-B-DETAILED-V1
```

Select Model B for generation and recovery by passing the same explicit model identity to both commands:

```bash
hdmatch generate-blind --config configs/synth_month.yaml --run-dir run_artifacts/model_b_smoke --ephemeris /path/to/declared-swiss-files --model MODEL-B-DETAILED-V1
hdmatch recover --run-dir run_artifacts/model_b_smoke --ephemeris /path/to/declared-swiss-files --cache-dir run_artifacts/candidate_cache --model MODEL-B-DETAILED-V1
```

The normative V4/V3.2 files do not provide directness, answer direction, or contradiction semantics for the detailed structures. All eight detailed behavioral mapping families are therefore frozen as `unresolved`. Model B currently generates and scores only its unchanged Model A behavioral base; a behavioral A/B recovery run is guaranteed to rank identically. This is intentional and prevents post-result interpretation mining.

The detailed mechanics can still be audited as a clearly labeled structural-resolution upper bound, using no responses or answer keys:

```bash
hdmatch compare-models \
  --cache-dir run_artifacts/candidate_cache \
  --ephemeris /path/to/declared-swiss-files \
  --year 2000 \
  --timezone UTC \
  --output run_artifacts/structural_comparison.json
```

Over the retained 13,777 exact 2000/UTC intervals, Model A produced 950 structural signatures and Model B 2,963. This shows additional mechanical partitioning only—not behavioral observability, recovery, or human validity. The transparent summary is in `reports/model_b_structural_audit_2000/`.

## Research claim boundary

The project now explicitly allows **post-hoc fitting on human development data**.

That is not a methodological error. It is the training stage.

The error would be fitting a model to people and then citing its performance on those same people as evidence that it predicts new people.

The intended cycle is:

```text
development humans
    ↓
fit / revise / learn
    ↓
freeze model version
    ↓
untouched humans
    ↓
prospective evaluation
    ↓
new version if needed
    ↓
new untouched test
```

Synthetic tests come first to validate the machinery.

## Reference material

`reference/core/` contains the core scoring/search/questionnaire files already developed in this project.

`reference/legacy_runs/` contains previous search outputs for regression/debugging only.

`reference/custom_gpt/` contains the Custom GPT/transit materials, which are secondary to the research harness.

`reference/research/` contains the forum research supplied for methodological context.

## Security

For a real blind run, keep the answer key outside this project/workspace or encrypted with a passphrase unavailable to the decoder until predictions are frozen.
