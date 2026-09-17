"""Owner-facing continuous-flow UX for the Life Patterns development interview.

Normal progress no longer pauses at a Continue interview checkpoint. Finish for now remains
available at all times. Synthesis review exposes ordinary free-form feedback plus a distinct
literal-wording override, without a redundant button that merely focuses the text box.
"""

from __future__ import annotations

from .life_patterns_v2_owner_natural_flow_ui import NATURAL_FLOW_RECOVERABILITY_HTML


def _build_continuous_flow_html() -> str:
    html = NATURAL_FLOW_RECOVERABILITY_HTML
    marker = "resumeOrStart();"
    index = html.rfind(marker)
    if index < 0:
        raise RuntimeError("continuous-flow JS insertion point not found")

    js = r'''
window.__lifePatternsAnswerMemory=Array.isArray(window.__lifePatternsAnswerMemory)?window.__lifePatternsAnswerMemory:[];
window.__lifePatternsPaused=false;
let __continuousAdvancing=false;

function rememberParticipantAnswer(text){
  const clean=String(text||'').trim();if(!clean)return;
  const mem=window.__lifePatternsAnswerMemory;
  if(!mem.length||mem[mem.length-1]!==clean)mem.push(clean);
  if(mem.length>400)mem.splice(0,mem.length-400);
}

// Persist cross-area participant answer memory in the same browser audit/recovery bundle.
const __continuousClientState=currentClientRecoveryState;
currentClientRecoveryState=function(){
  const state=__continuousClientState();
  state.answer_memory=[...(window.__lifePatternsAnswerMemory||[])];
  return state;
};
const __continuousRestoreClientState=restoreClientState;
restoreClientState=function(bundle){
  __continuousRestoreClientState(bundle);
  const state=(bundle&&bundle.client_state)||{};
  let memory=Array.isArray(state.answer_memory)?state.answer_memory.filter(x=>typeof x==='string'&&x.trim()):[];
  if(!memory.length&&bundle&&bundle.server_snapshot&&Array.isArray(bundle.server_snapshot.conversation)){
    memory=bundle.server_snapshot.conversation.filter(r=>r&&r.role==='user'&&r.text).map(r=>String(r.text));
  }
  window.__lifePatternsAnswerMemory=memory.slice(-400);
};

// The normal textbox already handles "what fits / what does not / what is missing". The old
// explanatory-revision button duplicated that interaction. Keep only the genuinely different
// escape hatch: exact literal wording that must be recorded unchanged.
const explainRevision=$('revise');
if(explainRevision){explainRevision.classList.add('hidden');explainRevision.setAttribute('aria-hidden','true');explainRevision.tabIndex=-1}
const exactWording=$('editExactWording');
if(exactWording)exactWording.textContent='Write exact wording to record';
const synthesisNote=document.querySelector('#patternPanel .note');
if(synthesisNote)synthesisNote.textContent+=' Use the text box below for ordinary feedback, corrections, or nuance. Use “Write exact wording to record” only when you want literal replacement wording saved unchanged rather than interpreted conversationally.';

// There is no routine Continue checkpoint. Finish for now is the standing opt-out and stays
// fixed on-screen while the interview is active. The hidden Continue button remains only as an
// exceptional retry frontier if a next-question request fails.
const continueButton=$('continueCoverage');
if(continueButton){continueButton.classList.add('hidden');continueButton.setAttribute('aria-hidden','true');continueButton.tabIndex=-1}
const finishButton=$('finishForNow');
if(finishButton&&__naturalMain){
  const finishWrap=document.createElement('div');finishWrap.id='persistentFinish';finishWrap.className='row';
  finishWrap.style.position='fixed';finishWrap.style.right='1rem';finishWrap.style.top='.75rem';finishWrap.style.zIndex='60';finishWrap.style.justifyContent='flex-end';
  finishButton.className='secondary';finishButton.style.boxShadow='0 1px 5px rgba(0,0,0,.12)';
  finishWrap.appendChild(finishButton);document.body.appendChild(finishWrap);
  finishButton.onclick=async()=>{
    window.__lifePatternsPaused=true;
    try{await syncExactRecovery()}catch(_e){}
    hideWorking();
    $('sessionState').textContent='Interview paused';
    $('sessionSummary').textContent='Paused here. Your current working audit/recovery checkpoint remains saved in this browser; reopen or refresh when you want to resume.';
    $('sessionSummary').className='note';show('sessionSummary');
  };
}

function showContinuousCoverageComplete(){
  hide('composer');hide('patternPanel');hide('result');show('continuation');
  if(continueButton)continueButton.classList.add('hidden');
  $('sessionState').textContent='Development conversational probe · coverage complete';
  $('sessionSummary').textContent='Interview coverage is complete. You can freeze/export the measurement when you are ready.';
  $('sessionSummary').className='note';show('sessionSummary');
  renderProgress();scheduleExactRecovery();scrollToNextAction();
}

async function advanceInterview(){
  if(window.__lifePatternsPaused||__continuousAdvancing||!sessionId)return;
  __continuousAdvancing=true;
  try{
    await ensureCoverageBlueprint();
    if(!incompleteCoverage().length){showContinuousCoverageComplete();return}
    showWorking('Choosing the next useful question…');
    const context={
      aggregate_coverage:Object.values(coverageAggregate),
      completed_results:completedResults.map(r=>({status:r.status,wording:r.wording||null})),
      answer_memory:[...(window.__lifePatternsAnswerMemory||[])]
    };
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/advance`,{method:'POST',body:JSON.stringify(context)});
    if(p.complete){showContinuousCoverageComplete();return}
    hide('result');hide('continuation');hide('patternPanel');show('composer');
    $('message').value='';$('message').placeholder='Answer in your own words…';
    $('sessionState').textContent='Development conversational probe';
    if(p.opening)bubble('ai',p.opening);
    $('message').focus();
    scheduleExactRecovery();scrollToNextAction();
    if(continueButton){continueButton.classList.add('hidden');continueButton.setAttribute('aria-hidden','true');continueButton.tabIndex=-1}
  }catch(e){
    $('sessionSummary').textContent=e.message;$('sessionSummary').className='error';show('sessionSummary');
    if(continueButton){continueButton.textContent='Try next question again';continueButton.classList.remove('hidden');continueButton.removeAttribute('aria-hidden');continueButton.tabIndex=0;continueButton.onclick=advanceInterview}
  }finally{hideWorking();__continuousAdvancing=false}
}

// Topic completion is now a transient internal boundary: display its short acknowledgment, then
// move straight into the next admitted question rather than asking the participant to press Continue.
showNaturalTopicComplete=function(message){
  hide('composer');hide('patternPanel');hide('result');hide('continuation');
  $('sessionState').textContent='Development conversational probe · moving on';
  $('sessionSummary').textContent=message||'That area is covered; moving to the next useful question.';
  $('sessionSummary').className='note';show('sessionSummary');
};

// Remember every submitted participant answer, then auto-advance only when the just-completed
// turn ended a measurement area or directly recorded participant-authored person-specific material.
const __continuousSend=send;
send=async function(){
  const text=$('message').value.trim();
  if(text)rememberParticipantAnswer(text);
  await __continuousSend();
  const p=__naturalLastApiPayload;
  if(p&&(p.direct_pattern_recorded||p.move_type==='topic_complete'))await advanceInterview();
};
$('send').onclick=send;

// Successful participant judgment of a genuine interviewer inference also advances automatically.
// renderResult still performs the authoritative result bookkeeping first.
const __continuousRenderResult=renderResult;
renderResult=function(p){
  __continuousRenderResult(p);
  scheduleExactRecovery();
  if(!window.__lifePatternsPaused)setTimeout(()=>{advanceInterview()},0);
};

// Exact recovery of a locally completed area should resume the continuous flow rather than reopen
// a Continue checkpoint. A pending inferred synthesis still restores to its judgment controls.
const __continuousRecoveredWorkflow=renderRecoveredWorkflow;
renderRecoveredWorkflow=function(p){
  if(p&&p.workflow_phase==='topic_complete'){
    hide('composer');hide('patternPanel');hide('result');hide('continuation');
    $('sessionSummary').textContent='Restored the completed area; continuing from the next missing distinction.';
    $('sessionSummary').className='note';show('sessionSummary');
    setTimeout(()=>{advanceInterview()},0);
    return;
  }
  __continuousRecoveredWorkflow(p);
};
'''.strip()

    return html[:index] + js + "\n\n" + html[index:]


CONTINUOUS_FLOW_RECOVERABILITY_HTML = _build_continuous_flow_html()
