# 02 — Scoring and Model Policy

## Existing scoring system is the starting point

Use the existing V4/V3.2 model in `reference/core/` as the canonical symbolic decoder.

Do NOT generate a second independent questionnaire/scoring theory for synthetic cases.

Normative files:
- `human_design_reverse_matching_protocol_v4_1.md`
- `human_design_search_instructions_fixed_candidate_blind(6).md`
- `v3_2_scoring_delta.md`
- `question_bank_v1.json`
- `profile_schema_v1.json`
- `hd_global_search_results.json` as legacy-run evidence only, not a universal mapping source.

## Symbolic tier

Until human calibration exists, implement the V4 symbolic quantities:

```text
raw_bits_j = -log2(prevalence_j)
info_bits_j = min(6, raw_bits_j)

evidence_bits_i =
    effective_confidence_i
    * support_i
    * info_bits_primary_anchor

contradiction_bits_i =
    effective_confidence_i
    * contradiction_severity_i
    * 4

NetInformation =
    sum(evidence_bits_i)
    - sum(contradiction_bits_i)
```

Call these `rubric_bits`, never probability bits.

Rank according to the protocol's declared ordering and report all tie-breaks.

## Effective confidence

Keep separate:
- behavioral confidence: how strongly the behavior is established;
- measurement reliability: how reliably this person can report that domain now.

`effective_confidence = behavioral_confidence * measurement_reliability`

Reliability can only remove/downweight evidence. It cannot create chart support.

## Dependencies

One underlying chart structure must not receive full information credit repeatedly because several questions paraphrase it.

Represent dependency clusters explicitly.

Alternative pathways compete; they are not summed as independent evidence.

## V3.2 corrections

Encode these as updated constructs:
- distinctive original contribution: high-confidence;
- institutional participation does not imply identification/conformist influence;
- expertise can be incidental to curiosity rather than a mastery motive;
- material/resource competence is separate from status/hierarchical advancement.

Do not use the old “mastery” or “material advancement” observations as positive evidence unless a future human-development model empirically re-establishes them.

## Mapping compilation task

The current question bank is intentionally candidate-blind and does not contain the server-side HD mapping keys.

Codex must produce a machine-readable `mapping_library_v1.json` by formalizing ONLY mappings already supported by the existing protocol/source set.

For every mapping store:
- observation_id
- dependency_cluster
- question_ids
- chart_feature predicate
- predicted response distribution or symbolic support rule
- structural salience
- mapping directness
- contradiction rule
- source/rationale
- status: frozen | unresolved | empirical_only

If the repository does not contain enough information for a mapping, mark it `unresolved`.
Do not invent one merely to improve recoverability.

## Empirical tier

When human development data becomes available, fit:

```text
LLR_i(c) = log2( P(answer_i | chart_features_c) /
                 P(answer_i | reference_universe) )

EmpiricalScore(c) =
    sum effective_confidence_i * LLR_i(c)
```

Prefer regularized/hierarchical estimates, not raw rare-cell frequencies.

Human-learned mappings are versioned separately from theory-derived mappings.
