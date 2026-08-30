# Natal-time pre-inference study-design and falsification contract — 2026-08-30

## Status and authority

This is the frozen, synthetic-only study-design contract authorized by
`docs/PRO_SUPERVISION_CHECKPOINT_3_20260830.md`. Its machine-readable authority is
`state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json`. The JSON object is self-hashed after
removing only its top-level `contract_sha256` field and canonicalizing the remaining object with
sorted keys and compact JSON separators.

Phase-0 correction 2.4 preserves that v1 contract and its
`c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9` digest. Checkpoint-5
contract remediation also preserves the v2 metric contract at
`067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`. The operative
selected-subset and candidate/reference-domain semantics are now the content-hashed
`state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json` contract
(`75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe`) and
`docs/NATAL_TIME_PREINFERENCE_METRIC_SEMANTICS_V3_20260830.md`. V3 supersedes v2 only for
selected-subset adjacency and candidate/reference-domain compatibility; all other v2 rules and
every non-superseded v1 study-design surface remain authoritative. No v1 or v2 bytes were
overwritten.

This contract defines evaluation objects, documentary eligibility, leakage controls,
falsification baselines, and future measurement-development requirements. It does **not** define
participant inference. It contains no questionnaire question, response choice, scoring key,
chart-linked interpretation, estimator choice, prior, weight, operating threshold, participant
meaning, or participant-facing output. Any item-writing phase requires another ChatGPT Pro
checkpoint.

The qualified deterministic engine, enumerator, evidence state machine, identity specification,
and fixture artifacts are inputs to this design and are unchanged by it. The contract makes no
claim that Human Design is valid or that a birth time can be recovered from human responses.

## Formal evaluation objects

Let an interval be half-open, `[a, b)`, and let `mu(A)` be the summed elapsed duration of the
non-overlapping intervals in set `A`. Each interval in the definitions below is a whole qualified
full-state interval; an inferential layer may not manufacture an interval by splitting or merging
that identity unit.

### `C_i`: frozen complete candidate interval set

For participant `i`, `C_i` is the complete unordered set of maximal, engine-distinct intervals
over every manifest-valid candidate civil date, place, and timezone in the frozen
candidate-construction evidence domain. Candidate date, weekday, source, and lineage fields may
come from any source class accepted by the evidence state machine; they remain isolated from the
hidden value, precision, and derivatives of `T_i`. `C_i` and its construction manifest must be
content-hashed and frozen before inferential response evidence is collected or exposed.

Completeness means that no qualifying interval is omitted. There is no ranking, duration mass,
candidate weight, or favorable-story selection. A full-state change always creates an interval
boundary; intervals may not be merged across it. The reference standard `T_i` is unavailable to
candidate construction and cannot narrow or otherwise alter `C_i`.

### `T_i`: independently sourced documentary reference interval

For participant `i`, `T_i` is an independently sourced documentary birth-time interval that
preserves the source record's actual precision. Raw `T_i` remains in separate reference custody.
It is unavailable to candidate construction, measurement development, model development,
procedure execution, stopping, and returned-set construction.

Only an independent evaluator may compare `T_i` with a previously committed output. A
participant without an eligible independent documentary interval has no `T_i` for this study and
cannot contribute to a calibration or validation claim about recovery accuracy. Memory-only time
reports may later be studied for feasibility or reliability under separate authorization, but are
not accuracy ground truth.

### `S_i`: returned subset or explicit abstention

For participant `i`, `S_i` is either:

- any nonempty unordered subset of exact unchanged, whole intervals from the frozen `C_i`; or
- explicit abstention, in which case no candidate subset is returned.

An abstention is reported as its own outcome. It is neither a success nor an error. `S_i` cannot
be a newly manufactured window, a ranked list, a single best minute, or a candidate carrying a
probability or confidence label. Selected intervals need not be adjacent or contiguous, including
within one date. This does not relax candidate construction: `C_i` must still be complete and form
the canonical gap-free, non-overlapping partition within every declared civil-day domain.

### `D_i`: exact candidate-domain union and reference compatibility

