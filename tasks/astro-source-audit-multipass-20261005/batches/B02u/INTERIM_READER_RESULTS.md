# B02u interim source-reader evidence (not accepted)

The historical-documentation parent remains OPEN. Canonical baseline **2,305 Lilly + 1,066 Ptolemy = 3,371 combined**; B02u **zero** accepted new units.

Source archive: exact original 1647 Wellcome PDF SHA-256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. All 20 images pixel-verified independently from the full PDF. Original PDF364 lower through PDF381 before the *Of the house of the Thiefe* heading is current candidate scope, not the entire Chapter L.

**Reader route:** Claude Opus image-reader attempt returned weekly usage limit, with zero content; this is recorded as provider-specific interruption, not source inadequacy. OpenAI Codex CLI v0.160.0 was authenticated via the owner's ChatGPT account; a read-only original-image smoke test succeeded. Four isolated `gpt-6.1-sol` source-reader sessions were launched (high reasoning, sandbox read-only, no author reports or previous findings). Three windows have **completed** with valid structured output:

| Window | Original PDF pages | Source draft file | Raw unit count | Errata-only units |
|---|---|---|---:|---:|
| B | 369–373 | SOURCE_READER_B.json | 88 | 3 |
| C | 373–377 | SOURCE_READER_C.json | 74 | 2 |
| D | 377–381 | SOURCE_READER_D.json | 65 | 0 |

Window **A**, PDF364–369, experienced upstream WebSocket disconnections and was restarted in a fresh read-only medium-effort session. It has not yet produced a verified source draft; do not silently assume success or relaunch another paid attempt before reading that existing process state.

**Overlap**: Printed PDF369/373/377 appear in adjacent windows and duplicate candidate units must be inspected, not counted as independent rules. The consolidation script `consolidate_reader_windows.py` will preserve excluded overlaps and needs source review before acceptance. Page888 units in B/C are original **errata witness metadata**, not chapter-body records. The same-volume original enlarged errata visibly reads **p335 last line 'Planet'; p336 lines4 and9 'vertue'; p337 line28 'for ☉ and ♂'**, and printed p330 'read or' belongs to already accepted B02t text. See separate draft ERRATA_COLLATION.json and recovery original.

**Do not advance canonical counts or publish any extraction** until A is recovered, all source windows consolidated, overlap audited, independent reviewer verifies material clauses and tests, and archived extraction/replay and nonforce GitHub publication pass. Source claims about crime, suspects, physical descriptions and names are early-modern speculative text, not verified accusations or useful criminal/legal advice.
