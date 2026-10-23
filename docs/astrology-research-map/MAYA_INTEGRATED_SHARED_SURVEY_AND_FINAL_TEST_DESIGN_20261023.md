# Integrating Maya research into the shared cross-tradition survey

**23 October 2026 — owner decision implemented as a research integration.** **Do not run a separate Maya participant study now.** Instead incorporate source-specific Maya claims and uncertainties into the existing evidence map and reuse the same Life Patterns / Human Design respondent instrument whenever the whole multi-tradition framework is ready for its final prospective study. **Nothing in this batch deploys or modifies the live Life Patterns app, frozen HD V4.3 engine, current participant data, or personal answer histories.**

## 1. What the existing surveys already provide

Actual anchored survey-bank sources, recovered from the **pre-existing** `humandesign` branches rather than recreated:

| Existing instrument | Source and state | Question inventory | What Maya can reuse |
|---|---|---:|---|
| **Life Patterns V3 opt-in research candidate** | Existing 2026-10-21 `research/life-patterns-external-design-merge` branch, exact commit `7971b3c1564d9c38bce17abe4c4575affcba2c76`; development-only/not live or scored | **23** existing optional topics, **7** conditional probes; at most **5** base optional topics and **2** new conditional followups per session, skip/decline allowed | Existing topic identifiers **ART**, **VOCATION**, **LEARNING_HISTORY**, **TRAVEL**, **RECIPROCITY**, plus **BONDS**, **ANGER_REPAIR**, **BELIEF**. Directness varies. |
| **Life Patterns tendency-first** | Existing source-registry snapshot, not asserted live in this turn | **25** items | `TF1-G01` may partly describe how a person approaches messy information, not evidence of historical "No'j wisdom" or a natal result. |
| **Life Patterns experience-meaning** | Source status: separate optional, unscored | **8** items | Mostly **not** direct behavioral measures of proposed Maya birth traits; do not count meaning or mystical experience as their confirmation. |
| **Human Design V2 questionnaire bank** | Existing frozen/reference HD-specific source | **81** items | No Maya rules enter HD V4.3. Any genuinely overlapping observable belongs in a separate cross-tradition measurement mapping, not a cloned V4.3 score. |

A [complete **offline V3 shared-survey candidate**](MAYA_SHARED_LIFE_PATTERNS_V3_FINAL_STAGE_CANDIDATE_V1.json) is now generated from the original **23 question objects and seven conditional microprobes preserved verbatim at the question-object content level**, with the **single possible neutral craft detail clarification held outside the existing question arrays**. It has *not* been deployed or frozen; [its builder](build_maya_v3_shared_research_candidate.py) requires the exact source commit and refuses changed question hashes, and [tests](test_maya_shared_v3_full_preservation.py) verify offline that the original 30 question/probe objects have been preserved unchanged. That makes it a usable candidate for a later unified survey rather than a second Maya-specific questionnaire.

The full provenance hashes, IDs, exact source question text for the selected optional bank items, and **no private answers**, are retained in [the small source-controlled survey inventory](MAYA_SHARED_SURVEY_EXISTING_INSTRUMENT_SNAPSHOT_V1.json). Its builder, [`build_maya_shared_survey_snapshot.py`](build_maya_shared_survey_snapshot.py), reads the existing *pinned historical Git commit*. Later survey updates need an explicit new baseline version and a coverage reconciliation; do not silently pretend these 2026-10-21 prompts are still live or frozen. The personal survey master already merged from multiple owner sources **stays entirely private and development-only**. No prior personal interview answer is read by the Maya integration and none can become an untouched prospective evaluation just because a different tradition now consumes the same construct.

## 2. Full Maya source identity is present, not collapsed into one horoscope

The [combined source day-name inventory](MAYA_COMBINED_SOURCE_DAYNAME_SURVEY_INDEX_V1.json) brings together:

