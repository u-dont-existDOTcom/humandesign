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

Generation creates or uses an owner-only AES key under `/tmp/hdmatch-secrets` by default, but ordinary command output does not disclose its path. Recovery accepts no key or answer-key path and performs a plaintext-answer-key preflight before scoring. That scan is defense in depth, not a substitute for running the decoder in a separate keyless operating-system user, container, or equivalent access boundary. Reveal binds the exact encrypted envelope and canonical decrypted payload; evaluation refuses a different in-memory key. Exact ephemeris files and their hashes must be supplied for every chart run.

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

This command reads the complete public provenance chain: blind input, recovery
manifest, predictions, prediction freeze, reveal record, encrypted envelope, and
post-reveal evaluation. It decrypts nothing. It verifies exact bytes, recovery-config
hash, frozen model and noise settings, envelope path/hash, freeze/reveal bindings,
timestamp ordering, candidate-universe binding, case denominator, aggregation rule,
and revealed target consistency. The report preserves every tier, failure, and
unevaluable case and shows Top-1/3/5 and MRR degradation from oracle. It is an
engineering robustness result, not human validation.

## Model A and Model B

`MODEL-A-CORE-V1` is the unchanged coarse architecture model. `MODEL-B-DETAILED-V1` is a structural-only intermediate containing all source-supported detailed mechanics: 36 complete channels, separate Personality/Design Sun–Earth gate and line representations, Definition, mechanics-only repeated gates and Nodes, a deliberately empty unresolved prominent-activation allowlist, hanging-gate candidates, dependency controls, and the conditional-prevalence framework. It is not completion of the detailed behavioral-model objective.

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

The legacy result proves that an earlier D1–D10/A1–A6 detailed scorer existed. A source-recovery audit found the exact frozen target and generic rubric, but not the pre-search per-observation definitions, selectors, roles, directness assignments, dependency clusters, or contradictions. The eight V1 behavioral-family placeholders remain `unresolved`; that status is an intermediate limitation, not an acceptance condition or a completed Model B. Model B V1 currently generates and scores only its unchanged Model A behavioral base, so no behavioral A/B benchmark may run until a provenance-reviewed Model B actually produces different behavioral predictions. See `reports/model_b_source_recovery_audit.md` and the machine-readable audit under `mappings/`.

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
