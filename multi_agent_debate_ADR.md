# ADR-001: Multi-Agent Debate System Architecture

**Status:** Proposed
**Date:** 2026-07-04
**Deciders:** Nabin Acharya

---

## Context

Per the PRD, this system runs a 3-agent debate (Optimist, Critic, Judge) over a user-submitted topic, using local inference (Ollama + Phi-4-Mini), orchestrated with LangGraph, exposed via FastAPI, rendered in Streamlit, and persisted to PostgreSQL. Async/await is used throughout I/O-bound paths.

The project's explicit purpose (per PRD Section 1) is to demonstrate architecture and LLD competence, not just ship a working demo. That reprioritizes some decisions below toward "defensible and instructive" over "minimal."

Forces at play:
- Domain logic (debate rules, turn sequencing, verdict logic) must stay testable without live Ollama/Postgres.
- LangGraph, Ollama, FastAPI, Streamlit, and Postgres are all infrastructure concerns that change independently of debate rules.
- Four LLD patterns (Strategy, Template Method, Chain of Responsibility, DI) need real homes, not forced insertions.
- Turn structure is fixed (PRD FR2): 2 rounds each, Optimist → Critic → Optimist → Critic → Judge.

---

## Decision

Adopt **Hexagonal Architecture (Ports & Adapters)**. Three layers:

```
┌─────────────────────────────────────────────────────────┐
│                      ADAPTERS (outside)                  │
│  ┌───────────┐  ┌────────────┐  ┌──────────┐ ┌────────┐  │
│  │ FastAPI   │  │ Streamlit  │  │ Ollama   │ │Postgres│  │
│  │ (driving) │  │ (driving)  │  │ (driven) │ │(driven)│  │
│  └─────┬─────┘  └──────┬─────┘  └────▲─────┘ └───▲────┘  │
│        │               │             │           │       │
│  ┌─────▼───────────────▼─────────────┴───────────┴────┐  │
│  │              APPLICATION LAYER                      │  │
│  │   DebateService (orchestrates use case, async)       │  │
│  │   Depends on ports, injected at composition root      │  │
│  └─────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐ │
│  │                  DOMAIN (core hexagon)                │ │
│  │  Agent, DebateStrategy, ArgumentHandler chain,        │ │
│  │  Debate state machine, Verdict — zero infra imports   │ │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Driving adapters** (call into the app): FastAPI, Streamlit (via FastAPI, not directly into domain)
**Driven adapters** (called by the app): OllamaAdapter, PostgresDebateRepository

LangGraph is treated as **infrastructure for running the domain's state machine**, not the source of truth for debate rules — see "LangGraph placement" below.

---

## Ports (interfaces owned by the domain)

All I/O ports are `async` per NFR7.

```python
class LLMPort(Protocol):
    async def generate(self, prompt: str, *, temperature: float) -> str: ...

class DebateRepositoryPort(Protocol):
    async def save_turn(self, debate_id: UUID, turn: Turn) -> None: ...
    async def save_verdict(self, debate_id: UUID, verdict: Verdict) -> None: ...
    async def get_debate(self, debate_id: UUID) -> Debate: ...

class PresenterPort(Protocol):
    async def on_turn_complete(self, turn: Turn) -> None: ...
    async def on_verdict(self, verdict: Verdict) -> None: ...
