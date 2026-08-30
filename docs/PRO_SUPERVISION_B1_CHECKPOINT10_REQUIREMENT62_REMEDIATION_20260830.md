# Pro supervision: B1 checkpoint-10 requirement-62 remediation

Date: 2026-08-30

## Ruling

`OWNER DECISION REQUIRED: NO`

Pro found the B1 pre-content governance architecture substantively qualified, with 63 of the 64
controlling requirements established. Checkpoint 10 remains open only because requirement B1-62
requires every substantive artifact to have exactly one controlling requirement, while the v1
artifact manifest records one or more requirement identifiers per artifact.

This is a traceability-cardinality defect, not a scientific, privacy, construct, or mapping
failure. The deterministic chart foundation, Option B measurement-reliability architecture, B1
independent-first ordering, content embargo, role separation, freeze-before-mapping rule, separate
R/M/I lanes, and preservation of null or weak mapping outcomes remain qualified.

## Authorized bounded slice

`REQUIREMENT-62 TRACEABILITY-CARDINALITY CLOSURE ONLY`

Local additive work on `codex/astrohd-relationship-continuation` is authorized solely to:

- determine whether the existing manifest already has one controlling assignment or requires a
  superseding manifest;
- produce a single-assignment proof or superseding manifest;
- add validator tests for the exact cardinality and resolution conditions;
- correct the checkpoint evidence for requirement B1-62; and
- return a narrowly scoped checkpoint-10 closure packet.

Because the v1 manifest uses plural `requirement_ids` arrays containing multiple values, Route B
applies: preserve v1 unchanged and create a v2 manifest with exactly one
`primary_requirement_id` per substantive artifact plus optional, explicitly non-controlling
`supports_requirement_ids` cross-references.

## Required closure properties

- Exactly 33 substantive artifacts remain represented.
- Each artifact has one valid primary requirement in B1-01 through B1-64.
- Missing, multiple, unknown, malformed, duplicate, or non-string primary assignments fail closed.
- Secondary references cannot be treated as additional primary assignments.
- All 64 matrix requirements remain covered.
- Every matrix row resolves to a manifest-bound artifact and exact digest.
- No substantive artifact is omitted.
- A changed primary assignment changes the superseding-manifest digest.
- The v1 manifest, original matrix, conception, methods scan, governance contracts, schemas,
  firewall, threat model, owner dossier, all 48 protected paths, and accepted checkpoint-8 and
  checkpoint-9 artifacts remain byte-identical.
- Full tests, strict mypy, changed-file Ruff, privacy/history/build, diff, and cleanliness gates pass.

## Hard stops retained

No construct-specific scan, source-route or authorship selection, construct content, mapping work,
human work, push, PR action, merge, migration, deployment, or external mutation is authorized.
Return to Pro immediately if closure would require changing a scientific or governance artifact,
if a protected/accepted artifact changes, if the manifest cannot express honest single-primary
provenance, or if any test/privacy gate fails.

The source-route and authorship decision becomes mandatory only after B1-62 closes and Pro accepts
checkpoint 10.
