"""Materialize the Chat-authored second-pass review; no model or runtime calls."""
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);SRC=p.parse_args().source_dir
ROOT=Path(__file__).resolve().parent
old=json.loads((SRC/'pilot/interviewer-bank.json').read_text())
req=json.loads((SRC/'study/requirements-v2.json').read_text())
rows='''A0|narrow+probe|Action is not motive, responsibility or durable value tension. Use WHY only when reason is missing; keep all motives the respondent supplies.
G23|keep|What attracts attention does not measure speed of noticing or establish willingness to help. Preserve only noticed features.
G19|narrow+probe|The stimulus supplies a conflict, not evidence of a chronic inner conflict. A decision procedure does not establish whether the tension ends.
F0|narrow+probe|Noise aversion is stipulated, not discovered. A reply describes communication here, not persuasion skill or general preference.
G05|rewrite|An unspecified practical change leaves audience and stakes open. Self-rated effectiveness remains self-report, not observed ability.
M11|rewrite|An unspecified useful offer asks the respondent to invent the core situation. Demonstrating a sales pitch does not establish enjoyment of persuading.
G06|narrow|Entry behavior in a new group does not establish general leadership or cross-context consistency. The requested role is a later variant.
R02|variant|Invitation changes one important condition. Treat as a named imagined contrast, not proof the respondent actually received recognition.
G07|rewrite+probe|A future opportunity is not an observed pathway. Ask habitual source with a scene cue and ask deliberate outreach only if still missing.
G08|keep|Familiarity can support a reported recurrence or lack of experience, not proof of a projection field or actual skill.
R03|mode_guard|A hypothetical response to unfamiliar expectations is allowed only as imagined behavior; never count it as an experienced mismatch.
M07|narrow|A learned skill is not automatically natural talent. Retain ease, instruction and practice separately when reported.
M08|guard|Needs a participant-named ability. Nobody asking is valid; recognition and competence are not interchangeable.
G01|keep+probe|Organizing messages is not automatically checking their accuracy. Probe verification only when needed and not already explained.
G02|rewrite|What would you give them presupposes sharing and a deliverable. Permit no intervention, private insight, speech, example, or a reusable artifact.
G03|keep|A thought returning under a specified important problem is not population rarity, existential drive or exact frequency.
R01|guard|Only ask what ends recurrence after recurring attention is reported. Putting a thought down successfully needs no closure interrogation.
G04|narrow+variant|Fixing a repeatedly failing instruction is not evidence of an independent drive to invent. Include a working-method contrast only when useful.
D0|narrow+probe|Choosing practice today does not establish intrinsic enjoyment of repetition. Keep motivation and persistence separate.
G22|narrow+probe|The stimulus already says absorbed. Resumption after interruption does not establish usual depth, duration or stationary-focus preference.
E0|narrow+probe|Checking facts or deciding tomorrow is not itself a report of changing clarity. Allow immediate clarity and stable uncertainty.
G09|keep|Any bodily sensation may be nondiagnostic. None is a valid answer; bodily language is an explicit topic, not proof of an HD authority.
R04|narrow+guard|Usefulness, across-occasion dependability and conditions of override are distinct. Do not credit all from one generic statement.
M10|guard|Needs a reported bodily reaction in the same frame. Its within-choice time course is distinct from cross-choice repeatability.
M05|rewrite|The old scene asserted early detection before reasoning. New scene permits no cue and cues noticed during deliberate checking.
M06|guard|Only reuse a cue actually described. Familiar versus unfamiliar is a hypothetical boundary probe, not measured calibration.
G10|rewrite+probe|Least willing to give up demands an invariant and a morally admirable boundary. Permit flexible direction and ask what changes separately.
G20|narrow+probe|Spending priorities alone do not establish status or ownership motives. Do not infer anti-status from silence about status.
M03|keep|A self-predicted response to a promise is not observed reliable will. Not finishing and renegotiation remain valid.
M04|variant|Continuing intention is a stipulated variant, not an inference from M03. Keep wanting to finish separate from physical capacity.
C0|narrow|Disappointment about losing company need not be dislike of novelty. Keep cancellation response narrow; do not generalize to all change.
G21|keep|A day the person controls does not describe an imposed work schedule. Both flexible and structured arrangements can be intentional.
M09|keep|Familiarity, retained value, sunk cost and replacement costs are possible distinct reasons; do not supply them as an answer list.
G11|rewrite+probe|The room lacks details and the old prompt forces a defect and a modification. First ask what they attend to; obtain function separately.
G12|mode_guard|Allow no attraction, no opportunity, privacy or imagined-only response. Do not silently infer orientation, a partner or general absence of intimacy.
G13|mode_guard+probe|Depth of closeness is not automatically physical affection or sexual desire. Keep current, historical and imagined relationship frames separate.
R05|mode_guard|More contact is a contrast, not proof of dependence. Use the same chosen relationship frame; absence of current romance is not a defect.
G14|keep|No recent major event does not mean the person is calm. Do not infer their solo baseline from the settled premise in B0.
B0|keep+guard|Settled starting mood and partner worry are stimuli. Their effect, if any, is reportable; no contagion mechanism is established.
R06|rewrite+probe|The old prompt asked only after conflict but claimed both during-conflict effect and recovery. Ask the current effect, then aftermath only if missing.
M01|keep|External urgency is stated. An internal reaction is optional; no reaction is not hidden pressure needing to be uncovered.
M02|guard|Removal of external pressure can be imagined, but an absent internal response needs no presumed recovery question.
G15|keep|After-work energy under a manageable workload is not infinite stamina. Allow part-day or nonemployment equivalents with adaptation recorded.
R07|variant|Change intensity and duration explicitly; do not turn the chance to rest into evidence that recovery actually happened.
R08|variant|Too much work without recovery bakes in overload. Record the response but do not label an ordinary depletion response distinctive.
R09|rewrite+probe|Continuing is no longer useful can refer to project value rather than a stopping signal. Stopping signals and recovery need distinct support.
G16|rewrite|An unspecified difficult project lacks stakes. Supply an ordinary shared-space task; do not assume the respondent values it or accepts it.
R10|variant|Prior investment is a named counterfactual, not a fabricated past event. Refusing the initial project does not prove inconsistency.
G18|keep|A next activity does not by itself reveal how much retreat is needed. No withdrawal and more social contact are valid responses.
R11|guard|Requires downtime or withdrawal reported in this frame. Do not manufacture a re-entry problem where none was described.
G24|narrow+guard|One earlier-versus-now comparison cannot establish a whole developmental phase map. No change and uncertain recall are valid.
R12|rewrite+guard|The old wording presupposes learning and improvement. Ask what contributed only after a change is described, including deterioration or constraints.
G17|narrow+probe|Correcting one error does not establish the threshold or cost conditions. Probe the missing reason without defining the error as dangerous.
G25|keep|Trust can remain stable, become conditional or decrease. The scenario is not an actual betrayal or a relationship diagnosis.
R13|rewrite+guard|Before relying again assumes lost trust and a wish to restore it. Permit no repair, limited access and no change without pushing reconciliation.'''
audit={}
for line in rows.splitlines():
 i,action,note=line.split('|',2);audit[i]={'id':i,'disposition':action,'finding_and_limit':note}
