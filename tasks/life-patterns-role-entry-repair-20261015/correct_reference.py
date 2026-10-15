# ruff: noqa: E501
"""Repair the previous owner's comparison reference (V4.3 was not the accepted reference).

The old source comparison remains identical; only misleading reference assertions,
aggregation labels and report prose change. No private input enters Git.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tasks/life-patterns-v32-owner-comparison-20261015"
REPORT = BASE / "compare_private_owner.py"


def exactly(text: str, old: str, new: str) -> str:
    if new in text and old not in text:
        return text
    n = text.count(old)
    if n != 1:
        raise ValueError(f"Unexpected reference anchor count {n}: {old[:75]}")
    return text.replace(old, new, 1)


def fix() -> None:
    s = REPORT.read_text(encoding="utf-8")
    swaps = [
        (
            "V43-SURVEY-CROSSWALK-RESULT-20260923.md",
            "ASTROHD-V14-EXACT-CENTURY-RECEIPT-20260925.md",
        ),
        (
            'assert "ranked **#1562**" in baseline, "Prior frozen V4.3 rank not confirmed"',
            'assert "Exactly nine instants reach it" in baseline, "Accepted V1.4d maxima not confirmed"',
        ),
        (
            'assert "The exact recorded moment" in baseline, "Prior frozen recorded instant not confirmed"',
            'assert "recorded 10:25 is jointly first" in baseline, "Accepted V1.4d instant not confirmed"',
        ),
        (
            'assert "2013-01-28/29" in baseline, "Prior top interval not confirmed"',
            'assert "January 29, 1985 is the sole maximum-scoring date" in baseline, "Accepted V1.4d date not confirmed"',
        ),
        (
            '"prior_frozen_v43_exact_recorded_interval_rank": 1562,\n        "prior_frozen_v43_top_interval": "2013-01-28/29",',
            '"accepted_reference_model": "astrohd-v14-v1.4d",\n        "accepted_reference_recorded_instant_joint_first": True,\n        "accepted_reference_tied_minute_count": 9,\n        "accepted_reference_unique_maximum_date": "1985-01-29",',
        ),
        (
            "<p><strong>Birth-date test:</strong> zero new V3.2 questions have an admitted chart mapping or weight. A new V3.2 date ranking would be arbitrary, so none was performed. The earlier <em>frozen V4.3 survey translation</em> placed the exact recorded birth-time interval at <strong>#1,562</strong>; the strongest interval was January 28–29, 2013. This is a historical result, not a fresh ranking or an improved model.</p>",
            "<p><strong>Accepted birth-date reference:</strong> AstroHD V1.4d, six equal-vote clauses, 52,596,001 minute-grid candidates: January 29, 1985 is the only maximum-scoring calendar day. Nine nearby minutes (10:18–10:26 UTC) tie for first, including the recorded 10:25 UTC. This six-rule signature was fitted to the known owner case; it is not independent DOB recovery. The older V4.3/NetInformation comparison is a different, discarded diagnostic and must not replace this benchmark. No new V3.2 reranking was performed. The existing V1.5 five-domain behavioral bridge and its unconfirmed role-entry interpretation remain separate.</p>",
        ),
        (
            "**No new V3.2 DOB inference was possible.** All eight new prompts have zero chart-admitted mappings, and no score updates were run. The previously frozen V4.3 survey crosswalk ranked the actual recorded instant's stable interval **#1,562**, not first; the top interval was January 28–29, 2013. This is a prior result, not a new test.",
            "**Accepted reference:** AstroHD V1.4d's fixed six-rule century scan found the recorded 10:25 UTC instant **joint #1** among nine maximum-scoring minutes, all on January 29, 1985, within a 52,596,001-minute grid. It was fitted using the known development case and is not independent recovery. The older V4.3/NetInformation #1,562 diagnostic is **discarded as the comparison benchmark**, not retconned as the latest result. None of the eight new V3.2 prompts added a scored mapping or new rank. The existing V1.5 bridge can score confirmed five-domain responses, but the usual role-entry interpretation remains unresolved.",
        ),
    ]
    for old, new in swaps:
        s = exactly(s, old, new)
    REPORT.write_text(s, encoding="utf-8")

    # Research note and previous release receipt are amended, not deleted:
    for name in ("PLAN.md", "RESULT.md"):
        p = BASE / name
        text = p.read_text()
        paragraph = (
            "\n\n## Reference correction — 2026-10-15\n\n"
            "The prior V4.3 NetInformation #1,562 description in this historical note is **not the accepted comparator**. "
            "Owner-corrected reference: fitted six-rule AstroHD V1.4d's 52,596,001-minute century scan. "
            "On its one-minute grid, all nine maximum-scoring minutes occur on January 29, 1985 "
            "(10:18–10:26 UTC), including the recorded time (joint #1). "
            "The V1.5 five-domain behavioral bridge exists separately; determining typical meaningful "
            "role-entry sequence from actual episodes is the remaining measurement gap. "
            "Read the correction as superseding—not deleting—the obsolete benchmark text above. "
            "No new participant DOB recovery is claimed.\n"
        )
        if "## Reference correction — 2026-10-15" not in text:
            p.write_text(text + paragraph)
    receipt = BASE / "VERIFICATION-RECEIPT.json"
    data = json.loads(receipt.read_text())
    data["birth_date_audit"] = {
        "accepted_reference": "astrohd-v14-v1.4d",
        "scanned_minutes": 52596001,
        "recorded_instant_joint_first": True,
        "maximal_minutes": 9,
        "single_maximal_calendar_date": "1985-01-29",
        "reference_fitted_with_known_developer_birth": True,
        "prior_v43_rank_reference_disposition": "DISCARDED_AS_REFERENCE",
        "v32_new_chart_predicates_admitted": 0,
        "new_v32_reranking_executed": False,
        "existing_v15_behavioral_bridge_available": True,
        "role_entry_typicality_resolved": False,
    }
    receipt.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("CORRECTED_PREVIOUS_REFERENCE_NO_NEW_DOB_SEARCH")


if __name__ == "__main__":
    fix()
