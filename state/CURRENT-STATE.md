# Current state — CF-003 independent behavioral dominance secondary module

Updated 2026-09-29. Branch: `chat/cf003-secondary-module-20260929`.

## Owner outcome

A separate CF-003 DEVELOPMENT/SECONDARY module is now implemented without changing TN-001, LiteratureModelV1, the main Life Patterns score, or the dark Railway participant deployment.

The purpose is to test the published CF-003 weighted planetary-dominance predictor against a genuinely independent chart-blind human target instead of reusing the historical chart-conditioned biographical target.

## Predictor status

The source-replayed CF-003 scaffold from commit `9461567f26029fcb4580d83c602908217cbfc1d8` is included. It exactly preserves the published seven weights and tie-preserving ten-body scoring surface once the seven binary factor flags for each candidate body are supplied.

Important limitation: the repository does **not** yet reproduce the exact historical Mastro factor extraction from raw birth data. The source replay records missing software/settings/factor-code details. A prospective study therefore must either obtain those historical conventions or freeze and label a transparent new CF-003 factor reimplementation before opening target responses. Do not describe the current helper as an exact raw-chart reproduction.

## Independent behavioral target

The behavioral classifier sees ten neutral construct IDs/definitions only. It never receives planet names, birth/chart data, predictor scores/ranks, prior chart interpretation, or the evaluator-only construct-to-planet map.

Nine constructs preserve or explicitly extend the existing chart-blind survey role language for recurring drive, repeated communication/thinking, values/boundaries, action/maturation, growth principles, discipline/accountability, unconventionality, mystery/opacity, and transformation/deepening. The new tenth construct is central identity/purpose/self-expression.

Every construct uses the same source-bounded 0–4 centrality/dominance rubric, with null for insufficient evidence. Exact participant-answer quotes are required; absence of mention cannot earn 0; conditions/counterevidence constrain the score; question count, verbosity and model confidence do not add points; ties remain ties.

The evaluator-only mapping is stored separately and is applied only after the ten-construct behavioral target is frozen.

## Secondary survey module

The voice-first collector now knows about a separate three-question CF-003 development module. The main Life Patterns record is frozen first. Then, before any chart reveal, the collector may ask:

1. central identity/purpose/self-expression across life;
2. which recurring patterns are most organizing/central;
3. which recurring patterns are real but peripheral/situational.

Those answers freeze separately as `life-patterns-cf003-secondary-v0.json` and never alter the primary Life Patterns record or score.

The three-question supplement is sufficient only when the existing autobiographical source already covers the nine inherited domains. Missing source stays missing; it is never converted into a low behavioral score merely because a construct was not asked often enough.

## Two-stage blind workflow

1. Build a classifier packet from frozen behavioral source only.
2. Run the classifier in a fresh tool-free context with no repository, web, Memory, connected apps, chart files, predictor files or evaluator mapping.
3. Validate exact source quotations and freeze the ten-construct behavioral target with `prediction_opened=false`.
4. Only after that freeze, load the separately frozen chart-side predictor and evaluator mapping.
5. Compare the two ten-body rankings.

The packet builder rejects obvious chart/target leakage and strips nonbehavioral metadata/quarantined turns. The behavioral-target freezer refuses incomplete ten-way ranking when any construct is null.

## Endpoints

Primary per-person endpoint: mean behavioral midrank of every body tied for the highest CF-003 predictor score. With a unique predictor top this is simply that body's chart-blind behavioral rank. No predictor tie is broken.

Secondary:
- tie-aware Spearman correlation across the complete ten-body rank vectors;
- inclusive top-3 overlap count;
- inclusive top-3 Jaccard overlap.

Group null: apply the same permutation of the ten evaluator labels to every participant behavioral profile and recompute the group statistic. This preserves each participant's behavioral profile and construct-specific marginal distributions; the historical finished-target shuffle is not reused.

## Development versus prospective status

Existing participant records may be used only to debug missingness, target balance, ties, classifier behavior and clarification needs. Any apparent CF-003 signal in those records is exploratory because the target was designed after their responses existed.

Before new prospective target responses, freeze the behavioral contract, classifier prompt/model/version, evaluator mapping, three question wordings, quote/source validation, rank/tie/endpoints, global-permutation count/seed, chart-side predictor convention, and software commit/hashes. Held-out replication remains required.

## Verification

- CF-003 predictor + target + voice-manifest affected checks: 49 PASS.
- Empirical-astrology suite after final manifest refresh: 32 PASS.
- Target implementation/scripts Ruff F/E9/I: PASS.
- One private multi-turn development record was used only to verify packet construction: source remained private, no evaluator mapping entered the packet, and no participant text or content-derived hash is stored in public Git.
- No Venice/OpenRouter calls and no Railway deployment occurred.

Cross-family methodology check: Claude Opus 5.5 max via Claude Code was attempted on a public, redacted method packet. It returned no verdict after more than 15 minutes and was stopped. No same-family substitute was used. Therefore this module remains DEVELOPMENT/SECONDARY and is **not** called prospectively frozen. See `tasks/cf003-secondary-module-20260929/CROSS-FAMILY-CHECK.md`.

## Previous Railway state

The parent voice/Railway work remains unchanged: the optimized Railway participant service is a dark preview with inference disabled and no participant gateway credential. This CF-003 task did not deploy or activate it.

Historical owner-method correction remains in force: there was never a completion policy requiring predetermined question coverage. The survey bank remains a menu, not a quota.
