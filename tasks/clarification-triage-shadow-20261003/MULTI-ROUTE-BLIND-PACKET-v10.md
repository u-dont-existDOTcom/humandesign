# Fresh exact-authority multi-route blind packet v10 — 2026-10-04

Frozen before any v10 implementation replay.

The 10 synthetic cases were generated in a fresh Claude Sonnet/high context that received the exact frozen route questions, admission rules, interpretation limits, context rules, and the route-specific response-task rule. It was instructed not to inspect implementation code/output, prior validation cases, expected outputs, benchmarks, or repair history.

Key evaluation rule:
- judge whether source answers the response the exact route asks for;
- "check/ask first" may be complete for a next-action route but preliminary for a property/meaning route when the deciding result is unstated;
- a factor can answer a "what matters" route without a threshold/final choice unless the route asks for those;
- richer possible detail and missing coverage are not gaps;
- dependent/optional follow-ups require their exact context/admission rules plus a source-exposed unresolved distinction.

Cases R1–R10 are frozen in `MULTI-ROUTE-CASES-v10.json`.
