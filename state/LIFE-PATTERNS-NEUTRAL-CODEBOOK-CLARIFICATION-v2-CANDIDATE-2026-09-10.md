# Life Patterns neutral codebook clarification v2 — candidate — 2026-09-10

**Status:** Development-only, theory-blind candidate for a separate fresh blind review. It is not an implemented coding manual or response schema.

## 1. Scope and authority

This document is a versioned clarification overlay for `LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`. The historical v1 codebook remains immutable and is not overwritten. The historical non-action classification, normalized ambiguity resolutions, recurrence-v2 policy, and v2 response structures also remain immutable records.

The repair problem is the frozen overlap/absence audit at commit `7ea0641e0913815306f8c182be5e7e8b18115fff`, raw audit SHA-256 `37642f31135f3d446488a3a0a6736468b30b6114d5a292bcaf01096d65fb16e6`, and summary SHA-256 `7184f89a9d6c8fa0560e0ceba07287f101f559ddcf872b3db62e39de34cb7b47`.

Only changed or clarified observables are specified below. Unmentioned v1 wording remains candidate wording subject to this document's global rules. No target-theory information was available or used.

## 2. Global v2 candidate rules

### 2.1 Facets, stages, and relations

1. A response is organized as an observable containing one or more **facet groups**. A facet may allow zero, one, or multiple supported values according to its definition.
2. A bounded act or meaningful state transition is an **event/stage**. Values from different facets may be co-present on one event/stage. Co-presence does not imply temporal order.
3. Temporal order is recorded only between event/stage identities when the source establishes order. Unknown order stays unknown. A single relation over an observable's entire value list is prohibited.
4. Multiple values on one event/stage describe that event at different levels or facets; they are not separate behavioral events.

### 2.2 Evidence-unit and independence rule

Every observed event/stage receives one `evidence_unit_id`. Every value assertion points to the event/stage and evidence unit it describes. Assertions derived from the same act, choice, utterance, terminal course, or endpoint history share that evidence unit even when they occupy different facets.

Neither a more specific value nor several co-present facet labels create additional independent evidence. Counts of values must never be used as counts of episodes or opportunities. A composite or derived trajectory adds no evidence unit beyond its component events. Recurrent support follows the recurrence-v2 evidence policy: retellings and self-selected examples do not become independent frequency observations, and opportunity-level frequency requires an eligible sampling frame.

### 2.3 Missingness and absence components

`not reported`, `unknown`, transcript silence, a partial transcript, and an unbounded follow-up are evidence missingness, not behavioral nonoccurrence.

An absence-dependent value or component must name all of the following:

- the exact action or proposition asserted not to have occurred;
- the person or actor to whom that absence applies;
- the meaningful opportunity/window;
- awareness, opportunity, reasonable feasibility, and established nonoccurrence;
- exact source provenance for each required gate fact.

All four gate elements must be established for the named proposition. A gate for one absence target cannot authorize a different absence target. In a hybrid value, the affirmative component and the absence component are separately asserted and separately sourced; failure of the absence gate makes that component insufficient even when the affirmative component is observed.

### 2.4 Specificity and cumulative coding

For one event/stage and one facet, assign the narrowest supported value. Do not also assign a broader value when the broader value adds no distinct fact. A broad and narrow value may both appear only when they describe different sourced components or different event/stages; they then share an evidence unit if they still arise from the same act.

Cross-facet values may co-occur when each facet fact is independently established, but the co-present labels still share the event's evidence unit. When a boundary below cannot be established, mark the affected facet `insufficient` and preserve the uncertainty; do not choose a favorable or apparently precise label.

### 2.5 Response states

`observed`, `insufficient`, and `not_applicable` apply at observable, facet, and event/stage scope under the v3 contract candidate. `not_applicable` requires affirmative evidence that the relevant prerequisite is absent. Non-mention is `insufficient`, not `not_applicable`. An observed facet contains at least one sourced assertion; an insufficient or not-applicable facet contains none.

### 2.6 ID disposition

