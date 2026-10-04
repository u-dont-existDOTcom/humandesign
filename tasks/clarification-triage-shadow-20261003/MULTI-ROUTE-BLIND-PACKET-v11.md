# Fresh exact-authority multi-route blind packet v11 — 2026-10-04

Frozen before any v11 implementation replay.

The 10 synthetic cases were generated in a fresh Claude Sonnet/high context with no tools. The generator received only the exact frozen route authority and response-task rules. It was instructed not to inspect implementation code/output, prior validation cases, expected outputs, benchmark results, repair history, or prior adjudications.

Key rule:
- ask only for a route-requested response that source itself leaves materially unresolved;
- missing coverage and merely richer possible detail are not gaps;
- judge answer completeness by the route's exact response task;
- a check/ask procedure can be complete for a next-action route but preliminary for a property/meaning route when the deciding result is unstated;
- an in-scope factor can answer a what-matters route without thresholds/ranking/final choice unless exact route authority asks for them;
- explicit unknown remains unknown rather than triggering repetition;
- dependent/optional follow-ups require exact context/admission plus a source-exposed unresolved distinction;
- return all independent useful gaps, maximum three.

Cases S1–S10 are frozen in `MULTI-ROUTE-CASES-v11.json`.
