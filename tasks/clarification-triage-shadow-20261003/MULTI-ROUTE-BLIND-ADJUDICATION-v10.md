# Fresh exact-authority multi-route blind adjudication v10 — frozen targets

Frozen before the first v10 implementation replay.

Two separate fresh Claude contexts received only the exact route authority, route-specific response-task rule, and R1–R10 synthetic packet:
- Claude Sonnet, high effort.
- Claude Opus 5.5, max effort.

They agreed exactly on R1–R9:
- R1: M09.
- R2: ready.
- R3: M05.
- R4: ready.
- R5: G20.
- R6: ready.
- R7: M09 + G19.
- R8: M11 + M05.
- R9: ready.

R10 is a frozen mixed target: both adjudicators require G19. Sonnet selected only G19; Opus selected M11 + PREFER-EXCHANGE + G19. Scoring therefore requires G19 and permits M11/PREFER-EXCHANGE as additional admitted routes. No post-output target adjustment is allowed.
