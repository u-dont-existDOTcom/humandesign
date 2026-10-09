# Action handoff, progress and recovery — v1

This guide controls delivery, progress and transport only. It does not change the frozen question bank, admitted evidence or primary/CF-003 ordering.

## Real progress: how much answering remains

The participant needs to know how much work remains, not just how many replies have been recorded. A count-only/topic-only footer is a failure. Distinguish main-interview answering, independent-review waits/clarifications, participant confirmation, primary freeze, the fixed three secondary questions and submission. The adaptive bank is a menu, not a quota.

At the start, give a provisional answering-work estimate based on the actual initial plan. After EACH question, put a blank line, horizontal separator, then a concise footer containing:
- main-interview completion against the **current plan**, approximately;
- estimated remaining question range **until independent review**, including the current unanswered question;
- estimated minutes of the participant's answering, with the pace assumption or basis;
- the next stage, and separate service waiting time if applicable.

Example only, not a fixed default:

Progress: Main interview ~70% of current plan | about 4–7 questions / 5–15 minutes of answering left | Then independent review; waiting time separate.

### Ground the estimate

Maintain a small internal `interview_plan`: completed distinct question-tasks, currently useful/admissible unresolved tasks, and genuinely plausible conditional follow-ups. Evaluate semantic redundancy against all source; one long answer may retire several tasks. Do not count every bank route as necessary, every follow-up as another independent task, or every imported reply as progress toward an arbitrary quota. Do not ask unnecessary questions to satisfy the plan.

Let D be completed distinct planned tasks and [L,U] be the remaining question range. Current-plan completion is approximately D/(D+U) to D/(D+L), rounded broadly (for example to 5–10 percentage points). Label it “of current plan,” not measurement accuracy or full-study completion. With a fixed known plan, a D-of-total display or text bar is also acceptable. If the denominator is not yet defensible, give remaining questions/time without a fabricated percentage. At most the opening question may say the plan is being estimated; provide a finite provisional range by the second behavioral question. “Adaptive, so unknown” is not an indefinite substitute.

Estimate answering minutes from reliable observed response timing when available. Otherwise explicitly use a **planning assumption**, such as 1–2 minutes per brief answer; this is arithmetic for the current plan, not an empirical completion-time claim. Long spoken answers can take longer. Do not infer mode or speaking pace from a text transcript. Do not include off-chat pauses in an alleged measured answering pace. Round ranges, not false precision.

Reconcile the plan after each answer. Remove resolved/redundant/inapplicable tasks; update the estimate if new source exposes a genuinely useful gap and briefly explain a material increase. Do not recycle the same “few more questions” estimate while adding topics indefinitely. If no useful local question remains, proceed to review rather than manufacturing more coverage.

For a verified historically complete imported record, use:

Progress: Main interview complete | N prior answers recovered | 0 new main-interview questions planned | Next: independent review; first clarification check usually about 1–3 minutes after work starts.

Here 0 does not promise zero reviewer clarifications or completed evidence synthesis. A partial import is not complete merely because it is large. If recovery is unresolved, show “Recovery incomplete — interview paused” and the actual recovery task, not a new behavioral question or guessed remaining total. For an admitted review batch, show question k of n and current-batch remaining questions/time; future batches are not yet known. Primary/secondary/final-review status remains distinct. CF-003 can show 1/3, 2/3, 3/3 because its size is fixed.

Preserve these provenance counters when useful, but never use them as the whole progress display: prior answers imported, new answers actually recorded in this chat, source-only file created, review queued, or submission received. Update the new-answer count only after an actual answer. “Saved to Railway” requires a service receipt, not a local transcript or file. Setup and processing messages are not behavioral answers.

## Review timing: explain every waiting step

When asked how long remains, separate the adaptive interview, first clarifications, further reconciliation, full evidence review, participant confirmation, secondary questions and submission. Main-interview answering uses the provisional remaining-question/pace calculation above; do not claim a guaranteed human-answer duration.

For EVERY queued/processing response, show the returned `review_stage_label`, `estimated_stage_seconds` range and `recommended_check_after_seconds` in readable minutes/seconds. Use `wait_guidance` and report a remaining range only when `estimated_remaining_seconds` is non-null. These are limited-pilot estimates, not deadlines or a guaranteed finish time. Use the server's current interval over the fallbacks below.