- Historical `R07-a` remains preserved in v1 and is retired from v2 candidate assignment in favor of the already normalized `R07-a1` and `R07-a2` split.
- Historical `R16-d` remains preserved in v1 and is retired from v2 candidate assignment in favor of the already normalized `R16-d1` and `R16-d2` split.
- `R19-g` remains preserved in v1 and is retired from v2 candidate substantive assignment. Its chronology is represented by ordered component events using stable IDs `R19-a`, `R19-c`, and/or `R19-d`.
- No other blocker repair creates, renames, or retires a subcode. Hybrid values retained below are represented as separately sourced affirmative and absence components under the v3 contract.

## 3. Observable-specific clarifications

### 3.1 NBM-R02 — Information Seeking

**Facets:** acquisition method (`R02-a`–`R02-e`) and search disposition (`R02-f`, `R02-g`). Acquisition methods may co-occur on one search event.

- `R02-f` requires a search already underway, an affirmative stop to that search, and proceeding with the information already available.
- `R02-g` requires an affirmative decision to forgo otherwise feasible further information acquisition despite a recognized gap, but is used only when the complete `R02-f` pattern is not established.
- For the same search-termination decision, `R02-f` replaces `R02-g`. `R02-g` remains available when no prior search is established or when proceeding on available information is not established. Distinct later forgoing decisions may be separate ordered stages.
- The same stop/forgo decision never creates two evidence units.

### 3.2 NBM-R03 — Action With Unresolved Uncertainty

**Facets:** action extent, decision procedure/ownership, and temporal disposition.

- `R03-c` is an affirmative deferral tied to identified information, a stated revisit time, or a stated condition. It is not inferred from inactivity.
- `R03-h` asserts that no focal course began or was carried out during a named feasible action window. It requires the four-part gate for that exact focal-action absence.
- In the same window, established `R03-c` replaces `R03-h`; the deferral is the response. `R03-h` may follow `R03-c` only in a later distinct window after the stated revisit time/condition becomes due and no action or renewed deferral occurs.

### 3.3 NBM-R05 — Choice Construction and Resolution

**Facet groups:**

1. `option_construction`: `R05-O1`, `R05-O3`, `R05-O4`, `R05-O5`, `R05-O6`;
2. `alternative_search_disposition`: `R05-O2`;
3. `choice_resolution`: `R05-R1`–`R05-R9`.

Values in different groups may be co-present on the same event/stage. Resolution stages may be temporally ordered. The number of labels on one choice event never becomes the number of independent choice observations.

#### R05-O2 decomposition and evidence

`R05-O2` is retained as a two-component assertion:

- affirmative context component: an existing option or designated default was accepted or selected; and
- exact absence component: the narrator did not search for additional alternatives during a named meaningful, feasible preselection search opportunity.

The four-part gate applies only to `absence_of_additional_alternative_search`. Acceptance alone, a fast choice, and silence about comparison or search cannot establish `R05-O2`. The affirmative selection procedure is coded separately in the resolution facet only when its own evidence supports `R05-R1` or `R05-R4`.

#### R05-R1 and R05-R4

- `R05-R1` means the narrator affirmatively used a first-acceptable stopping strategy: an option was selected when it met an expressed acceptance threshold, without an established designated default, prior commitment, or other explicit decision rule determining the result. Delete the v1 alternative phrase `without reported comparison`; missing comparison information is insufficient, not evidence of no comparison.
- `R05-R4` means a stated rule, prior commitment, or designated default determined the selection. The rule/default must be identified in the source.
- For one resolution event, `R05-R4` replaces `R05-R1` when an explicit rule, prior commitment, or designated default determined selection. Both may appear only at distinct stages with distinct sourced procedures.
- `R05-O2` may co-occur with either resolution value because alternative search and selection procedure are separate facets, but all labels from one selection act share one event and evidence unit.

#### Comparison, constraint, and rule precedence

- `R05-R2` records comparative trade-off or evaluation across at least two alternatives on stated dimensions.
- `R05-R3` records elimination of one or more alternatives because an identified hard eligibility constraint was applied.
- `R05-R4` records final resolution determined by a stated rule, prior commitment, or designated default rather than a comparative trade-off.
- A criterion used only to eliminate an option is `R05-R3`, not also `R05-R2`. A criterion used to compare degrees across surviving alternatives is `R05-R2`. If elimination is followed by a separate comparison, record ordered `R05-R3` then `R05-R2` stages.
- A hard eligibility constraint that eliminates all but one option is `R05-R3` only, even though elimination determines the result. `R05-R4` is reserved for a rule, prior commitment, or designated default that selects among options still eligible after any constraint step. If a constraint step is followed by a separate final-rule step, record ordered `R05-R3` then `R05-R4` stages.

