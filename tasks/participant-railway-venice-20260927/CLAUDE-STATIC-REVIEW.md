# Public-code review

Requested model: Claude Opus 5.5 max. No private participant data, credentials or actual model-test responses were supplied.

**Overall: FINDS_ERROR.** It is safe to stage DISABLED. It is not ready for participant activation.

## Claims

1. **AGREES, with a caveat.** `command` commits the exact `answer_text` before any `/api/next`. Imports keep `record_as_received` and a per-turn `original_record`. Caveats: "exact" holds only at the parsed-JSON level, since duplicate keys collapse. `finish` also overwrites imported turn `conditions`/`process_feedback` with unquoted model output, and `dispositions` are not exported.
2. **AGREES** on confidentiality: 256-bit tokens are stored hashed, the cookie is HttpOnly/SameSite=Strict, and comparisons use `compare_digest`. **FINDS_ERROR** on write binding (D5).
3. **AGREES** for in-flight results: `finish` checks lease id and generation, and stop/pause bypass the revision check. **FINDS_ERROR** on D3 and D5.
4. **FINDS_ERROR**, in the code rather than the model. The model gates hold: quotes must be substrings, route IDs must be in the bank, import IDs are kept only when recorded, and skip means unknown. The code itself invents provenance (D2, D4).
5. **AGREES**: blob-SHA pinning, exact canonical wording, two-stage admission, "unassessed" is not treated as negative, and there is no coverage quota. **UNCERTAIN** whether 400 calls per session covers a 1,000-turn import (at least 168 calls at 12 per batch) plus the full bank. If it doesn't, D9 applies.
6. **AGREES.** `advance` is reachable only through `/api/next`, which is gated by `ready()`. Join and consent are gated too. Invitations and imports never touch the provider.
7. **FINDS_ERROR.** Freeze-once and the complete/stopped/partial labels hold. The blinding and verification fields overclaim (D1, D2).
8. **AGREES** for server logs, errors and responses: `--no-access-log`, code-only `ProviderError`, `from None`, and a sanitized 422. **FINDS_ERROR** against the store docstring "never enter … URLs" (D7).

## Activation blockers

**D1: target hold is broken and the export overclaims** (`engine.py` `advance`/`finish`, `domain.py` `export_record`).
- PLANNER says to use `hold` for volunteered target information. Admission rejects any hold without `control_is_participant_request`, and REVIEWER is asked whether it is "a request about the interview". A correct reviewer answers no, so the run repairs or errors, and every retry resends the text.
- If a hold does pass, `finish` only pauses. The turn stays in `semantic_turns` for all later calls, no `contamination_notes` entry is added, and evidence quoting it is not blocked.
- The export hard-codes `birth_or_chart_data_used_by_interviewer: false`, `birth_or_chart_data_in_this_export: false` and `frozen_before_birth_or_chart_reveal: true`. These are false whenever the conservative regex or key list misses, e.g. "I'm a Projector", a `dob` key, or "born 3 March 1990 around 4am".
- *Repair:* add a hold-specific admission flag. On hold, add a note, mark the turn quarantined, exclude it from `semantic_turns` and reject evidence that quotes it. Export `"not_detected_by_conservative_check"`/`null` instead of `false`/`true`.

**D2: verification is self-declared** (`import_record`).
- Choosing `raw_transcript` in a client dropdown sets `original_wording_verified: true` and `question_wording_status: "verified_original"`. `semantic_turns` then passes that status to both models.
- *Repair:* record it as `declared_raw_transcript_unverified`.

**D3: questioning can reopen after the interpretation is shown** (`command`).
- Pausing at `review` and then resuming yields `ready`, because there is no pending question. Separately, `correct` at review sets `review_only=False`.
- Either way, the next `advance` may `ask` after the evidence summary was displayed, and the new turns are not marked.
- *Repair:* once `review_seen` has stamped `shown_at`, make resume return to `review` and keep the `review_only` action filter.