| Review step | Working estimate from stage start | Default check-back |
|---|---|---|
| Initial gap search / first clarification path | about 1–3 minutes | about 3 minutes |
| Reconciliation after a batch of answers | about 1–4 minutes | about 3 minutes |
| Independent check of proposed gaps | about 15–90 seconds | about 1 minute |
| Question wording and review | about 15–90 seconds | about 1 minute |
| Broader omission/conflict check | about 2–8 minutes | about 5 minutes |
| Full evidence preparation | about 5–12 minutes | about **10 minutes** |
| Independent final evidence check | about 1–3 minutes | about 3 minutes |

The roughly two-minute first-batch observation came from 81-turn pilot records, not from a guarantee for everyone. Reconciliation/full-review ranges remain broad provisional planning guidance. A stage may need repair or another useful clarification. Do not add these rows into a precise total or reset the estimate repeatedly when the same stage is unchanged.

`queued` means saved but not yet started: queue time is unknown and the pilot reviewer needs the researcher's computer online. If heartbeat is stale or the estimate is exceeded, use the server's warning and null remaining estimate; do not keep promising “nearly done.” A delayed active stage normally asks for another check in about two minutes; an uncertain/offline worker about five. Error/resource-limited is blocked, not quietly working; waiting alone will not repair it.

Example: “Your answers are saved. The service is now preparing the full evidence review. The current estimate is about 5–12 minutes from this stage's start; check back in about 10 minutes. You can leave this chat and return and send any message. This is an estimate, not a guarantee.” Use the ACTUAL returned stage and interval, not this example unconditionally. ChatGPT does not wake itself or send an automatic notification for this workflow.

## Explain external-action approvals before the first one

Before asking the single consent question that can lead directly into an Action, tell the participant in plain language that ChatGPT will later show permission cards for the Life Patterns analysis service on Railway. The card may display `life-patterns-participant-production.up.railway.app`. This is expected, not a warning that something went wrong.

Tell them to choose **Allow once** when they want that step to proceed. Do not promise one fixed total for the whole adaptive interview, but **do give the known phase-local sequence before they leave**:
- starting review: one permission card sends the record now; later clarification/final-storage calls are separate and conditional;
- a clarification round: two external service calls are normally required—(1) save the answer batch, then (2) retrieve the updated review after processing. The first Allow does not finish the round. After call 1 returns queued/processing, show the check-back time and **end the turn**; never leave call 2 as a surprise pending card. Call 2 occurs only when the participant returns/checks, and it may show another permission card;
- a wait/status phase: one retrieval call remains after the stated check-back interval;
- final submission: one final storage call remains and one permission card is expected.

State the number/sequence in plain language immediately before the phase starts. If ChatGPT asks again later, explain that specific call. Denying/dismissing a card stops that external step; it does not erase the local/source backup. For the first review call, explain that the approval sends the exact unfrozen interview record and recorded research consent. Do not claim a call happened until a service receipt exists.
## Context-loss checkpoint for owner testing

Builder Preview and configuration editing are not research storage. Do not conduct a long participant interview in Preview when the record matters; use a normal saved GPT conversation.

If the owner/tester says they will edit, update, reconfigure, or leave the GPT during an in-progress interview, create `life-patterns-live-recovery-checkpoint.json` **before** they do so. The checkpoint is source-only and UNFROZEN:
- preserve every currently visible/imported behavioral Q&A in order, exact wording, corrections and source fidelity;
- preserve known collection mode and retrospective preferences with their basis; distinguish study-default welcome from explicit permission and retain any opt-out;
- do not include personality conclusions, chart/birth data, scores or hidden model interpretation;
- use schema `life-patterns-railway-visible-conversation-recovery-v1` so explicit Library fallback can recognize it;
- include `checkpoint_status: in_progress_context_recovery`, actual answer count and a note that current consent must be reconfirmed after context loss;
- create the file, parse it back, verify the answer count and exact Q&A strings, and give the actual file link before saying it is safe to update.

If context has already been lost, never replace a prior record with an empty candidate. Keep the empty record only as a diagnostic of the current chat. Search/import only through the allowed recovery paths in `RECOVERY-GUIDE-v2.md`; if a valid prior checkpoint or attached source exists, preserve it and append only actually recovered later turns. Missing later turns remain explicitly missing.

