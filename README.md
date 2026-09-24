# USCIS EB-1 Policy Assistant

This is the original combined development workspace. Use the separate repositories below for the weekly submissions. Both projects run locally with Streamlit.

| Week | Public repository | Editable report |
| --- | --- | --- |
| Week 2 | [EB-1 Policy Q&A](https://github.com/bhargavkoduru/eb1-policy-qa-week2) | [Week 2 Word document](docs/WEEK2_PROJECT_REPORT.docx) |
| Week 3 | [EB-1 Research Agent](https://github.com/bhargavkoduru/eb1-research-agent-week3) | [Week 3 Word document](docs/WEEK3_PROJECT_REPORT.docx) |

The Word reports include the project overview, framework, dataset, AI coding assistance, evaluation results, limitations and repository links. Open each file in Google Docs and replace `[Your name]`.

## Run this combined workspace locally

The local environment, credentials, public corpus and index are already prepared here. In PowerShell, from this project folder:

```powershell
$env:EB1_HOSTED = 'false'
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Open http://127.0.0.1:8501 and select the week in the sidebar. Each separate repository instead opens directly to its own workflow; follow its README for a fresh installation with Python 3.12 and your own Nebius key. No app login is required.

## Implementation and validation

Week 2 implements ingestion, cleaning, page-aware chunks, embeddings, local persistent vectors, BM25 fusion, reranking, cited answers, clarification and refusal. The 15-question development evaluation passed all expected behavior checks. A separate assistant evidence audit supported 25/26 final factual claims; one overbroad criterion statement remains documented.

Week 3 adds a LangGraph agent with four tools, SQLite checkpoints, bounded recovery and human review before final save. Local research can be resumed across app restarts. Five workflow scenarios were covered; no measured human time saving is claimed.

The combined suite passed 28 tests. The standalone suites passed 13 tests for Week 2 and 27 for Week 3, with GitHub Actions validation. Unit and UI tests use substitutes for provider calls; live evaluation scripts consume Nebius credits.

## Documentation

- [Week 2 submission draft](docs/WEEK2_SUBMISSION.md) and [evaluation](docs/WEEK2_EVALUATION.md)
- [Week 3 submission draft](docs/WEEK3_SUBMISSION.md) and [evaluation](docs/WEEK3_EVALUATION.md)
- [Document and code checklist](docs/SUBMISSION_CHECKLIST.md)
- [Project plan](docs/PROJECT_PLAN.md), [architecture](docs/ARCHITECTURE.md), and [source preparation](docs/SOURCE_AUDIT.md)

## Source and data handling

The corpus uses 23 unique pages from USCIS Policy Manual Volume 6, Part F, Chapters 2 and 3, printed September 23, 2026. The print date is not the effective date of every provision. LlamaParse OCR produced cached Markdown after direct PDF extraction proved garbled; 65 chunks and precomputed embeddings are included for reproducibility.

Questions and retrieved policy passages go to Nebius. Local answers and research files are not published. API keys, original PDFs, private settings, runtime databases and the Python environment are excluded from Git. The included corpus and evaluation examples contain public policy material only.

```powershell
$env:EB1_HOSTED = 'false'
.\.venv\Scripts\python.exe -m pytest -q tests
.\.venv\Scripts\python.exe -m scripts.export_submission
```

The allowlisted export includes the two Word reports and scans their uncompressed contents for configured credentials. The independent weekly repositories also provide their own exports.
