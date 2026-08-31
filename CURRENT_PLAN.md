# Current Research Plan

## Owner coordination directive — 2026-08-31

- Continue routine, safe, in-scope execution autonomously. Do not ask the owner to
  approve obvious implementation steps, choose an execution mode, or reconfirm an
  authority already granted.
- Ask the owner only when a genuine product/scientific/policy tradeoff, an
  irreversible or materially consequential choice, missing authority, or a
  mandatory security boundary requires owner action. When a choice is genuinely
  required, explain the viable options, material benefits and drawbacks,
  consequences for the result, and the recommended option before asking.
- When a service requires the owner to complete a private authentication step,
  state the exact action needed; do not present it as a discretionary project
  decision or restart governance review.

## Active Issue #18 execution state — 2026-08-31

This section supersedes the generic next-action order below. Human Design issue #18
remains the controlling chat-authored supervisor directive. The owner subsequently
authorized the exact PR #20 merge, production deployment, and one owner-only live
questionnaire/recovery test. That authorization superseded the earlier release-closed
checkpoint only for this bounded owner test; first external participants remain out
of scope.

- PR #20 head `7f24ebc9936cb98db7e69a9ffa8dfbe018008a3c` passed required CI and was merged
  to `main` as `b5c2cc57513d4b5505fd23a8e4c605e4607c11b9`.
- Railway production deployment `0c26073a-ff83-449b-a976-7ae4342d7e00` is `SUCCESS`
  and is bound to that exact merge commit on `main`.
- Railway GitHub App access is restricted to this repository, the production source
  is `main`, and automatic deployment on GitHub push is enabled.
- Railway's retired Amsterdam region identifier was replaced by the current
  `EU West (Amsterdam, Netherlands)` identifier. The geography did not change.
  The mounted private volume's file count, total bytes, and aggregate digest matched
  exactly before and after migration; raw records and the private digest were not
  copied into Git.
- Public `/healthz` returns `{"status":"ok"}`. Recovery status reports both
  `magic_link` and `six_digit_otp`. The live questionnaire exposes explicit
  hour/minute/optional-second controls for both people and no native browser time
  controls.
- One authorized recovery request for the owner's address returned the deliberately
  generic `202` response. A privacy-safe private check found no saved study associated
  with that address, so no email was sent. This is correct anti-enumeration behavior,
  not an SMTP failure. A complete email/OTP round trip requires the owner first to
  create a study using that address.
- No friend has been contacted and no new scientific result exists. Incremental paid
  spending remains `$0`.

Adequacy states:

- **Operational alignment:** `PASS` for deployment, persistence, live repaired time
  intake, and recovery configuration; `PENDING_OWNER_SESSION` for a real email/OTP
  round trip because no eligible owner study exists yet.
- **Scientific adequacy:** `NOT_ESTABLISHED`; the deployment and owner usability smoke
  are not evidence that AstroHD or AstroRRF predicts humans.
- **Release adequacy:** `OPEN_OWNER_ONLY`; the questionnaire is ready for the owner's
  fresh test. External participant sharing remains closed until that smoke completes.

The owner subsequently corrected the test order: natal AstroHD must be tested before
AstroRRF because relationship predictions depend on two natal layers. The relationship
questionnaire remains a secondary development mode and no arbitrary response count is
required before showing its frozen raw predictions. Neither runtime currently retrains
automatically from a submission.

Current continuation branch `codex/issue18-release-receipt` and draft PR `#21` now
contain the relationship `[object Object]` validation-message repair plus an
AstroHD-first owner route. The local real-engine/browser smoke creates a sealed natal
session in about 8.6 seconds from an exact hash-pinned century-cache month slice.
Details and scientific boundaries are in `docs/36_astrohd_owner_pilot.md`.

The first exact-diff Extra High review required changes. The local repair set now
requires a distinct high-entropy session token in addition to the opaque session ID,
keeps exact birth/chart data out of the external interviewer responses, records exact
OpenAI consent, rejects owner-pilot mode/scope changes, fails closed if the active
source/model/mapping/question-bank/engine differs from the frozen session, preserves
legacy reveal readability, and uses private filesystem modes.

Next: verify this repair set and route its new exact head/diff back to Extra High;
privately transfer the verified 28 MB cache into the Railway volume and prove its
hashes plus restart persistence; configure the private/unlisted Custom GPT and its
model receipt; then deploy and smoke only the bounded owner test. Do not publish the
cache artifact. External participant sharing remains closed until the owner completes
that smoke.

## Core hypothesis

Human Design can be tested as an information-recovery problem: if birth-derived chart structure predicts sufficiently specific behavior, a blinded behavioral questionnaire should rank the person's true concealed birth state above alternatives.

This repository separates four claims:

1. **Engineering recoverability** — can a decoder recover a hidden chart/date/time from synthetic answers generated by the same frozen HD model?
2. **Human descriptive specificity** — do real human responses carry out-of-sample information about their true birth-derived HD chart/date/time?
3. **Responder heterogeneity** — is the signal concentrated in a reproducible subgroup rather than the whole population?
4. **Somatic usability** — separately, does Strategy/Authority improve prospective decisions, and is usability moderated by trauma/dissociation/body access?

These claims must not be conflated.

## Current implementation priority

Before expanding validation, migrate the existing V4.1/V3.2 implementation to the hardened **V4.3/V3.5** contract.

Required migration gates:

- full required feature registry for all frozen mappings;
- flexibility penalty;
- dependency/corroboration controls;
- duration-weighted conditional prevalence;
- exact V4.3 rank tuple;
- full-universe rerun after accepted refinements;
- anti-simplification tests;
- verified reusable century cache.

A reduced architecture-only implementation must never identify itself as V4.3.

## Immediate proof-of-concept ladder

