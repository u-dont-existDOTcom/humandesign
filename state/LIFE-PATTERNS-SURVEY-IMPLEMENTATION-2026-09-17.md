# Approved survey implementation — 2026-09-17

Status: local candidate verified; hosted CI/deployment readback pending. Owner natural-use evaluation is not self-certified.

## Implemented

Phase A: explicit current workflow phase and pending action; revision-bound, single-flight, idempotent mutations; transactional rollback; durable pending response/draft; visible retries; recovery cannot replace a newer live session or silently start over; original checkpoint retained on restore failure; stable pause across late responses/reload; original raw-recovery API retained for already-open old tabs.

Phase B: request-local full practical interview evidence context shared across elicitation, refinement, coverage and admission; final question check after fallback transformations; cross-area no-worthwhile-question outcome leaves coverage incomplete; source-context formulation review distinguishes direct reports, new inferences and unsupported/context-only material. The deployed model/provider is unchanged. Semantic judgments remain fallible and need owner evaluation.

Phase C: consolidated template/client rather than inherited string-replacement layers; one labeled textbox; current-action progress/status; stable pattern collection with sources; append-only correction notes make the prior wording disputed; genuine finish/resume; readable summary, current/previous recovery backups, and self-contained frozen development evidence with non-null blueprint metadata even with zero accepted patterns. Existing v2 scientific semantics and accepted historical adjudications were not rewritten.

Phase D: local verification complete; hosted browser job added so actual UI transitions, rather than merely HTML strings, are exercised in future CI. Short owner evaluation remains the next product evidence boundary after deployment.

## Local verification

- Full suite: **815 passed, 7 skipped**, 10.92 seconds. Skips: four historical-commit checks unavailable in the shallow checkout and three official-ephemeris-file smoke cases. One existing-stack Starlette/httpx deprecation warning; no dependency migration was undertaken for it.
- Focused workflow/API/gate cases: **23 cases**, all included in the final passing full suite.
- Existing affected owner interview checkpoint: **68 passed** before the final five added focused cases; the later full suite includes them all.
- Browser: **13 scenarios passed**, zero page errors, zero model calls. Covers failed restoration/checkpoint preservation, hidden retry, retained failed draft, lost acknowledgement, overlapping sends, pause/late response/reload/resume, historical acceptance vs new question, stable patterns/corrections, inference judgment, bounded stop, zero-pattern export metadata, six-width geometry and reduced motion.
- `ruff check src tests --ignore E501,I001`: PASS, using the repository's current command.
- `mypy src/hdmatch`: PASS, 207 source files.
- `git diff --check`: PASS.
- Canonical Universal test observer: See the test observer receipt for final totals. Full checkpoints were repeated only after the legacy-correction projection fix and the required owner-state prose repair; zero forced unchanged green reruns. Bootstrap/transport preparation is not counted as product improvement.

The isolated local Python setup used the checked-in lock without the unrelated `pyswisseph` build, because the VPS has no compiler/ensurepip. No system packages changed. The official PyPA pip zip application bootstrapped that isolated environment. The hosted CI uses the complete lock, including ephemeris support. Httpx and its previously unpinned dependencies are now explicitly in the development lock for the API tests. Puppeteer is pinned in the browser fixture lock.

## Limits and next boundary

No live model turns, owner-session mutations, birth/chart scoring, independent fresh semantic review or full accessibility conformance certification were performed. The frozen export is an immutable development record, not proof of scientific validity. A saved-pattern correction is represented as a source-bound annotation with current unresolved/disputed status; it does not retroactively turn an old accepted proposal into a newly accepted different proposition.

No new service, authentication policy, provider/model selection, recruitment, public release or merge is part of this work. The existing development prototype may be updated only from the verified candidate. Its hosted verification identities must be recorded before claiming it is live.

Research/tool reuse: existing revision/idempotency patterns, browser form/status semantics, current Design OS and the official Puppeteer request-interception and PyPA installation documentation. No new infrastructure or evaluation framework was made a prerequisite.
