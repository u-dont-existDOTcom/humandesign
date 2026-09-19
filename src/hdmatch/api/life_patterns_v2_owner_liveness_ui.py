"""UI liveness overlay for recovered and long-running Life Patterns operations."""

from __future__ import annotations

from .life_patterns_v2_owner_import_resume_ui import IMPORT_RESUME_RECOVERABILITY_HTML


def _build_liveness_html() -> str:
    html = IMPORT_RESUME_RECOVERABILITY_HTML

    # Long-running model calls must never look like a dead UI. This indicator is separate
    # from scientific interview progress: it reports request liveness only.
    working_markup = """
<div id="operationStatus" class="card soft hidden" aria-live="polite" aria-busy="true">
  <div class="row" style="justify-content:space-between;align-items:baseline">
    <strong id="operationStatusText">Working on it…</strong><span class="count">Please wait</span>
  </div>
  <progress max="100" style="width:100%;height:.8rem;margin:.55rem 0 .15rem"></progress>
  <div class="note">The interview is still processing; you do not need to click again.</div>
</div>
""".strip()
    if '<p class="lede">' not in html:
        raise RuntimeError("operation-status insertion point not found")
    html = html.replace('<p class="lede">', working_markup + '\n<p class="lede">', 1)

    helper_marker = "function scrollToNextAction(){"
    helpers = r'''
function showWorking(label){
  const box=$('operationStatus');const text=$('operationStatusText');
  if(text)text.textContent=label||'Working on it…';
  if(box)show('operationStatus');
  requestAnimationFrame(()=>{if(box)box.scrollIntoView({behavior:'smooth',block:'nearest'})});
}
function hideWorking(){const box=$('operationStatus');if(box)hide('operationStatus')}
async function ensureCoverageBlueprint(){
  if(coverageBlueprint.length){renderProgress();return coverageBlueprint}
  const b=await api('/api/owner-v2/conversation/coverage/blueprint');
  coverageBlueprint=b.domains||[];
  if(!coverageBlueprint.length)throw new Error('Interview coverage blueprint did not load.');
  renderProgress();
  return coverageBlueprint;
}
'''.strip()
    if helper_marker not in html:
        raise RuntimeError("liveness helper insertion point not found")
    html = html.replace(helper_marker, helpers + "\n\n" + helper_marker, 1)

    # Recovery used to restore answer/coverage rows without restoring the blueprint. That
    # left progress stuck at "Preparing…" and made an empty blueprint look 100% complete.
    exact_marker = "async function restoreExactBundle(bundle){\n  const snapshot="
    if exact_marker not in html:
        raise RuntimeError("exact-restore blueprint insertion point not found")
    html = html.replace(
        exact_marker,
        "async function restoreExactBundle(bundle){\n  await ensureCoverageBlueprint();\n  const snapshot=",
        1,
    )
    visible_marker = "async function restoreVisibleBundle(payload){\n  const turns="
    if visible_marker not in html:
        raise RuntimeError("visible-restore blueprint insertion point not found")
    html = html.replace(
        visible_marker,
        "async function restoreVisibleBundle(payload){\n  await ensureCoverageBlueprint();\n  const turns=",
        1,
    )

    old_resume = r'''async function resumeOrStart(){
  let saved=null;
  try{saved=JSON.parse(localStorage.getItem(EXACT_RECOVERY_KEY)||'null')}catch(_e){}
  if(saved&&saved.schema==='life-patterns-browser-recovery-v2'&&saved.server_snapshot){
    try{await restoreExactBundle(saved);return}catch(_e){}
  }
  await start();
  scheduleExactRecovery();
  scrollToNextAction();
}'''
    new_resume = r'''async function resumeOrStart(){
  showWorking('Preparing or restoring your interview…');
  try{
    await ensureCoverageBlueprint();
    let saved=null;
    try{saved=JSON.parse(localStorage.getItem(EXACT_RECOVERY_KEY)||'null')}catch(_e){}
    if(saved&&saved.schema==='life-patterns-browser-recovery-v2'&&saved.server_snapshot){
      try{await restoreExactBundle(saved);return}catch(_e){}
    }
    await start();
    scheduleExactRecovery();
    scrollToNextAction();
  }finally{hideWorking()}
}'''
    if old_resume not in html:
        raise RuntimeError("resume/start liveness insertion point not found")
    html = html.replace(old_resume, new_resume, 1)

    old_import = r'''$('importRecoveryFile').onchange=async()=>{
  const file=$('importRecoveryFile').files&&$('importRecoveryFile').files[0];
  if(!file)return;
  try{
    const payload=JSON.parse(await file.text());
    await importRecoveryPayload(payload);
  }catch(e){$('sessionSummary').textContent='Import failed: '+e.message;$('sessionSummary').className='error';show('sessionSummary')}
  finally{$('importRecoveryFile').value=''}
};'''
    new_import = r'''$('importRecoveryFile').onchange=async()=>{
  const file=$('importRecoveryFile').files&&$('importRecoveryFile').files[0];
  if(!file)return;
  showWorking('Loading your recovered interview…');
  try{
    await ensureCoverageBlueprint();
    const payload=JSON.parse(await file.text());
    await importRecoveryPayload(payload);
  }catch(e){$('sessionSummary').textContent='Import failed: '+e.message;$('sessionSummary').className='error';show('sessionSummary')}
  finally{$('importRecoveryFile').value='';hideWorking()}
};'''
    if old_import not in html:
        raise RuntimeError("recovery-import liveness insertion point not found")
    html = html.replace(old_import, new_import, 1)

    old_decision = r'''async function decision(decision){
  if(window.__patternDecisionPending)return;
  window.__patternDecisionPending=true;
  document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=true);
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
  finally{window.__patternDecisionPending=false;if(!$('patternPanel').classList.contains('hidden'))document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false)}
}'''
    new_decision = r'''async function decision(decision){
  if(window.__patternDecisionPending)return;
  window.__patternDecisionPending=true;
  document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=true);
  $('patternStatus').textContent='Working on it…';$('patternStatus').className='note';
  showWorking(decision==='accept'?'Saving that and updating interview progress…':'Updating the interview…');
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
  finally{hideWorking();window.__patternDecisionPending=false;if(!$('patternPanel').classList.contains('hidden'))document.querySelectorAll('#patternPanel button').forEach(b=>b.disabled=false)}
}'''
    if old_decision not in html:
        raise RuntimeError("adjudication liveness insertion point not found")
    html = html.replace(old_decision, new_decision, 1)

    old_continue = r'''$('continueCoverage').onclick=async()=>{
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
};'''
    new_continue = r'''$('continueCoverage').onclick=async()=>{
  await ensureCoverageBlueprint();
  const missing=incompleteCoverage();
  if(!missing.length){$('sessionSummary').textContent='Interview coverage is complete.';show('sessionSummary');renderProgress();return}
  showWorking('Choosing the next useful question…');
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
  finally{hideWorking()}
};'''
    if old_continue not in html:
        raise RuntimeError("continue-interview liveness insertion point not found")
    html = html.replace(old_continue, new_continue, 1)

    old_reconstruct_prefix = (
        "const btn=$('resumeRecoveredTranscript');btn.disabled=true;\n"
        "  $('recoveredTranscriptStatus').textContent='Rebuilding an audit-only working ledger from your recovered answers…';\n"
        "  try{"
    )
    new_reconstruct_prefix = (
        "const btn=$('resumeRecoveredTranscript');btn.disabled=true;\n"
        "  $('recoveredTranscriptStatus').textContent='Rebuilding an audit-only working ledger from your recovered answers…';\n"
        "  hide('composer');showWorking('Rebuilding the recovered interview and preparing a synthesis…');\n"
        "  try{"
    )
    if old_reconstruct_prefix not in html:
        raise RuntimeError("recovered-transcript liveness insertion point not found")
    html = html.replace(old_reconstruct_prefix, new_reconstruct_prefix, 1)
    if "}finally{btn.disabled=false}\n};" not in html:
        raise RuntimeError("recovered-transcript liveness cleanup point not found")
    html = html.replace(
        "}finally{btn.disabled=false}\n};",
        "}finally{btn.disabled=false;show('composer');hideWorking()}\n};",
        1,
    )

    old_clean = "$('startCleanFromRecovery').onclick=async()=>{\n  localStorage.removeItem(EXACT_RECOVERY_KEY);"
    new_clean = "$('startCleanFromRecovery').onclick=async()=>{\n  showWorking('Starting a clean interview…');\n  localStorage.removeItem(EXACT_RECOVERY_KEY);"
    if old_clean not in html:
        raise RuntimeError("clean-interview liveness insertion point not found")
    html = html.replace(old_clean, new_clean, 1)
    old_clean_catch = "    setStatus(e.message,true);\n  }\n};"
    new_clean_catch = "    setStatus(e.message,true);\n  }finally{hideWorking()}\n};"
    if old_clean_catch not in html:
        raise RuntimeError("clean-interview liveness cleanup point not found")
    html = html.replace(old_clean_catch, new_clean_catch, 1)

    return html


LIVENESS_RECOVERABILITY_HTML = _build_liveness_html()
