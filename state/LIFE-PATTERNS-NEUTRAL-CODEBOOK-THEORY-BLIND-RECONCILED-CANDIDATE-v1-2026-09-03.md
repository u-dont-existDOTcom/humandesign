# Neutral Behavioral Measurement Codebook — Theory-Blind Reconciled Candidate v1

**Version status:** Theory-blind reconciliation candidate for blind human pilot reliability testing.

**Source naming for auditability:**

* **Draft A:** *Neutral Behavioral Measurement Codebook — Independent Replication Draft v1* using NBM-* identifiers.
* **Draft B:** *Theory-Neutral Behavioral Measurement Codebook* using OBS* identifiers.

Both source drafts explicitly frame the task as coding reported behavior rather than personality, diagnosis, morality, or hidden motive.

> **Preservation constraint:** **This exact reconciliation output must be preserved unchanged before any external hypothesis, target model, prediction, or model-fit result is revealed.** Any later alteration, mapping, scoring system, composite, external-model correspondence, or validity-driven revision must receive a new version and must not overwrite this artifact.

---

# 1. Measurement architecture

## 1.1 Primary unit: behavioral episode

A **behavioral episode** is a bounded first-person autobiographical account containing enough information to identify a concrete situation or opportunity and at least one reportable action, explicit non-action, decision, or action sequence.

An episode should preserve, when available:

* the situation, opportunity, demand, obstacle, request, rule, choice, or other relevant event;
* what the narrator reports knowing, noticing, experiencing, or recognizing at the time;
* relevant perceived or objectively stated alternatives;
* what the narrator did or explicitly did not do;
* temporal order;
* relevant opportunity and feasibility conditions;
* immediate or later outcome where reported;
* narrator-stated explanations or causal claims;
* counteractions, reversals, and exceptions;
* context modifiers;
* uncertainty in memory or chronology.

A complete episode need not contain all fields. Each observable below has its own minimum evidence requirements.

### Episode splitting rule

Split a narrative into separate episodes when at least one of the following occurs:

1. a prior action cycle has substantially closed and a new opportunity or demand begins;
2. a meaningful time gap creates a new decision or action opportunity;
3. the same recurring situation occurs on a new occasion;
4. the goal changes sufficiently that later behavior is no longer pursuit of the same focal endpoint;
5. a new request, conflict, obstruction, error, or other prerequisite creates an independently codable behavioral opportunity.

Do **not** split merely because one continuous episode contains several steps. Preserve those as a sequence.

Two descriptions of the same historical incident count as one episode.

---

## 1.2 Non-action eligibility

Non-action is substantively codable only when all four conditions are supported:

1. **Awareness:** the narrator knew about the relevant opportunity, demand, alternative, request, problem, or possible action.
2. **Opportunity:** a meaningful occasion or response window existed.
3. **Reasonable feasibility:** action was realistically possible given the reported constraints.
4. **Established non-action:** the narrator explicitly reports not acting, or the chronology directly entails that the defined opportunity passed without the action.

If any component is unclear, do not infer refusal, delay, avoidance, noncompliance, failure to help-seek, failure to check, or other substantive non-action. Use **insufficient evidence** or a missingness flag.

## This reconciles the Awareness–Opportunity–Feasibility rule in Draft A with Draft B's additional requirement that non-action be explicitly reported or entailed by a defined chronology.

## 1.3 Evidence states

Evidence state is separate from substantive code value.

### O — Observed

At the **episode level**, the minimum evidence requirements for a substantive value are met.

At the **person-level recurrence summary**, O means the stated recurring value meets the recurrence rule below. It never means a permanent trait.

### C — Contradicted

Use only when there is a defined proposition to evaluate, such as:

* a narrator's stored global claim;
* a previously formulated context-bounded recurring proposition.

Qualifying episode evidence directly opposes the proposition. Record the competing observed value.

A universal claim can be contradicted by one valid counterexample. A context-bounded proposition requires a sufficiently comparable counterepisode.

### M — Mixed

At an aggregation scope, qualifying episodes support materially different substantive values and no adequately supported context split resolves them.

Do not use M merely because a single episode contains a sequence. Code that sequence directly.

### IE — Insufficient evidence

Use when required information is missing, opportunity or feasibility is unclear, chronology is insufficient, too few episodes exist for a recurrence claim, or the relevant distinction cannot be made reliably.

### NA — Not applicable

Use only when the observable's prerequisite circumstance is affirmatively absent from the bounded episode or explicitly defined scope.

Non-mention is normally IE, not NA, at the person level.

## The source drafts use the same five-state family, although they differ slightly on when “observed” applies; this reconciliation explicitly distinguishes episode-level observation from recurrent person-level observation.

## 1.4 Missingness and uncertainty flags

Keep missingness visible rather than resolving it through inference.

Permitted flags include:

* **UNK:** relevant fact not reported;
* **APPROX:** timing, amount, count, or sequence approximate;
* **CONFLICTING-RECALL:** internally inconsistent recollection;
* **UNCLEAR-AGENCY:** unclear whether action was chosen or compelled;
* **UNCLEAR-AWARENESS:** uncertain whether prerequisite was known;
* **UNCLEAR-OPPORTUNITY:** uncertain whether a meaningful opportunity occurred;
* **UNCLEAR-FEASIBILITY:** alternative action may not have been realistically possible;
* **UNCLEAR-WINDOW:** response or observation window cannot be bounded;
* **UNCLEAR-SEQUENCE:** necessary temporal order cannot be established;
* **UNCLEAR-ENDPOINT:** completion criterion is ambiguous.

A low-detail episode may be usable for one observable and IE for another.

---

## 1.5 Causal and temporal claims

For every claimed X→Y relation, distinguish:

* **Narrator-explicit influence:** narrator explicitly says X affected, prompted, changed, prevented, or contributed to Y.
* **Temporal precedence only:** X is reported before Y, but no influence is established.
* **Coder inference prohibited:** a coder believes X probably caused Y.

Only the first may be stored as a narrator-stated influence claim. Neither form establishes objective causation.

## Narrator explanations are preserved but are not upgraded into hidden motives or causes. This restriction is explicit in both source drafts.

## 1.6 Sequence coding

Whenever behavior changes during an episode:

* retain all qualifying substantive values in temporal order;
* do not reduce the episode to the final action;
* distinguish immediate response from later response when the observable provides both;
* retain explicit reversals and renegotiations.

Recommended notation:

`value 1 → value 2 → value 3`

Example:

`declines request → asks for clarification → accepts reduced scope`

Sequence is not “mixed” unless the aggregation across comparable episodes is also mixed.

---

## 1.7 Context modifiers

Record only modifiers supported by the narrative.

Common modifiers:

* life period;
* domain/activity;
* setting;
* task type;
* familiarity/novelty;
* voluntariness versus obligation;
* relationship and role;
* power or authority asymmetry;
* public/private setting;
* social scrutiny;
* stakes as reported;
* reversibility;
* deadline/time pressure;
* competing demands;
* financial/material/time constraints;
* available information;
* available assistance;
* fatigue, pain, illness, or workload;
* explicitly reported emotional state;
* prior relevant outcomes;
* explicit rules/procedures;
* expected consequences;
* alternatives available;
* opportunity duration;
* whether outcome was immediately observable;
* locally described cultural, family, community, or organizational expectations.

Modifiers do not automatically become explanations.

---

## 1.8 Context splitting

Do not average away contextual differences.

A context-bounded split may be reported when:

1. the underlying observable is the same;
2. opportunities are sufficiently comparable;
3. a documented contextual distinction separates different substantive values;
4. the evidence is not based only on one isolated contrast.

For a **systematic** context split, ordinarily seek at least two qualifying opportunities in each proposed context class. With thinner data, record the difference as provisional rather than asserting a stable context rule.

If values differ but no supported contextual relation distinguishes them, use **mixed**.

---

## 1.9 Recurrence rules

A single qualifying episode supports an **episode-level observation**.

A provisional recurrent person-level pattern requires:

* at least **two independent qualifying episodes** showing the same substantive value; or
* one detailed episode plus an **anchored repeated-series report** that establishes at least one additional occurrence.

Retellings of the same incident count once.

### Derived repeated-condition summary

For a specifically recurring cue or opportunity, a stronger repeated-condition summary should ordinarily require:

* at least **three identifiable opportunities**, or
* at least two concrete occasions plus an anchored series statement establishing one or more additional occasions.

Do not label recurrence “automatic,” “habitual,” or “routine” unless those features themselves are independently evidenced.

### Derived context-variability summary

Ordinarily requires at least three qualifying episodes across at least two contexts. A claimed systematic split should preferably have repeated evidence within each context.

### Derived temporal-change summary

Ordinarily requires at least three time-ordered comparable opportunities. Preserve reversions and isolated exceptions.

No universal frequency threshold is imposed beyond these provisional measurement rules.

---

## 1.10 Person-level aggregation

Person-level output is a **derived summary**, not another independent behavioral observation.

Each summary should contain:

`Observable | scope | substantive value(s) | evidence state | supporting episodes | counterepisodes | opportunity count if known | context qualifiers | time period | missingness/certainty`

Permitted:

> “Across three reported workplace deadline episodes, the narrator began after an external reminder in two and at the first feasible opportunity in one; state = mixed.”

Not permitted:

> “Procrastinator.”

Do not produce:

* midpoint values from incompatible behaviors;
* personality scores;
* latent scales;
* global rankings;
* favorable/unfavorable ratings;
* unversioned composites.

---

## 1.11 Treatment of narrator global claims

Statements such as:

* “I am decisive.”
* “I never ask for help.”
* “I always finish what I start.”
* “I hate conflict.”

are stored in a separate **Narrator Claim** field.

They do not themselves establish a behavioral value.

Concrete episodes may support, qualify, or contradict the claim. One qualifying counterexample can contradict a literal universal claim, but it does not establish an opposite global trait.

