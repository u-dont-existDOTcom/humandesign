# Deep astrology analysis V2: source-compiled, coverage-checked, outcome-aware

**Status:** Current procedural revision for research use. V1 and all historical prediction/model freezes remain historical records. This revision does not alter their calculations, rerank their outcomes, activate a clinical/forensic predictor, or certify astrology's predictive validity.

## 1. What V1 got right—and what it did not establish

V1 correctly made prior-work retrieval, systematic chart examination, contradictory evidence, uncertainty, and source boundaries explicit. Its twenty passes remain a useful coverage map. But recording `DONE` is not the same as executing a calculation or interpreting its result correctly.

A synthetic probe against the actual V1 validator marked every unconditional pass `UNAVAILABLE`, supplied a nonexistent support reference for a fictitious claim, and still received exit code 0 and `valid: true`. The probe contains no participant data. This exposes a specific integrity defect, not a defect in astrology itself. Other gaps include receipt-controlled applicability, silently collapsed duplicate IDs, unverified references, and confusion between evidence provenance and scientific validation.

V2 separates five questions:

1. **Was the declared work accounted for?** Every expected method, rule and source unit has a disposition.
2. **Was it executed?** The required calculations and rule evaluations exist and match the predeclared scope.
3. **Was it interpreted faithfully?** Claims follow the source's actual conditional logic, exceptions and scope.
4. **Was the comparison informative?** Predictions discriminate outcomes or people, not merely describe something generally applicable.
5. **Was it independently tested?** Development success, held-out transfer and prospective evidence remain distinct.

A script can verify parts of the first two and references supporting the third. It cannot certify all five. A download, a passing unit test, a second-model agreement, and an attractive reading answer different questions.

## 2. Define a finite corpus, not “all astrology”

The research universe is a versioned set of **works, editions, books/chapters, and technique families**. “All rules in this declared corpus have been screened” is a defensible target. “Every possible astrological explanation has been exhausted” is not a useful completion criterion.

For each work, preserve author, translator/editor, edition, publication date, language, completeness, access provenance, file digest, print-page/PDF-page correspondence, and any known errata. A modern translation has a separate provenance from the ancient original. An annotated derivative and its parent are not independent sources.

Screen the entire table of contents and every in-scope section. Each section becomes one of: rule extracted, prerequisite/definition, example, qualification/exception, commentary, out of declared scope, illegible/missing, or unresolved. Do not search only for already-favored planetary combinations. The source audit must discover rules that weaken, reverse, limit, or contradict the attractive ones.

Examples are calculation checks and demonstrations of the author's practice. They are not untouched validation data for a rule inferred from those same examples.

**Source-completeness labels:**

- `CORPUS_INDEXED`: all intended units are listed; unread units may remain.
- `SOURCE_SCREENED_WITH_GAPS`: each unit is accounted for, with explicit gaps.
- `DECLARED_SOURCE_SCOPE_AUDITED`: every in-scope readable unit has been examined, disputed passages retained, no unreported missing sections.
- `DECLARED_PROFILE_EXECUTED`: a case ran every required executable module for its predeclared profile.
- `SCOPED_WITH_GAPS`: an honest result when required modules, inputs or evidence remain unavailable.

None means empirical validation. A library inventory of 538 paths is discovery coverage, not 538 verified methods.

## 3. Make the rule, not the paragraph, the reusable unit

Extract a **RuleSpec** with stable ID and these separate components:

- source locator and exact supporting passage boundary;
- genre and scope: natal, horary, electional, mundane, annual timing, or a declared modern extension;
- vocabulary definitions and original frame;
- prerequisites and applicability conditions;
- antecedent logic (`all`, `any`, numerical comparison, order, direction);
- modifiers, exceptions, mitigating and reversing conditions;
- calculation settings, thresholds and equality conventions;
- output: astronomical fact, source-symbolic testimony, proposed behavioral bridge, or fitted empirical prediction;
- dependence on other rules and shared geometric facts;
- interpretation directions and any author-supplied synthesis/priority rule;
- executable status, tests, and unresolved alternatives.

