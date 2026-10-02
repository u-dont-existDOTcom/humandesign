# Father-loss timing V4 — causal/dependency correction

Date: 2026-10-02
Status: accepted V4 development specification for later cross-person testing.
Supersedes for implementation: the centered-window mechanics in `FATHER_LOSS_TIMING_V4_DEVELOPMENT_FREEZE_20261002.md`.

## Why this correction was mandatory

Two implementation issues were found before owner-facing acceptance:

1. A centered +/-60-day window allowed post-event information to contribute to an earlier candidate date. That is invalid for prospective timing.
2. A single Uranus-to-Sun/Saturn aspect could qualify both the father-contact and sudden-rupture gates. It may satisfy both logical gates, but the physical aspect must be scored only once.

These are causality/dependency corrections, not new astrological features.

## Correct window

For every candidate date, inspect only:
- candidate date minus 120 days
through
- candidate date itself.

No future contact may contribute.

## Dependency rule

A physical body x natal target x aspect contact is scored once at its highest applicable weight.

It may satisfy more than one gate logically, but it cannot contribute score twice.

## All other V4 rules unchanged

Father anchors, derived-house anchors, Uranus rupture modifier, aspect families, orbs, weights, exactness buckets and convergence multiplier remain as frozen in the original V4 development file.

## Evidential status

The owner's exact event date was already known during V4 development.

Therefore success on 2002 is development regression only. This corrected specification is now frozen for testing on other people/cases and must not be retuned on those validation cases.