assert set(audit)=={q['id'] for q in old['questions']}
rewrites={
'G05':"You think a group trip would work better if everyone left an hour earlier, but the others would rather keep the original time. When you make a case like this, how does it usually go?",
'M11':"You offer to organise a shared meal if someone else buys the ingredients. They are interested but unsure about the arrangement. How would you explain your proposal?",
'G07':"Imagine starting a worthwhile new activity with someone you did not know well before. In your own life, how do connections like that usually begin?",
'G02':"You have worked out why a familiar practical problem keeps happening. Someone else is running into the same problem. What would you usually do next?",
'M05':"You are checking the arrangements for a kind of journey you know well. What, if anything, would alert you that something was not right?",
'G10':"You join a group that does worthwhile work, but it expects everyone to follow a set way of working that differs from yours. How would you usually respond?",
'G11':"You will be using an unfamiliar room for work or a quiet activity for a week. What would you pay attention to before settling in?",
'R06':"During a disagreement, someone close to you says that you do not care about them. What, if anything, would usually happen to your mood during that conversation?",
'R09':"During work like this, what would tell you that you need a break?",
'G16':"A local group asks you to spend several weekends restoring a neglected shared space. The work will be slow and receive little recognition. What would determine whether it was worth the effort to you?",
'R12':"What do you think contributed to that change?",
'R13':"What, if anything, could change how much you rely on that friend afterwards?",
'M04':"For this version, suppose you still intend to deliver what you promised, but tiredness is making the work unreliable. What would you probably do?",
'R10':"For this version, suppose you chose to join the project and have put a month into it, but progress is poor. What would make you stop investing in it?",
'R11':"After the kind of time away you described, what, if anything, usually signals that you are ready to engage with people again?"
}
direct={'A0':[],'G19':['D18.competing_values'],'F0':['D05.audience_adaptation'],'G06':['D06.entry_signal'],'G07':['D07.usual_source'],'G01':['D01.approach'],'G02':['D02.output_form','D02.audience_use'],'G04':['D04.use_existing'],'D0':[],'G22':['D22.focus_depth_interruptions'],'E0':[],'R04':['D09.repeatability_trust'],'G10':['D10.stable_direction','D10.external_adaptation'],'G20':['D19.resources_purpose'],'G11':['D11.conditions'],'G24':['D20.continuity'],'R06':['D13.conflict_effect'],'R09':['D14.stopping_recovery'],'M11':['X08.offer_and_leverage'],'C0':['D21.novelty_disruption'],'G17':['D16.challenge_threshold']}
gates={'M08':'A specific ability has been named by the respondent.','R01':'G03 or another cited answer reports recurring attention to the same question.','R04':'A bodily/felt reaction is reported; its usefulness is not already described.','M10':'A bodily/felt reaction is reported; its within-choice time course is missing.','M06':'A cue is reported in M05; distinguish familiar experience from an unfamiliar prediction.','R11':'A need for time away or a return after withdrawal is actually reported.','R12':'A current-versus-earlier change is reported. Do not presume learning or improvement.','R13':'Changed reliance or trust is reported and the person has not already closed the topic.','M02':'An internal response to external pressure is reported and aftermath remains unknown.'}
variant={'R02','R07','R08','M04','R10'};frame={'G12','G13','R05','B0'};questions=[]
for q in old['questions']:
 i=q['id'];a=audit[i]
 nq={'id':i,'revision':'scenario-bank-v4-20260919','question':rewrites.get(i,q['question']),'kind':'matched_variant' if i in variant else 'conditional_followup' if i in gates else 'context_optional' if i in frame|{'R03','G24'} else 'scene','planning_targets':direct.get(i,q['neutral_information_targets']),'admission':gates.get(i,'The scene fits or the respondent knowingly chooses to imagine it; target information remains useful and unanswered.'),'interpretation_limit':a['finding_and_limit']}
 if i=='R03':nq['admission']='Use an experienced mismatch if reported; otherwise explicitly ask only as a knowingly imagined variant. Do not relabel it as familiar.'
 if i=='G24':nq['admission']='A current response is known and an earlier-life comparison is useful and welcome. Earlier recall is optional and need not be exact age five.'
 if i in frame:nq['admission']='A romantic/partner context is applicable, or the respondent explicitly chooses a past or imagined version; preserve that frame. A friend substitution is a different context.'
 if i in variant:nq['admission']='Introduce the changed premise as a hypothetical variant, not as something the person did. Do not repeat an already supplied comparison.'
 a['wording_changed']=i in rewrites;a['old_question']=q['question'];a['new_question']=nq['question'];questions.append(nq)
