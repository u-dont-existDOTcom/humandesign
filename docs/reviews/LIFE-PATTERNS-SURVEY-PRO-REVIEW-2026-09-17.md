# Life Patterns survey: product review and proposed improvement plan

Date: 17 September 2026, UTC.
Status: REVIEW COMPLETE; IMPLEMENTATION AWAITS OWNER APPROVAL.
Scope: the current owner-development survey/interview, not a release certification or fresh target-theory-blind semantic review.

## Decision in brief

Keep the conversational product, continuous interview, neutral measurement coverage, participant authority, and direct-report-versus-inference distinction. Do not replace them with a conventional personality questionnaire, a new research ontology, or another series of isolated UI overlays.

The recommended next work is a coordinated repair of workflow state, checkpoint integrity, question selection, and the participant-facing result. The highest-priority defects are reproducible browser behavior, not speculative polish. A healthy deployment and green unit tests currently coexist with invisible recovery controls, ineffective pause behavior, and overwrite of the previous exact checkpoint following a failed restore.

Approval should authorize the four implementation phases below as reversible development work. It should not authorize merge, public recruitment, new provider/model expenditure, chart-aware interviewing, production authentication changes, or a scientific-validity claim. Nothing in this review changes the running application.

## What was examined

The reviewed development tip was `fead8f59935e886c78fc31d15f243a32a9958b9c` on `codex/discover-life-patterns-mvp`. The existing Life Patterns development pull request remained draft/open/unmerged.

Railway's latest successful owner-service deployment was `3588d15c-4865-4c0d-ba37-331d5ac84483`, from application commit `56796a842ef3bc453f12f65c138458656e441490`. Comparing that application commit with the reviewed tip showed only state/task documents and a regression-test change; no runtime-source differences. Hosted CI run `35239835457` succeeded on regression commit `f861ac5d26f6e11aceb3c69804e416e15db612c9`. This was verified live, not inferred from the previous worker's receipt.

Read-only requests to the landing page and `/healthz` returned HTTP 200. The landing HTML was 54,245 bytes, SHA-256 `fd9641b6ef4b995bace2b75c272dd18285c11840eb074ea0396a3be679f719f0`.

The inspection covered the deployed entrypoint and continuous-flow, conversation, reasoning, natural-flow, persistence, import/recovery, liveness, dynamic-progress, and freeze/export consumer paths, together with affected tests. Two isolated headless-browser passes exercised the actual deployed HTML/JavaScript. All session mutations and other application API requests in those browser passes were intercepted and answered with synthetic fixtures. Only public page/blueprint reads reached the service. There were zero live model calls and no real participant-session writes.

Responsive geometry was checked at 320, 375, 414, 768, 1024, and 1440 CSS pixels. There was no horizontal overflow in the initial-state sweep. This does not establish correct keyboard behavior, overlay placement, screen-reader operation, contrast, or all-state responsiveness. Mobile and desktop inspection images were reviewed. Two owner-private historical recovery excerpts were also reviewed for conversation quality; they predate the latest deployment and are not evidence of its current error rate.

Companion evidence: `artifacts/life-patterns/survey-review-2026-09-17/evidence.json`. Private narrative, original recovery files, actual participant session identifiers, credentials, and account details are deliberately excluded from the public repository.

## 1. Repair the interview's executable state first

### R01 — Failed restore can replace the previous exact checkpoint

**Observed in the mocked browser.** A synthetic stored checkpoint was offered to the restore endpoint; the endpoint returned 503. Startup silently created a fresh session. The next automatic save replaced the prior exact-recovery value with the new empty session. The previous answer no longer existed in that exact-recovery value.

This demonstrates checkpoint overwrite, not that every possible legacy backup is necessarily lost. The defect is the fallback policy: a failure to restore is treated as permission to start and save over a new interview.

