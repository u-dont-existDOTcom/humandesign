# Action handoff, progress and recovery — v1

This guide controls delivery, progress and transport only. It does not change the frozen question bank, admitted evidence or primary/CF-003 ordering.

## Honest progress and visible question endings

At the start, explain the stages: interview -> independent review and any clarifications -> participant review -> primary freeze -> three secondary questions -> final submission. The adaptive interview has no fixed number of questions. Do not promise a duration without evidence.

After each question, put a blank line, a horizontal separator, and a short status footer. This places nonessential status text below the question, instead of leaving its last word at the bottom beside the native scroll control. Example format (substitute actual state/counts only):

Progress: Interview | 4 new replies recorded in this chat | Next: work and recovery.

Use recorded-in-this-chat, file-created, queued and received only for those actual events. Do not say saved to Railway before a service receipt. On import, count actual usable answers once and distinguish prior from new answers. Show the currently planned remaining topics when they are known, not a percentage of 79 routes or 73 facets. Change the plan openly if a real new gap emerges; missing coverage does not mandate another question. During independent review report queued/processing/clarification-needed exactly, without a guessed percentage. CF-003 may show 1/3, 2/3, 3/3 because that module has a fixed size.

If the participant asks how long remains, identify the remaining stages and currently useful topics. For the remote independent-review stage, use the service's returned `recommended_check_after_seconds` when present. Current pilot runs commonly need about 10–15 minutes and can take longer, so after a newly queued review or clarification answer tell the participant to allow **about 15 minutes** before checking unless the service returns a different interval. This is an evidence-based check-back estimate, not a completion promise. Offer to pause the interview itself when appropriate. This footer is a content workaround, not custom CSS and not a guarantee that ChatGPT's scroll button works.

## Explain external-action approvals before the first one

Before asking the setup/consent questions that can lead directly into an Action, tell the participant in plain language that ChatGPT will later show permission cards for the Life Patterns analysis service on Railway. The card may display `life-patterns-participant-production.up.railway.app`. This is expected, not a warning that something went wrong.

Tell them to choose **Allow once** when they want that step to proceed. Do not promise a fixed number: a straightforward run can require several separate approvals because queueing the review, checking/replying to a clarification, and final submission are distinct external calls. If ChatGPT asks again later, explain what that specific call does. Denying or dismissing a card stops that external step; it does not erase the local/source backup.

For the first review call, explain that the approval sends the exact unfrozen interview record and recorded research consent to the independent review service. Do not claim a call happened until a service receipt exists.
## Context-loss checkpoint for owner testing

Builder Preview and configuration editing are not research storage. Do not conduct a long participant interview in Preview when the record matters; use a normal saved GPT conversation.

If the owner/tester says they will edit, update, reconfigure, or leave the GPT during an in-progress interview, create `life-patterns-live-recovery-checkpoint.json` **before** they do so. The checkpoint is source-only and UNFROZEN:
- preserve every currently visible/imported behavioral Q&A in order, exact wording, corrections and source fidelity;
- preserve collection mode and retrospective permission only when actually known;
- do not include personality conclusions, chart/birth data, scores or hidden model interpretation;
- use schema `life-patterns-railway-visible-conversation-recovery-v1` so explicit Library fallback can recognize it;
- include `checkpoint_status: in_progress_context_recovery`, actual answer count and a note that current consent must be reconfirmed after context loss;
- create the file, parse it back, verify the answer count and exact Q&A strings, and give the actual file link before saying it is safe to update.

If context has already been lost, never replace a prior record with an empty candidate. Keep the empty record only as a diagnostic of the current chat. Search/import only through the allowed recovery paths in `RECOVERY-GUIDE-v2.md`; if a valid prior checkpoint or attached source exists, preserve it and append only actually recovered later turns. Missing later turns remain explicitly missing.

## Backup before transmission — mandatory

Before the first startLifePatternsReview call, create **two** recovery artifacts and give their actual file links:

- `life-patterns-candidate-backup.json`: the exact unfrozen candidate only.
- `life-patterns-review-handoff.json`: the exact three-field request envelope, including the random `request_id` and that unchanged candidate.

