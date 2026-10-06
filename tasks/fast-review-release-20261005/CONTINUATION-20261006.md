# Release continuation — 2026-10-06

Resumed the saved implementation at 764ff0f after the previous turn failed to deliver. Current owner request authorizes completing live integration and participant stage estimates. Pro review replaces the old Claude gate; no new provider wait is added.

Two release-boundary regressions were reproduced and repaired: explicit skips must remain visible to the fast model and remove that route from re-selection; uncalibrated integrated-stage estimates must be labelled provisional. Ten adapter-boundary tests now pass. Full participant suite: 170 pass. Root suite: 1,013 pass, six astronomy-data skips. Root lint and mypy pass. Affected application lint passes; a wider optional lint scan also identified three pre-existing style findings (UP035 in engine/inference_context and SIM105 in engine), outside the changed statements; the legacy engine was preserved rather than reformatted.

Frozen scientific authority is unchanged. The known current live service is still the legacy deployment; a package existing on disk is not deployment evidence. Next: exact-byte staged deploy, local worker atomic switch with prior target retained, synthetic live review and withdrawal, then verified package delivery.
