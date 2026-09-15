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
    old_coverage_text = (
        "function coverageText(){const missing=incompleteCoverage();const done=coverageBlueprint.length-missing.length;"
        "return `Required coverage: ${done}/${coverageBlueprint.length} domains complete${missing.length?'. Still open: '+missing.map(d=>d.title).join(', '):'. Complete.'}`}"
    )
    new_coverage_text = (
        "function coverageText(){const missing=incompleteCoverage();const done=coverageBlueprint.length-missing.length;"
        "return missing.length?`Interview coverage: ${done}/${coverageBlueprint.length}. I’ll use what you’ve already said and only ask about remaining gaps.`:`Interview coverage: ${done}/${coverageBlueprint.length}. Complete.`}"
    )
    if old_coverage_text not in html:
        raise RuntimeError("dynamic coverage summary insertion point not found")
    html = html.replace(old_coverage_text, new_coverage_text, 1)

    old_fresh = """async function startFreshPattern(){
  const p=await api('/api/owner-v2/conversation/sessions',{method:'POST'});
  sessionId=p.session_id;groundingChoice=null;
  $('sessionState').textContent='Private conversational probe · new pattern thread';
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
  if(!missing.length){$('sessionSummary').textContent='Interview coverage is complete.';show('sessionSummary');return}
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
