# Participant Railway + Venice activation handoff

## Current result

A separate `life-patterns-participant` service is deployed from the `humandesign` repository. It is intentionally **not open to participant interviewing**. The original owner service is unchanged; three unrelated staged Railway changes remain unaccepted.

The current application has full V2 source-bound interviewing, encrypted SQLite on its own volume, consent, per-participant capabilities, cross-tab session binding, exact prior-record import, source/correction provenance, participant review and server-authored JSON. The original 79-route bank and 73-facet evidence guide are retained as a menu, not a quota. No chart/scoring engine is part of the deployed image.

## Exact remaining access boundary

An authenticated synthetic request to the existing Venice-backed gateway was rejected by the interactive tool security controls **before execution**. This was not a response from Venice and is not evidence of bad credentials or exhausted Venice credit. Do not bypass that rejection through another tool, endpoint, encoding or remote execution path. The new participant service has no injected gateway token and `PARTICIPANT_LIVE_ENABLED=0`.

The application's existing live-inference access must be authorized through a supported permission path before the deferred connectivity verification can run. Do not turn a repeated owner 'continue' into proof that the platform restriction disappeared. No new API key should be requested based solely on this rejected call.

## Deferred launch work after that boundary is genuinely cleared

Complete the remaining review disposition first. Use only the existing Venice gateway, with the pinned GPT-5.6 Sol / XHigh setting and no automatic provider or model fallback. Verify an actual synthetic conversation through planning, independent admission, a submitted answer, review and final export. Neither mock tests nor a health endpoint certify that the real inference path works. Only after that actual verification passes may participant access be enabled.

Do not simply redirect existing participants to a closed or unverified application. Existing private survey records are preserved outside public Git and have not been moved here. A researcher can preload an existing record into a draft invitation, but inference begins only after app consent. Maintain exact source-type and historical-blinding qualifications when importing.

## Verified evidence

See `DEPLOYMENT-RECEIPT.json`, `PUBLIC-STAGING-RECEIPT.json`, `PERSISTENCE-BEFORE-REDEPLOY.json`, `PERSISTENCE-AFTER-REDEPLOY.json` and `LOCAL-BROWSER-RECEIPT.json` here. The 31 app tests use synthetic model responses. The browser test uses a local fake model. The separate actual Railway redeploy test proved that a synthetic draft and its exact saved answer survive replacement of the running container. No real participant responses or birth data were used.

The executable browser smoke is saved at `apps/life-patterns-participant/scripts/browser_smoke.py`. The test and deployment scopes are explicit: this is application verification, not evidence that astrology is scientifically valid.

## Preservation

Keep the encryption key and admin/invitation capabilities in authorized private storage and Railway variables, not Git or application logs. A database backup requires the same encryption key to be usable. Only this new service may be redeployed for this task. Do not accept the environment-wide staged changes, change the owner app, enable a second worker against the same SQLite file, or use an alternate inference provider.

## Closeout of the interrupted review

The first public-code review is saved in `CLAUDE-STATIC-REVIEW.md`. Its concrete repairs and supporting tests are recorded in `REVIEW-DISPOSITION.json`. No final reconciliation verdict was returned: the original attempt was interrupted by the host restart and its retry timed out at 900.56 seconds. No reviewer is running in the background. Do not call this final independent approval.


## Owner-run Venice activation helper

The authenticated Venice request is blocked only in the assistant tool surface, not by an observed Venice response. The owner-side continuation is:

`bash apps/life-patterns-participant/scripts/activate_venice.sh --activate`

The helper reads the existing Railway gateway credential without printing it, performs a real GPT-5.6 Sol/XHigh Venice smoke, injects that same credential into the participant service, redeploys only that service, then runs a real synthetic participant flow through Railway and verifies the frozen JSON. If anything after mutation fails, it restores the previous participant live flag and previous gateway credential and redeploys.

On success it writes private admin/join links and the synthetic smoke receipt under `~/.local/share/humandesign/private/participant-railway-20260927/`. The synthetic session must never enter research analysis.
