# Two small milestones

## Scope

Week 2: USCIS EB-1 Policy Q&A, adapting the handout's policy Q&A pattern through its permitted custom-use-case route. Week 3: a custom policy research/checklist agent. Use the two supplied handouts as the requirements; use the Academy's solution kit as a reference rather than copying its implementation.

Use only Volume 6, Part F, Chapters 2 and 3 in the first version. Candidate CVs, LinkedIn ingestion, AAO decisions, and recommendation letters are later features. A policy-based research checklist helps organize a user's questions; it does not determine eligibility or replace professional case review.

## Week 2

One-liner: Help applicants research EB-1A/EB-1B policy questions from a dated USCIS Policy Manual snapshot in a Streamlit web app, targeting at least 90% supported factual claims in a 15-question evaluation and p95 latency below 15 seconds. These are targets to measure, not achieved results.

| Planning field | Decision |
| --- | --- |
| Use case | Cited explanations of the selected policy chapters. |
| Corpus | Two English chapters, derived from 23 pages in the user's 105-page public USCIS excerpt; USCIS owns the source of truth. |
| Ingestion and cleaning | LlamaParse OCR after local orientation correction, preserve tables/footnotes/headings, trim adjacent chapters, retain source hash and page mapping. |
| Freshness | Show the snapshot date; the owner checks monthly and on USCIS update notices. Target refresh within two working days of receiving a new export, with a corpus/index rebuild before use. This is an operating commitment, not an automated refresh service. |
| Chunking and embedding | Split by section and page with a 550-token cap and 70-token overlap. Nebius `Qwen/Qwen3-Embedding-8B` returns 4,096 dimensions; retain table headings and page provenance. |
| Retrieval | Local vector search plus BM25; combine candidate ranks, rerank a small candidate set, pass top four passages to generation. |

Build with Python, Streamlit, LangChain/LangGraph, and Nebius. A local store minimizes account setup. Pinecone is already authenticated and can be added if needed; it is not required by the handouts. LlamaCloud performs the one-time parsing; local Markdown is reused for subsequent development.

The answer shows chapter/section/page citations and supporting excerpts. The app asks for clarification when the category is ambiguous and refuses unsupported questions. Validate citation identifiers against the retrieved context.

Evaluate 15 original questions: 6 direct, 3 across both chapters, 3 ambiguous, and 3 unanswerable. Create expected answers/behaviors and gold source sections first. Report retrieval precision/recall, supported-claim proportion, citation correctness, refusal/clarification behavior, latency, and failure analysis. Keep one baseline and one documented improvement. Manually verify evidence; a model's confidence is not a quality score.

## Week 3

One-liner: Help users turn a policy research question into a reviewed, cited research checklist in a Streamlit web app, replacing manual searching and note-taking, using four tools and handing off when sources are insufficient or before saving. Target normal completion within two minutes and successful handling of all five workflow scenarios. Measure the manual baseline rather than inventing it.

Four tools: `search_policy` (read), `load_research_session` (read), `draft_checklist` (prepare structured output), and `save_approved_checklist` (write after approval).

The model chooses whether to clarify the category/question, retrieve more policy evidence, prepare a draft, or hand off. Preserve conversation context, research question, sources, draft, review state, and saved record ID in SQLite-backed checkpoints. Human review supports approve, edit, and cancel; editing invalidates approval. Enforce approval in code, not just a prompt.

Use bounded tool loops and one retry for transient failures. Empty results lead to a truthful knowledge-gap response. A save failure must not be reported as success. Use idempotency to avoid duplicate saves after retries.

Five scenarios: successful reviewed save; missing information; unsupported question; restart during pending review followed by edit/cancel; injected tool/save error with recovery and no duplicate writes. Record end-to-end completion and timings.

## Time boxes and submission

After source preparation and environment/model checks, target one hour per core milestone. For Week 2, allocate about 35 minutes to the app, 15 to evaluation, and 10 to fixes/write-up. For Week 3, allocate about 35 minutes to the agent workflow, 15 to scenario checks, and 10 to fixes/write-up. These are stretch targets; unfinished checks remain unfinished when a time box ends.

Each week still needs a Google Doc with overview, datasets, prompts/agent instructions, AI coding prompts, iterations and learnings; a GitHub link to the corresponding code/assets. Preserve separate Week 2 and Week 3 milestones and results. User review and publication can require additional time.

Before submission, run a secret/data check, verify source attribution, and inspect the actual files to publish. This folder's original PDF, credentials, cloud job responses, and runtime databases stay out of Git by default.
