# Life Patterns participant collection service

Separate from the historical owner and chart/scoring apps. The full reviewed V2 survey is kept on the server, not replaced by a short fixed quiz. All 79 canonical routes and 73 neutral facets remain available; they are not a quota. The three original authority files are hash-checked and each session pins its authority payload, model and effort.

## Status

The service has previously completed a real Railway -> Venice synthetic pipeline, but the live provider later returned HTTP 402 after available API credit was exhausted. Current deployment/runtime status is tracked in `tasks/ACTIVE-TASK.json`; do not infer it from this README.

The current source candidate is the cost-optimized hybrid architecture: voice/text ChatGPT can collect the long source interview, while Railway preserves provenance and asks only useful clarifications. Venice remains the production inference provider for Railway; subscription-authenticated Codex is development-only. No paid Venice call is required to verify this candidate's prompt/schema behavior.

## Data and identity

Exact source turns are committed to encrypted SQLite before model work. The database must live on a dedicated Railway volume at `/data`; runtime startup checks the volume path. A stable Fernet key is supplied through `PARTICIPANT_DATA_KEY`, never Git. Back up that key separately: a database backup without it is not recoverable. One process/replica uses SQLite WAL. Session capability hashes, not raw tokens, are stored in the database.

Invitations and private resume capabilities appear only in URL fragments; authentication uses Secure, HttpOnly, SameSite=Strict cookies. Application access logs are disabled. Origin checks, body limits, strict request fields, static-file allowlists and text-only DOM rendering constrain the HTTP surface. The researcher uses a separate random bearer token. Neither credentials nor imported analyst assessments are sent to the model. Researcher exports require participant consent.

## Interview and records

The participant can consent, answer, skip, pause, resume, append a correction, review and confirm, or stop without more questions. Original edited records can be preloaded as draft invitations; they are not treated as verified original transcripts. No model call occurs before fresh app consent. Imports preserve original metadata and every exact received answer. The raw source and subsequent changes remain distinguishable.

Venice planning is followed by a separate semantic admission call. Deterministic checks reject unknown routes/facets, invented source quotes, invalid antecedents and repeated canonical questions. These checks cannot themselves certify semantic truth. Generated follow-ups must stay tied to a canonical route. A natural finish requires useful saturation, not route-count completion. The prompt uses the full prior behavioral record and original authority, so normal model context limits still exist; the app does not promise unlimited LLM memory.

A saved answer and its model processing are different operations. Idempotency and revision checks prevent duplicate/incorrect writes. Pause/stop invalidates in-flight results. Immutable final JSON is stored once; checkpoints remain labelled partial. The participant need not export a chat or understand JSON. The researcher can download consented records directly.

## Deployment configuration

Use repository-root build context and `apps/life-patterns-participant/Dockerfile`. The image copies only this app and the four neutral survey authority files, not the chart/scoring implementation or private records. Run exactly one worker. Required variables:

- `PARTICIPANT_DATA_KEY`: persistent Fernet key.
- `PARTICIPANT_ADMIN_TOKEN`, `PARTICIPANT_JOIN_TOKEN`: random strong access secrets.
- `PARTICIPANT_DB=/data/survey.sqlite3` and a dedicated `/data` volume.
- `PARTICIPANT_PUBLIC_ORIGIN`: the exact HTTPS service origin.
- `UDA_MODEL_GATEWAY_URL`: the Venice-backed gateway base URL, without `/v1`.
- `UDA_MODEL_GATEWAY_TOKEN`: runtime secret when activation is authorized.
- `PARTICIPANT_MODEL=openai-gpt-56-sol`, `PARTICIPANT_REASONING=xhigh`.
- `PARTICIPANT_LIVE_ENABLED=0` until real provider verification is permitted and passes.

No automatic provider/model fallback, no credit purchase, and no environment-wide acceptance of unrelated staged changes. API-call and session caps are operational spend safeguards, not questionnaire quotas or evidence completeness tests. An exhausted cap pauses with a visible error; it must not falsely finish the survey.

## Verification

From repository root with this app's requirements plus pytest/httpx installed:

`PYTHONPATH=apps/life-patterns-participant python -m pytest apps/life-patterns-participant/tests -q`

The suite uses a deterministic fake model and tests real HTTP handlers, encrypted persistence, exact imports, source checks, access isolation, retries/cancellation and final exports. A separate headless browser smoke covers consent through final download and resume. These do not establish scientific validity, live Venice compatibility, or perfect detection of volunteered birth details. Birth detection is conservative; source exposure must stay explicit.


### Reproduce the UI test

Install Playwright and the test dependencies in a development environment. Use a locally available Chromium-compatible browser without accessing personal profiles:

`python apps/life-patterns-participant/scripts/browser_smoke.py --browser /path/to/chromium --output /tmp/participant-ui-smoke`

The script launches an isolated local server and synthetic model, creates ephemeral test credentials and a temporary database, then checks mobile consent, questions, answers, review, JSON download, resume and researcher access. The output contains synthetic evidence only. It does not call Venice or certify production model access.


## First real Venice smoke and opening repair

