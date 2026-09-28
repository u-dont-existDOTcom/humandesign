# Heartbeat, progress and the 402 incident

The participant UI now distinguishes server responsiveness, worker liveness and actual arrival of AI response data. It shows elapsed time, time in the current stage, and Read answers / Check interpretation / Ready stages. The activity meter is indeterminate: no elapsed-time percentage or guessed remaining time is shown. A dropped connection or stale worker visibly loses its live indicator. Revision attempts are labelled and retain the original operation timer.

The gateway trace showed three HTTP 200 requests taking 178.946, 31.904 and 136.016 seconds, followed by a 402 response in 0.096 seconds. The wait was before the final fast refusal. Venice documents bearer HTTP 402 as insufficient available API credit. The original raw error body and current account balance were not retained, so this is not a balance measurement or proof of a specific amount spent.

A 402 now pauses the affected interview with a plain-language credit message, preserves its exact saved answers and partial record, and stops automatic inference retries. Reloading an old 402 session upgrades the display without starting another paid call. Polling is a status read, not an inference call.

The researcher page offers “Allow retry after fixing Venice API credit” for a payment-blocked record. Its confirmation acknowledges that the organizer has addressed billing; the app does not independently certify the balance or buy credit. The action clears the block only for that session and does not itself call the model. Participants are not asked to change keys, pay, reconstruct responses, or restart their survey.

Verification: 41 affected-service tests passed. A real headless mobile browser with a deliberately delayed synthetic model verified changing elapsed time, live/stale heartbeat, connection recovery, the 402 message, no automatic retry, and researcher-approved same-session continuation. Stream metadata tests verify no model/participant text is included. The app still uses Venice and the previously pinned model/effort. No live paid model retry or account purchase occurred in this repair.
