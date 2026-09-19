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
    (
        "Choose the correct result rather than relying on an auto"
        'matic guess. Birthplace search data © <a href="https://w'
        'ww.openstreetmap.org/copyright" target="_blank" rel="noo'
        'pener noreferrer">OpenStreetMap contributors</a>.</p>'
    ),
)
HTML = _replace_once(
    HTML,
    (
        '<p class="hint">We store the email privately for future '
        "result/recovery delivery. Email verification is not conn"
        "ected yet, so for this pilot the private resume credenti"
        "al is still stored in this browser.</p>"
    ),
    '<p class="hint">We store the email privately for result '
    "and recovery delivery. A private resume credential is al"
    "so kept in this browser as a fallback.</p>"
    '<details id="recoveryPanel"><summary>Resume a saved study by email</summary>'
    "<p>Request a single-use magic link and six-digit code. T"
    "he public response is the same whether or not an eligibl"
    "e study exists.</p>"
    '<label>Email<br><input id="recoveryEmail" type="email" a'
    'utocomplete="email" placeholder="you@example.com"></labe'
    "l> "
    '<button id="recoveryRequestButton" type="button" onclick'
    '="requestRecovery()">Send recovery email</button>'
    '<br><label>Six-digit code<br><input id="recoveryOtp" typ'
    'e="text" inputmode="numeric" autocomplete="one-time-code'
    '" maxlength="6" pattern="[0-9]{6}" placeholder="123456">'
    "</label> "
    '<button id="recoveryVerifyButton" type="button" onclick='
    '"verifyRecoveryCode()">Resume with code</button>'
    '<p id="recoveryStatus" class="hint"></p></details>',
)
HTML = _replace_once(
    HTML,
    '</details><div id="addendumBox" class="hidden">',
    (
        '</details><button type="button" onclick="startNewRelatio'
        'nship()">Start a new relationship</button><div id="adden'
        'dumBox" class="hidden">'
    ),
)
HTML = _replace_once(
    HTML,
    "checkLLM().then(()=>resume());",
    (
        "function recoveryMessage(message){document.getElementByI"
        "d('recoveryStatus').textContent=message}\nasync function "
        "checkRecovery(){try{const r=await fetch('/api/study/reco"
        "very/status');const d=await r.json();if(!d.configured){d"
        "ocument.getElementById('recoveryRequestButton').disabled"
        "=true;document.getElementById('recoveryVerifyButton').di"
        "sabled=true;recoveryMessage('Email recovery is temporari"
        "ly unavailable. A session already saved in this browser "
        "can still resume.')}}catch(e){}}\nasync function requestR"
        "ecovery(){const email=document.getElementById('recoveryE"
        "mail').value.trim();if(!email)return recoveryMessage('En"
        "ter the email used for the study.');const button=documen"
        "t.getElementById('recoveryRequestButton');button.disable"
        "d=true;recoveryMessage('Requesting a single-use link and"
        " code…');try{const r=await fetch('/api/study/recovery/re"
        "quest',{method:'POST',headers:{'content-type':'applicati"
        "on/json'},body:JSON.stringify({email})});const d=await r"
        ".json();recoveryMessage(d.message||'If an eligible study"
        " exists, a recovery email will be sent.')}catch(e){recov"
        "eryMessage('If an eligible study exists, a recovery emai"
        "l will be sent.')}finally{button.disabled=false}}\nfuncti"
        "on acceptRecoveredSession(d){sessionId=d.session_id;toke"
        "n=d.resume_token;localStorage.setItem('rr_session',sessi"
        "onId);localStorage.setItem('rr_token',token);recoveryMes"
        "sage('Recovery verified. Resuming the private study…')}\n"
        "async function verifyRecoveryCode(){const email=document"
        ".getElementById('recoveryEmail').value.trim();const otp="
        "document.getElementById('recoveryOtp').value.trim();if(!"
        "email||!/^[0-9]{6}$/.test(otp))return recoveryMessage('E"
        "nter the study email and the six-digit code.');const but"
        "ton=document.getElementById('recoveryVerifyButton');butt"
        "on.disabled=true;try{const r=await fetch('/api/study/rec"
        "overy/verify',{method:'POST',headers:{'content-type':'ap"
        "plication/json'},body:JSON.stringify({email,otp})});cons"
        "t d=await r.json();if(!r.ok){recoveryMessage(d.detail||'"
        "That code is invalid, expired, already used, or locked.'"
        ");return}acceptRecoveredSession(d);await resume()}catch("
        "e){recoveryMessage('Recovery could not be verified.')}fi"
        "nally{button.disabled=false}}\nfunction recoveryFragment("
        "){if(!location.hash.startsWith('#recovery='))return null"
        ";try{let encoded=location.hash.slice(10).replaceAll('-',"
        "'+').replaceAll('_','/');while(encoded.length%4)encoded+"
        "='=';return JSON.parse(atob(encoded))}catch(e){return nu"
        "ll}}\nasync function recoverFromMagicLink(){const credent"
        "ial=recoveryFragment();if(!credential)return;history.rep"
        "laceState(null,'',location.pathname+location.search);doc"
        "ument.getElementById('recoveryPanel').open=true;recovery"
        "Message('Verifying the single-use email link…');try{cons"
        "t r=await fetch('/api/study/recovery/verify',{method:'PO"
        "ST',headers:{'content-type':'application/json'},body:JSO"
        "N.stringify({session_id:credential.session_id,magic_toke"
        "n:credential.magic_token})});const d=await r.json();if(!"
        "r.ok){recoveryMessage(d.detail||'That link is invalid, e"
        "xpired, already used, or locked.');return}acceptRecovere"
        "dSession(d)}catch(e){recoveryMessage('Recovery could not"
        " be verified.')}}\nfunction startNewRelationship(){if(!co"
        "nfirm('Start a new relationship study? Your existing pri"
        "vate frozen record will not be deleted.'))return;localSt"
        "orage.removeItem('rr_session');localStorage.removeItem('"
        "rr_token');location.reload()}\ncheckRecovery();recoverFro"
        "mMagicLink().then(()=>checkLLM()).then(()=>resume());"
    ),
)