**Proposed behavior:** keep the original checkpoint untouched, show a visible restore failure, offer retry and download of the preserved checkpoint, and make starting a separate interview an explicit action. A new interview gets a separate recovery identity. Never silently demote a restore failure into a new saved session.

### R02 — An old adjudication is mistaken for the current workflow phase

**Source-confirmed, with the receiving UI reproduced.** `PersistentRecoverabilityCoverageSession._workflow_phase` returns `post_adjudication` whenever any participant adjudication exists and no draft is active. It does not determine whether the interview has already advanced and is waiting for an answer to a later question. The continuous-session change makes this distinction essential.

When the deployed UI was given `post_adjudication`, it displayed the old result, hid the composer, hid normal Continue, and did not automatically request the next question. Thus the historical acceptance can still restore into a dead end. Calling a derived string a workflow phase is not the same as storing the current executable phase.

**Proposed behavior:** persist the actual phase and pending action with a session revision. An old accepted pattern must not override a newer awaiting-answer state. After a completed adjudication, resume automatic continuation only when that is genuinely the pending action. An interview that was explicitly paused remains paused after refresh.

### R03 — Next-question failure can hide both its error and retry

**Observed in the mocked browser.** After topic completion, the UI hides the continuation container. When automatic next-question generation fails, it unhides a message and Retry button inside that still-hidden parent. The composer, error, and retry are all invisible. Finish remains visible.

**Proposed behavior:** error and retry belong to the current action region, not a container that was just retired. Retrying next-question generation must not resend or re-adjudicate the preceding answer. Preserve a readable transcript and saved-state status throughout the failure.

### R04 — Finish for now is not a durable pause

**Observed in three mocked cases.** An idle pause left the composer visible and Send enabled. Calling Send submitted another answer. Pausing while next-question generation was in flight did not prevent the arriving question from appearing or the status from returning to the normal interview state. The pause explanatory message was hidden inside an invisible parent.

**Proposed behavior:** Finish for now takes effect immediately and presents a clear paused view with Resume, saved patterns, and export. It stops further question selection. An already-committed response may be retained safely, but must not silently reactivate the interface. Resume does not require refresh. Do not equate aborting a browser fetch with undoing a server commit.

### R05 — Failed answers lose their editable draft and contaminate answer memory

**Observed in the mocked browser.** A failed turn left the textarea empty while participant-answer memory already contained the failed submission. The visible transcript retained the text, but there was no preserved editable draft. A later question selector can consequently receive text as though it were established server knowledge when processing actually failed.

**Proposed behavior:** distinguish draft, queued submission, server-accepted turn, and failed submission. Keep the draft or a retryable outbox until acknowledgement. Preserve client memory for pending text, but label its processing status rather than presenting it as accepted evidence. A retry must use the same operation identity.

### R06 — Concurrent turns are still possible

**Observed in the mocked browser.** Two Send invocations generated two turn requests before either completed. Disabling a button alone does not guard keyboard shortcuts or other calls to the handler.

**Proposed behavior:** one mutating operation per session revision, with a guard in the handler and server-side idempotency/revision checks. Bind each response to its initiating operation rather than a global last-API-payload variable. Never let a late response update a newer session, a paused interface, or a different question. This is targeted reliability work, not a reason to import an unrelated distributed-systems framework.

### Minimal implementation direction

Use one small, explicit state model for initialization/restoration, awaiting answer, processing answer, reviewing inference, advancing, paused, recoverable error, and finished. Keep data facts, adjudication status, processing status, and current UI phase separate. Render visible controls from this state in one place. Migrate the current string-replacement/global-wrapper chain incrementally instead of adding another overlay or rewriting the entire backend.

Checkpoint a consistent server revision plus client draft/pending-operation state. Serialize checkpoint writes and retain a last-known-good backup; do not combine an old server response with unrelated newer client state. Surface truthful saving/saved/save-failed status. A save request returning no usable snapshot must not produce an assurance that everything is saved.

## 2. Make question selection selective, contextual, and consistent