probe_rows=[
('WHY','A0','What would make you say yes?',['D23.responsibility','D23.withholding','D18.competing_values'],'A concrete action is supplied without the reason and the reason would change the description. Adapt yes to the action stated; no motive menu.'),
('AFTER-CHOICE','G19','Once you have made that decision, what, if anything, still pulls you in the other direction?',['D18.resolution_durability'],'Both competing concerns were reported; their persistence after the choice is missing.'),
('PREFER-INFLUENCE','G05','When you do not need their agreement, how much do you want to spend time persuading them?',['D05.preferred_use','X08.preferred_use'],'Capacity or a pitch was discussed, but desire to use it remains unknown; no assumed dislike of persuasion.'),
('OUTREACH','G07','When no new connection comes your way, what would you usually do?',['D07.deliberate_pathways'],'Habitual opportunity sources are known but deliberate creation of opportunities is not.'),
('VERIFY','G01','How would you decide which of the conflicting details to rely on?',['D01.checking_detail'],'The respondent described organising information without already resolving its accuracy.'),
('WORKING-METHOD','G04','In this version, the guide works adequately for your task. What would you usually do with the method then?',['D04.change_threshold'],'An ordinary-method contrast is useful; mark it as a changed scene rather than a new experience.'),
('PRACTICE-REASON','D0','What would make that practice worth doing for you?',['D22.repetition_value'],'The respondent would practise but has not said what makes it rewarding or worthwhile. For not practising, use WHY adapted to that action.'),
('FOCUS-DEPTH','G22','With that activity and no interruption, what is it usually like when your attention is fully engaged?',['D22.focus_depth_interruptions'],'Resumption is known but depth or duration is not; do not demand a number or infer immobility.'),
('CHOICE-TIME','E0','As you keep considering that choice, what, if anything, usually changes in how clear it feels?',['D09.clarity_over_time'],'A decision procedure is known but its time course is missing. No change and remaining unsure are allowed.'),
('SIGNAL-DEPENDABILITY','R04','Across similar choices, how consistent is that reaction as a guide for you?',['D09.repeatability_trust'],'A reaction exists; across-occasion consistency is missing. Self-rated usefulness is not proven accuracy.'),
('SIGNAL-NOT-FOLLOWED','R04','What, if anything, would make you set that reaction aside?',['D09.override_state'],'A reaction exists and override conditions are not already reported. Never imply it should be obeyed.'),
('ADAPTATION','G10','What about their way of working would you be willing to take on?',['D10.external_adaptation'],'A limit was described but adaptation was not; none is allowed. Ask the complementary boundary only if missing, not to manufacture resistance.'),
('ROOM-EFFECT','G11','What difference would that make to how you function there?',['D11.functional_effect'],'The respondent named an environmental condition or change; its effect is missing.'),
('PHYSICAL-CLOSENESS','G13','In that relationship, what place, if any, would physical affection have for you?',['D12.sensuality'],'The chosen romantic context is applicable or knowingly imagined and the person is comfortable with the topic. No touch or no wish for physical intimacy is valid; touch and sexual desire remain separate.'),
('MOOD-AFTER','R06','Once that conversation is over, what usually happens to the feeling you described?',['D13.recovery'],'A mood reaction was reported; aftermath is missing. Do not assume that it fades or that distance causes the change.'),
('WORK-RECOVERY','R09','After you stop, what usually helps your energy return?',['D14.stopping_recovery'],'Energy depletion was reported and recovery is unanswered. No reliable recovery is valid; a rational stopping decision is not itself depletion.'),
('STATUS','G20','Suppose the practical benefits of what you do stay the same, but other people begin seeing it as more impressive. What difference, if any, would that make to you?',['D19.status_ownership'],'Status value remains unknown; do not infer motive from whether money was spent on tools.'),
('OWNERSHIP','G20','You could have a useful tool available whenever you need it without owning it. What, if anything, would make owning it matter to you?',['D19.status_ownership'],'Ownership motivation remains unknown; record practical concerns rather than treating them as status motives.'),
('LIFE-PHASE','G24','Thinking about this same kind of situation, was there a period when your usual response changed noticeably?',['D20.phases'],'Earlier-versus-current continuity was discussed, but timing of a reported change is unclear. No change and approximate life periods are valid; do not request birth dates.'),
('CORRECTION-REASON','G17','What would matter most in deciding whether to point it out?',['D16.context_cost','D16.challenge_threshold'],'Action alone was given and its threshold is unclear. Do not specify harm, politeness or perfectionism for the person.')]
for i,parent,text,targets,admission in probe_rows:
 questions.append({'id':i,'revision':'scenario-bank-v4-20260919','question':text,'kind':'optional_probe','parent':parent,'planning_targets':targets,'admission':admission,'interpretation_limit':'One optional question at a time; an answer supports only the parts it actually states. Parent association is a suggested location, not permission to repeat answered information.'})