Do not convert a source's **conditional** testimony into an unconditional trait. Do not convert a rule about capacity into preference, motivation into observable success, planetary strength into benevolence, or a house signification into a personality description. Preserve distinctions between the native, a parent, a partner, the quality of a relationship, and its occurrence/date.

The engine should retain source-defined interactions. A conjunction of ingredients can be predictive even if each ingredient has little marginal predictive value. Therefore V2 does not require every component to work alone before an authorized combination is tested. It does require that the combination, its provenance and its selection history be explicit.

**Genre firewall:** a horary perfection or judgement rule is not silently a natal-life rule. An adaptation may be researched as a named development hypothesis. Lilly's introductory and horary books are not substitutes for his third book on nativities. Likewise, Tājika annual astrology is not interchangeable with Parāśari natal/dasha practice.

## 4. Compile a case plan before seeing outcomes

First recover the live person-life index and catalog, including retained failures and newer supersession. Inspect every retained family for relevance; this is not a demand to apply every method to every question.

Prepare a compact task contract containing:

- the actual question and intended target: profile, capability, experienced theme, external event, relationship quality, event occurrence, or date localization;
- which inputs are known, their quality and permissible uses;
- mode: descriptive, development, retrospective-blind, or prospective;
- source/model versions, admitted interpretation variants and the evidence available at selection time;
- active modules, required checks and exact expected rule IDs;
- allowed timing horizon, event resolution, comparator/risk set and scoring rule where applicable;
- output scope and what will remain unresolved.

Bind the plan to the current protocol, catalog and input-manifest hashes. Applicability comes from this plan, not from booleans that an answer writer can switch off in its receipt.

Use dependency closure: a name-comparison question need not rerun an unchanged natal chart, while a deep natal reading must not quietly omit the geometry or ruler conditions. Reuse verified calculations when their input, engine and convention hashes are unchanged. New catalog entries require a relevance check, not automatic expensive recomputation.

Frozen parameter variants are legitimate comparisons. Choosing among house systems, orbs, translations, significators or windows because one fits the person's known life is **development selection**, even when the selected rule is historically authentic.

## 5. Strengthen the information boundary

“Did not deliberately search for outcomes” is weaker than “outcomes were unavailable to the interpreting worker.” A current prompt may already include memories, summaries, identifying biographical clues or prior results. Record actual exposure; do not declare a familiar person an untouched test by asking the same context to forget.

For a genuinely blind first pass, separate the calculator, interpreter and outcome evaluator. The calculator receives necessary names/birth records, the interpreter receives a source-bound feature packet without unnecessary identity/history, and the evaluator opens outcomes only after the prediction commitment. Record unavoidable identity recognition as a limitation. A fresh prompt by itself does not prove blinding.

For development, known history may be used openly. Preserve an unchanged benchmark and create a new version for every material rule/synthesis change. Do not pretend that this prohibition on relabeling old results prohibits new learning.

No clinical, forensic, or mortality assurance is produced from symbolic features. Historically medical or longevity chapters remain visible in source coverage, with an explicit research-only/non-admitted disposition for practical person-level forecasting.

## 6. Build the factual chart before choosing a story

The base ledger should include positions, velocities, relevant coordinates, calendar/time conventions, requested and returned ephemeris modes, and data-file hashes. Birth-time uncertainty is propagated, not replaced with an invented confidence interval.

For each admitted geometry family enumerate its full expected universe. For example, an unordered pair universe for n admitted bodies has n(n−1)/2 pairs; angle/body pairs have their own explicit list. Generate both sides of non-conjunction aspect geometry, handle 0°/360° wrap, and test sign/house boundaries. Preserve `ACTIVE`, `INACTIVE`, and `UNRESOLVED` separately. Not finding an aspect is not evidence of an opposite trait.

Do not hard-code one universal tight orb and call it all traditional astrology. Whole-sign configurations, source-defined moieties, exact degree contacts, applying/separating status, stations, solar visibility and declination contacts are distinct possible modules. Admit only the variants justified by the declared source or explicitly labelled development convention. Unimplemented does not mean false.

Source meaning matters in the calculations: “house” may mean domicile in one passage and a mundane house in another; solar phases, sect for Mercury, directional strength, nodal choice, sign-based versus degree-based relations, and divisions of signs must not be approximated without labels. A coarse condition such as being in a directional-strength house is not automatically an exact full strength calculation.

