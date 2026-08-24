# MoBa 5–15 replication access packet v1

**Purpose:** obtain the minimum approved MoBa + Medical Birth Registry of Norway (MBRN/MFR) data needed to execute the already-frozen `RAW_CHANNEL_5_15_FULL_ACTIVATION_SET` validation without exposing or using extra individual information.

Frozen validation protocol:
`reference/validation/moba_vitality_5_15_freeze_v1.json`

## Research question

Does the frozen 5–15 two-window birth-state object, discovered on Gauquelin DEVELOPMENT data, prospectively predict higher EAS temperament Activity at 18 months in MoBa?

MoBa data must not be used to modify the predictor, window geometry, activation set, Design anchor, outcome definition, direction, or primary analysis.

## Minimum requested MoBa variables

### Outcome

Questionnaire 5, age 18 months:

- `EE417` — child is always on the go
- `EE419` — child is off and running as soon as waking in the morning
- `EE423` — child prefers quiet, inactive games to more active ones

Primary aligned Activity score:

`mean(6 - EE417, 6 - EE419, EE423)`

Require all three valid values for the primary analysis.

### Linkage / clustering / control fields

Request the release's pseudonymous:

- child identifier
- mother/family identifier sufficient for clustered uncertainty
- pregnancy/birth identifier if distinct
- child sex
- questionnaire/form version if version can affect item availability

Do not request names, addresses, national identity numbers, free text, or other direct identifiers.

## Required MBRN birth variables

- `FDATO` — child's date of birth/delivery
- `FKLOKKEN` — child's time of birth, HHMM
- `KJONN` only if child sex is not already supplied consistently from MoBa
- `FLERFODSEL` / `PLURAL` for the prespecified multiple-birth sensitivity if available

Exact date/time are used only to derive the frozen astronomical predictor and frozen low-frequency calendar/time controls.

## Privacy-minimized preferred execution

If exact `FDATO`/`FKLOKKEN` may not be released to the analysis dataset, run the frozen derivation inside the approved secure/custodian environment and return only:

- `Z_5_15` (0/1/unresolved)
- birth-year category
- day-of-year sine/cosine, harmonics 1 and 2
- local-clock sine/cosine, harmonics 1 and 2
- DST ambiguity/unresolved flag

The raw date/time need not leave the secure derivation environment.

## Frozen predictor

`Z_5_15 = 1` iff at least one standard Personality/Design activation falls in each of:

- `[251.375°, 257.000°)`
- `[88.250°, 93.875°)`

using the standard 13 Personality + 13 Design activations and the exact backward 88° solar-arc Design moment.

Canonical derivation must use the repository's verified Swiss Ephemeris path and provenance checks.

## Civil-time handling

Treat MBRN clock time as Norwegian civil local time and use frozen `Europe/Oslo` timezone rules for that date.

For an autumn DST-fold time that maps to two possible UTC moments, calculate both and accept the predictor only if it is invariant. Mark a non-invariant case unresolved. Flag impossible spring-gap times rather than silently repairing them.

## Frozen primary model

Linear regression:

`Activity ~ Z_5_15 + sex + birth_year + DOY_fourier_k1_k2 + TOD_fourier_k1_k2`

Use family/mother-cluster-robust standard errors.

Primary test: two-sided coefficient for `Z_5_15`; development-predicted direction is positive.

## Secondary analyses already declared

- prorated Activity score with at least 2/3 items
- item-level ordinal models
- singleton-only and one-child-per-mother sensitivities
- five-channel secondary predictor: `2-14 OR 5-15 OR 29-46 OR 6-59 OR 3-60`
- Gate 5 only, Gate 15 only, and Gate 5 OR 15 predictor controls

No secondary result may be used to redefine a failed primary 5–15 hypothesis.

## Eligibility stop

Before individual outcome values are inspected, confirm that MoBa questionnaire records can be linked to `FDATO` and `FKLOKKEN`, or that the custodian can derive the frozen predictor internally.

If this cannot be done, stop and record **dataset ineligible**. Do not inspect outcomes and do not count it as a failed replication.

## Access logistics

Current NIPH documentation requires MoBa applications through `helsedata.no`, a completed variable list, and a project leader affiliated with a Norwegian research institution. International collaborators are restricted to approved secure access platforms.

Public documentation used for this packet:
- https://www.fhi.no/en/ch/studies/moba/for-forskere-artikler/research-and-data-access/
- https://www.fhi.no/en/ch/studies/moba/for-forskere-artikler/moba-research-data-files/
- https://www.fhi.no/globalassets/dokumenterfiler/studier/den-norske-mor-far-og-barn--undersokelsenmoba/instrumentdokumentasjon/instrument-documentation-q5.pdf
- https://www.fhi.no/globalassets/dokumenterfiler/mfr-record_v541_ver2.pdf
