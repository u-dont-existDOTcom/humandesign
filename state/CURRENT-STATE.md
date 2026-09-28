# Current state — imported-record latency hotfix deployed

The Railway participant service is live through Venice (GPT-5.6 Sol / XHigh). The imported-record latency incident is repaired in deployed commit `55bb92896b58de1c83dca3e97675b0214d328e4f`, Railway deployment `a1195246-b188-4168-96c0-7839b2c00858` (SUCCESS).

Production evidence for the failure was direct: one old `/api/next` request took 162.174 seconds; the next was client-closed with HTTP 499 after 203.057 seconds. The old engine processed imported turns in 12-turn semantic batches while resending the complete imported record and survey authority each pass, and held each `/api/next` request open for the model result.

The deployed repair reviews all currently pending imported source turns in one semantic Plan + one independent Admission pass. All exact imported source turns remain stored. Only material evidence is emitted; omitted imported turns are explicitly left `unassessed`, not treated as negative, coded, scored, or validated. New participant answers continue through the ordinary one-turn source-bound path.

Long semantic work now detaches from `/api/next`. The participant browser polls `/api/session` and shows whether it is on the planner or admission pass. A planning lease from a previous process is recovered on poll; the specific legacy admission error from this incident is automatically retried at most once. The existing private session remains on the persistent volume and requires no re-import or restart.

Verification before deployment: 35 participant HTTP/store/engine regressions passed, including a synthetic 96-turn import in one semantic pair, detached slow processing and restart recovery. The survey verifier passed 497/497. V2 source preservation passed 15/15 and import/resume preservation 8/8. A deliberately slow mobile browser regression passed and showed semantic-pass progress. Ruff checks passed. One Claude Opus 5.5 max public-code review was attempted but timed out after more than 15 minutes without a verdict; no second reviewer was started.

Post-deploy health is OK with `participant_enabled=true` and `provider_configured=true`. The owner service and unrelated Railway staged changes remain outside this task. The next action is simply to refresh the same private participant tab; no new invitation or survey repeat is needed.