#### Combination boundary

- `R05-O6` applies when elements are combined to construct a new candidate option, whether or not it is ultimately selected.
- `R05-R9` applies when combination itself is the final resolution rather than selection of one existing option.
- If one combining act both creates and immediately adopts the combination, both cross-facet assertions may be retained on the same event/stage, with the same provenance and evidence unit; they are not independent observations.

### 3.4 NBM-R06 — Decision Revision

`R06-h` means the narrator affirmatively abandons the previously selected course. The existence or identity of a replacement is not part of the substantive value. If subsequent-course information is absent, store `UNK` at the subsequent-course scope. Never infer that no replacement existed. A later replacement, when reported, is a later event/stage and does not invalidate the earlier abandonment.

### 3.5 NBM-R07 — Preparation and Sequencing

**Facet groups:** preparation extent (`R07-a1`, `R07-a2`), preparation type (`R07-b`–`R07-h`), and transition status (`R07-i`). Preparation types may be co-present; a later failure to transition is a distinct ordered stage.

- `R07-a1` is affirmative limited preparation and may co-occur with supported type values on the same evidence unit.
- `R07-a2` is no preparation during a named feasible pre-action window, followed by proceeding; it is mutually exclusive with `R07-b`–`R07-h` for that window and requires the gate for `absence_of_concrete_preparation`.
- `R07-i` contains an affirmative continued-preparation component and an absence component `no_transition_to_focal_action_during_the_defined_feasible_observed_period`; only the absence component receives the gate.
- `R07-b` is assembling, creating, checking, or configuring material needed to perform the focal action. Mere placement is insufficient.
- `R07-g` is intentionally positioning an already available resource/material at a useful place, time, or access point in advance so it is ready without later retrieval or setup. Mere assembly or checking is insufficient.
- If one sourced act both materially prepares and prepositions, both values may be attached to that one event and evidence unit. Otherwise use the one matching the act; never duplicate ordinary placement as both values.

### 3.6 NBM-R10 — Allocation Among Competing Courses

**Facets:** allocation schedule, allocation mechanism, and displaced-course status.

- `R10-a` is the specific serial schedule in which the current focal course is completed before resource moves to another course. It replaces every other schedule value for that same allocation interval.
- `R10-c` applies when the resource is partitioned into identified non-overlapping blocks, the current course is not completed before the first move, and the observation window contains no return to a previously left course and no concurrent interleaving.
- `R10-d` applies when the schedule includes a return to a previously left course or concurrent/fine-grained interleaving within the allocation window.
- `R10-e` is the fallback serial-order value when courses are placed in non-overlapping temporal order but the narrower `R10-a`, `R10-c`, or `R10-d` rule is not met.
- Apply the deterministic schedule decision order `R10-a` finish-current-first; otherwise `R10-d` return/interleaving; otherwise `R10-c` explicit block partition; otherwise `R10-e` other serial order. The four are mutually exclusive for one allocation interval. A changed schedule is a later event/stage.

### 3.7 NBM-R11 — Goal-Course Response to Obstruction or Disruption

`R11-G6` is an affirmative stop event. `R11-G7` is a later status asserting no return to the focal goal at any point in a stated defensible follow-up window.

Do not derive `R11-G7` from the stop statement itself. Both values may appear only when a distinct follow-up window supplies evidence for nonreturn; record `R11-G6` then `R11-G7`, bind both to the same goal-course episode, and do not count the later status as a second independent disruption observation. Without distinct follow-up evidence, use `R11-G6` only; without an affirmative stop but with a sufficient nonreturn window, use `R11-G7` only.

### 3.8 NBM-R12 — Method Adjustment Across Attempts or Feedback

