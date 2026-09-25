# Lilly horary retrospective v0 — input-normalization freeze — 2026-09-24

Status: FROZEN BEFORE PREDICTIONS AND BEFORE ANY INCLUDED-CASE OUTCOME RETRIEVAL.

1. Source local clock time plus named place is normalized with the historical IANA civil timezone for that place/date.
2. If a poster supplies a daylight/standard abbreviation inconsistent with the civil timezone in force on that date, the named place/date/local clock controls and the discrepancy is recorded. No outcome information may be used to choose the offset.
3. When exact coordinates are not printed, use the standard city-center coordinates recorded in the corpus. This approximation is fixed before scoring.
4. A lost-object case may be represented as the binary recovery proposition “will the object be recovered?” only when the opening post explicitly seeks finding/recovery. Location-of-object detail is ignored by the v0 binary scorer.
5. No case may be added, removed, or have its normalized input altered after its prediction is computed, except to mark a predeclared engine failure as DEFER.
