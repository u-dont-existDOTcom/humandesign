# Questionnaire changes for the expanded astrology study

**26 October 2026 — review and proposed changes; no live questionnaire or score changed.**

## Recommendation

Keep **one shared, neutral questionnaire** and reuse the existing answers across the eligible systems. The present questionnaire already covers most of the additional subject areas. The main work is to connect each source claim to the exact observation it requires, improve capture of dated events where a timing hypothesis needs them, and carry birth-quality and prior-knowledge metadata through the existing intake.

**No new mandatory questions are justified by this review.** Preserve the existing 23 optional topics and seven conditional probes. A small number of source-specific gaps may justify optional clarifications after measurement review; those clarifications must share the current burden allowance, not accumulate into another questionnaire for each tradition.

The research is developed enough to choose bounded tests. That does not establish that every book, calculation engine, mapping and study is complete. Further book reading is not a prerequisite to testing claims whose source, calculation and measurement are already sufficiently specified. Unready claims can remain unscored without delaying an otherwise ready study.

This review follows the earlier decision to integrate Maya into the shared instrument and the later correction to stop the unproductive Gene Keys message-style questionnaire. It adds an auditable change ledger, not a new personality theory or scoring interface. [S1, S4]

## 1. What already exists

There are several different objects called a questionnaire or “v3” in the repository. Their inventories must not be added together as a participant quota.

| Existing component | What it contains | Current evidence of status |
| --- | --- | --- |
| Tendency-first collection bank | 25 direct questions about usual behavior; 30 older routes retired from new elicitation | Present in the source of the October 18 backend release. This is a question menu, with prior answers and skips retained. |
| Optional experience and meaning section | Eight items, offered as four starting topics plus four optional additional topics | Present in that release; separately consented and excluded from primary and CF-003 scores. |
| **Adaptive shared-survey V3** | **23 optional topics + seven conditional probes** | Latest reviewed shared design, pinned to `7971b3c1564d9c38bce17abe4c4575affcba2c76`; not deployed, frozen for confirmatory use or scored. |
| Existing Maya integration | Eleven provisional source claims, eight constructs, nine reused question IDs; a complete copy of the 23+7 objects | Preserves the original question objects unchanged. One possible craft clarification is outside the active arrays. |
| Other reference instruments | Historical V7 menu, HD V2 reference questions, CF-003 secondary module, separate TN-001 IPIP study | Their meanings and historical scores remain distinct. They are not extra required sections of this shared interview. |

The latest retrieved deployment receipt confirms **Railway Action v1.9.0 on October 18**. The same receipt says the private Custom GPT editor update was still pending. It does not prove that the private GPT has since been updated, or that either service is working today. [S2, S3, S5]

### The 23 topics already cover a broad range

| Existing topics | Observable information already requested |
| --- | --- |
| `VOCATION`, `LEARNING_HISTORY`, `STATUS` | Actual work and contribution, learning and skills, responsibilities and recognition; preferences kept separate |
| `ART`, `PLAY`, `SENSORY_ENJOYMENT` | Creative production, aesthetic appreciation, play and sensory enjoyment |
| `BONDS`, `KINSHIP`, `PARENTING`, `UPBRINGING` | Actual relationship patterns, relatives, caregiving and changes in early living arrangements |
| `HOME`, `TRAVEL`, `RESOURCES` | Belonging, actual travel/relocation and material circumstances |
| `BELIEF`, `BELIEF_CHANGE`, `RENUNCIATION`, `MYSTERY`, `DREAM` | Practice and worldview, changes in conviction, withdrawal from ordinary goals, investigation of unresolved questions, dream recall |
| `ANGER_REPAIR`, `RECIPROCITY`, `CONTENTMENT`, `PRIVACY` | Anger duration/context, helping and receiving help, satisfaction and striving, disclosure preferences |
| `TIMELINE` | Up to three personally important turning points, approximate age/year and date confidence, external change versus inner change |

The seven conditional probes already address reasons/evidence in disagreements, independent feedback, chosen solitude, group departure, held leadership roles, partner priorities and project follow-through. Work, family, travel, learning, spirituality and creativity should therefore not be presented as missing new subject areas. [S1, S2]

## 2. Changes I recommend

### A. Complete the claim-to-answer mapping before adding questions

For each candidate model, record the source rule, actual observable, existing question and answer dimension, reference period, expected direction, relevant condition/exception, and a possible contradictory answer. Classify the measurement link as **direct**, **partial proxy**, **missing**, or **not testable by this questionnaire**. Keep unimplemented/calculation-uncertain status separate from measurement status.

