# Participant Session v1 implementation notes

## Implemented on `participant-session-v1`

The branch contains a deployable participant interview harness with the following guarantees:

- local civil birth time is resolved with the repository's historical IANA timezone layer;
- the exact natal chart and frozen AstroHD prediction dimensions are serialized and SHA-256 bound before any behavioral evidence is accepted;
- participant evidence is stored as a canonical append-only, hash-chained event stream;
- each observation is tagged as trait, behavior, outcome, timing, environment, or conventional covariate;
- only trait/behavior observations with a valid frozen response token can enter the primary natal behavioral ranking;
- a free-form/Other clarification can neutralize a stale forced-choice token without deleting history;
- confirmatory evidence is locked before the true rank/predictions are revealed;
- the confirmatory ranking artifact is immutable;
- post-reveal clarifications generate a distinct final profile and a distinct exploratory ranking;
- the final report preserves the confirmatory result and labels the post-hoc result `posthoc_exploratory_not_independent`;
- outcome/timing/environment/covariate evidence is retained for later incremental/residual research rather than being mixed into the natal score.

## Current ranking universe

Participant v1 supports `known_birth_month` using the exact chart-state interval engine. Month universes can be persisted with the existing canonical candidate-universe cache, keyed by year, month, IANA timezone and chart-engine fingerprint.

`century_global` exists in the schema but deliberately raises an unavailable-capability error. The existing 100-year V4.3/V3.6 audit is a completed target-specific scientific audit, not a generic arbitrary-participant production universe. The next astronomy/search milestone is to convert the saved century ephemeris work into a reusable generic state cache and validate it before enabling this scope.

## Mapping limitation

The current participant scorer uses the repository's frozen symbolic mapping library. This is enough to exercise and scientifically test the session protocol, but it is not yet the final high-dimensional holistic AstroHD mapping. Expanding independently sourced, discriminative mappings for the richer V4.3 feature surface remains the main model-quality bottleneck after the session infrastructure itself is validated.

Free-form holistic observations are never discarded simply because they are not currently mapped. They remain in the evidence log for future mapping/model versions, but they do not silently acquire a numerical weight in the current frozen run.

## Deployment

Install the API and ephemeris extras, provision the licensed/authorized Swiss Ephemeris `.se1` files, and configure:

```text
HDMATCH_EPHEMERIS_PATH=/private/path/to/swiss/files
HDMATCH_MAPPING_PATH=/app/mappings/mapping_library_v1.json
HDMATCH_QUESTION_BANK_PATH=/app/reference/core/question_bank_v1.json
HDMATCH_PARTICIPANT_STORE=/private/persistent/participant-sessions
HDMATCH_CANDIDATE_CACHE=/private/persistent/candidate-universes
HDMATCH_CODE_COMMIT=<deployed-git-sha>
```

Run the FastAPI factory with an ASGI server, for example:

```text
uvicorn hdmatch.api.participant_app:create_participant_app_from_env --factory --host 0.0.0.0 --port 8000
```

The session store contains sensitive birth and behavioral data and should be private, access-controlled, backed up appropriately, and excluded from the repository.

## Custom GPT assets

- `reference/custom_gpt/participant_interviewer_instructions_v1.md`
- `reference/custom_gpt/participant_action_openapi_v1.yaml`
- `reference/custom_gpt/scientific_intake.html`

For a genuine blind test, serve the intake page from the same trusted backend origin (or an equivalent trusted intake service). The participant enters birth data there and pastes only the returned opaque `HD-...` code into the GPT conversation.

For self-discovery mode, the GPT may create the session after receiving birth data, but the resulting pre-reveal ranking must be described as precommitted exploration rather than a fully blinded scientific test.

## Scientific outputs

The participant report separates three quantities:

1. frozen AstroHD prediction agreement with independently elicited behavior;
2. pre-reveal person-to-birth-state/date rank;
3. post-hoc final-profile-to-birth-state/date rank.

The third is intentionally exposed to the participant but cannot be counted as independent confirmation.

Future outcome/timing work should use separate predeclared models and held-out/prospective evaluation for:

- behavior + environment -> outcomes;
- chart variables added to an ordinary outcome model;
- progressions/transits added to time-varying behavior/event models;
- chart variables added after conventional covariates such as validated personality measures and relevant environmental/demographic predictors.
