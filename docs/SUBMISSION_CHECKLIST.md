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
| GitHub assets and live video up to five minutes | Inspected ZIP prepared; user publication/recording remains. |

| Week 3 item | Evidence/status |
| --- | --- |
| Multi-step task, tool choices and state | Single model-driven LangGraph agent with four LangChain tools and SQLite checkpoints. |
| Read/write boundary and human intervention | Final save gated on exact-draft approval; edit, re-review and cancellation implemented. |
| Memory across restart | Goal, clarification history, sources, draft, trace and approval state recover from checkpoints. |
| Failure handling | Bounded calls, API retries, source-empty handoff, failed-save retention and idempotent retry. |
| End-to-end validation | Five scenario categories covered by live and deterministic checks; 19 total tests passed. |
| Documentation and prompts | `WEEK3_SUBMISSION.md`, `WEEK3_EVALUATION.md`, `ARCHITECTURE.md` and `eb1/research.py`. |
| Manual baseline comparison | Not measured. Time one manual policy search and checklist preparation before claiming a time-saving percentage. |
| GitHub assets and live video up to five minutes | Same ZIP contains both modes; user publication/recording remains. |

## Finish your submission

1. Try one cited answer and one checklist yourself. Inspect the evidence and the recorded limitations.
2. Paste each week's submission draft and evaluation report into a Google Doc. Add your name, repository link and video link.
3. Upload only the inspected ZIP contents to your GitHub repository. Your local `.env`, PDF, sessions and `.venv` must stay out.
4. Record a separate live walkthrough of each milestone, no longer than five minutes.
5. Complete the course submission form with the requested links. This agent has not submitted anything for you.

The Week 2 answer-quality target was met on a small development set under an assistant evidence audit, with one documented failure. Neither the tests nor the citations certify legal accuracy or performance on new questions. An independent human review remains useful.
