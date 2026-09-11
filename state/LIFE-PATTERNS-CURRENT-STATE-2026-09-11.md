# Life Patterns current state — 2026-09-11

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. GitHub is canonical; historical artifacts remain immutable.

## Current gate

**The blind V5 semantic/contract gate and the public mechanical implementation gate have both PASSED.**

The current blocker is narrower: the exact existing **private V2 handoff** has not yet been regenerated through the final V5 builder, browser-smoked as the real private package, and accepted by the owner for usability. Independent human collection remains blocked until that owner UI gate passes.

No qualifying independent human first-pass annotations have been collected. No automated Life Patterns participant coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Accepted blind semantic chain

The record-containment repair is frozen at:

`320cb577f4adfbcc644c986f7f532feef0fbe80b`

The independent fresh blind V5 regression review is frozen at:

`ce04642146c41a7d5d94f85360572c78de887682`

That review re-graded all **47 carried findings** — 45 original OA blockers, `NR-001`, and `NR2-001` — and resolved all 47 with no partial, unresolved, regressed, or new blocking finding. It preserved the accepted R05, absence/missingness, stage-local cardinality, response-contract, record-containment, and same-act anti-double-counting semantics, with `semantic_change_required=false` and `safe_for_implementation=true`.

Public verification receipt:

`state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`

## Public V5 mechanical implementation — VERIFIED

Owner-facing implementation code head:

`35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`

GitHub Actions CI `34623829382`: **SUCCESS**.

Verification result:

- **675 passed, 7 expected skips, 0 failed**;
- Ruff: **all checks passed**;
- strict mypy: **no issues in 174 source files**.

Public verification receipt:

`state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`

### Implemented measurement mechanics

The V5 graph implementation now enforces the accepted response-level record model and referential integrity, including:

- direct containment of value assertions, component assertions, absence conditions, provenance, stages, windows, and evidence units;
- exact-one typed reference resolution within one observable response;
- unique component binding to one event stage and that stage's evidence unit;
- stage-local cardinality;
- cross-facet co-presence without inventing temporal order;
- same sourced fact anti-double-counting;
- claim-specific provenance;
- four-part absence gates;
- distinct handling of mixed hybrid values versus pure absence-dependent values;
- retention of a supported hybrid affirmative component when its paired absence gate is insufficient, without asserting the combined parent value;
- the recurrence-v2 firewall for repeated series, including no fake independent frequency support from a confirming anecdote.

A prior implementation-only assumption that every component had to belong to a hybrid parent was rejected. Pure absence-dependent values such as `R14-i` require one separately gated absence component. The focused V5 graph and development-envelope tests cover this distinction.

## Final V5 human-first UI implementation — VERIFIED PUBLICLY

The controlling owner-facing builder is:

`scripts/build_life_patterns_human_calibration_ui_v5_final.py`

It reuses the verified final V2 auditor surface while leaving historical V2 builders/contracts unchanged. The human layer now:

- groups choices by behavioral facet instead of asking one global relation question;
- never turns cross-facet co-presence into a global ordered sequence;
- asks same-facet stage separation only when multiple active facts create a real stage/window question;
- asks chronology only after distinct stages are established and creates temporal edges only when the auditor explicitly establishes the order;
- separates hybrid affirmative and absence components;
- retains the affirmative fact if the absence gate is insufficient while withholding the combined hybrid parent;
- uses claim-specific quote provenance when multiple exact source segments exist and automatic provenance when there is only one source;
- hides graph/stage/evidence IDs from the human task;
- exports versioned V5 episode/series response envelopes;
- keeps the existing auditor attestation boundary;
- remains offline / no-network;
- uses **“Doesn't apply to this story”** only when the prerequisite is affirmatively absent and **“Not enough information”** when the exact source is insufficient; silence/non-mention does not count as not-applicable.

The browser exporter is tested by executing its pure JavaScript graph builder under Node and validating the resulting envelopes with the Python V5 models/contract for both a gated pure absence (`R14-i`) and a partial hybrid (`R05-O2`). Synthetic private-handoff builds are also tested for byte preservation and plaintext non-leakage.

## Exact next gate — real private V5 regeneration, browser smoke, owner review

Use:

`tasks/LIFE-PATTERNS-V5-PRIVATE-UI-REGEN-OWNER-REVIEW-WORKER-2026-09-11.md`

The next worker must use the **exact existing private V2 handoff** identified by the preserved private receipt. It must not reconstruct participant evidence from public state and must never commit private participant narrative or generated private HTML.

Required sequence:

1. verify the exact private handoff bytes against the preserved receipt;
2. build the final offline V5 UI with `scripts/build_life_patterns_human_calibration_ui_v5_final.py`;
3. browser-smoke the real private build, including save/reload, partial hybrid handling, absence fallback semantics, claim-specific provenance where applicable, V5 response download, progress backup, and auditor attestation;
4. return the private UI/package to the owner for usability review;
5. only after explicit owner acceptance, record the acceptance publicly without exposing private evidence and unlock the independent human first pass.

## Hard boundaries

- **human collection is not authorized yet**;
- existing/superseded auditor kits remain ineligible for new human collection;
- never commit private participant narrative, private handoff bytes, or generated private calibration HTML;
- no automated participant coding before the revised independent human first pass is completed and frozen;
- no target-model scoring/reveal;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.

## Preserved owner correction

The unrelated owner-test invariant remains binding: **“there was never a completion policy. that was invented nonsense by codex.”** Do not recreate a completion-policy premise or silently turn artifact counts into such a policy.
