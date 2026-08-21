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

The CLI exposes separate commands for generation, recovery, prediction freeze, and reveal/evaluation. Keep the answer-key encryption key outside this repository and outside the decoder workspace.

```bash
hdmatch generate-synthetic --config configs/synth_month.yaml --blind-output run/blind_cases.json --sealed-key-output /outside/project/answer_key.enc --key-file /outside/project/key.bin
hdmatch recover --blind-file run/blind_cases.json --run-dir run
hdmatch freeze-predictions run
hdmatch reveal --run run --sealed-key /outside/project/answer_key.enc --key-file /outside/project/key.bin
hdmatch report --run run
```

The default known-month configuration contains 1,000 oracle cases. Exact ephemeris files and their hashes must be supplied for a production engine run.

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
