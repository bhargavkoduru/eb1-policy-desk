from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
from eb1 import access, bootstrap, usage
from eb1.research import ResearchAgent
from eb1.usage import UsageLedger, UsageLimitError

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def test_password_hash_validation():
    stored = access.password_hash('random-test-access-code')
    assert access.verify_password('random-test-access-code', stored)
    assert not access.verify_password('incorrect', stored)
    assert not access.verify_password('anything', 'invalid')
    assert not access.verify_password('anything', 'pbkdf2_sha256$999999999$abc$def')


def test_workspace_separation_and_path_rejection(tmp_path, monkeypatch):
    monkeypatch.setenv('EB1_HOSTED', 'true')
    monkeypatch.setattr(access, 'RUNTIME', tmp_path)
    alice = access.viewer_runtime(access.workspace_id('alice'))
    bob = access.viewer_runtime(access.workspace_id('bob'))
    assert alice != bob and alice.is_relative_to(tmp_path)
    with pytest.raises((ValueError, PermissionError)):
        access.viewer_runtime('../../alice')
    with pytest.raises(PermissionError):
        access.viewer_runtime('local')
    planner = lambda *args: {'action': 'handoff', 'message': 'test only'}
    a = ResearchAgent(None, alice, planner=planner)
    b = ResearchAgent(None, bob, planner=planner)
    ident = a.start('Private research question', 'EB-1A')
    assert a.store.sessions()[0]['id'] == ident
    assert b.store.sessions() == []
    assert not b.snapshot(ident).values
    assert b.store.load(ident) == []
    a.close()
    b.close()


def test_atomic_usage_and_global_limit(tmp_path):
    meter = UsageLedger(tmp_path / 'usage.sqlite')
    def attempt(i):
        try:
            meter.reserve('viewer' + str(i % 2), 'attempts', 1, 100, 5)
            return 1
        except UsageLimitError:
            return 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(16))) == 5
    restarted = UsageLedger(tmp_path / 'usage.sqlite')
    with pytest.raises(UsageLimitError):
        restarted.reserve('new-viewer', 'attempts', 1, 100, 5)


def test_viewer_limit_and_failed_login_limit(tmp_path):
    meter = UsageLedger(tmp_path / 'usage.sqlite')
    meter.reserve('alice', 'attempts', 2, 2, 20)
    with pytest.raises(UsageLimitError):
        meter.reserve('alice', 'attempts', 1, 2, 20)
    meter.reserve('bob', 'attempts', 1, 2, 20)
    for _ in range(8):
        meter.login_attempt('alice')
    with pytest.raises(UsageLimitError):
        meter.login_attempt('alice')


def test_provider_denied_without_actor_and_kill_switch(tmp_path, monkeypatch):
    monkeypatch.setenv('EB1_HOSTED', 'true')
    monkeypatch.setattr(usage, 'RUNTIME', tmp_path)
    with pytest.raises(UsageLimitError):
        usage.reserve_provider_calls()
    with usage.live_operation('alice'):
        usage.reserve_provider_calls()
    monkeypatch.setenv('EB1_ENABLE_LIVE_CALLS', 'false')
    with pytest.raises(UsageLimitError):
        with usage.live_operation('alice'):
            pytest.fail('Paused demo must not execute a call')


def test_graph_threads_keep_authenticated_actor(tmp_path, monkeypatch):
    monkeypatch.setenv('EB1_HOSTED', 'true')
    monkeypatch.setattr(usage, 'RUNTIME', tmp_path / 'meter')
    seen = []
    def planner(*args):
        seen.append(usage._actor.get())
        usage.reserve_provider_calls()
        return {'action': 'handoff', 'message': 'Done'}
    agent = ResearchAgent(None, tmp_path / 'agent', planner=planner)
    with usage.live_operation('alice'):
        ident = agent.start('A public question', 'EB-1A')
    assert seen == ['alice']
    assert agent.snapshot(ident).values['message'] == 'Done'
    agent.close()


def test_cloud_bootstrap_without_api_calls(tmp_path, monkeypatch):
    monkeypatch.setattr(bootstrap, 'INDEX', tmp_path / 'index')
    bootstrap.ensure_index()
    assert (tmp_path / 'index/vectors.npy').exists()
    manifest = json.loads((tmp_path / 'index/manifest.json').read_text())
    assert manifest['chunks'] == 65
    bootstrap.ensure_index()  # Existing complete copy remains reusable.


def test_missing_auth_configuration_stops_before_app(monkeypatch):
    monkeypatch.setenv('EB1_HOSTED', 'true')
    monkeypatch.setattr(access, 'setting', lambda name, default=None: {} if name == 'viewers' else default)
    st.cache_resource.clear()
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception
    assert any('awaiting its private access settings' in e.value for e in app.error)
    assert not any(b.label == 'Find a cited answer' for b in app.button)


def test_login_logout_and_relogin_keep_workspaces_separate(tmp_path, monkeypatch):
    monkeypatch.setenv('EB1_HOSTED', 'true')
    monkeypatch.setattr(access, 'RUNTIME', tmp_path / 'viewers')
    monkeypatch.setattr(usage, 'RUNTIME', tmp_path / 'meter')
    viewers = {'alice': access.password_hash('alice-test-code'), 'bob': access.password_hash('bob-test-code')}
    monkeypatch.setattr(access, 'setting', lambda name, default=None: viewers if name == 'viewers' else default)
    st.cache_resource.clear()
    app = AppTest.from_file(APP, default_timeout=20).run()
    assert not app.exception
    app.text_input[0].set_value('alice')
    app.text_input[1].set_value('alice-test-code')
    next(b for b in app.button if b.label == 'Sign in').click().run()
    assert not app.exception
    assert any(b.label == 'Find a cited answer' for b in app.button)
    app.session_state['last_answer'] = {'question': 'private alice content'}
    # Logout happens before any previous answer can be rendered again.
    next(b for b in app.sidebar.button if b.label == 'Sign out').click().run()
    assert not app.exception
    app.text_input[0].set_value('bob')
    app.text_input[1].set_value('bob-test-code')
    next(b for b in app.button if b.label == 'Sign in').click().run()
    assert not app.exception
    assert all('private alice content' not in m.value for m in app.markdown)
    assert app.session_state['_viewer_auth']['username'] == 'bob'
    st.cache_resource.clear()
