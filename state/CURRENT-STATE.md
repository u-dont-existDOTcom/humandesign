# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — STRATEGY REPLACEMENT IMPLEMENTATION REQUIRED.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`.

Authenticated deployment-wrapper source head: `bca426b8ab873d02fe5038d271d13b1b814fc813`; hosted repository CI is green on that source head.

## Owner real-data judgment: current product strategy failed

Direct owner feedback on the deployed real-data browser established that the surfaced fact-review workflow is low-value as a product experience. It mainly demonstrates that the model can understand/paraphrase what the owner said and then asks the owner to certify those paraphrases.

That is not the owner outcome for Discover Your Unique Life Patterns.

Owner-facing target: an unusually attentive, theory-blind conversation that produces useful distinctions, cross-context pattern hypotheses, counterexamples/boundaries, and evidence-backed self-understanding.

Current direct outcome evidence: **UNMET**.

Surfaced fact-review strategy: **REPLACEMENT_REQUIRED**.

Judgment record: `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-PRODUCT-JUDGMENT-2026-09-14.md`.

Green tests, correct semantics, and successful deployment are supporting work; they do not establish owner-facing value.

## What remains valid

The accepted v2 semantic substrate remains authoritative and does not require revision:

- target-theory blindness;
- open-world episode facts;
- append-only correction/provenance;
- genuine-absence gating;
- participant authority over person-level patterns;
- preproposal/postproposal evidence separation;
- no automatic person-level recurrence reconstruction from raw facts.

The mistake was exposing the internal evidence ledger as the participant experience. Evidence hygiene can remain internal.

## Replacement method

Task: `tasks/LIFE-PATTERNS-v2-HIDDEN-LEDGER-CONVERSATIONAL-INSIGHT-PROBE-2026-09-14.md`.

Replacement probe:

`real episode -> one discriminating follow-up at a time -> deeper/contrasting detail -> tentative synthesis only when informative -> counterexample/boundary check -> natural participant correction -> compact pattern/limit summary`

Routine fact lists and keep/edit/reject controls should disappear from the owner-facing flow. Literal/minimally normalized facts remain in the internal v2 ledger. Ask for explicit correction only when a load-bearing interpretation is uncertain or a synthesis is being adjudicated.

The next probe must show information gain beyond paraphrase: a useful new distinction, a cross-episode contrast, a boundary/counterexample that changes the hypothesis, or a compact synthesis that explains more than the source sentences individually.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

## Deployment boundary

Existing owner-only authenticated Railway surface remains available at `life-patterns-owner-production.up.railway.app`. Reuse it; do not create another service.

Authorized: bounded owner-only redesign/implementation/testing on that surface and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Next gate after implementation: **OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED**.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
