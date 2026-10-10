"""Install source-only research audit beside existing Life Patterns question atlas."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def downloads() -> Path:
    try:
        path = subprocess.check_output(["xdg-user-dir", "DOWNLOAD"], text=True, timeout=5).strip()
        if path:
            return Path(path)
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.home() / "Downloads"


def install(base: Path) -> dict:
    report_dir = base / "Life-Patterns-Richer-Mapping-2026-10-10"
    report_dir.mkdir(parents=True, exist_ok=True)
    filenames = [
        "RESEARCHER_MAPPING_AUDIT.html",
        "RICHER_MAPPING_AND_QUESTION_DEFECT_AUDIT.md",
        "question_to_chart_hypotheses_v0.json",
        "source_to_target_evidence_codebook_v0.json",
        "ASTROHD_SIX_RULE_EXPANSION_ASSESSMENT.md",
        "ASTROHD_SIX_RULE_BASELINE_AND_EXPANSION_BOUNDARY.json",
    ]
    for name in filenames:
        shutil.copy2(HERE / name, report_dir / name)
    landing = base / "Life-Patterns-Researcher-Guide.html"
    index_modified = False
    target = "Life-Patterns-Richer-Mapping-2026-10-10/RESEARCHER_MAPPING_AUDIT.html"
    snippet = (
        '<article><h2><a href="'
        + target
        + '">New: richer chart-mapping hypotheses and questionnaire defects</a></h2><p>Audit of 25 current questions, 12 theory hypotheses, links that are not yet scoring-ready, and proposed revisions. NOT the live questionnaire or a validated birth-time decoder.</p></article>'
    )
    if landing.exists():
        current = landing.read_text()
        if target not in current:
            assert "</body>" in current
            modified = current.replace("</body>", snippet + "</body>")
            temp = landing.with_name(landing.name + ".tmp")
            temp.write_text(modified)
            os.replace(temp, landing)
            index_modified = True
        assert target in landing.read_text()
        assert (base / target).is_file()
    else:
        landing = report_dir / "RESEARCHER_MAPPING_AUDIT.html"
    return {
        "delivered_files": len(filenames),
        "landing_link_present": target in landing.read_text()
        or landing == report_dir / "RESEARCHER_MAPPING_AUDIT.html",
        "index_updated": index_modified,
        "report_dir": str(report_dir),
    }


if __name__ == "__main__":
    print(install(downloads()))