Rhetorical strength does not substitute for episode evidence.

---

## 1.12 Universal “other specified”

Every primary observable permits:

**OS — Other specified:** qualifying behavior clearly fits the observable's prerequisite but is not adequately represented by a listed substantive subcode.

The coder must provide a concrete behavioral description.

OS must never be used instead of IE.

---

# 2. Primary episode-level observables

## NBM-R01 — Optional Opportunity Response

**Short behavioral name:** Optional engagement.

**Operational definition:** The narrator's first substantive response after recognizing a genuine noncompulsory opportunity to enter, accept, explore, or participate in an activity, situation, opportunity, or interaction.

**Inclusion criteria:**

* a defined opportunity exists;
* the narrator knew it existed;
* participation was meaningfully optional;
* a response within a meaningful window is reported.

**Exclusion criteria:**

* participation was effectively compulsory;
* the episode concerns starting an already accepted task;
* unfamiliarity is inferred by the coder;
* only a global claim such as “I try anything” is given.

**Possible substantive values/subcodes:**

* R01-a enters directly;
* R01-b observes or gathers limited information before entering;
* R01-c enters on a limited/reversible trial basis;
* R01-d defers until a stated time or condition;
* R01-e enters after prompting or increased obligation;
* R01-f explicitly declines;
* R01-g transfers/delegates the entry decision;
* R01-h no response during a feasible defined opportunity.

**Minimum evidence requirements:** Opportunity + awareness + genuine optionality + response or qualifying non-action.

**Counterevidence:** Comparable optional opportunities receiving a materially different response.

**Relevant context modifiers:** Familiarity, narrator-reported novelty, reversibility, cost, social invitation, companions, stakes, prior experience, time demand.

**Fictional boundary examples:**

1. “A place opened in the workshop. I checked the dates and registered that afternoon.” → R01-b → entry.
2. “My department required everyone to attend the workshop.” → Not R01; genuine optionality absent.

**Common coding mistakes:** Calling entry “openness”; interpreting decline as fear; treating silence as non-entry without the non-action gate.

**Source provenance:** Draft A NBM-E01; Draft B OBS001.

**Reconciliation note:** Draft A made unfamiliarity a prerequisite. It is retained only as a context modifier; optional engagement itself does not require novelty.

---

## NBM-R02 — Information Seeking

**Short behavioral name:** Information seeking.

**Operational definition:** Deliberate action to obtain task-, choice-, or situation-relevant factual information after the narrator recognizes an information gap.

**Inclusion criteria:**

* an unknown or unresolved factual question is identifiable;
* acquisition behavior or deliberate non-search is reported;
* the information is relevant to a concrete task, decision, or action.

**Exclusion criteria:**

* information arrives unsolicited;
* practical assistance rather than information is the focal behavior;
* outcome verification is the focal behavior;
* the coder assumes an information need not recognized in the account.

**Possible substantive values/subcodes:**

* R02-a asks a person;
* R02-b consults a written/digital/reference source;
* R02-c compares multiple sources;
* R02-d directly observes, inspects, or tests in order to learn;
* R02-e delegates information gathering;
* R02-f stops searching and proceeds using available information;
* R02-g deliberately forgoes further information despite a recognized gap and feasible opportunity.

**Minimum evidence requirements:** Recognized information gap + concrete acquisition/non-acquisition behavior + relevant temporal placement.

**Counterevidence:** Comparable uncertainty episodes in which information is obtained differently or not sought.

**Relevant context modifiers:** Stakes, source accessibility, time pressure, expertise, prior familiarity, reported source trust, reversibility, search cost.

**Fictional boundary examples:**

1. “I didn't know which permit applied, so I called the city office and checked the website.” → R02-a + R02-b.
2. “A coworker happened to mention the rule at lunch.” → Not R02 unless the narrator solicited the information.

**Common coding mistakes:** Equating curiosity with information seeking; treating all advice as information; judging information quality instead of coding acquisition behavior.

**Source provenance:** Draft A NBM-C01; Draft B OBS003.

---

## NBM-R03 — Action With Unresolved Uncertainty

**Short behavioral name:** Uncertainty-point response.

**Operational definition:** What the narrator does when a recognized, decision-relevant unknown remains unresolved at the point when action is possible.

**Inclusion criteria:**

* the narrator recognizes a meaningful unknown;
* the unknown remains unresolved;
* an action point occurs;
* the subsequent action or qualifying non-action is reported.

**Exclusion criteria:**

* uncertainty was resolved before action;
* only the coder perceives uncertainty;
* the story ends before an action opportunity;
* mere unfamiliarity without an unresolved unknown.

**Possible substantive values/subcodes:**

* R03-a proceeds with the full action;
* R03-b takes a limited/reversible trial;
* R03-c delays pending information or a stated condition;
* R03-d follows an established default/rule;
* R03-e shares or transfers the decision;
* R03-f deliberately maintains multiple options;
* R03-g declines/exits;
* R03-h takes no action during a feasible defined window.

**Minimum evidence requirements:** Recognized unresolved unknown + awareness + identifiable action point + response.

**Counterevidence:** Comparable unresolved-uncertainty situations producing different responses.

**Relevant context modifiers:** Consequence severity, reversibility, deadline, backup options, responsibility for others, prior analogous experience, authority.

**Fictional boundary examples:**

1. “I wasn't sure the software would preserve the files, so I copied one file and tested it first.” → R03-b.
2. “The schedule later turned out to be uncertain, but I didn't know that at the time.” → Not R03.

**Common coding mistakes:** Equating uncertainty with indecision; assuming action means certainty; coding delay without showing that unresolved uncertainty was present at the action point.

**Source provenance:** Draft B OBS004; partial narrowing of Draft A NBM-E01.

---

## NBM-R04 — Exposure Setting After Recognized Possible Loss

**Short behavioral name:** Possible-loss exposure setting.

**Operational definition:** How the narrator sets the scale, duration, reversibility, distribution, or backup structure of an action after recognizing a specific possible negative consequence.

**Inclusion criteria:**

* a concrete possible downside is recognized before action;
* at least two feasible exposure levels or arrangements exist;
* the narrator's exposure-setting behavior is reported.

**Exclusion criteria:**

* danger or loss is visible only to the coder;
* downside is discovered only afterward;
* no alternative exposure level exists;
* the account merely labels an action “risky.”

**Possible substantive values/subcodes:**

* R04-a declines the exposure;
* R04-b caps amount or duration;
* R04-c stages exposure incrementally;
* R04-d creates a backup, reserve, or hedge;
* R04-e shares/transfers exposure;
* R04-f accepts the full identified exposure;
* R04-g increases exposure after additional favorable evidence;
* R04-h lets another person determine exposure level.

**Minimum evidence requirements:** Recognized downside before action + feasible alternative exposure + actual exposure-setting behavior.

**Counterevidence:** Comparable possible-loss episodes using materially different exposure-setting behavior.

**Relevant context modifiers:** Type/magnitude of possible loss, reversibility, available resources, responsibility for others, time horizon, prior losses, backup availability.

**Fictional boundary examples:**

1. “I knew the project might fail, so I committed only one month of funds and kept the rest untouched.” → R04-b + R04-d.
2. “The route was objectively dangerous, but I didn't know that until afterward.” → Not R04.

**Common coding mistakes:** Calling the code risk tolerance; using outcome severity to infer prior awareness; comparing incomparable kinds of possible loss.

**Source provenance:** Draft B OBS005.

**Pilot status:** Retained provisionally because its prerequisites are unusually clear, but rarity and overlap with R03/R10 require testing.

---

## NBM-R05 — Choice Construction and Resolution

**Short behavioral name:** Choice construction/resolution.

**Operational definition:** How recognized alternatives enter the narrator's consideration set and how selection, deferral, combination, or non-resolution subsequently occurs.

**Inclusion criteria:** A genuine choice point is reported and enough evidence exists to code at least one of the two facets below.

**Exclusion criteria:** Alternatives are invented by the coder; only the final action is known; sequential actions were never alternatives.

**Possible substantive values/subcodes:**

**Option-set facet**

* R05-O1 starts from a given/constrained menu;
* R05-O2 accepts one/default option without searching for alternatives;
* R05-O3 independently generates multiple options;
* R05-O4 solicits possible options from others;
* R05-O5 adds options as the episode unfolds;
* R05-O6 combines elements into a new option.

**Resolution facet**

* R05-R1 selects without reported comparison / first acceptable option;
* R05-R2 explicitly compares alternatives on stated dimensions;
* R05-R3 eliminates options using an explicit constraint;
* R05-R4 follows an explicit rule, prior commitment, or default;
* R05-R5 uses a trial/sample before final selection;
* R05-R6 delegates final selection;
* R05-R7 defers with an explicit revisit time/condition;
* R05-R8 remains unresolved during a feasible decision window;
* R05-R9 combines options rather than selecting one.

**Minimum evidence requirements:**
For option-set coding: choice point + how at least one considered option entered the set.
For resolution coding: at least two recognized alternatives, or a default-versus-search choice, plus selection process.

**Counterevidence:** Comparable choices using a materially different option-set or resolution procedure.

**Relevant context modifiers:** Number of options, option visibility, time, expertise, reversibility, stakes, institutional constraints, social input, decision ownership.

**Fictional boundary examples:**

1. “I listed driving, taking the later train, and joining remotely, then compared cost and arrival time.” → R05-O3 + R05-R2.
2. “I picked the cheapest.” → The selected criterion is known, but the exact resolution process may still be IE if comparison/sequence is unclear.

**Common coding mistakes:** Confusing option generation with comparison; assuming fast choice means no comparison; reconstructing unmentioned alternatives.

**Source provenance:** Draft A NBM-A03; Draft B OBS006 and OBS007.

