# Life Patterns participant collection service

Separate from the historical owner and chart/scoring apps. The full reviewed V2 survey is kept on the server, not replaced by a short fixed quiz. All 79 canonical routes and 73 neutral facets remain available; they are not a quota. The three original authority files are hash-checked and each session pins its authority payload, model and effort.

## Status

Implemented and tested with synthetic model responses. Venice is the only inference provider. The current deployment configuration is deliberately disabled (`PARTICIPANT_LIVE_ENABLED=0`) and contains no gateway token: a real authenticated Venice smoke request was denied by the interactive tool security boundary. Do not treat mocked tests or a green health endpoint as live inference evidence. Do not route around that denial. Participant cutover remains incomplete until the authorized connectivity/activation boundary is cleared and a real synthetic interview succeeds.

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
