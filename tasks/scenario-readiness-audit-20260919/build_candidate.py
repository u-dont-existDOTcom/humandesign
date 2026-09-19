"""Materialize the reviewed text-only design; does not call a model or the app."""
from pathlib import Path
import argparse, json, hashlib

V='scenario-bank-v5.1-20260919'
BASE_SHA='dced7797a726003d7efd1feb928feb7ca6566d8a87dbe68bab8c43db4a87ab01'
# Each changed question still asks for only one response task.
PATCH={
'G19': 'You promised to help a friend sort things for a move, but it is taking longer than expected and using up time you had set aside for yourself. Your friend is open to changing the arrangement. What would matter most in deciding what to do?',
'G05': 'You suggest leaving an hour earlier for a group trip to avoid traffic, but the others would rather have more time in the morning. When you try to persuade people about a plan like this, how does it usually go?',
'G06': 'You have joined a group organising a shared meal. People are deciding how to divide the work, and nobody has asked you to take a role. What would you usually do?',
'R02': 'Consider the same shared-meal scene, except someone asks you to coordinate the work. What would you usually do?',
'G07': 'You find yourself starting an activity with someone you did not know before. In your own life, how do connections like that usually begin?',
'R03': 'In the scene where you offered one task and people expected you to handle the whole situation, what would you usually say when that became clear?',
'G02': 'You have worked out why two sets of plans for a trip do not agree. Someone else is trying to make sense of the same messages. What would you usually do next?',
'G03': 'There is a disagreement about how a shared plan went wrong, and you care about understanding it. You have to put the question aside to do something else. What usually happens to your attention in a situation like this?',
'G04': 'You are following a guide to set up something you want to use. Most of it works, but the same step keeps failing. What would you usually do next?',
'G22': 'You are reading something that holds your interest. Someone interrupts briefly, then leaves you free to continue. What usually happens to your concentration?',
'G09': 'Return to the cooking-class offer. Before you have weighed it up, what, if anything, would you usually notice in your body?',
'M10': 'While you consider that same choice, what usually happens to the bodily reaction you described?',
'G10': 'You join a group whose work interests you. They ask everyone to use a fixed schedule rather than choose their own working times. How would you usually respond?',
'M03': 'You agreed to prepare something for a shared meal. Finishing it is dull, and nobody is checking on you. What would you usually do?',
'M04': 'Return to that meal preparation. In this version, you still intend to finish, but tiredness is making you make mistakes. What would you usually do?',
'M09': 'You have a way of keeping track of your plans that still works reasonably well. A new tool has useful features, but switching would take some effort. What would matter in deciding whether to switch?',
'G13': 'Think of a romantic connection you would want to continue, whether familiar or clearly imagined. What, if anything, would usually help you feel closer as you spend more time together?',
'R09': 'Return to the workload you were describing. What, if anything, would tell you it was time for a break?',
'G24': 'Return to the friend-and-book scene. At an earlier stage of your life that you remember reasonably well, what would your usual reply have been?',
'G17': 'While planning a shared meal, someone gives a time that you believe is wrong. Nothing has been booked yet. What would you usually do?',
'G25': 'A close friend has twice agreed to help you with a practical task, then not turned up and explained only afterwards. What difference, if any, would that usually make to your trust?',
'AFTER-CHOICE': 'Once you have made that choice, what is it usually like to live with the decision?',
'PREFER-INFLUENCE': 'In the kind of discussion you just described, how much do you usually want to try to persuade the other person?',
'FOCUS-DEPTH': 'When you are reading something that holds your interest and are left uninterrupted, what is your concentration usually like?',
'SIGNAL-DEPENDABILITY': 'Across similar choices, how consistently do you notice a reaction like the one you described?',
'ADAPTATION': 'In that fixed-schedule group, what, if anything, would you be willing to change about your way of working?',
'ROOM-EFFECT': 'What difference, if any, would that condition make to how you feel or function in the room?',
'WORK-RECOVERY': 'After the kind of tiredness you described, what usually happens to your energy once you stop?',
'OWNERSHIP': 'Suppose a tool you find useful is reliably available whenever you need it, but it belongs to someone else. What, if anything, would make owning it yourself matter?',
'LIFE-PHASE': 'When in your life did the change you described become noticeable?'
}
# An explicit row for every inherited node: review judgment, not a generated PASS label.
NOTES={
'A0':'Retain the owner-preferred opening. Yes establishes an anticipated reply, not guilt, generosity, obligation or actually owning an enjoyable book.',
'G23':'Retain a noticing question. Notice only what the person names; no inference from an omitted detail. A care-responsibility probe needs a particular need or helping choice, not mere arrival.',
'G19':'Replace the unspecified shared project with a friend’s move; ask what matters rather than assume two enduring values. A stipulated time conflict is not the person’s chronic dilemma.',
'F0':'Retain a concrete utterance task. Noise preference is stipulated. Audience adaptation requires the answer to describe it; a polite reply alone does not establish strategic adaptation.',
'G05':'Add the actual disagreement: traffic versus morning time. The answer supplies self-rated outcomes, not objectively demonstrated persuasive ability.',
'M11':'Retain the shared-meal exchange. Unsure listeners may need information rather than pressure; asking what concerns them is a valid response. No pitch-quality score.',
'G06':'Specify a shared-meal role context. No role assignment is not the same as exclusion. Initiation, observation and offering bounded help remain possible.',
'R02':'Use the same response task as G06 and name the one changed condition. Compare two scoped answers, never credit a contrast from this answer alone.',
'G07':'Label as habitual recollection with an activity cue, not a fictional future event. No compulsory recent example or claim that an imagined connection proves past pathways.',
'G08':'Retain familiarity as the task. An unfamiliar scene may still be imagined, but cannot supply recurrence evidence.',
'R03':'Bind to the overextended-help scene, even after a topic switch. A hypothetical response stays hypothetical when familiarity was denied.',
'M07':'Retain optional activity-based self-history. Explicitly mark it a recollection task; no need for one recent episode. Accept no identified skill and do not impose talent.',
'M08':'Only after an actual named ability; repeat its name if nonadjacent. No request from others is not absence of ability.',
'G01':'Retain conflicting travel messages as a concrete organization task. Organization and checking accuracy are distinct; a rich reply can satisfy both.',
'G02':'Use the trip-message puzzle as the concrete problem. Helping another is offered, not compelled. An explanation is not automatically a reusable protocol.',
'G03':'Use a shared-plan puzzle as the default. If too inconsequential or unfamiliar, adapt to one question the respondent already regards as important, without demanding autobiographical proof.',
'R01':'Requires a reported return to an unresolved question. If they never return, suppress it; if they want to drop the topic, do not reopen it to obtain closure data.',
'G04':'Make the troublesome step concrete enough to answer. Seeking clarification, retrying and abandoning are as legitimate as inventing a method.',
'D0':'Retain language-practice scene. The stimulus supplies interest and repetition, not evidence that the respondent enjoys repetition or lacks discipline.',
'G22':'Use an explicit reading context. Resumption after interruption is not the same as depth, duration or stillness; do not infer those.',
'E0':'Retain the cooking-class choice. It asks the next step, not every stage of decision-making. A direct no or no uncertainty is valid.',
'G09':'Bind body question to the existing cooking-class scene instead of silently introducing another commitment. Ask only if the initial bodily response is genuinely missing.',
'R04':'Use only a reported bodily reaction, with source context. Perceived usefulness is not objective accuracy; do not ask after explicit no signal.',
'M10':'Distinguish within-choice duration/recurrence from consistency across choices. A passing feeling and later reasoning may coexist.',
'M05':'Retain a familiar-journey cue question. A checked fact, a feeling, a learned pattern or no warning are all admissible; no automatic intuition label.',
'M06':'Requires a named cue. This changes familiarity and yields an anticipated transfer limit, not observed performance in unfamiliar situations.',
'G10':'Specify fixed scheduling rather than an undefined way of working. A boundary here is not global self-direction across life.',
'G20':'Retain conditional spare-money motive. It does not establish actual wealth or life circumstances; spending choice may have several motives.',
'M03':'Ask what happens rather than what keeps following-through. The old task presupposed continuing; leaving, renegotiating and finishing now fit equally.',
'M04':'Bind to meal preparation; explicitly stipulate continued intention only in the variant. Do not back-fill commitment strength into M03.',
'C0':'Retain cancellation example, but narrow to its immediate reported reaction. Disappointment at missing a friend does not establish resistance to novelty.',
'G21':'Retain the free-day arrangement. It measures preferred rhythm under that freedom, not actual scheduling freedom or ability to sustain a routine.',
'M09':'Use an existing planning tool as concrete durable-value context. Switching cost and preserving value are separate reasons; do not equate staying with rigidity.',
'G11':'Retain room-attention question with no assumed defect. A named preference needs its own reported effect before crediting functioning.',
'G12':'Retain optional attraction task. Lack of attraction, no experience, privacy and imagined prediction remain different states.',
'G13':'Allow closeness not to deepen; retain the selected familiar/imagined and time frame rather than blending current and earlier relationships.',
'R05':'Retain increased-contact boundary, but do not use it as the sole route for every way a relationship may weaken; ROMANCE-FADE handles other relevant changes.',
'G14':'Retain alone-time affect baseline. No strong event in the scene does not imply emotional steadiness.',
'B0':'Retain repeated-worry scene. Irritation at repetition, concern and a mood shift are distinguishable; no emotional-contagion mechanism follows automatically.',
'R06':'Retain accusation during disagreement as a distinct context. Repair or reassurance behavior does not itself tell us the emotional response.',
'M01':'Retain urgency with unchanged deadline. Feeling hurried, speeding up and refusing the pressure remain separate reports.',
'M02':'Bind the same task and deadline. Suppress redundant probing when removal is already described; a missing aftermath is not automatically no aftermath.',
'G15':'Retain manageable meaningful work. Meaningfulness is the premise; do not count it as a discovered life purpose.',
'R07':'Reset from G15, not from a preceding overloaded scene. The requested endpoint is before rest; the offered rest does not supply recovery data.',
'R08':'Reset from G15 with duration/intensity/recovery difference explicitly stated. General tiredness here is not a distinctive trait or proof of limited work capacity.',
'R09':'Bind to the exact workload just reported. Stopping cues can exist without a bodily warning or good recovery.',
'G16':'Retain slow shared-space project. The participant can find it unimportant, decline or condition the answer on who benefits; no moral preference is supplied.',
'R10':'Treat joining as a new stated hypothetical premise. Do not imply that the person previously joined after saying no.',
'G18':'Retain the post-social evening. A chosen solitary activity is not by itself a need to withdraw; no forced retreat label.',
'R11':'Requires an explicitly reported period away; does not assume solitude, improvement or a desire to return.',
'G24':'Bind earlier-life comparison to the exact friend/book task and earlier answer; do not claim a real childhood event or a truer original personality.',
'R12':'Only after a reported change, asking its attributed contributors. Learned management is not established if the answer names a different cause.',
'G17':'Specify an incorrect time in meal planning. Its consequences may need clarification; a correction is not automatically perfectionism.',
'G25':'Specify the kind of broken agreement. Distinguish reliability on that task from global distrust, affection and safety judgments.',
'R13':'Bind to that friend and the reported dimension of reliance. Never assume reconciliation is desired or a refusal needs another probe.',
'WHY':'Keep the open reason probe, adapted to the actual action. Its targets are possibilities, not automatic responsibility/value credit.',
'AFTER-CHOICE':'Remove the assumption that an opposite pull persists. Relief, regret, mixed feelings and nothing further remain possible.',
'PREFER-INFLUENCE':'Remove the condition that agreement is unnecessary, which made low motivation unsurprising. Ask inclination in the same persuasion context whose capacity was discussed.',
'OUTREACH':'Only when someone wants an opportunity or connection; lack of new contacts does not entail an unmet wish or need for outreach.',
'VERIFY':'Retain accuracy probe only if organization was supplied without checking. Do not repeat the person’s already-stated verification method.',
'WORKING-METHOD':'Name the adequate-method variant. Do not turn reasonable adjustment of a failing guide into an originality trait.',
'PRACTICE-REASON':'Only after a practice choice with missing value. For declining use an open action-matched reason, not why practice would be worthwhile.',
'FOCUS-DEPTH':'Bind to uninterrupted reading; permit ordinary concentration, drift or time-limited focus without forcing an immersive state.',
'CHOICE-TIME':'Only while the choice remains considered or an unresolved clarity question matters. Distinguish procedural waiting from feeling clearer.',
'SIGNAL-DEPENDABILITY':'Ask cross-choice noticing consistency rather than repeat R04’s usefulness-as-guide question. Notice rate and perceived accuracy are different.',
'SIGNAL-NOT-FOLLOWED':'Only after a reaction is reported. Ask override conditions without recommending obedience to a bodily cue.',
'ADAPTATION':'Bind the accepted fixed-schedule premise; do not ask again if accommodation and limits were already supplied.',
'ROOM-EFFECT':'Specify the named condition and permit no effect. A room preference does not establish impaired functioning.',
'PHYSICAL-CLOSENESS':'Optional, chosen romantic context only. Physical affection must not substitute for desire, sensuality as a whole or someone else’s behavior.',
'MOOD-AFTER':'Bind to the exact earlier emotional reaction, not whichever conversation happened most recently. Requires an actual reported mood change.',
'WORK-RECOVERY':'Ask what happens after stopping rather than assume an effective recovery aid or prompt return of energy.',
'STATUS':'Retain equal-practical-benefit contrast; prestige, being understood and pressure from visibility are distinct possible responses.',
'OWNERSHIP':'State reliable access so availability is not the main missing premise. Control, legal restrictions or security concerns are still valid assumptions to record, not personality labels.',
'LIFE-PHASE':'After a reported change, ask timing rather than repeat whether change happened. No calendar dates or exact ages required.',
'CORRECTION-REASON':'Retain threshold probe only when the action does not already explain stakes, relationship, confidence or cost.'
}
FAMILIES={
'friend_company':['A0','WHY'], 'shared_meal_needs':['G23','CARE-RESPONSIBILITY','CARE-LIMIT'],
'competing_commitments':['G19','AFTER-CHOICE'], 'persuasion':['F0','G05','PREFER-INFLUENCE'],
'value_exchange':['M11'], 'group_entry':['G06','R02'], 'connections':['G07','OUTREACH'],
'excess_expectations':['G08','R03'], 'ability':['M07','M08'],
'understanding':['G01','VERIFY','G02','G03','R01'], 'method':['G04','WORKING-METHOD'],
'practice_focus':['D0','PRACTICE-REASON','G22','FOCUS-DEPTH'],
'choice':['E0','CHOICE-TIME','G09','R04','M10','SIGNAL-DEPENDABILITY','SIGNAL-NOT-FOLLOWED'],
'risk_cues':['M05','M06'], 'external_role':['G10','ADAPTATION'],
'resources':['G20','STATUS','OWNERSHIP'], 'promise':['M03','M04'],
'rhythm_change':['C0','G21','ROUTINE-CHANGE','M09'], 'surroundings':['G11','ROOM-EFFECT'],
'romance':['G12','G13','R05','ROMANCE-FADE','PHYSICAL-CLOSENESS'],
'emotion':['G14','B0','R06','MOOD-AFTER'], 'urgency':['M01','M02'],
'work_energy':['G15','R07','R08','R09','WORK-RECOVERY'],
'purpose':['G16','R10'], 'retreat':['G18','R11'],
'development':['G24','LIFE-PHASE','R12'], 'correction':['G17','CORRECTION-REASON'],
'trust':['G25','R13']}
PARENTS={
'R02':['G06'], 'R03':['G08'], 'M08':['M07'], 'R01':['G03'], 'G09':['E0'],
'R04':['G09'], 'M10':['G09'], 'M06':['M05'], 'M04':['M03'],
'R07':['G15'],'R08':['G15'],'R09':['G15','R07','R08'],'R10':['G16'],
'R11':['G18'],'G24':['A0'],'R12':['G24','LIFE-PHASE'],'R13':['G25'],
'WHY':['A0','G23','G19','M03','D0'], 'AFTER-CHOICE':['G19'],
'PREFER-INFLUENCE':['F0','G05','M11'],'OUTREACH':['G07'],'VERIFY':['G01'],
'WORKING-METHOD':['G04'],'PRACTICE-REASON':['D0'],'FOCUS-DEPTH':['G22'],
'CHOICE-TIME':['E0'],'SIGNAL-DEPENDABILITY':['G09'], 'SIGNAL-NOT-FOLLOWED':['G09'],
'ADAPTATION':['G10'],'ROOM-EFFECT':['G11'],'PHYSICAL-CLOSENESS':['G13'],
'MOOD-AFTER':['B0','R06'],'WORK-RECOVERY':['G15','R07','R08'],'STATUS':['G20'],
'OWNERSHIP':['G20'],'LIFE-PHASE':['G24'],'CORRECTION-REASON':['G17']}
ADDITIONS=[
('CARE-RESPONSIBILITY','In that situation, what, if anything, would you feel responsible for?',['D23.responsibility'],['A0','G23'], 'A particular need or helping choice has been named, and personal responsibility is still unclear. Enjoying company alone is not a reason to search for guilt.'),
('CARE-LIMIT','What, if anything, would make you leave that help to someone else?',['D23.withholding'],['G23','CARE-RESPONSIBILITY'],'A particular form of help is under discussion; the limit has not been supplied. No answer is required if the topic is closed.'),
('ROUTINE-CHANGE','You have a free afternoon. You could go somewhere familiar that you enjoy, or try a new place that also appeals to you. Both are practical today. What would usually matter in choosing?',['D21.novelty_disruption'],['G21'],'Optional alternative to inferring novelty preference from a disappointing cancellation; record the particular comparison, not a global trait.'),
('ROMANCE-FADE','In the romantic connection you are considering, what, if anything, would usually make you feel less close over time?',['D12.weakening_boundaries'],['G13'],'Use only in an applicable or elected imagined romantic context that remains welcome. Do not infer fading from more or less frequent contact alone.')]

