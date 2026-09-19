# Life Patterns: scenario-first survey design — fresh-conversation handoff

Date: 2026-09-19.
Status: BRAINSTORM / PROPOSED DIRECTION. Not an approved implementation specification.
Recommended new conversation title: **Human Design — Scenario-First Survey Design**.

## 1. Start here: scope and authority

The owner requested a design discussion and a handoff for a new conversation. Do not interpret the earlier approval of runtime repairs as approval to implement this new elicitation design. Continue the design in Chat; do not start a Work execution task, modify deployed code, generate paid inference calls, run chart recovery, or wake the inference VM.

The owner explicitly asked to put the Cloud Agent to sleep. The preceding conversation verified sleeping / bridge stopped. This pass did not wake it or probe inference. Preserve that state until the owner authorizes resuming runtime use. Planning and document work do not require a running VM.

Save all work in `u-dont-existDOTcom/humandesign`. Current owner instructions outrank this packet. Proposed choices below are recommendations, not invented mandatory owner requirements.

Fresh conversation read order:

1. Fetch live default-branch `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` and its task-triggered guidance. Do not reuse a remembered copy.
2. Read this packet on `chat/scenario-first-survey-design-20260919`, beginning with `OWNER-CONCEPTION.md`, then this file, then `RESEARCH.md`.
3. Fetch live metadata for the Life Patterns development pull request (#24) and the subscription-bridge evidence pull request (#29). Read `tasks/ACTIVE-TASK.json` and `state/CURRENT-STATE.md` from the live development head, plus the bridge's current `tasks/life-patterns-subscription-bridge-20260919/INTEGRATION.md` on its own live head. Reconcile stale fields; do not assume the development branch already contains the bridge evidence.
4. Use the live design specialist skill for interaction-design work. Do not let generic UI conventions override the owner's one-question conversational flow.
5. Do not read target-chart outputs, birth-derived predictions, fit scores, or the target-model crosswalk to select scenarios. This is neutral elicitation design, not a fresh certified blind semantic review, and not a mapping/scoring exercise.

The immediate next deliverable is a small, coherent set of scenario-card candidates and a proposed way of selecting/adapting the next question, followed by owner discussion or an explicitly invited text-only walkthrough. Do not ask the owner to repeat the problem statement. No deployment is authorized merely by receiving this handoff.

## 2. Owner's problem and independent idea

The owner finds it difficult to identify their own patterns from an abstract prompt. Broad questions such as whether they prioritize themselves or others seem to require obvious qualifications: 'it depends.' The owner proposes relatable, representative situations that can be answered directly. They prefer more small questions over one question containing several response demands.

Their examples are (a) being five again, wanting to do something while a bored friend asks to play, and (b) being their current age with an often-anxious romantic partner, considering their own feelings while together versus apart at work. They ask whether approximate age is needed. These illustrate the method; they are not locked questionnaire wording, a request for therapy, or authorization to infer childhood events.

The independent conception was captured before the external literature pass. Preserve it rather than treating this as a plan to install a conventional trait questionnaire or employment selection test.

## 3. Recommended direction

**Start with recognizable situations; derive patterns afterward.** The participant should not have to do the analyst's abstraction work before the interview can begin.

Recommend a scenario-led hybrid, not an exclusively hypothetical test and not a compulsory 'tell me two real examples' interview. A short scene supplies enough context to answer. Participants can answer from familiar experience, give a clearly hypothetical prediction, supply a better-fitting real example, or say it does not fit. These modes all remain informative but distinct.

Three candidate approaches were considered:

- All hypothetical vignettes: easy to start, common stimuli, but vulnerable to idealized self-prediction and unrealistic circumstances.
- All remembered episodes: grounds discussion in reported experience, but returns the search/recollection burden the owner already finds difficult; chosen examples are selective rather than an unbiased frequency sample.
- Scenario-led with optional experience grounding: the recommended reversible direction. It combines a shared entry point with the participant's context, without turning recollection into a gate on every answer.

This is a methodological hypothesis, not an established result for this app. The external literature supplies useful components and cautions, not validation of this exact design.

## 4. 'It depends' is a design input, not a failure category

Separate missing scenario information from substantive conditionality.

If a person cannot answer because the scene omits a central fact, repair the scene. For example, casual boredom versus a serious need, or optional leisure versus an urgent obligation, may fundamentally change a response. Do not demand a trait answer before specifying the relevant case.

If a person says how their response varies, that can already be the pattern. Preserve the condition and both branches; do not force them to choose a side. A question about which conditions matter is not always needed if the person has already supplied them.

If the supplied scene is unfamiliar or inapplicable, allow a different scene or a skip. 'No partner,' 'I would need to know what help they want,' and 'I do not remember being five' are not defects to explain as personality.

Do not eliminate all ambiguity by writing a legal contract. Include only the details necessary for the response task. When an omitted detail matters, state it and return to the same task. Do not silently invent the participant's assumption, or turn a request for clarification into behavioral evidence.

## 5. One response task, not just one question mark

A scene may take a few sentences. The response demand should ask for one thing: the likely reply, the immediate action, the feeling, the interpretation, or a relevant change over time. Do not ask for all of these at once.

Examples of bad compound demands: 'What would you do, why, how would you feel afterward, and was that different in childhood?' Splitting this into four mandatory turns would also be excessive. Ask only a follow-up that is still unanswered and worth the effort.

A participant may naturally provide several pieces of information. Retain them and skip already-answered probes. Do not make the conversational system less attentive in the name of standardization.

Keep one flexible response field, automatic continuation, persistent Finish for now, and preserved drafts/recovery. No new routine confirmation controls, continuous sliders, time pressure, or verbose instructions are recommended.

## 6. Candidate interaction examples

All wording in this section is newly drafted for discussion, not validated inventory content. Optional variants are alternatives or later turns, never to be displayed together as a compound question.

### A. Casual invitation during chosen personal time

Scene: 'You have finally got an hour for something you have been looking forward to doing. A close friend messages: "I'm bored—want to hang out?" There is no urgent problem.'

Response task: 'What would you probably reply?'

This fixes one particular kind of request; it does not measure a universal preference for self versus others. The person can negotiate, invite the friend to join, defer, decline, change plans, ask for details, or offer something the authors did not anticipate. Do not impose a two-option dilemma.

If the person says 'I'd say later, but then I'd spend the hour feeling guilty,' both the boundary and the feeling have already been supplied. Do not ask how they would feel, and do not call the statement a new discovery.

Possible later contrast, only if unresolved and useful: same personal plan and friend, but the friend says they are having a difficult day and would like company. Ask the same single response question. Name the changed condition; do not simultaneously change the friend's identity, the importance of the plan, and the ability to help.

This is a descriptive within-person contrast, not proof of a causal psychological mechanism. If both answers merely show an ordinary response to different levels of need, record that context without manufacturing a distinctive pattern.

### B. Another person's anxiety while present

Use a romantic-partner version only when that role is applicable or the person knowingly elects to imagine it.

Scene: 'You are feeling fairly settled while doing a quiet activity at home. Your partner is nearby and says they are anxious about an upcoming event. They are not asking you to solve anything.'

Response task: 'What, if anything, happens to your own mood?'

Possible later distance variant: 'Imagine the same starting situation, except your partner is elsewhere and you know about the anxiety from an earlier message. You are doing the same quiet activity, with no further messages coming in.' Ask the same mood question.

Do not assume that mood changes, that anxiety is contagious, or that the participant should help. Concern, tension, irritation, steadiness, and mixed responses are all possible; do not display a leading list unless response options have separately earned their place.

A difference across these scenes does not diagnose empathy, attachment, emotional dependence, or an energetic mechanism. Distance also changes immediate cues. A later probe can ask about a material ambiguity without asserting its cause.

A friend/family version can be offered when more familiar, but it is a different relationship context, not a psychometrically equivalent substitution by fiat. Preserve the chosen relationship and exact scene.

### C. Childhood is a separate time perspective

Do not begin the interview by requiring an adult to reconstruct being exactly five. First distinguish actual recollection from present-day imagination.

Possible childhood entry: 'Think of a childhood age you remember reasonably well. A friend asks you to play while you are absorbed in something you chose. What do you remember usually doing?'

A participant can instead supply a particular memory or say they cannot remember. A question asking them to imagine their five-year-old self may still be used as explicitly imaginative self-description, but cannot be stored as an actual event or a direct observation of their childhood.

Do not imply childhood answers reveal the original, unconditioned, or truer personality. School, family rules, available freedom, relationships, memory, and developmental stage can all affect what the answer means. Do not frame this as memory recovery or age regression.

### D. Additional starting situations to draft next, not an item quota

Potential neutral families: an interruption during concentrated activity; plans changed at short notice; an unclear commitment requiring a decision; a task that loses its initial interest; choosing what to do in unstructured time; disagreement with an authority or a peer.

The next conversation can develop about six opening cards spanning different everyday contexts. Six is an editorial batch size for discussion, not a required episode count, coverage threshold, or measurement-validity criterion. Discard cards that cannot elicit a useful distinction without stacking demands.

## 7. Representative of what?

A scene should be recognizable to the intended respondent population and address an ordinary behavioral/experiential situation. Vividness alone does not establish representativeness. Do not let the whole interview become a test of saying no to requests or coping with anxious partners.

A fictional case is a probe of a situation family, not evidence that the respondent's life contains that case. One response does not establish a usual frequency. A collection of deliberately contrasting scenes samples responses under those scene conditions; it is not an unbiased sample of everyday opportunities.

Do not infer 'helps people 80% of the time' from accepting eight out of ten vignettes. Everyday frequency would additionally require knowing which kinds of situations actually occur. No such weighting is proposed for this first design pass.

Use matched variants when they can clarify one consequential distinction, but do not impose an exhaustive factorial design or a paired vignette after every answer. Participants can respond differently across contexts without contradiction. Several variants derived from one story are related evidence, not independent real episodes.

## 8. Standardization and the AI's role

Recommended split: a modest reviewed bank of scenario cores, paired with an adaptive interviewer. This removes the need for the model to invent a sensible situation from scratch at every turn while preserving meaningful follow-up.

Keep essential scenario conditions and wording versioned. Adapt role, cultural setting, or vocabulary only where necessary and record the adaptation. Do not silently raise emotional stakes or change a partner into a stranger while treating it as the same measurement.

Let the model select an appropriate next family, recognize already-answered information, repair a disputed premise, capture the person's added conditions, and ask at most one useful next question. Permit topic change or stopping with incomplete coverage rather than forcing filler.

Do not convert each apparent distinction into a multiple-choice taxonomy, attach trait/HD labels to response options, or make a new chain of low-quality model review calls the primary assurance. Retain Sol xhigh as previously authorized; this design discussion does not authorize changing the runtime model or provider.

## 9. Evidence semantics: hypotheses are data, not invented events

Keep the following distinctions explicit in the proposed design. These are semantic requirements; exact implementation fields need inspection later.

- Supplied scenario text and its conditions belong to the stimulus record, not the participant's biography.
- 'I think I would say later' is an anticipated response under specified conditions.
- 'In situations like this I usually say later' is an attributed usual-behavior self-report.
- 'Last week I said later' is a reported actual event.
- 'When I was a child, I generally said later' is a retrospective self-report with its time frame and uncertainty.
- 'I think people ought to say later' is a normative view, not necessarily the participant's behavior.
- 'Your question makes no sense' is process feedback, not an episode fact.

All are meaningful information in their own terms. Do not silently collapse them into occurrences or treat imagined answers as worthless. Preserve the full answer, source pointers, scenario/version, assumptions supplied or clarified, and current pattern status.

The accepted v2 evidence contract must not be silently changed. A later implementation pass must examine where stimulus and hypothetical-response metadata can safely live; the right solution may be an outer interview record rather than fabricating episode entries. Future downstream analyses must explicitly choose which evidence classes are admissible. No scoring or chart-recovery rule is changed by this brainstorm.

A direct self-report needs no redundant approval. A faithful paraphrase is a source-linked summary, not a newly inferred connection. A substantive new relationship can be proposed for judgment, with its extra content clear. Participant approval is authority over their intended self-description; it is not independent empirical validation.

Do not require a synthesis at every scene boundary. A good interview can record useful information and move on without announcing a discovery.

## 10. Age and life stage

Recommendation: current-life scenes first; no exact birth date or exact chronological age is necessary to ask a useful everyday question. Gather only context that materially affects scene applicability, such as whether the person has experience of a particular relationship or responsibility. Reuse known answers. Allow private/inapplicable responses.

A broad optional age band could help later, but its benefit is not established merely because it is easy to collect. Life-stage/role information may be more directly useful for selecting a scene, and is itself potentially age-informative. Do not stereotype an answer from a band or silently infer the person's age.

Specific project issue: the later DOB/time recovery evaluation must not count a disclosed age band, school year, calendar clue, or demographic cue as successful behavioral recovery of the birth year. Keep birth metadata separate from the elicitation/scoring path. If auxiliary demographic information is allowed in a later analysis, its availability and effect on the candidate universe/null comparison must be prespecified and reported. Separation alone does not remove all implicit age information in natural narratives.

For the initial scenario prototype, current-life framing plus minimal role applicability is the simpler default. Childhood/earlier-life comparisons can be optional and only as precise as the person's actual recollection. The population is not expanded to minors by this packet.

## 11. How to judge whether this improves the app

Run a small text-only question-design walkthrough before implementation or further runtime hardening. The owner is a development participant, not an untouched validation sample. Do not recruit others under this packet.

Use a short, well-written recent-situation prompt as a serious alternative baseline, not only the weakest existing abstract question. For example, compare the scenario entry with 'Think of the last ordinary time someone asked for your company while you were busy. What did you say?' This comparison may reveal that cueing a real incident is easier for some topics than imagining one.

Useful observations: can the participant answer without inventing decisive context; do they understand what is being asked; does the answer expose actual conditions rather than a moral slogan; does the follow-up avoid information already supplied; does the record preserve the distinction between imagination and recollection; does the participant experience it as less laborious?

A few cases can find defects and choose a direction, not validate a questionnaire or estimate stable trait reliability. Do not claim a clean causal A/B result from having one owner answer both forms in a fixed order. If later comparison becomes a scientific claim, order/carryover, sampling, measurement invariance, and held-out evaluation need separate design.

Measure useful, faithful information relative to effort and elapsed time. More short questions are acceptable, but a long sequence of arbitrary variants is not automatically better. Leave room for uncertainty; do not demand exact percentages or confidence scores unsupported by the evidence.

## 12. Current technical state and why repositories may look inconsistent

Freshly read during this pass:

- Development pull request #24: draft/open/unmerged, head `7837d7379b4349c120296d25d0c226373d217b72`, branch `codex/discover-life-patterns-mvp`.
- Subscription-bridge evidence pull request #29: draft/open/unmerged, head `f2ec1ab5e46108b4af6e98b98be462a58ccb0eb3`, branch `chat/life-patterns-subscription-bridge-20260919`.
- The development branch's ACTIVE-TASK and CURRENT-STATE still describe the older API-credit blocker. The bridge branch and the immediately preceding conversation describe the owner-authorized VM/Codex workaround. Do not overwrite either branch from an old summary.
- Last conversation evidence: a synthetic app turn succeeded through the awakened bridge, then the owner explicitly requested sleep; sleeping / stopped was verified. This pass deliberately did not re-probe or wake the VM.
- Existing inference policy: GPT-5.6 Sol xhigh, no weaker automatic fallback.
- Known accumulated defects and repairs: repetitive or circular questions, false contrasts, process-feedback contamination, restatement-as-inference, invisible/empty continuation states, optional historical-source hints aborting answers, provider credit failures, and misleading generic error messages. Green interface tests did not establish conversational quality.

Keep runtime recovery, source history, saved pattern corrections, and the separate scientific objective. This design changes the proposed entry point, not the entire application or the accepted research substrate by default.

## 13. Active lessons and closing boundary

Owner-source projection: the root product outcome remains OPEN; this turn's deliverable is brainstorming plus a usable handoff. Authority is design-only. Automatically executing a previously authorized bug repair is not the same as implementing a new unapproved method during an explicit brainstorm.

Applied lessons: preserve exact owner intent; replace a failing elicitation premise rather than adding more local wording patches; distinguish reported experience from interpretation; avoid invented mandatory examples/age bands/validation campaigns; verify research claims; keep age metadata from being mistaken for prediction success; save all work in the repo; deliver files directly; respect the explicit sleeping state.

L0–L4 design diagnosis: high abstraction and bundled response demands are the owner's observed cognitive-load problem; everyday scenes are the proposed entry; one response task and faithful adaptation support comprehension; hypothetical-versus-observed labeling protects credibility; pause, correction, uncertainty, and no forced synthesis preserve participant control. This is a shape/design pass, not a completed usability or accessibility certification.

Next conversation should first draft/refine the small scenario set and show how one selected example would branch after a plausible answer. It should not spend its first pass rebuilding transport, reviewing unrelated scoring code, or asking what the owner already explained. Implementation waits for a later explicit design/implementation instruction.