### Stage A — Known month + year
Ask for birth month, year, and birthplace/timezone only. Conceal day and time.

Search every exact chart-state interval intersecting every local day in that month. Rank all local dates using the frozen behavioral model.

Primary outcome: true local birth-day rank among 28–31 dates.

See `docs/14_month_first_blind_validation.md`.

### Stage B — Known year
Conceal month/day/time and rank the full year.

Primary outcome: true day-of-year rank among 365/366 days.

### Stage C — Known date, hidden time
Search exact state intervals across the 24-hour day.

Primary outcome: whether the true documented birth time lies inside the top-ranked stable interval.

### Stage D — Joint date + time
Known year, hidden date/time.

### Stage E — Broad multi-year / 100-year UTC search
Use the verified precomputed century cache. Do not rebuild the century per participant.

Initial cache horizon:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

## Exact-state search rule

Do not represent a day by noon, midnight, hourly samples, or a single best minute.

Enumerate all scoring-relevant chart boundaries and partition candidate time into stable state intervals. Report a minute only when the model actually discriminates at that scale. Otherwise report the full tied interval.

For date ranking, support duration-weighted integration across all intervals within the local day. Do not let a five-minute lucky peak dominate an otherwise poor day without an explicitly justified aggregation rule.

## Precomputed universe rule

Astronomy is target-independent. Build exact candidate states once, verify them, then reuse them.

The cache must include sufficient M0-M2 feature data for every frozen V4.3 predicate, exact interval boundaries, Design timestamps, engine/ephemeris provenance, and a cryptographic manifest.

Cache incompatibility is an error, not a reason to silently regenerate with a weaker engine.

## Adaptive questionnaire

The questionnaire begins with broad, behavior-first questions and then adapts to the remaining candidate set.

At each iteration:

1. rescore the entire candidate universe;
2. inspect which unanswered dependency cluster would best discriminate the current candidates;
3. ask a neutral question whose scoring key was frozen before seeing the participant's hidden date;
4. request concrete examples/counterexamples;
5. update all candidates uniformly;
6. continue until a predeclared stopping rule is reached.

Do not show the participant the live ranking before the result is frozen in confirmatory work.

## Synthetic validation first

Synthetic tests use the **same frozen scoring/mapping system as the decoder**.

Pipeline:

```text
hidden birth moment
→ deterministic HD chart
→ frozen HD→behavior model
→ coded questionnaire responses
→ blind decoder
→ ranked date/time prediction
→ prediction freeze
→ answer-key reveal
```

Synthetic success validates the decoder/search/blinding machinery only. It does not validate HD in real humans.

Use oracle, low-noise, medium-noise, and adversarial synthetic tiers.

## Human model development

Post-hoc fitting on known humans is explicitly allowed and encouraged on a DEVELOPMENT set.

Use development humans to:

- refine question wording;
- split conflated constructs;
- learn which questions people can answer reliably;
- learn empirical `P(answer | chart features)` relationships;
- correct weak or wrong traditional mappings;
- optimize adaptive question selection;
- shorten the questionnaire;
- analyze errors.

This is training, not validation.

Post-selection behavioral clarification may improve descriptive validity but must retain revision provenance and must not be relabeled untouched confirmation. Preserve frozen-independent and best-current-descriptive results separately.

After fitting, freeze a model version and test it on untouched humans. If the test motivates another redesign, create a new model version and use a new untouched test set.

## Three decoder tracks

1. **Theory / symbolic** — hardened V4.3 mappings and rubric bits.
2. **Empirical** — learned chart→response likelihoods from development humans.
3. **Hybrid** — theory mappings as priors, updated/shrunk using human data.

The empirical track is important because HD theory may contain real birth-linked signal even if some traditional behavioral descriptions are imperfect.

## Responder heterogeneity

Do not assume every person must show the same correlation strength.

Estimate whether the population contains reproducible classes such as:

- strong chart-correlated responders;
- weak/moderate responders;
- near-chance responders.

Potential moderators must be measured before outcome reveal where possible:

- body-access/reporting reliability;
- dissociative distance;
- hypervigilance/threat amplification;
- fawning/freezing/mental override;
- HD familiarity;
- birth-time documentation quality;
- other predeclared non-HD covariates.

A subgroup is meaningful only if membership or response strength generalizes to new people. Do not define the "good correlators" after seeing who matched and then treat that as confirmation.

## Trauma/body-access rule

Chart resonance and somatic usability are separate hypotheses.

Low body-access reliability may downweight affected Authority/somatic questions. It must never add support to a chart, rescue unrelated contradictions, or be used automatically to dismiss a failed prediction.

## Controls

Human validation must compare against:

- random/permuted chart assignment;
- date prior alone;
- calendar/month/season/cohort baselines;
- demographic baseline if demographics are collected;
- plausible mismatched HD charts;
- symbolic HD;
- empirical HD;
- hybrid HD.

If a date-recovery signal is explained equally well by ordinary calendar/season effects, do not claim HD-specific information.

## Primary human success metrics

- top-1 / top-3 / top-5 accuracy;
- true-date/state rank;
- mean reciprocal rank;
- percentile;
- rank margin;
- holdout stability;
- questions/clusters needed;
- stable interval width for time recovery;
- permutation-test comparison with null;
- subgroup-specific performance only when subgroup rules were predeclared or learned on development data and frozen.

## Authority practical-use warning

Authority is a decision process at its own timescale, not a long-term forecasting oracle.

A correct present signal does not mean a job, relationship, location, treatment, or other commitment will remain beneficial for years. Changed circumstances create new decisions.

Splenic and non-emotional Sacral processes are relatively present-moment; Emotional and Lunar processes require their longer timing. Practical Strategy/Authority experiments should be low-stakes and prospective, and are a separate validation question from birth-chart recovery.