### Q01 — The cross-area admission gate cannot stop

**Source-confirmed.** The in-thread gate can admit, replace, or stop. The cross-area gate requires an opening question and a selected open dimension, with instructions to output exactly one admitted question. It cannot return no worthwhile question while measurement coverage remains open.

That contract works against the intended quality rule. An open measurement category is an unanswered area, not proof that another useful question can be formulated right now.

**Proposed behavior:** all question-bearing routes can ask, clarify, move to another useful gap, defer an area, or stop with incomplete coverage explicitly preserved. No-useful-question is a legitimate local outcome. It is not permission to claim coverage complete.

### Q02 — Saving more history is not enough if different routes see different history

**Source-confirmed.** The main natural-flow planner uses a recent-conversation slice of 80 turns. The in-thread admission check uses 120 turns and operative facts. Cross-area admission additionally receives browser answer memory, but with its own limits. Initial cross-area candidate generation does not receive that same answer-memory input. Refinement/Keep investigating and backend fallback paths are not all covered by the same final question-admission method.

**Proposed behavior:** build one relevant-evidence view for every question-bearing route, including earlier direct answers, corrections, rejected interpretations, uncertain statements, and already-resolved topics. Preserve exact source pointers. Full history may remain stored, but retrieval for a question must find older relevant material rather than merely increasing the latest-N cutoff.

Place the final question check at the actual emission boundary, after any fallback or replacement. Do not apply it to status messages or acknowledgements. A separate call to the same model is useful instrumentation, not independent proof that a question is good.

### A useful-question contract

A proposed question should identify a real unresolved distinction, explain how materially different answers would change the current person-specific understanding or needed measurement, and show why that distinction is not already answered. It must be understandable without requiring the participant to invent arbitrary quantities or choose between overlapping abstractions.

Do not reject a question merely because its eventual answer might be 'it depends'. Conditionality can be the important information. The useful distinction is whether we already know what it depends on, in which settings, and whether resolving the remaining uncertainty is worth the participant's effort.

Likewise, do not require novelty or unusualness for every answer. Familiar self-knowledge can be important. Conversely, verbatim authorship alone does not make an underspecified statement a useful person-level pattern. A generic formulation can remain contextual or measurement evidence without being advertised as a distinctive discovery. Do not claim population rarity without population evidence.

Synthetic examples, not quotations from participant records:

- 'Do you change an approach when it needs changing?' invites a near-tautological answer. Preserve any useful context, but do not promote the wording automatically into a distinctive pattern.
- 'What made you stop using the last approach you replaced?' may identify a meaningful threshold when that threshold is missing and decision-relevant. Do not ask it when the existing interview already answers it.
- 'The time I need depends on task complexity' does not entail 'the benefit increases with complexity'. A new relationship must be identified as an inference, not smuggled in through polished wording.

Before a longer owner retest, evaluate a small set of cases for semantic repeats, generic praise/tautology, useful conditional answers, old corrected answers, missingness, and no-worthwhile-next-question. Do not turn this into a multi-model judging campaign.

## 3. Preserve participant authority without turning every utterance into a pattern

The owner's current distinctions remain controlling:

1. Generic/contextual information may contribute to measurement but does not automatically become an interesting person-specific pattern.
2. A person-specific pattern the participant has already directly stated should be recorded from that statement, without asking them to agree with themselves.
3. A new relationship, scope claim, causal explanation, comparison, or other interviewer inference needs participant judgment.

The strict direct-report implementation is a valuable protection: it requires an exact contiguous source substring and same-turn provenance. Keep that protection. However, a substring match alone does not establish endorsement or scope. The substring might appear inside a quotation, a negated statement, a discarded former belief, or before a crucial qualification. The recorded assertion must retain speaker, polarity, uncertainty, time, conditions, and relevant surrounding context. Ambiguous semantic transformations must not become silently accepted participant claims.

