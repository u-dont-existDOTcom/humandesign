# Optional modules after the reviewed interview

## Scope and capability

The primary interview retains its tendency-first policy, saturation rule and independent review. A completed or saturated interview still has zero new main-interview questions. These optional modules never reopen that interview, change its frozen evidence, or change a score.

After independent `ready`, participant confirmation, primary freeze, and the three separate CF003 questions and required metadata, offer optional modules in the same GPT if the participant is finishing there. Respect existing module/topic refusals. If they chose the private Railway continuation, Railway handles these steps; do not collect a parallel copy.

Experience & Meaning v2 keeps its existing separate opt-in and `EXPERIENCE-MEANING-OPTIONAL-v2.md` requirements. Keep typical/peak intensity and personal/social meaning distinct. Refusal omits `experience_record_json`.

Shared Life Topics v3 is a separately consented **development, unscored** supplement. Software validation is not independent semantic review, scientific validation, or proof of actual blinding. Do not add its answers to a reviewed primary candidate, CF003, Experience & Meaning, a personality verdict or a chart score.

With the bundled Action 1.10, set `include_shared_evidence=true` on the ordinary `getLifePatternsReview` call. This is a query parameter on that same retrieval, not another external call. The optional capability appears only when requested. Offer the shared supplement only if that saved review returns `shared_evidence_available: true`. Missing/false means it is not available for this review; proceed with the supported existing finish. A finalized submission cannot accept a changed addendum. Never send this new query or record field through an older installed Action schema.

## Offer and burden

Explain that the participant may finish now or choose a few additional life topics, that these are separate research drafts, and that they may skip or decline all. Ask for separate actual opt-in before collecting either module; consent to one does not imply consent to the other. Do not ask another main-interview “ready” or mode question.

For the shared supplement, use only `SHARED-LIFE-TOPICS-v3.json`. Show its topic labels and let the participant select up to five for this sitting. Present exact existing `question` wording one at a time. Do not send the original research candidate, its theory mappings or provenance file to the participant or blind reviewer. The runtime projection is the complete permitted menu.

Reuse adequate same-scope existing answers first. A new topic ID is not a reason to ask the same distinction again. Preserve prior opt-outs; never select a topic from chart information, source-theory coverage, an empty scoring cell or a desired answer. Do not activate the separate proposed craft question. Preserve the original question conditions; the engineer has not authored replacement behavioral wording.

The limit is five selected base topics and at most two additional conditional probes **per sitting**, not a lifetime cap, target or minimum. A followup needs an actual unresolved distinction and the exact `optional_followup` or probe `followup` wording. A probe also needs an eligible selected parent in both its `related_topics` and the parent's `conditional_new_probe_ids`. No followup/probe after a skipped, already covered, not asked, inapplicable, never or no-opportunity parent. Do not turn hypothetical scenarios into personal biography.

Stop at the end of the chosen sitting. Further sittings occur only on a participant's choice before final storage. Already answered, covered or skipped IDs cannot reopen; a previously unasked ID may be chosen later. Skips cover variants. There is no question quota for a different astrological system.

Show progress through the chosen sitting, including remaining selected questions and a revisable estimate of answering minutes. Keep this separate from review/service waits and from unknown future reviewer work. Completing a sitting is a real stopping point.

## Separate record

Create `life-patterns-shared-evidence-addendum-v1.json` with these exact outer fields:

```json
{
  "schema": "life-patterns-shared-evidence-addendum-v1",
  "instrument": "shared-life-topics-v3-20261026",
  "research_use_consented": true,
  "collection_mode": "gpt_optional",
  "status": "post_review_development_not_scored",
  "sittings": []
}
```

This is a shape example, not a consent record. Never copy `true` unless actual separate consent was supplied. An opted-in record needs at least one actual sitting; on refusal omit the whole record.

Each sitting contains:

- `sitting_id`: one stable, distinct random ID, such as `uuid.uuid4().hex`.
- `topics_selected`: one to five distinct chosen base topic IDs.
- `probe_admissions`: zero to two objects with `probe_id`, `parent_topic_id`, and the actual source-supported `unresolved_distinction`.
- `responses`: chronological source responses. Every selected base topic needs a main state, including `NOT_ASKED` if it was never reached. Unselected topics are absent.

