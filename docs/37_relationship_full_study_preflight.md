# 37 — Relationship full-study preflight

Status: implementation scaffold for the confirmatory public relationship study. The existing Railway questionnaire remains the development pilot until the required prediction layers can be computed pre-answer.

## Participant recovery: SHA receipts are not credentials

Participants must not be expected to save SHA-256 receipts. A freeze hash is scientific provenance: it demonstrates what bytes were sealed and when. It is not a human-friendly session identifier or authentication mechanism.

The full study intake therefore accepts a private contact email. The normalized email and a lookup hash stay in the private datastore; they are never written to the public GitHub repository or included in participant-safe preflight responses.

Email alone is not authentication. The intended production recovery path is a verified magic link or one-time code. Until a mail-delivery provider is connected, the browser resume token remains the actual credential. Do not implement an insecure `email -> session` lookup merely for convenience.

## Private intake before behavioral evidence

A confirmatory relationship case begins with:

- contact email (optional until verified-email delivery is enabled);
- respondent birth date, local time or explicit unknown time, birthplace, IANA timezone, time-source quality, and optional uncertainty window/coordinates;
- partner birth record with the same fields;
- explicit consent to store private research data;
- explicit consent to process the partner birth data;
- explicit consent to send questionnaire text to the chart-blind OpenAI answer auditor.

Exact email/birth data stay on the private Railway datastore. The public repo may contain only schemas, model/version hashes, deidentified aggregates, and public-safe learning artifacts.

## Mandatory pre-answer prediction freeze

The relationship study must not accept confirmatory behavioral answers until every layer declared `required_for_confirmatory` has status `computed`.

The current freeze contract binds:

- a SHA-256 of the two private birth records (not the raw records);
- exact frozen model versions and artifact hashes;
- questionnaire version/hash;
- code commit;
- Survey-v2 noise-policy artifact identity when available;
- computed prediction payloads and calculation provenance;
- explicit limitations for any layer that is not computable.

The freeze receipt itself is derived from the complete canonical freeze object. It is shown only as optional audit provenance; the participant does not need to retain it.

## Current layer status

### Human Design connection mechanics

`src/hdmatch/relationship/analysis.py` is already a deterministic mechanics engine. The full-study builder can calculate its pre-answer connection surface when:

1. both exact civil birth times and IANA timezones are available; and
2. `HDMATCH_EPHEMERIS_PATH` points to verified local Swiss Ephemeris files.

The strict engine refuses silent Moshier fallback. Unknown/estimated-time interval aggregation already exists in `uncertain_time.py` but is not yet wired into the public preflight builder.

The computed HD payload is mechanics only: types/authorities/profiles, connection-channel categories, center configuration/definition, shared gates, and Sun/Earth/Node alignments. It does not manufacture a compatibility scalar or relationship-outcome prediction.

### Western AstroRRF V0.1–V0.4

The frozen AstroRRF documents/specs are bound into the prediction freeze by exact file hashes. However, the repository does not yet contain one reusable production Western synastry/house/composite feature adapter that implements those frozen feature families end to end.

Therefore the current full-study builder marks this layer `pending_engine`. It must not replace the missing adapter with post-answer prose interpretation or manual chart inspection.

This is now the principal engineering blocker to unlocking new confirmatory public cases.

## Survey-v2 noise policy

The relationship layer inherits the Survey-v2 noise work; it does not invent an independent retry/corroboration policy.

`bind_noise_policy()` currently does two safe things:

- if no final artifact is available, marks policy status `pending_authoritative_artifact` and refuses to invent thresholds;
- when a final JSON artifact path exists, binds its exact SHA-256 and schema/version identifier.

A version-specific threshold adapter should be added only after the final scoring artifact/schema is frozen. The additional long-running scoring work is not a blocker to the private-intake/prediction-freeze architecture.

## API state

`src/hdmatch/api/relationship_study_app.py` layers new endpoints over the current direct-OpenAI questionnaire application:

- `POST /api/study/intake`
  - creates the private session;
  - saves intake/contact data;
  - binds/attempts the pre-answer prediction freeze;
  - returns only a participant-safe preflight plus the ordinary private resume token.
- `GET /api/study/sessions/{session_id}/preflight`
  - reports whether email is on file, intake is complete, freeze exists, each prediction-layer status, noise-policy status, and whether confirmatory capture is unlocked;
  - never returns raw birth data, email, charts, or hidden predictions.
- `POST /api/study/sessions/{session_id}/refresh-prediction-freeze`
  - may rerun the pre-answer builder only while zero behavioral answers exist;
  - rejects any attempt to regenerate predictions after behavioral evidence has been captured.

Middleware blocks both saved behavioral answers and live LLM quality calls for a `relationship-study-v1` session until its required prediction layers are computed and frozen.

## Next implementation work

1. Productionize Western birth-coordinate resolution and exact Western chart/synastry/composite features with explicit provenance.
2. Implement the frozen AstroRRF V0.1–V0.4 adapter on those features.
3. Wire unknown-time sensitivity rather than inventing noon charts.
4. When the final noise-scoring schema is canonical, add its version-specific threshold adapter.
5. Add the post-phenotype reveal/comparison endpoint and write deidentified hit/miss records to the existing relationship learning ledger.
6. Add a real email provider and verified magic-link/OTP recovery; until then keep browser token authentication.