`D_i` is exactly the set union of all unchanged intervals in `C_i`, not their convex hull. An
operative canonical `T_i` is `reference_domain_compatible` only when `T_i` is a subset of `D_i`.
It is `reference_domain_partially_incompatible` when it has positive-width overlap with `D_i` but
is not a subset, and `reference_domain_incompatible` when overlap width is zero, including
endpoint-only contact.

Partial and complete incompatibility issue no valid reference-accuracy result. Reference
intersection is the corresponding typed not-applicable state rather than true or false, and the
method receives neither credit nor error. The evaluator must not clip or otherwise mutate `T_i`,
fill a gap in `D_i`, or change `C_i`. Documentary width and domain status may remain diagnostics.

## Non-scalar evaluation frontier

The primary target is a joint coverage–temporal-width–state-count–abstention frontier. It is not a
correct-minute endpoint, raw rank, or weighted utility scalar. For each untouched validation
participant, the following components remain separate:

1. **Reference intersection.** If the procedure did not abstain and an eligible `T_i` is wholly
   contained in `D_i`, report whether the union of `S_i` intersects `T_i`. For abstention, absent
   `T_i`, or partial/complete domain incompatibility, record the corresponding typed
   not-applicable state instead of false.
2. **Temporal width retained.** If the procedure did not abstain, report `mu(S_i)`, `mu(C_i)`, and
   `mu(S_i) / mu(C_i)`.
3. **Full-state interval count retained.** If the procedure did not abstain, report `|S_i|`,
   `|C_i|`, and `|S_i| / |C_i|`.
4. **Abstention.** Report the explicit abstention indicator without recoding it as coverage,
   error, or success.
5. **Date coverage.** When `C_i` spans dates, report the candidate dates represented by `S_i`,
   their count relative to the dates represented by `C_i`, and whether a represented date
   intersects `T_i`.

Temporal width and full-state count are not substitutes: two returned sets can retain the same
elapsed duration but different numbers of chart states, or the same number of states but different
duration. Date coverage is also distinct. Participant and cohort reporting must preserve these
components and visible abstentions; no component may be combined into a utility, preferred
frontier point, or operating rule in this slice.

No coverage target, width target, state-count target, operating threshold, abstention threshold,
or preferred frontier point is selected.

## Documentary eligibility and precision

An eligible reference source must satisfy every rule below:

- It is documentary, not memory-only.
- It was created or maintained independently of the natal-inference study.
- Its provenance and custody lineage can be audited without exposing the value to candidate
  construction or inference.
- Its precision and rounding convention can be represented as an interval.
- It was not derived from astrology, Human Design, relationship interpretation, questionnaire
  responses, or candidate comparison.

Independently obtained civil or clinical birth records, certified extracts, and archive
transcriptions with an auditable chain to the underlying record are eligible source classes.
Memory, uninspected participant assertion, family recollection without an independently inspected
record, rectified times, relationship narratives, and sources that entered candidate construction
or inference are ineligible as accuracy ground truth.

Precision must not be manufactured:

- A bounded record remains the source-supported interval.
- A record rounded to five minutes, fifteen minutes, or one hour remains an interval at that
  precision; it is not promoted to an exact minute.
- When the rounding convention is known, preserve the complete compatible rounding cell.
- When the unit is known but the rounding direction is not, preserve the union or bounding
  interval of every source-compatible interpretation and mark the ambiguity.
- Preserve endpoint convention and timezone provenance with the reference receipt.

If `T_i` or any deterministic derivative of it influences `C_i`, candidate-evidence lineage,
wording, coding, model choice, fitting, procedure execution, stopping, or `S_i`, that participant
is development-only and invalid for calibration or validation. This prohibition does not block a
separately authorized independent calibration evaluator from comparing post-freeze method outputs
and committed `S_i` values with `T_i` for a predeclared calibration procedure. The method,
measurement specification, target, output form, and analysis must already be frozen; any
outcome-prompted methodological revision converts the exposed calibration component to
development and requires fresh calibration components.

## Data roles and access

Development, calibration, and locked validation are disjoint at the connected-component level.

