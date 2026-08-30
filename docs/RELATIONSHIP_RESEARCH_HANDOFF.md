# Relationship / AstroHD research handoff

Status: canonical continuation instructions for Codex/worker execution. GitHub and Railway remain canonical; this file is an orientation and supervision contract, not a substitute for fresh inspection.

Snapshot when this file was created: `main` was `450d806efe66e8299f5d43dd046685e8415b9a30`. Do not assume that SHA is still current.

## Mandatory start procedure

Before substantive work:

1. Read fresh `AGENTS.md`, `CURRENT_PLAN.md`, this file, and the current relationship/AstroHD docs and state artifacts relevant to the task.
2. Resolve current `main`, recent related branches/commits, merged/open PRs, exact CI status, and effective Railway `relationship-web` deployment/configuration.
3. Inspect current runtime behavior instead of trusting old chat claims.
4. Preserve private participant data and the mounted Railway `/data` volume.
5. Return a concise audit: actually complete, partially complete, not implemented, regressions/leakage risks, and next action.

## Pro supervision protocol — blocking

The implementation worker must use **Brave** to open or reuse one authenticated **ChatGPT Pro** conversation for project supervision.

- Reuse the same Brave tab and same Pro supervision conversation throughout the work when possible.
- Do not open a new Pro conversation for every checkpoint unless the previous conversation is unusable.
- At every supervision point below, post a compact packet containing: canonical repo/runtime state, the exact decision/question, relevant evidence, realistic options, the worker's recommendation, and scientific/operational risks.
- Then **wait for the complete Pro response before continuing substantive work**. Do not keep coding, merging, deploying, or making the supervised decision while waiting.
- If the Pro response says, in substance, **wait for owner decision / owner choice required / ask owner before proceeding**, stop and wait for the owner. Do not pick an option, merge, deploy, or work around the decision.
- If Pro does **not** require an owner decision, continue automatically using the Pro guidance and the repository rules. No additional owner approval is required merely because a supervision checkpoint occurred.
- Explicit owner instructions always outrank Pro advice. Pro supervision cannot authorize violating privacy, blinding, frozen-model, safety, or repository rules.
- If Brave cannot reach an authenticated Pro session, treat that as a supervision blocker at the next required checkpoint; do not silently substitute another model/account.

### Required supervision points

Use Pro supervision at minimum:

1. **After the fresh audit, before selecting or changing the scientific implementation plan.**
2. **Before defining or materially changing a scientific mapping, calibration target, scoring rule, cohort rule, stopping rule, or evidence interpretation.** This includes AstroRRF raw-score-to-outcome calibration and AstroHD birth-time inference semantics.
3. **Whenever a test/result creates two or more scientifically different valid fixes** rather than a purely mechanical bug fix.
4. **Before any change that could introduce circularity, outcome leakage, post-hoc rescue, cohort contamination, or use of relationship evidence to infer a birth time.**
5. **Before merging a substantive scientific PR into `main`.**
6. **Before production deployment of substantive participant-facing/scientific behavior.** Supply exact-head CI, diff summary, migration/data effects, and rollback boundary.
7. **When the worker believes an owner preference is genuinely needed.** Ask Pro first. If Pro says owner decision is needed, wait for owner; otherwise continue.

Purely mechanical edits that do not alter scientific meaning, privacy, participant behavior, auth semantics, or deployment can proceed between checkpoints, but the worker must not use that exception to split a substantive decision into many small edits.

## Current intended relationship-study architecture

For exact-time confirmatory cases:

1. collect private participant contact + both birth records and source quality;
2. resolve participant-confirmed birthplace/coordinates/timezone;
3. calculate and freeze required HD + Western/AstroRRF prediction layers **before Question 1**;
4. questionnaire/LLM auditor receives no birth data, charts, candidate identity, or hidden predictions;
5. collect structured relationship phenotype with direct OpenAI GPT-5.6 Sol chart-blind answer-quality and bounded clarification;
6. freeze responses/clarifications;
7. separate chart-blind phenotype classifier freezes relationship axes with evidence grounded in verbatim participant text;
8. reveal only the prediction package frozen before behavioral evidence.

No overall compatibility/soulmate scalar. Unknown or poorly observed states remain unknown.

Private data (email, exact birth data, raw narratives, private credentials) stays on Railway/private storage. Public GitHub receives only code, schemas, hashes, public-safe deidentified aggregates, and non-identifying calibration/model artifacts.

## Survey-v2 / AstroHD reliability boundary

The merged Survey-v2 robustness work is synthetic oracle/recoverability evidence. It may inform questionnaire reliability, redundant probes, classifier agreement, retry/corroboration, and stopping behavior.

It **does not calibrate AstroRRF relationship outcomes** and is not evidence of human accuracy.

