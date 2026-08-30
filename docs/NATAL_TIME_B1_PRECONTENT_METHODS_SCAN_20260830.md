# B1 pre-content generic methods scan — 2026-08-30

## Boundary and chronology

This bounded scan covers only source governance for independently conceived constructs, the
content embargo, provenance, discovery/validation separation, and the later mapping firewall. It
began only after the independent-conception snapshot was committed at
`496143ed1c04fce8b6f92f010d8f7bd7a11da30c`.

Bound provenance:

- owner B1 record commit: `cc6e8c3c05551c772d788d336994c3996d02ab78`;
- owner B1 record SHA-256:
  `64fe976c98c2b8ba82d86dc96e4bca2dee596338563dcc10c5934733e98b02af`;
- frozen conception Markdown SHA-256:
  `628f806f2dae876a58802113c7a2ef198420f13fc62d24e77ace922e187ce62d`;
- frozen conception JSON SHA-256:
  `0aab29cc1bdfae050581b3c7654603aad5fc8d195ce65a507a5245de8efa754e`.

The exact 20 queries, source versions and identifiers, eligibility decisions, exclusions, and
nonselection receipt are in
`state/NATAL-TIME-B1-PRECONTENT-SOURCE-LEDGER-V1.json`. Method-family dispositions and the
comparison with all eight independently conceived insights are in
`state/NATAL-TIME-B1-PRECONTENT-METHODS-DECISION-LEDGER-V1.json`.

The scan did not search for an instrument for a specific construct, select or prefer a source
route, or create construct or mapping content. It cannot establish that a future construct lacks
an established instrument. No copyrighted full-text corpus was downloaded or committed.

## Evidence and bounded decisions

### Define the construct and context before choosing an instrument — reuse directly

The official [COSMIN manual](https://www.cosmin.nl/wp-content/uploads/COSMIN-manual-V2_final.pdf),
the COSMIN instrument-selection overview, and FDA's final fit-for-purpose outcome-assessment
guidance all require the concept or construct and context of use to be explicit before instrument
selection. They also direct developers to examine existing instruments before developing or
modifying one. B1 therefore reuses this ordering. It does not instantiate a construct, population,
context of use, instrument, or method.

### Existing-work, near-neighbor, and proliferation checks — compose and adapt

COSMIN content-validity work and measurement-development guidance support systematic review of
existing instruments and assessment of relevance, comprehensiveness, and comprehensibility.
Primary work on construct proliferation, jingle/jangle problems, questionable measurement
practice, and scale development shows why names alone cannot establish distinctness and why a new
measure requires justification. The future construct-specific scan must therefore cover exact and
synonym terminology, neighbors, redundancy, established measures, and adverse evidence before any
bespoke content. This generic scan makes no overlap conclusion about a future construct.

### Content validity and chart-blind elicitation — compose; route remains unselected

FDA concept-elicitation guidance, COSMIN content-validity standards, and scale-development guidance
provide reusable process constraints for gathering and evaluating content. They do not determine
whether B1 should start from an established measure, chart-blind elicitation, observation, a
phenomenological taxonomy, independent theory, or a staged hybrid. Selecting among those routes—and
deciding whether humans, isolated model sessions, or both author future content—remains an owner
decision.

### Preregistration and discovery/evaluation separation — reuse directly

The Center for Open Science's Registered Reports model separates protocol review from knowing the
results and distinguishes confirmatory from exploratory work. Kriegeskorte and colleagues show why
using the same evidence for selection and evaluation creates circular analysis. B1 therefore
requires immutable freezes, separate evidence identities, and nonformulation evaluation. These
sources do not choose a mapping hypothesis or evaluation method.

### Theory-to-construct reasoning — baseline and composition only

Theory-construction methodology supports explicit definitions, inferential structure, and tests
that could fail rather than labels selected for apparent fit. B1 uses that as a baseline for a
future independently authored construct package and separately preregistered mapping. No theory,
construct, correspondence, ontology, feature, or model is entered now.

### Provenance, versioning, and post-exposure change control — adapt

W3C PROV supplies reusable entity/activity/agent, revision, and invalidation concepts. NIST's
generative-AI risk profile supports provenance and predeployment risk controls. B1 adapts these
into content hashes, append-only access/exposure history, explicit supersession, and preservation
of an original version and null result. This is governance architecture, not proof that content is
independent or scientifically valid.

### Model-context and connected leakage — adapt conservatively

Current primary work on data leakage and language-model benchmark contamination demonstrates that
training, retrieval, preprocessing, selection, and evaluation information can cross boundaries in
ways that invalidate an ostensibly held-out test. B1 conservatively treats repository access,
retrieval, prompt history, memory, embeddings, connected actors/sessions/sources, and fit-selected
examples as possible contamination routes. An AstroHD-exposed model cannot be made chart-blind by
an instruction. The architecture records exposure and fails closed on unknown provenance; it does
not claim that metadata controls alone guarantee absence of model-memory contamination.

## Independent-conception comparison

| Independent insight | Post-scan disposition | Bounded reason |
|---|---|---|
| Independence is information access and provenance, not an instruction | Composed/adapted | Provenance and contamination work supports access-state controls; the exact B1 firewall is project-specific. |
| Boundaries and reliability cannot move after mapping | Reused/composed | Preregistration and circular-analysis controls directly support freeze-before-test ordering. |
| Reliability, mapping, and incremental value need separate evidence | Composed | Discovery/validation separation supports distinct evidence; the exact three-lane registry is a B1 composition. |
| Null mappings must remain visible | Adapted | Results-independent review and immutable provenance support preserving failures; B1 adds its version rule. |
| Review existing work after definition and before new content | Reused | COSMIN, FDA, and scale-development guidance directly support the sequence. |
| Source selection can leak the hoped-for mapping | Adapted | Selection/evaluation circularity and provenance controls support treating source choice as exposure-sensitive. |
| A fresh model session can still be contaminated | Adapted | Leakage and benchmark-contamination work support the risk; no universal proof of model blindness exists. |
| Post-exposure revision is exploratory and needs new evidence | Composed/adapted | Preregistration plus revision/invalidation provenance supports the rule; its B1 application remains project-specific. |

No independent insight was superseded. None became construct or mapping content.

## Final bounded disposition

- **Reuse directly:** define before instrument selection; search existing instruments; specify
  context of use; freeze/preregister before confirmatory evaluation; separate formulation evidence
  from evaluation evidence.
- **Adapt:** opaque version identities, chart-blind authorship receipts, exposure/contamination
  states, append-only access provenance, separate mapping escrow, and post-exposure change control.
- **Compose:** content-validity, neighbor/redundancy, provenance, preregistration, and leakage
  controls into one pre-content governance boundary.
- **Reject as incompatible:** AstroHD-seeded generation, mapping-driven source selection or content
  revision, new-measure development before the future specific scan, and use of the same evidence
  to formulate and confirm a mapping.
- **Unresolved/owner-gated:** construct source route; future human, isolated-model, or hybrid
  authorship; actual construct and instrument; population/language/mode; reliability design; and
  every later mapping or incremental-value choice.

The strongest applicable baseline is established construct-definition and instrument-selection
guidance combined with preregistration, circular-analysis controls, and provenance standards. B1's
novel remainder is the AstroHD-specific information firewall and content-embargo auditability—not
a new measurement-development method.
