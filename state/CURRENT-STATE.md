# Current state

- As of: `2026-08-30 01:54 GMT`
- Task ID: `astrohd-relationship-continuation-20260830`
- Goal: continue the relationship/AstroHD program under the blocking Brave + ChatGPT Pro supervision contract in `docs/RELATIONSHIP_RESEARCH_HANDOFF.md`, beginning with the separate natal-first `Find my birth-time window` priority unless supervision changes the sequence.
- Authoritative Git baseline: `main` and `origin/main` at `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` (`Add canonical relationship research handoff and Pro supervision protocol`).
- Active branch: `codex/astrohd-relationship-continuation`, created directly from that baseline. The worktree was clean at branch creation.
- Rollback point for the local `main` refresh: prior commit `450d806efe66e8299f5d43dd046685e8415b9a30`; the fast-forward remains reachable through Git history/reflog.

## Fresh audit

- GitHub repository `u-dont-existDOTcom/humandesign` is public and uses `main` as its default branch. Exact-head `b7660b8` CI run `33283895301` passed. The other triggered workflows skipped because the handoff-only commit did not affect their paths.
- PRs `#16` (Survey-v2 empirical robustness) and `#17` (relationship email recovery) are merged. One old draft PR, `#1` (`codex/harness-integration`), remains open and failed its last 2026-08-25 CI run. A fresh diff audit found it at `3bab2c58`, conflicting/dirty against `main`, with 215 changed files (`+56030/-494`) and broad historical harness/cache/model work. It is not authoritative or safely reusable for this bounded foundation branch; it remains untouched pending owner authority.
- Hosted governance gap: GitHub reports no repository rulesets and `main` is not branch-protected. Continue to use a task branch/PR and exact-head verification despite the absent hosted enforcement.
- Railway project `humandesign-relationship`, production service `relationship-web`, is healthy. The checkpoint-2 re-audit confirmed the same latest successful deployment `60c360b2-6591-4e96-9d82-66e6808f82e5` at code commit `450d806` (the newer Git commit is documentation only), one `ams` replica, the confirmatory launch command, `/healthz`, and a persistent `/data` volume.
- Direct runtime checks passed: `/healthz` returned `{"status":"ok"}`; `/api/llm-status` reported configured direct OpenAI `gpt-5.6-sol`; `/api/study/recovery/status` reported configured magic-link and six-digit-OTP recovery.
- Railway exposes the expected service domain and variable names without values. `OPENROUTER_API_KEY` is still provisioned even though the active code path is direct OpenAI. Do not remove it until active-path and rollback dependency checks prove it unused. Preserve all existing secrets and the `/data` volume.
- Live UI inspection confirmed the exact-time Relationship Pattern Lab intake, participant-confirmed birthplace search, privacy disclosures, three consent gates, email recovery, and pre-answer sealing language. No participant record was created or modified during the audit.

## Scientific/implementation status

- Complete: deterministic exact-time HD connection mechanics; strict Swiss-backed Western geometry; frozen AstroRRF V0.1 raw directional scoring plus V0.2-V0.4 feature-family flags; chart-blind GPT-5.6 Sol answer audit and phenotype classifier; pre-answer relationship freeze; immutable response/phenotype reveal flow; secure email recovery.
- Survey-v2 status: `state/SURVEY-V2-NOISE-AUDIT.json` covers the complete `288938`-state universe and all 12 declared synthetic scenarios with reference equivalence. Its claim scope is synthetic oracle robustness only. It does not calibrate human classifier reliability, AstroRRF outcomes, or birth-time probabilities.
- Partial: `src/hdmatch/relationship/uncertain_time.py` aggregates already-enumerated partner-time intervals into stable and variable connection mechanics. It does not enumerate a civil day, collect natal behavioral evidence, rank natal states, or propagate a ranked distribution through the public relationship flow.
- Implemented on the non-production task branch at `592ff22fd914614a73e4c72861aa3c6514a796f4`: the Pro-approved deterministic natal-first foundation. It includes immutable evidence lineages, a server-enforced independent weekday lock, fail-closed date conflict states, explicit unordered candidate-date sets, a standalone natal-only API/private storage namespace, complete civil-day interval enumeration, full-state identity/provenance, immutable manifest/freeze/result records, stable/variable set facts, and a synthetic-only public allowlist boundary.
- Candidate-complete edge fixtures now cover ordinary/leap days, DST gap/fold days, a historical offset change, skipped-date failure, day-boundary transitions, multiple candidate dates, and reduced-signature collisions. The canonical synthetic receipt is `state/NATAL-TIME-FOUNDATION-AUDIT.json`, generated from implementation commit `592ff22`.
- The standalone API now also supports injected clocks and identifier factories solely for deterministic audit fixtures while retaining secure random/time defaults. `state/NATAL-TIME-WEEKDAY-LOCK-TRACE.json`, generated from implementation commit `3337b46`, records the synthetic intake and post-lock assessment responses and proves that the asserted date and implied weekday are absent from the first response.
- Still not implemented and explicitly blocked until checkpoint 2: reliability-aware natal questionnaire semantics, candidate ranking/elimination, weights/priors, score or duration mass, probability/confidence labels, stopping rules, participant-facing time-window recommendations, or downstream relationship marginalization.
- Not implemented: separately versioned AstroRRF raw-signal-to-ordinal outcome calibration; calibration/validation cohort workflow; or the public-safe outcome ledger required for durable model comparison.

