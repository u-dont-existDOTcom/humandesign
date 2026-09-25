# Life Patterns v2 — client-side measurement freeze — 2026-09-15

The owner AstroHD recoverability regression requires a clean separation between target-blind measurement and target-aware scoring. The development browser now provides `Freeze/export measurement` so the owner can create a local immutable handoff after completing the interview and before any AstroHD mapping/scoring occurs.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_recoverability_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_recoverability.py`
- `tests/unit/test_life_patterns_v2_owner_recoverability_ui.py`

The exported JSON contains only the browser's completed participant-adjudicated pattern results, their per-pattern v2 freeze hashes, standardized coverage reports, aggregate coverage state, blueprint identifiers, freeze timestamp, and a client-computed SHA-256 `measurement_bundle_sha256`.

The browser computes the hash locally using Web Crypto and downloads the JSON locally. It does not send the frozen measurement to an AstroHD endpoint, Git, or Railway persistence. The owner can later provide that unchanged file for the separately authorized post-freeze recovery regression.

This does not make the measurement private from the model calls already used during the live interview; it prevents target-aware post-freeze scoring from feeding back into elicitation and avoids adding a server-side store for the owner's narrative.

GitHub Actions run `34991996940`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

The DOB/time recoverability gate remains open until a genuinely fresh exported bundle is scored after freeze.
