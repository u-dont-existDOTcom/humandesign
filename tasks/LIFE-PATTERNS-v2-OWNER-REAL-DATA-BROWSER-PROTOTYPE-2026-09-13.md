# Life Patterns v2 owner real-data browser prototype — 2026-09-13

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
PR: `#24` (remain draft/open/unmerged)

## Objective

Advance from the synthetic HTML wording probe to the smallest owner-only browser conversation that uses the owner's own real episodes while preserving the accepted v2 participant-adjudicated semantics.

The owner should interact with the browser directly. Do not return to terminal prompt relays.

## Product slice

1. Owner enters one specific real episode in ordinary language.
2. A target-theory-blind model extracts only literal/minimally normalized episode facts.
3. Owner keeps, edits, or rejects each proposed fact.
4. Fact corrections are append-only in the v2 record; unsupported proposals do not enter the authoritative record.
5. After two reviewed episodes in this bounded development probe, the owner may ask whether the examples suggest a cross-episode pattern. The two-example wait is a probe design choice, not a universal scientific sufficiency threshold.
6. The model may propose at most one tentative pattern question and must cite reviewed facts from at least two episodes.
7. Owner accepts, revises, rejects, or leaves the pattern unresolved.
8. If the owner revises the wording, keep separate:
   - whether the wording feels true of the owner;
   - whether these particular examples actually support the added wording.
9. If the revised wording comes from other situations or support is unclear, keep the thread unresolved and invite another real episode rather than laundering the current examples into support.
10. Accepted/rejected/unresolved results pass through the frozen v2 validation/freeze/projection path.

## Implementation boundary

- Reuse the visual language of the earlier `life_patterns_interview_ui.py`.
- Use a new owner-only backend; do not call the historical automatic `/map` generator or `OpenAILifePatternsMapper`.
- Runtime narratives stay in memory only for this development process. Do not write owner narrative to Git.
- No auth/recovery/voice/public hosting is required for this bounded owner test.
- The model client may use `HDMATCH_LLM_API_KEY` or `OPENAI_API_KEY` at runtime. No paid model call is authorized merely by committing this implementation; actual owner runtime use is separately owner-controlled.

## Scientific boundaries

- No birth/chart/target-model information enters extraction or pattern proposal.
- Candidate patterns remain hypotheses until participant adjudication.
- No missingness-to-absence inference.
- Genuine absence claims are intentionally not extracted by this minimal owner prototype; the frozen four-gate route remains authoritative for any later absence support.
- Postproposal material is not converted into unbiased preproposal recurrence evidence.
- Historical person-level automatic map generation remains superseded.

## Verification

Run at minimum:

```sh
python -m pytest tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q
ruff check src/hdmatch/api/life_patterns_v2_owner_app.py src/hdmatch/api/life_patterns_v2_owner_ui.py tests/unit/test_life_patterns_v2_owner_app.py --ignore E501,I001
mypy src/hdmatch/api/life_patterns_v2_owner_app.py
python scripts/task_preflight.py
```

Hosted repository CI must also be green on the exact implementation/state head before this task is called technically complete.

## Authorization

Authorized: this bounded owner-only real-data browser prototype and owner self-testing.

Still unauthorized: external participant collection, automated participant coding, downstream target-model work, public deployment, recruitment/contact, spending beyond an explicitly owner-initiated runtime model call, merge/release.

## Stop boundary

Stop after the owner can use a direct browser surface with 2–3 real episodes and judge whether the interaction is actually intelligent/natural. Do not scale the interview, add public infrastructure, or resume target-model work before that owner judgment.