## Privacy, blinding, and leakage boundaries

- Private email, exact birth data, raw narratives, resume/recovery credentials, and classifier evidence remain on Railway/private storage. Public Git may receive only code, schemas, non-enumerable commitments, deidentified aggregates, and public-safe model/calibration artifacts.
- Do not use relationship evidence to infer natal time in the default workflow. Any future relationship-assisted rectification is exploratory and disqualifies that same relationship as validation evidence for the inferred chart/time.
- Do not convert raw symbolic/rubric scores into probabilities or high/low outcome labels without a separately frozen, supervised calibration layer.
- `.gitignore`, `.dockerignore`, CI, and `scripts/check_private_artifacts.py` now enforce private-path, staged/tracked secret, build-context, branch-diff, and reachable-history checks without deleting existing data.

## Supervision and verification

- Required supervisor surface: one authenticated ChatGPT Pro conversation in Brave, reused throughout this task. The existing `Romance Blind Reader Test` chat is a frozen-reader experiment and remains unchanged. The dedicated supervision conversation was created and run at Pro power (5/5).
- Checkpoint 1 completed on 2026-08-30. Pro returned `OWNER DECISION REQUIRED: NO` and approved **Option A — foundation only**. The full actionable contract is recorded in `docs/PRO_SUPERVISION_CHECKPOINT_1_20260830.md`.
- Approved now: a separate natal-first intake/evidence state machine, server-enforced independent weekday lock, exact candidate-complete civil-day interval enumeration, immutable manifest/freeze/result records, a synthetic-only public allowlist contract, privacy/build hardening, and focused tests.
- Pro hard-blocked ranking, candidate elimination, weights, priors, duration-normalized mass, probabilities, confidence percentages, stopping rules, time-window recommendations, relationship evidence, production migration, public deployment, and merge to `main` until checkpoint 2.
- Checkpoint 2 completed on 2026-08-30. Pro returned `OWNER DECISION REQUIRED: NO`, provisionally accepted the deterministic architecture, and identified actual-engine conformance as the remaining scientific foundation gate. The actionable contract is `docs/PRO_SUPERVISION_CHECKPOINT_2_20260830.md`.
- Authorized now: identify and pin the canonical repository chart engine, establish its actual temporal resolution, inventory every engine field, certify complete transitions, generate real-engine synthetic edge receipts, add an independent checker and evidence-state matrix, and conduct a documentation-only literature scan from `docs/NATAL_TIME_INDEPENDENT_CONCEPTION_SNAPSHOT_20260830.md`.
- Still prohibited: every inferential or participant-facing semantic, relationship-assisted pruning, live data, public mounting, migration, Railway changes, merge, and deploy. Stop and return to Pro if the canonical engine is ambiguous, cannot be pinned, lacks a defensible complete transition method, or requires a substantive precision/scope choice.
- Browser-control default from the owner: prefer headless operation. When the authenticated headed Brave session is genuinely required, reuse the existing controlled window on a dedicated secondary workspace or secondary physical monitor so it does not steal focus or cover the active screen. Do not repeatedly open and close visible windows.
- Test-efficiency telemetry is active under task ID `astrohd-relationship-20260830` in `.git/codex-test-efficiency/`.
- Foundation verification is green through the current local branch head: the final exact-head full suite passed 261 tests; the focused API/foundation suite passed 33 tests; Ruff passed; strict mypy found no issues across 131 source files; the privacy gate passed; and both canonical synthetic artifacts reproduced byte-for-byte.
- Before merge/deploy: exact-head focused/full tests, Ruff, strict mypy, participant JavaScript syntax checks if UI changes, privacy/blinding review, pre-merge Pro checkpoint, pre-deploy Pro checkpoint, exact-commit deployment, and production smoke verification.

## Next safe action

Audit the repository's actual chart-engine path against the checkpoint-2 contract. If one canonical engine is unambiguous, implement only its deterministic conformance adapter, fixtures, independent checker, field inventory, resolution evidence, and transition matrix; otherwise stop and return to Pro. Do not push without Joel's direct authority, and do not merge, change GitHub governance, modify Railway, touch `OPENROUTER_API_KEY`, or deploy.