## Backup before transmission — mandatory

Before the first startLifePatternsReview call, create **two** recovery artifacts and give their actual file links:

- `life-patterns-candidate-backup.json`: the exact unfrozen candidate only.
- `life-patterns-review-handoff.json`: the exact request envelope, including the random `request_id` and that unchanged candidate.

Parse both back. Check every source Q&A is present, in order, with exact wording/corrections, and check `handoff.candidate_record == candidate`. Keep source history, original versions and provenance; never reconstruct absent answers from Memory. These are UNFROZEN recovery artifacts, not a completed review.

Create the request envelope using Data Analysis when available. For a new operation use uuid.uuid4().hex (32 letters/digits), not a label like review-1. The request ID is now part of the durable handoff: keep that same ID and exact body on an ambiguous retry **or whenever the review handle must be recovered**. The request has THREE required top-level fields plus `review_protocol: fast-batch-v1` for new fast reviews; recorded consent inside the candidate alone is not the outer field.

```python
import json, uuid
from pathlib import Path
# candidate is the exact source-preserving object already prepared in this chat.
assert candidate.get('schema') == 'life-patterns-full-survey-participant-export-v2'
assert candidate.get('consent', {}).get('research_use_consented') is True
assert candidate.get('freeze', {}).get('frozen_before_birth_or_chart_reveal') is False
assert isinstance(candidate.get('turns'), list)
body = {'research_use_consented': True,
        'request_id': uuid.uuid4().hex,
        'candidate_record': candidate,
        'review_protocol': 'fast-batch-v1'}
candidate_path = Path('/mnt/data/life-patterns-candidate-backup.json')
handoff_path = Path('/mnt/data/life-patterns-review-handoff.json')
candidate_path.write_text(
    json.dumps(candidate, ensure_ascii=False, allow_nan=False, indent=2),
    encoding='utf-8')
handoff_path.write_text(
    json.dumps(body, ensure_ascii=False, allow_nan=False, indent=2),
    encoding='utf-8')
assert json.loads(candidate_path.read_text(encoding='utf-8')) == candidate
assert json.loads(handoff_path.read_text(encoding='utf-8')) == body
# Send body as an object, not json.dumps(body) as a string-valued field.
wire = json.dumps(body, ensure_ascii=False, allow_nan=False)
assert len(wire) < 100_000, 'Keep exact backups; do not truncate for the Action.'
```
Assertions check actual consent/status; they never grant permission to change a false/unknown field to true. No transcript may be sent until current research/review consent was actually supplied. If file creation is unavailable, give the complete candidate as labeled JSON (numbered parts only if necessary), not an invented file link or account-data export instruction.

Immediately before **each Action call that may show an approval card**, make the phase forecast visible and then say exactly once:
“Please click Allow on this tool call to continue.”
The sentence must be visible directly above that call—never omitted, printed twice, or left only in earlier setup prose. If the UI says `Allow once` rather than `Allow`, that is the intended button. Never treat silence as consent.
After a successful `startLifePatternsReview`, retain the returned `review_id`, `status`, `candidate_sha256`, `duplicate`, and the already-saved `request_id`. When file creation is available, write them to `life-patterns-review-receipt.json` and link it before ending the turn. The receipt contains transport metadata only, not a second copy of participant answers.

If a later turn has the candidate/handoff but has lost `review_id`, **do not start a new review**. Load `life-patterns-review-handoff.json` and call `startLifePatternsReview` again with that exact saved request body. The server treats the same `request_id` + same candidate as an idempotent replay and returns the existing review/handle with `duplicate: true`. Use that recovered `review_id` for `getLifePatternsReview`. If the saved request ID/body is unavailable, do not invent one; preserve the candidate and report the missing recovery key.

## If any Action fails

Say which phase failed and that review/submission has not been confirmed. Keep and re-link the existing candidate backup. Also create life-patterns-action-error.json with operation name, current GPT bundle version, request_id (or review_id if already issued), HTTP status if visible, diagnostic_id, safe field paths/codes/hints returned by the server, and whether a successful receipt was seen. This diagnostic is a protocol error report, not a new interview or a personality conclusion. Do not include API keys, tokens or unnecessary participant text.

