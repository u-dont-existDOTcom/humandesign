# Life Patterns participant-adjudicated neutral substrate v2 — CANDIDATE — 2026-09-12

Status: candidate only; separate fresh target-theory-blind review required before implementation.

V2 preserves the v1 open-world architecture: bounded episodes -> source-grounded episode facts -> candidate person-level pattern -> participant adjudication/revision -> immutable freeze -> adapter-only projection. Optional vocabularies remain non-authoritative indexing metadata.

## Six semantic repairs

1. **Absence routing is semantic.** Any proposition whose truth condition asserts genuine real-world nonoccurrence must use `admitted_absence` backed by the four-gate absence assessment. Other assertion types cannot encode that claim. An explicitly attributed belief/appraisal about absence remains an appraisal and does not establish nonoccurrence.

2. **Evidence timing cannot reset.** Each pattern thread has one immutable first-proposal boundary. Every evidence link records `acquisition_phase = pre_first_proposal | post_first_proposal | timing_unclear`. Only pre-first-proposal evidence may be a preproposal anchor/counterexample; revisions cannot promote later evidence.

3. **Terminal wording must stay grounded.** Every proposal that can become terminal/accepted has `grounding_evidence_link_ids`. At least one must be a current admissible pre-first-proposal factual anchor that substantively supports the current proposition. An unrelated anchor inherited from an earlier revision does not qualify.

4. **Fact corrections are append-only.** Episode facts have stable `fact_lineage_id` and monotonic `revision_index`. A participant correction creates a new fact with exact correction provenance and `supersedes_fact_id`; originals remain audit history. In-place mutation and branching are forbidden. Only the unique current unsuperseded fact is adapter-admissible. Operative proposal grounding cannot use a superseded fact.

5. **Fact uncertainty travels with the fact.** Source-bound uncertainty/evidential qualification that changes a fact's meaning is stored on that fact with provenance and included in the adapter projection. An episode-only note is insufficient. Dropping or changing the qualification is a semantic mutation.

6. **Adapters cannot recreate person-level recurrence.** Episode facts remain episode-level evidence only. Adapters may not aggregate/count/cluster/score them into person-level recurrence, typicality, frequency, trait, or pattern claims. Downstream person-level recurrence/typicality may come only from accepted participant-adjudicated `resolved_pattern` records.

## Preserved invariants

The projection still excludes raw narrative/source resolvers and returns `unmeasured/not_represented` rather than rereading source. Open-world positive facts remain first-class without fixed categorical membership or `Other Specified`. Failed/unclear absence assessments cannot damage independent positive facts. No episode-count threshold can override participant rejection. Post-first-proposal examples remain selected scope/boundary evidence, not an unbiased recurrence sample. There is no completion denominator.

Companion contract: `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-CONTRACT-v2-CANDIDATE-2026-09-12.json`

Focused test matrix: `state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v2-FOCUSED-SEMANTIC-TESTS-2026-09-12.md`

Fresh-review prompt: `tasks/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v2-FRESH-BLIND-REVIEW-2026-09-12.md`
