# Life Patterns v2 owner real-data product judgment — 2026-09-14

Status: **PRODUCT STRATEGY FAILED / REPLACEMENT REQUIRED**.

## Owner-outcome evidence

The owner tested the authenticated real-data browser prototype and judged the experience low-value: the interaction mostly demonstrated that the model could understand an episode, paraphrase it, and ask the owner to certify the paraphrase. The owner did not experience that as the intended value of Discover Your Unique Life Patterns.

This is direct product evidence. It supersedes any inference from green tests, successful deployment, semantic correctness, or faithful implementation that the current interaction strategy is advancing the product outcome.

## Outcome assessment

Owner-facing target: an unusually attentive, theory-blind interview that produces useful distinctions and evidence-backed self-understanding rather than a personality quiz or an annotation workflow.

Current direct evidence: **UNMET**.

Outcome advancement for the surfaced fact-review strategy: **FLAT / FAILED AS PRODUCT EXPERIENCE**.

Strategy efficacy: **REPLACEMENT_REQUIRED**.

The current strategy must not receive another cosmetic copy/UI iteration before the interaction method changes.

## What failed

The surfaced flow was:

`episode -> model paraphrase/fact list -> owner keep/edit/reject -> repeat -> tentative pattern -> owner formal adjudication`

That flow made the evidence plumbing the product. The owner was asked to do annotation work that is scientifically useful internally but intrinsically uninteresting as an interview experience.

The main failure is not that the model misunderstood the owner. The failure is that correct understanding produced almost no information gain for the owner.

## What remains valid

This judgment does **not** reopen the accepted v2 semantic substrate.

Preserve:

- target-theory blindness before behavioral lock;
- open-world episode facts;
- append-only corrections/provenance;
- genuine-absence gating;
- participant authority over person-level pattern claims;
- separation of preproposal vs postproposal evidence;
- no automatic reconstruction of person-level recurrence from raw episode facts;
- the distinction between “this feels true” and “these examples support it.”

These are evidence-layer constraints. They do not require the participant to see or operate the ledger directly.

`semantic_change_required=false`.

## Method-necessity / manufactured-prerequisite check

### Owner outcome

Produce a conversation that helps the participant discover meaningful recurring and context-dependent life patterns while remaining useful even if all downstream birth-derived models fail.

### Genuine constraints

The interview must remain theory-blind; person-level claims must remain participant-adjudicated; evidence provenance and uncertainty must remain recoverable; unsupported inference and missingness laundering remain prohibited.

### Failed method

Expose the internal evidence ledger as fact-by-fact keep/edit/reject work and formal pattern adjudication controls.

This method was assistant-introduced. It is **not** required by the accepted semantics.

### Stronger simpler alternative

Keep the evidence ledger internal. Let the participant experience a normal conversation. The model should ask discriminating follow-up questions, notice contrasts/counterexamples/context switches, and surface a synthesis only when it adds information beyond paraphrase. Ask for correction only when a load-bearing interpretation is uncertain or when a proposed pattern is being summarized.

### Decision

The surfaced annotation workflow is rejected as the owner-facing method.

The hidden-ledger conversational method is **UNRESOLVED but live** and should be tested in one bounded reversible probe before broader architecture work.

## Required information gain in the next probe

The next probe must test whether the interviewer can do at least one of the following in a way the owner finds genuinely useful:

- ask a follow-up that reveals a distinction the initial episode did not already state;
- identify a meaningful contrast between episodes;
- find a counterexample or boundary condition that changes a tentative pattern;
- propose a compact cross-episode hypothesis that is more informative than restating the episodes;
- distinguish stable, context-dependent, developmental, or exception-limited behavior without forcing a taxonomy.

Fact extraction that only paraphrases the participant may remain as hidden research plumbing, but it is not sufficient owner-facing value.

## Stop / next gate

Stop iterating the current visible fact-review interface.

Next strategy: a **hidden-ledger conversational insight probe**. It must preserve the v2 evidence contract internally while removing routine participant-facing annotation work.

External participant collection, target-model activity, merge/release, recruitment/contact, and broader public deployment remain closed.
