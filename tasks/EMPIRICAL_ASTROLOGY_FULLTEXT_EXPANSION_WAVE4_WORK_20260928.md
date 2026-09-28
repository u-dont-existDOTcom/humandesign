# Empirical Astrology — Full-Text Expansion + Wave 3B/4 Work Continuation

Date: 2026-09-28

## Role boundary

This task is for a Work/execution chat.

It may:
- retrieve and archive lawful full texts;
- extract methods/results/statistics;
- update evidence registries;
- identify bibliographic/dataset identity;
- implement already-frozen model decisions;
- run deterministic development evaluations and ablations;
- prepare evidence packets for Pro.

It must NOT make substantive scientific/model-design judgments where reasonable experts could differ.

Do not use Deep Research.

## Starting state

The prior execution and Pro work is already published.

Canonical branches/commits:
- End-to-end evidence branch: `worker/empirical-astrology-end-to-end`
  - commit: `c4d98d0ad18f2b0d3ec0064d360af5b0b0f05da6`
- Wave 3 mechanical handoff branch: `worker/empirical-astrology-overnight-execution`
  - commit: `7e18f6b84fb923d7d99ba85a3f9ed23cfdc78013`
- Frozen Wave 3 Pro decision branch: `worker/empirical-astrology-pro-decisions`
  - commit: `ccdeaa9d563e243bfce2349b10d6c932e7f3bc57`

The frozen Pro decision must remain intact as a historical checkpoint. Do not rewrite it.

Current evidence limitations from the completed end-to-end report:
- 1,248 normalized feature records
- 913 canonical source documents
- 965 conservative dataset/cohort units
- 14 original/fullest texts deeply read
- 49 primary feature extraction rows
- 502 A-priority sources
- 489 A-priority full texts still missing

Because the original-source layer is incomplete, the next task is to expand full-text coverage before treating the Wave 3 decision as the final literature-informed architecture.

## Branch

Create/use:

`worker/empirical-astrology-fulltext-wave4-execution`

Base it from the frozen Wave 3 Pro decision commit:
`ccdeaa9d563e243bfce2349b10d6c932e7f3bc57`

If current `main` contains unrelated repository-management fixes, merge/rebase only if necessary for execution and do not alter any scientific artifact from the frozen decision.

## Phase A — Aggressive lawful full-text recovery

### Preferred access order

Use every lawful access tool available in the Work environment, including **InfoAccess MCP** if present.

For each A-priority source, search in this order:

1. InfoAccess MCP / connected library-resource resolver, if available.
2. Existing repository/Project/Library files.
3. DOI resolution and publisher page.
4. Institutional repositories / author manuscripts.
5. Europe PMC / PubMed Central where applicable.
6. Crossref/Unpaywall/open-location routes.
7. Journal/archive websites.
8. Thesis/dissertation repositories.
9. Google Books / Internet Archive / other lawful archival previews or scans where full text is legally accessible.
10. Author-hosted copies.

Do not bypass authentication or access controls.
Do not use pirated repositories.
Do not purchase individual articles automatically.

### Special handling: Correlation archive

Many important empirical astrology papers are in `Correlation`.

Use InfoAccess/library access first.

If, after exhausting all lawful connected routes, a substantial block of A-priority `Correlation` papers remains inaccessible, create:
- `notes/empirical_astrology/fulltexts/CORRELATION_ACCESS_GAP.md`

This file must list:
- exact missing articles;
- issue/year;
- why each matters;
- whether it is A or B priority;
- how many unique high-value papers would be unlocked by archive access.

Then stop only the purchase-dependent retrieval branch and continue all other work.

Do NOT ask the owner to buy a subscription unless this gap file shows meaningful information gain. The owner has indicated willingness to pay for an inexpensive archive subscription if it unlocks a substantial set of high-value papers.

### Retrieval target

Do not mechanically insist on all 489 A-priority sources.

Prioritize by expected decision impact:
1. sources directly relevant to CF-001 through CF-008;
2. major replications/reanalyses of those candidate families;
3. major negative studies that constrain those families;
4. sources needed to reconstruct exact executable rules;
5. sources needed to resolve dataset independence;
6. only then lower-information A sources.

Aim to maximize **decision-changing information per retrieved paper**.

## Phase B — Update primary-source evidence layer

Do not edit prior historical extraction files destructively.