```

`PresenterPort` is what gives you a clean seam for the deferred "Judge intervenes mid-debate" feature later (PRD FR6) — the domain already emits events per turn; a future mid-debate Judge just becomes a new subscriber/consumer of the same event, no domain rewrite needed.

---

## LLD Pattern Mapping

| Pattern | Where | Why |
|---|---|---|
| **Template Method** | `Agent` abstract base class defines `async def take_turn(context) -> Turn`, with fixed steps: `build_prompt() → call_llm() → validate() → parse_response()`. Subclasses (`OptimistAgent`, `CriticAgent`, `JudgeAgent`) override `build_prompt()` and `parse_response()` only. | All three agents share the same lifecycle (prompt → generate → validate → parse); only the prompt content and output shape differ per role. This is the textbook Template Method case, not a forced fit. |
| **Strategy** | `DebateStrategy` interface, e.g. `default_strategy` (current behavior) vs a future `steelman_strategy` (agent must first restate opponent's position before rebutting). Injected into `Agent.build_prompt()`. | Argument *construction approach* is naturally swappable per topic type or experiment, independent of which agent role is using it. |
| **Chain of Responsibility** | `ArgumentHandler` chain: `SchemaValidationHandler → RetryHandler → FallbackHandler`, each deciding whether to pass a raw LLM response along or intervene. | Directly resolves PRD FR5 (retry on malformed output). Each handler has one responsibility and the chain is extensible (e.g., add a `ProfanityFilterHandler` later without touching existing handlers). |
| **Dependency Injection** | Composition root (in FastAPI startup) constructs `OllamaAdapter`, `PostgresDebateRepository`, wires them into `DebateService` via constructor injection. Tests inject `FakeLLMAdapter`/`InMemoryRepository` instead. | This is what makes NFR3 (testable without live Ollama) actually true, not aspirational. |

---

## Retry Logic Placement (resolves PRD FR5 design question)

**Options considered:**

| Option | Assessment |
|---|---|
| **A: Retry inside `OllamaAdapter`** | Simple, but conflates "model produced garbage" (a domain-meaningful event worth logging/handling) with "network/transport retry" (pure infra concern). Domain has no visibility into retry attempts. |
| **B: Retry via Chain of Responsibility in the domain/application layer** | `RetryHandler` in the `ArgumentHandler` chain calls back into `LLMPort.generate()` directly on validation failure, up to a bounded count, before handing off to `FallbackHandler`. |

**Decision: Option B.** The retry is triggered by a **domain concern** (schema validation failure), not a transport failure — it belongs in the chain, not buried in the adapter. This keeps `OllamaAdapter` a pure, dumb `LLMPort` implementation (easy to swap/mock) and keeps retry policy visible and testable as domain logic with a fake `LLMPort` that returns bad output on purpose.

Bounded retry count and fallback behavior (what "documented failure state" means concretely — e.g., a `Turn` marked `status=FAILED` with the raw invalid output preserved) will be finalized during implementation, not re-litigated here.

---

## LangGraph Placement

LangGraph is a **driving-adapter-adjacent orchestration tool**, not domain logic. The domain defines the state machine's *rules* (whose turn is next, when 2 rounds are complete, when to invoke Judge) as a plain Python `Debate` state object with a `next_step()` method. LangGraph nodes are thin wrappers that call into `DebateService`/domain methods and manage the actual execution graph/runtime.

This is the direct payoff of hexagonal here: if LangGraph is swapped for a different orchestrator later, `next_step()` logic doesn't move.

**Graph shape (fixed per PRD FR2):**

```
START → optimist_turn_1 → critic_turn_1 → optimist_turn_2 → critic_turn_2 → judge_verdict → END
```

Each node calls `Agent.take_turn()` (Template Method) through `DebateService`, which persists via `DebateRepositoryPort` and notifies via `PresenterPort` after each turn.

---

## PostgreSQL Schema (initial)

```sql
CREATE TABLE debates (
    id UUID PRIMARY KEY,
    topic TEXT NOT NULL,
    status TEXT NOT NULL,       -- in_progress | completed | failed
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE turns (
    id UUID PRIMARY KEY,
    debate_id UUID NOT NULL REFERENCES debates(id),
    agent_role TEXT NOT NULL,   -- optimist | critic | judge
    round_number INT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL,       -- ok | failed_validation
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE verdicts (
    id UUID PRIMARY KEY,
    debate_id UUID NOT NULL REFERENCES debates(id),
    winner TEXT,                -- optimist | critic | null (synthesis)
    reasoning TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Accessed only through `PostgresDebateRepository implements DebateRepositoryPort` — no raw SQL or ORM session ever appears outside this adapter.

---

## Consequences

**What becomes easier:**
- Unit testing domain logic with fake ports — no Ollama/Postgres needed for CI or fast local iteration.
- Swapping Streamlit for another frontend later (talks to the same FastAPI driving adapter).
- Adding the deferred mid-debate Judge intervention (PresenterPort already carries per-turn events).
- Explaining the codebase in an interview: each pattern has one clear home and a one-line justification.
- **Deployment**: hosted environments generally can't run local Ollama, so `LLMPort` was implemented a second time as `GroqAdapter` for deployment, with zero changes to domain code. This is the port abstraction paying for itself in practice, not just in theory — a stronger interview answer than a single adapter would have given.

**What becomes harder / costs more upfront:**
- More files and indirection than a single-script debate bot would need — acceptable per PRD Section 10 (explicitly a learning trade-off, not accidental over-engineering).
- Every new capability requires deciding "domain or adapter?" — a discipline cost, but the intended one.

**What we'll need to revisit:**
- Bounded retry count and exact fallback UX once real Phi-4-Mini failure rates are observed.
- Whether `DebateStrategy` needs more than one concrete strategy to justify itself, or stays a documented extension point for now.

---

## Planned Extension: Groq Rate-Limit Backoff (not yet implemented)

**Problem:** `GroqAdapter.generate()` currently catches all exceptions and re-raises a generic `RuntimeError`, discarding Groq's 429 `retry-after` information. Deployment on Groq means rate limits will be hit; the system should back off gracefully and let the user see it happening, rather than fail silently or hang.

**Decision:**
- `GroqAdapter` raises a typed `RateLimitedError(retry_after_seconds: float)` on 429, instead of a generic `RuntimeError`. The adapter's only job is translating the Groq-specific error into a domain-meaningful one — it does not itself wait or retry.
- The wait/retry loop lives in the **application layer** (the workflow/`DebateService`), not the adapter, because only the application layer has access to `PresenterPort` to emit progress to the client. Adapters stay dumb per hexagonal principles.
- This is a **separate retry mechanism from the Chain of Responsibility** used for response validity (see Chain of Responsibility section below). Rate-limit backoff is a transient-infrastructure concern; validity retry is a domain concern. Keeping them distinct avoids conflating two different failure categories into one mechanism.
- A new `DebateEventType.RATE_LIMITED` is added to the existing `DebateEvent`/SSE pipeline, carrying `retry_after_seconds`, so Streamlit can render a live countdown using the streaming infrastructure that already exists (`/debates/stream`).
- FastAPI-level rate limiting (protecting the API itself from abuse) is a separate, simpler concern — middleware (e.g. `slowapi`) at the driving-adapter boundary, no domain involvement.

**Open questions:** max wait/attempt bound before giving up entirely; whether a debate that fails after exhausted rate-limit retries should be marked `failed` in Postgres (consistent with the existing `status` column design) or left `in_progress` for manual resume.

---

## Planned Extension: MCP Research Tools (not yet implemented)

**Problem:** Agents currently argue from the topic and debate history alone, with no ability to ground claims in external information. Adding search/Wikipedia research also serves as a deliberate MCP learning goal.

**Decision:**
- Modeled as a **new port**, `ResearchPort`, with concrete adapters (`WebSearchAdapter`, `WikipediaAdapter`), consistent with the existing hexagonal boundary — research is external I/O, same category as `LLMPort`.
- **Strategy pattern, genuinely earned this time**: a `ResearchStrategy` interface with two concrete variants:
  - `NoResearchStrategy` — the current (implicit) behavior, formalized as an explicit strategy rather than "no strategy at all."
  - `UncertaintyTriggeredResearchStrategy` — research runs only when the agent flags uncertainty about a specific claim. This is the feature actually wanted; `NoResearchStrategy` exists as the baseline/default and is what makes this a real Strategy choice rather than a single-implementation interface.
  - Not modeled as part of `DebateStrategy` (argument construction) — kept as its own interface since it governs information-gathering, a distinct responsibility (see prior reasoning below, still holds).
- **Uncertainty detection: single-pass structured flag (not a second LLM call).** The same generation call that produces the argument/verdict also includes a structured marker when the model is unsure of a factual claim (e.g. a `Research needed: <claim>` line), parsed alongside the existing structured output (the same mechanism already used for the Judge's `Winner:`/`Reasoning:` parsing — extended, not duplicated). 
  - **Explicit trade-off accepted:** this is less reliable than a dedicated self-assessment call would be — the model may fail to flag claims it should. That's an acceptable degradation: on a missed flag, the agent simply argues without research, and the debate still completes normally. No broken state, no crash.
  - **Why not the two-call self-assessment approach:** doubling LLM calls per turn compounds Groq rate-limit exposure (see Rate-Limit Backoff section above) — the two features are coupled, and adding calls here directly increases how often rate limiting triggers. Given Groq's token/rate constraints, single-pass was chosen deliberately over reliability, and this trade-off is intentional, not an oversight.
- **Judge's scope is narrower than Optimist/Critic's**, and deliberately so: Judge does not conduct open-ended topic research. It only verifies specific claims *already made* by Optimist or Critic during the debate (fact-checking), using the same uncertainty-flag mechanism but applied to statements in the debate history rather than to its own draft argument. This preserves "the Judge evaluates the debate that happened" while still allowing it to catch factually wrong claims.
- `Agent`'s Template Method skeleton gains an explicit new step: `research() → build_prompt() → generate() → validate() → parse()`. `research()` delegates to the injected `ResearchStrategy`; `NoResearchStrategy.research()` is a no-op.

**Open questions:** exact prompt phrasing to reliably elicit the `Research needed:` marker from Phi-4-Mini/Groq without over-triggering; how much research content gets injected into the follow-up prompt (raw snippets vs. summarized); whether a flagged-but-unresearched claim (e.g. research call itself fails or rate-limits) should block the turn or just proceed with a caveat.



1. [ ] Define domain models (`Agent`, `Turn`, `Debate`, `Verdict`) with zero infra imports
2. [ ] Define ports (`LLMPort`, `DebateRepositoryPort`, `PresenterPort`) as `Protocol` classes
3. [ ] Implement `OllamaAdapter`
4. [ ] Implement `PostgresDebateRepository` + migrations for the schema above
5. [ ] Implement `ArgumentHandler` chain (`SchemaValidationHandler → RetryHandler → FallbackHandler`)
6. [ ] Implement `Agent` base (Template Method) + `OptimistAgent`, `CriticAgent`, `JudgeAgent`
7. [ ] Implement `DebateStrategy` interface + one concrete `default_strategy`
8. [ ] Wire LangGraph nodes as thin adapters calling `DebateService`
9. [ ] Composition root in FastAPI startup (DI wiring)
10. [ ] Unit tests for domain layer using fake ports (no live Ollama/Postgres)
11. [ ] Streamlit UI calling FastAPI endpoints
12. [ ] `RateLimitedError` in `GroqAdapter`; backoff loop + `RATE_LIMITED` event in application layer
13. [ ] `ResearchPort` + `WebSearchAdapter`/`WikipediaAdapter`; `research()` step added to `Agent` Template Method
14. [ ] FastAPI-level rate limiting middleware (e.g. `slowapi`)