**Reconciliation note:** Option generation and choice procedure remain separate coded facets because their evidence requirements differ, but they are housed in one primary observable to reduce coder burden.

---

## NBM-R06 — Decision Revision

**Short behavioral name:** Decision revision.

**Operational definition:** What happens to a previously selected course when later information, changed circumstances, another person's intervention, or explicit reconsideration creates an opportunity to maintain, revise, reopen, or abandon it.

**Inclusion criteria:** Initial decision + later reconsideration/input point + subsequent action.

**Exclusion criteria:** Earlier statement was merely a possibility; implementation changes without reopening the decision; method adjustment toward the same unchanged choice.

**Possible substantive values/subcodes:**

* R06-a maintains the decision;
* R06-b revises after new evidence;
* R06-c revises after changed constraints;
* R06-d revises following a request/pressure;
* R06-e explicitly reopens without new external information;
* R06-f initial decision was provisional and later finalized;
* R06-g oscillates between alternatives;
* R06-h abandons the decision without a replacement reported.

**Minimum evidence requirements:** Definite initial selection + later input/reconsideration point + temporal order + subsequent decision/action.

**Counterevidence:** Comparable revision opportunities where the original decision is maintained or revised differently.

**Relevant context modifiers:** Reversibility, sunk resources, public commitment, authority, relationship, stakes, time elapsed, perceived quality of new information.

**Fictional boundary examples:**

1. “After booking the train, I learned the line would close, so I changed to a bus.” → R06-c.
2. “I said I might take the train, then later chose the bus.” → No definite initial decision; not R06.

**Common coding mistakes:** Calling all changed behavior inconsistency; confusing a provisional option with a decision; confusing method change with decision revision.

**Source provenance:** Draft B OBS008.

---

## NBM-R07 — Preparation and Sequencing

**Short behavioral name:** Preparation/planning.

**Operational definition:** Concrete preparatory behavior undertaken before or at the beginning of a focal action to arrange materials, steps, timing, rehearsal, resources, or contingencies.

**Inclusion criteria:** A future focal action is identifiable and the narrator reports creating or using a concrete preparation.

**Exclusion criteria:** Mere worry, hope, intention, or unacted thought; preparation inferred from a successful outcome; routine execution after the focal task is already underway.

**Possible substantive values/subcodes:**

* R07-a explicitly proceeds with little/no preparation despite a feasible preparation opportunity;
* R07-b basic material preparation;
* R07-c creates a step sequence/checklist;
* R07-d schedules timing/deadlines;
* R07-e rehearses or tests;
* R07-f prepares contingency action(s);
* R07-g prepositions resources/materials;
* R07-h uses a prior template/system;
* R07-i continues preparation without transitioning to the focal action during the observed period.

**Minimum evidence requirements:** Identifiable focal action + concrete preparatory act or explicit decision to proceed without available preparation + temporal ordering.

**Counterevidence:** Comparable actions with materially different preparation behavior.

**Relevant context modifiers:** Complexity, familiarity, stakes, deadline, institutional requirements, prior failure, coordination needs, preparation time.

**Fictional boundary examples:**

1. “The night before, I made a three-step checklist, tested the projector, and saved a backup.” → R07-c + R07-e + R07-f.
2. “The project turned out very organized.” → No R07 without prior preparatory behavior.

**Common coding mistakes:** Inferring planning from competence; counting all thinking as planning; automatically classifying lengthy preparation as delayed initiation.

**Source provenance:** Draft A NBM-A02; Draft B OBS009.

---

## NBM-R08 — Action Initiation

**Short behavioral name:** Action initiation.

**Operational definition:** The timing and manner by which the narrator moves from awareness of an accepted task, requirement, or definite intended action to the first task-directed behavior.

**Inclusion criteria:**

* relevant task/action is identified;
* narrator awareness is established;
* at least one feasible starting opportunity is known;
* initiation timing or qualifying non-initiation can be reconstructed.

**Exclusion criteria:**

* access/resources make action infeasible;
* no action window can be bounded;
* only a broad motive is reported;
* required preparation is misclassified as inactivity.

**Possible substantive values/subcodes:**

* R08-a starts at the first feasible opportunity;
* R08-b starts after a planned delay;
* R08-c starts later than the narrator's previously stated intended start;
* R08-d starts after an external prompt, reminder, deadline signal, or accumulating consequence;
* R08-e makes a limited/partial task-directed start;
* R08-f explicitly does not start during a defined feasible period.

**Initiation-trigger modifier, when reported:** self-set time; external deadline/request; environmental cue; threshold/condition; routine sequence cue; another person's presence/participation; strong reported state; other specified proximal trigger.

**Minimum evidence requirements:** Task/intention + awareness + feasible start window + actual start/non-start timing.

**Counterevidence:** Comparable initiation opportunities with different start patterns.

**Relevant context modifiers:** Deadline, task familiarity, competing demands, ambiguity, external dependency, public commitment, prior preparation, available time.

**Fictional boundary examples:**

1. “I decided Sunday to file it Monday morning, and I opened the form at nine Monday.” → R08-b.
2. “I wanted to submit it Monday, but the site was offline until Thursday.” → Do not code delayed/non-initiation for the blocked period.

**Common coding mistakes:** Treating aspiration as a definite intended action; treating necessary preparation as delay; inferring late initiation solely from a late completion date.

**Source provenance:** Draft A NBM-A01; Draft B OBS010, OBS011, and the initiation portion of OBS026.

---

## NBM-R09 — External Action Structuring

**Short behavioral name:** External structuring.

**Operational definition:** Concrete use, creation, modification, disabling, or deliberate rejection of external reminders, schedules, environmental arrangements, access conditions, or accountability structures linked to a target behavior.

**Inclusion criteria:** Target behavior + identifiable external structure + narrator action toward that structure.

**Exclusion criteria:** Structured environment merely exists; link to target behavior is absent; only an internal resolution is described.

**Possible substantive values/subcodes:**

* R09-a creates reminder/schedule cue;
* R09-b arranges materials/location;
* R09-c restricts access to a competing option;
* R09-d enlists accountability/accompaniment;
* R09-e adopts an externally imposed system;
* R09-f modifies a system to fit the target behavior;
* R09-g disables/bypasses a structure;
* R09-h deliberately declines an available structure.

**Minimum evidence requirements:** Target behavior + external structure + concrete use/modification/non-use decision.

**Counterevidence:** Similar opportunities where the structure is available but unused, or behavior occurs without it.

**Relevant context modifiers:** Recurrence, technology, privacy, social support, prior missed action, voluntariness, location.

**Fictional boundary examples:**

1. “I put the medication beside the kettle and set an alarm.” → R09-a + R09-b.
2. “My office had a shared calendar.” → No R09 unless the narrator actively used or modified it for the target behavior.

**Common coding mistakes:** Calling external structuring “discipline”; confusing one-off task sequencing with persistent cue/environment design; attributing another person's control to the narrator.

**Source provenance:** Draft B OBS013; conceptually adjacent but not merged with Draft A NBM-A02.

---

## NBM-R10 — Allocation Among Competing Courses

**Short behavioral name:** Competing-course allocation.

**Operational definition:** The action used when two or more recognized demands, intended actions, or salient alternatives compete for the same limited time, attention, money, effort, access, or other concrete resource.

**Inclusion criteria:**

* at least two courses are recognized;
* a genuine incompatibility or resource constraint exists;
* allocation behavior is reported.

**Exclusion criteria:** Separate tasks without overlap; scarcity assumed by the coder; alternative never noticed; original action already ended.

**Possible substantive values/subcodes:**

* R10-a concentrates resource on one course / finishes current course first;
* R10-b switches to another course;
* R10-c divides resource into blocks;
* R10-d alternates/multitasks;
* R10-e sequences demands over time;
* R10-f delegates one course;
* R10-g renegotiates scope/timing;
* R10-h preserves a reserve/buffer;
* R10-i postpones/drops one course;
* R10-j reduces access to the competing option;
* R10-k takes no action on either during the defined feasible window.

**Competition-type modifier:** simultaneous obligations; shared scarce resource; newly salient optional alternative; other specified.

**Minimum evidence requirements:** Competing courses + limited shared resource/incompatibility + narrator allocation response.

**Counterevidence:** Comparable competition episodes using a materially different allocation.

**Relevant context modifiers:** Urgency, deadlines, obligation, attractiveness as reported, delegability, authority, switching cost, scarcity severity, prior commitments.

**Fictional boundary examples:**

1. “I had two free hours, so I spent one on the report and one making dinner.” → R10-c.
2. “Two projects happened in different months.” → Not R10 unless their demands actually competed.

**Common coding mistakes:** Inferring priorities from the coder's view of importance; labeling switching distraction; assuming scarcity without narrative evidence.

**Source provenance:** Draft A NBM-E02; Draft B OBS012 and OBS021.

---

## NBM-R11 — Goal-Course Response to Obstruction or Disruption

**Short behavioral name:** Goal response to disruption.

**Operational definition:** The sequence of behavior after a concrete barrier, setback, interruption, rejection, illness episode, conflict, or other disruption materially impedes an accepted or ongoing goal.

**Inclusion criteria:** Identifiable focal goal + explicit obstruction/disruption + subsequent behavior.

**Exclusion criteria:** Task ends normally; no obstruction occurs; continuation is structurally impossible and no alternative route exists; the account skips all post-disruption behavior.

**Possible substantive values/subcodes:**

**Immediate-response facet**

* R11-I1 repeats the same attempt;
* R11-I2 inspects/diagnoses the problem;
* R11-I3 uses a workaround;
* R11-I4 seeks information/assistance;
* R11-I5 negotiates/removes the barrier;
* R11-I6 waits/pauses;
* R11-I7 reduces the immediate target;
* R11-I8 redirects effort.

**Later goal-status facet**

