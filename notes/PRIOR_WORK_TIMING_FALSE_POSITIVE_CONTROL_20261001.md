# Prior-work scan — false-positive control for sparse timing events

Date: 2026-10-01
Applicability: required
Disposition: adapt + compose

## Independent conception snapshot
Problem: the timing models reward high scores near revealed events but can still rank non-events higher, producing false historical peaks.
Owner correction: optimize both hits and "unhits"; a model should be penalized for predicting danger/fatherhood in periods where those events did not occur.

## Search formulation
How should sparse event-detection or event-forecasting models be evaluated so that false alarms during negative time windows are penalized under severe class imbalance?

## Relevant established work
- Precision/recall and PR-AUC are standard tools for rare-event discrimination where positives are sparse.
- Matthews correlation coefficient (MCC) provides a balanced thresholded summary under class imbalance.
- False-positive/false-alarm rates should be reported explicitly.
- Event-centric time-series evaluation distinguishes event localization from per-timestep classification.
- Class imbalance can make ordinary accuracy and ROC-style summaries misleading if used alone.

Representative sources located:
- Imani et al., "Why ROC-AUC Is Misleading for Highly Imbalanced Data" (Technologies, 2026), DOI 10.3390/technologies14010054.
- Ahmadzadeh & Angryk, "Measuring Class-Imbalance Sensitivity of Deterministic Performance Evaluation Metrics" (ICIP 2022), DOI 10.1109/ICIP46576.2022.9897445.
- Brabec et al., "On Model Evaluation Under Non-constant Class Imbalance" (2020), DOI 10.1007/978-3-030-50423-6_6.
- Peng & Dinçer, "Event Detection via Probability Density Function Regression" (2024), DOI 10.48550/arxiv.2408.12792.

## Existing-work map
Already solved:
- false-positive accounting;
- rare-event precision/recall evaluation;
- class-imbalance-aware threshold metrics.

Partially solved:
- event-window evaluation with timing tolerance.

Project-specific remainder:
- mapping astrology-derived continuous timing scores onto event windows;
- hierarchical prerequisite states such as relationship-active -> danger escalation or pregnancy/family-state -> childbirth.

## External baseline
Use a simple calendar/base-rate predictor at the same time resolution and event prevalence.

## Result
Do not invent a "hit score" that ignores negative windows. Compose the astrology-specific feature generator with established rare-event discrimination metrics and hard-negative regression.
