# Life Patterns participant-adjudicated semantic repair — candidate v1 — 2026-09-12

Status: **CANDIDATE ONLY — TARGET-THEORY-BLIND — NOT PRODUCTION AUTHORITY**

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Authoring base / live PR head at task start and immediately before commit: `1ebc72153e985abbe85b2f88e0d76c3512ce8d11`
Draft PR: `#24`

This candidate was authored under the fresh target-theory-blind launch packet `tasks/LIFE-PATTERNS-FRESH-THEORY-BLIND-SEMANTIC-REPAIR-LAUNCH-2026-09-12.md`. The authoring context did **not** inspect target-model mappings or scoring, fit results, birth/chart outputs, prior predictions, or any indication of which neutral behavioral findings would favor a candidate theory.

Historical V1/V2/V5 artifacts remain immutable. This candidate does not authorize human collection, automated participant coding, target-model scoring/reveal, merge, or deployment. Production implementation remains blocked pending separate fresh target-theory-blind semantic review.

---

## 1. Decision

Adopt a **participant-adjudicated neutral semantic freeze** whose primary substrate is:

1. immutable source episodes and exact provenance;
2. minimally structured, open-world episode facts;
3. system-authored candidate pattern questions kept explicitly as hypotheses;
4. recursive participant adjudication of whether a proposed person-level pattern actually characterizes the participant, with scope, conditions, exceptions, corrections, examples, and counterexamples preserved separately;
5. a frozen adapter-input projection created only after that adjudication history is recorded.

Do **not** retain the fixed 22-observable taxonomy as the mandatory semantic core. It remains development history and a source of reusable mechanics.

Do **not** infer participant-level recurrence, typicality, or scope from episode counts. Descriptive episode aggregates may remain as diagnostics and question-generation aids only.

Do **not** require `OS` / Other Specified as a primary code in the new substrate. Open-world factual records make a catch-all category unnecessary at the semantic core. If any optional indexing vocabulary is later used, unmatched clear behavior must be retained and surfaced as a vocabulary-gap signal rather than downgraded to `insufficient`.

---

## 2. Independent conception snapshot preserved before existing-work scan

Before consulting external methods literature, the repair conception was fixed as:

> Use minimal episode facts with exact provenance, keep appraisal and absence epistemically distinct from positive reported events, and make person-level pattern recurrence recursively participant-adjudicated rather than mechanically inferred from episode counts.

The external scan below was then used to test whether that mechanism already exists, should be reused, or needs project-specific adaptation.

---

## 3. Bounded existing-work scan and reuse decision

### 3.1 Strongest relevant established work checked

The bounded scan focused on qualitative member checking / participant validation and participatory qualitative analysis rather than on any target theory.

1. **Birt L, Scott S, Cavers D, Campbell C, Walter F. (2016). _Member Checking: A Tool to Enhance Trustworthiness or Merely a Nod to Validation?_ Qualitative Health Research.** DOI: `10.1177/1049732316654870`; PMID: `27340178`.
   - The paper critiques superficial one-shot “validation” and describes Synthesized Member Checking, in which participants engage with and add to both interview and interpreted data.
   - Project relevance: supports iterative participant engagement with researcher/system interpretation rather than treating an external coding pass as final person-level truth.

2. **Jennings H, Slade M, Bates P, Munday E, Toney R. (2018). _Best practice framework for Patient and Public Involvement (PPI) in collaborative data analysis of qualitative mental health research: methodology development and refinement._ BMC Psychiatry.** DOI: `10.1186/s12888-018-1794-8`; PMID: `29954373`; PMCID: `PMC6022311`.
   - The paper identifies consultation, development, application, and development-plus-application forms of collaborative qualitative analysis, and emphasizes co-production where appropriate.
   - Project relevance: supports meaningful participant/lived-experience involvement in interpretation, but does not require every participant to co-design a universal codebook.

3. **Jackson SF. (2008). _A participatory group process to analyze qualitative data._ Progress in Community Health Partnerships.** DOI: `10.1353/cpr.0.0010`; PMID: `20208250`.
   - The described process gives community researchers substantive control over interpretation rather than limiting them to raw-data provision.
   - Project relevance: reinforces separation between extracting material and deciding what it means at the interpretive level.

### 3.2 What is already solved vs project-specific

