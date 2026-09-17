"""The deployed interview surface: one renderer, no inherited HTML patch chain."""

from .life_patterns_v2_owner_client import CLIENT_SCRIPT

CONTINUOUS_FLOW_RECOVERABILITY_HTML = (
    r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Life Patterns — your interview</title>
<style>
:root{--ink:#20242a;--muted:#536071;--line:#d0d5dd;--soft:#f7f8fa;--accent:#315c5f;--user:#eef6f6;--ai:#f7f3eb;--bad:#a61b1b}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
[hidden]{display:none!important}main{width:min(54rem,calc(100% - 2rem));margin:0 auto 3rem}
header{position:sticky;top:0;z-index:10;display:flex;gap:.75rem;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:.75rem 0;background:#fff;border-bottom:1px solid var(--line)}
h1{font-size:1.35rem;line-height:1.2;margin:0}h2{font-size:1.2rem;margin:.25rem 0 .7rem}h3{font-size:1.05rem;margin:.2rem 0}.muted,.note{color:var(--muted)}.note{font-size:.9rem}.row{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
button,textarea,summary{font:inherit}button{border:1px solid var(--accent);border-radius:.6rem;padding:.65rem .85rem;font-weight:650;cursor:pointer;background:var(--accent);color:white;min-height:44px}
button.secondary{background:white;color:var(--accent)}button:disabled{opacity:.5;cursor:not-allowed}button:focus-visible,summary:focus-visible,a:focus-visible,textarea:focus-visible{outline:3px solid #1e6da8;outline-offset:3px}
textarea{width:100%;min-height:7rem;resize:vertical;border:1px solid #7b8797;border-radius:.65rem;padding:.8rem;line-height:1.5}label{display:block;font-weight:650;margin-bottom:.4rem}
.intro{margin:1.5rem 0;max-width:44rem}.chat{display:grid;gap:1rem;margin:1.25rem 0}.bubble{border-radius:.85rem;padding:.85rem 1rem;white-space:pre-wrap;overflow-wrap:anywhere;max-width:94%;background:var(--ai)}.bubble.user{margin-left:auto;background:var(--user)}.meta{font-size:.8rem;color:var(--muted);margin-bottom:.25rem}
.panel{border:1px solid var(--line);border-radius:.85rem;padding:1rem;margin:1rem 0;overflow-wrap:anywhere}.inference{border-left:4px solid var(--accent)}#formulation{white-space:pre-wrap;font-weight:650}#actionArea{scroll-margin-top:6rem}#composer{margin-top:.85rem}#progressArea{margin:.6rem 0 1rem}progress{width:100%;height:.65rem;accent-color:var(--accent)}#operationStatus{min-height:1.6rem}#operationStatus:empty{min-height:0}#errorArea{border:1px solid #c67575;background:#fff7f7;color:var(--bad)}#saveState{font-size:.8rem}#statusLine{min-height:1.5rem}details{margin:.7rem 0}summary{cursor:pointer;min-height:44px;padding:.55rem 0}#tools{border-top:1px solid var(--line);margin-top:1.5rem}.pattern{border-bottom:1px solid var(--line);padding:1rem 0}.pattern:last-child{border:0}.pattern p,.source{white-space:pre-wrap;overflow-wrap:anywhere}.source{font-size:.9rem;color:var(--muted)}
dialog{width:min(47rem,calc(100% - 1.5rem));max-height:85dvh;border:1px solid var(--line);border-radius:1rem;padding:1.25rem;color:var(--ink)}dialog::backdrop{background:rgba(0,0,0,.35)}.dialogTop{position:sticky;top:-1.25rem;background:#fff;padding:.5rem 0;display:flex;justify-content:space-between;align-items:center;gap:1rem}#jumpLatest{position:fixed;bottom:1rem;left:50%;transform:translateX(-50%);z-index:12;box-shadow:0 2px 10px #0002}
@media(max-width:414px){header h1{font-size:1.15rem}header button{padding:.55rem .65rem;font-size:.9rem}.bubble{max-width:100%}main{width:calc(100% - 1.5rem)}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*{animation:none!important;transition:none!important}}
</style></head><body><main>
<header><div><h1>Life Patterns</h1><div id="saveState" role="status">Preparing your interview…</div></div><div class="row"><button id="viewPatterns" class="secondary">Your patterns (0)</button><button id="finishForNow" class="secondary">Finish for now</button></div></header>
<div id="intro" class="intro"><p>Explore how you respond, choose, relate, and change. You can answer in your own words, correct anything, or finish whenever you need to.</p><details><summary class="note">About this development interview</summary><p class="note">Your answers are processed by the interview server and its configured AI service. Recovery copies stay in this browser; they are not account-synced. A saved checkpoint preserves the interview, not proof that its interpretations are correct. This is not a diagnosis or a validated personality assessment.</p></details></div>
<div id="conversation" class="chat" aria-label="Interview conversation"></div>
<section id="actionArea" aria-label="Current interview action">
<div id="errorArea" class="panel" role="alert" hidden><p id="errorText"></p><div class="row"><button id="retryAction">Retry</button><button id="reconcileAction" class="secondary">Check latest saved state</button><button id="errorBackup" class="secondary">Download backup</button></div></div>
<div id="pausedPanel" class="panel" hidden><h2>Paused here</h2><p>Your saved patterns and this conversation are still available. Resume when you are ready.</p><div class="row"><button id="resumeInterview">Resume interview</button><button id="pausedPatterns" class="secondary">Review your patterns</button></div></div>
<div id="boundedPanel" class="panel" hidden><h2 id="boundedTitle">A useful place to stop</h2><p id="boundedText"></p><div class="row"><button id="reviewFinal">Review your patterns</button><button id="tryAnother" class="secondary">Try another question</button></div></div>
<div id="patternPanel" class="panel inference" hidden><h2>A possible connection</h2><p id="formulation"></p><p id="inferenceNote" class="note"></p><p class="note">Does this fit? The interpretation is yours to accept, reject, or leave uncertain. You can explain a correction in the response box.</p><div class="row"><button id="accept">Yes — keep that</button><button id="investigate" class="secondary">Keep investigating</button><button id="reject" class="secondary">No — leave it out</button><button id="unresolved" class="secondary">Not sure</button></div></div>
<div id="progressArea"><div id="progressText" class="note"></div><progress id="progressBar" max="100" value="0" aria-label="Interview areas addressed"></progress><details><summary class="note">Coverage details</summary><div id="coverageDetails" class="note"></div></details></div>
<div id="operationStatus" role="status" aria-live="polite"></div>
<div id="composer"><div id="correctionTarget" class="note" hidden></div><label id="messageLabel" for="message">Your response</label><textarea id="message" maxlength="8000" placeholder="Answer in your own words…"></textarea><div class="row"><button id="send">Send</button><button id="cancelCorrection" class="secondary" hidden>Return to the question</button><span class="note">Ctrl/⌘ + Enter to send</span></div></div>
<div id="statusLine" class="note" role="status" aria-live="polite"></div>
</section>
<details id="tools"><summary>Save, export, and recovery</summary><p class="note">A readable summary, a backup for resuming, and a frozen research record serve different purposes.</p><div class="row"><button id="summaryExport" class="secondary">Download summary</button><button id="downloadRecovery" class="secondary">Download backup</button><button id="importRecovery" class="secondary">Import backup</button><button id="downloadPrevious" class="secondary">Previous backup</button><button id="freezeMeasurement" class="secondary">Freeze research record</button></div><input id="importFile" type="file" accept="application/json,.json" hidden><p class="note" id="qualityNote"></p><button id="reconstruct" class="secondary" hidden>Continue from this older transcript</button><p><button id="startSeparate" class="secondary">Start a separate interview</button></p><span id="buildLabel" class="note"></span></details>
<dialog id="patternsDialog" aria-labelledby="patternsTitle"><div class="dialogTop"><h2 id="patternsTitle">Your patterns</h2><button id="closePatterns" class="secondary">Back to interview</button></div><p class="note">Direct reports use your own words. Connections proposed by the interviewer are kept only after your judgment. Corrections remain visible and never silently rewrite the earlier record.</p><div id="patternsList"></div></dialog>
<button id="jumpLatest" hidden>Jump to latest</button>
</main><script>"""
    + CLIENT_SCRIPT
    + "</script></body></html>"
)
