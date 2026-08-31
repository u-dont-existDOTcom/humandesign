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
  <p class="eyebrow">First test · one person</p>
  <h1>Test AstroHD before relationship matching</h1>
  <p class="lede">This starts with your natal chart alone. The system freezes its current trait and behavior predictions before a neutral GPT interviewer asks about you.</p>
  <div class="callout">
    <strong>What you will see afterward</strong>
    <p>The reveal shows the exact prediction-versus-answer comparisons and your true birth state/date rank within the declared candidate set. It may show support, contradiction, partial support, or insufficient evidence.</p>
    <p class="note">This is a developmental symbolic model, not a validated personality test. Your submission does not silently retrain the model during your session; later versions must be trained and released separately.</p>
  </div>

  <form id="intake" novalidate>
    <fieldset>
      <legend>Create the sealed natal session</legend>

      <label for="pilotCode">Owner pilot access code</label>
      <input id="pilotCode" name="pilotCode" type="password" autocomplete="off" required>
      <p class="note">The code is sent only in the request header, is never stored in plain text, and can create one session.</p>

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

      <label for="fold">Repeated clock time, only if the page reports an ambiguity</label>
      <select id="fold" name="fold">
        <option value="">Not known / not ambiguous</option>
        <option value="0">First occurrence</option>
        <option value="1">Second occurrence</option>
      </select>

      <label class="check"><input id="storageConsent" type="checkbox" required><span>I consent to private storage of my exact birth data and interview evidence for this owner pilot.</span></label>
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
function showSession(sessionId){
  submitButton.disabled=true;submitButton.textContent='Session created';
  statusBox.classList.remove('hidden','error');statusBox.textContent='';
  const heading=document.createElement('strong');heading.textContent='Your sealed session is ready.';
  const code=document.createElement('code');code.textContent=sessionId;
  const note=document.createElement('p');note.textContent='Open the interviewer and paste only this code. Do not paste your birth data or chart into that chat.';
  statusBox.append(heading,code,note);
  if(interviewerUrl){const link=document.createElement('a');link.className='button';link.href=interviewerUrl;link.target='_blank';link.rel='noopener';link.textContent='Open the AstroHD interviewer';statusBox.append(link)}
  else{const pending=document.createElement('p');pending.className='note';pending.textContent='The interviewer link is not configured yet. Keep this code private.';statusBox.append(pending)}
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
  if(!selectedPlace)return showStatus('Search for and select your birthplace.',true);
  const pilotCode=document.getElementById('pilotCode').value;
  if(!pilotCode)return showStatus('Enter the owner pilot access code.',true);
  let local_datetime;try{local_datetime=localDateTime()}catch(error){return showStatus(error instanceof Error?error.message:'Check the birth time.',true)}
  const foldValue=document.getElementById('fold').value;
  const body={local_datetime,birthplace:selectedPlace.display_name,iana_timezone:selectedPlace.iana_timezone,fold:foldValue===''?null:Number(foldValue),mode:'scientific_blind',ranking_scope:'known_birth_month'};
  submitButton.disabled=true;submitButton.textContent='Loading and freezing predictions…';showStatus('Creating the session from the verified candidate cache before any answer is accepted. This normally takes only a few seconds.');
  try{
    const response=await fetch('./v1/participant-sessions',{method:'POST',headers:{'content-type':'application/json','x-astrohd-pilot-token':pilotCode,'x-astrohd-storage-consent':'yes','x-astrohd-development-consent':document.getElementById('developmentConsent').checked?'yes':'no'},body:JSON.stringify(body)});
    const payload=await response.json();if(!response.ok)throw new Error(apiErrorMessage(payload,'Could not create the natal session.'));
    document.getElementById('pilotCode').value='';localStorage.setItem('astrohd_owner_session',payload.session_id);showSession(payload.session_id)
  }catch(error){showStatus(error instanceof Error?error.message:'Could not create the natal session.',true);submitButton.disabled=false;submitButton.textContent='Freeze predictions and create my session'}
});
const savedSession=localStorage.getItem('astrohd_owner_session');if(savedSession)showSession(savedSession);
</script>
</body>
</html>
"""


def render_natal_pilot_html(interviewer_url: str | None) -> str:
    """Render the static intake without allowing a configured URL to become markup."""

    return _HTML.replace(
        "__INTERVIEWER_URL_JSON__",
        json.dumps((interviewer_url or "").strip()),
    )


HTML = render_natal_pilot_html(None)