**Facet groups:** structural relation to prior method (`R12-a`–`R12-d`, `R12-g`, `R12-h`) and directional resource/scope adjustment (`R12-e`, `R12-f`). Before assigning a structural value, identify the earlier method's operative steps and the later method's operative steps.

- `R12-b` applies when one bounded component changes while the earlier method's core operative sequence remains usable and recognizable.
- `R12-c` applies when the later attempt no longer uses the earlier method's core operative sequence as a functioning route. Replacing one load-bearing component is `R12-c` only when that replacement makes the earlier core route no longer operative; otherwise it is `R12-b`.
- `R12-d` applies when the later attempt simultaneously retains at least one operative step from each of two separately identifiable methods. Historical influence or superficial carryover does not count. If the earlier core route is no longer operative and no second method remains active, use `R12-c`, not `R12-d`.
- `R12-e` and `R12-f` are narrower directional descriptions. When the only component change is fully expressed as added resources (`R12-e`) or simplification/reduced scope (`R12-f`), use the directional value and suppress `R12-b` for that same change. Use `R12-b` as well only for a separately identified additional component change; attach both to the same event/evidence unit if one attempt contains both facts.
- `R12-h` is the affirmative discontinuation of the identified method. Replacement status is separate; missing replacement information is `UNK` and never means no replacement existed.
- If core continuity or retained-method identity cannot be established, the structural facet is `insufficient`; do not force `R12-b`, `R12-c`, or `R12-d`.

### 3.9 NBM-R13 — Outcome Checking and Feedback Acquisition

- `R13-b` is a deliberate self-check performed to determine or verify accuracy, completion, receipt, consequence, or quality before that outcome has already been established or accepted. This includes a check immediately after the focal action when the check establishes the outcome.
- `R13-f` is a retrospective re-examination after the focal outcome has already been established, experienced, or accepted; it reviews the completed course or known outcome rather than determining it for the first time.
- The same check cannot receive both values. If the source does not establish whether the outcome was already known before the review began, the timing facet is `insufficient`.

### 3.10 NBM-R14 — Response to a Recognized Possible Error

For `R14-i`, the exact absent proposition is `no_remedial_error_response_during_the_defined_feasible_window`. A remedial error response is one or more of: correcting the original work (`R14-c`), mitigating downstream effects (`R14-d`), informing an affected person so they can respond (`R14-e`), installing a prevention step (`R14-f`), or an OS action with one of those direct functions.

Verification (`R14-a`), acknowledgment alone (`R14-b`), dispute (`R14-g`), and concealment (`R14-h`) do not by themselves negate `R14-i`. Informing an affected person under `R14-e` does negate it. The four-part gate applies to the named remedial-action set and window; silence about remediation is insufficient.

### 3.11 NBM-R15 — Endpoint Completion and Closure

**Facet groups:** endpoint extent/timing (`R15-a`, `R15-b`, `R15-c`, `R15-l`), endpoint modification/transfer (`R15-d`–`R15-g`), affirmative terminal disposition (`R15-h`, `R15-i`, `R15-j`), and later closure (`R15-k`). All assertions remain attached to the one endpoint trajectory unless a genuinely new endpoint/opportunity begins.

- `R15-a` means the defined endpoint was completed substantially as specified by its due time or triggering condition. `R15-b` means it was completed after that due time/condition. They are mutually exclusive for one endpoint assessment.
- `R15-c` requires affirmative completion of at least one defined endpoint component plus established noncompletion of at least one other defined component during the assessment window. The gate attaches only to the named remaining component(s).
- `R15-l` means no defined endpoint component was completed during the named feasible window. It is mutually exclusive with `R15-a`, `R15-b`, and `R15-c` for the same window.
- `R15-h` requires an affirmative choice, statement, or act leaving a named element open. It does not itself establish partial completion or general noncompletion. It may co-occur with `R15-c` only when some components were actually completed and the remaining named component was established incomplete; both share one endpoint evidence unit.
- `R15-i` is explicit withdrawal/rescission of a commitment. `R15-j` is an affirmative stop in work toward the endpoint without withdrawal/rescission, transfer, substitution, or agreed closure. `R15-i` replaces `R15-j` for the same terminal act.
- For the same terminal event/window, `R15-i` or `R15-j` replaces `R15-l`; do not add the general absence value merely because the affirmative termination entails noncompletion. `R15-l` may precede a later withdrawal/stop only when a distinct earlier assessment window independently establishes noncompletion.
- `R15-k` requires a distinct return after an interruption to perform later closure. When that return produces late completion, `R15-k` and `R15-b` may describe the same return/completion event but share one evidence unit; `R15-b` is the endpoint timing state and `R15-k` the follow-up act.
- Renegotiation before (`R15-d`) versus after (`R15-e`) the due point is mutually exclusive for the same renegotiation event. An assented modified or substitute endpoint becomes the comparison endpoint for later extent coding.

