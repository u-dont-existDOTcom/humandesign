# Current state — imported-record latency hotfix ready to deploy

The Railway participant service is live through Venice (GPT-5.6 Sol / XHigh). The current incident concerns continuation of an already-consented 96-turn edited import, not Venice connectivity or lost answers.

Production HTTP evidence reproduced the failure: one old `/api/next` request took 162.174 seconds; the next was client-closed with HTTP 499 after 203.057 seconds. The old engine processed imported turns in 12-turn semantic batches while resending the complete imported record and survey authority each pass, and the browser held each `/api/next` request open for the model result. Eight such batches could therefore take far longer than twenty minutes.

The candidate hotfix reviews all currently pending imported source turns in one semantic Plan + one independent Admission pass. All exact imported source turns remain stored. Only material evidence is emitted; omitted imported turns are explicitly left `unassessed`, not treated as negative, coded, scored, or validated. New participant answers continue through the ordinary one-turn exact disposition/admission path.

Long semantic work now detaches from `/api/next`. The participant browser polls `/api/session` and receives visible progress (`planner` / `admission`) instead of keeping a several-minute HTTP request open. A planning lease from a previous process is recovered on poll, and the specific legacy admission error from this incident gets at most one automatic retry.

Verification: 35 participant HTTP/store/engine regressions pass, including a synthetic 96-turn import in one semantic pair, detached slow processing and restart recovery. The full survey verifier passes 497/497. The V2 source-preservation suite passes 15/15 and the older import/resume preservation suite 8/8. The slow-model mobile browser regression passes and shows semantic-pass progress. Ruff checks pass. One Claude Opus 5.5 max public-code review was attempted but timed out after more than 15 minutes without stdout/stderr or a verdict; no second reviewer was started.

No participant answer or private link is in public Git. The existing private session should be reused after deployment; no new import or survey restart is required. The owner service and unrelated Railway staged changes remain outside this task.