| Role | Permitted purpose | Raw `T_i` available to method actors? | Contamination result |
| --- | --- | --- | --- |
| Development | All adaptive design: concepts/wording, features/coding, missingness, model family, priors, hyperparameters, operating or abstention rules, baselines, subgroups, and outcome transformations | No; only an independent evaluator may compare a committed `S_i` and release permitted development diagnostics | Any outcome-informed revision remains development and creates a new version |
| Calibration | Apply a predeclared calibration procedure to outputs from a method, measurement specification, target, output form, and analysis plan frozen before calibration access | No; an independent calibration evaluator alone may compare post-freeze outputs with the reference | If diagnostics or reference outcomes change methodology, every exposed component becomes development and fresh calibration components are required |
| Locked validation | Evaluate the fully frozen method and analysis plan after release of the validation lock | No; an independent validation evaluator alone holds the reference | If any validation information affects methodology, every exposed component becomes development and a new untouched validation cohort is required |

Candidate constructors can access candidate-domain inputs but not inferential responses or `T_i`.
The future procedure can access frozen `C_i` and admissible responses but not `T_i`. The reference
custodian can access `T_i` but neither response evidence nor `S_i`. An independent calibration or
validation evaluator gains access to the committed `S_i` and `T_i` only after the applicable
method and output freezes, and only for the predeclared role-appropriate comparison.

Calibration cannot become repeated development. Locked-validation records, responses, labels,
references, and outcomes remain inaccessible until method, baselines, analyses, and disclosure
plan are content-hashed.

## Connected-component split rule

Before role assignment, construct an undirected leakage graph whose participant identities are
vertices. Add an edge for:

- the same participant or repeated identity under any alias;
- partners or members of one relationship pair;
- members of one household;
- any transitive relationship connection; or
- a shared record source or custodian capable of transmitting reference labels.

Each complete connected component is assigned to exactly one of development, calibration, or
locked validation. No observation, alias, participant, partner, household member,
relationship-connected participant, or label-transmitting shared-source component may cross
roles. Freeze digests of the pseudonymous vertex manifest, reason-coded edge manifest,
component assignment, and role assignment before outcomes are available.

Relationship evidence is excluded from natal inference. If a later, separately approved
relationship-assisted exploration occurs, the relationship and its entire connected component
become permanently ineligible for natal calibration and validation.

## Synthetic leakage acceptance cases

The machine-readable contract declares one valid case and deliberate invalid cases as structured
synthetic role assignments, reference-access events, and contamination events. These are contract
tests, not participant records.

| Synthetic case | Expected result |
| --- | --- |
| Disjoint identities, households, relationships, sources, and custodian-only references | Eligible role assignment |
| Repeated observations of one participant split across roles | Invalidate the component; development-only |
| Aliases of one identity split across calibration and validation | Invalidate the component; replace affected later roles |
| Partners split across development and validation | Invalidate the relationship component; replace validation |
| Household members split across calibration and validation | Invalidate the household component; replace affected later roles |
| A transitive relationship chain crosses roles | Invalidate the complete transitive component |
| A label-transmitting record source crosses roles | Invalidate the shared-source component |
| `T_i` narrows candidate construction | Participant becomes development-only |
| `T_i` or its derivative enters measurement development | Exposed components become development-only; regenerate held-out work |
| `T_i` enters fitting or candidate selection | Participant becomes development-only |
| `T_i` affects stopping or whether a subset is returned | Participant becomes development-only |
| Calibration diagnostics change the method | Calibration becomes development; obtain fresh calibration components |
| A validation peek changes methodology | Validation becomes development; obtain a new untouched cohort |
| Partner or relationship evidence assists natal inference | Entire relationship component permanently ineligible for natal calibration or validation |

`hdmatch.natal_time.preinference_validation` constructs connected components from shared real
identity, alias, household, relationship, and label-transmitting record-source keys. It separately
enforces the post-freeze evaluator-only `T_i` access boundary. Automated tests execute every
structured case through that validator, require the clean calibration/validation comparisons to
pass, and require every deliberate leakage case to fail with the declared violation code and
explicit disposition.

## Complete baseline and falsification matrix

Every applicable control is mandatory for a future claim. Random-width and random-state-count
controls remain separate and are not probability models.