The historical private excerpts contain both near-restatements presented as discoveries and an added relationship not licensed by the participant's response. They demonstrate the need for semantic restraint, but do not establish the current model's failure frequency after the latest repair.

For a genuine inference, show a short formulation and make the actual inferential addition apparent. Avoid repeating a long recitation of all source facts. Preserve the single correction textbox. Keep clear choices to accept, reject that interpretation, leave it uncertain, or ask for further investigation; do not reintroduce multiple editors for different backend intent classes. Keep investigating means another useful inquiry, not a quota of counterexamples.

Do not demand a synthesis at each section boundary. Do not shrink a broad, well-supported pattern into a collection of trivial local rules merely to make recording easier. Equally, an all-in-one paragraph that combines unrelated claims is difficult to correct: make separable claims navigable while preserving their meaningful relationships and original breadth. Editing or correction appends a traceable revision; it must not silently rewrite past participant authority.

## 4. Give the participant one coherent working surface

The present initial screen is dominated by development instructions, evaluation language, and recovery machinery. The initial answer box even asks about correcting an inference before any inference exists. In the browser sweep, the textarea had no explicit aria-label; the initial markup also lacked a corresponding label. These are concrete defects, not a request for cosmetic reinvention.

Recommended surface:

- A compact header with the product name, persistent Finish for now, and a quiet saved-state indicator.
- The conversation, with the current question or inference immediately adjacent to the one response field.
- A compact progress/status row near the current interaction. Expand coverage details only on request. Do not put a large diagnostic/download panel after the answer box and then scroll toward it on every operation.
- An accessible Your patterns view and a separately collapsed recovery/development section.

Use a normal-answer label during interviewing and a correction/response label during inference review. A placeholder is not the only instruction. Eliminate repeated explanatory paragraphs and obsolete hidden-control wiring during consolidation. Keep the underlying scientific distinctions, but explain them when they affect a participant action instead of exposing internal terminology throughout the conversation.

Make one function own scroll behavior. Auto-follow a new turn only while the person is already near the current interaction; preserve position when they are reading earlier material and offer a jump-to-latest affordance. Status/progress changes should not move the viewport. Focus should not cause a competing scroll. Respect reduced-motion preferences: the tested page retained smooth scrolling when reduced motion was requested.

The width sweep found no initial horizontal overflow, but fixed controls and sticky input still need real viewport, mobile keyboard, focus, and zoom checks in the implementation pass. Give fixed controls reserved space and do not obscure the current question or focused element. Add appropriate live announcements for completed actions/errors without continuously rereading the transcript. Test labels, focus order, contrast, keyboard operation, non-color state cues, and reduced motion.

Keep approximate coverage progress, not a fabricated question count or psychological accuracy score. Distinguish sufficiently evidenced areas from explicitly unknown, declined, or inapplicable areas, even when all are handled for workflow completion. The current remaining-time calculation uses fixed heuristic conversions; remove or clearly withhold an ETA until actual interaction timings justify one. A paused or exhausted interview can be useful while remaining scientifically incomplete.

## 5. Make the accumulated result worth returning to

Accepted and directly recorded patterns should form a stable, readable working collection rather than disappear as automatic continuation begins. Recording a direct report without interrupting the interview must not mean recording it invisibly.

A modest Your patterns panel is sufficient; a decorative graph is unnecessary. Each item should show its wording, relevant context, and whether it was directly stated, an accepted inference, disputed, or unresolved. Its source and revision history can be expanded on demand. Related material may be grouped without inventing a new relationship between it. Avoid a numerical confidence score unless its meaning and calibration are established.

The participant must be able to inspect a saved item, add a correction, or return to the interview without losing their place. This is not a return to routine fact-by-fact approval. A short nonblocking 'Saved to your patterns' acknowledgement is enough for an unambiguous direct report.

Finish for now should show the current collection, what remains open, the actual save status, and Resume. Distinguish a readable summary, a recovery backup, and a research freeze. Those are different artifacts with different promises.

