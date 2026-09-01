# AstroHD-first owner pilot

Status: owner-only pilot merged and deployed from main `afc0bb8`; the 2026-09-01
evidence-quality/participant-explanation repair is in progress on
`codex/astrohd-owner-intake-quality-v1`.

## Why this is the first test

AstroRRF depends on two natal calculations. The owner therefore tests the current
natal AstroHD layer first, before asking friends to complete a relationship study.
The existing relationship study remains available as a secondary development mode;
it is not being discarded or delayed until an arbitrary sample count.

The owner pilot uses an exact recorded birth time. It is not the separate unknown-time
rectification workflow described in the research handoff.

The participant page now states the research motivation plainly. This is the
project's first real blinded test of astrology, Human Design, and their proposed
combined use. It arose from Joel's chance one-person finding that the systems appeared
surprisingly informative together only after mismatches were interrogated rather than
explained away. That observation motivates a test; it is not itself validation. The
page also explains why the simpler personality metrics used by the astrology/HD tests
this project compares against are inadequate for the detailed claims under study and
why participants must not rush their answers. A required in-page acknowledgment makes
the time/detail expectation explicit before session creation.

## Participant path

1. The trusted web intake accepts the owner's local birth date, explicit
   hour/minute/optional-second, and a participant-selected birthplace/timezone.
2. A strong single-use access code authorizes exactly one session. Only its SHA-256
   digest is configured; the raw code is never written to the session store.
3. The backend computes and freezes the current chart-derived predictions and exact
   known-month candidate universe before accepting any behavioral answer.
4. The page returns an opaque `HD-...` session ID plus a separate high-entropy
   session token. The token is shown once and only its SHA-256 digest is stored.
   Both values are required for every interview action; a session ID alone grants
   no access.
5. The interviewer appends evidence. A new conforming lock and reveal require a
   server-owned completion policy with owner-explicit authority. That policy is
   currently unresolved, so both operations fail closed.
6. When a policy-bound result is available, the interviewer-facing reveal returns birth-redacted prediction comparisons,
   the true state/date rank in the declared candidate set, and a public-safe receipt
   identifying the exact model, mapping, question bank, chart engine, candidate
   universe, code commit, prediction freeze, and configured interviewer assets.
   Exact birth data and the raw chart remain available only through the same-origin
   trusted result page using the session ID plus token.

The required OpenAI consent names the actual boundary: questionnaire answers and
the birth-redacted comparison may be processed by OpenAI; exact birth data and the
raw chart are not included in the interviewer Action responses.

The two credentials can be copied together with one click. The page explains their
roles: the ID selects the sealed session and the token proves private access. There is
no credential-bearing magic link because URLs leak into history, logs, screenshots,
and forwarded messages. The ChatGPT interviewer link itself contains no credential.
This is separate from the relationship study's email magic-link recovery flow.

The owner invitation code is also explained in place: it exists only because this is
an owner-restricted pilot, authorizes one session, and is not a participant identity.
Ongoing session authorization is now stored separately by opaque session ID, so
rotating the one-use invitation for a new test cannot strand an existing session.
Already-deployed invitation receipts migrate to that layout after successful session
authorization without ever storing the raw token.
The daylight-saving `fold` control is hidden unless the submitted local time actually
occurred twice; if needed, the page explains earlier versus later occurrence in plain
language.

## Interview evidence-quality gate

The first deployed interviewer could advance after fluent but incomplete or random
text, and the server could lock after one scoreable observation. That is not adequate
for the stated study.

The repaired contract now:

- returns each selected question's frozen `minimum_evidence` requirement;
- treats a broad claim as domain-specific until cross-domain examples support a broader
  conclusion (the chess example is the explicit regression case);
- requires the interviewer to check new claims against earlier claims and reconcile
  apparent contradictions by context or life-stage change;
- does not count random, joke-like, off-topic, incoherent, or refused clarification as
  adequate evidence;
- requires each trait/behavior observation to carry a minimum-evidence decision,
  consistency status, and evidence-specific quality rationale;
- keeps legacy/unreceipted observations readable but never silently migrates them into
  the repaired scoring protocol;
- removes client-authored cluster IDs and binds an eligible `question_id` only to its
  unique server-owned dimension in the immutable session freeze; and
- stores a server-owned completion-policy snapshot. Its current status is
  `UNRESOLVED_OWNER_AUTHORITY`, with no policy ID, required-question count, coverage,
  or authority source. The 23 mapped question IDs and the 76 non-validation bank items
  are descriptive facts, not authorized completion criteria. New lock/reveal therefore
  fails with `SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED` until Joel explicitly selects
  and sources a scientific completion policy. An adequately assessed `answer: null`
  remains unscored and never forces a token.