| Baseline | Preserved information | Falsification question |
| --- | --- | --- |
| Complete unordered candidate set | All of `C_i`; no responses | Does the proposal improve on deterministic candidate construction alone? |
| No pruning after responses | All of `C_i` plus the same response-collection process | Do responses add information beyond doing nothing inferentially? |
| Random/permuted subset matched on temporal width | Proposed temporal compression, not state count | Is performance more specific than temporal compression alone? |
| Random/permuted subset matched on full-state count | Proposed state-count compression, not temporal width | Is performance more specific than retaining that many states? |
| Calendar-only | Admissible calendar structure; no HD state | Does calendar structure explain the result? |
| Season-only | Admissible seasonal structure; no HD state | Does season explain the result? |
| Birthplace-only | Admissible place structure; no HD state | Does birthplace explain the result? |
| Timezone-only | Admissible timezone structure; no HD state | Does timezone explain the result? |
| Cohort-only | Admissible cohort structure; no HD state | Does cohort membership explain the result? |
| Source-quality-only | Candidate-source metadata; no HD state and no `T_i` | Does source quality explain the result? |
| Response-style-only | Missingness and generic response-process features; no content meaning or HD state | Does response style explain the result? |
| Participant-to-chart label permutation | Participant/connected-component clustering and nuisance structure | Does the result survive destruction of participant-chart association? |
| Plausible mismatched charts | Predeclared nuisance structure | Is fit specific to the concealed participant-chart association? |
| Blinded matching | Concealed identity and role-appropriate blinding | Do expectancy, identity cues, or generic personal validation explain the result? |
| Strongest ordinary non-HD model | Exactly the same admissible inputs and development opportunity | Is there incremental out-of-sample information beyond the strongest ordinary account? |

Beating random assignment alone is insufficient. A future HD procedure must improve out of sample
over the strongest applicable non-HD baseline and survive all applicable negative controls on
untouched connected components.

## Future measurement-development requirements

This section specifies evidence obligations only. It deliberately does not write content or select
participant semantics.

Any future, separately approved measurement phase must address:

- test–retest reliability while retaining participant clustering;
- inter-rater reliability with a predeclared coding unit, rater population, and agreement target;
- missingness without forcing unknown or context-dependent answers into support;
- acquiescence, response extremity, and other response-style effects;
- social-desirability effects;
- Forer/Barnum susceptibility through blinded and mismatched-description controls;
- item transparency and chart-feature cueing;
- construct overlap and redundant wording;
- language and population invariance for every contemplated claim population;
- blinded authorship, coding, and evaluation where practical, with unavoidable exposure recorded;
  and
- strict separation of development-only content generation from held-out calibration and
  validation labels.

### Proof that no measurement content was written

The JSON contract records zero questionnaire items, response choices, scoring keys, chart-linked
interpretations, selected participant semantics, selected estimator formulas, selected operating
thresholds, and accessed participant records. Its only measurement entries are the methodological
requirements above. The tests assert those zero counts, the new-checkpoint gate, and the absence
of executable inference or item-content fields.

## Methods dispositions

The machine-readable ledger uses only the checkpoint-authorized classifications:

- **Direct reuse:** measurement-reliability constraints, connected-component splitting, nested
  adaptation controls, and post-selection claim limits.
- **Adaptation:** interval-preserving reference representation, future calibration principles,
  explicit abstention, and disclosure governance.
- **Baseline only:** participant/component permutation and negative controls.
- **Incompatible:** traditional natal-rectification heuristics as a direct method or evidentiary
  basis.
- **Unresolved/experimental:** natal priors and conformal/set-valued procedures pending an
  established target, appropriate grouped data, and later authorization.

No estimator is selected. Every ledger entry states what evidence would be required before use.
The underlying literature dispositions and citations are preserved in
`docs/NATAL_TIME_METHODS_SCAN_20260830.md`.

## Machine verification

`tests/unit/test_natal_time_preinference_design_contract.py` verifies:

- schema identity and the canonical self-hash;
- exact `C_i`, `T_i`, and `S_i` definitions and set constraints;
- separate non-scalar evaluation components;
- documentary eligibility and precision preservation;
- completeness of the baseline matrix;
- role access and contamination rules;
- executable connected-component/reference-access validation and every structured synthetic
  leakage case;
- the item-writing checkpoint gate and zero-content proof; and
- fail-closed forbidden-semantics flags.

The contract authorizes no participant execution, recruitment, public release, push, merge,
migration, or deployment.
