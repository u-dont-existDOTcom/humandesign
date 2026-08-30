# Pro supervision checkpoint 1 — deterministic natal-time foundation

Status: complete on 2026-08-30. This document records the actionable contract returned by the dedicated authenticated Brave ChatGPT Pro conversation after the fresh repository, GitHub, Railway, and live-runtime audit.

## Gate decision

- `OWNER DECISION REQUIRED: NO`
- `APPROVED: OPTION A — FOUNDATION ONLY`
- Work only on a non-production branch with synthetic fixtures.
- Do not merge to `main`, migrate production, or deploy publicly before checkpoint 2.

The approved result layer may express only candidate completeness and exact set-theoretic facts: which declared mechanics are invariant across every candidate interval and which vary. It must not rank or eliminate candidates, assign weights or priors, normalize durations into score mass, produce probability-like labels, recommend a time window, or imply that any candidate is more likely.

The natal-time workflow must remain separate from relationship intake in routes, schemas, storage namespace, and tests. Existing relationship unknown-time handling remains fail closed and unchanged.

## Evidence-state contract

Every evidence item records the asserted value, evidence source (`documentary`, `memory`, or an explicitly confirmed candidate-date set), whether documentary status is participant-reported or independently verified, entry time and method, and any supplemented or superseded evidence item.

The independently remembered weekday must be captured and server-locked before any client response, calendar control, validation message, generated text, server response, analytics event, or preloaded data reveals the weekday implied by the declared date. A client-supplied independence flag is insufficient.

Required transitions:

| Date evidence | Weekday evidence | Required behavior |
| --- | --- | --- |
| Documentary | unavailable | Preserve the documentary date; record weekday unavailable. |
| Documentary | agrees | Preserve the date; record concordance without adding precision. |
| Documentary | conflicts | Preserve the date byte-for-byte; record conflict; never correct it. |
| Memory | unavailable | Preserve the memory-sourced, unverified date. |
| Memory | agrees | Preserve the date; record memory concordance, not validation. |
| Memory | conflicts | Set `birth_date_uncertain`; block single-date enumeration until an explicit candidate-date set is confirmed. |
| Conflicting documentary dates | any | Fail closed; require explicit resolution or explicit candidate-date set. |
| Later correction | any | Create a new immutable lineage through `supersedes`; never overwrite an earlier evidence record or freeze. |

A required candidate-date set is shown only after weekday lock and conflict disclosure, is never preselected, is explicitly confirmed in full, enters enumeration with no order or prior, and preserves the originally declared date in the lineage. Weekday agreement must not be called verification.

Schemas must reject relationship responses, relationship identifiers, compatibility output, debrief content, and undeclared fields.

## Candidate-complete interval contract

“Exact” is always qualified by the pinned engine, astronomical files, timezone data, state-identity specification, and supported temporal resolution.

For every explicitly accepted date and resolved IANA timezone:

- enumerate every valid instant mapping to that civil date;
- store absolute interval boundaries plus local offset/fold data;
- support 23-hour and 25-hour days, repeated and nonexistent local times, leap days, and historical offset changes;
- fail closed when place/timezone ambiguity changes the instant domain;
- partition the domain into ordered maximal half-open intervals `[start, end)`;
- include every discrete engine field eligible to affect downstream natal or relationship work in a versioned full state identity;
- never merge states merely because their reduced model-visible signatures match;
- mark a mechanic stable only when the same defined value occurs in every candidate interval, and variable when any two defined values differ;
- treat missing/error/unresolved values as not stable;
- retain duration only for coverage accounting, never as evidence or score mass.

Boundary enumeration must use authoritative engine/ephemeris transition events with verification, or exhaustive evaluation of every representable input instant. A sampled search is acceptable only with a machine-checkable no-missed-transition proof. Coverage tests must prove exact union, no gaps/overlaps/zero-length intervals, maximality, one interval per representable instant, transition-side state checks, and byte-identical reruns.

Required fixtures cover an ordinary day, leap day, DST gap, DST fold, historical offset change, transition at day start/end, closely spaced transitions, multiple candidate dates, fail-closed timezone ambiguity, and two full states sharing one reduced signature.

