# HD Reverse-Matching Codex Project V1

This folder is a Codex-ready specification for building a blinded Human Design birth-moment recovery research harness.

## Start

Open this folder as the Codex project and give Codex the contents of:

`CODEX_MASTER_PROMPT.md`

Codex should then read `AGENTS.md`, `ARCHITECTURE.md`, and the numbered documents in `docs/`.

## Why this version exists

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
