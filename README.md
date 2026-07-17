# Multi-Agent Debate System

An offline, local-first multi-agent debate system structured using **Hexagonal Architecture (Ports & Adapters)** and orchestrated using **LangGraph**. 

This project is built to demonstrate real-world low-level design (LLD) software patterns (Strategy, Template Method, Dependency Injection, etc.) in an agentic workflow, using a local model running on [Ollama](https://ollama.com/) (Phi-4-Mini / Ministral-3:8b) for zero-cost API dependencies.

---

## 📖 Table of Contents
- [Goals & Motivation](#-goals--motivation)
- [Architecture & Design Patterns](#-architecture--design-patterns)
- [Debate Roles](#-debate-roles)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Running Tests](#-running-tests)
- [Future Roadmap](#-future-roadmap)

---

## 🎯 Goals & Motivation

Most "multi-agent" projects are thin wrappers around a single prompt looped sequentially. This project is built to demonstrate:
1. **Dynamic Multi-Agent Orchestration**: Coordinating specialized agents with unique personalities (Optimist, Critic, Judge) using a state-graph loop rather than linear scripts.
2. **Production-Ready System Design**: Implementing Hexagonal Architecture to isolate core business domain logic from infrastructure details (like specific databases or LLM providers).
3. **Clean Low-Level Design (LLD)**: Utilizing established design patterns because they solve actual system complexities, not just for resume padding.

---

## 🏗️ Architecture & Design Patterns

The application is structured using **Hexagonal Architecture (Ports & Adapters)**:

```
                  ┌──────────────────────────────┐
                  │            ADAPTERS          │
                  │  (Ollama, PostgreSQL, UI)    │
                  └──────────────┬───────────────┘
                                 │ (Implements)
                                 ▼
                  ┌──────────────────────────────┐
                  │             PORTS            │
                  │   (LLMPort, RepositoryPort)  │
                  └──────────────┬───────────────┘
                                 │ (Uses)
                                 ▼
                  ┌──────────────────────────────┐
                  │         CORE DOMAIN          │
                  │  (Agents, State, Templates)  │
                  └──────────────────────────────┘
```

* **Core Domain**: Contains the main business entities (`TurnContext`, `DebateMessage`), base agent structures (`Agent`), prompt rendering (`prompt_renderer.py`), and the state machine rules.
* **Ports**: Boundary interfaces (like `LLMPort` and `DebateRepositoryPort`) defining how the domain interacts with the outside world.
* **Adapters**: Concrete implementations (like `OllamaAdapter` for local inference and `PostgreSQL` for storage) plugged in through dependency injection.

### Applied Design Patterns
* **Ports & Adapters**: Keeps the core domain completely framework-agnostic.
* **Template Method**: The base [Agent](app/core/domain/agents/base.py) class defines the skeleton of turn execution (`build_prompt` $\rightarrow$ `generate` $\rightarrow$ `validate` $\rightarrow$ `parse`), leaving specialized prompt building to individual agent subclasses.
* **Dependency Injection**: Adapters are passed into agents and services at runtime (e.g. passing `LLMPort` implementation to the `Agent` base class).
* **Strategy Pattern**: Prompts are dynamically compiled using Jinja2 templates, keeping prompt engineering strategy separate from python logical execution.

---

## 🎭 Debate Roles

The debate takes place in a structured conversational graph:

1. **Optimist** (Proponent):
   * Focuses on positive outcomes, constructive reasoning, and opportunities.
   * Template: [optimist_prompt.j2](app/core/domain/prompts/optimist_prompt.j2)
2. **Critic** (Opponent):
   * Identifies unproven assumptions, logical fallacies, and potential risks in the Optimist's argument.
   * Template: [critic_prompt.j2](app/core/domain/prompts/critic_prompt.j2)
3. **Judge** (Evaluator):
   * Analyzes the conversation flow, evaluates the validity of the arguments, and delivers a structured verdict.
   * Template: [judge_prompt.j2](app/core/domain/prompts/judge_prompt.j2)

---

## 📂 Project Structure

```text
├── app/
│   ├── core/
│   │   ├── adapters/          # Infrastructure adapters (Ollama, PostgreSQL, etc.)
│   │   │   └── OllamaAdapter.py
│   │   ├── domain/            # Core business logic (isolated from external tools)
│   │   │   ├── agents/        # Agent classes (Optimist, Critic, Judge)
│   │   │   │   ├── base.py
│   │   │   │   ├── optimist.py
│   │   │   │   ├── critic.py
│   │   │   │   └── judge.py
│   │   │   ├── models/        # Data models & schemas (TurnContext, DebateMessage)
│   │   │   │   └── turn_context.py
│   │   │   ├── ports/         # Outbound and inbound interfaces
│   │   │   │   └── llm_port.py
│   │   │   ├── prompts/       # Jinja2 templates for LLM prompts
│   │   │   │   ├── optimist_prompt.j2
│   │   │   │   ├── critic_prompt.j2
│   │   │   │   └── judge_prompt.j2
│   │   │   └── utils/         # Prompt loaders and shared helpers
│   │   │       └── prompt_renderer.py
│   └── __init__.py
├── tests/
│   ├── unit/                  # Mocked unit tests (runs offline without Ollama)
│   │   └── test_agent_prompt.py
│   └── integration/           # End-to-end adapter and agent execution tests
│       ├── test_ollama_adapter.py
│       ├── test_optimist_agent.py
│       ├── test_critic_agent.py
│       └── test_judge_agent.py
├── pyproject.toml             # Project dependency configuration
├── uv.lock                    # Fast package manager lockfile
└── multi_agent_debate_PRD.md  # Product Requirements Document
```

---

## 🛠️ Tech Stack

* **Language**: Python >= 3.12 (using Python 3.14 features)
* **Local Inference**: Ollama (model: `phi4` or `ministral-3:8b`)
* **State Machine**: LangGraph (for state-graph loops & memory)
* **Testing**: Pytest & Pytest-asyncio
* **Package Manager**: [uv](https://github.com/astral-sh/uv) (for ultra-fast and reliable environment management)

---

## 🚀 Installation & Setup

1. **Install Prerequisites**:
   * Install [Ollama](https://ollama.com/) and run the service locally.
   * Pull the target model (e.g., `ollama pull ministral-3:8b` or whichever model you configure).
   * Install [uv](https://github.com/astral-sh/uv) package manager.

2. **Clone and Initialize Environment**:
   ```bash
   git clone https://github.com/NAVIN-STAR/Multi_Agent_Debate.git
   cd Multi_Agent_Debate
   uv sync
   ```

3. **Activate Virtual Environment**:
   * On Windows (PowerShell):
     ```powershell
     .venv\Scripts\activate
     ```
   * On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

---

## 🧪 Running Tests

All core logic is completely mockable, allowing quick verification without sending requests to local models.

* **Run all Unit Tests** (Offline / Instant):
  ```bash
  python -m pytest tests/unit/
  ```

* **Run a single test in isolation**:
  ```bash
  python -m pytest tests/unit/test_agent_prompt.py::test_optimist_build_prompt
  ```

* **Run all Integration Tests** (Requires Ollama running locally):
  ```bash
  python -m pytest tests/integration/
  ```

---

## 🗺️ Future Roadmap

- [ ] Integrate **LangGraph** to manage debate states and loop iteration limits.
- [ ] Add the **PostgreSQL repository port** for persistency of debate histories.
- [ ] Build a **Streamlit Web UI** for entering topics and displaying real-time agent arguments.
- [ ] Add structured JSON validation for the **Judge verdict**.