* R11-G1 continues without meaningful interruption;
* R11-G2 pauses and later resumes;
* R11-G3 continues the same goal by a different route;
* R11-G4 narrows the goal;
* R11-G5 switches to a different goal;
* R11-G6 stops pursuing the focal goal;
* R11-G7 does not return within a stated observation window.

**Minimum evidence requirements:** Focal goal + obstruction/disruption + first or later post-event behavior. R11-G7 requires a defensible follow-up window.

**Counterevidence:** Comparable disruptions yielding different immediate or later responses; later re-engagement after apparent stopping.

**Relevant context modifiers:** Obstruction source, controllability, prior setbacks, cost of retrying, time remaining, substitute routes, support, physical recovery, deadline.

**Fictional boundary examples:**

1. “The site rejected the form, so I checked the fields, called support, and resubmitted the same application.” → R11-I2 → R11-I4 → R11-G3.
2. “The building closed permanently and the course existed nowhere else.” → Do not treat noncompletion as voluntary stopping.

**Common coding mistakes:** Coding only the eventual outcome and losing the first response; labeling stopping “lack of persistence”; treating forced termination as a chosen goal response.

**Source provenance:** Draft A NBM-B01; Draft B OBS014 and OBS023.

---

## NBM-R12 — Method Adjustment Across Attempts or Feedback

**Short behavioral name:** Method adjustment.

**Operational definition:** Whether and how the method used toward a continuous goal changes across successive attempts or after task-relevant result/feedback information becomes available.

**Inclusion criteria:**

* continuous focal goal;
* identifiable initial method;
* result, feedback, or successive-attempt boundary;
* identifiable subsequent method.

**Exclusion criteria:**

* goal changes completely;
* only one method is observed with no comparison point;
* later behavior differs but chronology is unknown;
* coder assumes the earlier feedback caused the change.

**Possible substantive values/subcodes:**

* R12-a repeats method substantially unchanged;
* R12-b changes one component;
* R12-c substantially replaces the method;
* R12-d combines methods;
* R12-e adds time/effort/resources/personnel;
* R12-f simplifies the method or reduces its scope;
* R12-g returns to an earlier method;
* R12-h discontinues the method, replacement unknown.

**Influence-link field:** narrator-explicit influence / temporal precedence only.

**Minimum evidence requirements:** Continuous goal + initial method + intervening result/feedback or attempt boundary + subsequent method.

**Counterevidence:** Later attempts reversing the apparent method pattern.

**Relevant context modifiers:** Feedback source/clarity, number of attempts, resources, switching cost, familiarity, stakes, time.

**Fictional boundary examples:**

1. “After two cakes failed at 200°C, I lowered the third one to 180°C.” → R12-b; causal link only if narrator says the failures prompted the change.
2. “Months later I used a different recipe.” → IE for R12 unless continuity and sequence are established.

**Common coding mistakes:** Inferring learning from difference; treating increased effort automatically as a new method; conflating method change with goal abandonment.

**Source provenance:** Draft A NBM-B02; Draft B OBS015 and the behavioral-use portion of OBS016.

---

## NBM-R13 — Outcome Checking and Feedback Acquisition

**Short behavioral name:** Outcome checking.

**Operational definition:** Deliberate behavior undertaken during, near completion of, or after an action to verify accuracy, completion, receipt, consequence, or quality, or to solicit outcome-relevant feedback.

**Inclusion criteria:** Distinct active monitoring, checking, confirmation, or solicitation behavior.

**Exclusion criteria:** Successful outcome inferred to imply checking; passive unsolicited feedback; automatic outcome visibility requiring no deliberate check.

**Possible substantive values/subcodes:**

* R13-a monitors during action;
* R13-b direct self-check after/near completion;
* R13-c obtains external confirmation from a person/system;
* R13-d solicits feedback;
* R13-e repeatedly checks the same outcome;
* R13-f retrospective review after outcome is known;
* R13-g explicitly does not check despite awareness, opportunity, and feasibility.

**Minimum evidence requirements:** Relevant action/outcome + deliberate check/solicitation, or qualifying explicit non-check.

**Counterevidence:** Comparable tasks with materially different checking behavior.

**Relevant context modifiers:** Stakes, error cost, outcome visibility, deadline, reversibility, external verification requirements, feedback source.

**Fictional boundary examples:**

1. “I recalculated the totals before sending the spreadsheet.” → R13-b.
2. “The alarm rang automatically when the test finished.” → Passive signal alone is not R13.

**Common coding mistakes:** Inferring carefulness; coding unsolicited criticism as the narrator's checking behavior; interpreting repeated checking as pathology.

**Source provenance:** Draft A NBM-B05; Draft B OBS016, narrowed to active monitoring/acquisition.

---

## NBM-R14 — Response to a Recognized Possible Error

**Short behavioral name:** Error response.

**Operational definition:** Actions taken after the narrator identifies or is informed of a specific possible mistake attributable to their own prior action or omission.

**Inclusion criteria:** Specific possible error + narrator awareness + subsequent behavioral response.

**Exclusion criteria:** Error unknown to narrator; merely unfavorable outcome; coder decides the disputed action was erroneous.

**Possible substantive values/subcodes:**

* R14-a verifies before accepting the error claim;
* R14-b acknowledges the error;
* R14-c corrects original work;
* R14-d mitigates downstream effects;
* R14-e informs affected people;
* R14-f installs/records a prevention step;
* R14-g disputes the error;
* R14-h explicitly withholds/conceals it;
* R14-i takes no corrective action during a feasible defined opportunity.

**Detection-source modifier:** self-identified; informed by another person/system; learned through consequence.

**Minimum evidence requirements:** Specific possible error + awareness + response/non-response.

**Counterevidence:** Later acknowledgment after dispute, correction without disclosure, disclosure without correction, or later prevention behavior. Preserve sequence.

**Relevant context modifiers:** Consequence, reversibility, blame exposure, authority, public visibility, correction availability, affected parties, time pressure.

**Fictional boundary examples:**

1. “I noticed I'd sent the wrong file, told the recipient, resent it, and changed the naming system.” → R14-e → R14-c → R14-f.
2. “They said my calculation was wrong, so I reopened the raw data and showed it matched.” → R14-a/R14-g; do not adjudicate who was correct.

**Common coding mistakes:** Treating dispute as dishonesty; collapsing disclosure and correction; calling an unfavorable outcome an error without reported recognition.

**Source provenance:** Draft B OBS017.

---

## NBM-R15 — Endpoint Completion and Closure

**Short behavioral name:** Endpoint closure.

**Operational definition:** How the narrator handles a bounded task, definite intended deliverable, agreement, promise, or commitment when its defined endpoint becomes due or otherwise relevant.

**Inclusion criteria:**

* a sufficiently clear endpoint exists;
* later performance can be compared with that endpoint;
* timing/constraints are known enough to distinguish completion, modification, or noncompletion.

**Exclusion criteria:** Vague aspiration; ongoing activity with no bounded endpoint; coder-imposed completion standard.

**Possible substantive values/subcodes:**

* R15-a completes substantially as defined;
* R15-b completes after delay;
* R15-c completes partially;
* R15-d renegotiates/modifies endpoint before due point;
* R15-e renegotiates/modifies after due point;
* R15-f substitutes another action/endpoint with relevant assent where assent is required;
* R15-g hands off and confirms transfer;
* R15-h leaves a known element open;
* R15-i withdraws/rescinds the commitment;
* R15-j stops without closure;
* R15-k returns later to close;
* R15-l does not complete despite awareness, opportunity, feasibility, and a defined window.

**Commitment-type modifier:** self-only definite intention; interpersonal assented commitment; formal obligation; negotiated endpoint; other.

**Minimum evidence requirements:** Defined endpoint + timing/condition + actual terminal/follow-up behavior. Noncompletion requires the non-action gate.

**Counterevidence:** Comparable bounded endpoints with different follow-through; later closure after apparent noncompletion.

**Relevant context modifiers:** Reliance by others, commitment formality, deadline, external dependency, changed circumstances, difficulty, handoff requirement, ability to renegotiate.

**Fictional boundary examples:**

1. “I promised the draft Tuesday, called Monday to renegotiate, and we agreed on Thursday.” → R15-d.
2. “I always wanted to learn Arabic.” → No bounded endpoint or definite commitment; not R15.

**Common coding mistakes:** Equating aspiration with commitment; treating renegotiation as simple failure; imposing an unstated completion standard.

**Source provenance:** Draft A NBM-B03; Draft B OBS018, OBS033, and the endpoint-correspondence portion of OBS026.

---

## NBM-R16 — Help Seeking and Help Use

**Short behavioral name:** Help seeking/use.

**Operational definition:** How the narrator requests, signals for, accepts, declines, delegates to, or uses another person's assistance in relation to a concrete task, obstacle, or need.

**Inclusion criteria:** Concrete need/task + actual or potential helper + assistance behavior.

**Exclusion criteria:** Pure factual information request; ordinary mutually interdependent teamwork; coder assumption that help was needed.

**Possible substantive values/subcodes:**

* R16-a requests before attempting independently;
* R16-b requests after one or more solo attempts;
* R16-c requests only after prompting;
* R16-d signals indirectly/waits for offer;
* R16-e accepts and uses offered help;
* R16-f accepts but does not use offered help;
* R16-g declines offered help;
* R16-h delegates a defined task portion;
* R16-i seeks practical/material assistance;
* R16-j seeks emotional/supportive presence;
* R16-k seeks help from multiple sources;
* R16-l does not request available help despite awareness, opportunity, and feasibility.

**Minimum evidence requirements:** Concrete need + potential/actual helper + timing + assistance-related behavior.

**Counterevidence:** Comparable needs handled with different help-seeking timing or use.

**Relevant context modifiers:** Relationship, expertise, power, privacy, urgency, prior attempts, cost/obligation, helper availability, prior helper response.

**Fictional boundary examples:**

