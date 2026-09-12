# Life Patterns Model Tournament — Independent Conception Snapshot

Status: pre-existing-work-scan conception snapshot. This records the independent design before consulting external literature/standards for the next milestone.

Date: 2026-09-03
Parent branch state before this snapshot: `593d27b4ae1f1a679ffcca5b3e0cd02d4e64310e` on `codex/discover-life-patterns-mvp` / PR #24.

## Problem

The Life Patterns architecture now has a theory-blind interview, participant-approved episodes, a neutral evidence-linked map, participant claim review, and a content-addressed immutable behavioral freeze. The next scientific boundary is to let separately specified birth-derived models consume an exact behavioral freeze without:

- retroactively changing the behavioral evidence;
- allowing model outputs to change which behavioral claims count;
- silently selecting favorable model variants after seeing a participant result;
- conflating development, confirmatory testing, and post-hoc exploration;
- treating the participant's act of freezing their profile as consent to birth-model analysis;
- obscuring which exact code/data/model version produced each result.

## Candidate mechanism

Separate **analysis authorization**, **model roster/manifest freeze**, **execution**, and **reveal**.

### Analysis authorization

A participant who has created a behavioral freeze may explicitly authorize a named analysis scope. Authorization should bind to:

- exact `freeze_sha256`;
- stated model families to be run;
- whether exact birth data will be used;
- purpose (research comparison vs participant-facing curiosity/reveal);
- what outputs may be stored;
- whether the analysis result may be shown immediately or retained blinded for a study protocol.

The behavioral freeze itself must remain usable without giving this authorization.

### Tournament manifest

Before executing a confirmatory comparison, create an immutable manifest that binds:

- exact behavioral freeze hash;
- exact birth-input record hash and civil-time/location interpretation receipt;
- exact model roster;
- per-model status: `confirmatory_predeclared`, `development_only`, or `exploratory_posthoc`;
- exact model implementation/version/commit/configuration;
- exact mapping/scoring contract;
- candidate universe and aggregation semantics where reverse matching is involved;
- exact metrics and tie handling;
- missing-data/uncertain-claim policy;
- exclusion rules;
- model complexity accounting where applicable;
- reveal policy;
- random seeds or deterministic execution identity where relevant.

Manifest identity should be a canonical SHA-256 and every result should bind to it plus the behavioral freeze hash.

### Execution boundary

A tournament runner receives only:

1. immutable behavioral freeze artifact;
2. separately authorized birth/astronomy input;
3. immutable tournament manifest;
4. pinned model adapters.

The runner must not mutate any of them. Result artifacts are append-only/content-addressed.

### Baseline requirement

A meaningful tournament cannot be only `HD vs astrology vs AstroHD`. It needs at least one non-birth/context or prevalence baseline appropriate to the exact prediction task. Otherwise a model can appear useful merely by reproducing common behavioral statements.

### Development vs validation

Model development and model comparison must be separated at the person/cohort level. Owner data and any participants whose responses influenced model/mapping design are development cases, not untouched validation.

A model family may remain in the system as `development_only` without being counted as confirmatory evidence.

### Reveal

Reveal is downstream from locked execution. Revealing a result can never alter the prior behavioral freeze or confirmatory result. Any mismatch exploration after reveal is explicitly post-hoc and stored separately.

## Candidate result object

Each model result should include at minimum:

- `freeze_sha256`;
- `tournament_manifest_sha256`;
- `model_id` and model-manifest hash;
- execution timestamp/runtime commit;
- prediction outputs sufficient to reproduce the score;
- score/rank/calibration metrics defined before execution;
- uncertainty/tie information;
- result status (`confirmatory`, `development`, `exploratory`);
- machine-verifiable receipt hashes;
- no mutation channel back into the behavioral record.

## Constraints

- no model execution before explicit analysis authorization;
- no model-family roster changes after a confirmatory tournament manifest is frozen;
- no choosing metrics after seeing the participant result;
- no post-reveal behavioral edits entering the already-run confirmatory score;
- no owner/development case described as untouched validation;
- no hidden use of outcome success to reinterpret decision-process evidence;
- uncertain/rejected behavioral claims handled according to a frozen policy, not improvised per participant;
- exact birth/civil-time/location handling must be independently auditable;
- model complexity/overfitting must matter when comparing increasingly flexible models;
- no merge/deployment/participant analysis authorized by this snapshot.

## Candidate insight

The core object is not "a score" but a **triple binding**:

`behavioral freeze hash + tournament manifest hash + model implementation hash -> immutable result`

This makes the scientific question auditable: what exact participant evidence, exact preregistered comparison contract, and exact model generated the reported result?

## Existing-work questions to scan

Search the underlying problems rather than project terminology:

- preregistration / registered reports and specification of confirmatory vs exploratory analyses;
- model comparison and predeclared analysis plans;
- data leakage and adaptive overfitting from repeated evaluation;
- nested cross-validation / held-out validation for model development;
- benchmark and model-card / dataset-card versioning and provenance;
- cryptographic/content-addressed reproducible analysis manifests;
- informed/dynamic consent for secondary analysis of participant data;
- baseline selection and proper scoring/calibration for predictive comparisons;
- multiple-comparisons/model-selection corrections where many model variants are tested.

After the scan, explicitly choose reuse, adaptation, composition, invention, or experiment for each component.