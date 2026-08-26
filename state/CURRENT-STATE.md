# Current state

- As of: `2026-08-26`
- Task ID: `participant-session-v1`
- Goal: ship the first participant-facing AstroHD interview harness with immutable pre-answer predictions, candidate-blind adaptive interviewing, confirmatory reveal, and a separately labeled post-hoc holistic-profile ranking.
- Branch: `participant-session-v1`.
- Primary scientific claim under test: `natal chart -> persistent trait/behavior fingerprint`.
- Secondary research layers are stored separately: `behavior + environment -> outcomes`, natal outcome increment, progression/transit timing increment, and residual chart prediction after conventional covariates.
- Evidence rule: only `trait` and `behavior` observations with valid frozen response tokens can affect the primary natal rank. Outcome, timing, environment and conventional-covariate records are retained but excluded from that score.
- Blinding rule: scientific participants should submit birth data through trusted external intake and give the conversational interviewer only the opaque `HD-...` session ID. Direct DOB entry is supported only as explicitly precommitted self-discovery.
- Prediction rule: exact chart plus human-readable frozen prediction dimensions and provenance are SHA-256 bound before the first behavioral observation.
- Session rule: evidence is append-only/hash-chained; confirmatory lock/reveal artifacts are immutable; post-hoc evidence cannot modify the blind result.
- Participant result: show both the pre-reveal confirmatory rank and the final refined post-hoc rank. The latter is always labeled `posthoc_exploratory_not_independent`, even when it improves substantially.
- Interview rule: prioritize persistent patterns, childhood-to-adult continuity/change, contexts, exceptions, examples and counterexamples. Always permit an Other/free-form answer rather than forcing a category; a later free-form correction may neutralize an earlier scoring token without deleting history.
- Astronomy state: exact Swiss-Ephemeris chart calculation and historical IANA timezone resolution are implemented. A completed exact 100-year V4.3/V3.6 audit exists, and the generic Swiss-backed AstroHD ephemeris cache is checked into the repo with provenance.
- Ranking state: participant v1 currently supports exact `known_birth_month` candidate-state ranking and persistent month-universe caching. `century_global` is represented but fails closed until the target-specific 100-year audit is converted into a reusable arbitrary-participant candidate universe.
- Mapping state: the frozen symbolic mapping library is adequate for an end-to-end pilot, but richer independently supported/discriminative V4.3 mapping coverage remains the principal model-quality bottleneck for a truly holistic global-identification test.
- API state: participant-safe create/progress/next-question/evidence/lock/reveal/finalize/final-report routes are implemented behind optional dependency injection; environment-configured deployment factory is `hdmatch.api.participant_app:create_participant_app_from_env`.
- Custom GPT assets: participant interviewer instructions, Action OpenAPI schema, and same-origin blind scientific intake page are under `reference/custom_gpt/`.
- Current verification target: run the repository CI suite plus `python -m pytest tests/unit/test_participant_session.py`, resolve formatting/type/test failures, then merge the participant-session PR.
- Next after v1 merge: build/certify reusable generic century-wide candidate-state cache; then expand the natal holistic mapping before enabling strong 100-year identification claims. Relationship/future ephemeris extensions are not required for this milestone.