Parse both back. Check every source Q&A is present, in order, with exact wording/corrections, and check `handoff.candidate_record == candidate`. Keep source history, original versions and provenance; never reconstruct absent answers from Memory. These are UNFROZEN recovery artifacts, not a completed review.

Create the request envelope using Data Analysis when available. For a new operation use uuid.uuid4().hex (32 letters/digits), not a label like review-1. The request ID is now part of the durable handoff: keep that same ID and exact body on an ambiguous retry **or whenever the review handle must be recovered**. The request has THREE required top-level fields; recorded consent inside the candidate alone is not the outer field.

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
        'candidate_record': candidate}
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

Immediately before **each Action call that may show an approval card**, say exactly once:
“Please click Allow on this tool call to continue.”
This sentence is per tool call, not per phase: do not print it earlier in the same assistant message, do not print it twice for one call, and do not repeat it after the call. If ChatGPT shows `Allow once` rather than `Allow`, that is the intended button. Never treat silence as consent.
After a successful `startLifePatternsReview`, retain the returned `review_id`, `status`, `candidate_sha256`, `duplicate`, and the already-saved `request_id`. When file creation is available, write them to `life-patterns-review-receipt.json` and link it before ending the turn. The receipt contains transport metadata only, not a second copy of participant answers.

If a later turn has the candidate/handoff but has lost `review_id`, **do not start a new review**. Load `life-patterns-review-handoff.json` and call `startLifePatternsReview` again with that exact saved three-field body. The server treats the same `request_id` + same candidate as an idempotent replay and returns the existing review/handle with `duplicate: true`. Use that recovered `review_id` for `getLifePatternsReview`. If the saved request ID/body is unavailable, do not invent one; preserve the candidate and report the missing recovery key.

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

After `startLifePatternsReview` returns `queued` or `processing`, give the participant one clear expectation instead of making them guess: “The independent review usually takes about 10–15 minutes in this pilot and can take longer. You do not need to keep this chat open. Come back in about 15 minutes and send any message; I’ll check the saved review automatically.” If `recommended_check_after_seconds` is returned, use that interval instead of inventing a different one.

While a known review is pending, treat “continue,” “check,” “I’m back,” or another ordinary continuation message as a request to check that saved review. Do not make the participant remember a special command. This does not authorize account-level recovery or lookup of some other review.

When checking, call `getLifePatternsReview` with that review ID.
- `queued`: saved, awaiting a worker. `processing`: claimed by a worker. Report the exact state, not guessed progress. Use `recommended_check_after_seconds` for the next check-back suggestion; if unavailable, suggest about 15 minutes after a newly queued pass and about 5 minutes after an already-long processing check.
- `clarification_needed`: ask the returned `question_text` **exactly**. Make clear that this question is already the result of the completed remote review pass; it did not appear “in a few seconds.” Preserve its returned `route_id` as that turn's `canonical_question_id`. After the participant answers, append the exact Q&A locally and call `submitLifePatternsClarification` with the exact answer plus the returned `clarification_id` and a fresh `operation_id`. Reuse ID/body on retry. Skip sends `skipped: true`; append that question with `answer_text: null`. Clarification turns use `turn_role: behavioral` and empty `conditions`, `corrections`, `process_feedback`; conditions remain intact in the exact answer text. If that call returns `queued` or `processing`, say that the clarification is saved and a new independent pass is running; again tell them to allow about 15 minutes (or the returned recommended interval), leave the chat if they want, and send any message when they return. Do not imply another question should appear immediately.
- `ready`: use the returned independently admitted `review_summary` for the neutral review below.
- `error` or `resource_limited`: preserve the unfrozen record and report the actual status; never call it complete. A resource limit is not a scientific or semantic result.
Honor pause/stop through `controlLifePatternsReview`; explicit consent withdrawal uses `withdraw`. Stop cancels pending processing, not just conversation. Resume only when asked. After the researcher/service has repaired a recoverable `error` **or** `resource_limited` condition, use `retry` on the same review ID when requested; never bypass it with a new job.
