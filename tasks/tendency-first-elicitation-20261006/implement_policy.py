"""Build the owner-requested versioned elicitation layer; preserve v7 bytes."""
from pathlib import Path
import json, subprocess, hashlib

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
assert subprocess.check_output(['git','-C',str(ROOT),'branch','--show-current'],text=True).strip() == 'fix/tendency-first-review-20261006-1839'
assert subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip() == '52ef9d4349eabd3938e32649f7ad95ede176ed11'
assert json.loads((TASK/'WRITER-LEASE.json').read_text())['status'] == 'active'
APP = ROOT/'apps/life-patterns-participant'
CUSTOM = ROOT/'reference/custom_gpt'
audit = json.loads((ROOT/'tasks/survey-owner-feedback-20261001/QUESTION-ALIGNMENT-AUDIT.json').read_text())
original = json.loads((ROOT/'tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json').read_text())
source = {q['id']:q for q in original['questions']}
# Examples are optional aids, not a second response task or required corroboration.
replacements = {}
for row in audit['routes']:
    if row['disposition'] == 'replace':
        text = row['draft_question']
        cut = next((x for x in (' For example,', ' Preparing a meal', ' Preparing a shared', ' A non-urgent', ' A group with', ' A short practical') if x in text), None)
        if cut:
            question, example = text.split(cut,1)
            example = cut.strip() + example
        else:
            question, example = text, ''
        replacements[row['source_route_id']] = (question, example)
# These retained v7 prompts still relied on an isolated hypothetical scene. Give
# their new usual-pattern versions distinct IDs rather than silently broadening v7.
replacements.update({
 'G23': ('In a group where nobody has assigned you a role, what do you usually find yourself noticing first?', ''),
 'G04': ('When a method or set of instructions fails, how do you usually approach working out what to try next?', ''),
 'G22': ('When something interrupts an activity you are absorbed in, how do you usually return to it?', ''),
 'M05': ('When you get a sense that something is off, what do you usually notice that gives you that impression?', 'The setting may matter; a familiar place is only one possible example.'),
 'G20': ('What do you usually want extra money or resources to make possible in your life?', ''),
 'M01': ('How do other people\u2019s urgency or pressure usually affect you when the actual deadline has not changed?', ''),
 'PREFER-EXCHANGE': ('When someone objects to your proposed division of work or costs, how inclined are you usually to keep negotiating?', 'This concerns willingness, not skill or whether either side is objectively right.'),
})
replacements['M11'] = ('When sharing work or costs with someone, how do you usually work out an arrangement?', 'A shared meal is one possible illustration, not a scenario you must role-play. Do not assume that an agreement is reached.')
replacements['G10'] = ('When joining a group with a different way of doing things, how much of your own usual approach tends to change?', 'Keep any limits or differences across groups in the answer; do not require two separate lists.')
replacements['G05'] = ('When you actually try to persuade someone, how does it usually go?', 'This is about self-reported experience, not demonstrated ability or enjoyment of persuading.')
replacements['B0'] = ('How do other people\u2019s moods usually affect your own?', 'Differences by relationship may be relevant; an example is optional.')
retired = {q['source_route_id'] for q in audit['routes'] if q['disposition'] == 'demote'} | set(replacements)
policy_rules = [
 'Ask the person\u2019s usual pattern directly. Use an example only if it helps them understand or resolve an actual ambiguity; never demand a demonstration or anecdote after an adequate answer.',
 'Before any clarification, identify the unresolved person-level distinction and how materially different answers could change its supported reading. Completing a hypothetical scene, updating prompt versions, or filling missing coverage is not sufficient value.',
 'A conditional general answer may already be sufficient. Do not force a fixed trait, a single frequency, or a usual winner when the person says their pattern varies.',
 'For historically complete interviews, use the complete source. Do not administer the new menu from the beginning or treat a TF1 identifier as a new unanswered question merely because its identifier is new.',
 'Do not infer stable personality from a rational response to the practical constraints supplied by a hypothetical scene. Context, stakes, affordability and ordinary role obligations are alternative explanations, not traits.',
 'Legacy v7 questions and evidence retain their original scope. TF1 answers are versioned usual-pattern self-reports; no automatic old-facet or score equivalence is claimed. A TF1 route ID never supplies an old facet. Independently admit a facet only if exact answer content satisfies its actual evidence contract; otherwise retain the observation with candidate_facet_ids=[] rather than discarding it.',
 'Only source-exposed, material ambiguity in a reported pattern can justify a retained context probe. Prefer the participant\u2019s actual context. Never manufacture a new scenario to make a follow-up eligible.',
 'Respect skips, opt-outs and uncertainty. A skipped old item may not be reopened under its new ID or via a dependent variant.',
 'When explaining a question, name its actual neutral purpose without revealing answer directions or inventing validated diagnostic power. Do not say it has no purpose for understanding the person and then insist they answer it.',
]
questions=[]
for rid,(text,example) in replacements.items():
    old=source[rid]
    questions.append({
      'id':'TF1-'+rid, 'source_route_id':rid, 'question':text,
      'example_if_needed':example, 'kind':'tendency_first', 'family':old.get('family'),
      'planning_targets':[], 'context_sources':[],
      'context_requirement':'Self-contained usual-pattern question; prior source still controls nonredundancy.',
      'admission':'Tendency-first policy: a material unresolved recurring response or preference, not completion of a hypothetical or missing coverage. Check the complete source. Do not re-ask after an adequate general answer, explicit unknown or skip.',
      'interpretation_limit':'Only the person\u2019s reported usual pattern with their conditions and uncertainty. Not an objectively demonstrated trait, skill or diagnostic result. Independently verify any facet against the exact answer and original contract; no automatic equivalence to the original '+rid+' scenario contract.',
      'context_binding_rule':'Examples illustrate the question and never establish biography, recurrence or independent corroboration.',
    })
policy={
 'schema':'life-patterns-elicitation-policy-v1', 'version':'tendency-first-v1-20261006',
 'status':'development_collection_policy_not_validated_personality_test',
 'historical_evidence_authority':'Frozen v7 remains unchanged for historical source; new TF1 self-reports are not automatically scored as v7 facets.',
 'rules':policy_rules, 'retired_from_new_elicitation':sorted(retired),
 'questions':questions,
}
raw=(json.dumps(policy,ensure_ascii=False,indent=2)+'\n').encode()
(APP/'participant/static/tendency-first-v1.json').write_bytes(raw)
(CUSTOM/'TENDENCY-FIRST-GUIDE-v1.json').write_bytes(raw)
(TASK/'POLICY-MANIFEST.json').write_text(json.dumps({'version':policy['version'],'sha256':hashlib.sha256(raw).hexdigest(),'new_direct_questions':len(questions),'retired_original_questions':len(retired),'frozen_v7_bytes_changed':False},indent=2)+'\n')
print('POLICY_GENERATED',len(questions),'direct questions;',len(retired),'old routes retired from new elicitation')