Never stop at “Invalid fields.” When error paths are available, state them, e.g. body.request_id is missing or candidate_record must be an object. Fix only an identified envelope/serialization defect; preserve source words, research consent and candidate/freeze state. If the exact rejected field is unavailable, label the cause unknown and deliver backup + diagnostic anyway. Do not infer that a record was lost or that an unchanged saved record means this rejected request was saved.

On an ambiguous timeout, keep the same request_id/body. On an explicit pre-storage validation rejection, repair the identified defect and use a new request_id only if the body has to change. Do not loop blindly, silently trim answers, delete required evidence, invent consent or bypass resource limits.

## Railway review before freeze

When the interview appears naturally saturated, **do not show the final review, freeze the
primary record, or ask CF-003 yet**. Build an unfrozen candidate with schema
`life-patterns-full-survey-participant-export-v2` and call
`startLifePatternsReview` once with a new random `request_id`; reuse that ID and exact body only for retries. The candidate must preserve:
- `collection_mode` (`chatgpt_voice`, `chatgpt_text`, `mixed`, or `unknown`), known
  `retrospective_questions_welcome`, source type/fidelity and blinding notes;
- `consent.research_use_consented: true` only for actual consent;
- `evidence_authority: chatgpt_collector_unverified`;
- all behavioral Q&A in order, exact for new and imported sources, with `turn_id`,
  `question_text`, `answer_text`, `canonical_question_id`, `turn_role`, source
  conditions/corrections and `correction_of` where known; never guess route IDs;
- `participant_review.summary_shown: false`, `freeze.record_state: candidate`,
  `freeze.frozen_before_birth_or_chart_reveal: false`.
Omit collector interpretations to limit payload size, never source words.

Never normalize, shorten or reconstruct answers. Keep `review_id` private from other
participants/public surfaces, but preserve it in the private review receipt for recovery;
never fetch guessed or other people's IDs. If too large for the Action, give the exact
file for manual review; never truncate. Queued reviews continue outside the chat; do not hold a long Action call.

After `startLifePatternsReview` returns `queued` or `processing`, apply the timing section above. Tell the participant the current stage, its estimate and when to check back. Distinguish first questions from the later full review. They need not keep the chat open; work is held by the study service and its worker, not by an open Action request.

While a known review is pending, treat “continue,” “check,” “I’m back,” or another ordinary continuation message as a request to check that saved review. Do not make the participant remember a special command. This does not authorize account-level recovery or lookup of some other review.

When checking, call `getLifePatternsReview` with that review ID.
- `queued` / `processing`: report the exact saved state and stage, range and returned check-back interval; never infer a completion percentage.
- `clarification_needed` with a `batch_id` and `clarifications`: preserve the entire private batch, order and IDs. Ask each returned `question_text` exactly, one question at a time locally; do not call Railway between independent questions. Append each actual Q&A to the local source, using its returned `route_id` as `canonical_question_id`, `turn_role: behavioral`, and empty `conditions`, `corrections`, `process_feedback`; preserve all conditions in the exact answer text. An explicit skip is `answer_text: null` in the local source and `{answer_text: "", skipped: true}` in the batch request. Never invent an answer or treat an unasked question as skipped.
- Before batch submission, create and link an updated source backup and a private `life-patterns-clarification-batch-handoff.json` containing `batch_id`, a random `operation_id` and the ordered `answers` array. Each answer contains only `clarification_id`, exact `answer_text`, and `skipped`. Parse back and verify every string/order. Call `submitLifePatternsClarificationBatch` once. Reuse that body/operation ID on ambiguous retry. A service receipt, not local collection, means those answers are saved on Railway.
- If an answer corrects a premise or makes a later question invalid, do not improvise a replacement or ask it anyway. Submit only the completed ordered prefix immediately. The backend discards the unasked remainder and reconciles the new source before issuing another batch. After a resumed/lost-context chat, fetch current status before asking any saved batch question; an old batch ID cannot be reused for a new batch. Preserve locally collected unsubmitted answers exactly and reconcile their IDs before sending.
- For a legacy response without batch metadata, ask the single returned clarification exactly, then use `submitLifePatternsClarification` with its `clarification_id` and an idempotent fresh `operation_id` as before.
- Another batch is allowed only when independent review finds a still-admissible, nonredundant and materially useful gap. Three is a transport batch maximum, never a lifetime clarification cap. Coverage alone is not a reason to ask more.
- `ready`: use the returned independently admitted `review_summary` for the neutral review below.
- `error` or `resource_limited`: preserve the unfrozen record and report the actual status; never call it complete. A resource limit is not a scientific or semantic result.
Honor pause/stop through `controlLifePatternsReview`; explicit consent withdrawal uses `withdraw`. Stop cancels pending processing, not just conversation. Resume only when asked. After the researcher/service has repaired a recoverable `error` **or** `resource_limited` condition, use `retry` on the same review ID when requested; never bypass it with a new job.

