# Current state — Railway participant migration using Venice

Read `tasks/ACTIVE-TASK.json` and `apps/life-patterns-participant/README.md`.

Current owner explicitly authorized the separate Railway participant service and Venice API path. The full reviewed V2 bank/protocol/evidence guide remain unchanged. The app implements encrypted durable SQLite, individual resume capabilities, exact source import, consent, two-stage semantic planning/admission, revision/idempotency guards and server-side V2 exports. No scoring/chart code is loaded by the app.

The original owner service and the pre-existing three staged environment changes are untouched. A new service with its own volume is created. A real authenticated Venice smoke request was rejected by the tool security boundary; the request was not executed, and no alternate authenticated inference route was substituted. Model activation is disabled and no Venice gateway token was injected into this new service. Mock/local test success must not be reported as live provider success or completed participant cutover.

All private source records remain outside public Git. No existing participant record has yet been moved into the new service. Runtime storage/access secrets are kept privately, not in source. Continue independent safe implementation/deployment verification, preserving the authenticated-inference boundary.