1. “After two failed attempts, I asked Mei to show me how to run it.” → R16-b.
2. “Nobody helped me move.” → Does not establish non-help-seeking.

**Common coding mistakes:** Inferring dependence/independence; confusing factual information with assistance; coding nonrequest when no suitable helper was available.

**Source provenance:** Draft A NBM-C02; Draft B OBS027.

---

## NBM-R17 — Task Coordination and Coordination Initiation

**Short behavioral name:** Coordination.

**Operational definition:** Behavior used to initiate or align roles, timing, responsibilities, or interdependent actions among two or more people engaged in a concrete shared task.

**Inclusion criteria:** At least two people's actions are interdependent and an alignment or initiation behavior is reported.

**Exclusion criteria:** Pure social initiation; ordinary conversation; one-directional assistance with no joint-action dependency.

**Possible substantive values/subcodes:**

* R17-a initiates coordination;
* R17-b responds to another person's coordination attempt;
* R17-c proposes/divides roles;
* R17-d synchronizes timing/sequence;
* R17-e uses a message/system/intermediary to coordinate;
* R17-f renegotiates roles/timing after change;
* R17-g waits for another party to initiate despite a feasible coordination opportunity;
* R17-h proceeds independently despite established interdependence and feasible opportunity to coordinate.

**Minimum evidence requirements:** Interdependent task + relevant parties + who initiated/what alignment occurred + feasibility for any non-coordination value.

**Counterevidence:** Similar shared tasks with materially different coordination behavior.

**Relevant context modifiers:** Group size, authority, role clarity, urgency, communication access, institutional responsibility, prior agreements.

**Fictional boundary examples:**

1. “Before we started, I messaged everyone and proposed who would draft each section.” → R17-a + R17-c.
2. “I answered an invitation to dinner.” → Not R17; no interdependent task.

**Common coding mistakes:** Treating all collaboration as coordination; calling initiation leadership; confusing help-seeking with mutual alignment.

**Source provenance:** Draft A NBM-C03; Draft B OBS028, narrowed to task-relevant coordination.

---

## NBM-R18 — Communication of Own Need, Limit, or Uncertainty

**Short behavioral name:** Own-condition communication.

**Operational definition:** How and when the narrator communicates a personally experienced need, capacity limit, relevant constraint, lack of knowledge, or uncertainty to others for whom that information matters to shared action.

**Inclusion criteria:** Narrator-reported own condition + relevance to shared action + meaningful communication opportunity.

**Exclusion criteria:** Need inferred by coder; condition irrelevant to others; episode solely concerns answering another person's request.

**Possible substantive values/subcodes:**

* R18-a communicates directly before action;
* R18-b communicates directly after a problem appears;
* R18-c communicates indirectly/hints;
* R18-d selectively communicates part of the condition;
* R18-e uses writing/intermediary;
* R18-f communicates only after a consequence occurs;
* R18-g corrects/revises an earlier statement;
* R18-h withholds despite a relevant feasible opportunity.

**Minimum evidence requirements:** Experienced need/limit/uncertainty + relevance + opportunity to communicate + communication or explicit withholding.

**Counterevidence:** Comparable situations with earlier/later/more direct/non-communication behavior.

**Relevant context modifiers:** Relationship, privacy, power, urgency, anticipated consequences as reported, role expectations, communication channel.

**Fictional boundary examples:**

1. “Before the trip, I told everyone I couldn't safely drive at night.” → R18-a.
2. “She looked exhausted.” → No R18 unless the narrator reports the relevant condition and communication opportunity.

**Common coding mistakes:** Inferring internal needs; rating disclosure as healthy/unhealthy; treating selective communication as deception without evidence.

**Source provenance:** Draft B OBS029.

---

## NBM-R19 — Response to Another's Request or Stated Limit

**Short behavioral name:** Request/limit response.

**Operational definition:** The narrator's response after another party makes a concrete request, demand, boundary, refusal, capacity limit, or condition that requires a behavioral response.

**Inclusion criteria:** Request/limit is identifiable, received/understood, and a response opportunity exists.

**Exclusion criteria:** Other person merely expresses a preference with no action relevance; voluntary help initiated without a request; narrator is stating their own limit rather than answering another's.

**Possible substantive values/subcodes:**

* R19-a accepts/adapts substantially as stated;
* R19-b asks for clarification;
* R19-c negotiates scope/timing/conditions;
* R19-d declines;
* R19-e defers response;
* R19-f does not respond during a feasible defined window;
* R19-g initially complies/accepts then renegotiates or withdraws;
* R19-h seeks an exception;
* R19-i involves a third party;
* R19-j bypasses/acts contrary to the other person's stated limit.

**Minimum evidence requirements:** Concrete request/limit + awareness + feasible response opportunity + response.

**Counterevidence:** Comparable requests/limits receiving different responses.

**Relevant context modifiers:** Relationship, authority, ability to decline, urgency, cost, prior agreement, public/private context, consequence of refusal.

**Fictional boundary examples:**

1. “He asked me to cover Sunday. I said I could do the morning but not the afternoon.” → R19-c.
2. “I cooked dinner because I knew they were busy.” → Not R19; no request or stated limit.

**Common coding mistakes:** Labeling refusal assertive; labeling compliance people-pleasing; treating conditional acceptance as full acceptance.

**Source provenance:** Draft A NBM-D01; Draft B OBS030.

---

## NBM-R20 — Disagreement Handling

**Short behavioral name:** Disagreement handling.

**Operational definition:** Observable communication or action after the narrator recognizes that another party holds an incompatible position, interpretation, plan, or demand.

**Inclusion criteria:** Concrete recognized disagreement + subsequent behavior.

**Exclusion criteria:** Private dislike without interaction; unaware divergence; conflict inferred by coder.

**Possible substantive values/subcodes:**

* R20-a asks questions/seeks clarification;
* R20-b restates the other person's position;
* R20-c states own position;
* R20-d supplies reasons/evidence;
* R20-e accommodates/concedes;
* R20-f proposes compromise, trial, or alternative arrangement;
* R20-g postpones discussion;
* R20-h withdraws/ends interaction;
* R20-i involves third party/mediator;
* R20-j repeats position without engaging the other's content;
* R20-k uses specifically reported escalation behavior such as insult, threat, raised voice, or widened stakes.

Record sequences.

**Minimum evidence requirements:** Recognized disagreement + observable response.

**Counterevidence:** Comparable disagreements handled through a different sequence.

**Relevant context modifiers:** Relationship, hierarchy, audience, perceived safety, medium, stakes, history, time pressure, third parties.

**Fictional boundary examples:**

1. “I asked what she objected to, restated her concern, then proposed a one-week test.” → R20-a → R20-b → R20-f.
2. “I disliked the decision but never discussed it.” → No R20 interaction response.

**Common coding mistakes:** Using assertive/passive/aggressive labels; inferring tone; coding only the final resolution.

**Source provenance:** Draft A NBM-D02; Draft B OBS031.

---

## NBM-R21 — Interpersonal Repair After Recognized Strain or Harm

**Short behavioral name:** Interpersonal repair.

**Operational definition:** Behavior after the narrator recognizes relational strain, offense, misunderstanding, broken trust, or interpersonal harm and has an opportunity to address the relationship or consequence.

**Inclusion criteria:** Recognized strain/harm + narrator awareness + later relational behavior or qualifying non-action.

**Exclusion criteria:** No recognized rupture; regret without action; earlier period before the narrator became aware of the impact.

**Possible substantive values/subcodes:**

* R21-a acknowledges action/impact/strain;
* R21-b apologizes;
* R21-c explains or clarifies;
* R21-d offers restitution/corrective action;
* R21-e asks what response is needed/invites discussion;
* R21-f resumes contact without discussing the rupture;
* R21-g responds to the other person's repair attempt;
* R21-h uses an intermediary;
* R21-i delays repair and later acts;
* R21-j withdraws/ends contact;
* R21-k takes no repair action despite awareness, opportunity, and feasibility.

**Outcome modifier:** repair attempt accepted/rejected/response unknown. Outcome is not the behavior.

**Minimum evidence requirements:** Recognized interpersonal strain/harm + awareness + repair opportunity + subsequent behavior/non-behavior.

**Counterevidence:** Later repair after initial withdrawal, repeated strain after claimed correction, or different repair responses in comparable relationships.

**Relevant context modifiers:** Relationship, severity, responsibility as perceived by narrator, safety, power, time elapsed, available restitution, other person's response.

**Fictional boundary examples:**

1. “I realized my message sounded accusatory, so I called and explained what I meant.” → R21-c.
2. “He was upset, but I didn't learn that until six months later.” → Earlier lack of repair cannot be coded as R21-k.

**Common coding mistakes:** Inferring sincerity; treating explanation as proof of fault; equating successful reconciliation with the existence of a repair attempt.

**Source provenance:** Draft A NBM-D03; Draft B OBS032.

---

## NBM-R22 — Response to Explicit Rule or Procedure

**Short behavioral name:** Rule/procedure response.

**Operational definition:** Behavior when an identifiable explicit rule, instruction, agreed procedure, or formal requirement applies and the narrator is aware of it.

**Inclusion criteria:** Explicit rule/procedure + awareness + relevant opportunity to comply, clarify, modify, or depart.

**Exclusion criteria:** Vague norm, custom, etiquette, or cultural expectation; compliance impossible; rule inferred by coder.

**Possible substantive values/subcodes:**

* R22-a follows the stated rule/procedure;
* R22-b seeks clarification;
* R22-c requests exception/modification;
* R22-d uses an explicitly permitted alternative;
* R22-e openly departs from the rule;
* R22-f explicitly conceals a departure;
* R22-g takes no required response during a feasible defined opportunity.

**Minimum evidence requirements:** Identifiable explicit rule + awareness + feasible relevant opportunity + response.

**Counterevidence:** Comparable rule-governed situations producing a different response.