### R07 — Freeze/export needs a clearer and more reproducible contract

**Source-confirmed and one edge case browser-reproduced.** The current measurement download contains completed results and aggregate coverage, but not the full evidence ledger/source conversation. In a synthetic zero-pattern session, both blueprint version and blueprint hash exported as null despite a loaded blueprint. A hash of an absent underlying artifact does not make that artifact recoverable.

Retain the distinction between an unvalidated working checkpoint and a scientific freeze. Before actual research use, define the self-contained evidence package or explicit companion dependency that downstream analysis needs. Include applicable schema/blueprint/build identities even when no patterns were accepted, and keep source timing, provenance, qualification, corrections, and unresolved status reproducible. Do not silently declare old reconstructed interviews clean scientific data. These requirements concern evidence completeness, not another approval prompt for every participant fact.

## 6. Reduce waiting and measure the right failures

Source inspection shows serial model stages for extraction, planning, admission, and sometimes coverage assessment. Their actual latency distribution was not measured: this review made no live inference calls. Do not claim that changing the model, provider, or framework will solve the observed interface failures.

First remove avoidable waiting from the participant's critical path. An acknowledged judgment should not wait for an unrelated coverage refresh. Show concrete, honest operation status and a bounded retry path. Keep last-good coverage when an auxiliary estimate fails, but identify it as such in diagnostics. Do not introduce speculative parallel writes to the same session.

Record operation type, session revision, duration, outcome, checkpoint success, and admitted-question reason in privacy-safe diagnostics. A minimal build/version marker helps reconcile the browser with the deployed source. Raw participant text should not become the default application log. Improvements should be judged by preserved answers, successful resume, unnecessary/repeated-question rate, owner-rated usefulness, and correction burden—not merely more accepted patterns, more coverage, or more passing tests.

## 7. Proposed implementation sequence and acceptance checks

### Phase A — Reliable continuity and recovery

Repair R01–R06 together through a shared phase/operation/checkpoint model. Preserve current conversational and evidence semantics. Add executable browser tests for the reproduced paths before asking the owner to repeat a long interview.

Acceptance: a failed restore preserves the original exact checkpoint; later interview questions restore after earlier acceptances; next-question failure has a visible retry; pause survives refresh and late responses; failed submissions retain editable text and correct processing status; duplicate/late operations do not double-apply evidence. Include tests after both direct recording and explicit inference adjudication, not only a pristine first session.

### Phase B — Better questioning and faithful pattern recording

Unify relevant memory and final admission across normal, cross-area, refinement, recovery, and fallback questions. Admit no-worthwhile-next-question without falsely completing coverage. Preserve direct reports, contextual evidence, and inferred relationships as different things. Add source-context checks around direct excerpts and respect corrections/uncertainty.

Acceptance: a bounded case set demonstrates no semantic repeat of a relevant old answer, no forced filler when a category remains open, no automatic acceptance of negated/quoted/qualified substrings, and no unsupported causal or directional relation inserted as fact. A useful conditional answer is not rejected just for being conditional. Owner-private examples remain private; public fixtures are synthetic.

### Phase C — Clear interaction and usable results

Implement the compact current-action surface, correct labels, non-jumping progress, persistent patterns view, genuine finish/resume panel, and clearly separated export types. Consolidate obsolete DOM controls instead of continuing to hide them through successive wrappers. Address R07's metadata edge case and freeze/companion semantics before research use.

Acceptance: ordinary answer and inference review are visually unambiguous; a saved pattern remains findable during automatic continuation; correction does not create redundant confirmation; all six widths and mobile keyboard/focus states are exercised; error/save status is visible and accessible; export distinguishes summary, backup, and research evidence.

### Phase D — Short owner evaluation and bounded closeout

Use the repaired flow for a short owner evaluation focused on whether the next question actually adds useful information and whether the resulting collection represents what was said. Inspect admission reasons only for failures. Fix the identified shared cause rather than adding another local exception. Run focused/affected tests during iteration and the repository's applicable checks at the actual delivery boundary. Reconcile the deployed source before claiming a repair is live.

