# 37 — Relationship full-study preflight

Status: implementation scaffold for the confirmatory public relationship study. The existing Railway questionnaire remains the development pilot until the required prediction layers can be computed pre-answer.

## Participant recovery: SHA receipts are not credentials

Participants must not be expected to save SHA-256 receipts. A freeze hash is scientific provenance: it demonstrates what bytes were sealed and when. It is not a human-friendly session identifier or authentication mechanism.

The full study intake therefore accepts a private contact email. The normalized email and a lookup hash stay in the private datastore; they are never written to the public GitHub repository or included in participant-safe preflight responses.

Email alone is not authentication. The implementation now provides a single-use magic link and six-digit OTP through authenticated SMTP. The browser resume token remains a fallback credential, while a successful email recovery rotates that credential and invalidates the previous browser token.

Recovery security properties:

- valid-email issuance always returns the same public `202` response, whether the address is unknown, rate-limited, SMTP delivery fails, or a message is sent;
- the datastore contains only domain-separated SHA-256 hashes of the magic token and OTP, never the plaintext recovery credentials;
- credentials expire after 15 minutes, have a persistent per-session issuance window/cooldown, allow at most eight verification attempts, and are consumed once;
- magic credentials travel in the URL fragment, so the initial HTTP request and ordinary server access logs do not receive them;
- successful verification issues a new random resume token and stores only its SHA-256 hash;
- SMTP requires STARTTLS or implicit TLS. There is no plaintext mode.

`HDMATCH_SMTP_PASSWORD` is the only required Railway secret. The non-secret defaults are `smtp.porkbun.com:587`, STARTTLS, and `joel@u-dont-exist.com` for both authenticated username and sender. They can be overridden with `HDMATCH_SMTP_HOST`, `HDMATCH_SMTP_PORT`, `HDMATCH_SMTP_SECURITY`, `HDMATCH_SMTP_USERNAME`, `HDMATCH_SMTP_FROM`, and `HDMATCH_PUBLIC_BASE_URL`. No SMTP credential belongs in Git.

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

`src/hdmatch/relationship/western.py` now provides deterministic Western relationship geometry on the same strict Swiss-backed natal calculations:

- tropical personality longitudes;
- major conjunction/sextile/square/trine/opposition detection with explicit orb;
- Placidus Ascendant/MC and house cusps when exact coordinates are supplied;
- directional partner-in-actor-house overlays;
- midpoint composite longitudes and major composite aspects.

`src/hdmatch/relationship/astro_rrf.py` implements the exact weighted V0.1 directional families frozen in `astro_rrf_directional_v0_1.json` for both actor directions and retains contribution-level evidence. It also records later frozen-family features for cognitive/composite and V0.4 Uranus/novelty hypotheses without inventing new weights.

The full-study prediction builder now computes this AstroRRF layer when both people have exact local time, IANA timezone, birth coordinates, and verified Swiss ephemeris files. If any required geometry/provenance is missing, the layer remains locked. It does not silently drop house terms, substitute noon, use Moshier fallback, or create post-hoc absolute `high/low` thresholds.

V0.2–V0.4 are primarily target/feature-family extensions rather than complete weighted outcome maps. Their frozen feature flags can be bound pre-answer, while any later calibration from raw feature/score values to ordinal relationship outcomes must be versioned separately and frozen before use as confirmatory prediction.

The remaining deployment blockers are therefore operational rather than conceptual: verified Swiss files must be available to Railway, and ordinary participant birthplace text needs a trustworthy coordinate/timezone resolution step or explicit confirmed coordinates.

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
- `GET /api/study/recovery/status`
  - reports only whether magic-link/OTP delivery is configured; it exposes no SMTP credential.
- `POST /api/study/recovery/request`
  - accepts a normalized email and always returns a generic response for valid input;
  - privately chooses only the most recently updated matching confirmatory session.
- `POST /api/study/recovery/verify`
  - consumes either `email + OTP` or `session_id + magic_token`;
  - returns a freshly rotated resume token only after successful one-time verification.

Middleware blocks both saved behavioral answers and live LLM quality calls for a `relationship-study-v1` session until its required prediction layers are computed and frozen.

## Next implementation work

1. Merge/bind the authoritative Survey-v2 noise artifact, while keeping Survey noise reliability separate from AstroRRF relationship-outcome calibration.
2. Wire unknown-time/full-day sensitivity into a separate natal-first, noncircular inference workflow rather than inventing noon charts or selecting a flattering time from relationship answers.
3. Freeze a pre-outcome AstroRRF ordinal calibration artifact before labeling raw directional scores as high/low or hit/miss.
4. Write only deidentified, public-safe outcome comparisons to the relationship learning ledger.
5. Run the exact-head production gates and verify a real SMTP delivery/recovery round trip before enabling email as the primary participant recovery path; keep browser-token fallback in place.