For historic examples verify Julian/Gregorian calendar, noon/midnight conventions, local mean versus civil time, sexagesimal fractions, latitude, and translator corrections before comparing ephemerides. A modern accurate sky cannot repair an incorrectly transcribed ancient time.

## 7. Evaluate source-native structure before modern translation

Traverse the V1 coverage map without dropping its protections: authority; exposure boundary; input provenance; uncertainty; astronomy; full geometry; Lilly; Hellenistic; Jyotish; rulers/dispositors; the admitted rule vector; contradictions/dependencies; topic-specific rules; timing state; triggers; experimental candidates; cross-system comparison; completeness; synthesis.

Improve the content of those passes:

**Whole-chart organization.** Inspect luminaries, chart/Ascendant ruler, relevant house rulers and dispositors, distributions/concentrations, source-defined chart leadership and topical significators. Do not equate the numerically strongest planet with a complete generic personality model. CF-003 retains its own prerequisites and unresolved factor-extraction boundary.

**Conditions and modifications.** Dignity, capacity to act, visibility, sect, angularity, reception and harmful/helpful configurations are not one axis. A strong planet can be difficult; a weak significator can be helped. Record the ordered explanation and exceptions rather than adding favorable keywords until they dominate.

**Source disagreement.** Differences between authors or reference frames stay visible as separately testable branches. A modern interpreter may synthesize them, but must distinguish source-native judgement from that new synthesis. A source-based approach is not an instruction to average every testimony equally.

**Dependency accounting.** Keep both semantic roles and physical origins. The same geometric contact can matter for several topics; that need not be erased. But it is one underlying observation, not three statistically independent votes because three texts describe it. Record raw and dependency-adjusted outputs when the research contract requests both. Novel fitted interactions remain possible; do not suppress them by requiring independent component success.

## 8. Timing: separate four tasks and correct a misleading shortcut

Distinguish:

1. background chapter/state;
2. topical relevance or event class;
3. activation/trigger window;
4. a particular date within that window.

Finding a family-stress day does not identify whose medical event occurred. Locating the right year does not identify the day. An exact-day criterion cannot borrow a broad-window success without a separate, frozen refinement rule.

A run must preserve a full candidate timeline, competing peaks, ties, gate-positive exposure, event-date uncertainty, and the distinction between known non-events and unknown background. If the year was supplied, report conditional within-year localization—not lifetime discovery. If only a month is documented, do not score an exact day as verified.

**Forecast-time information is the governing leakage boundary.** Future astronomical positions can be calculated before a forecast is issued. Therefore a centered window containing a later ephemeris contact is not automatically look-ahead leakage. It may be valid in a model fixed before the target event. A future biography label, post-event choice of window, or later-selected rule is different. Preserve the original trailing and centered candidates unchanged; this clarification authorizes no retroactive promotion of their results. New prospective protocols must record issue time, known inputs, model commitment, horizon, and permitted ephemeris look-ahead.

For historical model comparison, account for search over windows, planets, aspects, endpoints and candidate models. A sole qualifying date out of 365 is not automatically a 1/365 significance result when the rule was selected after the date was known. Compare to realistic base rates and dependency-preserving controls. Separate alert burden per person-year, hit fraction, precision and rank; none is a substitute for another.

## 9. Produce specific, falsifiable interpretations without flattening richness

Keep a comprehensive evidence ledger and a bounded reader-facing forecast. A long inventory of every conceivable symbolism should not make it impossible to miss.

Each substantive claim records:

- target and direction, resolution/time window where relevant;
- source/native rule IDs and exact calculated support;
- contrary and mitigating evidence;
- dependency groups;
- robustness across the admitted input/convention alternatives;
- whether it is source-symbolic, a modern translation, or a fitted empirical claim;
- exposure/evidence class and what would count against it.

Use source-native synthesis where the source provides it. Otherwise state the bridge as a project hypothesis and freeze the comparison rubric before scoring people. Distinct dimensions—ability, desire, outward style, burden, opportunity, event and outcome—must not be swapped to rescue a miss.

