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
  if(!missing.length){$('sessionSummary').textContent='Required coverage is complete.';show('sessionSummary');return}
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
    $('sessionState').textContent='Development conversational probe · adaptive coverage';
    bubble('ai',p.opening);
    $('message').focus();
  }catch(e){$('sessionSummary').textContent=e.message;$('sessionSummary').className='error';show('sessionSummary')}
};
""".strip()
    if old_handler not in html:
        raise RuntimeError("dynamic coverage handler insertion point not found")
    return html.replace(old_handler, new_handler, 1)


DYNAMIC_RECOVERABILITY_HTML = _build_dynamic_html()
