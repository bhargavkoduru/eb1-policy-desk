# Week 2 — USCIS EB-1 Policy Desk

## Overview and one-liner

My RAG app helps applicants research EB-1A and EB-1B policy questions from a dated, two-chapter USCIS Policy Manual snapshot in a Streamlit web app, targeting at least 90% supported factual claims and p95 response latency under 15 seconds.

This is the permitted custom-use-case route, adapting the Enterprise Policy Q&A pattern. It implements ingestion, cleaning, chunking, embeddings, persistent storage, hybrid retrieval, reranking, cited generation and refusal/clarification. It does not predict personal immigration outcomes.

## Dataset and framework

The supplied 105-page public employment-based policy PDF contains the two selected chapters on 23 unique source pages. LlamaParse agentic OCR produced page-aware Markdown after direct PDF extraction proved garbled. The original was preserved. The corpus contains two English chapter documents and 65 retrieval chunks; USCIS is the source of truth. The print/snapshot date is September 23, 2026, not the effective date of every provision.

Chunking is page/section-aware, capped at 550 tokens with 70-token overlap. `Qwen/Qwen3-Embedding-8B` on Nebius produces 4,096-dimensional vectors. Local NumPy storage is sufficient for this small corpus; BM25 provides keyword matching. Reciprocal-rank fusion supplies ten candidates for model reranking, then four passages go into answer generation. Generation and reranking use `Qwen/Qwen3-235B-A22B-Instruct-2507`.

The owner checks for source updates monthly and on USCIS notices, targeting refresh within two working days of receiving a new export. Refresh is manual; corpus changes require a rebuilt index. The full six-field framework is in `docs/PROJECT_PLAN.md`.

## Instructions and AI coding assistance

The answer instruction requires the model to use only supplied evidence, clarify ambiguous categories, refuse unsupported requests, and select exact source evidence IDs for each claim. Code supplies the quote and page reference; the model cannot invent a citation identifier. Exact runtime prompts are in `eb1/qa.py` and `eb1/retrieval.py`.

The user's scoping requests included a simple project that covers both handouts, uses existing Nebius/LlamaCloud credits, and can be completed quickly. Codex was asked to proceed with implementation in the selected local folder. Codex wrote original Python/Streamlit code, prepared the corpus, ran live evaluations and revised failure cases. The Academy solution kit informed the pattern but its implementation was not copied.

Selected user prompts given to Codex, reproduced verbatim:

- "Let's consider a simple project that can check all boxes laid out in the week2 and 3 files but can be wrapped up sooner, using any public repositories"
- "I have downloaded the Policy manual and created a pdf for the pages covering Employment based immigration"

## Evaluation, iterations and learnings

Fifteen original questions cover six direct questions, three cross-chapter questions, three ambiguous requests and three unsupported requests. Gold passages and expected behavior were defined before evaluation. Dense retrieval is compared with hybrid retrieval plus reranking. The evaluation report includes measured retrieval scores, latency, citation checks, claim-support review and a retained failure.

Main iterations: preserve table headings during cleaning; replace model-generated quotations with evidence-ID selection; add explicit category clarification; reduce tangential claims; replace the smaller generation model after source review revealed overbroad statements. Valid source IDs alone do not prove a claim is supported. The final model still produced one overbroad 'mandatory criterion' statement, documented as a failure.

See `docs/WEEK2_EVALUATION.md` and `evals/` for actual measurements. This small development set was used to improve the app, so results should not be described as unseen-test performance.

## Examiner access

The app runs locally with Python 3.12 and Streamlit. Clone the public repository and follow the README setup instructions. Live model requests require the reviewer's own Nebius API key in a local `.env`; credentials are not included or shared. The bundled corpus and index let the app start without another parsing or embedding job.

No app login is required. Answers stay in the current browser session.

## Submission links to add

- GitHub repository: https://github.com/bhargavkoduru/eb1-policy-qa-week2 (public; no examiner invitation needed).
- Google Doc: open `WEEK2_PROJECT_REPORT.docx` in Google Docs and replace `[Your name]`.
