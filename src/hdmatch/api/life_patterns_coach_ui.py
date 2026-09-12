# ruff: noqa: E501
"""Optional coaching UI layered on top of a participant-approved Life Patterns Map."""

COACH_SCRIPT = r'''<script>
(function(){
  const mapPanel=document.getElementById('mapPanel');if(!mapPanel)return;
  const coach=document.createElement('div');coach.id='coachPanel';coach.className='card soft';coach.innerHTML='<h2>Ask My Life Patterns Coach</h2><p class="note">Use your approved pattern map to think through a current situation. Coaching cannot change your research evidence.</p>';
  const chat=document.createElement('div');chat.id='coachChat';chat.className='chat';
  const box=document.createElement('textarea');box.placeholder='What are you dealing with, deciding, or trying to understand?';
  const row=document.createElement('div');row.className='row';const send=document.createElement('button');send.type='button';send.textContent='Ask Coach';row.append(send);const status=document.createElement('p');status.className='note';coach.append(chat,box,row,status);mapPanel.append(coach);
  function bubble(role,text){const el=document.createElement('div');el.className='bubble '+role;const meta=document.createElement('div');meta.className='meta';meta.textContent=role==='user'?'You':'Life Patterns Coach';const body=document.createElement('div');body.textContent=text;el.append(meta,body);chat.append(el)}
  send.onclick=async()=>{const message=box.value.trim();if(!message||!session)return;bubble('user',message);box.value='';send.disabled=true;status.textContent='Looking at your approved pattern evidence…';try{const payload=await api(`/api/life-patterns/interview/sessions/${encodeURIComponent(session.session_id)}/coach`,{method:'POST',body:JSON.stringify({token:session.resume_token,message})});const result=payload.result;bubble('ai',result.reply);if(result.suggested_experiment){const exp=document.createElement('div');exp.className='insight';exp.textContent='Possible experiment: '+result.suggested_experiment;chat.append(exp)}if(result.important_uncertainty){const uncertainty=document.createElement('p');uncertainty.className='note';uncertainty.textContent='Uncertainty: '+result.important_uncertainty;chat.append(uncertainty)}status.textContent='Coach is read-only: this did not change your Life Patterns evidence.'}catch(e){status.textContent=e.message;status.className='error'}finally{send.disabled=false}};
})();
</script>'''