Joel may invite only people he reasonably expects to take a long, candid interview
seriously. That screen should be based on willingness and data quality, not on expected
AstroHD agreement, astrology/HD belief, or a desired result. Invitation judgment cannot
prove truthfulness, so the in-session evidence-quality and coherence checks remain
important even though they do not choose the unresolved completion policy.

The deployable Custom GPT instruction block is
`reference/custom_gpt/participant_interviewer_instructions_under_8000_v1.md`; the
interview-only Action schema is
`reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml`.

## What is and is not scored

The natal participant runtime has an executable symbolic scoring path and a preserved
historical diagnostic reveal format. Once a separately authorized completion policy
exists, it can classify each frozen mapped dimension as supported, partially
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

Every rank, discrimination, and question-selection operation now compares the active
runtime with the session's exact frozen source commit, chart-engine fingerprint,
model version and bytes, mapping bytes, and question-bank version and bytes. Any
drift fails closed instead of silently scoring with a different bundle. Existing
`participant-reveal-v1` artifacts remain readable without being rewritten; newly
created reveals use v2 with the required model receipt.

## Runtime and integrity boundary

The mounted pilot requires:

```text
HDMATCH_NATAL_PILOT_ENABLED=1
HDMATCH_PARTICIPANT_STORE=<private persistent directory>
HDMATCH_NATAL_PILOT_TOKEN_SHA256=<sha256 of strong single-use owner code>
HDMATCH_PUBLIC_BASE_URL=<HTTPS production origin>
HDMATCH_NATAL_INTERVIEWER_URL=<private/unlisted Custom GPT URL>
HDMATCH_NATAL_INTERVIEWER_MODEL_RECEIPT=<exact configured GPT/model receipt>
RAILWAY_GIT_COMMIT_SHA=<exact deployed 40-character commit, supplied by Railway>
HDMATCH_CENTURY_CACHE=<verified extracted century-cache directory>
HDMATCH_CENTURY_MANIFEST_SHA256=154f2a27d4dc1e632a81c13b82b109fe83064cac5fe3673f82303ac6c24deae8
HDMATCH_CENTURY_CANONICAL_ROWS_SHA256=eb58516030f2176d4c136055829a8168ffe33715a35bfe0b4095c83824c88dfa
```

The chart engine must match fingerprint
`09e811ca0fe517975f9718ea7e12b72f66bf3d2509e049bc29f47169adef5397`.
Startup hashes the exact manifest and every compressed shard and fails closed on a
pin, inventory, content, or engine mismatch. A known-month request then parses only
the overlapping shard and clips the exact UTC range. Participant directories are
created with mode `0700`; session, freeze, evidence, lock, reveal, and invitation
receipt files use mode `0600`.

The verified cache is GitHub Actions artifact `9653492396` from run `33088719809`.
It contains 288,938 structural intervals and no participant data. Its outer ZIP
SHA-256 is `c1db39b07d36ea88d5be95c809168fc8e8717ee416cd29963262b70f9c977237`.
It must be transferred privately into the Railway volume, extracted through a
temporary path, verified against the outer ZIP, manifest, shard, canonical-row, and
engine pins, then atomically installed and verified again after restart. Publishing
the artifact is not part of this owner-only release.

## Verification receipt

- Local real-cache month slice: 251 exact stable structural states for the synthetic
  January 2000 Europe/London test.
- Real freeze through the owner intake: approximately 8.6 seconds, versus more than
  seven minutes when regenerating irrelevant month boundaries on demand.
- Predictions remained unchanged through confirmatory lock and reveal.
- Post-repair browser/API smoke at source commit
  `cc00febe382acb8f66628cbfc43e5668a0dba4a0`: AstroHD is the primary landing
  choice; explicit time controls, live OpenStreetMap search, participant-selected
  timezone, both required consents, the single-use gate, real prediction freeze,
  and two-credential session creation passed with synthetic data. Session-ID-only
  access returned `403`; the authorized flow accepted evidence, locked it, and
  revealed a 6-of-31 date rank over 251 exact states. The interviewer response had
  no `birth` or `chart` field, while the same-origin trusted page displayed both
  only after receiving the separate token.
- The relationship validation formatter no longer renders FastAPI issue objects as
  `[object Object]`.

Adequacy is deliberately split:

- **Operational alignment:** local unit/static/full-suite and real-cache two-token
  browser/API smokes pass; private production artifact staging, restart/readback,
  and the configured real Custom GPT Action smoke remain open.
- **Scientific adequacy:** the blind freeze/reveal design is suitable for an owner
  development case; human predictive validity is not established and the mapping is
  incomplete.
- **Release adequacy:** closed for friends and not yet deployed; bounded owner-only
  release awaits a clean second exact-diff review plus the operational gates above.
