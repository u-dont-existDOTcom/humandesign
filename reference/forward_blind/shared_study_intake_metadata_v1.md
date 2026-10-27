# Separate shared-study intake metadata

This utility validates a **private, separate metadata file**. It does not collect an interview,
calculate a chart, change a primary or CF003 record, update a prediction freeze, submit anything,
or authorize scoring. It accepts no birth tuple, identity/contact fields or chart/profile values.

Copy `shared_study_intake_metadata_template_v1.json` to a private directory outside the repository.
The blank template deliberately fails validation: do not invent IDs, timestamps, hash links,
answers or consent just to make it pass. Record actual consent to this research use. Keep the
original private birth record separate and link its exact-byte SHA-256 hash.

## Record meanings

- Use the participant's pseudonymous ID and the actual study ID. `selected_system_ids` is the
  study's declared selection, not a global list or a new questionnaire. The validator checks the
  record's internal consistency; it cannot establish that the study or consent is legitimate.
- `collection_stage` is `trusted_intake_before_interview` or `separate_post_freeze`.
  The second stage requires `primary_record_sha256` for the exact frozen primary file; the first
  forbids that field's value. This records the asserted stage, not proof of a freeze or chronology.
- `recorded_at_utc` is an explicit timezone-bearing recording timestamp, never a birth time or
  behavioral-event date. `source` identifies self-report, supplied record, transcription, an
  existing private record, or unknown. `source_record_sha256` may link the exact source when known.
  Use separate records for different collection stages or source batches; do not flatten them.
- `birth_quality.time_source` reuses the existing intake meanings: `certificate`, `hospital_record`,
  `family_record`, `memory`, `rectified`, `unknown`. `stated_uncertainty_seconds` is nonnegative
  or null. It does not validate the source or make a rectified time independently observed.
- `reported_uncertainty_interval`, when already stated by the source, carries signed
  `lower_offset_seconds` and `upper_offset_seconds` relative to the linked birth record's nominal
  time, plus `source` (`participant_statement` or `source_record`). Preserve the reported bounds;
  do not derive an interval, a midpoint or symmetry. This helper never propagates uncertainty
  through a chart calculation; that remains the selected study's calculation contract.
- Each `system_knowledge` entry identifies one selected `system_id`. `familiarity` accepts `none`,
  `heard_of_it`, `basic`, `intermediate`, `advanced`, `unsure`, `prefer_not_to_say`, `unknown`, or
  `not_asked`. `own_profile_known` and `prior_personal_interpretation` accept `yes`, `no`, `unsure`,
  `prefer_not_to_say`, `unknown`, or `not_asked`. Store the labels only, never what the profile was.
- Omitted knowledge fields or system entries become `unknown`. Explicit `not_asked`, decline,
  uncertainty and `no` remain different values. Missing uncertainty remains null, never zero.
  The two existing CF003 familiarity items and their timing are unchanged by this utility.

No behavioral wording is added. Keep this metadata outside the blind interviewer/reviewer input.
Any study-specific recruitment, consent, source-quality, blinding and measurement requirements
still apply. A successful structural check is not scientific validation or evidence that the
linked files, consent, source labels or stage assertions are true.

## Use on private files

Run from the repository with its Python dependencies installed:

```bash
PYTHONPATH=src python3 scripts/validate_shared_study_intake.py /private/input.json
PYTHONPATH=src python3 scripts/validate_shared_study_intake.py /private/input.json --output /private/metadata.canonical.json
```

Validation alone leaves the input untouched. Output is optional, uses the project's canonical
JSON format, includes explicit unknowns, has private file permissions on POSIX systems, and never
replaces an existing file. The output directory must already exist. Corrections create a new
version in a new file; they do not overwrite a frozen primary, CF003 or prediction record.

Successful output reports only schema, canonical hash and whether a file was written. Invalid
input diagnostics show field paths and error types without echoing submitted values. Exit status
is zero on success and two on validation or output failure. Duplicate JSON keys and non-finite
numbers are rejected. Keep all completed records out of the public repository.