The first owner-run activation established that the existing gateway credential and Venice route work: openai-gpt-56-sol returned successfully at XHigh. The app-level smoke failed earlier, before any participant answer, because two model-proposed opening plans were rejected by the deterministic survey gate. No semantic-admission call occurred.

The empty-record boundary now uses the frozen bank's first self-contained route (A0) deterministically. This is not a shorter questionnaire and does not constrain later routing: once the first answer exists, the normal Venice planner plus independent semantic admission operate against the full prior record, bank, protocol and evidence guide.

The activation helper also restores an originally absent participant gateway credential by deleting the variable rather than attempting to set an empty Railway stdin value. The service stays disabled unless the complete real synthetic smoke passes.

## Create a private continuation invitation

For an existing participant record, use `scripts/create_invitation.py`. It reads the participant-admin credential from a file, rejects birth/chart/ranking fields before upload, preserves the prior JSON record as the declared source type, and writes the private resume link to a mode-0600 output file without printing the link or credential. Inference still begins only after the participant consents in the app.

## Imported-record latency behavior

Imported prior records are reviewed for routing in one complete-source semantic pass plus independent admission, rather than in sequential 12-turn model batches. This is not bulk scoring: exact imported turns remain source records, only material evidence is emitted, and other turns remain explicitly unassessed. New participant answers continue through ordinary source-bound admission. Long model work is detached from the HTTP request; the browser polls saved processing state and can recover after container replacement without losing answers.


## Processing visibility and payment-required responses

The status card shows total and stage elapsed time, server acknowledgement age, a five-second guarded worker heartbeat, and the age/count of received model stream events. These are different signals: a live server or worker is not proof of token progress. The meter is indeterminate and stops when status becomes stale or terminal. The browser uses bounded status requests and does not hold a multi-minute model request open.

A provider 402 is a `provider_blocked` state. Raw answers remain saved; model retries do not resume automatically. Existing `error` records carrying `provider_http_402` migrate when read. After resolving Venice API credit, use the existing authenticated researcher page's “Allow retry after fixing Venice API credit” action. It does not purchase credit, rotate a credential, certify the balance, or execute inference itself.

Run the synthetic UI check with `python apps/life-patterns-participant/scripts/browser_heartbeat_smoke.py --browser /path/to/chromium --output /tmp/heartbeat-proof`. No provider credentials or real participant data are used.

## Voice-first hybrid collection and inference budget

The preferred development path is now **voice-first ChatGPT collection -> frozen JSON -> Railway clarification only when useful**. Railway remains available for fully typed collection, but the research system does not assume that an hour of typing is measurement-equivalent to a natural spoken interview.

The voice collector bundle is under `reference/custom_gpt/`:

- `life_patterns_voice_interviewer_v2.md` — must-follow behavior/accuracy instructions;
- `life_patterns_voice_gpt_manifest_v2.json` — hashes and size receipt;
- `LIFE-PATTERNS-VOICE-GPT-SETUP.md` — setup and participant workflow.

The collector uses the same frozen v7 protocol/bank/evidence guide as Knowledge. It includes the core attribution/quotation/absence/correction checks adapted from PR #42 without merging that older AstroHD owner-pilot PR. Voice/text mode is recorded explicitly and survives Railway import.

### Cost architecture

The server still keeps the complete raw source and full frozen instrument locally, but routine semantic calls no longer resend them. The planner receives exact pending/current source plus only required antecedent/recent turns, the compact accepted evidence ledger, at most 12 deterministically eligible routes, and evidence-guide entries relevant to the pending answer.

The independent admission call receives only proposal-relevant source, the selected route's full admission/interpretation constraints, the used evidence-guide entries and any evidence being amended. A bulk ChatGPT import is the exception: the complete source is reviewed once so the next clarification is not already answered somewhere in the transcript.

Hard runtime guards prevent silent prompt growth: 35,000 serialized context characters for routine calls and 110,000 for a bulk import. Default model-call ceiling is 12 actual semantic model calls per session, with two Plan+Admission pairs reserved so a later review correction can still use the one permitted repair. Output-token ceilings remain at the previously exercised provider setting until exact Venice/XHigh truncation behavior can be tested without consuming scarce development credit. These are spend guards, not survey-completeness rules.

Production telemetry records prompt/completion tokens plus request/context characters. `scripts/analyze_collection_modes.py` compares voice/text modes descriptively and can add cost estimates when explicit current per-million token rates are supplied.

### Development inference

Do not consume Venice credit for ordinary semantic development probes. `scripts/codex_dev_probe.py` runs the planner or admission prompt through the subscription-authenticated Codex CLI and validates the returned JSON locally. It is a development harness only; it is not a participant/public inference backend.

Railway Cloud Agents can host Codex with available Codex credentials, so the same dev harness may be run there when that agent is reachable. Railway Agent itself is separately token-metered and is not treated as free inference. A Cloud Agent VM also has VM cost while awake; sleep it when not in use.

### Mode comparison

`scripts/analyze_collection_modes.py` reports answer-length distribution, conditions/corrections, neutral-evidence/facet yield, Railway clarification burden and model usage by explicit collection mode. These are product/measurement diagnostics, not evidence that voice and typed modes are psychometrically equivalent.
