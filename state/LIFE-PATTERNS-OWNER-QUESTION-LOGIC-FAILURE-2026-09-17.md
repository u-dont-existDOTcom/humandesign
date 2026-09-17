# Life Patterns: failed owner question-quality evaluation — 2026-09-17

**Status: FAIL; diagnosis completed, application not repaired in this pass.**

## Evidence and limits

The owner supplied a private browser recovery checkpoint and reported worse question quality. Read-only checks verified its checksum, final phase, candidate/source equality, reused evidence and admission records. The raw narrative, participant identifiers and source-derived hashes are not committed.

Current GitHub source was inspected at `b15240527b6fc46bc52367118b455bf9d4626aa3`, containing application commit `aace9ac3a40f1a8dfd6244ab714a86563d0132c8`. The upload itself contains no application-commit identifier, so its exact producing head is not independently bound by that file.

## Confirmed failures

- **Invalid contrasts:** an instrumental method and its practical purpose were treated as competing motives without an established distinguishing condition. A later question confused willingness to act with the opportunity to act and treated action and distress as alternatives even though both can occur.
- **Failure to repair:** five turns after the concrete example questioned the interview's meaning or logic. The responses defended the disputed distinction, switched or merged constructs, and transferred a condition from one class of problems to its contrasting class rather than answering the objection.
- **Duplicate synthesis:** the last draft is exactly the earlier participant message, using exactly the evidence set already used for an accepted formulation. The recorded inference note describes additions absent from that actual candidate.
- **Misleading closure:** the reply says the area supplies enough information to move on, but the saved state remains `synthesis_review`. It is not a recorded whole-interview completion. Coverage is one sufficient, two partial and twenty unassessed areas.
- **Process feedback in the event ledger:** four facts derive from interview-feedback turns. At least three concern the question's logic or construct framing rather than the original event. No use in downstream target scoring is established.
- **Legacy coverage inconsistency:** nine older summaries survive, but nine historically sufficient domains are now unassessed; explicit legacy answer memory is empty. Preserve old planning knowledge separately from evidence that cannot be recovered. Do not silently certify missing raw source data or treat an unassessed default as proof nothing was learned.

The admission gate ran: six decisions, comprising four replacements and two admissions. Its decisions generated or approved the defective questions. This was not simply a missing gate.

## Code-supported explanation

`life_patterns_v2_owner_workflow.py` routes ordinary textbox submissions through the same answer/extraction/planning path, with no explicit question-repair branch. `_advance` returns a measurement-domain identifier without retaining it as active-focus state. Having the whole conversation available does not ensure coherent focus or repair behavior.

`_create_pattern` lets a formulation review disable the direct-report path. It has no explicit duplicate/new-information check. The final candidate meets the base verbatim/source checks in `life_patterns_v2_owner_natural_flow.py`, yet it became an inference to judge. The audit note does not match its wording; the complete raw reviewer response is not retained, so the exact internal model cause remains unknown.

`_admit_final_question` checks question moves, not closure prose attached to a synthesis move. `_merge_progress` overwrites aggregate rows with normalized current rows, including unassessed defaults.

The extractor and shared-context instructions in `life_patterns_v2_owner_conversation.py` and `life_patterns_v2_owner_continuous_flow.py` do not mechanically separate process feedback from event evidence. A model-written rationale that a distinction is useful is not proof that the premises and answer alternatives are valid.

## Disposition and next bounded experiment

The parent owner outcome remains OPEN. The current question-repair/formulation approach failed direct use. Preserve recovery, single-flight operations, participant authority and the accepted scientific substrate. Earlier green browser tests verify those tested transitions, not conversational intelligence.

The next candidate should prioritize repairing the participant's actual objection. Clarification is neither a substantive behavioral answer nor consent to stop. Explain or withdraw an invalid premise, preserve the current topic, and require a real informational change before resurfacing an accepted pattern. Mixed messages containing real new information must still enter the evidence path.

Do not respond with another UI-only patch, another generic gate reminder, a keyword blacklist, a forced counterexample quota or an additional model judge. Keep the owner-requested pre-send check and the configured provider/model. The precise implementation is a small reversible experiment, not a new mandatory architecture or release-grade campaign. Use this failure privately or a synthetic analogue for focused comparison before requesting another unchanged owner retest.

No production code, deployment, provider/model, live participant session or scientific scoring changed. No live model call or running application replay occurred. The sandbox could not resolve GitHub for an execution checkout; connected GitHub source reads succeeded.

Machine-readable receipt: `artifacts/life-patterns/survey-implementation-2026-09-17/owner-question-logic-audit.json`.

## Authority and closeout

Live Universal root, Iteration-lane, strategy-efficacy, governance and requirement-accretion guidance were activated in this turn. This pass is evidence acquisition and strategy learning, not direct product improvement. Private narrative remains private; no unrelated Mission Control record is created.

**There was never a completion policy.** Existing privacy, spending, model-change, recruitment, publication and merge restrictions remain unchanged.