**Relevant context modifiers:** Rule clarity, source/authority, enforcement, stated purpose, consequences, exception process, available alternatives.

**Fictional boundary examples:**

1. “The policy required approval, so I submitted the request first.” → R22-a.
2. “Everyone usually dressed formally.” → Not R22 unless an explicit requirement is established.

**Common coding mistakes:** Treating convention as rule; moralizing compliance/departure; inferring concealed behavior.

**Source provenance:** Draft A NBM-E03.

---

# 3. Source constructs not retained as primary episode codes

The following source distinctions are deliberately preserved elsewhere rather than silently dropped.

## 3.1 Action-guiding cues

Draft B OBS002 is moved to **episode sequence/context metadata**.

Record:

* cue/event noticed;
* whether narrator explicitly says it guided action;
* temporal position;
* cue type.

Reason: a generic “cue guiding next action” can be attached to almost any behavior and would duplicate more specific primary observables. Proximal start triggers remain explicitly represented under NBM-R08.

---

## 3.2 Repetition under recurring conditions / routine enactment

Draft A NBM-B04 and Draft B OBS019 become a **derived repeated-condition summary**.

Reason: recurrence is not an independent episode behavior. Coding both each enactment and “repetition” as separate primary observations would double-count the same evidence.

Derived fields:

`underlying observable/behavior | recurring opportunity | number of opportunities | number enacted | exceptions | context | external structure present | derived state`

Do not label the result “habit,” “automaticity,” or “discipline.”

---

## 3.3 Prior-experience use

Draft B OBS020 is moved to **cross-episode link metadata**.

Record:

* prior episode ID;
* later episode ID;
* narrator-explicit link versus temporal precedence only;
* later behavior actually observed.

Reason: the later behavior should be coded under its substantive primary observable. A second primary “change after experience” code would duplicate the changed behavior and invite causal inference.

---

## 3.4 Strong emotion or bodily state

Draft A NBM-F01 and Draft B OBS022 are moved to:

1. **context modifier:** explicitly reported state and intensity;
2. **sequence field:** behavior occurring during/after the state;
3. **narrator-stated influence field:** only when the narrator explicitly links state to action.

Reason: the source values mainly recode the same underlying actions under an emotional context. Retaining the state and explicit link preserves evidence without treating “emotion-linked behavior” as an independent mechanism or implying regulation success.

A state-related action that independently satisfies another primary observable is coded there.

---

## 3.5 Load/fatigue-linked behavior change

Draft B OBS024 becomes a **derived context-conditioned comparison** based on primary episode codes plus fatigue/load modifiers.

Reason: “change under fatigue” requires comparison with another state or earlier phase and is therefore not a primitive episode observation.

---

## 3.6 Pressure-linked behavior change

Draft B OBS025 becomes a **derived context-conditioned comparison** based on primary episode codes plus pressure modifiers.

Reason: it requires a baseline or within-episode contrast. Pressure is preserved as context; the underlying action remains the primary observation.

---

## 3.7 Context-linked variability

Draft B OBS034 becomes a **derived cross-episode summary**.

Minimum provisional basis: at least three comparable coded episodes across at least two context classes. A systematic split should ordinarily have repeated evidence within each class.

---

## 3.8 Change in repeated behavior over time

Draft B OBS035 becomes a **derived temporal summary**.

Ordinarily require at least three comparable time-ordered opportunities. Preserve reversions, context shifts, and source compression.

Temporal order alone does not establish what caused the change.

---

# 4. Reconciliation ledger — all primary source constructs

## 4.1 Draft A

| Source construct                                              | Decision                               | Final location                                                     | Measurement reason                                                                                                                         |
| ------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| NBM-A01 Action Initiation                                     | merged                                 | NBM-R08                                                            | Same core behavioral evidence as OBS010/011; trigger retained as modifier rather than separate primary code.                               |
| NBM-A02 Pre-Action Planning and Sequencing                    | merged                                 | NBM-R07                                                            | Closely matches OBS009; concrete preparation is more reliably coded than inferred “planning.”                                              |
| NBM-A03 Choice Resolution                                     | merged                                 | NBM-R05                                                            | Preserved with separate option-set and resolution facets; avoids duplicating one choice episode.                                           |
| NBM-B01 Goal Continuation After Friction                      | merged                                 | NBM-R11                                                            | Combined with obstruction/re-engagement constructs while retaining immediate versus later sequence.                                        |
| NBM-B02 Strategy Modification After Feedback                  | merged                                 | NBM-R12                                                            | Same method-change evidence as OBS015; causal link to feedback separated from mere temporal sequence.                                      |
| NBM-B03 Commitment Follow-Through                             | merged                                 | NBM-R15                                                            | Generalized to bounded endpoint closure; commitment type retained as modifier.                                                             |
| NBM-B04 Routine Enactment                                     | moved to derived cross-episode summary | repeated-condition summary                                         | Repetition is an aggregation property, not a second episode-level observation.                                                             |
| NBM-B05 Outcome Checking and Review                           | merged                                 | NBM-R13                                                            | Retained as active checking/verification; passive feedback kept outside substantive values.                                                |
| NBM-C01 Information Seeking                                   | merged                                 | NBM-R02                                                            | Strong match to OBS003 after removing unnecessary restriction to only pre-action decisions.                                                |
| NBM-C02 Help Seeking and Help Use                             | merged                                 | NBM-R16                                                            | Substantially same prerequisites and behaviors as OBS027.                                                                                  |
| NBM-C03 Coordination With Others                              | merged                                 | NBM-R17                                                            | Preserved as interdependent task alignment; generic sociability excluded.                                                                  |
| NBM-D01 Response to Requests and Personal Limits              | merged                                 | NBM-R19                                                            | Combined with OBS030; own-limit communication separated into R18.                                                                          |
| NBM-D02 Disagreement Handling                                 | merged                                 | NBM-R20                                                            | Substantially same observable sequence as OBS031.                                                                                          |
| NBM-D03 Interpersonal Repair                                  | merged                                 | NBM-R21                                                            | Expanded slightly to recognized strain even when narrator disputes responsibility.                                                         |
| NBM-E01 Engagement With Unfamiliar Options                    | narrowed                               | NBM-R01 + novelty modifier; R03 when unresolved uncertainty exists | “Unfamiliarity” is context, not a necessary distinct mechanism; optional response and unresolved uncertainty remain separately measurable. |
| NBM-E02 Resource Allocation Under Constraint                  | merged                                 | NBM-R10                                                            | Same resource-allocation structure as OBS012 and overlapping competing-course cases in OBS021.                                             |
| NBM-E03 Response to Explicit Rules or Procedures              | retained substantially intact          | NBM-R22                                                            | Clear prerequisite and distinguishable actions; little unnecessary duplication.                                                            |
| NBM-F01 Action During Strong Reported Emotion or Bodily State | moved to context/modifier metadata     | state modifier + sequence + narrator-link field                    | Prevents duplicate coding of the same action and avoids implying emotion regulation/function.                                              |

## 4.2 Draft B

