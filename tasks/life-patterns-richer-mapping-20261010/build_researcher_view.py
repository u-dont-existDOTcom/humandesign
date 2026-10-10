"""Readable, provenance-preserving owner-only map: no participant private answers."""

from __future__ import annotations

import html
import json
from pathlib import Path

TASK = Path(__file__).resolve().parent
BRIDGE = json.loads((TASK / "question_to_chart_hypotheses_v0.json").read_text())
CODEBOOK = json.loads((TASK / "source_to_target_evidence_codebook_v0.json").read_text())
THEORY = {row["hypothesis_id"]: row for row in BRIDGE["theory_hypotheses"]}
EVIDENCE = {row["hypothesis_id"]: row for row in CODEBOOK["hypotheses"]}
ROWS = BRIDGE["current_question_contracts"]


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


summary = """# Richer mapping and questionnaire defects — research development audit

**Status:** Development proposal only. Not a live/questionnaire change, not a decoder, not a scientific validation of Human Design or astrology. No owner DOB, birth-chart target, or private answer content was used to select predictions.

## What the previous report meant

The present interview questions are good at preserving qualitative source but not necessarily at testing a chart model. The 25 current TF1 records all have `planning_targets: []`. That *alone* is not an accidental defect: a chart-blind interviewer should not be told the participant's predicted chart features or which answer helps the theory. A separate, frozen codebook must link the neutral answer dimensions to theory predictions for independent scoring. It did not exist for these 25 current questions.

The older six-clause AstroHD bridge tests five signed behavioral domains with nine historical question routes. It cannot be turned into a strong new birth-time validation merely by attaching more uncalibrated questions to the same six clauses; six binary chart clauses produce at most 64 different clause signatures, though a rare conjunction may still distinguish a particular interval. The 84-turn owner's record reuses 78 of the earlier 79 exact question/answer pairs and cannot count as new independent evidence. A prior genuinely frozen V4.3 crosswalk failed to identify the recorded birth time. Keep all these results separately.

## What this audit actually provides

- **25/25** current questions receive a measurable behavioral distinction, necessary contrast, major confounds and a concrete defect/scope assessment.
- **12** distinct source-anchored Human Design theory hypotheses are recorded separately from the interviewer. They are ideas to test, not validated mappings.
- **10/25** current questions have even a plausible link to one of these chart hypotheses. **Nine require a meaningfully improved question or better evidence before the link is eligible**, and one is close to the theory but remains unscored. The other 15 do **not** acquire chart predictions by analogy or wishful thinking.
- **Four new prospective questions** target previously missing contrasts in decision timing, role invitation, emotional settling and identity-direction stability.
- Twelve hypothesis-specific evidence, counterevidence and abstention rules are drafted with numeric scoring and probabilities deliberately unset.

**No mapped question is currently admitted for birth ranking.** The new bridge and any wording changes must be frozen and tested prospectively on a new independent birth-data cohort of untouched participants, using an independent blinded behavioral coder and a separately precommitted chart-feature/scoring/decoy universe.

## Key questionnaire defects worth addressing before another validation interview

1. **TF1-G06 (group entry):** unassigned group participation is not the same thing as having one's particular contribution recognized and being invited. The theory's Projector claim would not be tested by the original question.
2. **TF1-D0 (practice):** intrinsic pleasure in refining technique must be separated from practicing to avoid learning a mistake. The present question partly allows that distinction but earlier responses show it can still be misinterpreted.
3. **TF1-G17 (correction):** the existing question focuses on harmless errors. A channel-of-correction hypothesis is about impulse to improve meaningful faults. Compare the same person's harmless vs consequential cases, and felt impulse vs speaking up.
4. **TF1-G15 (energy):** interest, workload, duration and fatigue are separate dimensions; an ordinary sustainable workday does not imply unlimited stamina or vice versa.
5. **TF1-M03 (commitments):** small favors one loses interest in do not test a source claim about consciously accepted substantial commitments.
6. **TF1-G02 (explaining):** adjusting explanations to the audience is not the same as originating an insight and then articulating it.
7. **TF1-G23/G04:** 'what do you notice first?' and 'what do you try when instructions fail?' can yield generic or tautological responses without distinctive competing alternatives.
8. **TF1-B0 (others' moods):** mood contagion, empathy, conflict and after-separation recovery need distinct questions/conditions.
9. **TF1-STATUS (recognition):** liking praise from intimates is not the same as being invited into a role based on recognition. Keep the status question as a behavioral dimension without automatically turning it into Projector evidence.
10. **TF1-G20 (resources):** asking what extra money could do is often practically obvious; it does not isolate resource control/autonomy from security or consumption.

Several original questions are useful for a general life-pattern narrative **without** a defensible chart linkage. Those should be retained as qualitative context or non-HD controls rather than forced into a reverse-match score.

## Mapping design and scientific gates

1. Independently define source-feature predictions, plausible rival features and question-level contrasts. Keep source classes (official HD theory vs prior owner-conditioned hypotheses) distinct. Publisher statements describe *the theory*, not empirical evidence that it is correct.
2. Use a new pinned question version, not a silent rewrite of live TF1 v1 or frozen v7. Conduct cognitive interviews with new people unfamiliar with the designer's intended answer. Check relevance, comprehensibility and comprehensiveness; ordinary reply variance is not automatically trait variance.
3. Blind human and model coders to all birth/chart targets. Require source quote + neutral construct + conditions + explicit alternative/counterexample; otherwise abstain. Measure inter-rater agreement separately from birth matching.
4. Freeze chart calculation, feature predicates, candidate set, conditional probabilities or explicitly symbolic scores, coding thresholds, dependency/duplicate caps, stopping rules, negative controls, baseline, and model/bank hashes **before** revealing true targets to any scoring pipeline.
5. Evaluate new people with paired same-person comparisons: prior fixed six-clause AstroHD model; new hypothesis bridge; simple Big Five-like trait or demographics baseline where ethical/consented; shuffled birth assignments; matched and broad decoy charts. Do not treat equivalent chart states as independent time hits.
6. Report every abstention, null, failure and adversarial alternative. More features increase chances of post-selection false positives; only *prospective improvement over controls* would justify richer model claims.

The proposed registry does **not** mix Human Design BodyGraph hypotheses with Lilly/Phaladeepika six-clause astrology. That second symbolic system needs its own separately sourced feature bridge and should be tested as another predeclared arm, not pooled after outcomes.

## Relevant methodological and theoretical references

- COSMIN content validity framework: <https://pubmed.ncbi.nlm.nih.gov/40562250/> (relevance, comprehensiveness, comprehensibility; framework adapted, not a claim Life Patterns is validated).
- COSMIN cognitive interview guidance: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5891557/>.
- AERA/APA/NCME *Standards for Educational and Psychological Testing*: <https://ncme.org/resources/books/testing-standards/>.
- Human Design theory claims: the source links appear individually in the machine-readable hypothesis registry. Their presence is not evidence for predictive validity.

## Existing artifacts intentionally left unchanged

- Participant-facing `tendency-first-v1.json`, custom GPT's interviews and Railway reviewed records.
- Historical frozen v7 scenario bank, six-rule AstroHD V1.5 bridge, owner development and failed V4.3 survey-crosswalk results.
- Existing separate 9-question v2-development rewrite, which remains non-live.

"""

