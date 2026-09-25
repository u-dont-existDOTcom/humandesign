"""Dynamic coverage UI overlay for the Life Patterns recoverability interview."""

from __future__ import annotations

from .life_patterns_v2_owner_recoverability_ui import RECOVERABILITY_HTML


def _build_dynamic_html() -> str:
    html = RECOVERABILITY_HTML
    html = html.replace(
        "Continue required coverage",
        "Continue interview",
        1,
    )

    progress_markup = """
<div id="interviewProgress" class="card soft" style="margin:.75rem 0 1rem">
  <div class="row" style="justify-content:space-between;align-items:baseline">
    <strong>Interview progress</strong><span id="progressText" class="count">Preparing…</span>
  </div>
  <progress id="progressBar" max="100" value="0" style="width:100%;height:.8rem;margin:.55rem 0 .25rem"></progress>
  <div id="progressNote" class="note">The estimate will update as your answers cover more of the required material.</div>
</div>
""".strip()
    if '<p class="lede">' not in html:
        raise RuntimeError("progress-card insertion point not found")
    html = html.replace('<p class="lede">', progress_markup + '\n<p class="lede">', 1)

    old_coverage_text = (
        "function coverageText(){const missing=incompleteCoverage();const done=coverageBlueprint.length-missing.length;"
        "return `Required coverage: ${done}/${coverageBlueprint.length} domains complete${missing.length?'. Still open: '+missing.map(d=>d.title).join(', '):'. Complete.'}`}"
    )
    new_coverage_text = r"""
function coverageMetrics(){
  const total=coverageBlueprint.length||0;
  let resolved=0,partial=0;
  for(const d of coverageBlueprint){
    const row=coverageAggregate[d.domain_id];const s=row&&row.status;
    if(s==='sufficient'||s==='unknown'||s==='inapplicable'||s==='declined')resolved++;
    else if(s==='partial')partial++;
  }
  const weighted=resolved+(partial*0.5);
  const pct=total?Math.max(0,Math.min(100,Math.round((weighted/total)*100))):0;
  const remaining=Math.max(0,total-weighted);
  const lowQ=remaining?Math.max(1,Math.ceil(remaining/2.5)):0;
  const highQ=remaining?Math.max(lowQ,Math.ceil(remaining/1.2)):0;
  const lowMin=lowQ?Math.max(2,Math.round(lowQ*1.2)):0;
  const highMin=highQ?Math.max(lowMin+1,Math.round(highQ*2)):0;
  return {total,resolved,partial,pct,remaining,lowQ,highQ,lowMin,highMin};
}
function coverageText(){
  const m=coverageMetrics();
  return m.remaining?`Interview progress: about ${m.pct}% through required coverage. Roughly ${m.lowQ}–${m.highQ} substantive questions remain.`:`Interview coverage is complete.`;
}
function renderProgress(){
  const m=coverageMetrics();
  const bar=$('progressBar');if(bar)bar.value=m.pct;
  const text=$('progressText');
  const note=$('progressNote');
  if(!text||!note)return;
  if(!m.total){text.textContent='Preparing…';note.textContent='The estimate will update as your answers cover more of the required material.';return}
  if(!m.remaining){text.textContent='100% · coverage complete';note.textContent='All required dimensions are resolved or explicitly marked missing.';return}
  text.textContent=`≈${m.pct}% · roughly ${m.lowQ}–${m.highQ} questions left`;
  note.textContent=`Very rough time estimate: about ${m.lowMin}–${m.highMin} minutes, depending on answer length. One answer can cover several areas, so this can shrink faster than a fixed questionnaire.`;
}
""".strip()
    if old_coverage_text not in html:
        raise RuntimeError("dynamic coverage summary insertion point not found")
    html = html.replace(old_coverage_text, new_coverage_text, 1)

    old_render = "function renderCoverageStatus(){if(coverageBlueprint.length){$('sessionSummary').textContent=coverageText();show('sessionSummary')}}"
    new_render = "function renderCoverageStatus(){renderProgress();if(coverageBlueprint.length){$('sessionSummary').textContent=coverageText();show('sessionSummary')}}"
    if old_render not in html:
        raise RuntimeError("progress render insertion point not found")
    html = html.replace(old_render, new_render, 1)

    old_blueprint_load = "const b=await api('/api/owner-v2/conversation/coverage/blueprint');coverageBlueprint=b.domains||[];"
    new_blueprint_load = old_blueprint_load + "renderProgress();"
    if old_blueprint_load not in html:
        raise RuntimeError("progress initialization insertion point not found")
    html = html.replace(old_blueprint_load, new_blueprint_load, 1)

    # The participant should have one clear nonterminal action: ask the interviewer
    # for more discriminating evidence. A separate "No — keep investigating" button
    # created a distinction the product could not explain cleanly. If the participant
    # knows what is wrong, the always-visible chat box remains the direct correction path.
    old_continue = '<button id="continuePattern" class="secondary">Keep trying to pin it down</button>'
    new_continue = '<button id="continuePattern" class="secondary">Keep investigating</button>'
    if old_continue not in html:
        raise RuntimeError("synthesis continue button insertion point not found")
    html = html.replace(old_continue, new_continue, 1)

    old_reject_continue = '<button id="reject" class="danger">No — keep investigating</button>'
    hidden_reject_continue = (
        '<button id="reject" class="danger hidden" aria-hidden="true" tabindex="-1">'
        'No — keep investigating</button>'
    )
    if old_reject_continue not in html:
        raise RuntimeError("redundant synthesis rejection button insertion point not found")
    html = html.replace(old_reject_continue, hidden_reject_continue, 1)

    html = html.replace(
        "Would you like to keep trying to pin this pattern down, or make a judgment now? Saying the synthesis does not fit keeps the underlying inquiry open; use Reject and stop only when you actually want to end this thread.",
        "If you are not ready to accept this synthesis, choose Keep investigating and I’ll ask one more useful question. If you already know what is wrong or missing, type it in the chat box below. Use Reject and stop only when you actually want to end this thread.",
        1,
    )
    html = html.replace("bubble('user','Keep trying to pin it down.');", "bubble('user','Keep investigating.');", 1)

    # Prevent accidental duplicate adjudication requests from repeated clicks while a
    # participant decision is in flight. The server also rolls back failed finalization.
    old_decision = """async function decision(decision){
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
}"""
    new_decision = """async function decision(decision){
  if(window.__patternDecisionPending)return;
  window.__patternDecisionPending=true;
  document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=true);
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
  finally{window.__patternDecisionPending=false;if(!$('patternPanel').classList.contains('hidden'))document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false)}
}"""
    if old_decision not in html:
        raise RuntimeError("pattern-decision guard insertion point not found")
    html = html.replace(old_decision, new_decision, 1)

    # Once one pattern is settled, the normal path is the finite adaptive interview.
    # "Explore another pattern" invited indefinite participant-created branches and
    # duplicated the purpose of the information-gain selector. Keep the DOM node hidden
    # only so inherited event wiring remains harmless.
    old_explore = '<button id="exploreAnother">Explore another pattern</button>'
    hidden_explore = (
        '<button id="exploreAnother" class="hidden" aria-hidden="true" tabindex="-1">'
        'Explore another pattern</button>'
    )
    if old_explore not in html:
        raise RuntimeError("explore-another button insertion point not found")
    html = html.replace(old_explore, hidden_explore, 1)
    html = html.replace(
        "You can explore another pattern, continue the standardized coverage checklist, or finish with any remaining domains explicitly marked incomplete.",
        "Continue the interview to cover the remaining gaps using what you have already told me, or finish for now. The interviewer will keep choosing the next useful question rather than opening an unlimited sequence of extra pattern threads.",
        1,
    )
    html = html.replace(
        '<button id="continueCoverage" class="secondary">Continue interview</button>',
        '<button id="continueCoverage">Continue interview</button>',
        1,
    )

    old_fresh = """async function startFreshPattern(){
  const p=await api('/api/owner-v2/conversation/sessions',{method:'POST'});
  sessionId=p.session_id;groundingChoice=null;refiningPattern=false;
  $('sessionState').textContent='Development conversational probe · new pattern thread';
  hide('result');hide('continuation');hide('patternPanel');show('composer');
  $('message').value='';bubble('ai',p.opening);$('message').focus();
}"""
    new_fresh = """async function startFreshPattern(){
  const context={
    aggregate_coverage:Object.values(coverageAggregate),
    completed_results:completedResults.map(r=>({status:r.status,wording:r.wording||null}))
  };
  const p=await api('/api/owner-v2/conversation/sessions/contextual',{method:'POST',body:JSON.stringify(context)});
  sessionId=p.session_id;groundingChoice=null;refiningPattern=false;
  $('sessionState').textContent='Development conversational probe · new pattern thread';
  hide('result');hide('continuation');hide('patternPanel');show('composer');
  $('message').value='';$('message').placeholder='Answer in your own words…';bubble('ai',p.opening);$('message').focus();
}"""
    if old_fresh not in html:
        raise RuntimeError("contextual fresh-pattern insertion point not found")
    html = html.replace(old_fresh, new_fresh, 1)

    old_handler = (
        "$('continueCoverage').onclick=async()=>{const missing=incompleteCoverage();"
        "if(!missing.length){$('sessionSummary').textContent='Required coverage is complete.';"
        "show('sessionSummary');return}try{await startCoverageDomain(missing[0])}catch(e){"
        "$('sessionSummary').textContent=e.message;$('sessionSummary').className='error';"
        "show('sessionSummary')}};"
    )
    new_handler = r"""
$('continueCoverage').onclick=async()=>{
  const missing=incompleteCoverage();
  if(!missing.length){$('sessionSummary').textContent='Interview coverage is complete.';show('sessionSummary');renderProgress();return}
  try{
    const context={
      aggregate_coverage:Object.values(coverageAggregate),
      completed_results:completedResults.map(r=>({status:r.status,wording:r.wording||null}))
    };
    const p=await api('/api/owner-v2/conversation/coverage/next-session',{method:'POST',body:JSON.stringify(context)});
    sessionId=p.session_id;groundingChoice=null;refiningPattern=false;
    hide('result');hide('continuation');hide('patternPanel');show('composer');
    $('message').value='';
    $('message').placeholder='Answer in your own words…';
    $('sessionState').textContent='Development conversational probe · continuing interview';
    bubble('ai',p.opening);
    $('message').focus();
  }catch(e){$('sessionSummary').textContent=e.message;$('sessionSummary').className='error';show('sessionSummary')}
};
""".strip()
    if old_handler not in html:
        raise RuntimeError("dynamic coverage handler insertion point not found")
    return html.replace(old_handler, new_handler, 1)


DYNAMIC_RECOVERABILITY_HTML = _build_dynamic_html()
