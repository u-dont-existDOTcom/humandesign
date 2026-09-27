# Current state — Railway participant staging verified; live cutover not complete

The user authorized switching participant collection to Railway and using Venice for API calls. The separate service is deployed and reachable; it is deliberately not accepting participant interviews. The original owner application is unchanged. The three unrelated staged environment changes were not accepted.

Read `tasks/ACTIVE-TASK.json`, `tasks/participant-railway-venice-20260927/DEPLOYMENT-RECEIPT.json`, `REVIEW-DISPOSITION.json`, and `ACTIVATION-HANDOFF.md` in that task directory.

## Completed

- A standalone participant app preserves the complete V2 survey authority with version-pinned storage, 79 available canonical routes, 73 neutral facets, and no route-count quota or scoring/chart imports.
- Encrypted SQLite is attached to a dedicated Railway volume. Exact answers are stored before inference. Session capabilities, cross-tab request binding, append-only corrections, consent and stable JSON exports are implemented.
- Venice-only planning and separate semantic admission are implemented with no automatic provider/model fallback. Current intended model is GPT-5.6 Sol, XHigh.
- 31 application regressions pass with a synthetic model. The headless mobile browser test passes consent, questions, answers, review, final download, participant resume and researcher reload.
- Actual Railway deploy and redeploy reached SUCCESS. A synthetic draft session and its exact source answer survived the redeploy. This is direct persistence evidence, not a model-performance claim.

## What is not completed

The real authenticated Venice smoke call was blocked before execution by the tool security controls; no reason was supplied beyond the block. It was not a Venice HTTP response, and does not establish an invalid key, credit problem, or provider outage. No gateway token was injected into the new service and `PARTICIPANT_LIVE_ENABLED=0`. No equivalent alternate inference route was executed. The user-facing survey is not live.

Claude's first public-code review accepted disabled staging but identified activation defects. Repairs were made and regression-tested. The reconciliation was interrupted by a host restart; the retry timed out after 900.56 seconds without a verdict. There is no completed final independent approval. Do not start another unbounded reviewer loop or present mock tests as actual Venice verification.

No private participant survey or birth record has been imported to the deployed service. Private local records are retained outside Git. The app supports draft imports, but participant consent precedes inference. There are no background workers left running for this task.

## Recovery

The owned branch is `chat/participant-railway-venice-20260927-2234`. Deployed app code is `f35a94f3e4feaf0dfa562f97516ed2c42a51fd82`; later documentation/test-reproduction commits do not imply a redeploy. After the host reboot, the corrupted local Git object store was preserved separately and the owned working copy recovered from that exact pushed remote commit.

The next live step depends on a permission-approved gateway execution path and actual synthetic end-to-end verification. This is an operational boundary, not a reason to redesign the survey, request a new API key without evidence, migrate other services, or discard the participant's existing answers.