### 3.12 NBM-R16 — Help Seeking and Help Use

**Facet groups:** request timing/trigger (`R16-a`, `R16-b`, `R16-c`), indirect/nonrequest pathway (`R16-d1`, `R16-d2`, `R16-l`), offer response/use (`R16-e`, `R16-f`, `R16-g`), task transfer (`R16-h`), help type (`R16-i`, `R16-j`), and source breadth (`R16-k`). Request/offer events may be ordered; help type and breadth may be co-present on those events.

- `R16-d1` is an affirmative indirect signal intended to invite or obtain help; it makes no claim that a direct request did or did not occur outside the bounded stage.
- `R16-d2` requires affirmative waiting for an offer plus the exact absence `no_direct_help_request_during_the_named_feasible_request_window`.
- `R16-l` is the general absence `no_direct_or_otherwise_explicit_help_request_during_the_named_feasible_request_window` and applies only when no more specific waiting-for-offer strategy is established. An indirect signal is not an explicit request.
- For the same nonrequest window, `R16-d2` replaces `R16-l`. `R16-d1` may co-occur with `R16-d2` when an indirect signal and subsequent wait without direct request are both established. It may instead co-occur with `R16-l` when an indirect signal and gated nonrequest are established but no wait-for-offer strategy is established. Co-present values share one evidence unit. A later direct request is a later ordered stage.
- `R16-e`, `R16-f`, and `R16-g` are mutually exclusive for the same offer and use window. Different offers or a later reversal require distinct ordered stages.
- Timing, help type, and source breadth labels attached to one request do not become separate help-seeking observations.

### 3.13 NBM-R18 — Communication of Own Need, Limit, or Uncertainty

**Facet groups:** timing (`R18-a`, `R18-b`, `R18-f`), directness (`R18-c`), content extent/withholding (`R18-d`, `R18-h`), channel (`R18-e`), and revision (`R18-g`).

- `R18-c` means the affirmative communication is indirect or a hint. It makes no claim about how much of the condition was communicated or why anything was omitted.
- `R18-d` has an affirmative component identifying the communicated subset and an absence component naming the relevant part not communicated during a sufficiently observed communication opportunity. No withholding intent is inferred. The absence component receives its own four-part gate.
- `R18-h` requires an affirmative decision or act to withhold a named relevant part despite a feasible communication opportunity. It is not inferred from partial disclosure or transcript silence.
- When one event is both indirect, partial, and intentionally withholding, the supported facet assertions may co-occur, but all share the communication event's evidence unit. `R18-h` supplies the intentional-withholding fact; `R18-d` supplies content extent; neither may be inferred from `R18-c`.
- `R18-f` applies when communication occurs only after a realized consequence of the condition and requires the gated absence `no_communication_of_the_named_condition_during_the_defined_feasible_preconsequence_window`.
- `R18-b` applies to direct communication after a problem becomes apparent but before any realized consequence qualifying for `R18-f`. For the same communication event, `R18-f` replaces `R18-b` when a qualifying consequence has already occurred.

### 3.14 NBM-R19 — Response to Another's Request or Stated Limit

**Facet groups:** ordered response acts (`R19-a`–`R19-f`, `R19-h`, `R19-j`) and response mechanism (`R19-i`).