| Question | Existing work status | Project decision |
|---|---|---|
| Can participants meaningfully engage with interpretations rather than merely supply data? | Established in member checking / collaborative qualitative analysis. | **Reuse/adapt.** |
| Should participant feedback be iterative rather than a single yes/no validation event? | Supported by synthesized member checking and participatory methods. | **Reuse/adapt.** |
| Must participant involvement imply a universal participant-designed coding taxonomy? | No. Participatory analysis supports multiple levels/forms of involvement. | **Reject as unnecessary.** |
| How should exact source facts be frozen before later competing-model interpretation? | Not solved by those qualitative methods. | **Project-specific composition required.** |
| How can competing models receive one shared semantic substrate without forcing a closed ontology? | Not solved by the checked methods. | **Project-specific composition required.** |
| Can participant endorsement be treated as objective causal truth? | No; qualitative participant validation does not convert self-report into objective fact. | **Explicitly reject.** Participant adjudication governs self-characterization, recurrence and scope in this product record, not external objective truth. |

### 3.3 Reuse / adaptation / invention decision

**Decision: adaptation + composition.**

Reuse established iterative participant-validation/co-analysis principles for person-level interpretation. Compose them with the project’s already-developed exact-provenance, immutable-freeze, missingness, and absence-gate mechanics. Invent only the narrow project-specific interface needed to freeze that participant-adjudicated record before later competing-model adapters consume it.

This is preferable to further extending the fixed ontology because the latter solves the wrong problem: it makes external classification more complete, but participant-level recurrence and scope still would not become participant-adjudicated merely by adding more categories.

---

## 4. Minimum shared frozen substrate

The scientific requirement is not “one exhaustive ontology.” The requirement is:

> **Every later model must consume the same pre-model, theory-blind, immutable semantic record and must not go back to raw narrative to reinterpret it after model-specific outputs are available.**

### 4.1 Alternatives compared

| Candidate substrate | Strength | Failure mode | Disposition |
|---|---|---|---|
| A. Structured participant-adjudicated pattern claims + exact episode provenance only | Very compact; directly aligned with the product. | Risks losing literal episode facts needed to audit whether a generalization distorted source material and to generate better follow-up questions. | **Too thin alone.** |
| B. Minimally structured episode facts + participant-adjudicated person-level patterns | Preserves source semantics, supports questioning, and makes recurrence explicitly participant-adjudicated without requiring an exhaustive taxonomy. | Requires disciplined epistemic typing and provenance. | **RECOMMENDED CORE.** |
| C. Compact extensible episode-fact vocabulary only for indexing/question generation | Useful retrieval and QA aid without claiming exhaustive semantics. | Becomes harmful if tags silently become the authoritative meaning of the episode. | **OPTIONAL SECONDARY INDEX.** |
| D. Mandatory categorical person-level codes | Easy to score and calibrate mechanically. | Recreates the fixed-taxonomy premise; external coder can silently become final authority on recurrence and scope. | **NOT CORE.** Use only if a later decision demonstrates a genuinely necessary category and it survives blind review. |

### 4.2 Retained structured categories and why each is necessary

The episode layer uses **epistemic roles**, not a personality taxonomy.

1. `reported_event` — preserves a positively reported action, choice, transition, consultation, information-seeking act, timing relation, outcome, or resolution. Needed to preserve what the participant says happened without requiring a construct label.
2. `reported_appraisal` — preserves the narrator’s stated belief, evaluation, motive, interpretation, or reason without promoting it to objective fact. Needed because “I thought it was infeasible” is materially different from “it was infeasible.”
3. `externally_supported_condition` — optional and only when the frozen source actually contains independent support for an objective condition. Needed so stronger evidence can be represented without conflating it with narrator appraisal.
4. `gated_absence` — represents genuine nonoccurrence only when awareness, opportunity, reasonable feasibility, and established nonoccurrence are all established for a defined window. Needed because absence is a stronger claim than a positive event report.
5. `context` — records relevant situational or life-phase qualifiers when directly supported. Needed to ask whether a candidate pattern is global or context-bound.

The factual content itself remains open-world text plus exact provenance. Optional index tags can be added for retrieval/question generation but are not required to preserve a fact and are not the semantic authority.

---

## 5. Revised semantic layers

