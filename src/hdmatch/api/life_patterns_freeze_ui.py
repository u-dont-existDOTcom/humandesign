# ruff: noqa: E501
"""Participant-facing review and immutable behavioral-freeze controls."""

FREEZE_SCRIPT = r'''<script>
(function(){
  const mapPanel=document.getElementById('mapPanel');if(!mapPanel)return;
  const actionRow=mapPanel.querySelector('.row');if(!actionRow)return;
  const open=document.createElement('button');open.type='button';open.className='secondary';open.textContent='Review & freeze for research';actionRow.append(open);
  const panel=document.createElement('div');panel.id='freezePanel';panel.className='card hidden';
  panel.innerHTML='<h2>Review a research snapshot</h2><p class="note">Your ordinary Life Patterns profile can keep changing later. This review creates a separate immutable research snapshot. It does not run or authorize any Human Design, astrology, or other birth-model comparison.</p><div id="freezeMeta"></div><div id="freezeClaims"></div><div id="freezeUnknowns"></div><label class="check hidden" id="freezeAttestLabel"><input id="freezeAttest" type="checkbox"><span>I reviewed every claim and understand that this research snapshot will not change after I freeze it, even though my live profile can continue evolving.</span></label><div class="row"><button id="finalizeFreeze" class="hidden">Freeze reviewed snapshot</button></div><p id="freezeStatus" class="note"></p>';
  mapPanel.insertAdjacentElement('afterend',panel);
  let candidate=null;
  const status=(text,error=false)=>{const el=document.getElementById('freezeStatus');el.textContent=text;el.className=error?'error':'note'};
  function prettyStatus(value){return String(value||'tentative').replaceAll('_',' ')}
  async function apiJson(path,body){return api(path,{method:'POST',body:JSON.stringify(body)})}
  function reviewBadge(review){if(!review)return 'Not reviewed';if(review.action==='approve')return 'Approved';if(review.action==='edit')return 'Edited & approved';if(review.action==='reject')return 'Rejected';return 'Uncertain'}
  async function reviewClaim(claimId,body){
    if(!session||!candidate)return;
    try{candidate=await apiJson(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}/freeze-candidates/${encodeURIComponent(candidate.candidate_id)}/claims/${encodeURIComponent(claimId)}/review`,{token:session.resume_token,...body});renderCandidate()}catch(e){status(e.message,true)}
  }
  function renderClaim(claim){
    const box=document.createElement('div');box.className='card soft';
    const title=document.createElement('strong');title.textContent=claim.title;box.append(title);
    const summary=document.createElement('p');summary.textContent=claim.summary;box.append(summary);
    const meta=document.createElement('p');meta.className='note';meta.textContent='Original synthesis: '+prettyStatus(claim.status)+' · synthesis confidence '+Number(claim.synthesis_confidence||0).toFixed(2)+' · '+reviewBadge(claim.latest_review);box.append(meta);
    if((claim.contexts||[]).length){const contexts=document.createElement('p');contexts.className='note';contexts.textContent='Contexts: '+claim.contexts.join('; ');box.append(contexts)}
    if((claim.limits||[]).length){const limits=document.createElement('p');limits.className='note';limits.textContent='Limits: '+claim.limits.join('; ');box.append(limits)}
    if(claim.latest_review?.action==='edit'&&claim.latest_review.participant_revision){const corrected=document.createElement('div');corrected.className='insight';corrected.textContent='Your correction: '+claim.latest_review.participant_revision.summary;box.append(corrected)}
    const buttons=document.createElement('div');buttons.className='row';
    const approve=document.createElement('button');approve.type='button';approve.textContent='Approve';approve.onclick=()=>reviewClaim(claim.claim_id,{action:'approve'});
    const edit=document.createElement('button');edit.type='button';edit.className='secondary';edit.textContent='Edit';
    const uncertain=document.createElement('button');uncertain.type='button';uncertain.className='secondary';uncertain.textContent='Uncertain';uncertain.onclick=()=>reviewClaim(claim.claim_id,{action:'uncertain'});
    const reject=document.createElement('button');reject.type='button';reject.className='secondary';reject.textContent='Reject';reject.onclick=()=>reviewClaim(claim.claim_id,{action:'reject'});
    buttons.append(approve,edit,uncertain,reject);box.append(buttons);
    edit.onclick=()=>{
      buttons.classList.add('hidden');
      const titleLabel=document.createElement('label');titleLabel.textContent='Corrected title';const titleInput=document.createElement('input');titleInput.value=claim.latest_review?.participant_revision?.title||claim.title;titleLabel.append(titleInput);
      const summaryLabel=document.createElement('label');summaryLabel.textContent='Corrected wording';const summaryInput=document.createElement('textarea');summaryInput.value=claim.latest_review?.participant_revision?.summary||claim.summary;summaryLabel.append(summaryInput);
      const statusLabel=document.createElement('label');statusLabel.textContent='Pattern status';const select=document.createElement('select');select.style.marginTop='.3rem';select.style.padding='.72rem .8rem';select.style.border='1px solid #98a2b3';select.style.borderRadius='.55rem';for(const value of ['stable','context_dependent','mixed','tentative']){const option=document.createElement('option');option.value=value;option.textContent=prettyStatus(value);if(value===(claim.latest_review?.participant_revision?.status||claim.status))option.selected=true;select.append(option)}statusLabel.append(select);
      const note=document.createElement('p');note.className='note';note.textContent='A correction is preserved as new participant data from the review phase; the original AI synthesis remains in the audit record.';
      const editRow=document.createElement('div');editRow.className='row';const save=document.createElement('button');save.type='button';save.textContent='Save my correction';const cancel=document.createElement('button');cancel.type='button';cancel.className='secondary';cancel.textContent='Cancel';editRow.append(save,cancel);
      box.append(titleLabel,summaryLabel,statusLabel,note,editRow);
      save.onclick=()=>reviewClaim(claim.claim_id,{action:'edit',title:titleInput.value,summary:summaryInput.value,status:select.value});cancel.onclick=()=>renderCandidate();
    };
    return box;
  }
  function renderCandidate(){
    if(!candidate)return;
    panel.classList.remove('hidden');
    const meta=document.getElementById('freezeMeta');meta.textContent='';const p=document.createElement('p');p.className='note';p.textContent=`Candidate ${candidate.candidate_id} · ${candidate.reviewed_claim_count}/${candidate.claim_count} claims explicitly reviewed`;meta.append(p);
    const claims=document.getElementById('freezeClaims');claims.textContent='';for(const claim of candidate.claims||[])claims.append(renderClaim(claim));
    const unknowns=document.getElementById('freezeUnknowns');unknowns.textContent='';if((candidate.important_unknowns||[]).length){const h=document.createElement('h3');h.textContent='Important unknowns';unknowns.append(h);const ul=document.createElement('ul');for(const item of candidate.important_unknowns){const li=document.createElement('li');li.textContent=item;ul.append(li)}unknowns.append(ul)}
    const attestLabel=document.getElementById('freezeAttestLabel');const finalize=document.getElementById('finalizeFreeze');
    if(candidate.finalized_freeze_receipt){attestLabel.classList.add('hidden');finalize.classList.add('hidden');const receipt=candidate.finalized_freeze_receipt;status('Frozen as '+receipt.freeze_id+' · SHA-256 '+receipt.freeze_sha256+'. Your live profile can continue changing; this research snapshot cannot.');return}
    if(candidate.review_complete){attestLabel.classList.remove('hidden');finalize.classList.remove('hidden');status('Every claim has an explicit review decision. Check the acknowledgment to freeze this exact snapshot.')}else{attestLabel.classList.add('hidden');finalize.classList.add('hidden');status('Review every claim before freezing. Rejected and uncertain claims stay in the audit record but are not admitted as participant-endorsed profile claims.')}
  }
  open.onclick=async()=>{
    if(!session)return;open.disabled=true;status('Preparing the exact current evidence snapshot…');
    try{candidate=await apiJson(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}/freeze-candidate`,{token:session.resume_token});renderCandidate();panel.scrollIntoView({behavior:'smooth',block:'start'})}catch(e){status(e.message,true);panel.classList.remove('hidden')}finally{open.disabled=false}
  };
  document.getElementById('finalizeFreeze').onclick=async()=>{
    if(!session||!candidate)return;const attest=document.getElementById('freezeAttest');if(!attest.checked){status('Check the acknowledgment before freezing.',true);return}
    const button=document.getElementById('finalizeFreeze');button.disabled=true;status('Writing immutable research snapshot…');
    try{const payload=await apiJson(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}/freeze-candidates/${encodeURIComponent(candidate.candidate_id)}/finalize`,{token:session.resume_token,attest_profile_reviewed:true,attest_snapshot_immutable:true});candidate=payload.candidate;renderCandidate()}catch(e){status(e.message,true)}finally{button.disabled=false}
  };
})();
</script>'''
