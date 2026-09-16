"""Final owner-facing UX refinements for Life Patterns natural interview flow.

This layer keeps scientific progress visible without pulling the participant away from the
current interaction, and lets a coverage topic end without forcing an obvious paraphrase into a
participant-adjudicated Life Pattern.
"""

from __future__ import annotations

from .life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def _build_natural_flow_html() -> str:
    html = LIVENESS_RECOVERABILITY_HTML

    startup = "resumeOrStart();"
    if startup not in html:
        raise RuntimeError("natural-flow JS insertion point not found")

    natural_js = r'''
// Progress and request-liveness belong at the active end of the interview. Move the existing DOM
// nodes rather than duplicating/rebuilding their markup, because upstream recovery controls may
// legitimately add content inside the progress card.
const __naturalMain=document.querySelector('main');
if(__naturalMain){
  const op=$('operationStatus');const progress=$('interviewProgress');
  if(op)__naturalMain.appendChild(op);
  if(progress)__naturalMain.appendChild(progress);
}

// Rebind Send so ordinary model turns also expose liveness and so a measurement area can close
// without leaving a meaningless blank composer behind.
const __naturalBaseApi=api;
let __naturalLastApiPayload=null;
api=async function(path,options={}){
  const p=await __naturalBaseApi(path,options);
  __naturalLastApiPayload=p;
  return p;
};

const __naturalLegacySend=send;
send=async function(){
  const text=$('message').value.trim();
  if(!text||!sessionId)return;
  showWorking('Thinking about that…');
  try{
    __naturalLastApiPayload=null;
    await __naturalLegacySend();
    const p=__naturalLastApiPayload;
    if(p&&p.move_type==='topic_complete'){
      hide('composer');hide('patternPanel');hide('result');show('continuation');
      $('sessionState').textContent='Development conversational probe · area covered';
      $('sessionSummary').textContent='That measurement area is covered. Continue when you are ready for the next useful question.';
      $('sessionSummary').className='note';show('sessionSummary');
      scrollToNextAction();
    }else if(p&&p.pattern_active){
      // A returned synthesis is a stable judgment state, not an in-flight operation.
      window.__patternDecisionPending=false;
      document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false);
    }
  }finally{
    hideWorking();
  }
};
$('send').onclick=send;

// Recovery can also restore a topic that was deliberately completed without a participant-level
// synthesis. Preserve that executable phase instead of reopening a blank textarea.
const __naturalRecoveredWorkflow=renderRecoveredWorkflow;
renderRecoveredWorkflow=function(p){
  if(p&&p.workflow_phase==='topic_complete'){
    hide('composer');hide('patternPanel');hide('result');show('continuation');
    $('sessionSummary').textContent='That measurement area was already completed before this checkpoint. Continue when you are ready for the next useful question.';
    $('sessionSummary').className='note';show('sessionSummary');
    return;
  }
  __naturalRecoveredWorkflow(p);
};

resumeOrStart();'''.strip()

    return html.replace(startup, natural_js, 1)


NATURAL_FLOW_RECOVERABILITY_HTML = _build_natural_flow_html()
