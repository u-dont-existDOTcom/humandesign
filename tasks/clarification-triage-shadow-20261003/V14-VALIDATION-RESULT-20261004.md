# V14 untouched validation result — 2026-10-04

## Frozen design

The v14 source packet and adjudication targets were committed and pushed before any implementation replay. Nine cases were scored: eight exact Sonnet/high + Opus 5.5/max agreements, plus V2 with G20 required and G19 permitted. V7 was frozen unscored because the adjudicators disagreed.

Malformed first adjudication outputs were preserved as structured-output/interface failures. Sonnet attempt 2 was admitted only after the explicitly authorized removal of one outer Markdown JSON fence; Opus attempt 2 was a fresh serialization-only retry and was admitted directly.

## Untouched implementation result

The first implementation replay did not complete.

- V1 passed.
- V2 passed.
- During V3, GapMatchAudit returned source-reference metadata that differed from the immutable caller-supplied pair metadata.
- The validator rejected the artifact with: "Gap match audit changed its supplied source references."

This is an implementation serialization/interface robustness defect. It is not a semantic failure of V3 and v14 must not be scored as a completed validation run.

## Bounded repair

GapMatchAudit no longer asks the semantic model to echo immutable route/source IDs.

- The model-facing response contains only `status` and `independent_for_batch` for each supplied pair, in order.
- Route IDs and source-turn IDs remain caller-owned.
- A deterministic binder reattaches those immutable IDs by pair order after schema validation.
- The richer bound GapMatchAudit object remains unchanged for downstream provenance and ordering.
- The validator still checks the resulting bound object against the supplied context.

This reduces both the serialization surface and output burden without weakening semantic checks or allowing route coverage to create questions.

Focused verification after repair: **28/28 tests passed** and Ruff passed.

A contaminated V3 replay then passed exactly with M09 in about 30 seconds. That is tuning evidence only.

## Remaining gate

One fresh post-repair exact-authority packet is required. If it passes, run one unchanged repeat to measure stochastic stability, then measure owner-scale 81-turn latency. Do not add further synthetic validation cycles unless those decision-relevant checks expose a new failure.
