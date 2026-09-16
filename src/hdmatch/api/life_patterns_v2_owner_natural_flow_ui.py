"""Final owner-facing UX refinements for Life Patterns natural interview flow.

This layer keeps scientific progress visible without pulling the participant away from the
current interaction, and lets a coverage topic end without forcing an obvious paraphrase into a
participant-adjudicated Life Pattern.
"""

from __future__ import annotations

from .life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def _build_natural_flow_html() -> str:
    html = LIVENESS_RECOVERABILITY_HTML

    accept_button = '<button id="accept">Yes — keep that</button>'
    if accept_button not in html:
        raise RuntimeError("obvious-synthesis button insertion point not found")
    html = html.replace(
        accept_button,
        accept_button
        + '\n    <button id="skipObvious" class="subtle">True, but too obvious — just move on</button>',
        1,
    )

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

function showNaturalTopicComplete(message){
  hide('composer');hide('patternPanel');hide('result');show('continuation');
  $('sessionState').textContent='Development conversational probe · area covered';
  $('sessionSummary').textContent=message||'That measurement area is covered. Continue when you are ready for the next useful question.';
  $('sessionSummary').className='note';show('sessionSummary');
  scrollToNextAction();
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
      showNaturalTopicComplete('That measurement area is covered. Continue when you are ready for the next useful question.');
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

$('skipObvious').onclick=async()=>{
  if(!sessionId)return;
  const btn=$('skipObvious');btn.disabled=true;
  $('patternStatus').textContent='Marking this area covered without recording the obvious summary as a Life Pattern…';
  $('patternStatus').className='note';
  showWorking('Moving on without recording that obvious summary…');
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/obvious`,{method:'POST'});
    if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
    showNaturalTopicComplete(p.reply||'That area is covered; the obvious summary was not recorded as a Life Pattern.');
    scheduleExactRecovery();
  }catch(e){
    $('patternStatus').textContent=e.message;$('patternStatus').className='error';
    document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false);
  }finally{btn.disabled=false;hideWorking()}
};

// Recovery can also restore a topic that was deliberately completed without a participant-level
// synthesis. Preserve that executable phase instead of reopening a blank textarea.
const __naturalRecoveredWorkflow=renderRecoveredWorkflow;
renderRecoveredWorkflow=function(p){
  if(p&&p.workflow_phase==='topic_complete'){
    showNaturalTopicComplete('That measurement area was already completed before this checkpoint. Continue when you are ready for the next useful question.');
    return;
  }
  __naturalRecoveredWorkflow(p);
};

resumeOrStart();'''.strip()

    return html.replace(startup, natural_js, 1)


NATURAL_FLOW_RECOVERABILITY_HTML = _build_natural_flow_html()
