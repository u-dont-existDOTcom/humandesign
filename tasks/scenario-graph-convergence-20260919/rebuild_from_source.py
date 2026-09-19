"""Build a review index for the frozen questionnaire; not an interview runtime."""
from pathlib import Path
import json, hashlib, copy, re
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'source'; OUT=ROOT
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n' if not isinstance(obj,str) else obj,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bank=json.loads((SRC/'interviewer-bank-v5.json').read_text()); original=copy.deepcopy(bank)
by={q['id']:q for q in bank['questions']}
changes=[]
def change(qid,field,value,finding):
    old=by[qid].get(field)
    if old!=value:
        changes.append({'id':qid,'field':field,'before':old,'after':value,'finding':finding})
        by[qid][field]=value
change('G04','question','You are following instructions to set up a shared calendar on your phone. Most steps work, but the step for inviting another person keeps failing. What would you usually do next?','F01')
change('R08','question','Return to the worthwhile work at a manageable pace. In this version, the workload stays too heavy for several weeks, without enough recovery. What would your energy usually be like at the end of that period?','F02')
change('M02','context_sources',['M01'],'F03')
# A reference can supply context without being a mandatory preceding question.
standalone=set(q['id'] for q in bank['questions'] if not q['context_sources'])|{'ROUTINE-CHANGE','STATUS','OWNERSHIP'}
for qid in sorted(standalone):
    change(qid,'context_requirement','Self-contained starting scene or report cue; no prior participant answer is required. Apply usefulness, applicability, privacy and pause rules. Any topic-related context links are advisory, not prerequisites.','F04')
# These are interpretation demonstrations, never revised participant observations.
evidence=json.loads((SRC/'EVIDENCE-REVIEW.json').read_text()); old_evidence=copy.deepcopy(evidence)
for e in evidence:
    if e['facet_id']=='D05.audience_adaptation':
        e['fictional_answer']="With these friends I'd mention not being able to hear each other; with my family I'd emphasise having time to talk."
        e['revision_note']='F05: newly authored illustration aligned with F0 noise/meeting scene; historical evidence and transcripts remain unchanged.'
bank['version']='scenario-bank-v6.0-20260919'
bank['status']='Graph-organized text-only candidate; no application implementation'
for q in bank['questions']:q['revision']=bank['version']
write('interviewer-bank-v6.json',bank)
write('EVIDENCE-GUIDE-v6.json',evidence)
write('CHANGES.json',{'source_version':original['version'],'candidate_version':bank['version'],'question_edits':[x for x in changes if x['field']=='question'],'context_repairs':[x for x in changes if x['field']!='question'],'illustration_edits':['D05.audience_adaptation'],'source_transcripts_changed':False})
# Human-reviewed predicate vocabulary. Inputs are explicitly annotated states, not parsed text.
guards={
 'WHY':('action_reason',['reported_action','reason_missing']),
 'CARE-RESPONSIBILITY':('help_responsibility',['specific_need_or_help','responsibility_missing']),
 'CARE-LIMIT':('help_limit',['specified_help','help_limit_missing']),
 'AFTER-CHOICE':('competing_concerns',['both_concerns_reported','aftermath_missing']),
 'PREFER-INFLUENCE':('inclination',['influence_context','inclination_missing']),
 'OUTREACH':('wanted_opportunity',['connection_wanted','deliberate_pathway_missing']),
 'M08':('ability',['named_ability','external_requests_missing']),
 'VERIFY':('accuracy',['organization_reported','accuracy_missing']),
 'R01':('recurrence',['recurring_attention','closure_missing']),
 'PRACTICE-REASON':('practice',['would_practise','practice_value_missing']),
 'FOCUS-DEPTH':('uninterrupted_focus',['interruption_response_known','uninterrupted_focus_missing']),
 'CHOICE-TIME':('clarity',['choice_still_considered','clarity_time_missing']),
 'R04':('body_usefulness',['bodily_reaction_reported','usefulness_missing']),
 'M10':('body_time',['bodily_reaction_reported','within_choice_time_missing']),
 'SIGNAL-DEPENDABILITY':('body_occurrence',['bodily_reaction_reported','across_choice_occurrence_missing']),
 'SIGNAL-NOT-FOLLOWED':('body_override',['bodily_reaction_reported','override_missing']),
 'M06':('risk_cue',['named_risk_cue','unfamiliar_reliance_missing']),
 'ADAPTATION':('adaptation',['limit_reported','adaptation_missing']),
 'ROOM-EFFECT':('environment',['named_condition','effect_missing']),
 'MOOD-AFTER':('affect_after',['mood_reaction_reported','aftermath_missing']),
 'M02':('urgency_after',['pressure_response_reported','aftermath_missing']),
 'WORK-RECOVERY':('energy_after',['depletion_reported','recovery_missing']),
 'R11':('reentry',['time_away_reported','reentry_missing']),
 'G24':('earlier_comparison',['current_response_known','earlier_comparison_welcome']),
 'LIFE-PHASE':('change_timing',['change_reported','timing_missing']),
 'R12':('change_cause',['change_reported','contributors_missing']),
 'CORRECTION-REASON':('correction_reason',['reported_action','correction_reason_missing']),
 'R13':('trust_after',['trust_or_reliance_changed','repair_scope_open'])}