Reuse the canonical Survey-v2 architecture rather than building a parallel questionnaire system.

## Priority 1 — Find my birth-time window

Build/continue a separate natal-first AstroHD mode for participants with known date/place but unknown time.

- Ask source quality for DOB and remembered birth information.
- Ask remembered weekday independently, with `I don't know`, before showing the weekday implied by the date.
- Never auto-correct DOB from weekday memory.
- Documentary date outranks memory. If date and weekday are both memory-based and conflict, mark `birth_date_uncertain` and evaluate declared nearby-date uncertainty separately if appropriate.
- Enumerate exact stable chart-state intervals across the civil day; do not use noon, hourly sampling, or fake minute precision.
- Improve the participant questionnaire using lessons from the relationship survey: one substantive construct per control, explicit mixed/context-dependent/unknown/not-applicable, direct GPT-5.6 Sol semantic quality, bounded contextual clarifications, progress, verbatim preservation, and reliability-aware redundant probes without adding structural bits.
- Rank intervals/states and return a probability/rank distribution over windows, not a fabricated exact minute.
- Show which chart features vary across likely windows.

Default scientific workflow: infer birth-time distribution from **natal AstroHD evidence first**, then use that distribution in relationship prediction.

If relationship evidence is optionally used for rectification, label it exploratory and make that same relationship ineligible as validation evidence for the inferred chart/time.

Relationship prediction with unknown time should propagate the ranked chart-state distribution and distinguish stable, probability-weighted, time-sensitive, and unresolved predictions rather than silently choosing one best time.

## Priority 2 — AstroRRF outcome calibration

Raw AstroRRF scores/features are not calibrated ordinal relationship predictions. Do not invent thresholds after seeing outcomes.

Build a separately versioned calibration layer that maps frozen raw AstroRRF signals to frozen relationship phenotype outcomes. Prefer probabilistic/ordinal output such as `P(very_low..very_high)` per mapped axis/direction, with appropriate regularization/partial pooling and uncertainty when N is small.

Keep separate:

1. frozen raw AstroRRF model/features;
2. calibration model;
3. validation results.

Existing development relationships helped construct AstroRRF and therefore cannot supply unbiased headline calibration/validation. They may be used for implementation diagnostics only.

Use explicit cohort roles: development, calibration, validation. Freeze the calibrator before untouched validation cases are revealed. Unmapped axes remain `not_predicted`.

The old `actor_eros_passion` construct predates the later split among physical attraction, partner-specific sexual desire, and Eros/in-love. Determine any mapping on calibration data, then freeze it before held-out validation; do not map it to all three by assumption.

## Priority 3 — public-safe outcome ledger

Create/maintain a deidentified durable comparison ledger suitable for calibration and validation statistics without raw narratives or identifying birth/contact data. It should retain model/calibration versions, freeze receipts, axis/direction, predicted distribution, observed ordinal/status, classifier confidence, context/observability, comparison status, cohort role, and learning eligibility.

Continuous evidence accumulation is allowed. Continuous silent mutation of the active model is not. Use explicit V-next proposals and held-out evaluation.

## Email recovery

Secure magic-link/OTP recovery has been merged. SMTP credentials and participant email remain private; never commit secrets or participant contact information. Verify live SMTP round-trip only with an authorized test session and without exposing secrets. Browser-token fallback remains until email recovery is proven operational.

## Relationship phenotype separation

Do not collapse directional attraction, physical attraction, partner-specific desire, baseline libido, initiation, satisfaction, dyadic chemistry, familiarity/habituation, novelty dependence, Eros, love/attachment, Storge, commitment, intimacy, readability, responsiveness, intellectual compatibility, intellectual stimulation, comprehension/application, communication quality, communication abundance, shared interests, knowledge complementarity, mystical salience/curiosity/stimulation, theatrical drama, serious conflict/aggression, repair difficulty, internal ease, autonomy, engulfment, sexual jealousy, romantic-priority jealousy, proximity sensitivity, trust, care/support, and practical-life fit.

## Engineering/deployment gates

Before merge/deploy of substantive work:

- fresh `main`/branch conflict check;
- exact-head tests;
- Ruff;
- strict mypy;
- participant JS syntax check if UI changed;
- confirm privacy/blinding invariants;
- Pro supervision checkpoint and wait for response;
- if Pro says owner decision required, stop and wait;
- otherwise continue;
- preserve Railway secrets and `/data` volume;
- deploy exact commit only;
- verify effective start command, healthcheck, expected public UI/endpoints, and safe smoke tests.

## Cleanup boundaries

Do not bulk-delete participant records. Synthetic cleanup is allowed only for records conclusively identified as synthetic test records with no real participant evidence. Legacy OpenRouter residue may be removed only after proving it is unused by the active direct-OpenAI path.
