# 15 — Project Bundle Inventory

This note records which files from the August 21–22 Human Design project bundle were imported, superseded, or intentionally left as legacy material.

## Imported / promoted

- `reference/core/v4_3_scoring_algorithm.md` — current implementation-facing symbolic scoring contract.
- `reference/core/behavioral_target_combined_v3_5.md` — current descriptive/refinement target.
- `docs/14_month_first_blind_validation.md` — preserved month-first human validation design.
- `reference/verified_cases/joel_verified_natal_baseline_v2.json` — official-engine-visible-field golden/reference case.
- `CODEX_V4_3_MIGRATION_PROMPT.md` — explicit task prompt for migrating the existing V4.1/V3.2 worker.

## Already represented in the repository

The bundle also contained older Custom GPT / transit support material. The repository already contains current copies/versions under `reference/custom_gpt/`, including:

- `authority_and_transit_guardrails.md`
- `custom_gpt_instructions_under_8000.md`
- `daily_hd_transit_task_prompts_v2.md`

An older singular `daily_hd_transit_task_prompt.md` is therefore not promoted as current.

The repository already contained the original push/readme/handoff material, so duplicate copies are not added as new normative files.

## Behavioral target history

The bundle contained `behavioral_target_reverse_match_blind.md` and multiple V3.4 target variants. These are useful provenance, but V3.5 is the active development target. They must not override V3.5 merely because they are older or more candidate-blind.

When importing them later for archival completeness, place them under a history/provenance path rather than making them normative.

## V4.2 protocol

The bundle contains the full V4.2 protocol, whose substantive additions include full-depth feature calculation, flexibility penalties, revision adjudication, and dynamic-conditioning modules. V4.3 adopts and hardens the scoring-critical portions of those additions.

For Codex implementation, `reference/core/v4_3_scoring_algorithm.md`, `AGENTS.md`, and `docs/13_v4_3_migration_and_century_cache.md` are authoritative. The old V4.1 file must not be treated as newer merely because it is the only old monolithic protocol file already present in the repository.

## Simplified global scan artifacts

The bundle also contains global-scan JSON outputs produced by an earlier simplified scorer. These may be preserved only as explicitly labeled legacy/debug artifacts.

Rules:

- never compile mappings from their winning features;
- never use their integer scoring formula as V4.3;
- never use them as the authoritative century cache;
- never treat their candidate ranking as a regression target that the new model must preserve.

The correct long-term replacement is the verified exact-state century cache described in `docs/13_v4_3_migration_and_century_cache.md`.

## Import principle

Preserve provenance without creating multiple competing sources of truth. Current normative model files live at explicit versioned paths; historical artifacts live under archival/legacy paths and must be labeled accordingly.
