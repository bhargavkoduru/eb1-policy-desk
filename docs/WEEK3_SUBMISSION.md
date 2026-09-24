# Week 3 — Reviewed policy research checklist agent

## One-liner

My agent helps applicants turn an EB-1 policy research question into a cited, reviewed checklist in a local web app, replacing manual searching and note-taking. It selects among four tools, hands off when information is missing or unsupported and before a final save, and targets completion within two minutes with successful handling of five workflow scenarios. The manual time baseline remains to be measured.

## Agent framework

| Field | Implementation |
| --- | --- |
| Goal | Research a policy question and prepare a checklist that the user can inspect, edit and approve. |
| Surface | Streamlit, Week 3 mode, running on the user's computer. |
| Steps | Choose whether to clarify, load, search again, draft or hand off; pause for review; save after approval. |
| Tools | `search_policy` and `load_research_session` read; `draft_checklist` prepares a draft; `save_approved_checklist` writes a final approved record. |
| Memory | Goal, category, clarification history, evidence, tool trace, draft and review state persist in local SQLite checkpoints across restarts. |
| Limits | No personal eligibility decision, approval probability, invented candidate facts, LinkedIn scraping, email sending or automatic final save. |
| Human review | Approve displayed draft, edit suggested tasks/notes and review again, or cancel. Editing clears approval. |
| Recovery | One client retry for transient API failures; bounded planning/search; empty evidence hands off. Save retries once, retains failed state, and supports an idempotent retry. |
| Success | Five scenario categories tested; final live judging task produced a focused checklist and survived restart/edit/approval in 12.87 scripted seconds. Real human review time is excluded. |

## Why this is an agent

The model chooses the next action using the current goal and tool observations, including additional searches or clarification. LangGraph routes those decisions, stores state and interrupts for human review. Tool inputs and writes are enforced in code. This extends the Week 2 retrieval system rather than simply renaming a Q&A chain.

## Dataset, prompts and implementation

Reuse the Week 2 public USCIS corpus and local index. The planner uses `Qwen/Qwen3-235B-A22B-Instruct-2507` on Nebius. The exact planner prompt and four LangChain tool definitions are in `eb1/research.py`; shared answer/evidence instructions are in `eb1/qa.py`. The architecture and data locations are documented in `docs/ARCHITECTURE.md`.

Codex generated and revised original code from the user's requested scope. Testing specifically targeted restart behavior, edit-before-approval, cancellation, tool failures and duplicate-save prevention. Initial live testing exposed a generic checklist that did not address judging; a stronger model and an explicit focus check corrected that failure.

## Evaluation and learnings

The local suite passed 19 tests, including Streamlit form interactions. Live checks covered a judged-evidence checklist with simulated review, ambiguity/cancellation and unsupported requests. Error/retry scenarios use controlled injected failures. See `docs/WEEK3_EVALUATION.md` and `evals/week3_live.json`.

Approval belongs in code, not only in the prompt. A durable checkpoint is necessary to resume an unfinished review. A successful save is not sufficient evidence of a useful checklist: topic focus and claim support must also be checked. No measured human time saving is claimed until the manual baseline is recorded.

## Submission links to add

- GitHub repository and Week 3 milestone: add after uploading.
- Live demo video, at most five minutes: add after recording.
- Google Doc: paste this document and the Week 3 evaluation report into your own Google Doc.
