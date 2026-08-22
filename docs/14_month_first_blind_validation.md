# 14 — Month-First Blind Validation

## Rationale

Known month/year reduces the initial search to 28–31 local dates while preserving a hard concealed answer. This is the preferred first human proof of concept.

## Inputs visible to decoder

- birth month;
- birth year;
- birthplace;
- historical IANA timezone or enough location data to resolve it;
- behavioral questionnaire responses.

## Hidden until freeze

- true local day;
- true local time;
- resolved UTC birth moment;
- chart identity.

## Candidate universe

For every local day in the month, enumerate every exact chart-state interval intersecting that day. The unit of search is the state interval; the unit of primary reporting is the local date.

## Date aggregation

Implement and compare, on development/synthetic data only:

1. duration-weighted mean evidence;
2. duration-weighted log-likelihood integration;
3. best-state score plus stability penalty;
4. posterior-like normalized date mass only after empirical calibration.

Freeze one primary aggregation rule before untouched human validation.

## Stopping

Do not stop simply because a candidate reaches rank 1.

Use a fixed initial block plus a maximum adaptive block, or a frozen information/rank-margin threshold sustained across multiple independent clusters.

## Reveal

Freeze final ranked dates, best intervals, model hash, questionnaire hash, and prediction hash before revealing the real day/time.