### Layer 0 — immutable source evidence

Preserve the already-useful behavioral-freeze mechanics:

- episode identity;
- source-turn/segment identity;
- exact source hashes;
- participant revision status;
- input modality where relevant;
- immutable/content-addressed artifact identity.

Later semantic records must point into this frozen evidence. A model adapter must never substitute a new reading of the raw transcript for the frozen semantic record.

### Layer 1 — open-world episode fact records

A single episode may yield zero, one, or multiple facts. A fact is a small source-supported proposition, not a person-level trait.

Recommended fields are specified normatively in the companion contract:

`state/LIFE-PATTERNS-PARTICIPANT-PATTERN-RECORD-CONTRACT-v1-CANDIDATE-2026-09-12.json`

Each fact must preserve:

- `fact_id`;
- `episode_id`;
- epistemic role;
- neutral proposition text;
- exact source provenance;
- optional sequence/timing relation;
- optional context qualifiers;
- optional index tags that cannot replace the proposition;
- explicit uncertainty where needed.

A clear positive behavior with no available category remains a valid fact. “No category fits” is never sufficient reason to emit `insufficient`.

### Layer 2 — candidate pattern proposal

A system may propose a person-level generalization **only as a hypothesis/question**. It must record:

- exact proposal text;
- non-leading question text shown to the participant;
- the fact IDs or prior adjudication material that motivated the proposal;
- proposed scope/conditions, if any;
- proposal version/round.

The proposal does not become a participant pattern merely because multiple episodes appear similar.

### Layer 3 — recursive participant adjudication

Use the loop:

`episode -> factual decomposition -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question -> participant adjudication -> accepted/rejected/unresolved pattern`

Each adjudication round keeps the system proposal and participant response separate. The participant may revise:

- whether the generalization fits at all;
- its wording;
- recurrence/typicality claim;
- contexts in which it does or does not fit;
- conditions/triggers;
- exceptions;
- relevant life phases;
- whether supplied examples are representative, unusual, private, uncertain, or merely illustrative.

No previous round is overwritten. A later correction supersedes the current candidate formulation while preserving the history that produced it.

### Layer 4 — final participant pattern record

Final state is one of:

- `accepted`;
- `rejected`;
- `unresolved`.

Only an explicit participant adjudication may finalize this state. Episode counts, external classifier votes, coder agreement, or model fit cannot do so.

An accepted pattern stores the participant-confirmed formulation plus confirmed scope/conditions/exceptions. A rejected pattern remains in the frozen record as a rejected hypothesis rather than disappearing. An unresolved pattern preserves the unresolved question and the reason/ambiguity where available.

### Layer 5 — frozen adapter-input bundle

After the semantic record is complete and separately reviewed, create one immutable projection for later model adapters. All competing adapters receive the same projection.

Adapters may consume:

- canonical episode fact propositions and their epistemic roles;
- final accepted/rejected/unresolved pattern records;
- participant-confirmed scope, conditions and exceptions;
- support links to fact IDs;
- evidence-role labels on examples/counterexamples;
- unresolved/gap records;
- provenance hashes sufficient for audit.

Adapters may **not**:

- reread raw transcript/episode narrative to invent a model-specific semantic interpretation;
- alter the frozen fact proposition;
- recode narrator appraisal as objective condition;
- derive a new person-level recurrence state from episode counts;
- suppress rejected/unresolved records merely because they are inconvenient to a model;
- request target-tailored recoding before comparison.

The adapter mappings themselves can later be model-specific, but they must map from the **same frozen semantic bundle**, be versioned/frozen under the project’s model-comparison protocol, and remain downstream of this target-theory-blind semantic layer.

---

## 6. Positive behavior and absence claims

### 6.1 Positive facts survive an absence-gate failure

The old architecture correctly recognized that non-action is a stronger claim than an action report, but fixed categorical values could entangle the two.

The repair separates them.

Example structure:

- `reported_event`: “Participant postponed enrollment until a later term.”
- `reported_appraisal`: “Participant reported considering the course too difficult at that time.”
- attempted `gated_absence`: “Participant did not investigate any alternatives before postponing.”

If awareness/opportunity/reasonable-feasibility/nonoccurrence cannot all be established for the last proposition, the absence assertion is `unestablished` or omitted from established facts. The postponement and narrator-reported appraisal remain intact.