sections = ["## Complete 25-question defect and mapping audit", ""]
for q in ROWS:
    t = [THEORY[x] for x in q["hypothesis_ids_behind_blind_wall"]]
    sections += [
        "### " + q["question_id"],
        "",
        "**Current question:** " + q["original_question"],
        "",
        "**Intended observable:** " + q["measured_construct"],
        "",
        "**Discriminating contrast:** " + q["discriminating_contrast"],
        "",
        "**Important confounds:** " + q["important_confounders"],
        "",
        "**Defect/limit:** " + q["defect_or_limit"].replace("_", " "),
        "",
        "**Mapping assessment:** " + q["target_link_status"].replace("_", " "),
        "",
        "**Potential chart hypothesis:** "
        + (
            "; ".join(x["source_feature_label"] + " [" + x["hypothesis_id"] + "]" for x in t)
            if t
            else "*No defensible direct chart link supplied.*"
        ),
        "",
    ]
    if q["draft_revised_question"]:
        sections += ["**Non-live revised wording:** " + q["draft_revised_question"], ""]
sections += ["## New, non-live targeted supplemental questions", ""]
for q in BRIDGE["supplement_question_candidates"]:
    sections += [
        "### " + q["draft_id"],
        "",
        q["candidate_question"],
        "",
        "**Limit:** " + q["coding_limit"],
        "",
        "**Chart hypotheses:** " + ", ".join(q["hypothesis_ids"]),
        "",
    ]
