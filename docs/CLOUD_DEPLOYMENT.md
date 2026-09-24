# Public examiner demo deployment

One Streamlit app serves both Week 2 Policy Q&A and Week 3 Research checklist. It opens without a password. Code is at https://github.com/bhargavkoduru/eb1-policy-desk; the hosted URL is still pending the owner's deployment steps below.

## Owner setup, once

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
2. Choose **Create app**, repository `bhargavkoduru/eb1-policy-desk`, branch `main`, entrypoint **`app.py`**, and Python **3.12** in Advanced settings.
3. In Advanced settings > Secrets, paste the contents of the local file `runtime/deployment/streamlit.secrets.toml`. This contains the owner's Nebius key and usage settings. Keep it out of GitHub and Google Docs. No viewer credentials are needed. For a fresh checkout, add your own key to `.env` and run `python -m scripts.prepare_cloud_secrets` first.
4. Click **Deploy**. In Sharing settings, make the app **public** so anyone with its URL can view it. If updating an earlier deployment, replace the old secrets with the regenerated file and remove the obsolete `[viewers]` section.
5. Open the actual assigned URL in a private/incognito browser window. It should open directly to the app, without a sign-in screen. Check one cited answer and one reviewed checklist save/download. The examiner needs neither your Streamlit account nor an API key.
6. Add that same URL to the README and both week's submission drafts. Each submission identifies its own sidebar mode. Do not use the local `127.0.0.1` address as the examiner link.

These steps require the owner's Streamlit browser sign-in. GitHub CLI authentication does not automatically create a Streamlit deployment. `VIEWER_ACCESS.txt` is obsolete as a credential file and now explains that no examiner login is needed.

## Examiner experience

Open the link, select the relevant week, and use the app. Week 2 displays cited answers and supporting passages. Week 3 researches a question, pauses for human review, allows edits or cancellation, and saves a final checklist only after approval. Download the approved checklist before refreshing or closing the page.

Each browser session receives a random server-generated workspace. It cannot select another workspace through a URL parameter. The public retriever is shared; the research agent and its SQLite directory are separate per browser session. Questions and excerpts go to Nebius. There are no candidate uploads in this version.

## Usage and state

- The Nebius key stays in server secrets. Public source text and a precomputed index are bundled, so startup needs no new parsing or embedding calls.
- One live model operation runs at a time. Default UTC-day allowances: 30 actions and 120 reserved provider attempts per browser session, 100 actions and 400 attempts across the app. Each provider invocation reserves two attempts to cover one retry.
- A new browser session gets a new session allowance but does not reset the global allowance. These are request limits, not a guaranteed monetary cap. A server storage reset can clear the counters.
- Set `EB1_ENABLE_LIVE_CALLS = false` in server secrets to pause new model calls. Review, edit, cancel, and saving an existing draft remain available.
- **Hosted work is temporary.** Refreshing or closing the page loses the anonymous workspace identity. Its server files are not immediately deleted, but a platform rebuild can clear them. The server owner can access stored questions and checklists.
- **Local mode retains state across restarts.** Use the local app for the Week 3 checkpoint/restart demonstration. Hosted visitors can resume and edit during their active browser session, and keep approved work by downloading it.

## Validation

`python -m pytest -q tests` passes 28 tests locally. These cover both app modes without examiner credentials, independent browser sessions (including attempted workspace selection via URL), local restart recovery, approval enforcement, atomic global limits, provider-call metering and index startup without API calls. Tests do not call Nebius. [GitHub Actions](https://github.com/bhargavkoduru/eb1-policy-desk/actions/workflows/tests.yml) runs the suite on Ubuntu with Python 3.12.

For local use, set `$env:EB1_HOSTED='false'` and run with `--server.address 127.0.0.1`, or use `start.ps1`.

Sources: [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [public sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), [server secrets](https://docs.streamlit.io/deploy/concepts/secrets), and [browser-session lifetime](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state).