| Source construct                                   | Decision                               | Final location                                                                        | Measurement reason                                                                                                        |
| -------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| OBS001 Optional engagement response                | merged                                 | NBM-R01                                                                               | Combines cleanly with the behavioral portion of A E01.                                                                    |
| OBS002 Reported cue guiding next action            | moved to context/modifier metadata     | episode cue/link field; initiation triggers in R08                                    | Too generic as a primary code and would duplicate specific behaviors.                                                     |
| OBS003 Information seeking before action           | merged                                 | NBM-R02                                                                               | Same mechanism as A C01; timing retained as metadata rather than defining the entire code.                                |
| OBS004 Action under unresolved uncertainty         | retained substantially intact          | NBM-R03                                                                               | Clear prerequisite and distinct action point.                                                                             |
| OBS005 Exposure to a recognized possible loss      | retained substantially intact          | NBM-R04                                                                               | Behaviorally explicit and not reducible to uncertainty alone; pilot needed for rarity/overlap.                            |
| OBS006 Option generation                           | represented as a subcode               | NBM-R05 option-set facet                                                              | Distinct evidence retained without maintaining a separate full observable.                                                |
| OBS007 Choice procedure                            | represented as a subcode               | NBM-R05 resolution facet                                                              | Same choice episode; separate facet reduces burden while preserving distinction.                                          |
| OBS008 Revision after an initial decision          | retained substantially intact          | NBM-R06                                                                               | Distinct prerequisite: a prior actual decision followed by a reopening opportunity.                                       |
| OBS009 Preparation and contingency setup           | merged                                 | NBM-R07                                                                               | Same core evidence as A A02.                                                                                              |
| OBS010 Action initiation trigger                   | represented as a subcode               | NBM-R08 trigger modifier                                                              | Trigger is informative but is not independent of the initiation episode.                                                  |
| OBS011 Transition from stated intention to action  | merged                                 | NBM-R08                                                                               | Direct overlap with initiation timing.                                                                                    |
| OBS012 Handling simultaneous demands               | merged                                 | NBM-R10                                                                               | Shared-resource competition is the same observable allocation problem as A E02.                                           |
| OBS013 Use of external structure                   | retained substantially intact          | NBM-R09                                                                               | Concrete mechanism distinct from one-off task preparation.                                                                |
| OBS014 Immediate response to an obstruction        | merged                                 | NBM-R11 immediate-response facet                                                      | Immediate versus later response preserved sequentially.                                                                   |
| OBS015 Strategy adjustment across attempts         | merged                                 | NBM-R12                                                                               | Same method-comparison evidence as A B02.                                                                                 |
| OBS016 Outcome monitoring and feedback use         | narrowed                               | R13 for active acquisition; R12 for method change; passive feedback as event metadata | Source code combined distinct behaviors and passive events; separation improves observability and avoids double counting. |
| OBS017 Response to a recognized error              | retained substantially intact          | NBM-R14                                                                               | Specific prerequisite supports reliable distinction from generic feedback.                                                |
| OBS018 Completion and follow-up                    | merged                                 | NBM-R15                                                                               | Shares bounded-endpoint evidence with commitment follow-through.                                                          |
| OBS019 Repetition under recurring conditions       | moved to derived cross-episode summary | repeated-condition summary                                                            | Repetition belongs in aggregation.                                                                                        |
| OBS020 Change after prior experience               | moved to context/modifier metadata     | explicit cross-episode link field                                                     | Later behavior is coded elsewhere; causal link is stored separately.                                                      |
| OBS021 Response to a salient competing option      | merged                                 | NBM-R10                                                                               | Competing optional courses are treated as one subtype of constrained allocation.                                          |
| OBS022 Emotion-linked action shift                 | moved to context/modifier metadata     | state + sequence + explicit narrator link                                             | Avoids a second code for the same underlying action and causal overinterpretation.                                        |
| OBS023 Recovery and re-engagement after disruption | merged                                 | NBM-R11 later-goal-status facet                                                       | Same goal-course question after interruption.                                                                             |
| OBS024 Load-/fatigue-linked behavior change        | moved to derived cross-episode summary | context-conditioned comparison                                                        | Requires a baseline/comparison; not primitive episode evidence.                                                           |
| OBS025 Pressure-linked behavior change             | moved to derived cross-episode summary | context-conditioned comparison                                                        | Same reason: comparison-dependent rather than primitive.                                                                  |
| OBS026 Intention–action correspondence             | merged                                 | NBM-R08 and NBM-R15                                                                   | Generic correspondence duplicated start timing and endpoint follow-through; distributed by temporal target.               |
| OBS027 Help seeking and use of help                | merged                                 | NBM-R16                                                                               | Same mechanism as A C02.                                                                                                  |
| OBS028 Initiating social contact or coordination   | narrowed                               | NBM-R17                                                                               | Task coordination retained; generic optional social initiation excluded as too heterogeneous/context-loaded.              |
| OBS029 Communicating needs, limits, or uncertainty | retained substantially intact          | NBM-R18                                                                               | Distinct observable not adequately represented in Draft A.                                                                |
| OBS030 Response to requests and stated limits      | merged                                 | NBM-R19                                                                               | Same response class as A D01, broadened to others' stated limits.                                                         |
| OBS031 Behavior during disagreement                | merged                                 | NBM-R20                                                                               | Same concrete interaction sequence as A D02.                                                                              |
| OBS032 Interpersonal repair after strain or harm   | merged                                 | NBM-R21                                                                               | Same repair opportunity with slightly broader responsibility-neutral prerequisite.                                        |
| OBS033 Follow-through on interpersonal commitments | merged                                 | NBM-R15                                                                               | Reliance/formality retained as commitment-type context rather than separate endpoint code.                                |
| OBS034 Context-linked variability                  | moved to derived cross-episode summary | context-variability summary                                                           | Cross-episode property; primary coding would double count evidence.                                                       |
| OBS035 Change in repeated behavior over time       | moved to derived cross-episode summary | temporal-change summary                                                               | Cross-episode trajectory, not an episode behavior.                                                                        |

---

# 5. Ledger — source candidate constructs already rejected or treated as non-primary

The source drafts also explicitly discuss broader candidate constructs that should not silently reappear under new names. They remain excluded from first-pass primary measurement.

| Source construct(s)                          | Source | Decision                           | Measurement reason / behavioral replacement                                                                            |
| -------------------------------------------- | ------ | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Motivation                                   | A, B   | excluded                           | Hidden intensity/cause; use initiation, goal response, endpoint closure, and narrator-stated reasons.                  |
| Willpower / self-control                     | A, B   | excluded                           | Collapses competing-course response, external structuring, state/context, and follow-through.                          |
| Discipline                                   | A      | excluded                           | Normative composite of recurrence, preparation, initiation, and closure.                                               |
| Responsibility                               | A      | excluded                           | Normative umbrella; use closure, coordination, repair, or rule response.                                               |
| Reliability                                  | A      | excluded                           | Person-level evaluation; use repeated endpoint evidence and counterexamples.                                           |
| Resilience                                   | A, B   | excluded                           | Conflates disruption response, method change, re-engagement, affect, and outcome.                                      |
| Adaptability                                 | A, B   | excluded                           | Too broad; use decision revision, method adjustment, context-conditioned summaries.                                    |
| Flexibility                                  | A      | excluded                           | Ambiguous across methods, commitments, requests, and decisions.                                                        |
| Independence                                 | A      | excluded                           | Conflates help use, coordination, choice ownership, and social preference.                                             |
| Dependence                                   | A      | excluded                           | Same problem as independence plus evaluative loading.                                                                  |
| Assertiveness                                | A      | excluded                           | Mixes direct speech, refusal, negotiation, and conflict behavior.                                                      |
| Agreeableness                                | A      | excluded                           | Latent/global personality construct rather than episode behavior.                                                      |
| Conscientiousness                            | A      | excluded                           | Composite external construct spanning multiple primary behaviors.                                                      |
| Openness                                     | A      | excluded                           | External global construct; optional engagement and novelty context are coded directly.                                 |
| Extraversion / introversion                  | A      | excluded                           | Global dimensions not uniquely determined by concrete social episodes.                                                 |
| Neuroticism                                  | A      | excluded                           | External personality inference from affect or behavior.                                                                |
| Impulsivity                                  | A, B   | excluded                           | Requires a normative standard for deliberation; code choice, information, initiation, competing courses, and sequence. |
| Risk-taking / risk aversion / risk tolerance | A, B   | excluded                           | Global inference; R04 records concrete recognized-loss exposure setting.                                               |
| Confidence                                   | A, B   | moved to context/modifier metadata | Internal reported state may be retained if explicitly stated; does not uniquely determine action.                      |
| Courage                                      | A      | excluded                           | Normative inference from acting while afraid; retain reported fear plus actual action.                                 |
| Empathy                                      | A, B   | excluded                           | Requires inference about another mind; code questions, assistance, repair, communication.                              |
| Leadership                                   | A, B   | excluded                           | Conflates role, authority, initiation, influence, and coordination.                                                    |
| Proactivity                                  | A      | excluded                           | Broad evaluative umbrella; use initiation, planning, information, coordination.                                        |
| Avoidance / avoidance trait                  | A, B   | excluded                           | Functionally heterogeneous; specify what was deferred, declined, left, or not initiated and apply the non-action gate. |
| People-pleasing                              | A      | excluded                           | Motive inference; use R19 request responses and narrator-stated rationale.                                             |
| Perfectionism                                | A      | excluded                           | Latent/evaluative; use R07 preparation, R13 checking, R12 revisions, explicit standards as context.                    |
| Stubbornness                                 | A      | excluded                           | Evaluative interpretation; use method retention, goal continuation, or disagreement sequence.                          |
| Laziness                                     | A      | excluded                           | Moralized hidden-cause attribution.                                                                                    |
| Maturity / emotional maturity                | A, B   | excluded                           | Normative and developmentally theory-loaded.                                                                           |
| Emotional regulation                         | A      | excluded                           | Functional interpretation; states remain modifiers and behavior is coded directly.                                     |
| Emotional intelligence                       | B      | excluded                           | Broad evaluative construct not uniquely recoverable from episode behavior.                                             |
| Coping style                                 | A      | excluded                           | Broad theoretical grouping of heterogeneous episode behaviors.                                                         |
| Attachment style                             | A      | excluded                           | External psychological classification.                                                                                 |
| Personality type of any kind                 | A      | excluded                           | Composite latent classification outside first-pass measurement.                                                        |
| Decisiveness                                 | B      | excluded                           | Could reflect speed, option set, procedure, revision, uncertainty, or initiation.                                      |
| Trust                                        | B      | excluded                           | Cannot be uniquely inferred from delegation, disclosure, help use, or exposure.                                        |
| Authenticity                                 | B      | excluded                           | Normative/global judgment not operationally tied to one episode mechanism.                                             |
| Good judgment                                | B      | excluded                           | Requires an external standard of correctness or quality.                                                               |
| Rationality                                  | B      | excluded                           | Requires a normative decision model; procedures are coded without ranking them.                                        |
| Values / moral character                     | B      | excluded as primary observable     | Narrated values may be stored as claims; isolated actions do not establish character.                                  |
| Identity consistency                         | B      | excluded as primary observable     | Identity claims are stored separately; behavioral consistency is derived from episodes.                                |

## The source drafts independently reject many of these broad labels for the same measurement reasons. Draft A's explicit rejected-construct list emphasizes their inferential and evaluative nature, while Draft B likewise replaces them with concrete procedures and actions.

# 6. Unresolved decisions requiring blind pilot evidence

Conceptual reconciliation alone should not settle the following.

## U1 — R04 possible-loss exposure versus R03 unresolved uncertainty

**Question:** Can coders reliably distinguish “I do not know what will happen” from “I recognize a specific downside and choose how much exposure to accept”?

**Pilot evidence needed:** Double-code episodes containing:

* uncertainty without a stated downside;
* stated downside with no unresolved factual uncertainty;
* both together;
* objectively risky situations where narrator awareness is absent.

Compare applicability and subcode confusion, not merely total agreement.

---

## U2 — R05 option-set facet versus resolution facet

**Question:** Should option generation and choice procedure remain two facets of one observable or become separate primary codes?

**Pilot evidence needed:** Missingness and reliability separately for:

* how options entered consideration;
* how selection occurred.

If one facet is routinely unavailable while the other is reliable, separation may improve data integrity.

---

## U3 — R07 preparation versus R09 external structuring

**Question:** Can coders reliably distinguish one-off preparation of a focal action from modification of the external environment/system intended to shape later behavior?

