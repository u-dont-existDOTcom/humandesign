# Current state

## Life Patterns — 2026-09-14

Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED.

Frozen semantic candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`.

Independent semantic review: **PASS** — zero blockers, `semantic_change_required=false`.

Bounded v2 core repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`.

Real-data owner browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`.

## Owner real-data judgment: surfaced paraphrase strategy failed

Direct owner feedback on the first deployed real-data browser established that the surfaced fact-review workflow was low-value as a product experience. It mainly demonstrated that the model could understand/paraphrase what the owner said and then asked the owner to certify those paraphrases.

That is not the owner outcome for Discover Your Unique Life Patterns.

Owner-facing target: an unusually attentive, theory-blind conversation that produces useful distinctions, cross-context pattern hypotheses, counterexamples/boundaries, and evidence-backed self-understanding.

Prior surfaced fact-review strategy: **FAILED / REPLACEMENT_REQUIRED**.

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

The mistake was exposing the internal evidence ledger as the participant experience. Evidence hygiene remains internal.

## Replacement implemented: hidden-ledger conversational insight probe

Task: `tasks/LIFE-PATTERNS-v2-HIDDEN-LEDGER-CONVERSATIONAL-INSIGHT-PROBE-2026-09-14.md`.

Implementation receipt: `state/LIFE-PATTERNS-v2-HIDDEN-LEDGER-CONVERSATIONAL-IMPLEMENTATION-2026-09-14.md`.

Exact conversational source head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`.

Hosted GitHub CI on that exact head: **SUCCESS** — unit/integration tests, Ruff, and mypy passed.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_conversation.py`
- `src/hdmatch/api/life_patterns_v2_owner_conversation_ui.py`
- authenticated deployment entrypoint `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- focused regression tests `tests/unit/test_life_patterns_v2_owner_conversation.py`

Owner-facing loop:

`real episode -> one discriminating follow-up at a time -> deeper/contrasting detail -> tentative synthesis only when informative -> counterexample/boundary check -> natural participant correction -> compact pattern/limit judgment`

Routine fact lists and keep/edit/reject controls are gone from the owner-facing flow. Literal/minimally normalized facts remain in the internal v2 ledger. Explicit participant judgment is reserved for the consequential person-level synthesis.

The conversational planner is instructed to optimize for information gain rather than proof of comprehension. It may request a contrasting situation instead of mining trivial detail, and a formal cross-episode hypothesis is withheld until a boundary/counterexample question has been answered. Any surfaced hypothesis must cite operative hidden facts from at least two episodes and cannot be an exact restatement of one cited fact.

Participant corrections to hidden facts remain append-only with lineage and provenance. Genuine absence is not silently inferred or admitted by this minimal extractor; the accepted four-gate route remains authoritative.

The historical automatic `OpenAILifePatternsMapper` / `/map` person-level authority remains unused.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

## Owner-only deployment

The replacement is deployed on the existing authenticated Railway surface; no new service was created.

- domain: `life-patterns-owner-production.up.railway.app`
- service: `life-patterns-owner`
- conversational deployment ID: `aabaaaaf-5178-40a8-afe0-2150a6846f45`
- source head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- deployment status: **SUCCESS**
- deploy log: application startup complete; `/healthz` returned HTTP `200`
- owner-facing routes remain HTTP-Basic protected
- runtime model credentials remain Railway references; no API secret is committed

## Current outcome / next gate

Replacement-strategy technical state: **IMPLEMENTED AND DEPLOYED**.

Direct owner-facing information-gain evidence for the replacement: **NOT YET MEASURED**.

The next decision-changing evidence is owner use of the deployed conversational surface. Success requires at least one interaction that genuinely adds information beyond paraphrase: a useful new distinction, a cross-situation contrast, a boundary/counterexample that changes the hypothesis, or a compact synthesis that explains more than the participant's source sentences individually.

If it remains essentially paraphrase plus confirmation, classify the replacement strategy as failed rather than cosmetically polishing it.

Authorized: bounded owner-only testing of the deployed conversational probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

Current task lock: `tasks/ACTIVE-TASK.json`.

**There was never a completion policy.** Do not infer one from artifact counts, test counts, review status, or gate status.