family_titles={
 'friend_company':'A friend asks for company','shared_meal_needs':'Noticing needs and helping','competing_commitments':'Competing commitments','persuasion':'Explaining and persuading','value_exchange':'Making a practical arrangement','group_entry':'Joining a group role','connections':'How connections begin','excess_expectations':'Other people expect too much','ability':'Ability and learning','understanding':'Making sense of information','method':'Following or changing a method','practice_focus':'Practice and concentration','choice':'Making a choice','risk_cues':'Noticing a possible problem','external_role':'Adapting to a group','resources':'Money, recognition and ownership','promise':'Following through on a promise','rhythm_change':'Routine and change','surroundings':'Room and surroundings','romance':'Romantic connection','emotion':'Mood alone and with others','urgency':'External pressure to hurry','work_energy':'Workload and energy','purpose':'Effort worth making','retreat':'Time away and re-entry','development':'Earlier and current responses','correction':'Pointing out a mistake','trust':'Trust and reliability'}
romance={'G12','G13','R05','PHYSICAL-CLOSENESS','ROMANCE-FADE','B0'}
requirements=[];edges=[];nodes=[]
for q in bank['questions']:
    qid=q['id']; code,flags=guards.get(qid,('scene_context',[]))
    mode='self_contained' if qid in standalone else ('semantic_action' if qid=='WHY' else 'one_matching_context')
    record={'id':qid,'family':q['family'],'context_mode':mode,'context_candidates':q['context_sources'],
            'all_context_candidates_required':False,'accept_equivalent_cited_context':True,
            'required_annotations':flags,'predicate_name':code,
            'default_topic':'romance' if qid in romance else q['family'],
            'scope_rule':'Use the exact chosen scene, role, time perspective and current unsuperseded answer; labels alone never supply context.',
            'possible_targets':q['planning_targets'],'targets_are_evidence':False,
            'nonadjacent_rendering':'Name the concrete earlier scene and the reported subject in the delivered question.',
            'global_rules':['not_paused','not_declined','applicable_or_elected_imagination','useful_unanswered_distinction','no_repeated_unresolved_probe']}
    requirements.append(record)
    nodes.append({'id':'q:'+qid,'kind':'question','label':qid,'family':q['family']})
    for ref in q['context_sources']:
        edge_type='advisory_context' if qid in standalone or qid=='WHY' else 'context_candidate'
        edges.append({'from':'q:'+ref,'to':'q:'+qid,'kind':edge_type,'requires_all':False,'label':'context only; admission still required'})
    for facet in q['planning_targets']:
        edges.append({'from':'q:'+qid,'to':'f:'+facet,'kind':'may_inform','evidence_credit':False,'label':'may inform; answer meaning required'})