Salience is not just the smallest orb. It can depend on question relevance, prerequisite satisfaction, robustness, structural position and supported source priority. Any new numerical weighting requires a declared development procedure; do not assign pseudo-calibrated probabilities to interpretive confidence.

When a later discovery occurs, classify it as an omitted implemented rule, source gap, input correction, computational defect, new hypothesis, or genuine model miss. Repair the appropriate layer. A genuine evaluated miss is not automatically an “overlooked aspect.”

## 10. Test whether added depth earns its cost

Preserve the strongest simpler baseline and the same outcome definitions. For fusion compare astrology-only, numerology-only, the authorized combination and appropriate non-symbolic/calendar baselines on the same cases. Use person-separated development/holdout logic; decisions selected across model variants belong inside training. Do not require a combination's components to each succeed individually.

For personal readings, high absolute fit is not the same as specificity. A prospectively fixed own-chart-versus-matched-decoy comparison can test specificity, while discrete predeclared claims test where the difference arises. Presentation, information exposure and scoring must be comparable. A numerology name can also carry ordinary language/demographic information; distinguish that from numerical-symbolism claims.

For timing, preserve wrong peaks, date uncertainty and eligible exposure. Unknown years remain unknown. Known cases may test engineering and develop hypotheses, but are not new independent confirmation. Larger technique libraries increase opportunities for both meaningful conditional rules and fitting noise; depth alone proves neither.

## 11. Mechanical implementation delivered with V2

`validate_astrology_deep_analysis_receipt_v2.py` checks an externally supplied contract digest; matching task/mode/protocol/catalog/input anchors; exact disposition of the committed catalog with selected entries linked to planned modules; actual evidence-file hashes; confined paths; unique IDs; exact required module/check/rule coverage; resolvable JSON pointers or line references; and prohibition on a receipt promoting development evidence to prospective validation.

All-unavailable work can be honestly accounted for, but its result is `SCOPED_WITH_GAPS`, never `DECLARED_PROFILE_EXECUTED`. `--require-executed` returns a nonzero exit status for that gap. A model may legitimately return no supported claims; it must not fabricate one merely to satisfy a form.

The checker explicitly outputs that semantic correctness, actual blinding, and predictive validity are not certified. The contract's selection and the source interpretations still need substantive review. This is a focused integrity control, not an autonomous complete astrology engine.

Keep V1 interfaces/files for historical replay. New saved analyses use V2. A reader on an old branch must follow the live research-authority pointer; a note on one branch does not mechanically update every deployed app or every old conversation. No production application or participant survey is deployed by this task.

## 12. Source audit and implementation sequence

1. Recover full versions of the existing four primary works, especially Lilly's Book III, not merely the page-115 strength table or Books I–II.
2. Add a bounded bridge corpus for currently missing rule families: Dorotheus, Rhetorius/Paulus, medieval introductions, and the complete Abu Maʿshar annual work.
3. Expand Jyotish using explicitly identified Phaladeepika/Brihat Jataka/BPHS editions; treat Tājika separately.
4. Add a modern timing reference for secondary progressions/transits and a technical directions guide without attributing those modern methods to ancient authors.
5. Build section inventories, RuleSpecs, ambiguity tables and worked-example fixtures before person-specific source selection.
6. Compile the smallest complete executable profile for the requested domain, freeze it, then evaluate it without changing the old benchmarks.

Downloading the corpus completes acquisition, not reading, source extraction, implementation or validation. The acquisition manifest and Work handoff state these boundaries separately.

## References informing this revision

- Current HumanDesign V1 source, validator, current-candidate catalog and frozen timing specifications at base commit `1b4553d0f9f03360a057cb7677be6a0969a8ae1e`.
- Cawley & Talbot (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*: https://www.jmlr.org/papers/v11/cawley10a.html . This supports separating model selection from evaluation, not a conclusion about astrology.
- Swiss Ephemeris programmer documentation: https://www.astro.com/swisseph/swephprg.htm . Numerical conventions and returned flags remain part of calculation provenance.
- Edition and technique-specific primary/translator/publisher sources are listed in `ASTROLOGY_SOURCE_ACQUISITION_V2.json` and the companion reading list. Publisher descriptions establish scope/edition, not empirical effectiveness.
