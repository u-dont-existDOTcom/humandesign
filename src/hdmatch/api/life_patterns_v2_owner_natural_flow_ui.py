"""Final owner-facing UX refinements for Life Patterns natural interview flow.

This layer keeps scientific progress visible without pulling the participant away from the
current interaction, and lets a coverage topic end without forcing an obvious paraphrase into a
participant-adjudicated Life Pattern.
"""

from __future__ import annotations

from .life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def _build_natural_flow_html() -> str:
    html = LIVENESS_RECOVERABILITY_HTML

    progress_markup = """
<div id="interviewProgress" class="card soft" style="margin:.75rem 0 1rem">
  <div class="row" style="justify-content:space-between;align-items:baseline">
    <strong>Interview progress</strong><span id="progressText" class="count">Preparing…</span>
  </div>
  <progress id="progressBar" max="100" value="0" style="width:100%;height:.8rem;margin:.55rem 0 .25rem"></progress>
  <div id="progressNote" class="note">The estimate will update as your answers cover more of the required material.</div>
</div>
""".strip()
    operation_markup = """
<div id="operationStatus" class="card soft hidden" aria-live="polite" aria-busy="true">
  <div class="row" style="justify-content:space-between;align-items:baseline">
    <strong id="operationStatusText">Working on it…</strong><span class="count">Please wait</span>
  </div>
  <progress max="100" style="width:100%;height:.8rem;margin:.55rem 0 .15rem"></progress>
  <div class="note">The interview is still processing; you do not need to click again.</div>
</div>
""".strip()

    # The previous layout put both progress and request-liveness near the page top. Showing a
    # working state therefore pulled the participant away from the current question, and the
    # subsequent return trip depended on another scroll succeeding. Keep both surfaces at the
    # active end of the document instead.
    for block, name in ((progress_markup, "progress"), (operation_markup, "operation status")):
        if block not in html:
            raise RuntimeError(f"{name} block not found for relocation")
        html = html.replace(block + "\n", "", 1)

    end_marker = "</main>"
    if end_marker not in html:
        raise RuntimeError("natural-flow footer insertion point not found")
    html = html.replace(
        end_marker,
        operation_markup + "\n" + progress_markup + "\n" + end_marker,
        1,
    )

    startup = "resumeOrStart();"
    if startup not in html:
        raise RuntimeError("natural-flow JS insertion point not found")

    natural_js = r'''
// Keep request liveness and scientific progress separate, but keep both near the current action.
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
