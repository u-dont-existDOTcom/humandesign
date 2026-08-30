# Natal-time B1 checkpoint-10 requirement-62 closure packet

Date: 2026-08-30

## Requested ruling

Please answer first with exactly `OWNER DECISION REQUIRED: YES` or
`OWNER DECISION REQUIRED: NO`, then accept or reject the requirement-62 traceability-cardinality
closure. If checkpoint 10 is accepted and the source-route/authorship choice is now required,
identify that exact owner decision and stop. This packet does not authorize a source choice,
construct-specific search, construct content, mapping content, human work, push, merge, migration,
deployment, or external mutation.

## Pro finding and authorized scope

At the first checkpoint-10 review, Pro returned `OWNER DECISION REQUIRED: NO`, qualified 63 of 64
requirements, and found only B1-62 unestablished. The v1 manifest used plural `requirement_ids`
arrays, while B1-62 requires each substantive artifact to have exactly one controlling
requirement. Pro classified this as a traceability-cardinality defect rather than a scientific or
privacy failure and authorized only `REQUIREMENT-62 TRACEABILITY-CARDINALITY CLOSURE`.

The exact ruling and retained hard stops are recorded at
`docs/PRO_SUPERVISION_B1_CHECKPOINT10_REQUIREMENT62_REMEDIATION_20260830.md`, SHA-256
`d43372ce36646899caecc849a65e1062cb92ae07ac4b946847bdd17c4170be86`.

## Closure route and identities

Route B applies because v1 genuinely contains multiple requirement identifiers for many
artifacts; describing it as single-primary would be inaccurate. V1 remains unchanged. The local
closure topology is:

- traceability implementation commit `c7ba8d2bfc6d5546754036a90e4860925bb2b704` / tree
  `2d26b14868b72a0fd4fbac1cd2f2b636a29fe82b`;
- byte-evidence child `506199ebdb94f234be33e542ff8d4229b592337c` / tree
  `f2bdd608a497812a98b725f0d0dfe26d80223edf`;
- superseding v2 manifest SHA-256
  `2e43991833150b590bff56abd4501a4c38bcc8366227e25ede5cdb88d21354f9`;
- closure receipt SHA-256
  `f1617270faf0f7e4e97f59a60b8da9e39ca97793796865f0b971e2e1003649d0`;
- validator SHA-256
  `b2f0a8da9733b35f4339ba6d3baf2bd9971ad9956b2a53549db57c31e3d6e990`;
- validator-test SHA-256
  `ff009cb3d40fe3afba0af749b3aa618c4e284c4a2faa12b8f6c9240aec63d4fe`.

The final documentation-only child that adds this packet and current-state pointers is supplied
with its exact tree and exact-head gates in the Pro return rather than embedded self-referentially.

## Single-primary semantics

`state/NATAL-TIME-B1-ARTIFACT-MANIFEST-V2.json` preserves the same 33 substantive artifact paths
from v1 and gives each exactly one scalar `primary_requirement_id`. Optional
`supports_requirement_ids` are explicitly typed as non-controlling cross-references and cannot
create another primary assignment.

Two matrix rows depend on pre-B1 immutable artifacts that were never members of the v1 33-item
substantive set. V2 binds them separately as `matrix_dependencies`: the 48-path protected-baseline
closure and the accepted Option B artifact manifest. This keeps the substantive count honest at 33
while allowing every matrix row to resolve to a manifest-bound exact digest.

The validator fails closed for:

- missing, null, empty, list-valued, non-string, malformed, or unknown primary assignments;
- multiple or duplicate primary representations;
- duplicate artifact paths;
- silent artifact omission;
- unknown artifact fields that could smuggle an additional primary assignment;
- duplicate secondary references; and
- a primary requirement repeated as a secondary reference.

It also proves that all 64 ordered matrix rows remain present, every row resolves to a substantive
artifact or immutable dependency at the exact recorded digest, all 33 original substantive paths
remain represented, and changing a primary assignment changes the canonical manifest digest.

## Preserved evidence

The following bytes remain unchanged:

- v1 33-artifact manifest SHA-256
  `9755682f8e4b0e634d36ef1a4170b9caa919cf7a3d8e4a3216e6371065298f11`;
- original 64-row acceptance matrix SHA-256
  `104d8b8f920a64250ca78ca0411186bebe92bbe5e1af2a3c1ec62418ff797861`;
- both independent-conception artifacts;
- generic methods scan and ledgers;
- construct-source governance, schemas, role/access matrix, freeze gate, mapping firewall, claim
  lanes, post-freeze change control, threat model, unresolved-decision register, and owner dossier;
- all 48 protected paths; and
- all accepted checkpoint-8 and checkpoint-9 scientific artifacts.

No production `src/` path changed. The only executable changes are test-only traceability
validation and its tests.

## Focused closure verification

At the evidence child:

- all 64 original B1 acceptance nodes pass;
- the expanded focused file passes 95 tests;
- changed-Python Ruff passes; and
- JSON parsing and `git diff --check` pass.

The documentation-only child receives the complete exact-head full suite, strict mypy, changed-file
Ruff, canonical privacy/history/build, protected/accepted comparisons, JSON/digest, diff, and clean
index/worktree gates. Their exact results are supplied in the Pro return.

## Claim boundary and prohibited-action confirmation

This closure establishes traceability cardinality only. It adds no construct, source, instrument,
item, prompt, response, domain, measurement model, metric, threshold, population, language, mode,
burden, reliability design, mapping ontology, mapping feature, AstroHD hypothesis, chart field, live
record, or progression rule.

No source route or authorship class was selected. No construct-specific scan, construct content,
AstroHD mapping work, human workflow, participant/reference/relationship/chart access, recruitment,
data collection, production change, push, remote branch, PR action, GitHub governance change,
merge, rebase, cherry-pick, squash, force update, Railway mutation, migration, deployment, secret
read/removal, public ledger, publication, release, or disclosure occurred.

If checkpoint 10 is accepted, the next gate is the owner choice Pro already identified: the
construct-source route and whether humans, a fresh isolated model context, or a separated hybrid
may author future chart-blind content. The worker must stop for Joel if Pro says that choice is now
required.
