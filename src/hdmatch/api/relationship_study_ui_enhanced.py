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
    "</details><div id=\"addendumBox\" class=\"hidden\">",
    "</details><button type=\"button\" onclick=\"startNewRelationship()\">Start a new relationship</button><div id=\"addendumBox\" class=\"hidden\">",
)
HTML = _replace_once(
    HTML,
    "checkLLM().then(()=>resume());",
    "function startNewRelationship(){if(!confirm('Start a new relationship study? Your existing private frozen record will not be deleted.'))return;localStorage.removeItem('rr_session');localStorage.removeItem('rr_token');location.reload()}\ncheckLLM().then(()=>resume());",
)
