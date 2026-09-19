# Life Patterns — Structured Annotation V2 / Automated Calibration Milestone Receipt

Date: 2026-09-04

Status: **pre-execution development infrastructure complete; external theory-blind inputs still required**.

No merge, deploy, participant/coder contact, spending, validation promotion, target-model adapter execution, target-model scoring, or reveal is authorized by this receipt.

## Scientific decision now implemented

The default Life Patterns measurement-development route is LLM-primary with independent human calibration, rather than full-corpus dual-human coding.

The development workflow is:

1. freeze the exact theory-neutral codebook/corpus/procedure/prompt/task set;
2. run at least three isolated high-capability theory-blind automated coding passes;
3. preserve raw outputs and deterministic canonical normalization;
4. validate complete episode–observable coverage and response provenance;
5. derive unanimous / strict-majority / unresolved consensus without forcing unresolved units;
6. obtain an independent theory-blind human calibration pass on a frozen sampled subset before the human sees automated labels;
7. use disagreement/stability evidence for theory-blind measurement revision only;
8. freeze one validation route before target-model results;
9. only later permit validation coding/model comparison under separately authorized boundaries.

LLM self-consistency does not establish correctness or construct validity.

## Frozen substantive source remains unchanged

Canonical development codebook:

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

It remains a **development candidate**, not a validation candidate.

No substantive wording in that frozen theory-blind reconciliation was changed by this milestone.

## V2 annotation fidelity layer

Added:

- `src/hdmatch/evaluation/structured_annotation_v2.py`
- `tests/unit/test_structured_annotation_v2.py`

V1 schemas remain unchanged so prior canonical hashes are preserved.

V2 explicitly represents:

- frozen participant-reviewed episode boundaries;
- episode-level `observed / insufficient / not_applicable` states;
- `single / ordered_sequence / unordered_multiple` substantive values;
- four-part non-action evidence gate: awareness, opportunity, feasibility, established non-action;
- universal missingness flags from the reconciled codebook;
- universal `OS` / Other Specified with mandatory concrete behavioral description;
- supporting/counterevidence source-turn provenance;
- narrator-explicit influence versus temporal-precedence-only;
- context, language, life-phase, and theory-exposure provenance;
- explicit exclusion of person-level `contradicted/mixed` from primary episode coding.

## Raw output normalization

Added:

- `src/hdmatch/evaluation/structured_annotation_normalization.py`
- `tests/unit/test_structured_annotation_normalization.py`

Raw LLM output is preserved/hashable. Deterministic normalization accepts schema-valid compact JSONL or whitespace-separated/pretty-printed JSON objects and emits canonical V2 JSONL.

Normalization cannot repair substantive labels, infer missing evidence, change states, invent gates, or rewrite sequences.

## Automated coding prompt / execution specification

Preserved prompts:

- `state/LIFE-PATTERNS-AUTOMATED-CODING-PROMPT-v1-2026-09-04.txt`
- `state/LIFE-PATTERNS-AUTOMATED-CODING-PROMPT-v2-2026-09-04.txt`

Binding execution specification:

- `docs/research/LIFE_PATTERNS_AUTOMATED_CODING_EXECUTION_SPEC.md`

Prompt v2 covers the full V2 schema including sequence, non-action, missingness, OS, evidence provenance, and influence semantics. The preferred development execution context is GPT-5.6 Sol in fresh theory-blind ChatGPT Pro contexts when that exact displayed model identity is available; the product tier is not substituted for a scientific model identity.

## Lossless codebook source / mechanical ontology projection

Added:

- `src/hdmatch/evaluation/reconciled_codebook_source.py`
- `tests/unit/test_reconciled_codebook_source.py`
- `src/hdmatch/evaluation/reconciled_ontology.py`
- `tests/unit/test_reconciled_ontology.py`

The parser:

- reads the frozen Markdown directly;
- requires the exact `NBM-R01` through `NBM-R22` primary sequence;
- preserves raw section Markdown and hashes;
- extracts exact substantive subcode IDs/descriptions/facets;
- preserves exact definitions, criteria, evidence requirements, examples, coding mistakes, provenance, IE/NA semantics, and OS rule;
- accepts source criteria represented either as Markdown bullets or as a single non-empty paragraph;
- explicitly does **not** classify non-action or rewrite substantive content.

The ontology projection uses those exact parsed fields and subcode IDs plus `OS`, marks all observables `unreviewed / not_evaluated`, and can emit only a development ontology without content-authority promotion.

