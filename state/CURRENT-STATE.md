# Current state — voice-first collection / compact Railway clarification

Updated 2026-09-28. Branch: `chat/hybrid-voice-cost-optimization-20260928`, based on the current participant-service line at `dabcb1a6b60e7fd85d5765a780f2c9f933ff61b5`.

## Owner outcome

The long Life Patterns interview should not require an hour of typing when voice produces richer answers. The development direction is now **voice-first ChatGPT collection -> frozen behavioral JSON -> Railway durable provenance and only genuinely useful clarifications**. Railway text remains available as a comparison mode; no claim of voice/text psychometric equivalence is made.

API inference must fit the owner's limited Venice allowance. OpenRouter is not used. Development semantic probes use the owner's subscription-authenticated Codex CLI where available rather than Venice API credit.

## Cost diagnosis and repair

The prior Railway planner repeatedly sent the full protocol/controller, all 79 routes, all 73 evidence facets and accumulated transcript, followed by a second large independent-admission request. One private 96-turn development record measured ~175k characters for the old planner request alone; participant text/identity were not published.

The candidate keeps full raw source and frozen authority server-side but compacts model context:

- one complete-source bulk review after import;
- later calls receive exact current/pending source plus necessary antecedents/recent turns;
- accepted evidence is a compact ledger;
- at most 12 deterministic eligible routes are supplied for ordinary clarification;
- evidence guidance is scoped to relevant routes/facets;
- the independent reviewer receives only proposal-relevant source, the selected route's route-specific rules and cited evidence guidance;
- routine context fails closed above 35k serialized characters, bulk above 110k;
- output-token ceiling remains at the previously exercised provider setting; proposed low caps are deferred until exact Venice/XHigh truncation behavior can be tested without consuming scarce development credit;
- default model-call ceiling: 12 actual semantic calls/session, with only 8 available before final review so both final-review Plan+Admission attempts remain reserved;
- optional-retrospective routes are excluded unless the participant explicitly welcomed earlier-life comparisons.

The latest aggregate planning proxy on the private 96-turn development record is in `tasks/hybrid-voice-cost-optimization-20260928/COST-BENCHMARK.json`. It reports ~33.3k token-equivalent for the one-time bulk Plan+Admission pair, ~7.5k per later clarification pair, and ~55.8k input-equivalent for one bulk pair plus three clarification pairs before the four-call final-review reserve. These are planning proxies, not provider-billed totals; actual completion/reasoning tokens remain provider-dependent.

## Voice-first collector

The development Custom GPT bundle is under `reference/custom_gpt/`:

- `life_patterns_voice_interviewer_v2.md`
- `life_patterns_voice_gpt_manifest_v2.json`
- `LIFE-PATTERNS-VOICE-GPT-SETUP.md`

It uses the frozen v7 protocol/bank/evidence guide as Knowledge and keeps must-follow collection/accuracy rules in Instructions. The instruction block is 7,691 characters on the repository's conservative count.

The collector records collection mode and retrospective-question preference as nonbehavioral metadata. It treats the visible transcript—not inaccessible original audio—as the source record, labels model-exported transcript fidelity, exports collector evidence as unverified, preserves exact quotations, scopes absence claims to checked source, rechecks corrections, and does not infer motive/backstory/history. Railway preserves that source but does not admit GPT-authored evidence without its own independent admission. These are the core PR #42 claim-integrity protections adapted to the new collector. The older deployable interviewer remains unchanged because it is already at 7,933 strict characters.

`apps/life-patterns-participant/scripts/analyze_collection_modes.py` provides a descriptive whole-pipeline CSV/JSON comparison of answer richness, conditions/corrections, collector-unverified versus Railway-admitted evidence, clarification burden and model/token usage. It explicitly does not establish voice/text equivalence or attribute a pipeline difference to voice alone.

## Development inference

`apps/life-patterns-participant/scripts/codex_dev_probe.py` runs planner/admission prompts through subscription-authenticated Codex CLI and validates the JSON locally. The final reconciled GPT-5.6 Sol XHigh synthetic probe selected fresh route G23 and independent admission approved first-pass. No paid API was used.

The existing Railway Cloud Agent `codex-human-46r` is preserved and sleeping. Codex is installed there, but its saved refresh token was revoked; a cloud semantic probe was not run. Re-authentication is a dev-harness matter, not a production blocker.

## Verification

Final candidate evidence: focused reconciliation 73/73 PASS; complete participant-service suite 79/79 PASS; mobile browser smoke PASS with no JavaScript errors; repository-wide pytest 940 passed / 6 skipped; V7 authority verifier 497/497 PASS. The task app lint passes. Global Ruff, mypy and task-acceptance remain baseline-broken outside this task: 895 Ruff diagnostics across 56 unchanged files, mypy Python-3.11 target versus locked NumPy-2.5.2 3.12-only stub syntax, and missing parent oracle artifacts/worktree-local `.venv`. See `VERIFICATION.json`.

Claude Opus 5.5 max returned FINDS_ERROR on the initial architecture check and again on the single reconciliation. The second review explicitly found no blocker to a dark deployment with inference disabled; every concrete remaining live-inference defect it identified was subsequently repaired and regression-tested. No third reviewer round is claimed.

## Production boundary

Dark preview deployed and verified on Railway from commit `8978e543b492c4497d501c4f4d2d2c296f7a312f` as deployment `2fb89371-12bf-43cf-969f-ae0ee1b9dc06`. Health reports `railway-participant-v2.2-cost-hybrid-20260928`, `participant_enabled=false`, `provider_configured=false`, and encrypted SQLite persistence on the existing `/data` volume. `PARTICIPANT_MAX_MODEL_CALLS=12`; the participant gateway credential is absent. No paid inference or participant inference was run. The original `life-patterns-owner` service remains on deployment `2d60d3dd-2634-427c-a48f-62a36ee27350`.

This is not a release-certified live inference deployment. Venice previously returned HTTP 402, and repository-wide Ruff/mypy/task-acceptance have the baseline debt recorded in `tasks/hybrid-voice-cost-optimization-20260928/VERIFICATION.json`. Keep Railway inference disabled. Before any live enable: resolve Venice API credit/access, address or explicitly disposition the release debt, update the activation helper for the exact reviewed v2.2 build, and obtain explicit paid/live inference authorization. Do not route public participants through Codex CLI.


Historical owner-method correction remains in force: **there was never a completion policy** requiring predetermined question coverage. Natural stop is based on whether another route is both admissible and useful; the bank remains a menu, not a quota.
