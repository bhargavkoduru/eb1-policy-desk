# Examiner demo deployment

This version is ready for Streamlit Community Cloud. It serves both Week 2 and Week 3 modes from `app.py`. The public USCIS corpus and its precomputed index are included; cloud startup makes no parsing or embedding calls.

## Final account steps

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account. Authorize access to the project repository if requested.
2. Choose **Create app**, select repository `bhargavkoduru/eb1-policy-desk`, branch `main`, entrypoint **`app.py`**, and Python **3.12** under Advanced settings.
3. In Advanced settings → Secrets, paste the contents of the local file `runtime/deployment/streamlit.secrets.toml`. Do not upload this file to GitHub or put it in a Google Doc. It contains the Nebius key and hashed viewer access codes.
4. Click **Deploy**. Verify that the first screen requires sign-in and that a cited answer works after login. Copy the URL Streamlit actually assigns; an example URL is not evidence of a successful deployment.

The owner and examiner usernames/codes are in the local **`runtime/deployment/VIEWER_ACCESS.txt`**. Provide only the examiner login through your private submission channel. Anyone sharing one username shares that username's workspace; create a separate viewer account for each person who needs isolated history.

If Streamlit also restricts the app to invited viewers, add the examiner in its Sharing settings. A private GitHub repository also requires examiner repository access for code review. App-level login remains required even when Streamlit's sharing setting is public.

These last account steps require your Streamlit sign-in. GitHub authentication in the development environment does not automatically sign in to Streamlit Community Cloud.

## What changed for hosting

- The app defaults to hosted mode and stops before corpus/model access if viewer credentials are missing.
- Access codes are randomly generated, stored as PBKDF2-SHA256 hashes in cloud secrets, and compared on the server. Eight attempts per username and 100 globally are allowed in a rolling ten-minute period.
- Each authenticated username maps to a separate SQLite directory. A viewer cannot list or open another account's research sessions by changing a session ID. Sign-out clears the browser session state; credential changes revoke existing app sessions on their next rerun.
- Public retrieval resources are shared; private research services are cached separately by viewer identity.
- Only one live model operation runs at a time. Defaults are 30 actions per viewer per UTC day, 100 actions globally, 120 reserved provider attempts per viewer, and 400 globally. Each provider invocation reserves two attempts to cover its one possible retry. This conservative allowance counts unused retry capacity too.
- Set `EB1_ENABLE_LIVE_CALLS = false` in cloud secrets to pause model requests. Viewing, editing, cancelling and saving an already prepared draft do not invoke models.
- These are request limits, not a guaranteed dollar spending cap. They persist only while the server's local usage database survives. A redeploy/storage reset resets its counters; use provider-level billing controls for stronger account-wide limits.
- The checked public index restores automatically from `corpus/index/`, with source fingerprint and file checksum validation. Nebius is used only when a signed-in viewer makes a live request.

## Storage limitations

On this computer, SQLite sessions persist across app restarts. On Community Cloud, **local file persistence is not guaranteed**. Browser refresh and sign-in reuse the server's existing workspace, but a platform rebuild/replacement can remove research history and usage counters. The hosted UI states this limitation and provides approved-checklist downloads. Keep the local version for the Week 3 restart demonstration, or use an external database if guaranteed hosted durability is required.

The owner of the server can access its data. Viewer isolation is not encryption from the app owner. This demo accepts public policy questions and has no candidate upload feature.

## Local use and tests

In PowerShell, set `$env:EB1_HOSTED='false'` and run Streamlit with `--server.address 127.0.0.1`, or use `start.ps1`. Local mode refuses to start on a non-loopback bind address.

Run `python -m pytest -q tests`. The hosting tests cover password verification, missing configuration, real login/logout form interactions, cross-viewer workspace isolation, atomic quotas, login limits, credential-free index startup and identity propagation into LangGraph tools. They use fake credentials and do not call Nebius.

Sources: [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [secret management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [local storage limitations](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data).