This uses the existing source-to-observable schema. A new astrological system does not itself create a new interview requirement. One answer may be used by several separately evaluated models, but it remains one observation. Three traditions interpreting the same work-history answer do not create three independent confirmations. [S1, S8]

The accompanying JSON ledger does this for the existing eleven Maya bindings, two primary-directions event endpoints and the narrow Hellenistic marriage-count draft. It also gives a preservation review for every one of the 23 V3 topics. It is **a bounded gap audit**, not a claim that every annotation in every historical source has been converted into a scored prediction.

### B. Add precision to event records, using the existing topics

`TIMELINE` already records important changes. `VOCATION`, `STATUS`, `BONDS` and `TRAVEL` can already produce useful history. Their broad narrative answers need a few structured details **only when an admitted timing or count hypothesis requires them**:

- The participant's exact event description and which event category it actually satisfies.
- Approximate date or date range, with day/month/year/age-only/unknown precision retained.
- Whether the date comes from memory, a contemporaneous record or another voluntarily supplied source; documentation is not universally mandatory.
- Whether the event was an external occurrence, an internal change, or both.
- The period of life covered by the report, and whether the participant reported all relevant events or only selected turning points.
- Whether a relevant outcome was reported, explicitly absent within a defined period, not asked, uncertain, declined, or still in the future.

Do not convert “around 2018” into January 1, 2018 or invent an exact age. Do not infer an event-free year from a blank entry. “Three turning points” is a selective autobiographical sample; it is not a full inventory of promotions, separations or moves. Its omissions cannot support false-positive or true-negative calculations. [S2, S6]

These are additions to evidence capture, not a demand to ask everyone a complete lifetime chronology. The current primary-directions scorer consumes documented **positive events** only. It must remain labeled that way; a later complete forecasting score would need separately defined observation windows and negative outcomes. This review does not change that scorer or make complete lifetime negatives a prerequisite for its present bounded diagnostic.

### C. Use narrowly defined clarifications only for actual measurement gaps

| Candidate claim | What the current questions provide | Specific remaining gap | Recommended action |
| --- | --- | --- | --- |
| Documented formal role gain | `STATUS`, `VOCATION`, `EP-LEADERSHIP-HISTORY` | Formal role change versus increased informal influence, desire for recognition or an inner sense of purpose; date and evidence | Reuse a sufficient existing answer. Otherwise flag this as a conditional event-capture need if that endpoint enters the study. |
| Documented involuntary role loss | Work and status history | Involuntary loss versus a voluntary resignation, ordinary job change or reduced interest; date and evidence | Same rule. Preserve uncertainty instead of guessing the cause of departure. |
| More than one marriage in the narrow Ptolemy draft | `BONDS` provides broad friendship/partnership history | Count and culturally specified definition of marriage, age/window observed; long partnerships are not interchangeable with marriages | Retain as an optional, separately defined outcome. The existing “by age 50” cutoff is an analyst choice, not a generic question for every participant. |
| Skilled physical making in the colonial Yucatec craft claim | `VOCATION`, `LEARNING_HISTORY`, `ART` | Actual learned physical-making activity versus art appreciation, digital creativity or interest | Retain the **already proposed** optional craft clarification. Activate only if existing answers do not resolve the construct and the claim is selected. |
| Teaching | Learning and work history | Having studied a subject does not establish having taught it | Reuse an explicit teaching role if reported; otherwise record partial coverage. No new question is automatically admitted. |
| Mediation | Personal relationships and anger/repair history | Managing one's own conflict is different from mediating other people's disputes | Preserve as partial coverage unless the actual answer establishes mediation. |
| Ceremonial or religious role | `BELIEF` and `VOCATION` | Holding beliefs/practices is different from holding a community role | Preserve the source's actual scope and use only directly reported roles. |
| Childbirth-related claim | `PARENTING` records caregiving | Caregiving is not childbirth count, biological parenthood or an event date | Keep the claim unmapped unless a separately justified, consented and source-faithful endpoint is selected. Do not expand the family section by default. |

The Hellenistic draft is a **partial sign-only subrule**, not the complete Ptolemaic method. Its comparison group does not literally predict one marriage. The Western event draft is explicitly a **modern diagnostic**, not a complete historical Lilly/Argoli reconstruction. [S6, S7]

