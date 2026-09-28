# Current state — participant heartbeat and payment-required hotfix

Read `tasks/ACTIVE-TASK.json` and `tasks/participant-heartbeat-402-20260928/CHANGE-NOTE.md`.

The owner requested visible liveness/progress after a long wait ended in `provider_http_402`. The actual gateway trace confirms three lengthy successful HTTP responses followed by a fast 402. The failed call's original body and live balance are unavailable. Venice documents 402 as insufficient API credit; no purchase or alternate provider is authorized by this report.

The isolated hotfix adds elapsed/stage clocks, server polling freshness, guarded worker heartbeat and optional model-stream metadata; it does not invent a completion percentage. A 402 becomes a terminal provider-blocked session with clear participant messaging, no automatic retry and source-preserving migration of prior errors. The researcher can acknowledge a resolved API-credit issue and permit a future retry through the authenticated admin page.

The full affected service tests and headless mobile heartbeat/offline/402/recovery scenario passed. No live inference request was initiated. Survey authorities, model/effort and raw participant sources are unchanged. Deploy this tested candidate only to the participant service; preserve the original owner app and unrelated staged Railway changes.
