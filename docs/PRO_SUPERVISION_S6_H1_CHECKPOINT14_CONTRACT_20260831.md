# Pro supervision — checkpoint 13 verdict and checkpoint 14 contract

Date captured: 2026-08-31

## Checkpoint 13 verdict

Pro returned:

```text
OWNER DECISION REQUIRED: NO
CHECKPOINT-13 VERDICT: ACCEPTED — 48/48
```

The verdict is based on the submitted packet and its reported artifacts and tests; Pro did not
independently inspect the repository or rerun the validators. Pro recorded 48 passing, zero
failing, and no blocking defects. The accepted claim is a content-free control plane, not evidence
that the future workflow will generate valid constructs or that GPT can adjudicate P1 reliably.

Accepted implementation baseline:

- HEAD: `b2d745d350487095f355c3e8a1afc3d0d26c4154`;
- tree: `4204a3d9d17854663126c2d03fd74dd83d951c4d`;
- branch: `codex/astrohd-relationship-continuation`; and
- owner-source SHA-256:
  `97ce6179532c73e9668a5cff47b41006f49a536cf76e449084f3834847d28e59`.

## Non-blocking reporting corrections

Checkpoint 13 remains accepted. New records must incorporate two corrections without rewriting
the accepted checkpoint-13 artifacts:

1. Keep `root_contract_to_owner_alignment: PARTIAL` and `parent_outcome: OPEN` as separate fields.
   Do not use the composite value `PARTIAL_ROOT_OPEN` in new records.
2. Use `AstroHD-context-isolated content-support GPT`, or equivalent, instead of claiming the
   underlying pretrained model is chart-blind. Context and retrieval isolation do not establish
   that a pretrained model lacks latent Human Design or astrology familiarity.

These corrections do not prohibit source-constrained GPT processing and do not change the 48/48
result because no content-generation activity occurred.

## Separate supervisory states

```text
worker_to_contract_alignment: GREEN
bounded_A1_GPT_heavy_decision_to_owner_alignment: MATCH
root_contract_to_owner_alignment: PARTIAL
completion_claim: WORKING
parent_outcome: OPEN
root_completion: false
operational_alignment: PASS
scientific_adequacy: WARN
release_adequacy: NOT_APPLICABLE
release_permission: false
```

Scientific adequacy remains `WARN`. Checkpoint 13 does not establish GPT adjudication accuracy or
consistency, independent errors across runs, a valid reconciliation procedure, Joel's eligibility,
meaning preservation in actual GPT transformations, construct reliability or validity, AstroHD
mapping, birth-time recovery, or participant benefit.

## Authorized next child

# CHECKPOINT-14 — GPT ADJUDICATION PROTOCOL, RUN-INDEPENDENCE, AND REAL-USE DECISION ARCHITECTURE ONLY

This is one local, reversible, synthetic-only child. Local additive commits on
`codex/astrohd-relationship-continuation` are authorized. Push is not authorized.

The child may establish a model-agnostic protocol architecture and neutral decision dossier for
future GPT adjudication. It may not adjudicate Joel, select a model, write an adjudication prompt
or human-facing question, call an external model, or begin construct work.

## Authorized claim

The repository may establish only that it contains an evidence-informed, provenance-bound, and
synthetically tested architecture for future multi-run GPT adjudication under P1. The architecture
distinguishes model identity, run/context separation, evidence custody, sealed decisions,
disagreement, and reconciliation while leaving the actual model, prompt, evidence standard,
decision rule, and real-person execution unselected.

The child may not claim:

- GPT adjudication is valid, reliable, unbiased, calibrated, or superior to humans;
- multiple runs are statistically independent;
- agreement establishes correctness;
- Joel is eligible, ineligible, or requires adjudication;
- the protocol is ready for real-person use; or
- a model, provider, version, or reconciliation method is approved.

## Mandatory conception-before-search sequence

Before any checkpoint-14-specific methods search, freeze and commit:

- `docs/NATAL_TIME_GPT_ADJUDICATION_PREMETHOD_CONCEPTION_20260831.md`; and
- `state/NATAL-TIME-GPT-ADJUDICATION-PREMETHOD-CONCEPTION-V1.json`.

The conception must record the future adjudication problem; model versus run/context identity;
correlated-model-error risks; evidence-packet and access-order concerns; sealed initial judgments;
disagreement and reconciliation concerns; owner-override and confirmation-bias risks; candidate
independent mechanisms; constraints; and unresolved questions.

It must contain no citation or framework name, model or provider name, prompt or question wording,
real-person evidence, evidence threshold, decision rule, reconciliation algorithm, eligibility
result, construct, or AstroHD mapping content. Its exact bytes must be committed and
content-hashed before the first methods query.

## Bounded existing-work scan

The subsequent scan may cover:

- LLM-as-judge reliability and judge biases;
- prompt, order, framing, and label sensitivity;
- repeat-run consistency and correlated model errors;
- same-model versus heterogeneous-model evaluation;
- blinded and sealed evaluation procedures;
- abstention and insufficient-evidence behavior;
- model/version drift;
- reproducibility and run provenance;
- ensemble and reconciliation architectures;
- automation bias and owner influence;
- structured decision receipts and evidence citation;
- privacy and data minimization for model-mediated eligibility review; and
- synthetic evaluation and mutation testing of adjudication control planes.

The scan must search the underlying methodological problem rather than only “GPT Human Design
adjudication.” Every method family must receive exactly one classification from:

- `REUSE_DIRECTLY`;
- `ADAPT`;
- `COMPOSE`;
- `BASELINE_OR_DIAGNOSTIC_ONLY`;
- `INCOMPATIBLE`;
- `UNRESOLVED`;
- `REQUIRES_PRO_REVIEW`; or
- `REQUIRES_OWNER_DECISION`.

No final method may be selected.

## Authorized artifacts

The child may create:

- owner/baseline authority attestation;
- independent conception artifacts;
- methods scan, source ledger, and methods-decision ledger;
- GPT adjudication protocol contract;
- model/run/context identity schema;
- canonical evidence-packet manifest schema;
- initial-run commitment and decision-receipt schemas;
- access-order and run-isolation state machine;
- reconciliation-state contract;
- disagreement and procedural-invalidity registry;
- owner-influence and override threat model;
- real-use readiness gate with all execution fields unset;
- unresolved-decision register;
- neutral owner/Pro decision dossier;
- conspicuously synthetic metadata fixtures;
- test-only validators;
- single-primary content-addressed artifact manifest;
- exact 40-row acceptance matrix;
- checkpoint evidence and corrected-command ledger; and
- necessary updates to `CURRENT_PLAN.md` and `state/CURRENT-STATE.md`.

No production `src/`, API, UI, database, storage, Railway, chart, relationship, participant, or
public-release surface may change.

## Required protocol semantics

The architecture must distinguish:

- `model_provider`;
- `model_family`;
- `model_version`;
- `model_artifact_or_service_revision`;
- `run_id`;
- `context_id`;
- `context_history_digest`;
- `configuration_digest`;
- `evidence_packet_digest`;
- `decision_commitment_digest`; and
- `reconciliation_record_digest`.

All operative values remain unset or synthetic. The protocol must represent at least two
separately initialized initial-run slots, no cross-run output access before both initial
commitments are sealed, a separately initialized reconciliation slot, immutable initial
decisions, disagreement as a first-class result, insufficient evidence and procedural invalidity
as distinct from substantive outcomes, exact evidence-packet binding, exact
model/run/context/configuration binding, no owner override into `ELIGIBLE`, and no default majority
vote, averaging, confidence aggregation, or tie-break method.

Several runs under one model may be called separate runs. They may not be called independent
models or assumed to have independent errors.

## Authoritative acceptance requirements

The authoritative total is 40.

### Authority and prior-state preservation

1. `GPTA-01`: the corrected checkpoint-13 baseline, tree, and owner-source digest are exact.
2. `GPTA-02`: the incorrect expanded SHA remains a superseded transcription error.
3. `GPTA-03`: A1, P1, H1, and GPT-adjudicator authority remain unchanged.
4. `GPTA-04`: no real eligibility outcome concerning Joel exists.
5. `GPTA-05`: accepted checkpoint-8 through checkpoint-13 artifacts remain byte-identical.
6. `GPTA-06`: root completion and release remain false.

### Conception and methods chronology

7. `GPTA-07`: the checkpoint-14 conception precedes every checkpoint-14 query.
8. `GPTA-08`: it contains no citations, sources, models, providers, prompts, questions,
   thresholds, real-person evidence, or adjudication choices.
9. `GPTA-09`: it records the problem, candidate mechanisms, risks, constraints, and open questions.
10. `GPTA-10`: its bytes and digest remain unchanged after the scan.
11. `GPTA-11`: the scan records exact queries, dates, sources, versions, eligibility decisions,
    and exclusions.
12. `GPTA-12`: the scan covers model-judge reliability, run dependence, bias, drift, custody,
    sealing, and reconciliation.
13. `GPTA-13`: every method family receives exactly one permitted classification.
14. `GPTA-14`: no construct-, instrument-, chart-, relationship-, or mapping-specific search occurs.

### Identity, evidence, and access separation

15. `GPTA-15`: model identity is separate from run and context identity.
16. `GPTA-16`: context history and configuration have separate provenance digests.
17. `GPTA-17`: each initial run binds the same canonical synthetic evidence packet unless a later
    approved partition exists.