for e in evidence:nodes.append({'id':'f:'+e['facet_id'],'kind':'information','label':e['facet_id']})
graph={'schema':'scenario-review-graph-v1','candidate_version':bank['version'],'not_a_deployed_controller':True,
       'edge_semantics':{'context_candidate':'Possible source of the scene. Alternatives, not mandatory question order. A cited equivalent answer can also bind it.',
                         'advisory_context':'Related topic only; not a requirement to ask or answer the source question.',
                         'may_inform':'Opportunity to obtain information. Neither stimulus nor arrow is evidence.'},
       'families':[{'id':k,'title':family_titles[k],'question_ids':v} for k,v in bank['families'].items()],
       'nodes':nodes,'edges':edges,'routing_contracts':requirements,
       'comparison_rule':'A comparative interpretation needs answers in both explicitly bound conditions. A single condition supports only that condition, even when a variant was presented.',
       'coverage_rule':'No automatic scoring. Preserve individual subclaims; a compound information label cannot hide a missing part.',
       'equivalent_source_rule':'Alternatives are examples, not a closed whitelist. Reviewer/interviewer must bind an actual matching unsuperseded source; no simulated personal antecedents.'}
write('ROUTING-GRAPH.json',graph)
# Explicit findings kept separate from visualization additions.
findings=[
 {'id':'F01','severity':'minor','object':'G04','before':'Setting up something left the concrete task unspecified.','repair':'Use a shared calendar and the failed invitation step; preserve the same one-action task.','classification':'question_wording'},
 {'id':'F02','severity':'material','object':'R08','before':'The end-of-burst question asked about energy; prolonged overload asked the broader how it affects you and began Now.','repair':'Explicitly reset from the manageable baseline and ask energy at the endpoint. Multiple workload conditions remain bundled; no one-factor causal claim.','classification':'question_wording'},
 {'id':'F03','severity':'material_for_graph_recovery','object':'M02','before':'Conditional pressure-aftermath prompt has an empty context_sources list although That person refers to M01.','repair':'Add M01 as the context candidate, with reported-pressure-response admission unchanged.','classification':'context_link'},
 {'id':'F04','severity':'material_for_graph_recovery','object':'context_requirement defaults','before':'The same one actual matching antecedent text was attached even to self-contained starting scenes. A literal prerequisite interpretation leaves starting scenes with no source.','repair':'Normalize self-contained entries; keep topic associations advisory. No added screening questions or fixed order.','classification':'context_metadata'},
 {'id':'F05','severity':'minor','object':'D05.audience_adaptation illustration','before':'An example linked to the noise/meeting scene discussed traffic and waiting instead.','repair':'Replace only the interpretation illustration with a scene-aligned example. Preserve the frozen old example and every original interview.','classification':'illustration'}]
write('FINDINGS.json',{'pass':'A - full bank and graph audit','source_version':original['version'],'findings':findings,'closed_by_candidate':bank['version']})
write('SOURCE-IDENTITY.json',{'source_head':'55b894227022df3aee8ffd96a95e10f2a02ffe6c','source_files':{n:sha(SRC/n) for n in ['interviewer-bank-v5.json','EVIDENCE-REVIEW.json','INTERVIEW-PROTOCOL.md','DIALOGUE-CHALLENGES.json','source-requirements-v2.json']},'source_manifest_verified':True})
print(json.dumps({'questions':len(bank['questions']),'wording_changes':len([c for c in changes if c['field']=='question']),'context_fields_changed':len([c for c in changes if c['field']!='question']),'guide_examples_changed':1,'new_questions':0,'families':len(family_titles),'graph_nodes':len(nodes),'graph_edges':len(edges)},indent=2))

# Preserve the repaired graph-model and interpretation decisions in regeneration.
graph['comparison_rule']='A comparative interpretation needs both explicitly bound reported branches, possibly in one reply. A declared earlier-life comparison can change time frame. One branch supports only its own condition; no causal inference is implied.'
graph['inherited_scope_rule']='Dependent questions inherit the actual source answer topic and its closures. A generic catalog family never reopens a declined context; an explicitly elected alternative scene has its own recorded scope.'
write('ROUTING-GRAPH.json',graph)
for row in evidence:
    if row['facet_id']=='D13.others_effect':
        row['narrow_supported_reading']='Reports becoming concerned while expecting to remain calm; any broader change of mood is not fully specified.'
        row['revision_note']='Calmness is compatible with concern; do not code absence of all emotional change.'
