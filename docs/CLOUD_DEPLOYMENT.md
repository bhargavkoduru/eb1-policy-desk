# Deploy the separate weekly submissions

Each week now has its own public repository and standalone `app.py`:

| Submission | Repository | Deployment instructions |
| --- | --- | --- |
| Week 2 | [EB-1 Policy Q&A](https://github.com/bhargavkoduru/eb1-policy-qa-week2) | [Week 2 setup](https://github.com/bhargavkoduru/eb1-policy-qa-week2/blob/main/docs/CLOUD_DEPLOYMENT.md) |
| Week 3 | [EB-1 Research Agent](https://github.com/bhargavkoduru/eb1-research-agent-week3) | [Week 3 setup](https://github.com/bhargavkoduru/eb1-research-agent-week3/blob/main/docs/CLOUD_DEPLOYMENT.md) |

1. Sign in as the owner to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create an app from the relevant repository, branch `main`, entrypoint `app.py`, Python 3.12.
3. Paste that local project's `runtime/deployment/streamlit.secrets.toml` into Advanced settings > Secrets. These private files have been prepared in both standalone folders. Never upload them to GitHub or Google Docs.
4. Deploy and set public sharing. Repeat for the other repository if you want two separate hosted apps.
5. Verify each actual URL in an incognito/private browser window and add it to the corresponding submission. No examiner password or API key is required.

The repositories are published; hosted apps are **not deployed yet**. Each deployment has independent usage counters, so its limits do not cap combined usage of both apps. Week 3 hosted work lasts for the current browser session; download approved checklists before refreshing or closing it. Use the local Week 3 app to demonstrate checkpoint recovery across restarts.

This original folder remains the combined development workspace. Submit the two separate repository links above.