## Theory-blind non-action registry boundary

Added:

- `src/hdmatch/evaluation/non_action_registry.py`
- `src/hdmatch/evaluation/non_action_registry_exchange.py`
- corresponding unit tests;
- frozen classification prompt: `state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-PROMPT-v1-2026-09-04.txt`.

The current theory-exposed project context does **not** classify the real subcodes.

A theory-blind registry must classify every real reconciled subcode exactly once as:

- `non_action`;
- `not_non_action`; or
- `ambiguous`.

Any `ambiguous` classification blocks structured-procedure freeze. The eventual raw theory-blind JSON can be imported verbatim and canonicalized without manual transcription.

## Human calibration sampling

Added:

- `src/hdmatch/evaluation/calibration_sampling.py`
- `tests/unit/test_calibration_sampling.py`

The independent human burden is reduced to focused **episode–observable units** rather than requiring every sampled episode to be coded against all 22 observables.

The sampling manifest supports two separately reported strata selected before automated labels:

1. deterministic representative sample;
2. theory-neutral boundary/prerequisite-enriched sample bound to a frozen selector specification.

Initial development burden target is roughly 60–100 focused episode–observable judgments total, with expansion only if calibration evidence is too sparse/unstable or a later statistical substitution route requires more data.

The human auditor must freeze their first-pass labels before seeing LLM labels.

## Complete automated pass validation

Added:

- `src/hdmatch/evaluation/validated_automated_pass_v2.py`
- `tests/unit/test_validated_automated_pass_v2.py`

A validated pass must prove:

- exact corpus/codebook/procedure binding;
- exact raw-output hash;
- exact deterministic normalization;
- exact frozen task-set binding;
- every expected `(task, episode, observable)` unit exactly once;
- no missing/extra units;
- every response valid against task/evidence/ontology/procedure;
- exact canonical normalized-output hash.

A schema-valid but incomplete pass is not accepted as complete research evidence.

## Cross-pass consensus

Added:

- `src/hdmatch/evaluation/structured_consensus_v2.py`
- `tests/unit/test_structured_consensus_v2.py`

Consensus requires at least three validated passes with identical corpus/codebook/procedure/prompt/task-set bindings.

Semantic comparison preserves ordered sequences, normalizes unordered value sets and set-like metadata, ignores non-substantive annotation-note differences, and applies strict majority:

- all passes agree → `unanimous`;
- >50% agree → `majority`;
- no strict majority → `unresolved`.

Unresolved units carry no fabricated consensus response.

## Validation-route integration already established

The core neutral measurement system supports exactly one frozen validation route:

1. `human_human_benchmark`;
2. `statistically_justified_llm_substitution`;
3. `automated_measurement_instrument`.

The legacy stricter H1 human-only receipt remains backward-compatible but is no longer the mandatory Life Patterns authority path.

Generic theory-blind authority is integrated into `neutral_measurement.py`; automated scoreable validation still requires a frozen calibration/validation receipt and completed `automation_evaluated` or human-baseline readiness.

Earlier verified route-integration milestone:

- head `4e9310e375f9f2d22cbe2dd70924d3d66c6a7ccd`
- CI `33873917019`
- 432 passed, 6 expected skips; Ruff clean; mypy clean across 140 source files.

## Current verified V2 milestone

Implementation-bearing head: `c923ebbbe04b4bc3306ca50d34a10b2e039012f1`

GitHub Actions CI run: `33877395747` — **success**.

The immediately preceding failing run had 458 passed, 6 failing parser tests, and 6 expected skips. The six failures all came from an overly strict Markdown-parser assumption plus one mistaken test expectation; no frozen substantive codebook content was changed. On the verified head all test, Ruff, and mypy steps pass.

## Genuine external-input boundary

No additional scientific infrastructure should be invented to avoid these dependencies.

The next required external inputs are:

1. **Theory-blind non-action registry output** covering all real `R01–R22` subcodes, generated using the frozen non-action-classification prompt. This project chat must not author those substantive classifications.
2. **Actual frozen development behavioral corpus** / participant-approved episodes and resulting V2 task set, if not already available as a valid development corpus artifact.
3. Then **three or more isolated theory-blind automated coding passes** against the exact frozen prompt/procedure/task set.
4. Then an **independent blind human calibration subset**, frozen before the human sees any automated labels.
5. Then theory-blind revision if needed and a frozen Route A/B/C validation decision.

No target-model tournament/model-fit feedback may enter before those measurement-development steps are complete.
