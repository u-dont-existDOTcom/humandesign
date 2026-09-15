# Life Patterns codebook architecture root-cause audit — 2026-09-11

Status: owner-directed design-history audit. This does not delete or rewrite historical V1/V2/V5 artifacts. It identifies the architectural premise that should be superseded for future Life Patterns development.

## Decision

The elaborate fixed codebook process did **not** arise because strict theory-blindness logically requires a comprehensive external behavioral ontology. It arose from a legitimate anti-leakage requirement followed by an unjustified architectural substitution:

> **Need:** competing birth-derived models must not be allowed to reinterpret the participant's narrative differently after seeing their own predictions.
>
> **Substitution:** therefore the neutral substrate must be a fixed externally coded ontology with categorical values, frozen aggregation, and inter-rater reliability as the primary measurement instrument.

The first statement is correct. The second does not follow from it.

A stable, theory-blind, content-addressed participant-adjudicated pattern record with exact episode provenance can satisfy the anti-leakage requirement without making an external taxonomy the semantic authority on the person's recurring patterns.

## Chronology of the drift

### 1. 14:52 UTC — the original product already had the right center

Commit `026be220b18bbfd10ccfb1ac8d0db69f2d7f8971` (`docs: add Discover Your Unique Life Patterns roadmap`, 2026-09-03 14:52:35 UTC) defined the north star as an intrinsically useful interview producing a high-resolution evidence-backed map of how the participant actually operates.

It explicitly said:

- the product should feel like an attentive interview, not a personality quiz;
- the primary evidence chain ends in a **participant-confirmed summary**;
- the participant-facing map contains recurring/context-dependent patterns, counterexamples and limits;
- the interviewer should reflect tentative patterns back and ask the participant to correct overgeneralization;
- progress is not a fixed questionnaire-completion denominator.

The same roadmap also contained the seed of the later problem: it proposed a `model family requirements -> neutral measurement ontology -> chart-blind interview -> behavioral lock -> model scoring` flow. Thus the correct participant-centered product and an untested ontology assumption coexisted from the first roadmap.

### 2. 15:29–15:40 UTC — participant authority was strengthened, not weakened

The implementation then added participant episode review, required approved episodes for evidence, and made review occur before the interview continued (`70717f2f...`, `8dbd07e2...`, `342a20d5...`).

The missing-chat reconstruction at `e7cee21b880016ca97ef7f1520c193d6d7518fc5` confirms that the product direction was participant-reviewed Life Patterns, not an external personality test. It is explicitly a reconstruction, not a verbatim transcript, so exact conversational attribution is unavailable.

### 3. 17:04 UTC — the behavioral freeze still preserved participant-adjudicated patterns

Commit `6677f3866bcb6c79a824fea24ce1efb62dd847a7` (`docs: specify participant-reviewed behavioral freeze`, 17:04:41 UTC) defined:

`chart-blind interview -> participant-approved episodes -> neutral Life Patterns Map -> participant review of map claims -> immutable behavioral freeze -> later model tournament`

Map claims were individually `approve | edit | reject | uncertain`; only approved/edited claims became admissible. This already supplied a neutral, participant-adjudicated, immutable research object with provenance.

### 4. 17:23 UTC — a legitimate model-comparison problem was identified

Commit `7e294c18962342c06149815721c560d9179796c2` (`docs: specify post-freeze model tournament boundary`, 17:23:25 UTC) correctly observed that allowing each model to perform a flexible post-hoc LLM interpretation of raw narrative would create large researcher/model degrees of freedom.

It therefore required every model to bind a frozen **measurement bridge**. That requirement is sound.

The critical unsupported step appears in the stated next work: **“Design/freeze the neutral measurement ontology and bridge contract against the Life Patterns freeze.”** A frozen bridge was necessary; a new comprehensive shared ontology was treated as the predetermined solution rather than one candidate implementation.

### 5. 17:35 UTC — the solution became an external ontology/coder instrument

Only 12 minutes later, commit `5d40e6608ff7af3c8550d4eb5d746ccac6fa5088` (`docs: specify neutral Life Patterns measurement bridge`, 17:35:33 UTC) made the decisive change.

Its pre-scan conception states:

`immutable behavioral freeze -> versioned neutral ontology -> coded observable evidence`

and explicitly says the **shared ontology/coder is the main measurement instrument**. Person-level summaries are then derived from episode codes through frozen aggregation.

The external-method scan reinforced this choice with ontology engineering, psychometrics, codebook development, inter-rater reliability, annotation tooling, and selective-classification methods. These are legitimate methods for standardized annotation tasks, but they were imported without first asking whether Life Patterns' person-level target was actually an externally observable class rather than a participant-adjudicated idiographic self-model.

This is the principal conceptual fork.

## The specific reasoning errors

### A. Stable shared representation was conflated with fixed taxonomy

The model tournament needs the same frozen evidence substrate for all competing models. That requires stable semantics and provenance. It does **not** require every useful behavior to be forced into a closed categorical ontology.

### B. Measurement was equated with external-rater classification

Once the bridge was called a “measurement instrument,” conventional reliability logic took over: define categories, train independent coders, measure agreement, freeze aggregation. That is appropriate when the target fact is external classification. It is not sufficient for a question such as “is this actually a recurring pattern in your life?”, where the participant supplies essential information unavailable in selected episodes.

### C. Episode evidence and person-level pattern authority were collapsed