sections += ["## Source-based chart hypothesis codebook", ""]
for h in BRIDGE["theory_hypotheses"]:
    e = EVIDENCE[h["hypothesis_id"]]
    sections += [
        "### " + h["source_feature_label"] + " (" + h["hypothesis_id"] + ")",
        "",
        "**Provisional theoretical prediction:** " + h["theory_claim"],
        "",
        "**What might support this in repeated source:** "
        + e["positive_evidence_if_multiple_situations"],
        "",
        "**Possible counterevidence:** " + e["possible_counterevidence_not_automatic_inverse"],
        "",
        "**Do not infer when:** " + e["must_abstain_if"],
        "",
        "**Theory publisher:** " + h["theory_source_url"],
        "",
        "**Numeric score:** not defined; **empirical human validation:** absent.",
        "",
    ]

(TASK / "RICHER_MAPPING_AND_QUESTION_DEFECT_AUDIT.md").write_text(
    (summary + "\n".join(sections)).rstrip() + "\n"
)

cards = []
for q in ROWS:
    links = (
        " · ".join(
            esc(THEORY[x]["source_feature_label"]) for x in q["hypothesis_ids_behind_blind_wall"]
        )
        or "No defensible direct source link"
    )
    proposed = (
        (
            "<p><strong>Proposed wording, NOT LIVE</strong>: "
            + esc(q["draft_revised_question"])
            + "</p>"
        )
        if q["draft_revised_question"]
        else "<p><em>No replacement proposed; may be useful qualitative context.</em></p>"
    )
    status = q["target_link_status"]
    cards.append(
        '''<article class="question" data-search="'''
        + esc(
            " ".join(
                (
                    q["question_id"],
                    q["source_route_id"],
                    q["measured_construct"],
                    q["original_question"],
                    q["defect_or_limit"],
                )
            ).lower()
        )
        + '''" data-type="'''
        + ("linked" if q["hypothesis_ids_behind_blind_wall"] else "unlinked")
        + """">
<header><span class="id">"""
        + esc(q["question_id"])
        + """</span> <span class="pill">"""
        + esc(q["defect_or_limit"].replace("_", " "))
        + """</span></header>
<p class="question-text">"""
        + esc(q["original_question"])
        + """</p>
<details><summary>What it can measure / what it does NOT prove</summary>
<p><b>Observable dimension:</b> """
        + esc(q["measured_construct"])
        + """</p>
<p><b>Real distinction needed:</b> """
        + esc(q["discriminating_contrast"])
        + """</p>
<p><b>Confounds:</b> """
        + esc(q["important_confounders"])
        + """</p>
<p><b>Chart hypothesis status:</b> """
        + esc(status.replace("_", " "))
        + """ — """
        + links
        + """</p>
"""
        + proposed
        + """</details></article>"""
    )

theory_cards = []
for h in BRIDGE["theory_hypotheses"]:
    e = EVIDENCE[h["hypothesis_id"]]
    theory_cards.append(
        "<article><h3>"
        + esc(h["source_feature_label"])
        + "</h3><p><b>Theory claim:</b> "
        + esc(h["theory_claim"])
        + "</p><details><summary>Evidence, counterevidence and unknowns</summary><p><b>Potential evidence:</b> "
        + esc(e["positive_evidence_if_multiple_situations"])
        + "</p><p><b>Possible counterexample:</b> "
        + esc(e["possible_counterevidence_not_automatic_inverse"])
        + "</p><p><b>Do not code from:</b> "
        + esc(e["must_abstain_if"])
        + '</p></details><p class="foot"><a href="'
        + esc(h["theory_source_url"])
        + '" target="_blank" rel="noopener noreferrer">Theory-publisher source</a> · Proposed only; not scored or validated.</p></article>'
    )

