# Separate shared-study intake metadata utility

## Authority and scope

Parent owner outcome: improve the shared Life Patterns questionnaire for the additional systems
while preserving the neutral interview and existing answers. The owner reported installing the
previous GPT package and said “done continue.” Parent delegated the separate trusted-intake
metadata utility; the parent handles the optional questionnaire runtime integration.

This isolated branch is based on runtime source `7de212f027e14c198fb58dc91d11df3068d58e56`.
It adds no behavioral questions, coding/model rules, endpoints, deployment, participant collection,
or modification of the older intake service/HTML. Existing primary, CF003 and prediction records
remain outside the writer's scope. No actual private records were read or generated.

## Implemented

- Strict immutable `SharedStudyIntakeMetadata` model in
  `src/hdmatch/participant/shared_intake_metadata.py`, with selected-study system checks,
  consent validation, explicit missingness, stage/source labels and private birth-record hash link.
- Existing `time_source` and `stated_uncertainty_seconds` meanings, plus optional explicitly
  source-reported relative interval bounds. No birth tuple or chart/profile values are accepted.
- Post-freeze stage requires the primary record's hash; the pre-interview stage forbids that link.
  Omitted selected-system knowledge is represented as unknown, never as no or unasked.
- CLI `scripts/validate_shared_study_intake.py` validates private JSON, rejects duplicate keys,
  reports redacted structural diagnostics and optionally creates a new canonical private file.
- Blank template deliberately cannot pass as a consented record; companion guide documents
  actual-use steps, meanings and limits.

## Verification and limits

Executed in the isolated worktree:

```bash
PYTHONPATH=src /workspace/scratch/42e21f1a0b5d/life-patterns-venv/bin/python -m pytest tests/unit/test_shared_intake_metadata.py -q
/workspace/scratch/42e21f1a0b5d/life-patterns-venv/bin/python -m ruff check src/hdmatch/participant/shared_intake_metadata.py scripts/validate_shared_study_intake.py tests/unit/test_shared_intake_metadata.py
git diff --check
```

Result: **39 tests passed in 1.27s; Ruff and diff whitespace check passed.** Tests use synthetic
records only. Coverage includes unselected/duplicate systems, unknown versus explicit answers,
uncertainty and interval bounds, consent rejection, freeze links, forbidden target/identity fields,
timezone handling, canonical stability, strict JSON, private append-only output and CLI redaction.

The helper verifies structure and internal consistency. It does not establish consent legitimacy,
linked-file existence/authenticity, chronological truth, scientific eligibility or predictive
validity. Source quality is retained, not adjudicated. No full scientific/model suite is relevant
to this additive metadata utility. Parent should integrate/review this bounded change before
delivery; no independent publication or production activation was performed.
