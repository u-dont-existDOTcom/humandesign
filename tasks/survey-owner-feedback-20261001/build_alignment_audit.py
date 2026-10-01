"""Source-bound, manually adjudicated route audit; not an automatic validity score."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = ROOT/'tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json'
bank = json.loads(source.read_text())
# Each note is a substantive item disposition. These are not inferred from keyword matching.
notes = {
'A0': ('replace', 'A single invitation decision confounds recent contact, desire for company and current activity. It is not a social-orientation measure.'),
'G23': ('retain', 'Open description of what attracts attention can be useful; do not turn one dinner observation into a global noticing rank.'),
'G19': ('replace', 'Need, burden and negotiability explain a reasonable boundary choice. Ask the recurring way of balancing own plans and requests first.'),
'F0': ('replace', 'Matched audience contrast can clarify adaptation, but is burdensome as an opening and partly elicits communication skill. First ask the usual audience-dependent pattern.'),
'G05': ('replace', 'One transport argument mixes stakes, persuasion ability, desire to persuade and the partner response. Keep capacity and preferred use separate.'),
'M11': ('replace', 'A meal bargain may elicit an ordinary fair division rather than a stable bargaining preference. Start with how negotiation normally unfolds.'),
'G06': ('replace', 'A shared meal can illustrate entry into group work; spontaneous initiative and awaiting role clarity should be asked as a usual pattern, not inferred from this event alone.'),
'R02': ('probe', 'Use only to clarify a real difference between assigned and unassigned roles. An instruction to coordinate creates role expectations, not a leadership trait.'),
'G07': ('retain', 'Already asks a recurring actual pattern in how connections begin. Preserve life-stage and opportunity differences.'),
'G08': ('retain', 'Can reveal recurring expectations placed on the person. Keep others expectations distinct from verified competence or the persons responsibility.'),
'R03': ('probe', 'Useful boundary probe only after mismatched expectations were established; do not manufacture the antecedent.'),
'M07': ('retain', 'Explicitly separates ease at the start from improvement through practice. Self-report does not objectively establish exceptional ability.'),
'M08': ('probe', 'Others requests may corroborate recognition only at the named skill and source scope. Requests are not objective ability measurements.'),
'G01': ('replace', 'Organizing a contrived message thread is not the only competent approach. Delegation, asking another person or using a tool must be usable answers, not failures to answer.'),
'G02': ('replace', 'A trip explanation can illustrate information selection, but may test compliance with the task. Ask what the person usually does with an idea for different listeners.'),
'G03': ('retain', 'Directly asks the return of a personally important unresolved issue. Importance must be the persons, not supplied as proof of persistence.'),
'R01': ('probe', 'Ask what closes a returning issue only when closure remains unknown. Do not conflate injustice, curiosity and inefficiency.'),
'G04': ('retain', 'A failed instruction is a concrete way to observe the first troubleshooting step. Scope to troubleshooting, not global originality.'),
'D0': ('replace', 'Repeating while improvement is visible is instrumentally reasonable for many preferences. Ask whether refinement itself is rewarding, with activity-specific exceptions.'),
'G22': ('retain', 'A useful interruption-response question, but not by itself evidence of uninterrupted focus depth or a general attention trait.'),
'E0': ('probe', 'A choice context for subsequent questions, not an independently scored trait item. Prefer an already described choice rather than creating another scene.'),
'G09': ('probe', 'Only asks noticed bodily signals in the established choice. Do not imply everyone has one or that noticing makes it trustworthy.'),
'R04': ('probe', 'Useful only if a bodily signal was reported and its repeatability or perceived usefulness is genuinely unresolved.'),
'M10': ('probe', 'Within-choice change should not be mistaken for across-choice consistency. Suppress if the respondent already described the trajectory.'),
'M05': ('retain', 'Can elicit the cues underlying a feeling that something is off in a familiar setting. It cannot validate intuition accuracy.'),
'M06': ('demote', 'Knowing a familiar route helps detect a deviation almost by definition. Use only if a nontrivial familiarity threshold matters; never mandatory evidence.'),
'G10': ('replace', 'Accepting a groups fixed schedule often reflects feasibility or interest, not stable direction or a malleable identity. Ask a usual adaptation boundary directly.'),
'G20': ('retain', 'The normalized resource amount helps make purposes concrete. It yields reported priorities at that amount, not a population-level materialism score.'),
'M03': ('replace', 'A feasible, short promise with no competing demands invites a normative yes. Ask actual follow-through tendencies and meaningful exceptions.'),
'M04': ('probe', 'Fatigue or errors may change action without changing commitment. Ask only if intention versus available capacity remains unresolved.'),
'G21': ('retain', 'Already a direct usual-pattern question with a simple free-day example. A prior flexible-scheduling answer can fully settle it.'),
'M09': ('demote', 'Current contract measures a concrete cost-benefit switching condition, not novelty versus stability. A useful-feature answer may be adequate but adds little about temperament.'),
'G11': ('retain', 'Names environmental preferences. Functional effects require reported experience, not inference from noticing a room feature.'),
'G12': ('retain', 'Directly asks attraction onset when applicable. Keep affection, romance and libido separate, and allow non-disclosure.'),
'G13': ('retain', 'Directly asks what tends to deepen closeness. Do not infer that the inverse necessarily weakens a bond.'),
'R05': ('probe', 'Use only for a materially unresolved contact/availability boundary. Preferences vary across relationships and stages.'),
'G14': ('retain', 'A direct baseline question when alone; do not present a brief hypothetical period as measured longitudinal mood.'),
'B0': ('replace', 'Repeated partner worry may produce irritation, concern or emotional contagion. First elicit usual relationship-specific effects rather than treating one reaction as all emotional permeability.'),
'R06': ('probe', 'An accusation changes the social situation. Scope the reaction to that conflict rather than generic disagreement or stable mood.'),
'M01': ('retain', 'Keeping the actual deadline fixed makes subjective pressure separable from genuine urgency. Preserve interpretation and stakes.'),
'M02': ('probe', 'Only clarify persistence after pressure is removed if that trajectory was not already supplied.'),
'G15': ('replace', 'Computer-work energy is not all-work energy. Start with activity-specific energizing/draining patterns; mental fatigue, physical fatigue, interest and persistence are distinct.'),
'R07': ('probe', 'A matched short workload increase can be useful after a chosen activity baseline. Do not ask automatically after an already adequate duration/context answer.'),
'R08': ('probe', 'A four-week counterfactual is a self-prediction, not observed sustainable capacity. Use only if realistic and adding a missing duration distinction.'),
'R09': ('probe', 'Stopping cues and recovery are distinct. Keep any already supplied recovery information and avoid a second automatic question.'),
'G16': ('replace', 'Project meaning, progress, costs and social context all affect motivation. Ask recurring mobilizers first; a low-recognition scenario is an optional boundary.'),
'R10': ('probe', 'Leaving a costly conflict may be reasonable rather than low persistence. Ask only for a still-unknown disengagement threshold.'),
'G18': ('replace', 'Rest after a demanding social day is not a clean introversion indicator. Compare the persons usual recovery after different kinds of social contact.'),
'R11': ('probe', 'Useful re-entry cue only after a real wish for solitude has been established.'),
'G24': ('probe', 'Optional earlier-life comparison only with permission and a meaningful temporal question, not compulsory retesting.'),
'R12': ('probe', 'Change attribution is the respondents explanation, not verified causality. Ask only after actual change and permission.'),
'G17': ('replace', 'Correcting consequential misinformation is compatible with many temperaments. Ask the spontaneous pull to correct minor errors, then use matched stakes only to clarify the boundary.'),
'G25': ('demote', 'Reduced practical reliance after repeated unreliability is expected risk adjustment, not evidence of a globally suspicious disposition. Keep as a trust-change probe only.'),
'R13': ('probe', 'Evidence needed for renewed reliance is useful after trust change, but does not establish a universal forgiveness style.'),
'WHY': ('probe', 'Not automatic after every answer. Ask a reason only when different explanations would materially change the supported reading.'),
'AFTER-CHOICE': ('probe', 'Separate decision resolution from objective decision quality; skip if the answer already describes its later trajectory.'),
'PREFER-PERSUADE': ('probe', 'Preserves willingness versus capacity; only necessary if the first answer leaves preferred use unclear.'),
'PREFER-EXCHANGE': ('probe', 'Whether a person wants to keep bargaining differs from ability. Do not ask again if a limit is already stated.'),
'OUTREACH': ('probe', 'Only applicable when connections are desired and their deliberate initiation remains unknown.'),
'VERIFY': ('probe', 'Competing sources can clarify verification behavior. Asking a trusted person or AI is a response, not evidence that the person must personally sort all messages.'),
'WORKING-METHOD': ('demote', 'Reducing recurrent friction is sensible across many personalities. It is a practical threshold probe, not evidence of novelty seeking or resistance to tradition.'),
'PRACTICE-REASON': ('probe', 'Only clarifies intrinsic versus instrumental value when not already answered. Visible improvement alone does not establish intrinsic enjoyment.'),
'FOCUS-DEPTH': ('probe', 'Can add uninterrupted depth/duration if only interruption effects are known. Interest remains a stated condition.'),
'CHOICE-TIME': ('probe', 'Useful only for an unresolved trajectory of clarity over time; time taken is not intrinsically better reasoning.'),
'SIGNAL-DEPENDABILITY': ('probe', 'A report of perceived consistency is not proof of reliable somatic prediction. Retain counterexamples and uncertainty.'),
'SIGNAL-NOT-FOLLOWED': ('probe', 'Useful boundary between noticing a signal and acting on it; do not equate overriding it with dysfunction.'),
'ADAPTATION': ('probe', 'May clarify which preferences survive group adaptation. Do not duplicate the revised direct adaptation-boundary question.'),
'ROOM-EFFECT': ('probe', 'Ask experienced effects only if needed; mere dislike/notice does not establish impairment.'),
'PHYSICAL-CLOSENESS': ('probe', 'Optional affection/sensory preference is not automatically sexual desire, attachment or global sociability.'),
'MOOD-AFTER': ('probe', 'Recovery trajectory only for the specific interpersonal reaction already reported.'),
'WORK-RECOVERY': ('probe', 'Only after meaningful fatigue was reported; do not assume every person is exhausted or every break restores them.'),
'STATUS': ('replace', 'A yes to genuine appreciation does not quantify recognition motivation. Ask how important recognition is, apart from practical benefit.'),
'OWNERSHIP': ('demote', 'Perfectly equivalent reliable access is artificial; answers are meanings of ownership in that hypothetical, not a global possessions trait.'),
'LIFE-PHASE': ('probe', 'Useful temporal comparison with permission; approximate life periods suffice. Do not ask for birth information.'),
'CORRECTION-REASON': ('probe', 'Only after a real difference in correction thresholds and only if the reason is still materially unknown.'),
'CARE-RESPONSIBILITY': ('probe', 'Noticing need and feeling responsible are different. Preserve the persons actual boundary without a moral ranking.'),
'CARE-LIMIT': ('probe', 'Delegation/limits matter only if not already established; care burden alone cannot diagnose a trait.'),
'ROUTINE-CHANGE': ('replace', 'The existing guide accepts a mood-dependent novelty choice. That is not evidence of the persons usual balance of novelty and familiarity across opportunities.'),
'ROMANCE-FADE': ('probe', 'Ask for additional weakening conditions only if genuinely missing; do not automatically mirror a question about deepening.'),
}
rewrites = {
'A0': 'When your time is your own, do you usually protect uninterrupted time, look for company, or vary depending on who and what is involved? For example, a friend invites you out while you are enjoying something alone.',
'G19': 'When someone wants more of your time than you had planned to give, how do you usually balance helping them with your own plans? A non-urgent request that you could renegotiate is one example.',
'F0': 'Beyond what ordinary politeness calls for, how much do you usually change the way you express the same preference to different people? For example, asking for less noise with close friends versus people you have just met.',
'G05': 'When you actually try to persuade someone, how does it usually go? For example, explaining why you prefer an earlier departure. This is about your experience of doing it, not whether you enjoy persuading people.',
'M11': 'When sharing work or costs with someone, how do you usually work out an arrangement you both accept? Preparing a meal together is one example; another familiar situation is fine.',
'G06': 'In group work without assigned roles, what do you usually do: step in, offer a particular contribution, wait for a clearer role, or something else? Preparing a shared meal is one example.',
'G01': 'When information is messy or conflicting, what is your usual first move? For example, sorting it yourself, asking someone to explain, or using a tool. Describe what you actually tend to do.',
'G02': 'When explaining something you understand, how do you usually decide what to include for the listener? A short practical explanation is enough as an example; you do not need to perform one now.',
'D0': 'When practising a skill, how do you usually feel about repeating and refining a small detail? For example, repeating a pronunciation: the refining itself may feel enjoyable, neutral or tedious, whether or not you find it worthwhile, or differ across activities.',
'G10': 'When joining a group, which parts of your usual way of doing things tend to adapt, and which remain important to keep? A group with a different schedule or working style is one example.',
'M03': 'How do small voluntary commitments usually play out for you after the initial enthusiasm fades? For example, a manageable promise to help with a task. Describe your actual pattern, including exceptions, not what someone ought to do.',
'B0': 'How do other peoples moods usually affect your own, and does that differ by relationship? For example, a worried friend or partner may leave you concerned, similarly worried, irritated, or largely unchanged.',
'G15': 'What kinds of activity tend to leave you energized or drained? For example, mentally absorbing work, practical chores, physical activity or time with people may affect you differently. Describe the differences that matter for you.',
'G16': 'What usually makes sustained effort feel worth continuing for you? For example, progress, interest, usefulness, commitment to someone, recognition, or another factor may matter differently across projects.',
'G18': 'After time with people, including company you enjoyed, what usually makes you want more company versus time on your own? For example, length, group size or how demanding it was may make a difference.',
'G17': 'When you notice a minor factual error that has no practical consequence, how much do you usually feel pulled to correct it? Important misinformation can be different; describe that difference only if it helps explain your pattern.',
'STATUS': 'How important is recognition from other people to you, apart from its practical benefits? For example, appreciation for work you already value may add little, matter a lot, or depend on whose recognition it is.',
'ROUTINE-CHANGE': 'When you genuinely have a choice, do you usually seek new experiences, prefer familiar ones, or have different patterns in different areas? For example, when both outings are affordable, appealing and equally practical, do you more often explore somewhere new or return to a place you know?',
}
assert {q['id'] for q in bank['questions']} == set(notes), ({q['id'] for q in bank['questions']}-set(notes),set(notes)-{q['id'] for q in bank['questions']})
assert {k for k,v in notes.items() if v[0]=='replace'} == set(rewrites)
rows=[]
for q in bank['questions']:
    disposition,reason=notes[q['id']]
    rows.append({'source_route_id':q['id'],'source_question':q['question'],
                 'source_planning_targets':q.get('planning_targets'),
                 'source_interpretation_limit':q.get('interpretation_limit'),
                 'disposition':disposition,'reason':reason,
                 'draft_id':'HYB0-'+q['id'] if q['id'] in rewrites else None,
                 'draft_question':rewrites.get(q['id']),
                 'automatic_old_facet_equivalence':False})
counts=dict(Counter(r['disposition'] for r in rows))
audit={'version':'hybrid-alignment-audit-v0-20261001','status':'development_candidate_not_runtime_authority',
       'source_path':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'route_count':len(rows),'dispositions':counts,'empirical_discrimination_established':False,
       'method':['Direct usual-pattern question first; a familiar example illustrates the same question, rather than covertly replacing it.',
                 'Examples are optional when the direct answer already resolves the distinction; do not ask for ritual confirmation.',
                 'Treat novelty seeking, desire for predictability, willingness to change for practical benefit, and home preference as distinct unless evidence connects them.',
                 'General self-reports remain self-reports. A detailed scenario is not independent corroboration or proof of a general trait.',
                 'A conditional answer can be informative. Ask a boundary or usual distribution only if it changes the inference; otherwise retain uncertainty and move on.',
                 'Every proposed item must face a strongest rational/constraint explanation and a counterexample from a person with an opposite putative trait.',
                 'Known older answers and corrections must be checked first. A new version number alone does not justify repeating a distinction.'],
       'routes':rows}
folder=Path(__file__).parent
(folder/'QUESTION-ALIGNMENT-AUDIT.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
intro='''# Life Patterns: question-to-objective alignment audit

**Status: development candidate, not a validated instrument and not silently activated.** Frozen v7 source files, mappings and historical records are unchanged. All 79 routes were individually reviewed. A disposition is an engineering/method judgment, not a population result.

## Main finding

The bank often measures a narrow, defensible response to one situation while the product is expected to reveal a recurring pattern. Correctly forbidding a broad inference does not make that narrow answer useful for the broader objective. Several prompts are also economical descriptions of sensible cost-benefit decisions; their answer variation may reflect the supplied constraint rather than the intended preference.

Some items already ask general recurring behavior and need no rewrite. Many others should remain conditional probes, not a questionnaire to administer in full. The hybrid candidate starts with the usual pattern, adds an example only to clarify its meaning, then asks a boundary only when it can change the interpretation. It does not force a new anecdote after an adequate direct answer.

## Why the earlier checks were insufficient

The attribution/quotation/absence fix lane tests source fidelity, not whether an item identifies a general tendency. The independent service reviews a supplied route under the bank's existing narrow authority; it does not independently redesign that authority on every turn. Earlier calibration did flag tautology and construct mismatch, but contract-presence checks and later implementation tests did not establish that those failures were absent from actual participant use. Exact-wording restrictions can preserve a weak question as faithfully as a good one.

No claim is made that most people empirically give the same answer: that requires response data. The audit identifies concrete logical alternatives and likely low-information cases for targeted participant pretesting. Approval by another model is not a substitute for those data.

## How to test the replacement

Use a small, versioned cognitive pretest, not another complete interview for somebody whose answers already exist. For each trial, check what the participant thought the question meant, whether the example changed that meaning, whether the answer changes the intended reading versus an ordinary rational baseline, and whether an existing answer already settled it. Preserve both direct and example answers when they diverge; do not let the example silently overrule the general report. Measure actual burden, redundancy, and answer usefulness before switching the production instrument.

'''
intro+='Disposition counts: '+', '.join(f'{k}: {v}' for k,v in counts.items())+'.\n\n'
for r in rows:
    intro+=f"## {r['source_route_id']} — {r['disposition']}\n\n**Current question:** {r['source_question']}\n\n**Current permitted scope:** {r['source_interpretation_limit']}\n\n**Finding:** {r['reason']}\n\n"
    if r['draft_question']:
        intro+=f"**Hybrid candidate ({r['draft_id']}):** {r['draft_question']}\n\nThis is a new development item. Its answer is not automatically equivalent to the old scenario's facet contract.\n\n"
(folder/'QUESTION-ALIGNMENT-AUDIT.md').write_text(intro.rstrip()+'\n')
short='''# Hybrid question trial — read existing answers first

Development wording only. Do not restart a completed interview, replace frozen v7 silently, or infer a broad trait from one example. These prompts are alternatives to test, not another mandatory checklist.

'''
for key in ['ROUTINE-CHANGE','G15','F0','D0','G18','G17','STATUS']:
    short+=f'## {key}\n\n{rewrites[key]}\n\n'
short+='''## Calendar tools

The old calendar route asks about practical switching costs. It should be an optional probe, not a temperament item. Do not turn "the new features are worth the effort" into adventurousness. For familiarity itself, a distinct candidate is: "When two approaches meet your needs equally well, how much does already knowing one of them matter to you, apart from the time or effort it saves? A tool you use is one example; another area may have a different pattern." This still does not measure a single adventure-versus-stability axis.

## Work-duration follow-ups

First establish which activity and which type of fatigue matter. Ask about short bursts or sustained weeks only if the respondent has not already established a meaningful duration difference and can answer realistically. Do not automatically administer three increasingly precise hypothetical schedules. A self-prediction is not an observed endurance measurement.
'''
(folder/'HYBRID-QUESTION-TRIAL.md').write_text(short)
print(json.dumps({'audited':len(rows),'counts':counts,'draft_replacements':len(rewrites)}))
