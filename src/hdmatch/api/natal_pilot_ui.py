# ruff: noqa: E501
"""Owner-pilot intake page for the blind natal AstroHD interview."""

from __future__ import annotations

import json

_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AstroHD first test</title>
  <style>
    :root { color-scheme: light; --ink:#1f2933; --muted:#52606d; --line:#cbd2d9; --soft:#f5f7fa; --accent:#2f5d62; --danger:#a61b1b; }
    * { box-sizing: border-box; }
    body { margin:0; color:var(--ink); background:#fff; font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    main { width:min(46rem,calc(100% - 2rem)); margin:2.5rem auto 5rem; }
    h1 { margin:0 0 .65rem; font-size:clamp(2rem,7vw,3.2rem); line-height:1.04; letter-spacing:-.035em; }
    h2 { margin:2rem 0 .5rem; font-size:1.25rem; }
    p { margin:.55rem 0; }
    .eyebrow { color:var(--accent); font-weight:750; letter-spacing:.08em; text-transform:uppercase; font-size:.78rem; }
    .lede { max-width:42rem; font-size:1.1rem; color:var(--muted); }
    .callout { margin:1.4rem 0; padding:1rem 1.1rem; border-left:4px solid var(--accent); background:var(--soft); }
    form { margin-top:2rem; padding:1.25rem; border:1px solid var(--line); border-radius:.85rem; }
    fieldset { margin:0; padding:0; border:0; }
    legend { padding:0; font-weight:750; font-size:1.15rem; }
    label { display:block; margin-top:1rem; font-weight:700; }
    input, select, button, a.button { width:100%; min-height:2.75rem; margin-top:.35rem; padding:.7rem .8rem; border:1px solid #9aa5b1; border-radius:.45rem; background:#fff; color:inherit; font:inherit; }
    input:focus-visible, select:focus-visible, button:focus-visible, a.button:focus-visible { outline:3px solid #8fc3c7; outline-offset:2px; }
    button, a.button { border-color:var(--accent); background:var(--accent); color:#fff; font-weight:750; cursor:pointer; text-align:center; text-decoration:none; }
    button.secondary { width:auto; background:#fff; color:var(--accent); }
    button:disabled { opacity:.55; cursor:not-allowed; }
    .time-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; }
    .time-grid label { font-size:.92rem; }
    .search-row { display:grid; grid-template-columns:minmax(0,1fr) auto; gap:.65rem; align-items:end; }
    .search-row button { width:auto; }
    .results { display:grid; gap:.45rem; margin-top:.65rem; }
    .results button { margin:0; background:#fff; color:var(--ink); border-color:var(--line); text-align:left; font-weight:600; }
    .chosen { margin-top:.65rem; font-weight:700; color:var(--accent); }
    .note { color:var(--muted); font-size:.92rem; }
    .check { display:grid; grid-template-columns:auto 1fr; gap:.65rem; align-items:start; font-weight:500; }
    .check input { width:1.15rem; min-height:1.15rem; margin:.25rem 0 0; }
    .status { margin-top:1rem; padding:.85rem; border-radius:.45rem; background:var(--soft); }
    .error { color:var(--danger); border:1px solid #e8a1a1; background:#fff5f5; }
    .hidden { display:none; }
    code { display:block; margin:.65rem 0; padding:.75rem; background:#fff; border:1px solid var(--line); border-radius:.35rem; overflow-wrap:anywhere; user-select:all; }
    @media (max-width:34rem) { main { margin-top:1.25rem; } form { padding:1rem; } .search-row { grid-template-columns:1fr; } .search-row button { width:100%; } }
  </style>
</head>
<body>
<main>
  <p class="eyebrow">AstroHD research · first blinded test</p>
  <h1>Can astrology and Human Design work better together?</h1>
  <p class="lede">This is this project's first real blinded test of astrology and Human Design, and an attempt to learn whether a combined AstroHD system can make useful personality predictions. It starts with one person's natal chart before testing relationships between two people.</p>
  <p>The project began with a chance finding: for its creator, Joel, the two systems together appeared to describe his personality surprisingly well—but only after every inaccuracy was investigated instead of explained away. That process showed how complicated the combined system is to interpret, and how much harder it is to describe a real personality with enough nuance to test it fairly.</p>
  <p>The astrology and Human Design studies this project is comparing against generally use much simpler personality measures than the detailed claims AstroHD makes. This study therefore needs concrete examples across different domains, life stages, contexts, and counterexamples. A quick or superficial interview cannot tell a wrong prediction from an incomplete description.</p>
  <div class="callout">
    <strong>Please do not take this interview in a rush</strong>
    <p>Detailed, candid answers—including contradictions and places where a pattern does not fit—are the data. The interviewer should pause when an answer is too broad, incomplete, inconsistent, random, or unclear. If enough evidence cannot be obtained, the session will not produce a scientific result.</p>
  </div>
  <div class="callout">
    <strong>What you will see afterward</strong>
    <p>The reveal shows the exact prediction-versus-answer comparisons and your true birth state/date rank within the declared candidate set. It may show support, contradiction, partial support, or insufficient evidence.</p>
    <p class="note">This is a developmental symbolic model, not a validated personality test. Your submission does not silently retrain the model during your session; later versions must be trained and released separately.</p>
  </div>

  <form id="intake" novalidate>
    <fieldset>
      <legend>Create the sealed natal session</legend>

      <label for="pilotCode">One-time owner-test invitation code</label>
      <input id="pilotCode" name="pilotCode" type="password" autocomplete="off" required>
      <p class="note">This code exists because the first release is restricted to Joel's owner test, not open public recruitment. It authorizes one new session, is sent only in a request header, and is never stored in plain text.</p>

      <label for="birthDate">Local birth date</label>
      <input id="birthDate" name="birthDate" type="date" autocomplete="bday" required>

      <div class="time-grid" aria-describedby="timeHelp">
        <label for="birthHour">Hour (00–23)<input id="birthHour" name="birthHour" inputmode="numeric" maxlength="2" placeholder="00" required></label>
        <label for="birthMinute">Minute (00–59)<input id="birthMinute" name="birthMinute" inputmode="numeric" maxlength="2" placeholder="00" required></label>
        <label for="birthSecond">Second, optional<input id="birthSecond" name="birthSecond" inputmode="numeric" maxlength="2" placeholder="00"></label>
      </div>
      <p id="timeHelp" class="note">Use the time shown on your best available record. This exact-time first test does not infer an unknown birth time.</p>

      <div class="search-row">
        <label for="placeQuery">Birthplace<input id="placeQuery" name="placeQuery" type="search" autocomplete="off" placeholder="City, region, country" required></label>
        <button id="searchButton" type="button" class="secondary">Search</button>
      </div>
      <p class="note">Place search sends only this place text to OpenStreetMap Nominatim. Your date, time, access code, and later answers are not sent to the geocoder.</p>
      <div id="placeResults" class="results" aria-live="polite"></div>
      <p id="placeChosen" class="chosen"></p>

      <div id="foldPanel" class="hidden">
        <label for="fold">Which occurrence of this clock time is on the birth record?</label>
        <select id="fold" name="fold">
          <option value="">Choose one</option>
          <option value="0">Earlier occurrence, before the clock was moved back</option>
          <option value="1">Later occurrence, after the clock was moved back</option>
        </select>
        <p class="note">This appears only in the rare case when daylight-saving clocks made the same local time happen twice. If the record does not distinguish them, this exact-time pilot cannot safely choose one for you.</p>
      </div>

      <label class="check"><input id="storageConsent" type="checkbox" required><span>I consent to private storage of my exact birth data and interview evidence for this owner pilot.</span></label>
      <label class="check"><input id="openAIConsent" type="checkbox" required><span>I consent to my questionnaire answers and the birth-redacted prediction comparison being processed by OpenAI in the private AstroHD interviewer. My exact birth record and raw chart stay on this trusted site.</span></label>
      <label class="check"><input id="effortAcknowledgment" type="checkbox" required><span>I understand this is not a quick quiz. I can take the time to give candid details, examples, exceptions, and corrections; an incomplete interview will not produce a scientific result.</span></label>
      <label class="check"><input id="developmentConsent" type="checkbox"><span>I also permit this case to be considered for a future deidentified development dataset. This is optional and does not automatically update the current model.</span></label>

      <button id="submitButton" type="submit">Freeze predictions and create my session</button>
      <div id="status" class="status hidden" role="status" aria-live="polite"></div>
    </fieldset>
  </form>
</main>
<script>
const interviewerUrl=__INTERVIEWER_URL_JSON__;
const form=document.getElementById('intake');
const statusBox=document.getElementById('status');
const submitButton=document.getElementById('submitButton');
const placeResults=document.getElementById('placeResults');
const placeChosen=document.getElementById('placeChosen');
const foldPanel=document.getElementById('foldPanel');
let placeCandidates=[];
let selectedPlace=null;

function apiErrorMessage(problem,fallback){
  if(problem&&typeof problem==='object'&&!Array.isArray(problem)&&problem.error)problem=problem.error;
  if(problem&&typeof problem==='object'&&!Array.isArray(problem)&&problem.detail!==undefined)problem=problem.detail;
  if(typeof problem==='string'&&problem.trim())return problem.trim();
  const rootMessage=problem&&typeof problem==='object'&&typeof problem.message==='string'?problem.message.trim():'';
  const issues=problem&&typeof problem==='object'&&Array.isArray(problem.issues)?problem.issues:(Array.isArray(problem)?problem:[]);
  const details=issues.map(item=>item&&typeof item==='object'?(item.message||item.msg||''):'').filter(Boolean);
  return details.join(' ')||rootMessage||fallback;
}
function showStatus(message,isError=false){statusBox.classList.remove('hidden','error');if(isError)statusBox.classList.add('error');statusBox.textContent=message}
function readTwoDigit(id,max,label,optional=false){const text=document.getElementById(id).value.trim();if(optional&&!text)return 0;if(!/^\d{1,2}$/.test(text))throw new Error('Enter '+label+' as a number.');const value=Number(text);if(value>max)throw new Error('Enter '+label+' from 00 to '+String(max).padStart(2,'0')+'.');return value}
function localDateTime(){const date=document.getElementById('birthDate').value;if(!date)throw new Error('Enter your local birth date.');const hour=readTwoDigit('birthHour',23,'birth hour');const minute=readTwoDigit('birthMinute',59,'birth minute');const second=readTwoDigit('birthSecond',59,'birth second',true);return date+'T'+String(hour).padStart(2,'0')+':'+String(minute).padStart(2,'0')+':'+String(second).padStart(2,'0')}
async function copyText(value){if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value);return}const area=document.createElement('textarea');area.value=value;area.setAttribute('readonly','');area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();const copied=document.execCommand('copy');area.remove();if(!copied)throw new Error('Copy was blocked by the browser.')}
function showCredentialCopyFailure(target,error){target.classList.add('error');const detail=error instanceof Error?error.message:'Copy was blocked.';target.textContent=detail+' Your credentials are still shown above; select and copy both manually.'}
function showSession(sessionId,sessionToken){
  submitButton.disabled=true;submitButton.textContent='Session created';
  statusBox.classList.remove('hidden','error');statusBox.textContent='';
  const heading=document.createElement('strong');heading.textContent='Your sealed session is ready.';
  const sessionLabel=document.createElement('p');sessionLabel.textContent='Session ID';
  const sessionCode=document.createElement('code');sessionCode.textContent=sessionId;
  const sessionHelp=document.createElement('p');sessionHelp.className='note';sessionHelp.textContent='This identifies which sealed prediction belongs to your interview. It contains no birth data.';
  const tokenLabel=document.createElement('p');tokenLabel.textContent='Private session token';
  const tokenCode=document.createElement('code');tokenCode.textContent=sessionToken;
  const tokenHelp=document.createElement('p');tokenHelp.className='note';tokenHelp.textContent='This proves you are allowed to use that session. It is shown once; only its one-way SHA-256 digest is stored.';
  const credentials='AstroHD session ID: '+sessionId+'\nPrivate session token: '+sessionToken;
  const copyMessage=document.createElement('p');copyMessage.id='copyCredentialsMessage';copyMessage.className='note';copyMessage.setAttribute('aria-live','polite');
  const copyButton=document.createElement('button');copyButton.id='copyCredentials';copyButton.type='button';copyButton.className='secondary';copyButton.textContent='Copy both credentials';copyButton.addEventListener('click',async()=>{copyMessage.classList.remove('error');copyMessage.textContent='';try{await copyText(credentials);copyButton.textContent='Both credentials copied';copyMessage.textContent='Keep the copied block private.'}catch(error){showCredentialCopyFailure(copyMessage,error)}});
  const note=document.createElement('p');note.textContent='Paste the copied two-line block into the AstroHD interviewer. Do not paste your birth data or chart.';
  const linkNote=document.createElement('p');linkNote.className='note';linkNote.textContent='There is deliberately no credential-bearing magic link: URLs can leak through history, logs, screenshots, or forwarding. The separate interviewer link contains no private token.';
  statusBox.append(heading,sessionLabel,sessionCode,sessionHelp,tokenLabel,tokenCode,tokenHelp,copyButton,copyMessage,note,linkNote);
  if(interviewerUrl){const link=document.createElement('a');link.className='button';link.href=interviewerUrl;link.target='_blank';link.rel='noopener';link.textContent='Open the AstroHD interviewer';statusBox.append(link)}
  else{const pending=document.createElement('p');pending.className='note';pending.textContent='The interviewer link is not configured yet. Keep this code private.';statusBox.append(pending)}
  const result=document.createElement('a');result.className='button';result.href='./result';result.textContent='Open trusted result page after the interview';statusBox.append(result)
}
document.getElementById('searchButton').addEventListener('click',async()=>{
  const query=document.getElementById('placeQuery').value.trim();if(query.length<2)return showStatus('Enter a city or place to search.',true);
  selectedPlace=null;placeChosen.textContent='';placeResults.textContent='Searching…';
  try{const response=await fetch('./places?q='+encodeURIComponent(query));const payload=await response.json();if(!response.ok)throw new Error(apiErrorMessage(payload,'Birthplace search failed.'));placeCandidates=payload.candidates||[];placeResults.textContent='';if(!placeCandidates.length){placeResults.textContent='No matches. Add a region or country and try again.';return}placeCandidates.forEach((place,index)=>{const button=document.createElement('button');button.type='button';button.textContent=place.display_name+' · '+place.iana_timezone;button.addEventListener('click',()=>{selectedPlace=place;placeChosen.textContent='Selected: '+place.display_name+' · '+place.iana_timezone;placeResults.textContent=''});placeResults.append(button)})}
  catch(error){placeResults.textContent='';showStatus(error instanceof Error?error.message:'Birthplace search failed.',true)}
});
form.addEventListener('submit',async event=>{
  event.preventDefault();
  if(!document.getElementById('storageConsent').checked)return showStatus('Private-storage consent is required for this pilot.',true);
  if(!document.getElementById('openAIConsent').checked)return showStatus('Consent to the birth-redacted OpenAI interview is required.',true);
  if(!document.getElementById('effortAcknowledgment').checked)return showStatus('Confirm that you can take the time needed for a complete, candid interview.',true);
  if(!selectedPlace)return showStatus('Search for and select your birthplace.',true);
  const pilotCode=document.getElementById('pilotCode').value;
  if(!pilotCode)return showStatus('Enter the owner pilot access code.',true);
  let local_datetime;try{local_datetime=localDateTime()}catch(error){return showStatus(error instanceof Error?error.message:'Check the birth time.',true)}
  const foldValue=document.getElementById('fold').value;
  if(!foldPanel.classList.contains('hidden')&&foldValue==='')return showStatus('Choose the earlier or later occurrence shown on the birth record.',true);
  const body={local_datetime,birthplace:selectedPlace.display_name,iana_timezone:selectedPlace.iana_timezone,fold:foldValue===''?null:Number(foldValue),mode:'scientific_blind',ranking_scope:'known_birth_month'};
  submitButton.disabled=true;submitButton.textContent='Loading and freezing predictions…';showStatus('Creating the session from the verified candidate cache before any answer is accepted. This normally takes only a few seconds.');
  try{
    const response=await fetch('./v1/participant-sessions',{method:'POST',headers:{'content-type':'application/json','x-astrohd-pilot-token':pilotCode,'x-astrohd-storage-consent':'yes','x-astrohd-openai-consent':'yes','x-astrohd-development-consent':document.getElementById('developmentConsent').checked?'yes':'no'},body:JSON.stringify(body)});
    const payload=await response.json();if(!response.ok){const message=apiErrorMessage(payload,'Could not create the natal session.');if(message.toLowerCase().includes('ambiguous')){foldPanel.classList.remove('hidden');throw new Error('This local clock time happened twice when clocks moved backward. Choose the earlier or later occurrence shown on the birth record, then submit again.')}throw new Error(message)};
    document.getElementById('pilotCode').value='';showSession(payload.session_id,payload.session_token)
  }catch(error){showStatus(error instanceof Error?error.message:'Could not create the natal session.',true);submitButton.disabled=false;submitButton.textContent='Freeze predictions and create my session'}
});
</script>
</body>
</html>
"""

_RESULT_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AstroHD trusted result</title>
  <style>
    :root { color-scheme:light; --ink:#1f2933; --muted:#52606d; --line:#cbd2d9; --soft:#f5f7fa; --accent:#2f5d62; --danger:#a61b1b; }
    * { box-sizing:border-box; }
    body { margin:0; color:var(--ink); font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    main { width:min(48rem,calc(100% - 2rem)); margin:2.5rem auto 5rem; }
    h1 { font-size:clamp(2rem,7vw,3.2rem); line-height:1.05; letter-spacing:-.035em; }
    form,.card { padding:1.1rem; border:1px solid var(--line); border-radius:.75rem; margin:1rem 0; }
    label { display:block; margin:.8rem 0; font-weight:700; }
    input,button { width:100%; min-height:2.75rem; margin-top:.3rem; padding:.7rem .8rem; border:1px solid #9aa5b1; border-radius:.45rem; font:inherit; }
    button { border-color:var(--accent); background:var(--accent); color:#fff; font-weight:750; cursor:pointer; }
    button:disabled { opacity:.55; }
    .note { color:var(--muted); }
    .status { padding:.85rem; background:var(--soft); }
    .error { color:var(--danger); border:1px solid #e8a1a1; background:#fff5f5; }
    .hidden { display:none; }
    dl { display:grid; grid-template-columns:max-content 1fr; gap:.35rem .8rem; }
    dt { font-weight:750; } dd { margin:0; overflow-wrap:anywhere; }
    pre { white-space:pre-wrap; overflow-wrap:anywhere; background:var(--soft); padding:.8rem; }
  </style>
</head>
<body><main>
  <p class="note">Trusted same-origin result</p>
  <h1>See the complete frozen AstroHD result</h1>
  <p>Your external interviewer receives the prediction comparison and ranks, but not your exact birth record or raw chart. Enter the two values created by the intake to view those sensitive details here.</p>
  <form id="resultForm">
    <label for="sessionId">Session ID<input id="sessionId" autocomplete="off" required></label>
    <label for="sessionToken">Private session token<input id="sessionToken" type="password" autocomplete="off" required></label>
    <button id="loadButton" type="submit">Load my trusted result</button>
  </form>
  <div id="status" class="status hidden" role="status" aria-live="polite"></div>
  <section id="result" class="hidden" aria-live="polite">
    <div class="card"><h2>Confirmatory rank</h2><dl id="ranking"></dl></div>
    <div class="card"><h2>Frozen predictions compared with answers</h2><div id="comparisons"></div></div>
    <div class="card"><h2>Exact model receipt</h2><pre id="receipt"></pre></div>
    <details class="card"><summary><strong>Sensitive birth record and raw chart</strong></summary><pre id="sensitive"></pre></details>
  </section>
<script>
const form=document.getElementById('resultForm');const statusBox=document.getElementById('status');const result=document.getElementById('result');
function apiErrorMessage(problem,fallback){if(problem&&typeof problem==='object'&&!Array.isArray(problem)&&problem.error)problem=problem.error;if(problem&&typeof problem==='object'&&!Array.isArray(problem)&&problem.detail!==undefined)problem=problem.detail;if(typeof problem==='string'&&problem.trim())return problem.trim();const root=problem&&typeof problem==='object'&&typeof problem.message==='string'?problem.message.trim():'';const issues=problem&&typeof problem==='object'&&Array.isArray(problem.issues)?problem.issues:(Array.isArray(problem)?problem:[]);const details=issues.map(item=>item&&typeof item==='object'?(item.message||item.msg||''):'').filter(Boolean);return details.join(' ')||root||fallback}
function status(message,error=false){statusBox.classList.remove('hidden','error');if(error)statusBox.classList.add('error');statusBox.textContent=message}
function addRow(list,label,value){const term=document.createElement('dt');term.textContent=label;const detail=document.createElement('dd');detail.textContent=String(value);list.append(term,detail)}
function show(payload){
  const rank=payload.confirmatory_ranking;const list=document.getElementById('ranking');list.textContent='';addRow(list,'True date rank',rank.true_date_rank+' of '+rank.candidate_date_count);addRow(list,'True state rank',rank.true_state_rank+' of '+rank.candidate_state_count);addRow(list,'Date percentile',rank.true_date_percentile);addRow(list,'State percentile',rank.true_state_percentile);addRow(list,'Top state ties',rank.top_state_tie_count);addRow(list,'Scientific status',rank.scientific_status);
  const comparisons=document.getElementById('comparisons');comparisons.textContent='';payload.prediction_comparisons.forEach(item=>{const card=document.createElement('article');card.className='card';const title=document.createElement('h3');title.textContent=item.question_id+' · '+item.classification;const predicted=document.createElement('p');predicted.textContent='Frozen predicted answer: '+item.predicted_answer;const observed=document.createElement('p');observed.textContent='Observed answer: '+(item.observed_answer===null?'insufficient evidence':item.observed_answer);const statements=document.createElement('p');statements.textContent=(item.behavioral_statements||[]).join(' ');card.append(title,predicted,observed,statements);comparisons.append(card)});
  document.getElementById('receipt').textContent=JSON.stringify(payload.model_receipt,null,2);document.getElementById('sensitive').textContent=JSON.stringify({birth:payload.birth,chart:payload.chart},null,2);result.classList.remove('hidden');status('Result loaded from the private AstroHD store.');
}
form.addEventListener('submit',async event=>{event.preventDefault();const sessionId=document.getElementById('sessionId').value.trim();const token=document.getElementById('sessionToken').value.trim();if(!sessionId||!token)return status('Enter both the session ID and private session token.',true);const button=document.getElementById('loadButton');button.disabled=true;status('Loading the immutable reveal…');try{const response=await fetch('./trusted/v1/participant-sessions/'+encodeURIComponent(sessionId)+'/reveal',{method:'POST',headers:{'x-astrohd-session-token':token}});const payload=await response.json();if(!response.ok)throw new Error(apiErrorMessage(payload,'Could not load the result.'));show(payload)}catch(error){status(error instanceof Error?error.message:'Could not load the result.',true)}finally{button.disabled=false}});
</script>
</main></body></html>"""


def render_natal_pilot_html(interviewer_url: str | None) -> str:
    """Render the static intake without allowing a configured URL to become markup."""

    safe_url = json.dumps((interviewer_url or "").strip()).replace("<", "\\u003c")
    return _HTML.replace(
        "__INTERVIEWER_URL_JSON__",
        safe_url,
    )


def render_natal_result_html() -> str:
    return _RESULT_HTML


HTML = render_natal_pilot_html(None)
