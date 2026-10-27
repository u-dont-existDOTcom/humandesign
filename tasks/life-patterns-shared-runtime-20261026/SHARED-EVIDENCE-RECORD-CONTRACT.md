# Optional shared evidence record

This is an engineering integration of the existing development candidate. Its
23 topics and seven probes retain their original participant wording. It is
separately consented, optional and unscored. It does not change the independently
reviewed primary record, CF003, the Experience & Meaning record or an existing
score. Software validation does not establish measurement validity or blinding.

## Runtime boundary

The participant runtime receives only `shared-life-topics-v3.json`, produced by
the explicit whitelist in `build_shared_evidence_projection.py`. The complete
source and per-object hashes remain here as researcher provenance. Do not load
the original source or this provenance into a chart-blind interview/review.

## Record fields

- `schema`: `life-patterns-shared-evidence-addendum-v1`
- `instrument`: `shared-life-topics-v3-20261026`
- `research_use_consented`: the actual separate opt-in, `true`
- `collection_mode`: `gpt_optional` or `railway_finish`
- `status`: `post_review_development_not_scored`
- `sittings`: one or more separately chosen sittings before final submission

Each sitting records a unique `sitting_id`, one to five `topics_selected`, zero
to two `probe_admissions`, and chronological `responses`. An admission contains
`probe_id`, its eligible `parent_topic_id` and the actual
`unresolved_distinction`; theoretical coverage is not a reason to ask.

Each response has `question_id`, `prompt_kind` (`main` or `followup`) and `state`.
When asked, `question_text` must be the exact corresponding bank wording, and
`answer_text` preserves the exact supplied text, including whitespace. Followups
also require the actual `unresolved_distinction`. Process objections may be
preserved verbatim in `process_feedback`, a separate list of comments, never
trait answers.

Every selected topic has an explicit main response state. Unvisited selected
topics use `NOT_ASKED`; unselected topics are absent and do not become negative
outcomes. A question that was displayed but left unanswered must not be
misrepresented as never asked; offer an explicit skip/stop choice or preserve an
unfinished backup without finalizing the optional sitting.

`NOT_ASKED`, `SKIPPED`, `FUTURE_PENDING` and `ALREADY_COVERED` have no new answer.
The other original evidence states require the actual supplied response text.
A deliberately selected response label can itself be that exact source text;
never supply an answer label on the participant's behalf. `FUTURE_PENDING` is
only a no-answer state: future predictions are not trait evidence, and no future
outcome questions are added to this bank.

`ALREADY_COVERED` uses `source_ref` and `source_quote`; neither a new prompt nor a
new answer may be invented. Reference strings have these forms:

```text
/primary/turns/0/answer_text
/cf003/turns/2/answer_text
/shared/sittings/0/responses/0/answer_text
/experience/responses/0/note
```

The quote must be exact contiguous text at the actual referenced answer. The
source catalog excludes collection metadata, skipped/process-only/quarantined
answers and originals explicitly superseded by a correction. A correction's
own exact text may be used. This verifies reference integrity, not whether that
answer actually resolves the same distinction; the collector must preserve
scope, conditions and corrections.

Exact free-text notes from a separately consented, valid Experience & Meaning
record may also resolve a shared topic. Only nonempty notes in `ANSWERED`,
`NEVER` or `UNKNOWN` responses are eligible; skipped/unasked/covered entries,
structured choice values and other fields are not new source prose. The helper
`experience_source_catalog(record)` validates the existing record with its own
validator, then pairs each eligible note with the exact existing question.
The experience record is optional in both `source_catalog` and
`validate_shared_evidence_record`, preserving their earlier calling forms.

If adequate Experience & Meaning evidence consists only of structured choices,
leave the corresponding shared topic unselected. Do not reask it, manufacture a
note, or relabel structured values as exact prose to satisfy this bounded
reference format. Changing a draft note or removing its separate opt-in requires
revalidating dependent references; an absent or stale note cannot be reused.

An earlier substantive shared answer may also support another selected topic,
in the same sitting or a later one. Shared references become available only
after their source response has passed chronological validation. Self/forward
references, skipped or unasked states, process-feedback pointers and reuse
chains are rejected. Point directly to the original substantive answer instead
of another `ALREADY_COVERED` entry. A reference may also identify an earlier
validated followup answer. These are shared observations, not additional
independent confirmations.

Shared responses remain editable drafts until final submission. Shared pointers
identify positions in the current draft, so editing/reordering earlier answers
requires revalidating every dependent reference and its scope before submission.
An obsolete quote is rejected rather than silently repaired. Primary/CF003
source records stay immutable, and this draft behavior creates no requirement
to capture every keystroke or overwrite a previously frozen record.

A probe/followup requires a preceding `ANSWERED`, `CONTEXT_DEPENDENT` or
`UNCERTAIN` parent/main response. A skipped variant blocks further variants.
Previously answered, covered or skipped topic/probe IDs cannot reopen in another
sitting. `NOT_ASKED` may be selected later. Multiple sittings do not convert the
five/two burden allowance into a lifetime quota; the transport has a separate
250,000-byte JSON limit.

## Source and date fidelity

The new addendum rejects explicit birth/chart language but accepts ordinary
numeric event dates and clock times. A numeric date/time combination alone is
not proof of birth exposure. The guard is conservative and not a complete
semantic classifier. It does not rewrite source text; on rejection preserve the
participant's backup and report a safe diagnostic. The existing primary-record
guard is unchanged by this module.

## Verification

Run from the repository root with the participant package on `PYTHONPATH`:

```bash
PYTHONPATH=apps/life-patterns-participant python -m pytest apps/life-patterns-participant/tests/test_shared_evidence.py -q
```

The focused cases verify projection reproduction and source hashes, all 30
unchanged question/followup pairs, absence of source mappings in the runtime,
consent, exact text/date preservation, distinct missingness, source references,
corrections, per-sitting limits, multiple sittings and skip/repeat prevention.
They use fabricated examples only and do not establish human measurement validity.