def build(source:Path,out:Path):
 data=source.read_bytes()
 if hashlib.sha256(data).hexdigest()!=BASE_SHA: raise ValueError('Source bank differs from reviewed exact version')
 old=json.loads(data); qs=old['questions']
 if set(NOTES)!={q['id'] for q in qs}: raise ValueError('Incomplete node-by-node review')
 result=[]; audits=[]
 for q0 in qs:
  q=json.loads(json.dumps(q0)); i=q['id']; q['revision']=V
  q['question']=PATCH.get(i,q['question']); q['family']=next(k for k,v in FAMILIES.items() if i in v)
  q.pop('parent',None)
  q['context_sources']=PARENTS.get(i,[])
  q['context_requirement']='one actual matching antecedent; a claimed comparison requires both scoped answers'
  if i in ['G09','R09']: q['kind']='bound_probe'
  q['context_binding_rule']='Bind to one exact presented scenario and its actual answer. Re-name the scene or repeat its conditions when nonadjacent. IDs alone are not semantic evidence.'
  q['interpretation_limit']=NOTES[i]
  q['automatic_evidence_credit']=False
  q['admission']='INTERVIEW-PROTOCOL.md global admission AND: '+q['admission']
  if i in ['G07','M07']: q['kind']='habitual_or_developmental_recollection'
  if i=='G24':q['kind']='optional_retrospective'
  if i=='C0': q['planning_targets']=[]
  if i=='R02':q['admission']+=' The entry comparison requires the original G06 answer and the variant answer; ask the same action task.'
  if i=='PREFER-INFLUENCE':q['admission']+=' Desire is asked under the original stakes, not after removing any need to persuade.'
  if i=='OUTREACH':q['admission']+=' A wanted activity or connection is known; otherwise do not assume a social deficit.'
  if i=='CHOICE-TIME':q['admission']+=' Do not presume continued deliberation after an already settled choice.'
  if i=='G09':q['admission']+=' Recover E0 or a respondent-supplied equivalent explicitly before asking; never invent a different commitment.'
  if i=='M10': q['admission']+=' Requires the particular bodily reaction, not merely any decision reaction.'
  if i=='WHY':q['planning_targets']=[]
  audits.append({'id':i,'old_question':q0['question'],'question':q['question'],'wording_changed':q['question']!=q0['question'],'judgment':NOTES[i],'resolved_by':'wording and explicit context/admission/evidence rules; see actual question above'})
  result.append(q)
 for i,text,targets,parents,guard in ADDITIONS:
  result.append({'id':i,'revision':V,'question':text,'kind':'optional_probe' if i!='ROUTINE-CHANGE' else 'scene','planning_targets':targets,'family':next(k for k,v in FAMILIES.items() if i in v),'context_sources':parents,'context_binding_rule':'Bind to the indicated scene and actual answer, not the last utterance by position.','automatic_evidence_credit':False,'admission':'INTERVIEW-PROTOCOL.md global admission AND: '+guard,'interpretation_limit':guard+' The answer supports only what it says; the prompt never fills a response field.'})
 bank={'version':V,'status':'text-only design candidate; not a deployed runtime','intro':'Imagine yourself as you usually are in situations like these. Tell me what you would probably do or feel, rather than the ideal answer. If something important changes your answer, say so. You can change a scene that does not fit, skip a question, or stop. A remembered example is welcome, not required.','node_count':len(result),'required_question_count':None,'families':FAMILIES,'planning_rule':'Routes are opportunities to ask, not evidence or compulsory quotas. Credit only scoped, source-linked meaning. Declined/inapplicable/unknown are preserved, not passed.','questions':result}
 out.mkdir(parents=True,exist_ok=True)
 (out/'interviewer-bank-v5.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
 for q in result:
  if q['id'] not in NOTES:
   audits.append({'id':q['id'],'old_question':None,'question':q['question'],'wording_changed':False,'new_optional_route':True,'judgment':q['interpretation_limit'],'resolved_by':'Explicit optional route with antecedent and no automatic evidence credit; no mandatory question count.'})
 (out/'NODE-AUDIT.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n')
 lines=['# Scenario-first interview — reviewed question bank v5','',bank['intro'],'','This is a menu of scenes and conditional questions, not a 79-question form. Show only the selected question. Apply INTERVIEW-PROTOCOL.md before every question. There are no model/chart labels or answer keys for participants.','']
 lookup={q['id']:q for q in result}
 for family,ids in FAMILIES.items():
  lines+=['## '+family.replace('_',' ').capitalize(),'']
  for i in ids:
   q=lookup[i];lines += ['### '+i,'',q['question'],'','*Use only when:* '+q['admission'],'']
 (out/'SCENARIO-BANK-v5.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'inherited_nodes_reviewed':len(qs),'changed_wording':sum(x['wording_changed'] for x in audits),'new_optional_routes':len(ADDITIONS),'available_nodes':len(result)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.source,a.output)
