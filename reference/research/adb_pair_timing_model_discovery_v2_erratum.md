# ADB Pair-Timing Model Discovery V2 — Evaluator Erratum

The first completed V2 run produced an invalid apparent result in which every model had 100% top-1 / 100th-percentile event-date ranking while all fitted outer-fold models had zero nonzero coefficients.

Cause: at the selected strong L1 regularization, every candidate date in an event received exactly the same decision score. The evaluator sorted equal scores stably, and the true date had been inserted first in each event's candidate list. Therefore a complete tie was incorrectly assigned rank 1 rather than neutral rank.

This is an evaluation implementation bug, not a model result.

The frozen feature/model specification in `adb_pair_timing_model_discovery_freeze_v2.md` is unchanged. The rerun changes only tie handling:

- event percentile = percentage of control dates scored below the true date + half the percentage exactly tied with it;
- an all-tied event therefore scores 50th percentile;
- average rank = 1 + number of controls strictly above + 0.5 * number of controls tied;
- top-1 requires average rank <= 1; top-3 requires average rank <= 3;
- softmax log loss is unchanged.

The initial committed JSON with SHA/content corresponding to the buggy evaluator must not be cited as evidence. The next result generated under the corrected evaluator supersedes it while preserving the same frozen astrology feature rules.
