# ADB Exact-Pair State-History Recovery V2 — Result Summary

Status: **successful conservative competing-risk augmentation; still below the frozen model-sufficiency threshold**.

V2 freeze:
`reference/research/adb_exact_pair_state_history_recovery_freeze_v2.md`

Result:
`reference/research/adb_exact_pair_state_history_recovery_v2.json`

Freeze SHA-256:
`a6eb6b9cdc9f3f963fff12ef8bc9fd5807f7cc8b544cab1c8fae67dec96af579`

## Result

V1 had 22/64 pairs with an explicit dissolution/reunion endpoint. V2 used other structured ADB event dates only to establish whether both people were demonstrably alive after a finite relationship-range endpoint.

V2 found 21 relationship ranges satisfying the frozen Rule B later-life test. Most corroborated pairs that already had explicit V1 dissolution evidence.

- pairs newly gaining a nonfatal exit: **1**;
- total pairs with explicit or V2-supported nonfatal endpoint: **23/64**;
- inferred reunion sequences after V2: **0**;
- range conflicts excluded: **0**;
- frozen minimum before a separate semi-Markov model specification may be written: **30 pairs**.

Therefore the V2 stop/go result is **STOP**.

No semi-Markov dissolution/reunion model should be fit from the V1+V2 ADB histories, and the 30-pair criterion must not be lowered after observing 23.

## Interpretation

The V2 logic was intentionally conservative. A finite ADB relationship year-range alone was not treated as a breakup. It became a nonfatal exit only when both partners had structured dated events strictly after the range endpoint (or when explicit nonfatal ending language would have qualified; no Rule-A cases were counted in this run).

The limited increase from 22 to 23 indicates that further progress requires additional state-history ascertainment rather than more astrology feature engineering.

The next data pass should therefore use a source ladder frozen independently of astrology outcomes, while retaining the same 64-pair universe and the same >=30 endpoint-pair sufficiency gate.