parts={'D09.repeatability_trust':['across-occasion consistency','self-reported usefulness or trust'],'D09.override_state':['conditions of override','state dependence if reported'],'D22.focus_depth_interruptions':['depth or duration of engagement','effect of interruption and resumption'],'D14.stopping_recovery':['stopping cues','restoration after depletion'],'D19.status_ownership':['social status or recognition motive','ownership or control motive'],'D20.phases':['reported change or explicit continuity','time frame at the precision actually known'],'D23.responsibility':['whether an obligation is felt','what creates or limits that obligation'],'D23.withholding':['choice not to intervene or a stated limit','conditions attached to that choice'],'D12.sensuality':['physical affection preference','sexual desire only if explicitly reported; do not substitute affection'],'D13.recovery':['aftermath of a reported emotional change','time course or recovery condition if known'],'X05.ease_and_learning':['initial ease if known','practice or instruction reported'],'X08.offer_and_leverage':['how value is presented','adaptation to the other person if reported']}
facets=[]
for d in req['domains']:
 for f in d['facets']:
  routes=[q['id'] for q in questions if f in q['planning_targets']]
  facets.append({'facet_id':f,'domain':d['title'],'parts_to_keep_distinct':parts.get(f,[f.split('.',1)[1].replace('_',' ')]),'candidate_routes':routes,'status':'planned_not_empirically_verified','claim_rule':'Credit only a source-linked statement at its actual scope; missing parts remain missing. The question, premise, target and prior fixture labels are not evidence.'})
