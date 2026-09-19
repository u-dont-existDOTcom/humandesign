# Life Patterns v2 — multi-pattern owner interview continuation — 2026-09-14

Status: **ITERATION — OWNER-ONLY PRODUCT CONTINUATION**.

Repository: `u-dont-existDOTcom/humandesign`  
Branch: `codex/discover-life-patterns-mvp`  
PR: #24 — keep draft/open/unmerged.

## Owner outcome

The one-pattern pattern-first probe passed direct owner judgment. Preserve that interaction quality while removing the artificial dead end after one adjudicated pattern.

The next reversible product step is **not** external collection, full persistence, a fixed questionnaire, or a closed taxonomy. It is a continuing owner-only interview surface with a coherent next action after each completed pattern.

## Required behavior

After a terminal accepted/rejected/unresolved pattern result:

1. show `Explore another pattern`;
2. show `Finish for now`;
3. `Explore another pattern` starts a fresh bounded backend conversation session and shows the normal pattern-first opening;
4. prior completed pattern result(s) remain visible in the current browser page;
5. `Finish for now` shows a compact summary of completed pattern results without claiming the participant is scientifically complete;
6. provide a one-click client-side copy/export of the visible interview and completed results for optional supervisor sharing.

Use a fresh backend session per pattern thread in this iteration. This is deliberate: it prevents hidden evidence from one pattern thread from silently becoming grounding for another while the multi-thread evidence architecture is still being developed.

## Privacy / observability

Current runtime narratives remain process-memory-only. The supervising Chat cannot automatically read them through Railway because request bodies/session memory are not exposed by the available Railway tooling.

Do not add private transcript logging, Git persistence, or public telemetry to solve that. The bounded iteration may keep a browser-local transcript/result list and offer copy/export only when the owner chooses it.

## Scientific / semantic invariants

Preserve:

- pattern-first elicitation;
- target-theory blindness;
- hidden v2 evidence ledger;
- participant authority over person-level claims;
- append-only corrections within each successful backend thread;
- genuine-absence gate;
- preproposal evidence timing;
- no automatic person-level reconstruction from raw episode facts;
- no historical `/map` authority;
- no birth/chart/model concepts in the interview/evidence layer.

No fixed completion denominator. Historical domains remain optional coverage scaffolding only, not an exhaustive ontology.

## Verification

Add focused UI regressions proving:

- the old terminal `end of this bounded probe` wording is gone;
- `Explore another pattern` exists;
- `Finish for now` exists;
- supervisor copy/export exists;
- hidden-ledger / no-annotation assertions remain intact.

Run the focused Life Patterns owner conversation tests plus affected pattern-first tests. Hosted CI on the candidate head should be green before treating the deployed iteration as ready for owner use.

## Deployment boundary

Updating the existing authenticated owner-only `life-patterns-owner` Railway service is authorized. Do not create a new service or broaden access.

## Stop condition

Stop after the updated owner-only surface is deployed and verified to expose a coherent post-pattern frontier. The next owner evidence is whether repeated pattern threads still feel useful and whether the session-level summary is useful enough to justify the next persistence/profile step.
