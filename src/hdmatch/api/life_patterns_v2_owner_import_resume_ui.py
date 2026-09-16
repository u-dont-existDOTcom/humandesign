"""UI overlay that makes transcript-only recovery an explicit workflow state."""

from __future__ import annotations

from .life_patterns_v2_owner_persistent_ui import PERSISTENT_RECOVERABILITY_HTML


def _build_import_resume_html() -> str:
    html = PERSISTENT_RECOVERABILITY_HTML

    marker = '<div id="conversation" class="chat"></div>'
    panel = """
<div id="recoveredTranscriptActions" class="card hidden">
  <h2>Recovered transcript</h2>
  <p class="note">This older file restored what you said, but it never contained the original hidden ledger. You do not need to retype the interview. Continue from the recovered answers using a newly reconstructed development ledger, or start a clean scientific interview. The reconstructed route is for development continuity only and cannot become the clean scientific freeze.</p>
  <div class="row">
    <button id="resumeRecoveredTranscript">Continue from this recovered interview</button>
    <button id="startCleanFromRecovery" class="secondary">Start a clean scientific interview</button>
  </div>
  <p id="recoveredTranscriptStatus" class="note"></p>
</div>
""".strip()
    if marker not in html:
        raise RuntimeError("recovered-transcript action insertion point not found")
    html = html.replace(marker, panel + "\n\n" + marker, 1)

    old_scroll = (
        "if($('patternPanel')&&!$('patternPanel').classList.contains('hidden'))target=$('patternPanel');\n"
        "    else if($('composer')&&!$('composer').classList.contains('hidden'))target=$('composer');"
    )
    new_scroll = (
        "if($('patternPanel')&&!$('patternPanel').classList.contains('hidden'))target=$('patternPanel');\n"
        "    else if($('recoveredTranscriptActions')&&!$('recoveredTranscriptActions').classList.contains('hidden'))target=$('recoveredTranscriptActions');\n"
        "    else if($('composer')&&!$('composer').classList.contains('hidden'))target=$('composer');"
    )
    if old_scroll not in html:
        raise RuntimeError("recovered-transcript scroll priority insertion point not found")
    html = html.replace(old_scroll, new_scroll, 1)

    # The generic non-scientific guard remains true for both a bare transcript import and
    # a reconstructed development ledger. Only the bare transcript should show the
    # reconstruction choice again; reconstructed state is already actionable and resumable.
    old_quality = "window.__lifePatternsTranscriptOnlyRecovery=p.recovery_quality==='visible_transcript_only';"
    new_quality = "window.__lifePatternsTranscriptOnlyRecovery=p.recovery_quality!=='exact_hidden_ledger';"
    if old_quality not in html:
        raise RuntimeError("recovery-quality UI insertion point not found")
    html = html.replace(old_quality, new_quality, 1)

    # Exact recovery must restore the participant's *workflow phase*, not only data. A
    # post-adjudication snapshot should reopen at Continue interview / Finish, while an
    # active synthesis should reopen at its judgment controls.
    old_exact_pattern = "if(p.pattern_active){show('patternPanel');show('composer')}"
    new_exact_pattern = (
        "renderRecoveredWorkflow(p);\n"
        "  if(p.recovery_quality==='visible_transcript_only')showRecoveredTranscriptActions();else hide('recoveredTranscriptActions');"
    )
    if old_exact_pattern not in html:
        raise RuntimeError("exact restore action-state insertion point not found")
    html = html.replace(old_exact_pattern, new_exact_pattern, 1)

    old_state_copy = (
        "$('sessionState').textContent=p.exact_hidden_ledger_restored?'Recovered working ledger snapshot · unvalidated':'Recovered transcript-only session';\n"
        "  $('sessionSummary').textContent=p.exact_hidden_ledger_restored?'Recovered the exact working hidden ledger and conversation. This preserves the state for continuation/audit but does not certify that the ledger is correct.':'Recovered visible transcript context only; the old hidden ledger was not present in this file.';"
    )
    new_state_copy = (
        "const reconstructed=p.recovery_quality==='reconstructed_visible_transcript';\n"
        "  $('sessionState').textContent=p.exact_hidden_ledger_restored?'Recovered working ledger snapshot · unvalidated':reconstructed?'Recovered reconstructed development ledger · non-scientific':'Recovered transcript-only session';\n"
        "  $('sessionSummary').textContent=p.exact_hidden_ledger_restored?'Recovered the exact working hidden ledger and conversation. This preserves the state for continuation/audit but does not certify that the ledger is correct.':reconstructed?'Recovered the reconstructed development ledger made from the older visible transcript. It can resume development continuity, but it is not the lost original ledger and cannot become the clean scientific freeze.':'Recovered visible transcript context only; the old hidden ledger was not present in this file.';"
    )
    if old_state_copy not in html:
        raise RuntimeError("recovery-state copy insertion point not found")
    html = html.replace(old_state_copy, new_state_copy, 1)

    old_visible_state = (
        "renderRecoveredConversation(p.conversation||turns);\n"
        "  $('sessionState').textContent='Recovered visible transcript · hidden ledger unavailable';"
    )
    new_visible_state = (
        "renderRecoveredConversation(p.conversation||turns);\n"
        "  showRecoveredTranscriptActions();\n"
        "  $('sessionState').textContent='Recovered visible transcript · hidden ledger unavailable';"
    )
    if old_visible_state not in html:
        raise RuntimeError("visible restore action-state insertion point not found")
    html = html.replace(old_visible_state, new_visible_state, 1)

    startup = "resumeOrStart();"
    if startup not in html:
        raise RuntimeError("import-resume JS insertion point not found")
    action_js = r'''
function recoveredDecisionTitle(decision){
  if(decision==='accept'||decision==='revise')return 'Working pattern kept';
  if(decision==='reject')return 'Pattern rejected';
  return 'Pattern left open';
}

function renderRecoveredWorkflow(p){
  hide('patternPanel');hide('result');hide('continuation');
  if(p&&p.pattern_active){
    show('composer');show('patternPanel');
    return;
  }
  if(p&&p.workflow_phase==='post_adjudication'){
    hide('composer');
    const last=completedResults.length?completedResults[completedResults.length-1]:null;
    const decision=p.latest_adjudication_decision||(last&&last.status==='accepted'?'accept':last&&last.status==='rejected'?'reject':'unresolved');
    const wording=p.latest_adjudication_wording||(last&&last.wording)||null;
    let body='<strong>'+escapeHtml(recoveredDecisionTitle(decision))+'</strong>';
    if(wording)body+='<p><strong>'+escapeHtml(wording)+'</strong></p>';
    body+='<p class="note">This settled state was restored from the saved interview checkpoint.</p>';
    $('result').innerHTML=body;show('result');show('continuation');
    return;
  }
  show('composer');
}

function showRecoveredTranscriptActions(){
  show('recoveredTranscriptActions');
  show('composer');
  $('recoveredTranscriptStatus').textContent='';
  scrollToNextAction();
}

$('resumeRecoveredTranscript').onclick=async()=>{
  if(!sessionId)return;
  const btn=$('resumeRecoveredTranscript');btn.disabled=true;
  $('recoveredTranscriptStatus').textContent='Rebuilding an audit-only working ledger from your recovered answers…';
  try{
    const r=await fetch(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/reconstruct-visible`,{method:'POST',headers:{'content-type':'application/json'}});
    let p={};try{p=await r.json()}catch{}
    if(!r.ok)throw new Error(p.detail||'Could not continue from the recovered transcript.');
    hide('recoveredTranscriptActions');
    window.__lifePatternsTranscriptOnlyRecovery=true;
    if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
    if(p.reply)bubble('ai',p.reply);
    renderRecoveredWorkflow(p);
    $('sessionState').textContent='Recovered transcript · reconstructed development ledger';
    $('sessionSummary').textContent='Continued from your recovered answers using a newly reconstructed working ledger. This is useful for development/audit continuity, but it is not the lost original ledger and cannot become the clean scientific freeze.';
    $('sessionSummary').className='note';show('sessionSummary');
    scheduleExactRecovery();scrollToNextAction();
  }catch(e){
    $('recoveredTranscriptStatus').textContent=e.message;
    $('recoveredTranscriptStatus').className='error';
  }finally{btn.disabled=false}
};

$('startCleanFromRecovery').onclick=async()=>{
  localStorage.removeItem(EXACT_RECOVERY_KEY);
  completedResults=[];coverageAggregate={};
  window.__lifePatternsTranscriptOnlyRecovery=false;
  hide('recoveredTranscriptActions');
  resetVisibleInterview();
  $('sessionSummary').textContent='';$('sessionSummary').className='note';hide('sessionSummary');
  try{
    await start();
    renderCoverageStatus();
    scheduleExactRecovery();
    scrollToNextAction();
  }catch(e){
    $('sessionState').textContent='Could not start clean interview';
    setStatus(e.message,true);
  }
};
'''.strip()
    return html.replace(startup, action_js + "\n\n" + startup, 1)


IMPORT_RESUME_RECOVERABILITY_HTML = _build_import_resume_html()