Each coverage receipt records actual day duration, UTC/local boundaries, interval count, full-state digests, summed duration, coverage/overlap/maximality results, temporal resolution, and rounding convention.

## Provenance and immutable records

Required provenance includes repository commit, engine revision, dependency-lock digest, runtime/container digest, ephemeris and data checksums, timezone database version/checksum, canonicalizer and enumerator versions, input resolution/rounding, and the state-identity field specification/digest.

Use three distinct frozen objects with deterministic canonical serialization and content hashes:

1. `Manifest`: frozen evidence lineage, explicit unordered candidate-date set, location/timezone resolution, engine provenance, state identity, enumerator version, and privacy class; no relationship or outcome evidence.
2. `Freeze`: commits to exactly one manifest and deterministic computation before later evidence can enter.
3. `Result`: references exactly one freeze and contains only candidate-complete intervals, coverage receipts, state digests, and deterministic stable/variable facts.

Any scientific change creates a new digest. Corrections create a new manifest/freeze/result lineage linked by `supersedes`. Scientific immutability does not prevent separately governed deletion of private contact, consent, recovery, or raw-response records.

All schemas use `extra=forbid` semantics and explicitly reject rank, weight, score, probability, confidence percentage, duration-normalized mass, stopping recommendation, relationship evidence/outcome, and compatibility fields.

## Public-safe boundary

Public serialization is an allowlist, not a private object with fields removed. Before checkpoint 2, real participant export remains disabled and only conspicuously synthetic fixtures may exercise it.

Do not publish participant-level natal records, exact birth date/time candidates, birthplace, timezone history, contact/consent/session/recovery data, raw/free-text responses, relationship identifiers/evidence, or hashes derived solely from exact personal data. A public identifier is random and independent of all private identifiers. A detailed chart or interval sequence is not assumed anonymous. This contract is not the future public outcome ledger.

## Privacy and operations

`.gitignore`, Docker/build exclusions, and an automated privacy gate must cover participant records; contact and consent; session/recovery material; raw questionnaire/free-text data; private birth inputs and uploads; classifier transcripts; local databases/journals; private exports, backups, temporary files, and logs; credentials/tokens; and generated copies.

The gate checks ignored representative files, the Git index and branch diff, build/release contexts, reachable history, secret/private canaries, and log redaction. A finding in reachable history is an incident stop. No live participant record may be created, read for testing, modified, migrated, or deleted. No production variable changes are permitted; `OPENROUTER_API_KEY` remains untouched until a separate runtime-use proof exists.

## Hard stops

Return to Pro immediately if complete day coverage or engine resolution cannot be established; arbitrary clock bins become necessary; place/timezone ambiguity would be resolved silently; full state identity would collapse to the reduced visible signature; any inferential/ranking/weighting/stopping semantics appear; relationship evidence enters natal work; relationship and natal records/validation paths could leak; a freeze can mutate; private data reaches Git, CI, builds, logs, public schemas, or fixtures; production migration/deploy or live-record testing becomes necessary; synthetic robustness is described as human calibration; omitted fields are called irrelevant; or `OPENROUTER_API_KEY` removal enters scope.

## Checkpoint 2 evidence packet

Return with the exact branch/commit/diff; proof that `main`, Railway, variables, and participant records stayed unchanged; the transition test matrix and independent-weekday API trace; full versioned state-identity field list; exhaustive boundary method; all coverage receipts; pinned provenance/checksums; synthetic manifest/freeze/result/public objects and digests; immutability/schema/public-boundary tests; privacy/build/history/log gate evidence; GitHub ruleset and stale-PR status; confirmation that `OPENROUTER_API_KEY` was untouched; and every unresolved fail-closed condition.

Checkpoint 2 must independently review any proposed priors, ranking target, score meaning, duration use, stopping rule, uncertainty communication, calibration, validation split, or reduced-signature use. Before such semantics are implemented, the packet must include a bounded scan of established uncertainty-inference, rectification, calibration, and leakage-control methods against the strongest applicable baselines.