Do not require a new scientific-validity campaign, mutation suite, model tournament, or merge-ready omnibus PR merely to try a reversible candidate. Keep each implementation increment understandable with explicit acceptance evidence. No merge or public release follows automatically from approving this development plan.

## Scope deliberately deferred

The current passwordless owner-development route was an explicit prior owner decision, not an accidental finding to reverse during this review. Before external participant access, separately agree on authentication/access control, retention/deletion behavior, consent and model-provider disclosure, quotas/rate limits, session isolation, and abuse protection. No penetration test of real participant sessions was performed.

No new chart-aware questions, recruitment, external participant coding, provider/model changes, infrastructure migration, account system, diagnosis, scoring claims, or graphical personality dashboard are recommended as prerequisites for these repairs. No raw recovery data should be added to this public repository.

## Evidence interpretation and limits

The browser cases establish observable client behavior under controlled responses; they do not prove that the production server returned those failures during the owner's exact historical session. The server phase finding is source-level reasoning combined with reproduction of the receiving UI. Historical transcript examples are development evidence, not held-out validation. The precise frequency of poor questions in the newest model flow is unmeasured. Screen-reader behavior, native mobile keyboards, complete contrast/zoom conformance, multi-tab races, actual provider latency, and every research-data invariant were not certified.

These limits do not weaken the immediate repair recommendation: deterministic client failures and an impossible stop contract can be fixed without speculative model evaluation or further participant effort.

## Source map

All source references below use the reviewed tip named above.

- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow.py`: admission schemas, context payloads, `plan_continuation_question`, `_advance_existing_session`.
- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow_ui.py`: pause, automatic advance, error-container visibility, answer memory, global wrappers.
- `src/hdmatch/api/life_patterns_v2_owner_persistent.py`, especially lines 206–244: phase derivation and recovery status.
- `src/hdmatch/api/life_patterns_v2_owner_persistent_ui.py`: exact checkpoint synchronization, startup fallback, mutation/interval saving.
- `src/hdmatch/api/life_patterns_v2_owner_import_resume_ui.py`: `renderRecoveredWorkflow` and transcript-only safeguards.
- `src/hdmatch/api/life_patterns_v2_owner_natural_flow.py`: direct-source recognition and recording; main planner context slice.
- `src/hdmatch/api/life_patterns_v2_owner_natural_flow_ui.py`, `life_patterns_v2_owner_liveness_ui.py`: final control/operation wrappers and scroll behavior.
- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`, `life_patterns_v2_owner_resilient.py`: refinement/fallback and auxiliary coverage paths.
- `src/hdmatch/api/life_patterns_v2_owner_dynamic_ui.py`: progress heuristics and inherited controls.
- `src/hdmatch/api/life_patterns_v2_owner_recoverability_ui.py`: measurement bundle creation.
- `tests/unit/test_life_patterns_v2_owner_continuous_flow.py`: backend fake-model tests and HTML-string assertions. These useful checks do not exercise the browser failures reproduced here.

Established guidance was consulted rather than designing a new UX standard: GOV.UK Design System, Question pages; W3C WCAG 2.2 Understanding 3.3.2, Labels or Instructions; and Understanding 4.1.3, Status Messages. Their principles support only-needed questions, comprehensible inputs, and perceivable asynchronous outcomes, not a claim of full conformance. Exact primary pages were read on 17 September 2026:

- https://design-system.service.gov.uk/patterns/question-pages/
- https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

Universal authority and the current design specialist were loaded for this review. Applicable outcome/destination checks: plan only; no app mutation; no paid inference; protect public-repository privacy; distinguish observations from hypotheses; deliver usable artifacts; stop at owner approval. This review adds no new scientific acceptance criterion and does not supersede the accepted v2 evidence contract.
