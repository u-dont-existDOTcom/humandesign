# Current state — voice-first collection / compact Railway clarification

Updated 2026-09-30. Branch: `chat/hybrid-voice-cost-optimization-20260928`. CF-003 development-secondary work, the suggested-fix accuracy lane, and authenticated Custom-GPT auto-submission are integrated on this branch.

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

It uses the frozen v7 protocol/bank/evidence guide as Knowledge and keeps must-follow collection/accuracy rules in Instructions. The Life Patterns voice instruction block is 7,962 / 8,000 on the conservative strict count. The v2026-09-30.4 bundle includes one authenticated `submitLifePatternsRecords` GPT Action. After recorded research consent, primary pre-reveal freeze, and the separate three-question CF-003 freeze, it sends both records to the existing encrypted Railway store; JSON files remain fallback/local copies.

The collector records collection mode and retrospective-question preference as nonbehavioral metadata. It treats the visible transcript—not inaccessible original audio—as the source record, labels model-exported transcript fidelity, exports collector evidence as unverified, preserves exact quotations, scopes absence claims to checked source, rechecks corrections, and does not infer motive/backstory/history. Railway preserves that source but does not admit GPT-authored evidence without its own independent admission. The owner-requested UDA suggested-fix item `2026-09-30-interviewer-accuracy-checks` was processed as an adaptation in PR #48 and recorded in `docs/suggested-fixes-ledger.md`; the deployable participant interviewer is now 7,768 / 8,000 strict and the legacy reverse matcher is exactly 8,000 / 8,000.

`apps/life-patterns-participant/scripts/analyze_collection_modes.py` provides a descriptive whole-pipeline CSV/JSON comparison of answer richness, conditions/corrections, collector-unverified versus Railway-admitted evidence, clarification burden and model/token usage. It explicitly does not establish voice/text equivalence or attribute a pipeline difference to voice alone.

## Development inference

`apps/life-patterns-participant/scripts/codex_dev_probe.py` runs planner/admission prompts through subscription-authenticated Codex CLI and validates the JSON locally. The final reconciled GPT-5.6 Sol XHigh synthetic probe selected fresh route G23 and independent admission approved first-pass. No paid API was used.

The existing Railway Cloud Agent `codex-human-46r` is preserved and sleeping. Codex is installed there, but its saved refresh token was revoked; a cloud semantic probe was not run. Re-authentication is a dev-harness matter, not a production blocker.

## Verification

Integrated evidence: focused voice reconciliation 73/73 PASS; participant-service suite 79/79 PASS; mobile browser smoke PASS; V7 authority verifier 497/497 PASS; CF-003 + interviewer-accuracy + voice focused integration 68/68 PASS; repository-wide pytest 1013 passed / 6 skipped. The auto-submission affected set is 130/130 PASS and its focused endpoint suite is 7/7 PASS. Exact CI Ruff passes and mypy passes across 220 source files after the parent baseline repair in PR #47. The generic `scripts/task_acceptance.py` remains bound to an older known-month-oracle task and still expects its missing artifacts/worktree-local `.venv`; it is not the acceptance authority for this parent task. See the task verification receipts.

Claude Opus 5.5 max returned FINDS_ERROR on the initial architecture check and again on the single reconciliation. The second review explicitly found no blocker to a dark deployment with inference disabled; every concrete remaining live-inference defect it identified was subsequently repaired and regression-tested. No third reviewer round is claimed.

## Integrated CF-003 development module

CF-003 methodology repair merged through PR #45 after Opus 5.5 max returned `FINDS_ERROR` on the first implementation. The corrected inferential null reassigns complete frozen behavioral profiles within preregistered birth-cohort strata; the old global construct-label permutation is diagnostic only. Blinding/provenance, quote validation, predictor commitment, tie handling, and the neutral question module were also hardened.

CF-003 remains **DEVELOPMENT/SECONDARY only**. Existing participants are exploratory. No prospective target cohort is authorized until the chart-factor extraction convention, classifier model/version, balanced source-coverage/follow-up rule, literature-derived evaluator mapping decision, cohort strata, permutation seed/count, and final software/hash freeze are resolved. Its task-local recovery state is `tasks/cf003-secondary-module-20260929/CURRENT-STATE.md`.

## Production boundary

The participant service is deployed from merged commit `79e633ec113599362570ad757b81557f6b64294c` as deployment `5b4b9467-4d99-44f2-b094-69f2a1ffc4d4`. Health reports `railway-participant-v2.2-cost-hybrid-20260928`, `participant_enabled=false`, `provider_configured=false`, `gpt_submission_enabled=true`, and encrypted SQLite persistence on the existing `/data` volume. The submission route uses a separate Bearer credential, is idempotent, rejects structured birth/chart/ranking fields, requires recorded consent + primary pre-reveal freeze + all three CF-003 questions, and never invokes model inference. `PARTICIPANT_MAX_MODEL_CALLS=12`; the participant gateway credential is absent. No paid inference or participant inference was run. The original `life-patterns-owner` service remains on deployment `2d60d3dd-2634-427c-a48f-62a36ee27350`.

This is not a release-certified live inference deployment. Venice previously returned HTTP 402. Repository-wide Ruff and mypy are now green after PR #47; the generic task-acceptance script still carries unrelated legacy known-month-oracle binding debt. Keep Railway inference disabled. Before any live enable: resolve Venice API credit/access, update the activation helper for the exact reviewed v2.2 build, and obtain explicit paid/live inference authorization. Do not route public participants through Codex CLI.


Historical owner-method correction remains in force: **there was never a completion policy** requiring predetermined question coverage. Natural stop is based on whether another route is both admissible and useful; the bank remains a menu, not a quota.