- **20/20 colonial Yucatec named birth days** from Bolles's *U Mutil Uinic Zanzamal*, with literary ancestry (Kaua, Chan Cah and Pérez), page, status, and explicitly quarantined stigmatizing predictions.
- **20/20 Highland K'iche' day-name pairs**, preserving **Momostenango (Tedlock)** and **Zunil (Komon Tohil)** as separate, sometimes conflicting historical/community source testimonies, not 40 corroborations of identical traits.
- **Maya codices/Dresden/Madrid astronomy and ritual almanacs** as **NOT AUTOMATIC NATAL CLAIMS**; their calendar/event/electional hypotheses would use a suitable event-time analysis, not forced into a personality questionnaire.
- **Modern Dreamspell** as a separate later system, never misattributed to a Classical Maya manuscript or community practice.

The 20 correspondences between Yucatec/K'iche' names are **linguistic day-sequence crosswalks**, not proof of common natal meanings or time standards. `CHUWEN` (Yucatec) translates to K'iche' `B’ATZ’` linguistically; it is not automatically Tedlock's or Zunil's B'atz' personal prediction. Yucatec `KAB’AN` corresponds to K'iche' `NO’J`, where Momostenango and Zunil source claims **differ**. All 1–13 day-number modifiers and 1722 5×52 almanac interpretations remain source-specific; no synthetic universal 260-trait horoscope was generated.

## 3. Claims mapped to existing behavioral evidence, with honest gaps

The [compiled cross-tradition bridge](MAYA_SHARED_SURVEY_COMPILED_NONDEPLOYED_PLAN_V1.json), generated by [`compile_maya_shared_survey_bridge.py`](compile_maya_shared_survey_bridge.py) from the [source and survey mapping](MAYA_SHARED_CROSS_TRADITION_SURVEY_INTEGRATION_V1.json), connects **11 source-specific provisional claims to 8 common behavioral constructs and 9 already-existing question IDs**. The key mappings are:

| Different source-native prediction | Existing shared topic(s) | What those topics actually show |
|---|---|---|
| Colonial Yucatec **Chuen** carpenter/weaver/maker | **VOCATION**, **LEARNING_HISTORY**, **ART** | Work history, skills learned, broad creative production. **All partial proxies**, because the source's specific skilled physical-making role may not be elicited unambiguously. |
| Colonial Yucatec **Men** or **Caban** craft descriptions | **The same three topics** | **Reuse the same answers**; their craft wording is narrower/less stable across manuscript witnesses, and no separate duplicated craft survey is permitted. |
| Momostenango **No'j** creative/problem-solving thinking | **ART**, `TF1-G01` | Broad making and self-described handling of confusion; **not a direct independent creativity test**. |
| Zunil **No'j** prudence vs Zunil **Imox** creativity | `TF1-G01` (weak), **ART** (broad) | Separate community claims; **no historical agreement** on a pooled "Noj creativity" phenotype. |
| Zunil **E/Eb'** travel and generosity | **TRAVEL**, **RECIPROCITY** | Actual journeys vs desired travel and reported help, adjusted for opportunity. Not proven day-sign propensity. |
| Momostenango **E** ritual role; Zunil **Toj** mediation; Zunil **B'atz'** teaching | **VOCATION/BELIEF**, **BONDS/ANGER_REPAIR**, **LEARNING_HISTORY/VOCATION** | Only broad historical or role proxies; do not invent direct measures or recruit participants for a weak, culturally mismatched prediction. |

No statement about historical illness, criminality, sexuality, fate, religious punishment or moral worth becomes a modern person-level prediction or an interview prompt. The [20 named Yucatec source rows](MAYA_COMBINED_SOURCE_DAYNAME_SURVEY_INDEX_V1.json) retain the **15 quarantined** historical domain rows but show **zero scored features** for them.

### Only one *possible* additional question, and not now

