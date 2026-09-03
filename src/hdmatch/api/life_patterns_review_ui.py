# ruff: noqa: E501
"""Participant-review, voice, and coaching UI for Life Patterns."""

from .life_patterns_coach_ui import COACH_SCRIPT
from .life_patterns_voice_ui import VOICE_SCRIPT

REVIEW_SCRIPT = r'''<script>
(function(){
  const reviewRoot=document.createElement('div');reviewRoot.id='episodeReviews';reviewRoot.className='card hidden';
  reviewRoot.innerHTML='<h2>Check what I understood</h2><p class="note">AI summaries are provisional. Approve, edit, or reject them before they count toward your Life Patterns Map. Review this summary before continuing the interview.</p><div id="episodeReviewList"></div>';
  const progressCard=document.getElementById('progress')?.closest('.card');
  if(progressCard)progressCard.insertAdjacentElement('afterend',reviewRoot);
  let refreshTimer=null;
  function field(tag,value){const el=document.createElement(tag);el.value=value||'';return el}
  async function submitReview(episodeId,body){
    if(!session)return;
    await api(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}/episodes/${encodeURIComponent(episodeId)}/review`,{method:'POST',body:JSON.stringify({token:session.resume_token,...body})});
    await refreshReviews();
    const payload=await api(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}?token=${encodeURIComponent(session.resume_token)}`);
    renderProgress(payload.progress);const send=document.getElementById('send');if(send)send.disabled=false;
  }
  function renderReview(episode){
    const box=document.createElement('div');box.className='card soft';
    const heading=document.createElement('strong');heading.textContent=episode.title||'Provisional episode';box.append(heading);
    const domain=document.createElement('p');domain.className='note';domain.textContent='Area: '+String(episode.domain||'other').replaceAll('_',' ');box.append(domain);
    const summary=document.createElement('p');summary.textContent=episode.narrative||'';box.append(summary);
    if(episode.counterexample){const counter=document.createElement('p');counter.className='note';counter.textContent='Counterexample/exception: '+episode.counterexample;box.append(counter)}
    const buttons=document.createElement('div');buttons.className='row';
    const approve=document.createElement('button');approve.textContent='Yes, that captures it';approve.onclick=()=>submitReview(episode.episode_id,{action:'approve'});
    const edit=document.createElement('button');edit.className='secondary';edit.textContent='Edit';
    const reject=document.createElement('button');reject.className='secondary';reject.textContent='Reject';reject.onclick=()=>submitReview(episode.episode_id,{action:'reject'});
    buttons.append(approve,edit,reject);box.append(buttons);
    edit.onclick=()=>{
      buttons.classList.add('hidden');summary.classList.add('hidden');
      const titleLabel=document.createElement('label');titleLabel.textContent='Title';const title=field('input',episode.title);titleLabel.append(title);
      const narrativeLabel=document.createElement('label');narrativeLabel.textContent='What happened';const narrative=field('textarea',episode.narrative);narrativeLabel.append(narrative);
      const counterLabel=document.createElement('label');counterLabel.textContent='Counterexample/exception, if relevant';const counter=field('textarea',episode.counterexample);counterLabel.append(counter);
      const editButtons=document.createElement('div');editButtons.className='row';const save=document.createElement('button');save.textContent='Save my correction';const cancel=document.createElement('button');cancel.className='secondary';cancel.textContent='Cancel';editButtons.append(save,cancel);
      box.append(titleLabel,narrativeLabel,counterLabel,editButtons);
      save.onclick=()=>submitReview(episode.episode_id,{action:'edit',title:title.value,narrative:narrative.value,counterexample:counter.value||null});
      cancel.onclick=()=>refreshReviews();
    };
    return box;
  }
  async function refreshReviews(){
    if(!session)return;
    try{
      const payload=await api(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}?token=${encodeURIComponent(session.resume_token)}`);
      const pending=(payload.episodes||[]).filter(row=>row.review_status==='pending');
      const list=document.getElementById('episodeReviewList');list.textContent='';
      if(!pending.length){reviewRoot.classList.add('hidden');return}
      const send=document.getElementById('send');if(send)send.disabled=true;
      reviewRoot.classList.remove('hidden');for(const episode of pending)list.append(renderReview(episode));reviewRoot.scrollIntoView({behavior:'smooth',block:'nearest'});
    }catch{}
  }
  const observer=new MutationObserver(()=>{clearTimeout(refreshTimer);refreshTimer=setTimeout(refreshReviews,150)});
  const chat=document.getElementById('chat');if(chat)observer.observe(chat,{childList:true,subtree:true});
  window.addEventListener('focus',refreshReviews);setTimeout(refreshReviews,300);
})();
</script>''' + VOICE_SCRIPT + COACH_SCRIPT
