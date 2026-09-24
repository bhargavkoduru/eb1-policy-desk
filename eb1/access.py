"""Small invited-viewer login; no credentials or viewer identities in Git."""
import base64
import hashlib
import hmac
import os
import re
from pathlib import Path
from .config import RUNTIME, hosted, setting
from .usage import UsageLimitError, ledger


def password_hash(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600_000)
    return 'pbkdf2_sha256$600000$' + base64.b64encode(salt).decode() + '$' + base64.b64encode(key).decode()


def verify_password(password, stored):
    try:
        method, count, salt, expected = stored.split('$')
        if method != 'pbkdf2_sha256' or not 100_000 <= int(count) <= 2_000_000:
            return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), base64.b64decode(salt, validate=True), int(count))
        return hmac.compare_digest(actual, base64.b64decode(expected, validate=True))
    except (ValueError, TypeError, AttributeError):
        return False


def normalize_username(name):
    name = name.strip().lower()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{0,63}', name):
        raise ValueError('Invalid username')
    return name


def workspace_id(username):
    return hashlib.sha256(('eb1-viewer:' + normalize_username(username)).encode()).hexdigest()


def viewer_runtime(viewer):
    if viewer == 'local' and not hosted():
        return RUNTIME
    if not re.fullmatch(r'[0-9a-f]{64}', viewer):
        raise PermissionError('Invalid viewer identity')
    return RUNTIME / 'viewers' / viewer


def require_viewer():
    import streamlit as st
    if not hosted():
        if st.get_option('server.address') not in ('127.0.0.1', 'localhost', '::1'):
            st.error('Local mode must bind to 127.0.0.1. Use start.ps1 or add --server.address 127.0.0.1.')
            st.stop()
        return 'local'
    viewers = setting('viewers', {})
    if not viewers:
        st.error('The examiner demo is awaiting its private access settings. The owner must configure viewer credentials before it can be used.')
        st.stop()
    session = st.session_state.get('_viewer_auth', {})
    username = session.get('username', '')
    current_hash = str(viewers.get(username, ''))
    if current_hash and hmac.compare_digest(session.get('version', ''), hashlib.sha256(current_hash.encode()).hexdigest()):
        with st.sidebar:
            st.caption('Signed in as ' + username)
            if st.button('Sign out'):
                st.session_state.clear()
                st.rerun()
        return workspace_id(username)
    # No previous viewer's question or selected research ID survives logout/rotation.
    if session:
        st.session_state.clear()
    st.subheader('Examiner access')
    st.write('Sign in using the username and access code provided by the project owner.')
    with st.form('viewer_login', clear_on_submit=True):
        name = st.text_input('Username', max_chars=64)
        password = st.text_input('Access code', type='password', max_chars=256)
        submit = st.form_submit_button('Sign in', type='primary')
    if submit:
        try:
            name = normalize_username(name)
            ledger().login_attempt(workspace_id(name))
            stored = str(viewers.get(name, ''))
            if not verify_password(password, stored):
                st.error('The username or access code is incorrect.')
            else:
                st.session_state.clear()
                st.session_state['_viewer_auth'] = {'username': name, 'version': hashlib.sha256(stored.encode()).hexdigest()}
                st.rerun()
        except UsageLimitError as exc:
            st.warning(str(exc))
        except ValueError:
            st.error('The username or access code is incorrect.')
    st.stop()
