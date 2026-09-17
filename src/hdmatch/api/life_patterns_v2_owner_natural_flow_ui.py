"""Final owner-facing UX refinements for Life Patterns natural interview flow.

Scientific progress stays near the current interaction. Person-specific patterns that the
participant already stated directly can be recorded from their own source wording without a
redundant confirmation screen; only interviewer inference is surfaced for judgment.
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

function showNaturalTopicComplete(message){
  hide('composer');hide('patternPanel');hide('result');show('continuation');
  $('sessionState').textContent='Development conversational probe · area covered';
  $('sessionSummary').textContent=message||'That measurement area is covered. Continue when you are ready for the next useful question.';
  $('sessionSummary').className='note';show('sessionSummary');
  scrollToNextAction();
}

// Rebind Send so ordinary model turns also expose liveness. A person-specific pattern copied
// directly from the participant's own source wording is already participant-authored; it is
// recorded internally without making the participant approve the same statement again. An actual
// interviewer inference still arrives as pattern_active and uses the ordinary synthesis controls.
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
    if(p&&p.direct_pattern_recorded){
      completedResults.push({
        status:p.status||'accepted',
        wording:p.wording||null,
        freeze_payload_sha256:p.freeze_payload_sha256||null,
        coverage:p.coverage||null
      });
      if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
      showNaturalTopicComplete('That person-specific pattern was recorded from your own words. Continue when you are ready for the next useful question.');
      scheduleExactRecovery();
    }else if(p&&p.move_type==='topic_complete'){
      if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
      showNaturalTopicComplete('That measurement area is covered. There was no additional person-specific pattern to confirm here. Continue when you are ready for the next useful question.');
      scheduleExactRecovery();
    }else if(p&&p.pattern_active){
      // A returned synthesis here is an interviewer inference and therefore requires judgment.
      window.__patternDecisionPending=false;
      document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false);
    }
  }finally{
    hideWorking();
  }
};
$('send').onclick=send;

// Recovery can also restore a topic that was deliberately completed without a pending inference.
// Preserve that executable phase instead of reopening a blank textarea.
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
