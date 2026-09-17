"""Owner-facing continuous-flow UX for the Life Patterns development interview.

Normal progress no longer pauses at a Continue interview checkpoint. Finish for now remains
available at all times. Synthesis review uses one free-form textbox for disagreement, nuance,
correction, or participant-authored replacement wording rather than exposing duplicate edit modes.
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
window.__lifePatternsQuestionAdmissionLog=Array.isArray(window.__lifePatternsQuestionAdmissionLog)?window.__lifePatternsQuestionAdmissionLog:[];
window.__lifePatternsPaused=false;
let __continuousAdvancing=false;

function rememberParticipantAnswer(text){
  const clean=String(text||'').trim();if(!clean)return;
  const mem=window.__lifePatternsAnswerMemory;
  if(!mem.includes(clean))mem.push(clean);
  if(mem.length>400)mem.splice(0,mem.length-400);
}

function rememberQuestionAdmission(path,p){
  if(!p||!p.question_admission)return;
  const rows=window.__lifePatternsQuestionAdmissionLog;
  rows.push({
    recorded_at:new Date().toISOString(),
    path:String(path||''),
    question:String(p.opening||p.reply||p.question_admission.final_question||''),
    admission:p.question_admission
  });
  if(rows.length>400)rows.splice(0,rows.length-400);
}

// Persist cross-area participant answer memory and the internal question-admission trace in the
// same browser audit/recovery bundle. Admission traces are audit metadata, not scientific evidence.
const __continuousClientState=currentClientRecoveryState;
currentClientRecoveryState=function(){
  const state=__continuousClientState();
  state.answer_memory=[...(window.__lifePatternsAnswerMemory||[])];
  state.question_admission_log=[...(window.__lifePatternsQuestionAdmissionLog||[])];
  return state;
};
const __continuousRestoreClientState=restoreClientState;
restoreClientState=function(bundle){
  __continuousRestoreClientState(bundle);
  const state=(bundle&&bundle.client_state)||{};
  let memory=Array.isArray(state.answer_memory)?state.answer_memory.filter(x=>typeof x==='string'&&x.trim()):[];

  // Older exact snapshots predate answer_memory. They cannot recreate participant turns that were
  // never saved, but accepted wording is participant-authoritative and is useful for suppressing
  // repeats. Combine it with any raw user turns that the server snapshot still contains.
  if(!memory.length&&Array.isArray(state.completed_results)){
    for(const row of state.completed_results){
      if(row&&row.status==='accepted'&&row.wording)memory.push(String(row.wording));
    }
  }
  if(bundle&&bundle.server_snapshot&&Array.isArray(bundle.server_snapshot.conversation)){
    for(const row of bundle.server_snapshot.conversation){
      if(row&&row.role==='user'&&row.text)memory.push(String(row.text));
    }
  }
  window.__lifePatternsAnswerMemory=[...new Set(memory.map(x=>String(x).trim()).filter(Boolean))].slice(-400);
  window.__lifePatternsQuestionAdmissionLog=Array.isArray(state.question_admission_log)?state.question_admission_log.slice(-400):[];
};

// Capture the internal admission rationale returned with a displayed question so an uploaded
// audit/recovery snapshot can later explain why a questionable prompt passed the gate.
const __continuousApi=api;
api=async function(path,options={}){
  const p=await __continuousApi(path,options);
  rememberQuestionAdmission(path,p);
  return p;
};

// The always-visible textbox is the one synthesis-correction channel. It can carry an explanation,
// nuance, disagreement, or participant-authored replacement wording. The two old edit buttons both
// opened a way to type text, so exposing them created a distinction the participant did not need.
const explainRevision=$('revise');
if(explainRevision){explainRevision.classList.add('hidden');explainRevision.setAttribute('aria-hidden','true');explainRevision.tabIndex=-1}
const exactWording=$('editExactWording');
if(exactWording){exactWording.classList.add('hidden');exactWording.setAttribute('aria-hidden','true');exactWording.tabIndex=-1}
const synthesisNote=document.querySelector('#patternPanel .note');
if(synthesisNote)synthesisNote.textContent+=' If the inference is wrong, incomplete, or you want different wording, just type what you mean in the text box below. If you want literal wording, say “Exact wording: …”. Use Keep investigating only when you want another question instead of supplying the correction yourself.';
if($('message'))$('message').placeholder='If the inference is wrong or needs different wording, say what you mean here…';

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
