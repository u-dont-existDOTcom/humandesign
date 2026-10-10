"""Preserve the original six-clause astrology baseline as its own model arm."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ORIGINAL = ROOT / "reference/research/astrohd_v15_behavioral_bridge.json"
base = json.loads(ORIGINAL.read_text())
rows = []
for r in base["rules"]:
    rows.append(
        {
            "original_rule_id": r["rule_id"],
            "original_behavioral_domains": r["domain_ids"],
            "source_prediction_paraphrase": r["hypothesis"],
            "changed_in_this_version": False,
            "new_rules_added": False,
            "admitted_as_independent_validation": False,
        }
    )
plan = {
    "schema": "astrohd-theory-to-behavior-expansion-boundary-v0",
    "status": "DEVELOPMENT_RESEARCH_PROTOCOL_ONLY_NOT_A_NEW_MODEL",
    "frozen_baseline_sha256": hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
    "frozen_baseline_version": base["version"],
    "source_paths": {"original_bridge": str(ORIGINAL.relative_to(ROOT))},
    "original_six_clauses_unchanged": rows,
    "domain_count_original": len(base["domains"]),
    "new_astro_claims": [],
    "no_new_clause_inference": "Richer text answers cannot add independent chart bits when scored through the same fixed six Boolean astrology clauses.",
    "required_claim_for_expansion": [
        "Extract a new objective astronomical predicate directly from a specified classical source, including page/section, edition/translation and exact eligibility conditions.",
        "Freeze its chart-side truth definition independent of every known person and birth time; record conjunction/dependency with old six rules.",
        "Specify a falsifiable behavioral proposition and plausible alternative from source, not extrapolate from owner anecdotes or chart knowing.",
        "Design respondent-blind question and behavioral evidence threshold with negative and unknown rules; pre-register each before new-person testing.",
        "Verify chart computation for selected universe/timezones and report stable time intervals (not arbitrary isolated minutes).",
        "Compare to original six-rule baseline and independent non-astrological controls on untouched people, with all negative/null cases.",
    ],
    "candidate_sources": [
        {
            "work": "William Lilly Christian Astrology",
            "policy": "source-read_complete_applied_rules_not_yet_frozen_for_new_cohort",
        },
        {
            "work": "Phaladeepika",
            "policy": "primary_text_source_edition_page_and_translation_required",
        },
        {
            "work": "Other Hellenistic/Jyotish sources",
            "policy": "separate_rulesets_and_dependency_audit_before_prospective_admission",
        },
    ],
    "warning": "Owner historical six-rule fit is DEVELOPMENT. Do not call expanding after seeing their DOB or outcomes prospective validation.",
}
(HERE / "ASTROHD_SIX_RULE_BASELINE_AND_EXPANSION_BOUNDARY.json").write_text(
    json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
)
lines = [
    "# AstroHD astrology arm — frozen six-rule baseline vs richer new test",
    "",
    "**This is a separate problem from the Human Design question-to-feature prototype.** No new astrology clause is admitted or scored by this draft.",
    "",
    "The historical bridge uses six binary chart rules and five self-report domains. Six bits of deterministic clause identity allow **at most 64 possible six-clause signatures**; very rare conjunctions may still occur, but the system cannot represent hundreds of independently varying chart dimensions simply by asking more questions about the same six rule outputs. Repeated domains are not additional independent evidence.",
    "",
    "| Frozen historical rule | Existing neutral behavioral domains |",
    "|---|---|",
]
for r in rows:
    lines.append(
        "| `" + r["original_rule_id"] + "` | " + ", ".join(r["original_behavioral_domains"]) + " |"
    )
lines += [
    "",
    "## For a richer future test",
    "",
    "- Obtain source-complete rulebooks and preserve literal page/translation context for every NEW astronomical predicate. Do not take a favorable interpretation from the recorded owner chart and label it theory independent.",
    "- Freeze the chart-side predicate, feature dependence, neutral behavioral hypothesis, positive/contradictory/unknown codes, trait questions, model comparison, broad candidate universe and decoys **before** testing new people.",
    "- Keep original V1.5 six clauses as a negative/positive reference arm. Do not claim that four new questionnaire prompts change V1.5 rankings if they do not change its five frozen domain codes.",
    "- Human Design BodyGraph, Lilly/Phaladeepika astrology, generic personality, occupation and demographic baselines are different arms with separate contribution and null reporting. Combine only if a *new, predeclared* joint model earns out-of-sample gain.",
    "- Project materials already include older source/mapping revisions, but their outcome-informed rules are development hypotheses, not untouched validation. Unknown theory-to-person links remain unresolved.",
    "",
    "**Next milestone:** source-complete, independently frozen expanded AstroHD rule manifest plus cognitive-tested respondent questions, then first untouched human pilot. Not another rescore of the known owner DOB.",
    "",
]
(HERE / "ASTROHD_SIX_RULE_EXPANSION_ASSESSMENT.md").write_text("\n".join(lines))
print("preserved astrology six-clause baseline count", len(rows))
