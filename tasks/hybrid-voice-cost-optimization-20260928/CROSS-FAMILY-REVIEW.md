# Cross-family architecture review — voice-first / compact Railway

Date: 2026-09-28
Reviewer: Claude Opus 5.5 max
Private participant data supplied: no
Paid participant inference used: no

## Initial review

Models: ['claude-opus-5-5']
Error: False

**VERDICT: FINDS_ERROR**

**Weakest load-bearing step**
Routine calls use the accepted-evidence ledger plus four recent turns in place of the source they no longer send (see the `relevant_turns` comment). That ledger is incomplete by design:
- Bulk review is told to leave source unassessed, under a 5k-token cap.
- Routine facet vocabulary is limited to the guide entries of the pending turn's route.

The reviewer does not make up for this. It sees only turns the planner cited, and only those already in the planner's context (`make_review_context`). So nonredundancy, dropped conditions and correction re-checks are all judged against material the planner chose or wrote.

**Concrete failing case(s)**

1. **Dropped condition (A).** Two turns are pending:
   - P1: "I usually speak up when I disagree."
   - P2: "Except with my dad—there I go quiet."

   If the planner quotes only P1, the reviewer receives only P1 and passes the scope check. A full-context reviewer would have seen P2. When a fresh-route `ask` carries no evidence, the reviewer gets zero turns. So the probe's first-pass G19 approval barely tests nonredundancy.

2. **Correction re-check (A, PR #42).** `relevant_turns` adds turns that correct a wanted turn. It never adds the turn a pending correction points to.
   - If turn 40 corrects turn 9, turn 9 is missing unless it is recent or an antecedent.
   - The planner then re-checks against `existing_evidence.source_quotes`, which is the disputed reading's own excerpt.
   - If the planner cites turn 9 anyway, the reviewer filter drops it because it is not in planner context.

3. **Redundant question (A).** A long voice answer to G5 also describes the scene G19 asks about. G19 shares no context source or guide entry with G5.
   - The sparse bulk pass records nothing on G19's facets.
   - Later, G19 is not "presented" because that check is by ID, and its targets look uncovered, so it ranks first.
   - The G5 turn is neither recent nor an antecedent, so neither the planner nor the reviewer sees it.

   The participant is asked again. Native sessions reach the same state after four turns, because G19's facets were never in G5's vocabulary.

4. **Route gating (B).**
   - Excluding presented routes blocks a same-route context repair after "I'm not sure what you mean". Bulk mode still allows presented routes.
   - The four follow-up slots fill in bank order. After a large import, stale early follow-ups push out the follow-up to the turn just answered.
   - Dependency is checked by ID only. The voice export writes `null` when the ID is unknown, so real antecedents never unlock their dependents. In the other direction, `answered_route_ids` ignores `quarantined` and counts any non-None answer.
   - Ranking by coverage, then bank position, turns the menu into a queue of the bank's first routes. Coverage becomes the selector the prompt says it is not.

**Smallest repair**
Required:
1. In `make_review_context`, take turns from `state["turns"]` rather than from planner context. Include all non-quarantined pending turns, the cited turns, the `correction_of` chain in both directions, and the source turns of `prior_evidence_being_amended`.
2. Add the reverse `correction_of` link in `relevant_turns`.
3. Give review-stage corrections the bulk budget plus every source turn cited by evidence. These are rare and are the PR #42-critical path.

Next:
- Have the bulk plan return `addressed_route_ids` mapped to turn IDs, verified by the reviewer. Store them as routing metadata and exclude those routes from eligibility. Send their turns whenever a related route is shortlisted.
- Build routine vocabulary from the guide entries of both pending and shortlisted routes.
- Always shortlist follow-ups whose `context_sources` intersect the pending routes. Allow a route-tied repair of the route just presented.
- Recover imported route IDs by exact match against canonical wording. Exclude quarantined turns from `answered_route_ids`.

**Railway optimization deployability**
The validators, the default-deny retrospective filter and the scoping of absence claims are sound. Deploy the compact context once repairs 1–3 land. Repairs 1–2 are cheap because pending turns are already in context, and repair 3 runs rarely. Also:
- **Caps are unvalidated (a blocker for enabling them).** `invoke` passes caps only to Venice, so the Codex probes never exercised them. If reasoning tokens count toward `max_completion_tokens`, as in OpenAI semantics, a 1.8k admission at high effort can truncate. It then fails twice and costs more than it saves. Run a few synthetic paid calls and log `finish_reason`.
- **Call counting.** `canonical_opening` is appended to `calls`, so native sessions lose a whole plan/admission pair under the 12-call limit. Count only model calls, and reserve one pair for review corrections.
- **Bulk headroom.** A record about 18% larger than the one measured (93.3k serialized) hard-fails. That is likely for long voice answers. Queue such records for the operator instead.
- **Mixed pending.** A typed turn queued behind a 96-turn import forces 12-turn routine batches that each see only their slice. These hit the 12-call limit before the import finishes.
- **Full-guide fallback.** When `wanted` is empty, `guide_cards` returns the full guide for pending turns without a canonical route, such as corrections. Measure that case against the 35k cap.
- **Provider guard.** Assert Venice in production. The else-branch accepts any provider and silently drops the caps.
- **Benchmark mismatch.** The artifact (134,325/26,226) disagrees with the summary (130,217/25,908). Regenerate it from the deployed revision.

**Voice-bundle suitability**
It is suitable as a reversible development arm, and its claim-integrity rules cover PR #42 faithfully. The retrospective opt-in (C) is sound in code: it is a strict `is True` check, applied in both modes and never serialized to the model. Conditions, all on the importer or analysis side with no instruction growth:
- `compact_existing_evidence` filters out only superseded items. Any GPT-authored evidence stored in `state["evidence"]` would reach the planner as "accepted evidence" in place of unsent source. Import it as unverified and exclude it from context and coverage.
- Route IDs are never spoken, so the transcript carries no provenance for them. IDs at export time are rebuilt from question wording, which is reliable only for verbatim questions. Make the server-side exact-wording match the authority for IDs.
- The "exact transcript" is regenerated by the model. Label its fidelity and spot-check it with the participant's consent.
- "Every question and answer in order" includes the setup Q&A. Tag those turns as metadata and exclude them from evidence. Otherwise "I'd rather not revisit childhood" becomes evidence of avoidance. A mid-session withdrawal must also clear the flag.
- Evidence yield is confounded: the import arm is coded under the sparse bulk policy and the native arm turn by turn. Code both arms with the same pass. Report a comparison of whole pipelines (interviewer, admission and modality), not voice versus text. Analyze clarifications by per-turn `turn_source`.

## One reconciliation review

Models: ['claude-opus-5-5']
Error: False

**VERDICT: FINDS_ERROR.** The three blocking findings are repaired at the source-assembly level, and a dark deploy is safe. The narrowed guide, the new bulk gate and the call counter still have defects that block enabling live inference.

**Prior blocking findings**

1. Reviewer source: **RESOLVED.** `make_review_context` builds from `state["turns"]`. It includes every pending turn, every cited, antecedent and control turn, and the correction closure. `test_reviewer_reattaches_all_pending_source_not_just_planner_quotes` genuinely discriminates.
2. Correction reattachment: **RESOLVED in code.** `correction_closure` works in both directions and both builders use it. The regression test doesn't prove it, though. With only two turns, `RECENT_TURN_COUNT=4` already pulls in `old`, so the test passes even with closure deleted. The review-correction test has the same flaw.
3. Final-review source: **source RESOLVED; correction path REMAINING** (A).

Practical items: resolved as described, except B–D.

- **A. The correction path is under-supplied.**
  - (i) The non-bulk guide covers only shortlist routes plus pending turns' routes. Correction turns carry `canonical_question_id=None` in the fixtures (the constructor isn't in the packet), so they add no route. Presented routes are never shortlisted. The corrected evidence's facets are therefore absent unless a shortlisted route shares them.
  - Amendments that reuse those facets are rejected as "outside the supplied guide". The planner either fails or strips the facets, which unlinks the corrected reading from its facet.
  - At final review, if 10 pre-review calls were used, a rejection can't be recovered. Attempt 1 is call 11, attempt 2 needs 13 > 12, and the session goes to `resource_limited`.
  - (ii) Apart from evidence matching the next question's targets, the reviewer sees only evidence the proposal chooses to amend. A plan that leaves the corrected reading standing therefore passes.