The stronger failed inference must never erase the weaker supported observations.

### 6.2 Four-part gate retained exactly in substance

For every genuine absence/nonoccurrence assertion, retain:

1. `awareness` — was the actor aware of the relevant option/action?
2. `opportunity` — was there a meaningful opportunity in the defined window?
3. `reasonable_feasibility` — was the action reasonably feasible in that window?
4. `established_nonoccurrence` — is nonoccurrence itself established rather than merely unmentioned?

Only `established + established + established + established` can yield an established absence fact.

A failed/unclear gate may itself be stored as an unresolved absence assessment for audit/question generation, but it must not masquerade as an observed absence.

---

## 7. Appraisal versus objective condition

The semantic record must preserve evidence direction.

Allowed:

- “Participant reported believing the application was too difficult.”
- “Participant said cost made the option unattractive.”
- “The frozen external record states the application deadline had passed.”

Not allowed without independent support:

- “The application was too difficult.”
- “The option was infeasible.”

The participant remains authoritative over their reported appraisal. That does not transform the appraisal into an objective property of the world.

---

## 8. Open-world gap discovery and the disposition of `OS`

Historical V2’s universal `OS` mechanic solved an important local failure: a clear behavior should not disappear merely because a named code does not fit.

The new architecture generalizes that safeguard rather than requiring a catch-all code.

### Core rule

**Open-world fact propositions are always representable without a categorical code.**

Therefore:

- core semantic preservation does not require `OS`;
- optional index vocabularies may use an `unmatched`/gap state for retrieval diagnostics;
- a mismatch may create a theory-blind vocabulary-gap candidate;
- the underlying fact remains first-class and provenance-bound;
- repeated common unmatched behavior is evidence that the index vocabulary is inadequate, not that participants are “insufficient.”

If a future bounded vocabulary becomes normatively necessary for a narrow decision, it must include an explicit open-world escape and undergo separate theory-blind review.

---

## 9. Simplifying R05-type episode representation

The R05/V5 option-set + resolution machinery demonstrated useful local referential-integrity and absence-gate mechanics, but its facet structure is not required as the new product’s episode semantic core.

Represent the source more directly:

- positive action/choice facts;
- timing or transition facts;
- consultation/information/search actions actually reported;
- outcome/resolution facts;
- narrator appraisals/reasons;
- context;
- separately gated absence claims.

For example, “accepted a default, later changed course, and said the alternative initially seemed too costly” does not require a fixed “option-set facet” plus “resolution facet” to be retained faithfully. It can be decomposed into three source-supported propositions and later used to ask a participant whether any recurring pattern is present.

This reduces inference at the episode layer while preserving more raw semantic detail.

---

## 10. Examples, counterexamples, and recurrence evidence

Every example link must carry an `evidence_role`.

Recommended roles:

- `source_episode` — episode existed before the pattern proposal and may legitimately motivate the proposal;
- `elicited_example` — supplied after a candidate pattern question; useful for meaning/scope, not an unbiased recurrence-frequency sample;
- `elicited_counterexample` — useful for boundary conditions and revising scope;
- `elicited_nuance` — clarifies meaning but should not be counted as independent recurrence evidence.

A participant can explicitly state that an elicited example is typical, atypical, representative, or exceptional. Preserve that judgment. Do not infer population/frequency properties simply from the participant’s ability to retrieve examples after prompting.

---

## 11. Strong endorsement with poor example retrieval

An accepted or strongly endorsed candidate need not be invalidated because the participant cannot immediately retrieve examples.

Record the discrepancy explicitly and probe without diagnosis. Possible explanations include:

- retrieval difficulty;
- vague identity-level belief;
- privacy;
- low salience;
- misunderstanding of the question;
- limited self-observation;
- other participant-supplied explanations.

The system may ask a neutral follow-up. It may not automatically label the participant as lacking self-awareness. A repeated “endorsement without examples” phenomenon becomes a candidate meta-pattern only through the same participant-adjudication loop.

---

## 12. Descriptive aggregation is retained but demoted from semantic authority

The existing neutral-measurement implementation already labels its person aggregation:

`descriptive_distribution_preserving_no_trait_collapse`

That is the correct boundary.

Retain counts/coverage/context summaries when useful for:

- finding underexplored contexts;
- generating candidate questions;
- quality assurance;
- sampling/calibration diagnostics.

They must never directly set:

- final pattern state;
- recurrence/typicality;
- participant scope;
- accepted conditions or exceptions.

No threshold such as “2+ episodes = recurring pattern” is allowed as semantic finalization.

---

## 13. Old-mechanic disposition

| Existing mechanic | Disposition | Reason |
|---|---|---|
| Exact episode/source-turn provenance + hashes | **RETAIN** | Prevents unsupported semantic drift and makes every proposition auditable. |
| Immutable/content-addressed artifacts | **RETAIN** | Needed to freeze shared pre-model meaning. |
| Explicit `insufficient` / `not_applicable` distinctions | **RETAIN / ADAPT** | Missingness remains informative, but lack of taxonomy fit is not `insufficient`. |
| Participant-revised episode marker | **RETAIN** | Participant correction of source material matters to provenance. |
| Narrator appraisal distinct from objective condition | **RETAIN / STRENGTHEN** | Prevents self-reported reason/belief from becoming world fact. |
| Four-part absence/non-action gate | **RETAIN** | Stronger absence claims require awareness, opportunity, reasonable feasibility, and established nonoccurrence. |
| Positive and absence components represented separately | **RETAIN CONCEPTUALLY, SIMPLIFY RECORD SHAPE** | Essential evidence-direction safeguard; full V5 graph is not mandatory for ordinary facts. |
| Referential integrity between claims and evidence | **RETAIN** | Prevents dangling/ambiguous provenance. |
| Event stages / evidence-unit identity where genuinely needed | **OPTIONAL / ADAPT** | Useful for complex temporal cases, but should not be mandatory schema overhead for simple facts. |
| Universal `OS` catch-all | **SUPERSEDE AS CORE CODE; RETAIN PRINCIPLE** | Open-world propositions make a named catch-all unnecessary; unmatched facts must still survive and surface gaps. |
| Fixed 22-observable taxonomy | **SUPERSEDE AS PRIMARY SEMANTIC CORE** | Not required by neutrality; overconstrains product semantics. Historical artifact remains immutable. |
| R05 fixed option-set/resolution facets | **SUPERSEDE AS MANDATORY EPISODE SHAPE** | Simpler factual decomposition preserves the same positive facts with less inference. |
| Full V5 graph for every response | **SUPERSEDE AS DEFAULT** | Retain only mechanics that solve an actual claim; complexity is diagnostic rather than an objective. |
| External coder final person-level recurrence/typicality | **REJECT** | Recurrence/scope are participant-adjudicated in this product record. |
| Episode-count-derived person pattern | **REJECT** | Counts are descriptive/question-generating, not adjudicative. |
| External human/automated calibration of literal fact extraction | **RETAIN / REFRAME** | Appropriate if target is source-faithful fact extraction rather than a supposed true person-level label. |

---

## 14. Calibration target after repair

### Episode-fact extraction may be externally calibrated for

- source-proposition fidelity;
- exact provenance;
- correct epistemic role;
- appraisal/objective separation;
- positive-fact preservation;
- correct application of the four-part absence gate;
- abstention/uncertainty when support is inadequate;
- open-world retention rather than forced categorization.

### Person-pattern process should be calibrated for

- whether candidate questions are non-leading and grounded in frozen facts;
- whether the participant’s corrections are preserved exactly enough to be recognizable;
- whether scope, conditions and exceptions are revised correctly;
- whether rejected and unresolved hypotheses remain visible;
- whether elicited examples are distinguished from unbiased recurrence evidence;
- whether the final formulation is participant-recognized and properly scoped;
- whether system proposals remain distinct from participant adjudications.

Do **not** define person-pattern success as agreement between external coders on a person-level label the participant did not adjudicate.

---

## 15. Later model-adapter contract

The purpose of the semantic freeze is to prevent model-specific rereading, not to pre-map behavior into model constructs.

The frozen adapter input must have one content hash. Every model adapter receives the same hash-bound bundle.

The semantic bundle exposes neutral records only. It contains no target-model label, score, expected direction, prediction, fit result, birth/chart output, or model-specific hint.

