# Current state

- As of: `2026-08-30 01:09 GMT`
- Task ID: `astrohd-relationship-continuation-20260830`
- Goal: continue the relationship/AstroHD program under the blocking Brave + ChatGPT Pro supervision contract in `docs/RELATIONSHIP_RESEARCH_HANDOFF.md`, beginning with the separate natal-first `Find my birth-time window` priority unless supervision changes the sequence.
- Authoritative Git baseline: `main` and `origin/main` at `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` (`Add canonical relationship research handoff and Pro supervision protocol`).
- Active branch: `codex/astrohd-relationship-continuation`, created directly from that baseline. The worktree was clean at branch creation.
- Rollback point for the local `main` refresh: prior commit `450d806efe66e8299f5d43dd046685e8415b9a30`; the fast-forward remains reachable through Git history/reflog.

## Fresh audit

- GitHub repository `u-dont-existDOTcom/humandesign` is public and uses `main` as its default branch. Exact-head `b7660b8` CI run `33283895301` passed. The other triggered workflows skipped because the handoff-only commit did not affect their paths.
- PRs `#16` (Survey-v2 empirical robustness) and `#17` (relationship email recovery) are merged. One old draft PR, `#1` (`codex/harness-integration`), remains open and failed its last 2026-08-25 CI run; it is not authoritative for this task.
- Hosted governance gap: GitHub reports no repository rulesets and `main` is not branch-protected. Continue to use a task branch/PR and exact-head verification despite the absent hosted enforcement.
- Railway project `humandesign-relationship`, production service `relationship-web`, is healthy. Latest successful deployment `60c360b2-6591-4e96-9d82-66e6808f82e5` runs code commit `450d806` (the newer Git commit is documentation only), one `ams` replica, the confirmatory launch command, `/healthz`, and a persistent `/data` volume.
- Direct runtime checks passed: `/healthz` returned `{"status":"ok"}`; `/api/llm-status` reported configured direct OpenAI `gpt-5.6-sol`; `/api/study/recovery/status` reported configured magic-link and six-digit-OTP recovery.
- Railway exposes the expected service domain and variable names without values. `OPENROUTER_API_KEY` is still provisioned even though the active code path is direct OpenAI. Do not remove it until active-path and rollback dependency checks prove it unused. Preserve all existing secrets and the `/data` volume.
- Live UI inspection confirmed the exact-time Relationship Pattern Lab intake, participant-confirmed birthplace search, privacy disclosures, three consent gates, email recovery, and pre-answer sealing language. No participant record was created or modified during the audit.

## Scientific/implementation status

- Complete: deterministic exact-time HD connection mechanics; strict Swiss-backed Western geometry; frozen AstroRRF V0.1 raw directional scoring plus V0.2-V0.4 feature-family flags; chart-blind GPT-5.6 Sol answer audit and phenotype classifier; pre-answer relationship freeze; immutable response/phenotype reveal flow; secure email recovery.
- Survey-v2 status: `state/SURVEY-V2-NOISE-AUDIT.json` covers the complete `288938`-state universe and all 12 declared synthetic scenarios with reference equivalence. Its claim scope is synthetic oracle robustness only. It does not calibrate human classifier reliability, AstroRRF outcomes, or birth-time probabilities.
- Partial: `src/hdmatch/relationship/uncertain_time.py` aggregates already-enumerated partner-time intervals into stable and variable connection mechanics. It does not enumerate a civil day, collect natal behavioral evidence, rank natal states, or propagate a ranked distribution through the public relationship flow.
- Not implemented: separate natal-first `Find my birth-time window` participant mode; independent remembered-weekday capture and date-conflict handling; exact full-day state enumeration in that mode; reliability-aware natal questionnaire/audit/freeze; uncalibrated rank/mass output over windows; display of feature variation; or downstream relationship prediction marginalized over that distribution.
- Not implemented: separately versioned AstroRRF raw-signal-to-ordinal outcome calibration; calibration/validation cohort workflow; or the public-safe outcome ledger required for durable model comparison.

## Privacy, blinding, and leakage boundaries

- Private email, exact birth data, raw narratives, resume/recovery credentials, and classifier evidence remain on Railway/private storage. Public Git may receive only code, schemas, non-enumerable commitments, deidentified aggregates, and public-safe model/calibration artifacts.
- Do not use relationship evidence to infer natal time in the default workflow. Any future relationship-assisted rectification is exploratory and disqualifies that same relationship as validation evidence for the inferred chart/time.
- Do not convert raw symbolic/rubric scores into probabilities or high/low outcome labels without a separately frozen, supervised calibration layer.
- `.gitignore` currently lacks several private-artifact classes required by `docs/34_relationship_participant_data_storage.md`; harden it during the first implementation slice without deleting existing data.

## Supervision and verification

- Required supervisor surface: one authenticated ChatGPT Pro conversation in Brave, reused throughout this task. The existing `Romance Blind Reader Test` chat is a frozen-reader experiment and must remain unchanged; start one dedicated supervision conversation.
- First mandatory checkpoint: send Pro this audit and the exact implementation choice before scientific implementation. Recommended first slice: natal-first intake + source/weekday conflict semantics + exact state enumeration + immutable freeze/result schemas, while keeping ranking weights/probability semantics explicitly unresolved until a later supervised checkpoint.
- If Pro says an owner decision is required, stop. Otherwise apply its guidance automatically and write the decision back here before continuing.
- Test-efficiency telemetry is active under task ID `astrohd-relationship-20260830` in `.git/codex-test-efficiency/`.
- Before merge/deploy: exact-head focused/full tests, Ruff, strict mypy, participant JavaScript syntax checks if UI changes, privacy/blinding review, pre-merge Pro checkpoint, pre-deploy Pro checkpoint, exact-commit deployment, and production smoke verification.

## Next safe action

Post the compact fresh-audit packet to the dedicated Brave ChatGPT Pro supervisor and wait for the complete response. Do not select or implement scientific birth-time ranking/calibration semantics while that checkpoint is pending.
