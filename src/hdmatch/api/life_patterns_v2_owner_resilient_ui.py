"""Client overlay for resilient Life Patterns owner testing."""

from __future__ import annotations

from .life_patterns_v2_owner_dynamic_ui import DYNAMIC_RECOVERABILITY_HTML


def _build_resilient_html() -> str:
    html = DYNAMIC_RECOVERABILITY_HTML

    # Progress reports can now arrive on ordinary interview turns rather than only after
    # a pattern is adjudicated. Merge them immediately so the progress card moves during
    # a long thread instead of staying at zero until the end.
    old_send = """    bubble('ai',p.reply);
    setStatus('');
    if(p.pattern_active){"""
    new_send = """    bubble('ai',p.reply);
    if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
    setStatus('');
    if(p.pattern_active){"""
    if old_send not in html:
        raise RuntimeError("in-thread progress merge insertion point not found")
    html = html.replace(old_send, new_send, 1)

    # Keep a browser-local copy of visible turns. This is recovery convenience only: it
    # is not sent to Git/Railway, is not target scoring input, and is not a scientific
    # measurement freeze.
    bubble_prefix = "function bubble(role,text){const el=document.createElement('div');"
    recovery_prefix = r"""function bubble(role,text){
  try{
    const key='lifePatternsLocalRecoveryV1';
    const all=JSON.parse(localStorage.getItem(key)||'{}');
    const sid=sessionId||'UNASSIGNED';
    const row=all[sid]||{session_id:sid,saved_at:null,turns:[]};
    row.saved_at=new Date().toISOString();
    row.turns.push({role,text});
    row.turns=row.turns.slice(-240);
    all[sid]=row;
    localStorage.setItem(key,JSON.stringify(all));
  }catch(_e){}
  const el=document.createElement('div');"""
    if bubble_prefix not in html:
        raise RuntimeError("browser recovery bubble insertion point not found")
    html = html.replace(bubble_prefix, recovery_prefix, 1)

    progress_note = (
        '<div id="progressNote" class="note">The estimate will update as your answers cover more of the required material.</div>'
    )
    progress_note_with_backup = progress_note + (
        '\n  <button id="downloadLocalRecovery" type="button" class="subtle" style="margin-top:.55rem">'
        'Download local recovery copy</button>'
        '\n  <span class="note"> Browser-local transcript backup only; not the scientific freeze.</span>'
    )
    if progress_note not in html:
        raise RuntimeError("browser recovery button insertion point not found")
    html = html.replace(progress_note, progress_note_with_backup, 1)

    marker = "start();"
    recovery_js = r"""
$('downloadLocalRecovery').onclick=()=>{
  try{
    const all=JSON.parse(localStorage.getItem('lifePatternsLocalRecoveryV1')||'{}');
    const rows=Object.values(all).filter(x=>x&&Array.isArray(x.turns));
    rows.sort((a,b)=>String(b.saved_at||'').localeCompare(String(a.saved_at||'')));
    if(!rows.length){$('sessionSummary').textContent='No browser-local recovery copy is available yet.';show('sessionSummary');return}
    const row=rows[0];
    const payload={schema:'life-patterns-local-recovery-v1',recovery_only:true,not_scientific_freeze:true,...row};
    const blob=new Blob([JSON.stringify(payload,null,2)+'\n'],{type:'application/json'});
    const url=URL.createObjectURL(blob);const a=document.createElement('a');
    a.href=url;a.download=`life-patterns-recovery-${String(row.session_id||'session').slice(-12)}.json`;
    document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);
    $('sessionSummary').textContent='Local recovery copy downloaded. It preserves the visible conversation, not the hidden scientific ledger.';show('sessionSummary');
  }catch(e){$('sessionSummary').textContent='Could not create local recovery copy: '+e.message;$('sessionSummary').className='error';show('sessionSummary')}
};

start();""".strip()
    if marker not in html:
        raise RuntimeError("recovery handler insertion point not found")
    return html.replace(marker, recovery_js, 1)


RESILIENT_RECOVERABILITY_HTML = _build_resilient_html()