No new participant-facing wording is authored or promoted here. This context has seen candidate theories. Any substantive wording or coding repair must follow the existing theory-blind content-authority process; the mapping audit can identify the defect but cannot certify its own neutral measurement replacement. Detailed domain-seeded material remains development material until the existing independent review/calibration requirements are satisfied. [S9]

### D. Complete the intake metadata through the existing birth route

The forward-blind intake template already includes birth-time source, stated uncertainty, place/timezone, consent and prior Human Design knowledge. Reuse those fields. The inspected legacy reference HTML form renders fewer fields; this identifies a **template/form discrepancy**, not proof of the current private production form's behavior. Verify the actual chosen intake route before changing it. [S10]

For a multi-system study, extend prior-knowledge metadata to the systems actually being tested: familiarity, whether the person knows their own relevant placements/profile, and whether they have already received an interpretation. This should be collected without showing new chart information.

Participants need not calculate ayanamsas, local solar time, calendar rollovers or house systems. The calculation layer must apply its declared conventions to the same private birth record. Preserve source quality and uncertainty; do not choose a birth time or calendar variant because it fits the answers. If an uncertain input leaves a claim invariant, it may remain eligible under its contract; otherwise the system abstains on that claim. [S10, S11]

### E. Preserve a bounded, understandable interview

Keep one question at a time, reuse adequate existing answers, accept uncertainty and skips, and end the chosen sitting clearly. The adaptive supplement already allows at most **five participant-chosen optional topics and two additional conditional probes per sitting**. The caps do not mean 23+7 questions are required, and the optional supplement does not redefine the whole historical interview's completion rule. [S2]

Distinguish progress through the present sitting or reviewer batch from overall interview completion. If further reviewer work is genuinely undetermined, say so once. Do not repeatedly present “one remaining” as an overall promise. Completing a chosen optional sitting is still a real stopping point; the respondent need not continue into another system's questionnaire.

There should be no extra question merely because it has a new ID, a new astrological interpretation, a new prompt version or a still-empty coverage cell. A clarification needs an unresolved, material distinction in the person's evidence. Existing tendency-first rules already require this. [S3]

### F. Separate outcomes and comparisons while sharing the answers

Keep the following analyses identifiable:

1. Usual behavior and reported enduring/conditional patterns.
2. Actual biographical events and historical timing.
3. Future events, assessed only after their predeclared windows end.
4. Pair dynamics, which require suitable two-person data and consent.
5. Experience and meaning, retained as their own optional research section.

A questionnaire response about creativity cannot validate an eclipse table, horary judgment, relationship forecast or future event. Report each eligible source model separately. Any combined-system model is a separately frozen comparison arm; the design does not require every component to succeed independently before a prespecified combination can be tested. It does prohibit building the winning combination after seeing the final test answers and calling that confirmatory.

For comparisons between systems, report which outcomes and participants each could actually score, abstentions, missingness and uncertainty. Where models cover different domains, do not give a headline winner from incomparable denominators. Use shared eligible outcomes for direct comparisons, and preserve system-specific results separately. Retain the existing matched-chart and nonastrological controls and account for the number of variants tried. [S1, S11]

No historical owner or previously inspected participant record becomes untouched validation by passing it to another system. Those records remain useful development evidence. There is no reason for the owner to repeat an already adequate interview for this review.

## 3. How this applies to the additional systems

| System or research family | Questionnaire implication |
| --- | --- |
| Human Design | Retain frozen version meanings and the established forward-blind pipeline. Source/engine additions do not silently extend the old score. |
| Western and Hellenistic natal interpretation | Reuse behavior, work, education, relationship and family evidence where the source claim matches. Preserve each school and narrower rule's scope. |
| Primary directions and other timing methods | Use the structured event layer. The currently retrieved Western event scorer admits only formal role gain/loss; other possible event families are not thereby approved. |
| Jyotish schools | Share answers, but preserve source variants and conditional chart rules. Need for new questions depends on a specific observable gap, not the number of books. |
| BaZi and Zi Wei | Work, family, resources, relationships and travel are already represented. Source annotations alone do not establish an implemented natal engine or score-ready mapping. |
| Tibetan traditions | Separate individual natal claims from calendar, ritual and divination material. Use common questions only where a specific person-level observable has been specified. |
| Maya traditions | Reuse the completed shared-survey integration. Keep colonial Yucatec and distinct Highland community claims separate. The optional craft clarification remains the one existing possible addition. |
| Gene Keys | Preserve source work and unresolved profile-calculation parity. Retire the failed message-style questionnaire path; it supplies no basis for adding another respondent section. |