Episode facts can often be coded externally: a choice was delayed; the narrator said it seemed too difficult; the course was later rejected. But recurrence, typicality, scope and exceptions are partly participant knowledge. The architecture instead made the person-level pattern a derived aggregate over coded episodes.

### D. Anti-leakage safeguards expanded into unnecessary anti-participant authority

The real danger is target-model information feeding backward into neutral evidence. Participant recursive correction is not target-theory leakage. The design protected against model contamination by unnecessarily displacing the participant from the central adjudication role.

### E. Validation infrastructure began dictating product semantics

The schema became optimized for coder agreement, machine graph validity and future model scoring. Human UI then became a way to fill the graph. Owner review exposed the inversion: obvious positive behavior could be hard to record because the graph's named value required a stronger absence claim.

### F. Local repairs compounded the premise instead of retesting it

Overlap, absence, cardinality, stage, containment and provenance audits were often correct **conditional on the ontology premise**. Each discovered ambiguity led to more facets, gates, components and graph rules. There was no architectural stop condition saying: if ordinary positive behavior requires increasing machinery or falls into `insufficient`, reconsider the abstraction itself.

### G. A neighboring research paradigm was over-applied

The repository already contained AstroHD/Survey-style psychometric and validation machinery. That encouraged a standardized-instrument solution. Life Patterns is different: its product target is an idiographic, participant-recognized pattern model that can later be frozen for theory-blind comparison. Methods appropriate to population questionnaires and annotation benchmarks should support that goal, not replace it.

## Responsibility / attribution

The canonical evidence shows that the owner wanted a theory-blind empirical comparison and participant-useful Life Patterns product. It does **not** show an owner requirement for a comprehensive fixed behavioral codebook or for external coders to determine person-level recurring patterns.

Because the original chat is partially missing, exact conversational attribution cannot be proven. The best-supported conclusion is that the assistant/Codex methodological workstream introduced the fixed-ontology/external-coder solution as a way to solve the legitimate bridge problem, and the project then path-dependently optimized it.

## What remains valid

Retain:

- chart/model blindness before the neutral freeze;
- participant review/correction of extracted episode facts;
- exact source provenance and immutable/content-addressed freezes;
- no post-hoc recoding after target-model results;
- thin predeclared model adapters;
- missingness distinct from negative evidence;
- strict awareness/opportunity/reasonable-feasibility/nonoccurrence gates for genuine absence claims;
- theory-blind independent review of substantive measurement changes;
- explicit uncertainty, counterexamples and participant edits.

The V1/V2/V5 artifacts remain valuable development history and contain reusable mechanics. They are not erased.

## What should be superseded as the primary architecture

- a fixed 22-observable taxonomy as the mandatory semantic representation of all useful episode evidence;
- externally coded episode labels as the authority from which person-level patterns are mechanically aggregated;
- inter-rater categorical agreement as the main success criterion for the final Life Pattern;
- UI designed primarily to populate the V5 graph;
- treating elicited confirming examples as independent recurrence evidence;
- expanding schema complexity whenever a narrative fails to fit a value.

## Replacement architecture

Use the participant co-coding design in `docs/research/LIFE_PATTERNS_PARTICIPANT_CO_CODING_ARCHITECTURE_2026-09-11.md`:

`episode -> minimal factual decomposition -> candidate recurring-pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised candidate -> participant adjudication -> accepted/rejected/unresolved pattern`

Episode structure should be only as elaborate as needed to preserve facts and generate useful next questions. A compact extensible vocabulary may still help with timing, action state, resolution, explicitly reported appraisal/reason, context and genuine absence claims. It is an indexing/question-generation aid, not the final personality truth.

## Corrective invariants to prevent recurrence

1. **Neutrality does not imply taxonomy.** Every new fixed category must justify why an open factual representation plus participant adjudication is insufficient.
2. **Participant-level recurrence requires participant adjudication.** External coding may propose; it does not silently finalize typicality.
3. **Separate epistemic layers.** What happened, what the narrator explicitly believed/perceived, what GPT hypothesizes, and what the participant endorses are different records.
4. **Absence gates apply only to absence claims.** Failure of a stronger absence/counterfactual claim must never erase separately supported positive facts.
5. **Elicited examples are nuance evidence, not an unbiased frequency sample.** Their failure to materialize is a discrepancy to probe, not an automatic trait label.
6. **Complexity is a diagnostic.** If common intelligible behavior repeatedly requires OS/abstention or graph expansion, revisit the abstraction before adding more schema.
7. **Every research mechanism must name the downstream decision it improves.** If a field/category has no clear role in better participant questioning, faithful pattern adjudication, or predeclared model comparison, it should not automatically enter the primary instrument.
8. **Validation machinery may not dictate participant-facing semantics.** The scientific record should adapt to faithful evidence, not force evidence into a convenient scoring structure.
9. **Preserve open-world gap discovery.** Unknown but clear positive behavior must remain representable and usable for later blind refinement.
10. **Recheck the north star at every semantic expansion.** The product is “Discover Your Unique Life Patterns,” not “complete a behavioral ontology.”

## Required next step

Do not continue V5 owner acceptance or human collection. The next semantic repair must be performed in a fresh target-theory-blind context and must use this audit only as a methodological constraint, not target-model information. It should specify the minimal episode-fact representation, recursive participant co-coding protocol, gap-discovery mechanism, calibration targets and frozen participant-adjudicated pattern record. A separate fresh blind review must pass before implementation.
