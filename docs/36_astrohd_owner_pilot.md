# AstroHD-first owner pilot

Status: implemented and locally verified on `codex/issue18-release-receipt`; not yet
merged or deployed.

## Why this is the first test

AstroRRF depends on two natal calculations. The owner therefore tests the current
natal AstroHD layer first, before asking friends to complete a relationship study.
The existing relationship study remains available as a secondary development mode;
it is not being discarded or delayed until an arbitrary sample count.

The owner pilot uses an exact recorded birth time. It is not the separate unknown-time
rectification workflow described in the research handoff.

## Participant path

1. The trusted web intake accepts the owner's local birth date, explicit
   hour/minute/optional-second, and a participant-selected birthplace/timezone.
2. A strong single-use access code authorizes exactly one session. Only its SHA-256
   digest is configured; the raw code is never written to the session store.
3. The backend computes and freezes the current chart-derived predictions and exact
   known-month candidate universe before accepting any behavioral answer.
4. The page returns only an opaque `HD-...` session ID to paste into the neutral
   AstroHD Custom GPT interviewer. Birth data is not sent to that GPT.
5. The interviewer appends evidence, locks the confirmatory evidence, and only then
   calls reveal.
6. Reveal returns the frozen chart/prediction comparisons, the true state/date rank
   in the declared candidate set, and a public-safe receipt identifying the exact
   model, mapping, question bank, chart engine, candidate universe, code commit, and
   prediction freeze.

The deployable Custom GPT instruction block is
`reference/custom_gpt/participant_interviewer_instructions_under_8000_v1.md`; the
interview-only Action schema is
`reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml`.

## What is and is not scored

The current natal participant runtime has a complete executable symbolic scoring and
reveal path. It can classify each frozen mapped dimension as supported, partially
supported, contradicted, or insufficiently evidenced and rank the true birth
state/date against the declared known-month universe.

That does **not** mean the scientific scoring/model-development job is finished. The
active model is the limited frozen `V4/V3.2-symbolic-v1` mapping, not the intended
holistic Survey-v2/H1 model and not a validated personality instrument. A successful
synthetic or owner run proves workflow behavior, not Human Design accuracy.

AstroRRF separately has frozen raw directional scores. It does not yet have a frozen
raw-score-to-outcome calibration, defensible high/low thresholds, or formal hit/miss
labels. The participant copy now states that boundary rather than implying the
calibration already exists.

## Learning behavior

Neither natal AstroHD nor AstroRRF retrains automatically after a submission. The
optional development consent permits a case to be considered for a later
deidentified development dataset. Any improvement must be trained offline, evaluated,
versioned, reviewed, and activated only for later sessions. The participant's frozen
result never mutates.

Before model promotion is implemented for simultaneous/public use, the runtime must
also dispatch every in-progress session to its exact frozen model bundle rather than
merely recording hashes from the bundle active at session creation.

## Runtime and integrity boundary

The mounted pilot requires:

```text
HDMATCH_NATAL_PILOT_ENABLED=1
HDMATCH_PARTICIPANT_STORE=<private persistent directory>
HDMATCH_NATAL_PILOT_TOKEN_SHA256=<sha256 of strong single-use owner code>
HDMATCH_PUBLIC_BASE_URL=<HTTPS production origin>
HDMATCH_NATAL_INTERVIEWER_URL=<private/unlisted Custom GPT URL>
HDMATCH_CENTURY_CACHE=<verified extracted century-cache directory>
HDMATCH_CENTURY_MANIFEST_SHA256=154f2a27d4dc1e632a81c13b82b109fe83064cac5fe3673f82303ac6c24deae8
HDMATCH_CENTURY_CANONICAL_ROWS_SHA256=eb58516030f2176d4c136055829a8168ffe33715a35bfe0b4095c83824c88dfa
```

The chart engine must match fingerprint
`09e811ca0fe517975f9718ea7e12b72f66bf3d2509e049bc29f47169adef5397`.
Startup hashes the exact manifest and every compressed shard and fails closed on a
pin, inventory, content, or engine mismatch. A known-month request then parses only
the overlapping shard and clips the exact UTC range.

The verified cache is GitHub Actions artifact `9653492396` from run `33088719809`.
It contains 288,938 structural intervals and no participant data. GitHub's anonymous
artifact endpoint returns `401`, so the production volume still needs a reviewed
artifact-delivery method before deployment.

## Verification receipt

- Local real-cache month slice: 251 exact stable structural states for the synthetic
  January 2000 Europe/London test.
- Real freeze through the owner intake: approximately 8.6 seconds, versus more than
  seven minutes when regenerating irrelevant month boundaries on demand.
- Predictions remained unchanged through confirmatory lock and reveal.
- Browser smoke: AstroHD is the primary landing choice; explicit time controls,
  live OpenStreetMap search, participant-selected timezone, consent, single-use gate,
  real prediction freeze, and opaque session creation all passed with synthetic data.
- The relationship validation formatter no longer renders FastAPI issue objects as
  `[object Object]`.

Adequacy is deliberately split:

- **Operational alignment:** local path passes; production artifact staging and the
  configured interviewer link remain open.
- **Scientific adequacy:** the blind freeze/reveal design is suitable for an owner
  development case; human predictive validity is not established and the mapping is
  incomplete.
- **Release adequacy:** closed for friends and not yet deployed; bounded owner-only
  release awaits exact-diff review and the cache-delivery decision.