**Pilot evidence needed:** Boundary cases involving calendars, checklists, laying out materials, reminders, recurring schedules, accountability partners, and environmental arrangement.

---

## U4 — R08 initiation versus R07 preparation

**Question:** When does preparation itself count as the start of the task?

**Pilot evidence needed:** Extended episodes containing research, document gathering, scheduling, rehearsal, tool setup, and administrative prerequisites. Ask coders separately for:

1. first task-directed behavior;
2. preparation subcode;
3. whether any period constitutes delay.

---

## U5 — R10 simultaneous demand versus optional competing course

**Question:** Is the merged “competing courses” observable easier to code than separate demand-allocation and salient-alternative observables?

**Pilot evidence needed:** Confusion matrices by competition type: two obligations, obligation versus leisure option, two discretionary options, and resource allocation across money/time.

---

## U6 — R11 immediate obstruction response versus later goal status

**Question:** Should these remain two facets of one observable or become separate codes?

**Pilot evidence needed:** Episodes with first response and long-term response both known. Measure whether coders systematically overwrite the first response with the eventual result.

---

## U7 — R13 active checking versus unsolicited feedback

**Question:** Does excluding passive feedback from R13 improve reliability without losing needed information?

**Pilot evidence needed:** Cases with self-checks, solicited review, automatic system notices, unsolicited criticism, obvious outcomes, and direct consequences.

---

## U8 — R15 bounded task closure versus interpersonal commitment follow-through

**Question:** Does reliance by another party require a distinct commitment observable?

**Pilot evidence needed:** Parallel cases involving:

* private definite intentions;
* ordinary bounded tasks;
* explicit promises;
* negotiated agreements;
* externally imposed requirements.

Compare whether the same endpoint subcodes remain reliable and whether commitment-specific communication adds unique reliable evidence.

---

## U9 — R16 help versus R17 coordination

**Question:** Can coders consistently distinguish asymmetric assistance from interdependent joint action?

**Pilot evidence needed:** Joint work where one person has expertise, task delegation, demonstrations, role division, collaborative troubleshooting, and ordinary teamwork.

---

## U10 — R18 communicating own limits versus R19 responding to another's request

**Question:** Can coders preserve both sides of exchanges such as “I can't do the afternoon, but I can do the morning”?

**Pilot evidence needed:** Multi-turn request episodes where a request elicits disclosure of a limit and then negotiation.

---

## U11 — R20 disagreement versus R21 repair

**Question:** When exactly does disagreement behavior end and repair opportunity begin?

**Pilot evidence needed:** Episodes involving disagreement, perceived offense, delayed awareness, apology during continuing dispute, clarification without apology, and later resumed contact.

---

## U12 — Context split versus mixed

**Question:** How much evidence is necessary before coders should treat a behavioral difference as context-linked rather than merely mixed?

**Pilot evidence needed:** Matched sets with:

* one episode per context;
* two episodes per context;
* mostly systematic patterns with one exception;
* context variables that covary.

Measure the context rule separately from primary code agreement.

---

## U13 — Derived repeated-condition threshold

**Question:** Is three opportunities a workable minimum for a repeated-condition summary, or does an anchored repeated-series report support reliable recurrence with fewer concrete anchors?

**Pilot evidence needed:** Compare coder agreement on:

* two concrete occurrences only;
* one concrete occurrence plus “every week”;
* two concrete occurrences plus anchored frequency statement;
* three or more enumerated occasions with exceptions.

---

## U14 — State-linked metadata

**Question:** Does moving emotion/fatigue/pressure out of primary codes reduce double coding without losing reliable sequence information?

**Pilot evidence needed:** Have coders independently record:

1. state present;
2. state intensity if explicitly reported;
3. underlying action code;
4. explicit narrator influence claim;
5. temporal relation only.

Evaluate whether an additional state-action primary code would add reliable information rather than duplicating these fields.

---

# 7. Pilot-readiness check

## 7.1 Highest-risk coder-confusion pairs

Highest priority:

1. **R07 Preparation ↔ R08 Initiation**
2. **R07 Preparation ↔ R09 External Structuring**
3. **R03 Unresolved Uncertainty ↔ R04 Possible-Loss Exposure**
4. **R05 Choice Construction ↔ R02 Information Seeking**
5. **R05 Choice Resolution ↔ R06 Decision Revision**
6. **R10 Competing-Course Allocation ↔ R11 Goal Response to Disruption**
7. **R11 Goal Response ↔ R12 Method Adjustment**
8. **R12 Method Adjustment ↔ R13 Outcome Checking**
9. **R13 Outcome Checking ↔ R14 Error Response**
10. **R15 Endpoint Closure ↔ R08 Initiation**
11. **R16 Help Seeking ↔ R17 Coordination**
12. **R18 Own-Condition Communication ↔ R19 Request/Limit Response**
13. **R19 Request Response ↔ R20 Disagreement**
14. **R20 Disagreement ↔ R21 Repair**
15. **IE ↔ NA**
16. **qualifying non-action ↔ unknown/nonmentioned behavior**

Confusion matrices should be examined for these pairs rather than relying only on one overall reliability statistic.

---

## 7.2 Most important episode-segmentation problems

Special pilot material should include:

* a long story containing multiple choice points but one continuous goal;
* the same task revisited after a meaningful time gap;
* repeated recurring occasions compressed into one narrative paragraph;
* one obstacle followed by multiple attempts;
* an initial decision followed by later revision;
* a request that becomes a disagreement and later a repair episode;
* a goal interrupted and resumed the next day;
* one task with preparation, initiation, checking, error correction, and closure;
* a prior experience referenced in a later episode;
* one event retold twice in different interview sections.

Coders should mark episode boundaries **before** assigning substantive codes in the first pilot.

## Both source drafts already flag segmentation as a major reliability risk.

## 7.3 Distinctions requiring special training examples

Training sets should deliberately oversample:

* non-action with missing awareness;
* non-action with missing feasibility;
* non-action with an undefined response window;
* preparation that is itself the first task-directed action;
* preparation that genuinely precedes task initiation;
* information seeking versus practical help;
* option generation versus comparison;
* uncertainty versus recognized possible loss;
* changed goal versus changed method;
* immediate obstruction response versus eventual stopping;
* passive feedback versus deliberate checking;
* disputed possible error versus acknowledged error;
* aspiration versus definite intention;
* definite intention versus interpersonal promise;
* task completion versus negotiated endpoint change;
* request negotiation before any disagreement;
* disagreement that later produces strain;
* strain recognized only long after the interaction;
* explicit rule versus informal convention;
* temporal precedence versus explicit narrator-stated influence;
* systematic context split versus mixed evidence;
* behavior change over time with later reversion.

---

## 7.4 Constructs likely to be too rare for stable reliability estimates in small pilots

Potentially sparse observables include:

* **R04 Possible-Loss Exposure**, because awareness of the downside and alternative exposure levels must both be explicit;
* **R14 Error Response**, because a recognized self-attributable possible error must occur;
* **R21 Interpersonal Repair**, because awareness of strain and a repair opportunity must be documented;
* **R22 Rule/Procedure Response**, depending on interview content;
* some R11 stopping/re-engagement subcodes;
* explicit concealment subcodes in R14 or R22;
* R09 disabling/bypassing external structure.

Low frequency should not be “fixed” by relaxing prerequisites. Rare codes should remain IE/NA where appropriate.

Draft B separately warns that error, repair, and possible-loss opportunities may be uncommon, reinforcing the need to treat rarity as a sampling issue rather than fill missing cells by inference.

---

## 7.5 What should be measured separately in the first double-coding pilot

Do not collapse the first pilot into one global reliability statistic. Measure separately:

1. **Episode boundary identification**
2. **Episode-link identity** — same incident versus independent occurrence
3. **Prerequisite/applicability judgment for each observable**
4. **Non-action gate**

   * awareness
   * opportunity
   * feasibility
   * defined window / established non-action
5. **Primary substantive subcode**
6. **Sequential subcode ordering**
7. **Evidence-state assignment**
8. **IE versus NA**
9. **Missingness flag assignment**
10. **Context-modifier extraction**
11. **Explicit narrator influence versus temporal precedence**
12. **Counterepisode identification**
13. **Person-level recurrence determination**
14. **Context splitting versus mixed**
15. **Derived repeated-condition summary**
16. **Derived temporal-change summary**
17. **Coder use of OS (“other specified”)**
18. **Coder burden**, including time and skipped/forced decisions by observable

Where a primary observable contains two facets—especially R05 and R11—reliability should be reported separately for each facet before deciding whether the combined structure is sustainable.

---

# 8. Recommended blind-pilot coding record

For each episode:

`Person ID | Episode ID | transcript locator | situation | focal goal/opportunity | prerequisite status | awareness | opportunity | feasibility | observation window | primary observable ID | substantive value(s) in sequence | evidence state | evidence excerpt | outcome | context modifiers | state modifiers | narrator-explicit influence claim | missingness flags | counterepisode links | coder note`

For person-level derived summaries:

`Person ID | observable | scope | qualifying opportunities | supporting episode IDs | counterepisode IDs | substantive value(s) | evidence state | context split if supported | time period | recurrence basis | uncertainty note`

---

# 9. Pilot use constraint

This candidate is intended to test whether blind human coders can reliably recover the specified behavioral distinctions from concrete first-person autobiographical episodes.

The pilot should be allowed to show that:

* some distinctions are unreliable;
* some should be merged;
* some need narrower prerequisites;
* some are too rare;
* some context modifiers are not reproducible;
* some episode boundaries require a better rule;
* some source constructs add no independent information.

Such findings should drive **version 2 measurement revision before any external-model comparison**.

No code should be retained because it appears theoretically interesting, and no code should be revised to improve correspondence with an external target.

**This exact reconciliation output must be preserved unchanged before any external hypothesis, target model, prediction, or model-fit result is revealed.**