A later adapter may map the frozen record into its own pre-specified model vocabulary. It must not request a new semantic extraction tailored to its model or reopen the raw interview to seek favorable details.

If a later model requires information absent from the frozen bundle, that is recorded as **model-input missingness**. It is not permission to reinterpret the source differently for that model.

This is the anti-leakage guarantee that the fixed external ontology was trying to provide, without requiring the ontology itself.

---

## 16. Focused test requirements for a later implementation

No production implementation is authorized by this candidate. A subsequent implementation should at minimum prove the following.

1. **Open-world positive preservation** — a clear reported action with no index/category match remains a valid episode fact with provenance.
2. **No facet-forcing** — a fact can exist with no facet/category/tag when classification is uncertain.
3. **Appraisal isolation** — “participant considered X infeasible” cannot validate as `externally_supported_condition: X was infeasible` without independent support.
4. **Positive facts survive absence failure** — unclear feasibility for a no-search claim cannot remove a supported postponement/rejection/consultation/action fact from the same episode.
5. **Four-part absence gate** — established absence requires awareness + opportunity + reasonable feasibility + established nonoccurrence; any unclear/not-established element prevents established absence.
6. **Absence nonmention is insufficient** — silence about an action cannot itself establish nonoccurrence.
7. **Exact provenance integrity** — every established fact and every participant adjudication points to valid frozen source/adjudication records; dangling references fail closed.
8. **Recursive history preserved** — proposal round 1, participant correction, revised proposal round 2 and final adjudication remain separately inspectable; later rounds never overwrite earlier text.
9. **Participant-only finalization** — no function consuming only episode counts/facts may emit final `accepted`/`rejected` person-pattern state.
10. **Descriptive aggregation boundary** — episode counts may generate a candidate question but cannot change final recurrence/typicality fields.
11. **Elicited-example role** — an example produced after a proposal is tagged `elicited_example`/`elicited_counterexample`/`elicited_nuance` and is excluded from any unbiased recurrence-sample count.
12. **Endorsement-without-example allowed** — participant acceptance plus failed example retrieval remains representable without forced rejection or a self-awareness diagnosis.
13. **Rejected/unresolved preservation** — later adapter projection retains rejected and unresolved hypotheses or explicit constraints rather than dropping them as missing.
14. **Gap discovery** — repeated unmatched open-world facts can produce a vocabulary-gap diagnostic without altering the facts themselves.
15. **Single frozen adapter projection** — all later adapters bind the same semantic-bundle hash and cannot request raw narrative text through the adapter interface.
16. **No target-theory fields** — candidate semantic artifacts and adapter-input projection reject target labels/scores/prediction fields.
17. **Legacy immutability** — V1/V2/V5 artifacts and their parsers remain unchanged; the new path is versioned separately.
18. **Theory-blind review gate** — candidate cannot become production authority without a separate fresh target-theory-blind review receipt bound to the exact candidate/contract hashes.

---

## 17. Candidate-review questions

A separate fresh target-theory-blind reviewer should try to falsify this candidate by asking:

1. Does any retained structure still smuggle in a fixed taxonomy requirement that is unnecessary for the decision it serves?
2. Can any positive reported fact disappear merely because a category/facet/absence gate fails?
3. Can a narrator appraisal become an objective condition without independent evidence?
4. Can episode frequency, external coder consensus, or classifier output silently become person-level recurrence/typicality?
5. Can elicited examples be misread as unbiased recurrence samples?
6. Can a participant’s correction be lost when a candidate pattern is revised?
7. Can an adapter later reread raw narrative differently for different models?
8. Is any field present only because the historical V5 machinery had it, rather than because it improves source fidelity, questioning, participant adjudication, auditability, or the frozen adapter interface?
9. Does the architecture preserve rejected and unresolved hypotheses as evidence rather than silently collapsing them into missingness?
10. Is the north star still participant-recognizable unique life patterns rather than completion of an ontology?

---

## 18. Current authorization boundary

This candidate may be independently reviewed.

It does **not** authorize:

- production schema/runtime implementation;
- migration of historical artifacts;
- human participant collection;
- automated participant coding;
- target-model mapping/scoring/reveal;
- birth/chart processing for this task;
- recruitment/contact;
- merge or deployment.

Next scientific gate: **separate fresh target-theory-blind semantic review of this exact candidate and its companion contract.**
