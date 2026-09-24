"""Render both Streamlit milestones without model calls."""
from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_both_milestones_render():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=20).run()
    assert not app.exception
    assert app.title[0].value == 'EB-1 Policy Desk'
    assert any(b.label == 'Find a cited answer' for b in app.button)
    app.sidebar.radio[0].set_value('Week 3 · Research checklist').run()
    assert not app.exception
    assert any(b.label == 'Start research' for b in app.button)