The existing V3 bank is already fairly broad; a new independent Maya interview would add respondent burden and risk recycling the same claims. The overlay therefore declares at most **one future optional, neutral skilled-making clarification**, which would only be selected **if the existing ART/VOCATION/LEARNING_HISTORY evidence does not adequately cover skilled physical making**. It must be offered to *all eligible respondents with the same missing-domain state*, independent of chart signs, and only by a finalized consented instrument. An answer already available should be reused **once** without making the person answer another differently worded version merely to manufacture another supporting datum.

This proposed question is **not added to V3's actual 23-topic source**, not live, not requested of the owner, not scored, not a standalone Maya test, and not a new required prerequisite for other traditions.

## 4. What “test everything together at the end” means scientifically

**Yes: one common participant recruitment and interview pass for those *natal constructs* that are genuinely measurable in one session.** The proper scoring architecture is still **tradition-specific**, not an "everything predicted you" total manufactured from overlapping rules:

1. **Before any scored respondent:** finish each tradition's own source, birth calculation, observation, and allowable ambiguity decisions; record which claims are ethical/natal/testable and which remain source-only. Maintain a master *behavioral construct-to-question* ledger so **one actual occupational or creative answer is only one observation** regardless of how many charts reuse it. Historical calendar/method variants cannot be picked based on a matching personality.
2. **Single participant input:** separate private consented birth information from the common behavioral questionnaire. A source-agnostic topic/item selection policy must be frozen **before answers**; any adaptive clarifying question must follow recorded, chart-independent evidence-coverage triggers and the existing cap/skip rules. Prior owner/development responses support *wording design*, not the untouched validation denominator.
3. **Sealed, source-specific predictors:** for eligible natal systems—Human Design, Western, Jyotish, Chinese, Tibetan, and Maya—their algorithms and chart features, hypotheses, expected answer directions, statistical units and decoys must be independently documented and frozen. A modern GMT584283 Yucatec date-only Chuen test is an explicitly named **historical reconstruction**, not proof of local living birth-clock continuity. Unresolved community-specific calendar rules stay UNKNOWN/ABSTAIN.
4. **One answer set, several independent model evaluations:** score the same frozen answers against each eligible tradition's *predeclared* predictions and source-grounded nulls and baseline nonastrological predictors. Do **not** treat multiple traditions predicting the same creativity/craft/travel answer as separate successful behavioral observations; report dependence and correction for within- and across-family multiplicity (or a predeclared hierarchical test). Negative rules and no-prediction source-only states must be retained.
5. **Separate instruments for genuinely different targets:** family/partner dynamics need pair consent and independent relationship forecasts; future event timing needs predated event windows/outcomes; Horary, historical codex eclipse tables and electional auspices are **not** validated by asking a contemporary person whether they feel creative.

This is consistent with the existing [Human Design forward-blind trial specification](../../docs/20_forward_blind_prospective_validation.md) and the independent [cross-tradition source-to-test methodology](WORKFLOW.mmd) plus [focused shared-survey dataflow diagram](SHARED_SURVEY_INTEGRATION.mmd). Nothing silently relaxes HD's exact V4.3 scoring/ephemeris or response-freeze rules.

## 5. What this integration did and did not complete

**Implemented and reproducible on this branch:** version-pinned inventory of existing shared questions, a complete 20+20 Maya source identity index, 11 historical claim bindings into 8 common observables, an executable metadata-only adapter, one candidate future gap probe and a linked canonical source-to-test workflow. No actual prior respondent sources were touched.

**Not performed by design and by owner preference:** recruitment, a dedicated Maya experiment, editing the live Railway interview, adding automatic ART/VOCATION questions, freezing/retuning natal traits, privately calculating people's birth signs, pulling earlier user questionnaire answers into this public repository, updating the HD scorer, or claiming empirical effects. A final shared survey is **not yet frozen**, the V3 optional candidate is **not deployed**, and neither 16 traditions nor 20/20 source names mean 16/20 successful human tests.

**Current evidence boundary:** historical and living-source integration **DONE as source-level framework work**; confirmatory human predictive validity **OPEN** and intentionally deferred until the shared cross-tradition protocol is ready.
