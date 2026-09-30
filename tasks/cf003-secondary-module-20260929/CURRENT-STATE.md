# Current state — CF-003 independent behavioral dominance secondary module

Updated 2026-09-30. Branch: `chat/cf003-secondary-module-20260929`.

## Owner outcome

A separate CF-003 DEVELOPMENT/SECONDARY module is implemented without changing TN-001, LiteratureModelV1, the main Life Patterns score, or the dark Railway participant deployment.

The experiment keeps the published CF-003 seven-factor planetary-dominance score surface on the chart side and replaces the historical chart-conditioned biographical target with an independently frozen chart-blind behavioral target.

## Predictor status

The source-replayed CF-003 scaffold preserves the published seven weights once seven binary factor flags are supplied for each of the ten candidate bodies. A dedicated `cf003-predictor-scores-v0` artifact now freezes those scores and its SHA-256 before behavioral classification.

Important limitation: exact historical Mastro extraction of the seven factor flags from raw birth data is still unresolved. Prospective use therefore requires either the missing historical conventions or a separately frozen, transparently labeled new extraction convention.

Predictor ranking is quantized to the published 0.1-point grid before tie handling so mathematically equal published scores are not split by floating-point summation order.

## Independent behavioral target

The classifier sees only ten neutral construct IDs/definitions plus sanitized behavioral source. It never receives planet names, birth/chart data, predictor values/ranks, prior chart interpretation, evaluator mapping, astrology/Human Design labels, repository access, web, Memory, connected apps, or other participant context.

Nine constructs preserve explicit lineage to existing chart-blind Human Design survey roles and the tenth is a development self-expression/purpose proxy. This is therefore a **combined development hypothesis**, not a reconstruction of the authors' unavailable historical CF-003 target semantics. The literature review may replace the mapping only in a new version before prospective freeze.

All constructs use the same source-bounded 0–4 dominance rubric with null for insufficient evidence. Exact quotes must be at least four words; ratings 3–4 require at least two distinct support quotes; rating 0 requires explicit counterevidence; quote reuse across constructs is reported; conditions and counterevidence remain attached; ties remain ties.

## Secondary survey module

After the main behavioral record is frozen, but before any chart/predictor reveal, the development module may ask three concealed-direction coverage probes:

1. broad continuity/change across life;
2. recurring patterns that most shape choices, priorities, or action across settings;
3. recurring patterns that are real but peripheral or situational.

These are not a complete ten-construct battery. A secondary record must be cryptographically linked to the exact primary record. Missing construct evidence stays missing; no improvised construct-targeted follow-up is allowed until a balanced follow-up battery is separately specified and frozen.

Post-freeze metadata may record prior chart familiarity and whether ChatGPT Memory was enabled, but that metadata never enters the classifier.

## Blind workflow and provenance

1. Freeze the chart-side predictor artifact and its SHA-256 under an explicit factor-extraction convention.
2. Build a classifier packet from frozen behavioral source only. The builder fails closed on profile/chart/predictor fields, scans classifier-facing strings for external-profile leakage, requires explicit behavioral turn roles, honors exposure flags, and requires exact primary/secondary linkage.
3. Run the classifier in a fresh tool-free context using only that packet.
4. Validate source evidence and freeze the behavioral target while recording classifier model/version, raw classifier-output hash, manifest/mapping hashes, and the preclassification predictor commitment hash.
5. Compare only against the exact committed `cf003-predictor-scores-v0` artifact.

## Endpoints and null

Primary per person: mean behavioral midrank of every body tied for the highest CF-003 predictor score. With a unique predictor top, this is simply that predicted body's behavioral rank.

Secondary:
- tie-aware Spearman correlation across all ten ranks;
- fractional top-3 overlap;
- fractional top-3 Jaccard, with tied boundary labels sharing the remaining slot mass rather than expanding the top-3 set.

Inferential group null: keep each chart predictor and the evaluator mapping fixed, then reassign complete frozen behavioral profiles among participants **within preregistered birth-cohort strata**. Freeze strata, Monte Carlo seed, and permutation count before prospective target collection.

The old global construct-label permutation is diagnostic only. Opus's calibration simulation showed it can be materially miscalibrated under unequal predictor/behavioral marginals; it must not be used for CF-003 inferential p-values.

## Cross-family methodology review

Claude Opus 5.5 max via Claude Code completed the methodology review in session `a6e2eee0-204b-407a-a751-8b03dee3db73` with verdict **FINDS_ERROR**.

The reviewer was initially still `busy/working` after the earlier wrapper wait; liveness/log inspection showed active analysis, so it was left running. It later completed and identified seven defect families covering the null, leakage/provenance, construct/elicitation balance, quote validation, freeze ordering/provenance, tie/float behavior, and the scope of the behavioral meanings.

Those defect families are repaired and regression-tested. The reviewer probes are preserved under `tasks/cf003-secondary-module-20260929/reviewer-artifacts/`; null calibration is recorded in `NULL-CALIBRATION-20260929.md`.

## Development versus prospective status

Existing participant records may be used only for exploratory target diagnostics such as construct missingness, rating spread, quote reuse, ties, classifier behavior, and clarification burden. Any CF-003 association on those same records is exploratory.

The module is **not prospectively frozen**. Before a new prospective CF-003 target cohort, resolve and freeze:
- chart-factor extraction convention;
- classifier model/version;
- balanced source-coverage/follow-up rule;
- literature-derived evaluator mapping decision;
- birth-cohort permutation strata;
- permutation seed/count;
- final software commit/hashes.

Held-out replication remains required.

## Verification

The integrated CF-003 branch, rebased onto the repaired voice parent and its processed suggested-fix lane, now passes:
- combined CF-003 + interviewer-accuracy + voice focused checks: 68 passed;
- full repository: 1005 passed / 6 skipped (only absent production Swiss Ephemeris files);
- exact hosted-CI Ruff command: PASS;
- mypy: PASS across 220 source files;
- git diff check: PASS;
- CF-003 manifest/hash checks: PASS through focused/combined tests;
- Life Patterns voice instructions: 7960 / 8000 strict count;
- participant interviewer instructions: 7768 / 8000 strict count;
- legacy reverse matcher: 8000 / 8000 strict count;
- no paid API inference;
- no Railway deployment/change.

The earlier parent-branch Ruff/mypy baseline debt is resolved: the CI-baseline repair merged through PR #47, and the owner-requested interviewer-accuracy suggestion from the new UDA suggested-fix lane was adapted, recorded in docs/suggested-fixes-ledger.md, and merged through PR #48. The remaining failure of the generic scripts/task_acceptance.py is an unrelated legacy task binding: it still expects the old known_month_oracle_1000 artifacts and a worktree-local virtual environment, so it is not used as evidence that this CF-003 development module is incomplete.

This remains a DEVELOPMENT/SECONDARY scientific module, not a prospective freeze.

## Previous Railway state

The parent voice/Railway work remains unchanged: the optimized Railway participant service is a dark preview with inference disabled and no participant gateway credential. This CF-003 task did not deploy or activate it.

Historical owner-method correction remains in force: there was never a completion policy requiring predetermined question coverage. The survey bank remains a menu, not a quota.