css = """body{font:15px/1.55 system-ui,sans-serif;margin:0;background:#fafbfc;color:#232833}main{max-width:1100px;margin:auto;padding:30px 20px 70px}h1{font-size:27px;margin:4px 0 8px}h2{font-size:21px;margin-top:42px}p{max-width:100ch}article{background:white;border:1px solid #dbe0e5;border-radius:12px;padding:14px 20px;margin:12px 0;break-inside:avoid}header{display:flex;align-items:center;gap:12px}summary{cursor:pointer;font-weight:650;color:#213b64}details{margin:12px 0}.pill{font-size:12px;background:#edf0f5;padding:3px 9px;border-radius:999px}.id{font-weight:800;font-size:15px}.question-text{font-size:17px}input,select{font:inherit;padding:9px 11px;max-width:100%;border-radius:8px;border:1px solid #a6b1bd}input{width:360px}nav{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}.stat{background:#f3f6f9;border-radius:10px;padding:12px 17px}.summary{font-size:16px}.warning{border-left:4px solid #555;background:#f5f6f7;padding:15px}.foot{color:#667;font-size:13px}a{color:#174c8a}button{cursor:pointer}"""
body = (
    """<main><h1>Life Patterns · What each question can actually test</h1>
<p class="warning"><b>Research proposal, NOT a live questionnaire or validated birth decoder.</b> Human Design links are hypotheses from theory publishers, not empirical proof. The interviewed participant never sees chart targets.</p>
<div class="stat"><b>25 active questions audited</b> · 12 theory hypotheses · 10 potential but not scoring-ready question/chart links · 15 questions with no direct chart link · 4 new draft questions.</div>
<p class="summary"><b>Main finding:</b> all 25 live questions lack explicit target links, which is appropriate inside a blinded interviewer. The missing component is a separate, source-anchored construct-to-chart scoring protocol. Most plausible links fail the question-to-claim match without better questions.</p>
<h2>Current questions and detected limitations</h2>
<nav><input id="search" placeholder="Search question / trait / defect..." aria-label="Filter questions"><select id="type"><option value="all">All 25 questions</option><option value="linked">Potential chart links (not scored)</option><option value="unlinked">No direct chart link</option></select></nav>
<div id="questions">"""
    + "".join(cards)
    + """</div>
<h2>Four new supplemental question drafts (NOT LIVE)</h2>"""
    + "".join(
        "<article><h3>"
        + esc(q["draft_id"])
        + "</h3><p>"
        + esc(q["candidate_question"])
        + "</p><p>"
        + esc(q["coding_limit"])
        + "</p></article>"
        for q in BRIDGE["supplement_question_candidates"]
    )
    + """
<h2>Preliminary chart hypotheses and strict limits</h2>"""
    + "".join(theory_cards)
    + """
<h2>How to interpret a test correctly</h2><p>No source or chart feature has been empirically validated here. Never code general politeness, ordinary prudent decisions or question critiques as support. Abstain for ambiguity. Chart absence never implies the opposite personality. A new independent birth-data cohort must be scored against a fixed baseline and matched decoys after frozen mapping, coding and candidate-universe hashes.</p>
<p class="foot">Read the full audit and independent reference citations in RICHER_MAPPING_AND_QUESTION_DEFECT_AUDIT.md. Existing live v1, historical v7 and prior owner results remain unchanged.</p></main>"""
)
script = """const search=document.getElementById('search'),type=document.getElementById('type');
function update(){let query=search.value.toLowerCase().trim(),kind=type.value;document.querySelectorAll('.question').forEach(el=>{el.hidden=Boolean(query&&!el.dataset.search.includes(query))||(kind!=='all'&&kind!==el.dataset.type);});}search.addEventListener('input',update);type.addEventListener('change',update);"""
page = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Life Patterns: question defect and chart mapping audit</title><style>'
    + css
    + "</style></head><body>"
    + body
    + "<script>"
    + script
    + "</script></body></html>"
)
(TASK / "RESEARCHER_MAPPING_AUDIT.html").write_text(page)
print(
    "audit_questions",
    len(ROWS),
    "html_chars",
    len(page),
    "markdown_chars",
    len(summary + "\n".join(sections)),
)