18. `GPTA-18`: one initial run cannot read another's output before both commitments are sealed.
19. `GPTA-19`: reconciliation cannot begin before both initial commitments exist.
20. `GPTA-20`: reconciliation cannot mutate, replace, or delete an initial decision.
21. `GPTA-21`: separate runs are not labeled independent models.
22. `GPTA-22`: agreement is not represented as correctness.
23. `GPTA-23`: disagreement remains visible and cannot become silent consensus.
24. `GPTA-24`: insufficient evidence, evidence conflict, procedural invalidity, and substantive
    outcomes remain distinct.
25. `GPTA-25`: no owner action can convert an adverse or unresolved result into clean eligibility.
26. `GPTA-26`: no actual decision, screening, or classification algorithm exists.

### Selection and execution embargo

27. `GPTA-27`: no model, provider, version, sampling configuration, prompt, evidence standard,
    cutoff, or reconciliation rule is selected.
28. `GPTA-28`: no external model or API is called.
29. `GPTA-29`: no real-person evidence packet is created or processed.
30. `GPTA-30`: no human-facing screening or adjudication wording is written.
31. `GPTA-31`: no construct, instrument, category, scoring rule, or mapping content is created.
32. `GPTA-32`: the real-use readiness gate remains closed and records every unresolved prerequisite.

### Synthetic and operational closure

33. `GPTA-33`: closed schemas reject unknown, personal, human-facing, construct, chart,
    relationship, mapping, threshold, and result-smuggling fields.
34. `GPTA-34`: fixtures use only conspicuously synthetic opaque identifiers and metadata.
35. `GPTA-35`: validators are test-only and absent from production imports.
36. `GPTA-36`: every substantive artifact has a content hash and exactly one primary requirement.
37. `GPTA-37`: the matrix contains exactly ordered `GPTA-01` through `GPTA-40`.
38. `GPTA-38`: the packet incorporates the checkpoint-13 terminology corrections and avoids a
    claim of pretrained-model blindness.
39. `GPTA-39`: full tests, strict mypy, exact changed-file Ruff, privacy/history/build checks,
    digest validation, protected comparisons, production-no-diff, `git diff --check`, and clean
    index/worktree pass.
40. `GPTA-40`: the return records corrections, no prohibited action, separate alignment,
    completion, and assurance states, and the open parent outcome.

Any failure blocks checkpoint-14 completion.

## Minimum hostile synthetic tests

Reject the same context used twice while labeled separate; separate runs labeled independent
models; pre-seal cross-run reading; silently different evidence packets; missing model, context,
configuration, or evidence provenance; a sealed initial judgment changed; reconciliation
overwrite; silent consensus; agreement represented as correctness; default majority vote or
averaging; owner override into `ELIGIBLE`; an actual eligibility algorithm; real-person identifiers
or evidence; human-facing prompts or thresholds; external model/API execution; construct, chart,
relationship, or mapping content; and any claim that context isolation proves the pretrained model
is chart-blind.

## Hard stops

Return immediately to Pro if real evidence concerning Joel is introduced; an eligibility result is
produced; a model, provider, version, prompt, threshold, evidence standard, or reconciliation rule
is selected; an external model/API is called; human-facing wording is written; a run sees another
initial judgment before sealing; separate runs are treated as independent models or errors;
agreement is treated as validity; owner override is permitted; construct, instrument,
measurement, or mapping content appears; construct-specific search begins; an accepted artifact
changes; production or external mutation becomes necessary; existing work substantially resolves
a contemplated bespoke mechanism but invention continues without a reuse/adapt/compose
disposition; or any privacy, provenance, test, digest, or exact-diff gate fails.

## Continuing prohibitions

No real-person adjudication or eligibility evidence; human-facing screening, consent, or
adjudication language; human contact, assessment, recruitment, compensation, assignment, or
enrollment; construct or instrument content; construct-specific search; reliability execution;
AstroHD mapping; real chart, birth-time, relationship, reference, identity, or participant data;
external model/API adjudication calls; push, remote branch, PR, merge, rebase, cherry-pick, squash,
force-update, or main mutation; GitHub-governance or stale-PR interaction; Railway mutation,
migration, configuration, secret access, or deployment; publication, disclosure, public ledger,
release, or root-completion claim is authorized.

## Return packet

Return the exact implementation head and tree, complete diff from accepted checkpoint 13,
authority and baseline attestation, conception and chronology proof, methods ledgers, protocol and
identity registry, custody/decision/access/reconciliation schemas, threat/readiness/unresolved
records, neutral decision dossier, synthetic fixture and validator hashes, manifest, exact 40-row
matrix, protected comparisons, exact-head verification, corrected commands, no-prohibited-action
ledger, and separate worker/owner/root/completion/parent/operational/scientific/release states.

Confirm that no real adjudication, human-facing content, construct work, specific search, mapping,
production work, external model call, push, merge, migration, deployment, publication, or other
external mutation occurred. No work beyond checkpoint 14 is authorized without a new Pro ruling.
