"""Researcher login UI must not display empty counts when authentication is missing."""
from __future__ import annotations

from test_gpt_submission_action import auth, setup_submission


def test_admin_unlock_displays_access_guidance_and_no_fake_zero(tmp_path):
    settings, _, _, client = setup_submission(tmp_path)
    page = client.get('/admin')
    assert page.status_code == 200
    assert 'researcher-access' in page.text
    assert 'researcher-key' in page.text
    assert 'researcher-unlock' in page.text
    assert 'No record counts' in page.text or 'Records cannot be loaded' in page.text
    script = client.get('/assets/admin.js')
    assert script.status_code == 200
    assert 'if(key){refresh();refreshSubmissions();refreshQuestionFeedback();}' in script.text
    assert 'else{el("status").textContent="Researcher access required. No record counts have been loaded.";}' in script.text
    assert 'sessionStorage.setItem("lp_admin",key)' in script.text
    assert 'Researcher key was rejected' in script.text
    assert 'sessionStorage.removeItem("lp_admin")' in script.text
    assert 'el("researcher-lock")' in script.text
    assert client.get('/api/admin/question-feedback').status_code == 401
    assert client.get('/api/admin/question-feedback', headers=auth(settings.admin_token)).status_code == 200