This is a readiness-dependent shared design, not a declaration that all these models are implemented or validated. The new claim-level ledger is deliberately explicit about what remains a partial proxy or an unmapped source claim. [S1, S4, S6, S7]

## 4. Railway and what can proceed now

The questionnaire review, source-to-question mapping, change ledger, version reconciliation and local verification can all proceed without Railway. Those tasks are completed in this review package. The files do not claim to be a functioning hosted interview, a server-side saved participant record or a deployment.

Do not assume that the older offline HTML pilot can import the newer adaptive-V3 schema without an adapter check; they are different artifacts. A downloadable JSON candidate is useful for design review, but does not establish that the older app understands it.

The last independently retrieved access audit, dated October 25, reported both connector reauthorization and CLI `Unauthorized`, and could not refresh the private feedback queue. Its last authenticated snapshot was October 19. The eight annotations in that snapshot are overlapping development feedback, not eight new respondents or today's queue state. The draft wording repairs and proposed retirements have not been silently accepted here. [S12]

Restored account access has not been established in this review. A read-only `whoami` attempt returned no result before being aborted; it establishes neither successful authentication nor a fresh `Unauthorized` response. An account login, the ChatGPT-to-Railway connection and the running interview service are distinct routes; failure of one must not be reported as proof that all three are down. There is no verified universal account-reset step for the previously reported `could not validate id_token_hint` error.

The useful recovery sequence is:

1. Open [Railway's direct login](https://railway.com/login) and use the existing account's normal sign-in method. This checks whether the account itself is reachable, separately from the ChatGPT authorization callback.
2. If direct login works, authorize the Railway connection through the Railway plugin in ChatGPT. The official plugin uses its own OAuth connection and does not depend on the CLI. A successful CLI login alone would not repair that connection. If the same callback error recurs after a fresh authorization attempt, retain the exact error for the existing support conversation; repeating an already failed reconnect is not an established fix. [S13]
3. To restore CLI access on the laptop, the documented command is `railway login`; where opening the browser does not work, use `railway login --browserless` and complete the displayed pairing URL/code in the browser. Then check `railway whoami`. This signs in the CLI; it does not deploy or establish that the questionnaire service is healthy. The user's interactive account authorization is required to complete this step. [S14]
4. If direct account login itself fails, treat that as an account-access issue and continue the existing support route with the observed failure. The available evidence does not establish that deleting the account, resetting the project or rotating application keys would fix it.

These are verified authentication routes, not a claim that the reported error has been resolved. No account settings, credentials, deployments or feedback records were changed in this review.

## 5. What this review delivers and what comes next

**Delivered:** a preserved baseline inventory; a review of every optional topic; a concrete gap assessment of fourteen existing source-bound claim candidates; proposed metadata changes; session/scoring constraints; and verified Railway sign-in routes with their limits. No new source-reading campaign, synthetic cohort, live prompt rewrite or new scoring service is introduced.

**Implementation order:** choose the bounded claims for the first shared test from the existing readiness records; retain current question text wherever adequate; prepare only the demonstrated intake/event metadata and justified conditional wording repairs through the existing neutral-authoring process; verify the chosen GPT/intake/backend versions together; then freeze the models, selected questions, coding and controls before collecting new scored answers.

Railway access is a hosting dependency for that chosen service. Complete reading of every historical source is not a dependency for this review or for an otherwise ready bounded test. This review is complete at the decision boundary; actual deployment and human predictive validation remain separate outcomes.

## Sources and exact evidence

All repository documents below were retrieved during this review. Files on different branches are intentionally identified separately; their presence does not mean they have been merged into production.

- **S1 — Prior shared-survey decision and Maya integration:** [integration report](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/docs/astrology-research-map/MAYA_INTEGRATED_SHARED_SURVEY_AND_FINAL_TEST_DESIGN_20261023.md); same-commit candidate and eleven-claim integration JSON are beside it.
- **S2 — Exact adaptive V3 source:** [23-topic and seven-probe candidate](https://github.com/u-dont-existDOTcom/humandesign/blob/7971b3c1564d9c38bce17abe4c4575affcba2c76/tasks/life-patterns-external-questionnaire-merge-20261021/LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json) and [interviewer design delta](https://github.com/u-dont-existDOTcom/humandesign/blob/7971b3c1564d9c38bce17abe4c4575affcba2c76/tasks/life-patterns-external-questionnaire-merge-20261021/INTERVIEWER-V3-DESIGN-DELTA.md). Source file SHA-256: `fec3d0d18b9463d29842e65c4759fd7ed900a019889531896f89c1b3764e0084`.
- **S3 — Tendency-first source used in the release:** [25-item bank and collection rules](https://github.com/u-dont-existDOTcom/humandesign/blob/7de212f027e14c198fb58dc91d11df3068d58e56/apps/life-patterns-participant/participant/static/tendency-first-v1.json); [eight-item experience bank](https://github.com/u-dont-existDOTcom/humandesign/blob/7de212f027e14c198fb58dc91d11df3068d58e56/apps/life-patterns-participant/participant/static/experience-meaning-v2.json).
- **S4 — Gene Keys stop-loss and return to real evidence:** [owner-outcome correction](https://github.com/u-dont-existDOTcom/humandesign/blob/4a44067b5c9504bb8af7acc818567e692a32ea91/docs/astrology-research-map/ASTROLOGY_OWNER_OUTCOME_REBIND_20261025.md).
- **S5 — Verified historical backend release:** [October 18 deployment receipt](https://github.com/u-dont-existDOTcom/humandesign/blob/513ec84a658a5ae437852ef8e14f06297a89877a/tasks/life-patterns-experience-gpt-railway-20261017/LIVE-DEPLOYMENT-RECEIPT-20261018.json).
- **S6 — Existing two-endpoint event scorer:** [source-qualified modern diagnostic contract](https://github.com/u-dont-existDOTcom/humandesign/blob/a206838686e956d21d3d6a64629c022916dd2a4b/docs/astrology-research-map/western-event-only-blind-score-20261025/BLIND_EVENT_SCORING_CONTRACT.json).
- **S7 — Hellenistic marriage endpoint:** [C33 development-only study draft](https://github.com/u-dont-existDOTcom/humandesign/blob/ef8b143a9e30545118db72479a5cf3974f8b3c08/docs/astrology-research-map/HELLENISTIC_C33_BLINDED_MARRIAGE_COUNT_STUDY_DRAFT_V1.json).
- **S8 — Existing evidence-trace format:** [source-to-observable schema](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/docs/astrology-research-map/CLAIM_TRACE_SCHEMA_V1.json). This review reuses its concepts rather than inventing a competing runtime format.
- **S9 — Current Life Patterns neutral-content policy:** [theory-blind content-authority policy](https://github.com/u-dont-existDOTcom/humandesign/blob/3e82806d8877510ecc081ece69b9de1f74f4c76f/docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md). Current branch resolved to `3e82806d8877510ecc081ece69b9de1f74f4c76f` in the branch read.
- **S10 — Existing birth intake:** [intake template](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/reference/forward_blind/participant_intake_template.json), compared with [legacy reference HTML](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/reference/custom_gpt/scientific_intake.html). These are repository references, not live-page observations.
- **S11 — Frozen-model testing and threats:** [forward-blind specification](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/docs/20_forward_blind_prospective_validation.md), [checklist](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/docs/21_forward_blind_execution_checklist.md), [threats to validity](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/docs/12_threats_to_validity.md), and [HD scoring contract](https://github.com/u-dont-existDOTcom/humandesign/blob/b0c24930cc2c4b5b8ae8f792e061fd51dd8eac7e/reference/core/v4_3_scoring_algorithm.md).
- **S12 — Access and unresolved feedback:** [October 25 access audit](https://github.com/u-dont-existDOTcom/humandesign/blob/352e4434fead84828b007ca6c068faea2385264a/tasks/feedback-context-triage-20261009/DAILY-ACCESS-CHECK-20261025.md).
- **S13 — Railway's official ChatGPT connection:** [ChatGPT plugin documentation](https://docs.railway.com/ai/chatgpt-plugin), retrieved October 26, 2026; describes the plugin's OAuth connection and account authorization. [Direct login](https://railway.com/login) was also retrieved. No authenticated browser session was inspected.
- **S14 — Railway's official CLI authentication:** [railway login](https://docs.railway.com/cli/login), retrieved October 26, 2026; documents browser and browserless pairing flows. This does not document a specific fix for the reported `id_token_hint` error.

No private participant answers, identifying birth records, credentials, owned book scans or account-security messages are included in this public review.