- `R19-h` is the specific request that a stated requirement, limit, or applicability condition not apply in the narrator's case. It replaces general negotiation `R19-c` for that same exception request. `R19-c` remains for other scope, timing, or condition negotiation. Distinct later non-exception negotiation may be a later stage.
- `R19-g` is retired from v2 candidate substantive assignment. Record its initial acceptance/compliance as `R19-a`, then record later renegotiation as `R19-c` or later withdrawal/decline as `R19-d`, with explicit temporal edges. `R19-d` therefore includes an affirmative later withdrawal from a previously accepted response when so placed in sequence.
- Component events in that response history remain part of one request/limit episode unless a new request creates a new opportunity. No composite label or number of component labels adds independent evidence.

### 3.15 NBM-R20 — Disagreement Handling

**Facet groups:** dialogue content (`R20-a`–`R20-d`), position change/proposal (`R20-e`, `R20-f`), interaction disposition (`R20-g`, `R20-h`), mechanism (`R20-i`), engagement pattern (`R20-j`), and escalation feature (`R20-k`). Each dialogue turn is an event/stage; several facet values may be co-present on one turn, and supported order is recorded between turns.

- `R20-e` requires an affirmative change or abandonment of part or all of the narrator's prior position to accommodate the other party; reciprocal change is not required.
- `R20-f` requires proposing a compromise, trial, or alternative arrangement that would alter action or position for one or both parties; the proposal alone does not establish that the narrator conceded.
- A single utterance that both makes an actual concession and proposes an arrangement may carry both cross-facet components on one event/evidence unit. Otherwise proposal and later concession are separate ordered stages.
- `R20-j` has an affirmative component (the narrator repeats a previously stated position) and an exact absence component (`no_address_answer_or_other_engagement_with_the_other_partys_identified_content_during_the_defined_repeated_position_exchange`). Repetition alone is insufficient. The other party's content and a sufficiently complete exchange must be sourced, and the four-part gate applies only to non-engagement. In a partial transcript the absence component is insufficient.
- `R20-g` is an explicit temporary postponement tied to a later time or condition and therefore includes an intended revisit.
- `R20-h` is an affirmative withdrawal from or ending of the current interaction without a stated commitment to revisit. It need not assert permanent no-contact. For the same turn, a stated revisit makes the value `R20-g`, not `R20-h`. A later unplanned return does not erase an earlier supported withdrawal.

### 3.16 NBM-R21 — Interpersonal Repair After Recognized Strain or Harm

**Facet groups:** repair content (`R21-a`–`R21-e`), response origin (`R21-g`), channel (`R21-h`), timing/trajectory (`R21-i`), contact disposition (`R21-f`, `R21-j`), and absence of repair (`R21-k`). Repair/contact events may be ordered; repair content, origin, and channel may be co-present on one event.

- `R21-f` is retained as two separately sourced components: affirmative resumption of contact, and the exact absence `no_discussion_of_the_recognized_rupture_during_the_relevant_resumed_contact_interaction_or_named_feasible_discussion_opportunity`. The absence component requires the four-part gate; resumed contact plus silence in an incomplete record establishes only the affirmative component, not the full hybrid value.
- For `R21-k`, `repair action` means an action aimed at addressing the recognized strain/harm, the relationship, or its consequence. It includes `R21-a`–`R21-e`, a response under `R21-g` only when that response contains a repair-directed act, an intermediary under `R21-h` only when used to carry a repair-directed act, and an OS act with the same function.
- Ordinary resumed contact without rupture discussion (`R21-f`) is a contact disposition and is not by itself repair action. Therefore `R21-f` may co-occur with `R21-k` only when the full `R21-k` gate establishes no repair-directed act in the same defined opportunity; they share one event/evidence unit.
- `R21-j` is an affirmative withdrawal/end-contact act, not repair action and not mere inactivity. It may co-occur with `R21-k` only if the separate gated absence of every repair-directed act is established; both share one terminal event/evidence unit. Withdrawal alone cannot establish the absence.
- `R21-i` remains an ordered trajectory: an initial gated absence of repair in one defined window followed by a later affirmative repair event. Its later content/origin/channel values share the later event's evidence unit and do not add independent repair opportunities.

## 4. Admission for fresh blind review

This candidate is ready only for a separate fresh theory-blind review of the three repair artifacts. It does not authorize calibration, participant coding, automation, implementation, or any comparison with an external target. A reviewer should verify the literal codebook rules against the blocker matrix and the v3 semantic contract before any implementation proposal is admitted.