assert len(facets)==73 and all(f['candidate_routes'] for f in facets)
policy={'version':'scenario-bank-v4-20260919','status':'design candidate; pilot paused; not app implementation','source_pilot_commit':'1278520fa6fe334845ffd8c22d625d3c924d33d2','intro':old['intro'],'routing_policy':[
'Read the whole actual answer before selecting anything. Preserve spontaneously supplied reasons, feelings and conditions.',
'A bare action may warrant one open reason probe; do not presume wanting, guilt, duty, caring or avoidance.',
'Use a reaction-dependent follow-up only after a matching reaction is reported. A no-reaction report is not an unknown reaction.',
'An explicitly named hypothetical variant may stipulate a new premise, but never convert it into biography or observed change.',
'A declined, inapplicable or paused topic cannot be reopened just because a planning facet remains empty.',
'Repair a confusing or under-specified question before interpreting its answer. Do not code process feedback as a trait.',
'Retain within-person variation and mixed motives; do not seek a single correct personality answer.',
'A supported-part record is not a whole compound facet. These 73 locators are planning aids, not a response quota.',
'Pause stays paused until the owner elects to resume; save received records privately before claiming they are saved.'],
'question_count':len(questions),'core_candidate_count':55,'optional_probe_count':len(probe_rows),'new_wording_human_tested':False,'independent_semantic_review':False,'questions':questions}
for name,obj in [('interviewer-bank-v4.json',policy),('question-audit.json',list(audit.values())),('coverage-plan-v4.json',{'scope':'all 73 inherited planning facets; no claim all required information is elicited','facets':facets})]: (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
lines=['# Revised scenario bank — second review','', 'Design candidate v4. The pilot is paused. The 55 original nodes and 20 optional probes below are a bank, not a fixed 75-question interview. No claim of shorter burden or new semantic validity is made.','',policy['intro'],'','Do not show interpretation notes or coverage labels to the respondent.']
for q in questions: lines +=['',f"## {q['id']}",q['question'],'',f"Admission: {q['admission']}",'',f"Interpretation limit: {q['interpretation_limit']}"]
(ROOT/'SCENARIO-BANK-v4.md').write_text('\n'.join(lines)+'\n')
lines=['# Full question audit','', 'All 55 incoming question nodes inspected against wording, answer dependence, framing and interpretation. These are same-context design judgments, not an independent re-score of all fictional answers.','', '| Node | Disposition | Finding / repair boundary |','|---|---|---|']
for a in audit.values():lines.append(f"| {a['id']} | {a['disposition']} | {a['finding_and_limit']} |")
(ROOT/'QUESTION-AUDIT.md').write_text('\n'.join(lines)+'\n')
(ROOT/'source-interviewer-bank.json').write_bytes((SRC/'pilot/interviewer-bank.json').read_bytes())
(ROOT/'source-requirements-v2.json').write_bytes((SRC/'study/requirements-v2.json').read_bytes())
print(json.dumps({'reviewed':len(audit),'rewritten':len(rewrites),'optional_probes':len(probe_rows),'facets':len(facets)}))
