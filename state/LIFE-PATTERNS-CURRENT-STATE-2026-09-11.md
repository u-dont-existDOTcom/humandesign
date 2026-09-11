# Life Patterns current state — 2026-09-11

Status: public-safe controlling overlay for `codex/discover-life-patterns-mvp`, draft PR #24.

## Current gate

Owner-directed design-history review has now identified the **root architectural error** behind the codebook/V5 path.

The legitimate requirement was: competing target models must consume the same frozen, theory-blind behavioral substrate and must not reinterpret raw narrative differently after model predictions/results are available.

The unjustified substitution was: therefore the substrate must be a comprehensive externally coded behavioral ontology with fixed categorical values, frozen aggregation, and external-coder reliability as the primary measurement instrument.

That implication does not hold.

Root-cause audit:

`docs/research/LIFE_PATTERNS_CODEBOOK_ARCHITECTURE_ROOT_CAUSE_AUDIT_2026-09-11.md`

The fixed V5/codebook route is therefore no longer presumed to be the primary Life Patterns architecture. Historical artifacts remain immutable development evidence and contain reusable mechanics. Owner UI review and human collection remain paused.

## Where the drift occurred

The initial product roadmap at commit `026be220b18bbfd10ccfb1ac8d0db69f2d7f8971` already centered an attentive adaptive interview, participant-confirmed summaries, counterexamples, context differences, and a participant-reviewed Life Patterns Map. It also contained an untested `model requirements -> neutral ontology -> interview -> freeze -> scoring` assumption.

The participant-reviewed freeze at `6677f3866bcb6c79a824fea24ce1efb62dd847a7` still preserved the right semantic center:

`chart-blind interview -> participant-approved episodes -> neutral Life Patterns Map -> participant review of map claims -> immutable behavioral freeze -> later model tournament`

The tournament boundary at `7e294c18962342c06149815721c560d9179796c2` correctly required a frozen measurement bridge to prevent model-specific post-hoc interpretation. But it prematurely named a neutral ontology as the solution.

The decisive fork occurred in the neutral bridge specification at `5d40e6608ff7af3c8550d4eb5d746ccac6fa5088`, which made:

`immutable behavioral freeze -> versioned neutral ontology -> coded observable evidence`

the common Stage-A instrument, explicitly treating the shared ontology/coder as the main measurement instrument and person-level summaries as frozen aggregations over episode codes.

That was a category error: stable shared representation was conflated with fixed taxonomy, and an idiographic participant-adjudicated pattern product was pushed into a standardized external-annotation paradigm.

## Downstream symptom discovered in owner review

The later V5 work was often mechanically careful **conditional on the ontology premise**. It improved absence semantics, facets, stages, provenance, containment, cardinality and anti-double-counting.

But the architecture kept adding machinery when ordinary behavior did not fit cleanly. Owner review exposed the consequence directly:

- a choice was plainly delayed;
- the narrator explicitly described the proposed course as too difficult;
- there was a later resolution/rejection;
- yet the closest named value involved a stronger absence claim whose feasibility gate could not be established.

The four-part absence gate was not the problem. The problem was that failure of the stronger code could erase or demote clear positive facts. Historical V2's `OS` gap path was also dropped in V5, further exposing the closed-world assumption.

## Replacement architecture

Public-safe owner-directed architecture:

`docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`

Core principle:

> Episodes are grounding evidence. GPT/human coding may organize literal facts and propose candidate structure, but the participant is the primary authority on whether a recurring person-level pattern actually characterizes them and under what conditions.

Preferred loop:

`episode -> minimal factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

The episode layer should preserve simple facts with minimal inference: what happened, timing/sequence, outcome/resolution, explicitly narrator-reported appraisal/reason, context, and separately gated genuine absence/nonoccurrence claims.

Examples elicited after a pattern proposal are mainly useful for nuance, scope, contradiction and better subsequent questions. Their availability is not an unbiased empirical recurrence sample. A claimed pattern with no retrievable examples is a discrepancy to probe, not an automatic label such as poor self-awareness.

## Mechanics retained from historical V5 work

The following remain useful and should not be discarded merely because the primary architecture changes:

- independent V5 review `ce04642146c41a7d5d94f85360572c78de887682`;
- mechanically verified implementation head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02` / CI `34623829382`;
- exact provenance and immutable/content-addressed artifacts;
- missingness distinct from negative evidence;
- strict awareness/opportunity/reasonable-feasibility/nonoccurrence gates for genuine absence claims;
- no post-hoc recoding after target-model results;
- theory-blind substantive repair/review;
- useful stage/evidence ownership mechanics where a revised representation actually needs them.

These are reusable components, not proof that the fixed 22-observable taxonomy must remain the main instrument.

## Corrective invariants

Future semantic work must preserve the audit's guardrails:

1. neutrality does not imply a closed taxonomy;
2. participant-level recurrence requires participant adjudication;
3. observed fact, narrator appraisal, system hypothesis, participant pattern judgment and absence claim are separate epistemic layers;
4. absence gates apply only to absence claims and cannot erase positive facts;
5. elicited examples are not automatically frequency evidence;
6. recurring OS/abstention/schema growth is a signal to revisit the abstraction;
7. every structured field/category must have a clear downstream purpose;
8. validation machinery may not dictate participant-facing semantics;
9. clear positive behavior must remain representable in an open-world gap path;
10. every semantic expansion must be checked against the product north star: **Discover Your Unique Life Patterns**, not completion of a behavioral ontology.

## Exact next action

Run in a **fresh target-theory-blind context**:

`tasks/LIFE-PATTERNS-PARTICIPANT-CO-CODING-SEMANTIC-REPAIR-WORKER-2026-09-11.md`

The worker is now explicitly retargeted by the root-cause audit. It must first determine the **minimum shared frozen substrate actually required** to prevent model-specific reinterpretation; it must not assume the current fixed ontology is necessary.

Required outputs are candidate architecture/schema artifacts plus a separate blind-review prompt. Do not implement production changes until that independent blind review passes.

## Private calibration source remains frozen

The exact private transport and inner receipt remain verified and unchanged:

- outer ZIP SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`;
- inner LPHB2 receipt SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`;
- selected historical coverage remains 44 episode + 22 series units.

The private V5 owner-review candidates remain development evidence of how the flaw was discovered; they are superseded for acceptance.

## Hard boundaries

- no target-theory information in the semantic repair context;
- do not preserve the fixed taxonomy merely because it already exists;
- do not weaken genuine absence/non-action gates merely to force a case into a category;
- do not discard supported positive behavior because a stronger claim fails;
- do not treat elicited examples as unbiased recurrence evidence;
- do not give an external classifier final authority over person-level recurrence;
- no human collection, automated participant coding, target-model scoring/reveal, merge/deploy, recruitment/contact, or spending until the revised blind semantic chain authorizes it.

## Preserved owner correction

**There was never a completion policy.** That premise was invented earlier and must not be recreated or inferred from artifact counts.
