# Requirements and remaining submission actions

The handouts permit a custom use case. This project follows their RAG and agent frameworks; it does not claim to implement all specialized requirements of unrelated suggested projects.

| Week 2 item | Evidence/status |
| --- | --- |
| User, corpus, interface, faithfulness and latency target | `PROJECT_PLAN.md`, `WEEK2_SUBMISSION.md` |
| Six planning fields | Completed in `PROJECT_PLAN.md`, including a manual freshness cadence and target SLA. |
| Ingest, clean, chunk, embed and persist | LlamaParse scripts, page-aware Markdown, 65 LangChain chunks and local 4,096-dimensional vector index. |
| Hybrid retrieval and reranking | Dense + BM25 reciprocal-rank fusion, model reranking and top-four context. |
| Cited answers and refusal | Evidence-ID selection, exact source text, page links, ambiguous-category clarification and unsupported responses. |
| Fifteen-question evaluation and failure analysis | `WEEK2_EVALUATION.md`, definitions and raw runs under `evals/`. |
| Overview, dataset, prompts, iterations, learnings | Google Doc draft in `WEEK2_SUBMISSION.md`; exact runtime prompts in source. |
| GitHub assets and live video up to five minutes | Code published in the shared repository; inspected ZIP prepared. Video recording remains. |

| Week 3 item | Evidence/status |
| --- | --- |
| Multi-step task, tool choices and state | Single model-driven LangGraph agent with four LangChain tools and SQLite checkpoints. |
| Read/write boundary and human intervention | Final save gated on exact-draft approval; edit, re-review and cancellation implemented. |
| Memory across restart | Local mode recovers goal, history, sources, draft, trace and approval state from checkpoints across restarts. Hosted visitors resume during their current browser session; refresh starts a new workspace. |
| Failure handling | Bounded calls, API retries, source-empty handoff, failed-save retention and idempotent retry. |
| End-to-end validation | Five scenario categories covered by live and deterministic checks; 28 total tests passed, including hosted access/isolation checks. |
| Documentation and prompts | `WEEK3_SUBMISSION.md`, `WEEK3_EVALUATION.md`, `ARCHITECTURE.md` and `eb1/research.py`. |
| Manual baseline comparison | Not measured. Time one manual policy search and checklist preparation before claiming a time-saving percentage. |
| GitHub assets and live video up to five minutes | Shared repository and ZIP contain both modes. Separate Week 3 video recording remains. |

## One app, two submissions

The examiner opens the public app URL without signing in, then selects the relevant week in the sidebar. The same GitHub repository and hosted URL can appear in both submissions; each week has its own documentation, evaluation and video.

| Submit | Week 2 | Week 3 |
| --- | --- | --- |
| Google Doc | Copy `WEEK2_SUBMISSION.md` and the Week 2 evaluation | Copy `WEEK3_SUBMISSION.md` and the Week 3 evaluation |
| GitHub | Same public repository | Same public repository |
| Video | Live Policy Q&A walkthrough, at most five minutes | Live research/review/save walkthrough, at most five minutes |
| Hosted app link | Same URL, Policy Q&A mode | Same URL, Research checklist mode |

The first three rows come from the handouts. A hosted app link is a convenience, not an additional stated requirement. Google Docs and videos remain to be created; the hosted URL remains to be deployed. No examiner password, invitation or API-key sharing is needed.

## Finish your submission

1. For password-free examiner access, finish `CLOUD_DEPLOYMENT.md` and add the actual app URL to both submission drafts. Test the link in a private/incognito browser window. Try one cited answer and one checklist yourself. Inspect the evidence and the recorded limitations.
2. Paste each week's submission draft and evaluation report into a Google Doc. Add your name, repository link and video link.
3. Use https://github.com/bhargavkoduru/eb1-policy-desk for the code link. It is public; no invitation is needed. Credentials, demo scripts, source PDFs, sessions and `.venv` are excluded; future uploads should also use the inspected allowlist.
4. Record a separate live walkthrough of each milestone, no longer than five minutes.
5. Complete the course submission form with the requested links. This agent has not submitted anything for you.

The Week 2 answer-quality target was met on a small development set under an assistant evidence audit, with one documented failure. Neither the tests nor the citations certify legal accuracy or performance on new questions. An independent human review remains useful.
