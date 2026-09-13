# Life Patterns v2 owner real-data browser implementation receipt — 2026-09-13

Status: IMPLEMENTED; exact-head final CI pending at receipt creation.

## Implementation head

`002d6264f05a7e380d4cac7e188f8c9455fbf971`

Hosted repository CI on that implementation head: **success**.

## Added

- `src/hdmatch/api/life_patterns_v2_owner_app.py`
- `src/hdmatch/api/life_patterns_v2_owner_ui.py`
- `tests/unit/test_life_patterns_v2_owner_app.py`

## Behavior

The owner-only local browser app:

- accepts the owner's own real episode narratives;
- sends only episode text to a target-theory-blind extraction prompt;
- extracts literal/minimally normalized episode facts, not person-level recurrence;
- lets the owner keep, edit, or reject each proposed fact;
- stores corrections as append-only v2 revisions;
- excludes unsupported proposed facts from the authoritative record;
- waits for two reviewed episodes in this bounded product probe before offering a cross-episode pattern search;
- allows at most one tentative pattern hypothesis backed by reviewed operative facts from at least two episodes;
- keeps participant adjudication authoritative;
- separates “this wording feels true of me” from “these examples actually support this wording”;
- leaves revised wording unresolved when it comes from other situations or its support is unclear, inviting another episode instead of laundering current evidence;
- validates/freeze/projects final accepted/rejected/unresolved threads through `participant_adjudicated_v2.py`;
- keeps runtime narratives in memory only.

## Non-use of historical authority

The new app does not import or invoke `life_patterns_app`, `OpenAILifePatternsMapper`, or the historical `/map` person-level generator.

## Model runtime

The local app reads an owner-controlled runtime key from `HDMATCH_LLM_API_KEY` or `OPENAI_API_KEY`, with configurable model/endpoint environment variables. Committing the app does not initiate a paid model call.

## Scientific boundary

The two-reviewed-episode wait is a bounded product-probe choice, not a universal scientific sufficiency threshold. No birth/chart/target-model information is provided to extraction or hypothesis generation. Genuine absence extraction is deliberately outside this minimal prototype; the frozen four-gate absence route remains authoritative.

## Next gate

Owner uses the direct browser surface with 2–3 real episodes and gives product judgment before any broader scaling.