**D4: correction provenance is invented** (`command`).
- `correct` and `review_correction` turns default to `route_type: "missing_piece_followup"`, `question_wording_status: "rendered_v2"` and `id_basis: "rendered_v2_tag"`.
- Correcting an imported, edited turn therefore relabels its edited question as rendered.
- *Repair:* use `route_type: "participant_correction"` and copy `id_basis` and wording status from the corrected turn.

**D5: writes are not bound to a session** (`app.py` `operation`, `participant_import`, `next_question`).
- There is one cookie per browser, so opening a second resume link retargets older tabs.
- Stop/pause skip the revision check, import has no check, and fresh sessions all start at revision 0. A stale tab can therefore irreversibly stop, decline or import into another session. This is plausible when a researcher previews invitations.
- *Repair:* send `session_id` with every write and return 409 on mismatch.

**D6: uncaught failures lose call accounting** (`Venice.call`, `advance`).
- `http.client.IncompleteRead` (a truncated chunked stream) and `AttributeError` (a non-stream `"usage": null`) escape both except clauses.
- The result is a 500, a session stuck in `planning` until the lease lapses, and consumed calls that are never recorded. Under a persistent fault, `maximum_calls` never trips.
- Separately, the 750 s lease is shorter than four ~600 s calls, so a second advance can double-spend. Its result is correctly discarded.
- *Repair:* map `HTTPException` to `ProviderError`. In `advance`, catch `Exception` and record `failed_attempt` plus the `error` phase. Renew the lease per call, or bound total runtime below the TTL.

**D7: the admin master token sits in the URL** (`admin.js`).
- `/admin#key=…` persists in browser history and sync.
- *Repair:* read the key, then call `history.replaceState(null, "", "/admin")`, or use a password field. Rotate the token if it was used this way during staging.
- Also reword the docstring: resume links are fragment capabilities that are never sent to the server.

## Staging defect (fails closed, not a safety issue)

**D8: the Origin check likely fails behind Railway's proxy** (`privacy_headers`).
- Unless `FORWARDED_ALLOW_IPS` is set, uvicorn trusts `X-Forwarded-Proto` only from 127.0.0.1.
- Behind Railway's edge, `request.base_url` is therefore likely `http://…`, while browsers send `Origin: https://…`. Every browser POST, including resume and invitations, would get 403.
- The tests use `http://testserver`, so they miss this.
- *Repair:* compare against a configured `PARTICIPANT_PUBLIC_ORIGIN`, or pass `--forwarded-allow-ips` for the proxy. One browser POST in staging will confirm it.

## Minor (fix before activation)

- **D9:** at the call cap, `claim` raises before any state change. The client loops on 503 ("not activated"), and the only exit is Stop, which is exported as `stopped_by_participant`. Add a `model_call_limit_reached` path that leads to review or freeze.
- `public()` sends the whole `pending_question` to the browser mid-interview, including `missing_distinction`/`why_useful`. Return only `text`/`question_id`.
- Quarantine stores the flagged birth text. `app.js` also clears the textarea on a 200, so the participant loses the answer. Store only a length or hash, and don't clear the textarea when `state.error` is set.
- A zero-turn import leaves `turns` empty, so imports can repeat. This produces duplicate `import-1` records and unbounded state, and invitees can do it while the app is disabled. Refuse an import when `source_records` is non-empty.
- The controller file is not in `SOURCES`.
- An export frozen by stop omits calls that were in flight at freeze time.
- No test covers hold, pause-at-review, corrections, cross-session writes, or a proxied HTTPS Origin.

## Staging assessment

The app can be deployed DISABLED while the owner clears the API boundary:
- No call path reaches Venice without both `PARTICIPANT_LIVE_ENABLED=1` and a token. Leave `UDA_MODEL_GATEWAY_TOKEN` unset in the meantime.
- There is no coupling to the owner service and no astronomy code.

D8 only blocks UI testing. D1–D7 block participant activation.
