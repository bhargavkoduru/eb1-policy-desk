# USCIS EB-1 Policy Assistant

## Separate submission repositories

Submit the dedicated repository for each week:

| Week | Public GitHub repository | Local folder next to this project |
| --- | --- | --- |
| Week 2 | [EB-1 Policy Q&A](https://github.com/bhargavkoduru/eb1-policy-qa-week2) | `eb1-policy-qa-week2` |
| Week 3 | [EB-1 Research Agent](https://github.com/bhargavkoduru/eb1-research-agent-week3) | `eb1-research-agent-week3` |

Each repository contains its own app, setup instructions, Google Doc draft, evaluation and deployment guide. Week 2 opens directly to Q&A; Week 3 opens directly to the reviewed-checklist workflow. Both exclude API keys and demo scripts. Separate local suites passed 13 and 27 tests respectively.

This folder remains the combined development workspace. Its instructions below describe the combined app; use the two links above for course submissions.

Project workspace: `C:\Users\bharg\Desktop\Python\chatbot for EB1`.

This course project answers policy questions about EB-1A and EB-1B with citations, then extends the same retrieval system into a research/checklist workflow with saved state and human review.

Status: **both app milestones are implemented, with cloud hosting support**. The final evaluation passed 15/15 answer/clarify/refuse checks; the expanded local suite passes 28 tests, including password-free access and browser workspace isolation. A separate assistant evidence audit rated 25/26 final hybrid claims supported, with one overbroad criterion statement retained as a failure. This is a research aid, not an eligibility decision. See [Week 2 results](docs/WEEK2_EVALUATION.md), [Week 3 results](docs/WEEK3_EVALUATION.md), and [cloud deployment instructions](docs/CLOUD_DEPLOYMENT.md).

## Examiner access and submissions

For course submissions, use the two separate repositories above. This combined development app still has both sidebar modes:

| Submission | Select in the app | Documentation | Evaluation |
| --- | --- | --- | --- |
| Week 2 | Policy Q&A | [Week 2 draft](docs/WEEK2_SUBMISSION.md) | [RAG results](docs/WEEK2_EVALUATION.md) |
| Week 3 | Research checklist | [Week 3 draft](docs/WEEK3_SUBMISSION.md) | [Agent results](docs/WEEK3_EVALUATION.md) |

**Hosted URLs: pending owner deployment.** Follow [the deployment steps](docs/CLOUD_DEPLOYMENT.md), then add each real URL to its corresponding submission draft. Hosted visitors receive separate temporary browser workspaces; download approved checklists before refreshing or closing the page. Local mode retains research across app restarts.

The handouts require a Google Doc, a live video of at most five minutes, and GitHub assets for each week. A hosted URL is an extra convenience. See the [submission checklist](docs/SUBMISSION_CHECKLIST.md) for what remains.

## Run on this computer

Open PowerShell and run these lines. The environment, credentials, corpus and index are already prepared here:

```powershell
Set-Location -LiteralPath 'C:\Users\bharg\Desktop\Python\chatbot for EB1'
$env:EB1_HOSTED = 'false'
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Open **http://127.0.0.1:8501**. Select the policy category and the Week 2 or Week 3 mode in the sidebar. Stop a foreground server with Ctrl+C. If a server is already running at that address, use it instead of starting another copy.

- Week 2: ask a policy question, inspect the answer, open the evidence excerpts and source citations.
- Week 3: enter a research goal, review the proposed tasks, apply edits if needed, then approve and save. Reopen the session from the dropdown after a restart.
- Suggested first question: “For EB-1A, is an invitation to peer review enough to show judging?”
- Suggested first research goal: “Research EB-1B judging evidence and prepare a short checklist of documentation to verify.”

## Set up a fresh copy

Python 3.12 was used for testing. From the extracted project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item -LiteralPath .env.example -Destination .env
```

Edit `.env` locally and add your Nebius key. Run `Copy-Item` only in a fresh copy without an existing `.env`; preserve existing credentials. The included `corpus/` contains public policy text, so a new LlamaParse job is not needed to try the app.

```powershell
$env:EB1_HOSTED = 'false'
.\.venv\Scripts\python.exe -m scripts.check_nebius
.\.venv\Scripts\python.exe -m scripts.setup_index
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

The final default chat/reranking model is `Qwen/Qwen3-235B-A22B-Instruct-2507`; embeddings use `Qwen/Qwen3-Embedding-8B` with 4,096 dimensions. API model availability can change; optional model identifiers are in `.env.example`. Changing the embedding model requires rebuilding the index. Nebius calls consume your credits; its remaining balance is checked in the account dashboard, not by this app. Hosted mode is the default and opens without a login; the owner configures the Nebius key in server secrets. Use the explicit local-mode setting above only with a loopback bind address.

## Evaluation and submission

- [Week 2 Google Doc draft](docs/WEEK2_SUBMISSION.md)
- [Week 3 Google Doc draft](docs/WEEK3_SUBMISSION.md)
- [Requirement mapping and remaining submission actions](docs/SUBMISSION_CHECKLIST.md)
- [Architecture and data locations](docs/ARCHITECTURE.md)
- [Deploy for examiner access](docs/CLOUD_DEPLOYMENT.md)
- [Build plan](docs/PROJECT_PLAN.md) and [source preparation report](docs/SOURCE_AUDIT.md)

```powershell
$env:EB1_HOSTED = 'false'
.\.venv\Scripts\python.exe -m pytest -q tests
.\.venv\Scripts\python.exe -m scripts.evaluate
.\.venv\Scripts\python.exe -m scripts.smoke_week3
.\.venv\Scripts\python.exe -m scripts.export_submission
```

The evaluation scripts make live Nebius calls; unit/UI tests use controlled substitutes for those calls. Week 2 results are cached per configuration. If results change, an evidence audit must be repeated before updating the claim-support report; `scripts.build_reports` rejects stale audit hashes.

The export creates `dist/eb1-policy-desk-submission.zip` using a file allowlist and a scan for configured API keys and any legacy access codes. It includes public corpus text, its precomputed index and public evaluation samples, and excludes credentials, cloud secrets, access codes, demo scripts, original PDFs, raw cloud jobs, local sessions and the Python environment. Google Doc creation and live video recording remain submission actions. A GitHub repository does not itself mean the hosted app has been deployed; follow the cloud deployment instructions.

## Source material

The user supplied `Policy Manual_USCIS_eb.pdf`, a 105-page excerpt printed September 23, 2026. It contains a wider selection of employment-based immigration material. The initial corpus uses source PDF pages 2-24, containing Volume 6, Part F, Chapter 2 (Extraordinary Ability) and Chapter 3 (Outstanding Professor or Researcher), with neighboring material removed after parsing.

Two local PDF readers returned garbled text because the printed PDF uses Type 3 fonts without usable character mappings. We preserve the original, correct page orientation in a derivative, and render selected pages for LlamaParse OCR. This is source preparation, not legal interpretation. The print date does not establish the effective date of each policy provision.

## Files and data

- `.env`: your existing credentials; ignored by Git. Do not paste it into a document or commit it.
- `.env.example`: blank variable names for a reproducible setup.
- `scripts/prepare_pdf.py`: selected pages to an upright image PDF with a source hash and page map; requires PyMuPDF.
- `scripts/parse_policy.py`: submit/retrieve LlamaParse jobs; uses Python's standard library and does not print keys.
- `scripts/build_corpus.py`: trim to the two selected chapters and preserve source page references.
- `data/prepared/`: OCR inputs and page manifests.
- `data/parsed/`: cached parse jobs and per-page Markdown.
- `data/corpus/`: the two chapter documents, page records, and a source manifest.
- `corpus/`: public-only corpus copy included with the submission; used when `data/corpus/` is absent.
- `eb1/`: retrieval, cited answers and the persistent research agent.
- `app.py`: both Streamlit milestones.
- `evals/` and `tests/`: measured public-policy runs and controlled workflow/UI checks.

PDFs, `.env`, cloud secrets, viewer access codes, runtime data and local databases are excluded from Git. Only public USCIS excerpts were sent to LlamaCloud during preparation. Questions and retrieved passages go to Nebius during use. Candidate records are outside the initial scope. Local mode binds only to this computer. Hosted mode separates research files by a randomly generated browser-session identity; local server files are not additionally encrypted by the application. Refreshing or closing the browser loses access to that hosted workspace, and server rebuilds can clear stored files. Download approved checklists before leaving.

## Reproduce source preparation

Install PyMuPDF in your project Python environment first. From this folder:

```powershell
python scripts/prepare_pdf.py --start 2 --end 2 --name pilot
python scripts/parse_policy.py start pilot
python scripts/parse_policy.py poll pilot
python scripts/prepare_pdf.py --start 3 --end 24 --name eb1_remainder
python scripts/parse_policy.py start eb1_remainder
python scripts/parse_policy.py poll eb1_remainder
python scripts/build_corpus.py
```

Repeat `poll` if a job is pending/running. Existing job IDs and completed results are reused. The preparation script rejects a changed source under the same name, and an uncertain submission is not retried automatically. Treat a failed/empty/misordered parse as a problem to resolve, not a valid corpus.

The selected parser is the agentic tier, pinned to version `2026-09-13`. The completed jobs reported **230 credits used**: 10 for the pilot page and 220 for the remaining 22 pages. A subsequent account check reported **49,770 LlamaCloud credits remaining** on September 23, 2026. Reusing the cached Markdown does not submit a new parse. [LlamaParse pricing](https://developers.llamaindex.ai/llamaparse/general/pricing/)

The original document remains the source for visual checks. OCR text requires review, especially tables, numbers, superscripts, and footnotes. Future answers should cite the chapter, section, and source PDF page and clearly identify the snapshot used.
