# PRD: Multi-Agent Debate System

**Owner:** Nabin Acharya
**Status:** Draft v1
**Last updated:** 2026-07-04

---

## 1. Problem / Motivation

Most portfolio "multi-agent" projects are a thin wrapper around a single prompt looped three times. This project exists to demonstrate two things concretely:

1. **Multi-agent orchestration** — distinct agents with different roles, coordinated via a state graph rather than a linear chain.
2. **Applied LLD** — real software design patterns (Strategy, Template Method, Chain of Responsibility, Dependency Injection) used because the problem calls for them, not bolted on for a resume line.

Secondary motivation: complement an existing resume gap around system design / architecture thinking, targeting 15–20 LPA Bangalore roles.

---

## 2. Goals

- Build a working debate system where three agents — **Optimist**, **Critic**, **Judge** — argue a user-submitted topic and produce a verdict.
- Run entirely on local inference (Ollama + Phi-4-Mini) — no external API cost or dependency.
- Produce an architecture and codebase defensible in a technical interview: clear interfaces, documented design decisions, tested core logic.
- Ship a usable demo (Streamlit) that a non-technical person could run and understand.

## 3. Non-Goals (explicitly out of scope)

- Multi-user support, auth, or accounts
- Long-term analytics or querying across many past debates — PostgreSQL is used for transcript persistence (NFR6), but building dashboards/reports over historical debates is not a goal
- Streaming token-by-token UI
- Building or testing against more than one concrete LLM adapter (e.g., OpenAI, Anthropic). The `LLMPort` interface makes this structurally possible per hexagonal architecture, but only `OllamaAdapter` will be implemented — no provider-selection logic, fallback, or multi-provider testing
- Production concerns: horizontal scaling, queuing, rate limiting, deployment infra
- High debate "quality" tuning — Phi-4-Mini will sometimes produce mediocre arguments; this is acceptable and expected given the model size

Explicitly writing these down so scope doesn't creep mid-build.

---

## 4. Users & Use Case

**Primary user:** the developer (portfolio/demo use), and anyone reviewing the project (interviewers, recruiters).

**Core use case:**
1. User submits a debate topic via Streamlit (e.g., "Remote work is better than office work").
2. Optimist agent argues in favor.
3. Critic agent challenges the Optimist's argument / argues against.
4. Judge agent evaluates both and produces a verdict or synthesis.
5. Result displayed with each agent's turn visible (not just the final verdict) — transparency of reasoning is part of the value.

---

## 5. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | User can input a free-text debate topic |
| FR2 | Debate runs for 2 rounds each for Optimist and Critic (Optimist → Critic → Optimist rebuttal → Critic rebuttal), then proceeds to Judge. Flow is driven by a LangGraph state graph, not a hardcoded sequential script |
| FR3 | Each agent's output is shown separately in the UI, not just the final result |
| FR4 | Judge produces a clear verdict: winner, or reasoned synthesis if no clear winner. For v1, Judge evaluates only at the end (final judgement); mid-debate intervention is a documented future extension, not built now |
| FR5 | If an agent produces malformed/invalid output (fails schema validation), the system retries the LLM call (bounded retry count) before falling back to a documented failure state — not silently swallowed, not infinite retry |
| FR6 | Judge intervening mid-debate (rather than only at the end) is explicitly deferred — noted as a future extension, not a v1 requirement |

## 6. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR1 | Runs fully offline/local — Ollama + Phi-4-Mini, no external API keys required |
| NFR2 | Single debate completes in a reasonable demo time (target: under ~60s on the stated hardware — 16GB RAM, 4GB VRAM GTX 1650; adjust after benchmarking) |
| NFR3 | Codebase organized so agent logic is unit-testable without a live Ollama instance (LLM calls must be mockable) |
| NFR4 | Config (model name, temperature, turn count, topic templates) externalized, not hardcoded |
| NFR5 | Architecture and design decisions documented (ADR) well enough to explain in an interview without re-deriving them live |
| NFR6 | Debate transcripts persisted to PostgreSQL via a repository port (not SQLite — chosen for familiarity and to defend a "production-realistic" persistence story) |
| NFR7 | I/O-bound code paths (LLM calls, DB access, FastAPI endpoints) written with async/await, so the system can be defended as concurrency-ready even though the demo itself is single-user |

---

## 7. Success Criteria

- End-to-end debate runs and produces a coherent (if imperfect) verdict for at least 3 varied test topics.
- Codebase demonstrates all 4 target LLD patterns with a one-line justification each, documented in the ADR.
- Core agent logic has unit tests that pass without Ollama running (mocked LLM boundary).
- A stranger could read the README + ADR and understand the architecture without reading all the code.

---

## 8. Constraints

- Hardware: Windows PC, 16GB RAM, 4GB NVIDIA GTX 1650 → dictates Phi-4-Mini as the model choice (already validated).
- Time: side project around a 12PM–9PM work shift — needs to stay scoped, not open-ended.
- Stack is fixed: Ollama (Phi-4-Mini), LangGraph, FastAPI, Streamlit, PostgreSQL, hexagonal architecture, async/await throughout I/O-bound code. Not up for debate (pun intended) — decision already made, revisiting it is out of scope for this PRD.

---

## 9. Open Questions — Resolved

- ~~Exact turn structure~~ **Resolved:** 2 rounds each for Optimist and Critic, then Judge (FR2).
- ~~Does the Judge only evaluate at the end, or can it intervene mid-debate?~~ **Resolved:** final judgement only for v1; mid-debate intervention deferred as a future extension (FR4, FR6).
- ~~Malformed output retry policy~~ **Resolved:** bounded retry on schema-validation failure, with a documented failure state if retries are exhausted (FR5).
- ~~Persistence: SQLite vs in-memory~~ **Resolved:** PostgreSQL via a repository port (NFR6).
- ~~What does the async boundary actually buy us for a single-user demo?~~ **Resolved:** it's a deliberate architectural choice to demonstrate scalable I/O patterns (concurrent DB writes, non-blocking LLM calls) — not a response to an actual current load requirement. This trade-off is stated explicitly rather than implying the app is load-tested (see Section 10).

All open questions from v1 are now resolved. Any new questions surfaced during ADR/design work will be added here.

---

## 10. Architecture Note

The system will use **Hexagonal Architecture (Ports & Adapters)**: domain logic (debate rules, agent behavior) has no knowledge of Ollama, PostgreSQL, FastAPI, or Streamlit. These are adapters plugged in through ports (`LLMPort`, `DebateRepositoryPort`, `PresenterPort`), enabling the domain to be unit-tested with fakes and keeping infrastructure swappable in principle. Full rationale, port/adapter mapping, and LLD pattern placement to be detailed in the ADR (Phase 1).

This is a deliberate choice to prioritize architectural learning and interview defensibility over minimal-effort delivery — flagged here so it isn't mistaken for accidental over-engineering.

## 11. Next Step

Proceed to ADR (Phase 1): lock in the state graph shape, and map each LLD pattern to a specific component with a written rationale.
