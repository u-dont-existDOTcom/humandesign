"""No-human-data tests for automatic V3 contextual follow-ups."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-guided-followup-20261014"
GENERATOR = ROOT / "tasks/life-patterns-idiographic-20261010"
HTML = GENERATOR / "LIFE_PATTERNS_V3_OFFLINE_PILOT.html"
BANK = json.loads((GENERATOR / "tendency-first-v3-scaffold-development.json").read_text())
ROUTES = ["TF1-G01", "TF1-G02", "TF1-G16", "TF1-G23", "TF1-M05", "TF1-G20", "TF1-M01", "TF1-M03"]


def module():
    spec = importlib.util.spec_from_file_location(
        "make_private_guided", TASK / "make_private_prefilled.py"
    )
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_eight_routes_and_automatic_flow_are_source_neutral():
    html = HTML.read_text()
    generator = (GENERATOR / "build_interactive_pilot.py").read_text()
    assert all(x in html and x in generator for x in ROUTES)
    assert html.count('id="guided-section"') == 1
    assert "guidedBegin();" in html
    assert "if(d.prefilled_export)" in html
    assert "context_skipped" in html
    assert "function guidedNextOutstanding" in html
    assert "no stable default" in html.lower()
    assert "context_rule" in html
    assert "state.answers[id]={" in html
    guided_text = html.split('<section id="guided-section"', 1)[1].split("</section>", 1)[0]
    assert all(x not in guided_text.lower() for x in ("neptune", "birth time", "psychedelic"))
    assert "fetch(" not in html
    assert "XMLHttpRequest" not in html


def test_owner_private_prefill_preserves_synthetic_answers_without_html_execution(tmp_path):
    answer = {
        "schema": "local_life_patterns_v3_pilot_unsubmitted",
        "answers": {
            q["id"]: {
                "selected": [q["example_answer_paths"][0]],
                "other": '<script>alert("synthetic")</script>',
                "unsure": False,
                "skip": False,
            }
            for q in BANK["questions"]
        },
        "unique_behaviors": [{"behavior": "Synthetic <img src=x onerror=alert(1)> example."}],
    }
    source = tmp_path / "synthetic.json"
    source.write_text(json.dumps(answer))
    output = tmp_path / "private.html"
    receipt = module().prefill(HTML, source, output)
    assert receipt["questions"] == 25 and receipt["behavior_items"] == 1
    assert output.stat().st_mode & 0o777 == 0o600
    data = output.read_text()
    assert '<script>alert("synthetic")</script>' not in data
    assert "<img src=x onerror" not in data
    marker = '<script id="pilot-data" type="application/json">'
    structured = json.loads(data.split(marker, 1)[1].split("</script>", 1)[0])
    assert structured["prefilled_export"] == answer
    assert "Review all eight" in data


def test_malformed_input_is_rejected_before_private_file_written(tmp_path):
    output = tmp_path / "private.html"
    source = tmp_path / "synthetic.json"
    source.write_text(
        json.dumps(
            {
                "schema": "local_life_patterns_v3_pilot_unsubmitted",
                "answers": {},
                "unique_behaviors": [],
            }
        )
    )
    with pytest.raises(ValueError, match="25 answered"):
        module().prefill(HTML, source, output)
    assert not output.exists()


def test_owner_researcher_guide_links_to_private_file_without_embedded_answers(tmp_path):
    guide = tmp_path / "Life-Patterns-Researcher-Guide.html"
    guide.write_text("<html><body><h1>Existing guide</h1></body></html>")
    private = tmp_path / "Life-Patterns-8-Guided-Followups-PRIVATE-2026-10-14.html"
    private.write_text("PRIVATE_SYNTHETIC_RESPONSE_EXAMPLE")
    spec = importlib.util.spec_from_file_location("guide_install", TASK / "install_owner_guide.py")
    assert spec and spec.loader
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    assert installer.install(guide, private)["ready"]
    assert installer.install(guide, private)["ready"]
    source = guide.read_text()
    assert source.count(private.name) == 1
    assert "Answer my eight context follow-ups" in source
    assert "PRIVATE_SYNTHETIC_RESPONSE_EXAMPLE" not in source
