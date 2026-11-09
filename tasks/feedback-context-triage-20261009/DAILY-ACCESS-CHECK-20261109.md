# Life Patterns researcher feedback access audit — 2026-11-09 UTC

## Production access and baseline verification

- The connected Railway production environment still lists the `life-patterns-participant` service (`30746eb8-07c9-42e7-8825-152124b9337d`) and its existing 5,000 MB `/data` volume, with no staged changes. These metadata records do **not** imply a running app or prove volume contents.
- Its most recent successful deployment (`e8017b64-f7d4-4274-8de3-2397fb384dc0`, created October 29) remains **REMOVED** as of 2026-11-07 20:40:33 UTC, with no replacement successful deployment. Other deployments are removed or failed. Railway's environment summary reports an older failed deployment as `latestDeployment`, so current live status was resolved against the complete deployment list.
- On the authorized owner laptop, a public GET to the configured participant researcher route returned HTTP 404. A separate **authenticated** GET against the exact production `/api/admin/question-feedback` route, using the existing authorized Railway CLI `run` environment injection and the previously successful read-only private audit script, also returned **HTTP 404 Not Found**. No admin token was logged or persisted by this audit, and no new feedback JSON file was written.
- Therefore the November 9 queue could **not** be inspected. This is a removed-deployment blocker, not proof of an empty queue, no changes, or data loss. A deployment restoration would create a new running/cost-incurring service and conflicts with the owner's separately requested November 7 removal, so none was attempted.

## Historical privacy-safe baseline and dispositions

- The last independently authenticated private snapshot remains **November 7**: eight consented feedback annotations, with SHA-256 `e8a5ac4cbcdc52ce012d21cf99c3e7364b73ee96939839edf7e5f6e3ccd27902`. The old local private file was read for structural checks (record count, status/route distribution, hash only) and its bytes were not modified.
- Known disposition distribution: B0 3 resolved under accepted prospective `tendency-first-v1-20261006`; M11 1 new; VERIFY 2 new; ROMANCE-FADE 1 new; unmapped 1 new. The eight annotations overlap and must not be interpreted as eight independent human cases.
- Last validated analysis, not a new live decision: B0's unnecessary repeated vignette is already fixed prospectively; M11's discriminative-value claim is not population-validated; VERIFY's individual-vs-collective decision question is genuinely difficult to answer and requires a construct decision; ROMANCE-FADE/unmapped repetition is unproven without preserved interim chronology. The nine TF1-v2 rewordings and three proposed retirements are developmental, **not** activated. No newly observed complaint exists to justify a new version or disposition.
- Gmail's existing October 23 anonymized decision thread was read and still consists of exactly one sent message and no reply on November 9; a duplicate decision email was not sent. Prior decision choices remain pending, not owner-approved.

## Privacy and continuation

- No question bank, participant response, feedback disposition, frozen version, answered or blinded review, source words, deployed service, volume or deployment configuration was modified. No private answers, source feedback text, credentials, identifiers, or researcher report were committed.
- The next daily run must recheck live authorized production access and compare any newly available consented feedback to the November 7 verified baseline, the frozen question bank, accepted v1 policy, and v2 development proposals. Treat current queue status as **unknown** until an authenticated live read succeeds.
- The owner-defined daily task remains **enabled**, with no pause, disable, deletion or stop action. Restoring the removed deployment requires explicit owner authorization, not an automated workaround.
