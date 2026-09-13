# Life Patterns v2 owner-development prototype — method fork — 2026-09-13

Status: ACTIVE BOUNDED EXPERIMENT. This selects the next development phase after the verified v2 core implementation. It does not authorize external participant collection, target-model work, merge/deploy, recruitment/contact, or spending.

## What the owner asked for

After the participant-adjudicated v2 semantics and bounded core implementation pass, test the actual Life Patterns interaction before scaling the instrument: episode evidence -> candidate pattern question -> participant adjudication/correction -> refined accepted/rejected/unresolved pattern.

The purpose is to determine whether the product experience is genuinely useful and natural, not merely whether schemas and validators pass.

## Genuine constraints

- The frozen v2 semantic candidate and accepted contract remain unchanged.
- Person-level recurrence/typicality cannot be inferred into the frozen adapter projection from raw episode facts; accepted person-level patterns require participant adjudication.
- GPT may propose a candidate pattern from evidence, but it does not decide that the pattern characterizes the participant.
- Post-first-proposal examples are scope/boundary evidence, not an unbiased recurrence-frequency sample.
- Genuine absence claims retain the four-gate absence route.
- No target-model/chart/birth-derived information may influence the prototype.
- Private owner/development narratives remain private runtime data and must not be committed to Git.

## What is additionally being assumed

Use a very small interactive development harness bound directly to `src/hdmatch/evaluation/participant_adjudicated_v2.py`, rather than immediately repairing or extending the historical full Life Patterns web stack.

Origin: `assistant_hypothesis`, bounded by the previously agreed owner-testing sequence.

## Why it matters

The historical `life_patterns_app.py` / `life_patterns_interview_app.py` path contains pre-v2 map-generation semantics that can synthesize person-level patterns from approved episodes. Reusing that path as-is would risk reintroducing the architecture that v2 replaced. Conversely, building full auth/recovery/voice/deployment infrastructure before checking the new interaction would create substantial product and implementation commitment before owner usability evidence exists.

## Simplest live alternative

A pure chat mockup with no code integration.

## What would fail without the added method

A chat-only mockup can test wording but cannot establish that accept/edit/reject/unresolved decisions, append-only fact corrections, proposal timing, evidence roles, and resolved-pattern records survive the actual v2 implementation boundary.

Therefore a small implementation-bound harness is justified as a reversible experiment. A production-grade web application is not established as necessary at this stage.

## Concrete ordinary case

Existing private development episode at runtime -> system presents a few source-grounded episode facts -> owner corrects/accepts them -> system proposes a candidate recurring pattern as a question -> owner accepts/revises/rejects/unresolved -> one revised question may follow -> the harness shows the resulting v2 record and accepted wording with scope/exceptions. No target model is available anywhere in the flow.

The owner must actually make those decisions at runtime. A deterministic transcript with preselected correction/revision/acceptance verifies plumbing only and does not reach owner product judgment.

## Current method status

`UNRESOLVED` for the eventual product surface; `ESTABLISHED` only that an implementation-bound interactive probe is needed before scaling.

## Recommended next action

Repair `LP-PAN-v2-PROT-001` by adding the smallest owner-controlled runtime interaction over the existing prototype. Do not add production auth, recovery, voice, deployment, generalized map generation, model scoring, or broad participant collection.

Owner action: `NONE` until the interactive repair is green; then `OWNER PRODUCT JUDGMENT`.

## Success / stop boundary

The experiment succeeds only if the owner can directly judge a complete interaction slice and the generated v2 record preserves the accepted semantics. Technical green tests alone are not sufficient.

Stop after a small owner-usable prototype and focused tests. Return to the supervising chat for product judgment before broadening the implementation.

## Internal provenance

- Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Bounded core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Scripted prototype head: `1624c94f9ed130a446d86eed7fafd4309255c4a6`
- Defect: `state/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-INTERACTION-DEFECT-001-2026-09-13.md`
- Repair task: `tasks/LIFE-PATTERNS-v2-OWNER-PROTOTYPE-INTERACTION-REPAIR-001-2026-09-13.md`
- Universal method-fork guidance: `u-dont-existDOTcom/universal-dev-architecture/templates/METHOD-FORK-CARD.md`