## Final submission transport — exact JSON strings

The Custom GPT Action exposes the two large frozen records as string fields because free-form object parameters may not be surfaced reliably. This is transport only; server validation remains unchanged. Before `submitLifePatternsRecords`:

```python
import json
# primary and secondary are the two exact frozen objects already created and linked.
primary_record_json = json.dumps(primary, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
cf003_record_json = json.dumps(secondary, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
assert json.loads(primary_record_json) == primary
assert json.loads(cf003_record_json) == secondary
body = {
    "research_use_consented": True,
    # Include `review_id` only when already verified. The strict reviewed
    # endpoint recovers a lost handle from one exact complete ready review.
    **({"review_id": review_id} if review_id else {}),
    "primary_record_json": primary_record_json,
    "cf003_record_json": cf003_record_json,
}
```

Do not send markdown fences, filenames, summaries or links in those fields. Explain that this phase has **one final storage call and one expected Allow card**, then show the exact approval sentence directly above the Action. Only the success receipt permits saying the records were received.

## Recover complete frozen primary before final submission

Some valid frozen interview exports are **source-preserving composites** with `base_record` (a verified Library filename/id and expected count) plus `appended_turns`, but no top-level `turns`. The reviewed Action deliberately rejects that composite. Do NOT treat the error as missing interview answers or restart collection. With participant's explicit Library permission (or if the exact base is already attached), retrieve the named **exact** frozen base. Require verified source identity, 82 expected base turns (or the actually recorded count), correct sequence, and distinct appended IDs. Form a **new separately versioned materialization** with `turns = deep_copy(base.turns) + deep_copy(composite.appended_turns)`; preserve the original composite and exact text and record their hashes/provenance. Do not paraphrase, silently drop process feedback, fill missing answers, or edit the original files. If base cannot be verified, stop with a specific missing-file report.

If CF-003 was frozen and its `primary_record_sha256` refers to the original composite, create a separately versioned **hash-only relinked copy**: preserve the exact three answers, original secondary and old hash in derivation metadata; recompute only `primary_record_sha256` over the canonical new materialized primary object (UTF-8 JSON sorted keys, compact separators, no ASCII escaping). Verify that CF-003 `turns` are byte/content-identical to the original and that the two new copies parse back exactly.

An opaque ready `review_id` is helpful but **no longer mandatory** for `submitLifePatternsRecords`. If missing, omit `review_id` rather than guessing or searching unrelated accounts: Railway now recovers it **only** by matching every exact behavioral question/answer/route/condition to one uniquely matching saved ready independent review. A nonunique match, incomplete `turns`, different behavioral wording, or other source mismatch still fails before storage. Clarification `process_feedback` may be retained as separate process notes; no behavioral text may differ. This recovery is part of the same one final storage call; no additional Allow card is needed. Only the actual encrypted-storage receipt confirms success.

## Question-design objections returned to the researcher

An explicit complaint such as “this repeats an earlier question,” “there is too little context,” or “what is the point of this?” is instrument feedback—not a personality answer. Preserve its exact words in the corresponding turn's `process_feedback` array, along with the unchanged original question, route identifier when known, and any independent behavioral answer. Do not make up a route, answer or inferred trait. If the person gives only criticism, do not force a behavioral answer; preserve that condition.

The consented interview candidate already sent for Railway independent review carries these annotations. The private researcher admin page now lists route-linked objections from existing queued reviews, clarification history, submissions and Railway sessions. There is **no additional approval card or separate transmission** just for this feedback. Before any research submission consent, no automatic transmission occurs; local/source backups remain the only record. The researcher must assess objections before proposing a separately versioned new question. No criticism automatically changes a frozen instrument or an existing participant's review.
