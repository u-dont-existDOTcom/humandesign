"""Small participant UX additions on top of the confirmatory study UI."""

from __future__ import annotations

from hdmatch.api.relationship_study_ui import HTML as BASE_HTML


def _replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"expected enhanced UI fragment not found: {old[:100]!r}")
    return text.replace(old, new, 1)


HTML = BASE_HTML
HTML = _replace_once(
    HTML,
    "Choose the correct result rather than relying on an automatic guess.</p>",
    "Choose the correct result rather than relying on an automatic guess. Birthplace search data © <a href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\" rel=\"noopener noreferrer\">OpenStreetMap contributors</a>.</p>",
)
HTML = _replace_once(
    HTML,
    "<p class=\"hint\">We store the email privately for future result/recovery delivery. Email verification is not connected yet, so for this pilot the private resume credential is still stored in this browser.</p>",
    "<p class=\"hint\">We store the email privately for result and recovery delivery. A private resume credential is also kept in this browser as a fallback.</p>"
    "<details id=\"recoveryPanel\"><summary>Resume a saved study by email</summary>"
    "<p>Request a single-use magic link and six-digit code. The public response is the same whether or not an eligible study exists.</p>"
    "<label>Email<br><input id=\"recoveryEmail\" type=\"email\" autocomplete=\"email\" placeholder=\"you@example.com\"></label> "
    "<button id=\"recoveryRequestButton\" type=\"button\" onclick=\"requestRecovery()\">Send recovery email</button>"
    "<br><label>Six-digit code<br><input id=\"recoveryOtp\" type=\"text\" inputmode=\"numeric\" autocomplete=\"one-time-code\" maxlength=\"6\" pattern=\"[0-9]{6}\" placeholder=\"123456\"></label> "
    "<button id=\"recoveryVerifyButton\" type=\"button\" onclick=\"verifyRecoveryCode()\">Resume with code</button>"
    "<p id=\"recoveryStatus\" class=\"hint\"></p></details>",
)
HTML = _replace_once(
    HTML,
    "</details><div id=\"addendumBox\" class=\"hidden\">",
    "</details><button type=\"button\" onclick=\"startNewRelationship()\">Start a new relationship</button><div id=\"addendumBox\" class=\"hidden\">",
)
HTML = _replace_once(
    HTML,
    "checkLLM().then(()=>resume());",
    r"""function recoveryMessage(message){document.getElementById('recoveryStatus').textContent=message}
async function checkRecovery(){try{const r=await fetch('/api/study/recovery/status');const d=await r.json();if(!d.configured){document.getElementById('recoveryRequestButton').disabled=true;document.getElementById('recoveryVerifyButton').disabled=true;recoveryMessage('Email recovery is temporarily unavailable. A session already saved in this browser can still resume.')}}catch(e){}}
async function requestRecovery(){const email=document.getElementById('recoveryEmail').value.trim();if(!email)return recoveryMessage('Enter the email used for the study.');const button=document.getElementById('recoveryRequestButton');button.disabled=true;recoveryMessage('Requesting a single-use link and code…');try{const r=await fetch('/api/study/recovery/request',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email})});const d=await r.json();recoveryMessage(d.message||'If an eligible study exists, a recovery email will be sent.')}catch(e){recoveryMessage('If an eligible study exists, a recovery email will be sent.')}finally{button.disabled=false}}
function acceptRecoveredSession(d){sessionId=d.session_id;token=d.resume_token;localStorage.setItem('rr_session',sessionId);localStorage.setItem('rr_token',token);recoveryMessage('Recovery verified. Resuming the private study…')}
async function verifyRecoveryCode(){const email=document.getElementById('recoveryEmail').value.trim();const otp=document.getElementById('recoveryOtp').value.trim();if(!email||!/^[0-9]{6}$/.test(otp))return recoveryMessage('Enter the study email and the six-digit code.');const button=document.getElementById('recoveryVerifyButton');button.disabled=true;try{const r=await fetch('/api/study/recovery/verify',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email,otp})});const d=await r.json();if(!r.ok){recoveryMessage(d.detail||'That code is invalid, expired, already used, or locked.');return}acceptRecoveredSession(d);await resume()}catch(e){recoveryMessage('Recovery could not be verified.')}finally{button.disabled=false}}
function recoveryFragment(){if(!location.hash.startsWith('#recovery='))return null;try{let encoded=location.hash.slice(10).replaceAll('-','+').replaceAll('_','/');while(encoded.length%4)encoded+='=';return JSON.parse(atob(encoded))}catch(e){return null}}
async function recoverFromMagicLink(){const credential=recoveryFragment();if(!credential)return;history.replaceState(null,'',location.pathname+location.search);document.getElementById('recoveryPanel').open=true;recoveryMessage('Verifying the single-use email link…');try{const r=await fetch('/api/study/recovery/verify',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({session_id:credential.session_id,magic_token:credential.magic_token})});const d=await r.json();if(!r.ok){recoveryMessage(d.detail||'That link is invalid, expired, already used, or locked.');return}acceptRecoveredSession(d)}catch(e){recoveryMessage('Recovery could not be verified.')}}
function startNewRelationship(){if(!confirm('Start a new relationship study? Your existing private frozen record will not be deleted.'))return;localStorage.removeItem('rr_session');localStorage.removeItem('rr_token');location.reload()}
checkRecovery();recoverFromMagicLink().then(()=>checkLLM()).then(()=>resume());""",
)