Create new versioned outputs:
- `data/empirical_astrology/fulltexts_v2/fulltext_manifest.jsonl`
- `data/empirical_astrology/fulltexts_v2/primary_feature_extractions.jsonl`
- `data/empirical_astrology/master_v2/source_registry.jsonl`
- `data/empirical_astrology/master_v2/dataset_registry.jsonl`
- `data/empirical_astrology/master_v2/candidate_feature_registry.jsonl`
- `data/empirical_astrology/master_v2/negative_constraint_registry.jsonl`
- `notes/empirical_astrology/master_v2/evidence_map.md`
- `notes/empirical_astrology/master_v2/FULLTEXT_EXPANSION_REPORT.md`

For every newly read original:
- canonical source_document_id;
- DOI/citation;
- actual full-text access route;
- exact pages/sections read;
- source hash/provenance if available;
- exact sample;
- birth-data quality;
- exact feature calculation;
- all tested outcomes, not just significant ones;
- exact statistics;
- multiplicity;
- control construction;
- discovery vs confirmatory status;
- dataset lineage;
- relationship to existing candidate family;
- whether the new evidence strengthens, weakens, or merely specifies the family, **descriptively only**.

Do not make the final scientific adjudication yourself.

## Phase C — New Pro handoff before implementation

Because this expanded primary evidence may change the Wave 3 decision, prepare:

- `reference/empirical_astrology/pro_reasoning_packet_wave3b.json`
- `notes/empirical_astrology/master_v2/PRO_HANDOFF_WAVE3B.md`

The handoff must compare:
- frozen Wave 3 decision at `ccdeaa9...`;
- evidence available at that decision;
- all newly recovered originals;
- exact candidate-family changes;
- exact unresolved decisions.

For each CF-001 through CF-008, state:
- newly recovered sources;
- whether exact definitions are now reconstructable;
- whether apparent independent replications are truly independent;
- whether effect estimates changed;
- whether multiplicity/control concerns changed;
- whether any candidate now plausibly clears the prior exclusion/exploratory gate.

### HARD STOP FOR SCIENTIFIC JUDGMENT

At this point, if new evidence could plausibly change feature inclusion, weighting, interaction structure, or the prospective protocol, STOP and hand off to Pro.

Do not implement a changed model yourself.

If the expanded evidence clearly does not alter any substantive decision, still produce the Pro handoff; Pro must confirm that.

## Phase D — Wave 3B implementation after updated Pro decision

Only after a Pro chat commits an updated or reaffirmed frozen decision artifact, continue.

Expected Pro artifacts:
- `reference/empirical_astrology/literature_model_v1b_decision.json`
- `notes/empirical_astrology/master_v2/PRO_DECISION_WAVE3B.md`

Implement exactly that decision into:
- `reference/empirical_astrology/literature_feature_registry_v1.json`
- `reference/empirical_astrology/literature_model_v1.json`
- `docs/empirical_astrology/01_literature_model_v1.md`
- `src/hdmatch/empirical_astrology/`
- `tests/empirical_astrology/`

Do not improve or reinterpret the Pro decision.

## Phase E — Wave 4 mechanical development evaluation

Run only DEVELOPMENT evaluations.

Required comparisons where data permit:
- frozen full model;
- theory-neutral birth-time-distance model;
- feature-family ablations;
- date-only baseline;
- time-only baseline;
- location/site baseline;
- season/cohort controls;
- random-feature/null controls;
- negative-control analyses;
- leakage/control-generator checks.

Use historical literature data, previously inspected owner cases, and development cohorts only.
Never call these prospective validation.

Create:
- `experiments/empirical_astrology/wave4/`
- `data/empirical_astrology/master_v2/wave4_results.jsonl`
- `notes/empirical_astrology/master_v2/WAVE4_DEVELOPMENT_RESULTS.md`
- `notes/empirical_astrology/master_v2/PRO_HANDOFF_WAVE4.md`

The Wave 4 handoff must explicitly cover:
- robustness;
- ablations;
- null baselines;
- leakage;
- cohort structure;
- multiplicity;
- reused datasets;
- effect sizes;
- which results were impossible to evaluate because required data were unavailable.

Do not modify the model after seeing Wave 4 outcomes.

## Completion criterion

The Work task is complete when:
1. high-value full-text retrieval has been exhausted through available lawful sources;
2. the expanded evidence package exists;
3. the updated Wave 3B Pro decision has been implemented;
4. Wave 4 development evaluation has been run;
5. `PRO_HANDOFF_WAVE4.md` is ready for Pro.

If a Pro decision is required mid-run and the Work system can send a Pro request itself, do so using the prepared packet and then continue only after the frozen Pro artifact exists.

If it cannot, stop at the exact Pro gate and report what the owner should send.

Save all work in the humandesign repository.