- **B. The bulk addressed-route gate.**
  - (i) The engine requires `admission.addressed_routes_supported` on every bulk import, even when `addressed_routes` is empty, and the field defaults to `False`. If the model omits the field, or reads "true only if every proposed addressed route is actually answered" literally, a valid import fails. The repair attempt can't fix it.
  - (ii) `make_review_context` supplies only the question route's card. The reviewer must judge route scope without the addressed routes' definitions, so it can only rubber-stamp or reject.
- **C. The call guard undercounts.**
  - If `provider.call` raises (timeout, schema failure), `invoke` records nothing. `failed_attempt` bookkeeping is no longer counted, and `claim()` allows re-advance from `error`. Billed failures therefore never consume the limit.
  - If `Venice.call` lets pydantic's `ValidationError` (a `ValueError`) escape on the admission call, it is also misread as a plan rejection.
- **D.** `export_record` coverage still counts quarantined and collection-metadata answers.

Not in the packet, so unverified: `_model_call_count`, addressed-route persistence in `finish()`, correction-turn construction and the Venice factory assertion.

**Blocker to deploying while live inference stays disabled:** none. A–C run only on the advance/provider path. Import and export read the new keys through `.get`/`setdefault`, so the change is additive. A–C do block enabling live inference.

**Blocker to sharing the voice GPT as a development arm:** none hard. Records survive verbatim in `record_as_received`, and upstream evidence stays unadmitted. Three gaps still need fixing before Railway admits voice imports:
- The instructions never name the per-turn keys.
- `import_record` silently accepts turns that lack `question_text`/`answer_text` and stores them as null.
- The bulk context sends only question/answer text and IDs. Per-turn `corrections`/`conditions` and a top-level final-review response never reach the model.

**Smallest repair**

- A (`inference_context.py`): take the existing evidence whose sources intersect `correction_closure(state, pending_ids)`, or all evidence in review mode. Merge `evidence_guide_for_facets()` for those facets into `candidate_evidence_guide`, and pass the same evidence items into `make_review_context`.
- B (engine): gate on `candidate.addressed_routes and not admission.addressed_routes_supported`. Add the addressed route IDs to the `full_route_cards()` call in `make_review_context`.
- C: in `invoke`, append a counted telemetry record whenever `provider.call` raises.
- D: set `answered = answered_route_ids(state)` in `export_record`.
- Voice: add one line naming `question_text`, `answer_text` and `canonical_question_id`, and export corrections and the final-review exchange as ordered turns. That is about 150 chars, so recheck the 8k budget. Optionally, reject imported turns that lack both keys.
- Tests:
  - Put at least 4 turns after the corrected original, and drop `correction_of` from the review-correction fixture.
  - Add a correction whose route isn't shortlisted, and assert that its facets reach the guide.
  - Add a bulk case with empty `addressed_routes` and the admission field omitted.