write('EVIDENCE-GUIDE-v6.json',evidence)
write('FINDINGS.json',{'pass': 'A - full bank and graph audit', 'source_version': 'scenario-bank-v5.1-20260919', 'findings': [{'id': 'F01', 'severity': 'minor', 'object': 'G04', 'before': 'Setting up something left the concrete task unspecified.', 'repair': 'Use a shared calendar and the failed invitation step; preserve the same one-action task.', 'classification': 'question_wording'}, {'id': 'F02', 'severity': 'material', 'object': 'R08', 'before': 'The end-of-burst question asked about energy; prolonged overload asked the broader how it affects you and began Now.', 'repair': 'Explicitly reset from the manageable baseline and ask energy at the endpoint. Multiple workload conditions remain bundled; no one-factor causal claim.', 'classification': 'question_wording'}, {'id': 'F03', 'severity': 'material_for_graph_recovery', 'object': 'M02', 'before': 'Conditional pressure-aftermath prompt has an empty context_sources list although That person refers to M01.', 'repair': 'Add M01 as the context candidate, with reported-pressure-response admission unchanged.', 'classification': 'context_link'}, {'id': 'F04', 'severity': 'material_for_graph_recovery', 'object': 'context_requirement defaults', 'before': 'The same one actual matching antecedent text was attached even to self-contained starting scenes. A literal prerequisite interpretation leaves starting scenes with no source.', 'repair': 'Normalize self-contained entries; keep topic associations advisory. No added screening questions or fixed order.', 'classification': 'context_metadata'}, {'id': 'F05', 'severity': 'minor', 'object': 'D05.audience_adaptation illustration', 'before': 'An example linked to the noise/meeting scene discussed traffic and waiting instead.', 'repair': 'Replace only the interpretation illustration with a scene-aligned example. Preserve the frozen old example and every original interview.', 'classification': 'illustration'}], 'closed_by_candidate': 'scenario-bank-v6.0-20260919', 'graph_model_confirmation_findings': [{'id': 'F06', 'origin': 'new audit model, not inherited survey wording', 'finding': 'Distinct answer-event requirement would reject a single reply that supplies both conditional branches.', 'repair': 'Require two distinct explicitly bound conditions, not two messages.', 'validation': 'test_one_message_can_supply_both_contrast_branches'}, {'id': 'F07', 'origin': 'new audit model, not inherited survey wording', 'finding': 'Unconditional same-time-frame requirement would reject the intended optional earlier-life comparison.', 'repair': 'Permit only explicitly declared changed fields; reject accidental scope mixing.', 'validation': 'test_explicit_earlier_life_contrast_is_allowed'}, {'id': 'F08', 'class': 'interpretation_narrowing', 'finding': 'Remaining calm does not imply no emotional change when the same answer says concern arises.', 'repair': 'Retain both concern and calmness without crediting a completely unchanged mood.', 'status': 'resolved'}, {'id': 'F09', 'class': 'audit_model_privacy_scope', 'finding': 'A generic follow-up can inherit a declined romantic context while its catalog topic is emotion or a generic reason.', 'repair': 'Bind topic scope to the actual source answer and reject closed inherited scopes, not only the question family.', 'status': 'resolved'}]})
changes_record=json.loads((OUT/'CHANGES.json').read_text())
changes_record['additional_interpretation_changes']=[{'facet_id': 'D13.others_effect', 'before': 'Distinguishes concern from anticipated change in own mood.', 'after': 'Reports becoming concerned while expecting to remain calm; any broader change of mood is not fully specified.', 'reason': 'Calmness must not erase reported concern.'}]
write('CHANGES.json',changes_record)
import shutil
for a,b in [('interviewer-bank-v5.json','source-bank-v5.json'),('EVIDENCE-REVIEW.json','source-evidence-v5.json'),('DIALOGUE-CHALLENGES.json','source-dialogues-v5.json')]:shutil.copyfile(SRC/a,OUT/b)
