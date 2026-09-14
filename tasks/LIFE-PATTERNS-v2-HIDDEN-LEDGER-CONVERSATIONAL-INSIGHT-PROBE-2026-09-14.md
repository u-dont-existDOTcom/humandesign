# Life Patterns v2 hidden-ledger conversational insight probe — 2026-09-14

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Why this task exists

Owner real-data judgment found the current surfaced fact-review method product-inadequate. The app mostly proved model comprehension/paraphrase and converted the owner into an annotator.

Controlling feedback:

`state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-PRODUCT-JUDGMENT-2026-09-14.md`

The accepted v2 semantic substrate remains authoritative. This is a product/interaction strategy replacement, not a semantic rewrite.

## Objective

Build the smallest owner-only browser probe in which the participant experiences a **normal, attentive conversation** while the v2 evidence ledger remains internal.

The owner-facing loop should be:

`real episode -> one discriminating follow-up at a time -> deeper/contrasting detail -> tentative synthesis when informative -> counterexample/boundary check -> natural-language participant correction -> useful compact pattern/limit summary`

Do not expose routine fact lists, internal evidence codes, or keep/edit/reject annotation controls.

## Interaction requirements

1. Start from one concrete real episode.
2. Ask one conversational follow-up at a time, chosen for information gain rather than form completion.
3. Follow-ups should preferentially clarify mechanisms, timing, alternatives, context, exceptions, or contrasts that could change interpretation.
4. Do not restate the participant's last message unless the restatement is needed to disambiguate a load-bearing point.
5. Keep literal/minimally normalized episode facts in the internal v2 record.
6. Ask the participant to correct a fact only when the interpretation is uncertain and materially affects a later synthesis; otherwise keep the ledger invisible.
7. Once there is enough reviewed/grounded material across episodes, surface a tentative synthesis only if it adds information beyond paraphrase.
8. Actively seek a counterexample or boundary condition before presenting a pattern as settled.
9. Preserve the distinction between:
   - “this synthesis feels true of me”; and
   - “the evidence we discussed actually supports it.”
   Ask this naturally, not as a research form.
10. A participant correction must update the internal ledger append-only and must not be silently attributed to earlier examples.
11. If no nontrivial pattern is supported, say so and continue elicitation rather than manufacturing one.

## Information-gain success criterion

The probe is not successful merely because the model understands or accurately paraphrases the owner.

Owner judgment should find at least one interaction genuinely useful because it does one or more of the following:

- exposes a distinction not explicit in the first description;
- identifies a meaningful contrast across situations;
- finds a boundary/counterexample that changes the working hypothesis;
- produces a compact cross-episode hypothesis that explains more than any single restatement;
- identifies a stable vs context-dependent vs developmental difference without forcing a fixed taxonomy.

If the experience remains primarily paraphrase plus confirmation, classify the strategy as failed rather than polishing the UI.

## Semantic boundaries

Preserve the accepted v2 contract:

- target-theory blind before lock;
- open-world positive facts;
- participant-adjudicated person-level patterns;
- append-only correction lineage/provenance;
- preproposal/postproposal evidence distinction;
- genuine absence through the existing four-gate route only;
- no raw episode-fact aggregation into person-level recurrence outside participant-adjudicated pattern logic;
- no Human Design/chart/target-model information in interviewer context.

The research ledger may be hidden from the participant; hiding it does not weaken the semantic contract.

## Implementation scope

Prefer modifying/replacing the current owner browser flow rather than adding new infrastructure.

Reuse:

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- frozen v2 validation/freeze/projection core

The currently deployed Railway service may remain the owner-only test surface. Do not create another service.

Avoid production auth/recovery/voice work; Basic auth is sufficient for this owner probe.

## Verification

Add focused tests for at least:

- one-turn-at-a-time conversational follow-up;
- hidden fact ledger creation without participant-facing fact checklist;
- no unnecessary paraphrase/review requirement after every turn;
- participant correction updates ledger append-only when a load-bearing interpretation is challenged;
- synthesis withheld when evidence is insufficient;
- cross-episode hypothesis cites grounded reviewed evidence;
- counterexample/boundary evidence can narrow or leave a pattern unresolved;
- no historical `/map` authority;
- no target-model/chart leakage.

Run focused tests plus `python scripts/task_preflight.py`. Preserve full repository CI.

## Authorization

Authorized: bounded owner-only redesign/implementation/testing on the existing authenticated owner Railway surface and owner-initiated model use.

Still unauthorized: external participant collection, downstream target-model activity, recruitment/contact, merge/release, broader public participant deployment, and unapproved spending.

## Stop boundary

Stop at **OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED** after a directly usable owner-only run. Do not scale based on technical green status alone.