Each response contains `question_id`, `prompt_kind` (`main` or `followup`), and `state`. If actually asked, `question_text` is the exact corresponding bank wording and `answer_text` is the exact participant text, including conditions and meaningful whitespace. A followup also records its actual `unresolved_distinction`. Objections go verbatim into a separate `process_feedback` string list; they are not trait answers. Do not invent a question, answer, reason or previous event.

Keep these states distinct:

| State | Meaning and source requirement |
| --- | --- |
| `ANSWERED` | Actual supplied answer text |
| `CONTEXT_DEPENDENT` | Actual answer with its stated conditions |
| `NO_OPPORTUNITIES` | Explicit report of no relevant opportunities, not inability |
| `NEVER` | Explicit negative within the asked scope, never an omitted response |
| `NOT_APPLICABLE` | Explicit nonapplicability |
| `UNCERTAIN` | Actual uncertainty response |
| `SKIPPED` | Explicit skip; `answer_text` null/absent; retain a shown exact prompt if applicable |
| `ALREADY_COVERED` | Verified exact earlier source, with no newly invented question or answer |
| `NOT_ASKED` | Never reached; no question or answer text |
| `FUTURE_PENDING` | No current answer; do not add a future-prediction question or treat it as a trait |

The first six states require the actual supplied text. A response label may be recorded only if the participant actually selected or said it. Do not use a default to fabricate an answer.

Preserve date/age ranges, uncertainty and selective history in the actual source. A collection timestamp is not a life-event date. Do not convert selected turning points into a complete lifetime inventory or omissions into negatives. Ordinary numeric event dates and clock times are allowed here. Explicit birth/chart disclosures remain excluded; preserve a safe backup and diagnostic if rejected. Do not infer actual exposure from a software rejection alone.

## Exact reuse and draft correction

For `ALREADY_COVERED`, use `source_ref` and `source_quote`. The quote must be exact, contiguous, nonempty source text of at most 20,000 characters. A shorter exact relevant excerpt is allowed; do not shorten or rewrite the underlying source. The valid pointer forms are:

```text
/primary/turns/0/answer_text
/cf003/turns/2/answer_text
/experience/responses/0/note
/shared/sittings/0/responses/0/answer_text
```

Pointers refer to the exact final composite primary/CF003 files, an eligible note in the separately consented Experience & Meaning record sent in the same storage call, or an earlier substantive original shared response. Experience notes must be nonempty original text in an `ANSWERED`, `NEVER` or `UNKNOWN` response; structured choices alone are not quote sources. If an earlier structured choice already adequately covers a topic without a note, leave that shared topic unselected rather than reasking or inventing prose. Check indices again after materializing composites or relinking CF003. Do not refer to a summary, collection metadata, process feedback, skipped answer, quarantined/superseded source, future/self response or another reuse entry. A reused statement remains the same observation, not another vote or independent confirmation.

Quote containment verifies a link; it does not establish that the answer adequately covers the new topic. Preserve its actual scope and conditions. If the source is corrected, recheck every dependent reference and meaning. Optional form drafts may be edited before final submission; these are not changes to a frozen primary record. A material correction to the frozen primary follows the existing new-review/version procedure. Never alter frozen primary text merely to make a reuse reference pass.

## Final storage and recovery

Keep the complete optional JSON and a real download link before storage. On GPT completion, include it as `shared_evidence_record_json` in the **same** `submitLifePatternsRecords` call as the complete primary and CF003 JSON strings, plus the separately opted-in Experience & Meaning record if present. The existing one-final-call/one-expected-Allow-card explanation and exact approval sentence still apply. No additional Action is needed between optional questions.

Serialize as one raw JSON object string, not a filename, summary, link or fenced block. Validate source references and the 250,000-byte shared-record transport limit without truncating evidence. Other request-size limits still apply. On any error, preserve all original files and return the safe diagnostic; do not force success by inventing consent, deleting an answer or changing a frozen source.

The success receipt includes `shared_evidence_record_sha256` when the addendum was stored. Only that receipt permits a storage claim. Exact retries reuse the identical final envelope and stored review. An already finalized review cannot accept extra or altered answers, even if its review status still says `ready`. Later additions require their own explicit version/storage path; never start a replacement primary interview to smuggle in an optional addendum.

Birth-quality and study-specific familiarity metadata belong to the separate trusted researcher intake. They are never additional GPT Action fields and never behavioral-review input. The two established CF003 familiarity items keep their current timing and meaning.
