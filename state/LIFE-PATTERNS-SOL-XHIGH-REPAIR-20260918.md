# Sol xhigh and repair-first survey candidate — 2026-09-18

Status: CANDIDATE VERIFIED LOCALLY; hosted/deployed/model-response checks pending.

## Implemented

Semantic calls now request the owner-selected `gpt-5.6-sol` with `reasoning.effort=xhigh`. Literal source extraction also requests `gpt-5.6-sol`/xhigh; the initial Luna split was retired after a real-model test exposed a semantic classification dependency. This selection is immutable per request, not a shared model-object mutation. There is no fallback to Astra or a weaker semantic model. A 25,000-token total semantic output ceiling leaves room for reasoning; incomplete provider output is not silently admitted. Actual returned model/usage/latency metadata is allowlisted into private recovery, without raw reasoning or credentials. Health reports the effective profile.

Input is routed before extraction. Pure interviewer clarification/challenges produce an explanation, retraction or same-topic repair, without extracting personality facts, marking evidence sufficient, generating a synthesis or implicitly ending the area. Mixed feedback preserves exact full-context source spans and the original utterance. Explicit pause and skip are distinct. Source selection and routing survive recovery.

The active focus is retained. The final pre-send checks address unsupported premises, overlapping alternatives, means versus ends, willingness versus opportunity and context transfer. The final candidate is excluded from already-asked history during its admission check. Semantic checks are still fallible; boolean or narrative justifications are not proof.

Exact duplicate formulations are suppressed; semantic duplicate review binds to an existing proposal and checks for a material addition. A genuinely different supported inference may reuse sources. Explanations of inferential additions must anchor in actual candidate wording. Invalid candidates no longer trigger a generic fallback interrogation. Stopping refinement does not force a new synthesis. A visible pending inference cannot announce completion. Old restored drafts are rechecked before another approval, without rewriting accepted history.

Historical summaries/coverage are supplied as planning-only context, separate from actual evidence coverage. Old process-only source facts may be quarantined for interviewing; originals and their exclusion remain auditable. Summary/backup/research distinctions, the existing single renderer and pause/recovery remain intact.

## Verification so far

- Full local checkpoint: **842 passed, 7 environment/history skips**, one existing Starlette/httpx warning.
- Focused/affected workflow checks: **59 passed**.
- Browser consumer suite: **15 passed**, no page errors, six widths and reduced-motion handling.
- Ruff production/tests: PASS using the repository's current E501/I001 exclusions.
- Strict mypy: PASS across **208 source files**.
- `git diff --check`: PASS.
- Live provider responses: NOT YET TESTED. This must be completed before final delivery; use only bounded synthetic inputs, not the owner's ongoing session.

Official OpenAI Sol/Responses documentation was read for exact model/effort support and the shared reasoning/output token cap. No instruction to expose private chain-of-thought was added. Design specialist guidance was freshly read; this is an interaction hardening pass, not a visual redesign. Current visual identity, one input and controls are preserved.

## Remaining checks and limits

Reconcile hosted CI on the delivered code. Verify the actual deployed build/profile and bounded Sol response traces. Real-model sampled behavior does not guarantee universal competence or replace owner acceptance. No new research validity claim, external collection, authentication redesign, protected-main merge, or Astra comparison is part of this task.

## Actual model check and bounded correction

The first deployed candidate returned real Sol xhigh responses on four synthetic normal interview turns. It distinguished group unfamiliarity from unclear expectations, handled a clarification without adding facts or completing the topic, and separated process feedback from qualified behavioral evidence. However, it redundantly requested judgment of wording that Sol had correctly classified as direct. The cause was a legacy requirement that a cited fact have the particular `reported_appraisal_or_belief` label; the extractor had used `positive_occurrence`.

The follow-up removes that redundant label veto without relaxing source matching or semantic endorsement. All extraction is also moved to Sol xhigh, because occurrence-versus-self-report classification is semantic rather than mechanical. A clearer extraction policy distinguishes concrete events from general attributed reports. Archived old facts remain unchanged. Pending drafts from the earlier semantic policy are rechecked before approval. Fifty-seven affected tests plus lint and strict typing pass for the follow-up. Exact hosted/deployment and real-model recheck are still pending.
