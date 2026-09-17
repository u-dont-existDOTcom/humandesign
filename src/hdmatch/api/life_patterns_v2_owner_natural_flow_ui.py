"""Final owner-facing UX for the continuous Life Patterns interview.

The fixed scientific surface remains hidden behind a natural conversation. Local topic completion
and direct participant-authored patterns advance automatically to the next admitted question; the
participant can pause at any time. Only interviewer inference gets a judgment panel, and the normal
chat box is the single correction/rewriting channel.
"""

from __future__ import annotations

from .life_patterns_v2_owner_liveness_ui import LIVENESS_RECOVERABILITY_HTML


def _build_natural_flow_html() -> str:
    html = LIVENESS_RECOVERABILITY_HTML

    # The always-visible chat box already carries both correction intents: explain what is wrong
    # or state the exact wording the participant wants. Keep legacy DOM nodes hidden so inherited
    # event wiring remains safe, but do not expose three competing ways to type the same thing.
    revise_button = (
        '<button id="revise" class="secondary">Close — I’ll explain what needs changing</button>'
    )
    exact_button = '<button id="editExactWording" class="secondary">Edit exact wording myself</button>'
    if revise_button not in html or exact_button not in html:
        raise RuntimeError("synthesis correction controls not found")
    html = html.replace(
        revise_button,
        '<button id="revise" class="secondary hidden" aria-hidden="true" tabindex="-1">'
        'Close — I’ll explain what needs changing</button>',
        1,
    )
    html = html.replace(
        exact_button,
        '<button id="editExactWording" class="secondary hidden" aria-hidden="true" tabindex="-1">'
        'Edit exact wording myself</button>',
        1,
    )
    html = html.replace(
        "Or explain what fits, what does not, or what the buttons miss…",
        "If the inference is wrong or needs different wording, say what you mean here…",
        1,
    )
    html = html.replace(
        "The buttons are shortcuts; if none says what you mean, type it in the chat box below.",
        "If the inference is wrong or needs different wording, type what you mean in the chat box below. "
        "Use Keep investigating only when you want another useful question rather than giving the correction yourself.",
        1,
    )

    startup = "resumeOrStart();"
    if startup not in html:
        raise RuntimeError("natural-flow JS insertion point not found")

    natural_js = r'''
// Keep progress, request liveness, and the always-available pause control at the active end.
const __naturalMain=document.querySelector('main');
if(__naturalMain){
  const op=$('operationStatus');const progress=$('interviewProgress');const finish=$('finishForNow');
  if(op)__naturalMain.appendChild(op);
  if(progress){
    __naturalMain.appendChild(progress);
    if(finish){
      const row=document.createElement('div');row.className='row';row.style.marginTop='.7rem';
      row.appendChild(finish);progress.appendChild(row);
    }
  }
}
if($('continueCoverage'))$('continueCoverage').classList.add('hidden');

let __naturalAdvancePending=false;

function naturalCoverageComplete(){
  hide('composer');hide('patternPanel');
  $('sessionSummary').textContent='Interview coverage is complete. You can freeze/export the measurement when you are ready.';
  $('sessionSummary').className='note';show('sessionSummary');
  show('continuation');
  if($('continueCoverage'))$('continueCoverage').classList.add('hidden');
  scrollToNextAction();
}

async function advanceInterview(){
  if(__naturalAdvancePending||!sessionId)return;
  __naturalAdvancePending=true;
  try{
    await ensureCoverageBlueprint();
    if(!incompleteCoverage().length){naturalCoverageComplete();return}
    showWorking('Choosing the next useful question…');
    const context={
      aggregate_coverage:Object.values(coverageAggregate),
      completed_results:completedResults.map(r=>({status:r.status,wording:r.wording||null}))
    };
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/next-question`,{
      method:'POST',body:JSON.stringify(context)
    });
    if(p.coverage_complete){naturalCoverageComplete();return}
    hide('result');hide('continuation');hide('patternPanel');show('composer');
    $('message').value='';$('message').placeholder='Answer in your own words…';
    $('sessionState').textContent='Development conversational probe · continuing interview';
    bubble('ai',p.opening);
    $('message').focus();
    scheduleExactRecovery();
    scrollToNextAction();
  }catch(e){
    $('sessionSummary').textContent=e.message;$('sessionSummary').className='error';show('sessionSummary');
  }finally{
    hideWorking();__naturalAdvancePending=false;
  }
}

// Rebind Send so ordinary turns expose liveness. When the local topic closes, keep moving instead
// of creating a participant-facing Continue checkpoint.
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
      scheduleExactRecovery();
      setTimeout(()=>advanceInterview(),0);
    }else if(p&&p.move_type==='topic_complete'){
      if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
      scheduleExactRecovery();
      setTimeout(()=>advanceInterview(),0);
    }else if(p&&p.pattern_active){
      // A returned synthesis here is an interviewer inference and therefore requires judgment.
      window.__patternDecisionPending=false;
      document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false);
      show('composer');
      $('message').placeholder='If the inference is wrong or needs different wording, say what you mean here…';
    }
  }finally{
    hideWorking();
  }
};
$('send').onclick=send;

// A terminal judgment of a real interviewer inference also advances automatically. The kept or
// rejected result remains visible above the next question, so the participant does not lose the
// decision they just made.
const __naturalRenderResult=renderResult;
renderResult=function(p){
  __naturalRenderResult(p);
  if(p&&p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
  scheduleExactRecovery();
  hide('continuation');
  setTimeout(()=>advanceInterview(),0);
};

// Recovery should restore an actionable state. Completed local topics and already-adjudicated
// syntheses resume directly into the next admitted question; active inference review remains put.
const __naturalRecoveredWorkflow=renderRecoveredWorkflow;
renderRecoveredWorkflow=function(p){
  if(p&&p.workflow_phase==='topic_complete'){
    hide('composer');hide('patternPanel');hide('result');hide('continuation');
    setTimeout(()=>advanceInterview(),0);
    return;
  }
  if(p&&p.workflow_phase==='post_adjudication'){
    __naturalRecoveredWorkflow(p);
    hide('continuation');
    setTimeout(()=>advanceInterview(),0);
    return;
  }
  __naturalRecoveredWorkflow(p);
  if(p&&p.pattern_active){
    show('composer');
    $('message').placeholder='If the inference is wrong or needs different wording, say what you mean here…';
  }
};

resumeOrStart();'''.strip()

    return html.replace(startup, natural_js, 1)


NATURAL_FLOW_RECOVERABILITY_HTML = _build_natural_flow_html()
