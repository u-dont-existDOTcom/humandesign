# HD Reverse-Matching Research Harness

This repository contains a typed Python harness for blinded Human Design birth-moment reverse-matching research. Human Design is treated as an experimental symbolic hypothesis. Synthetic recovery validates engineering coherence only; it does not validate Human Design in humans.

## Current model status

The normative development model is now **V4.3 / behavioral target V3.5**.

Start with:

- `AGENTS.md`
- `reference/core/v4_3_scoring_algorithm.md`
- `reference/core/behavioral_target_combined_v3_5.md`
- `docs/13_v4_3_migration_and_century_cache.md`
- `CODEX_V4_3_MIGRATION_PROMPT.md`

The existing Python implementation was originally built around V4.1/V3.2 and must not call itself V4.3 until the migration/compliance tests pass. Reduced architecture-only runs must be labeled reduced and emit `v4_3_compliant=false`.

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

Ordinary green legacy tests do not by themselves prove V4.3 compliance. The migration must add anti-simplification/mutation tests described in `docs/13_v4_3_migration_and_century_cache.md`.

## Blind workflow

The CLI exposes separate commands for generation, recovery, prediction freeze, and reveal/evaluation. Keep the answer-key encryption key outside this repository and outside the decoder workspace.

```bash
hdmatch generate-synthetic --config configs/synth_month.yaml --blind-output run/blind_cases.json --sealed-key-output /outside/project/answer_key.enc --key-file /outside/project/key.bin
hdmatch recover --blind-file run/blind_cases.json --run-dir run
hdmatch freeze-predictions run
hdmatch reveal --run run --sealed-key /outside/project/answer_key.enc --key-file /outside/project/key.bin
hdmatch report --run run
```

## Precomputed 100-year universe

The expensive astronomical candidate universe should be generated once, verified, versioned, and reused across behavioral targets.

Initial canonical range:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

The migration target uses Zstandard-compressed Parquet shards plus a cryptographic manifest and cached duration-weighted prevalence tables. Normal broad searches should load the verified cache instead of rebuilding a century of exact states for every person.

If binary shards are too large for ordinary Git history, store them in Git LFS or versioned GitHub Release assets. Keep the manifest, schema, generation code, and verification code in the repository.

## Research claim boundary

The project explicitly allows **post-hoc fitting on human development data**.

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

`reference/core/` contains the scoring/search/questionnaire specifications and current target material.

`reference/verified_cases/` contains externally checked chart fingerprints useful for calculation parity/golden tests. These are references, not behavioral training targets unless a study explicitly declares them as such.

`reference/legacy_runs/` contains previous search outputs for regression/debugging only. Legacy/simplified result files must never be mined as a mapping source.

`reference/custom_gpt/` contains the Custom GPT/transit materials, which are secondary to the research harness.

`reference/research/` contains methodological context.

## Security

For a real blind run, keep the answer key outside this project/workspace or encrypted with a passphrase unavailable to the decoder until predictions are frozen.
