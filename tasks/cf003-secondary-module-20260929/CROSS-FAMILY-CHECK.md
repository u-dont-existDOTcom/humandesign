# CF-003 cross-family methodology check

Date: 2026-09-29
Route: Claude Code subscription, Claude Opus 5.5, effort max
Reviewer session: `a6e2eee0-204b-407a-a751-8b03dee3db73`
Private participant data supplied: no
Credentials/birth/chart/predictor outputs supplied: no

Result: **FINDS_ERROR — substantive methodology defects found in the first implementation.**

## Liveness receipt

The reviewer was initially still `busy/working` after the earlier wrapper wait. Its live log showed active analysis and generated reproducibility probes. It was therefore left running rather than declared unavailable. The same session later completed `idle/done` and returned the verdict above.

This directly applies the UDA correction merged on 2026-09-29: elapsed time or wrapper timeout is not reviewer failure without checking the underlying session/status/log.

## Material findings

1. The global construct-label permutation was not the right chart-to-behavior null. It changes semantic mapping rather than participant pairing and can be miscalibrated when predictor and behavioral base rates differ.
2. The classifier packet's leakage screen was too weak and allowed multiple astrology/Human-Design clues, unscanned pass-through fields, missing turn roles, unlinked secondary records, and profile fields.
3. Several behavioral constructs overlapped or baked centrality into one construct; the three-question supplement privileged the added self-expression construct.
4. Quote validation allowed one-word evidence, string booleans, one quote supporting a 4, and score 0 without explicit counterevidence.
5. The freeze boundary relied too much on self-description: predictor files were not cryptographically committed before behavioral classification, generic `planet_scores` JSON was accepted later, and classifier model/raw-output provenance was missing.
6. Inclusive top-3 ties could expand to all ten labels, and published one-decimal predictor ties could be split by floating-point arithmetic.
7. The behavioral meanings are mainly project/Human-Design-derived development meanings, not a reconstruction of the authors' unavailable historical CF-003 target semantics.

## Disposition after repair

All seven finding families were repaired in the development module:

- inferential null = whole frozen behavioral-profile reassignment within preregistered birth-cohort strata; old label permutation is diagnostic only;
- leakage and source provenance hardened, including exact primary/secondary linkage;
- construct definitions narrowed and the added self-expression construct no longer defines itself as central;
- the three questions are generic continuity/centrality/contrast probes and are explicitly only a development coverage probe;
- quote/evidence validation hardened and quote reuse reported;
- predictor file hash must be committed before behavioral classification, with dedicated predictor schema and model/raw-output provenance;
- top-3 uses fractional boundary ties and predictor ranking uses the published 0.1-point grid;
- documentation now labels this as a combined development hypothesis, not the historical target.

Reviewer probes are preserved unchanged in `reviewer-artifacts/`. Null-calibration results are recorded in `NULL-CALIBRATION-20260929.md`.

## Current boundary

The module remains **DEVELOPMENT/SECONDARY, not prospectively frozen**. Remaining prospective choices include exact chart-factor extraction convention, classifier model/version, balanced source coverage, birth-cohort strata, permutation seed/count, and the literature-derived mapping decision. Existing participants remain exploratory only.
