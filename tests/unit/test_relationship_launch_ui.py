from __future__ import annotations

from hdmatch.api.relationship_launch_ui import HTML


def test_launch_page_makes_natal_astrohd_the_first_test() -> None:
    assert "Start with one person" in HTML
    assert "First test" in HTML
    assert 'href="/astrohd/"' in HTML
    assert "A relationship claim depends" in HTML
    assert "Secondary development mode" in HTML
    assert 'href="/relationship"' in HTML
    assert "silently changes its model" in HTML
