# Multi-Agent Debate System

A local-first multi-agent debate system designed with **Hexagonal Architecture (Ports & Adapters)** and orchestrated through **LangGraph**.

This repository demonstrates a structured, graph-based debate workflow where specialized agents collaborate and compete to generate, challenge, and evaluate arguments.

---

## 📖 Table of Contents
- [Goals & Motivation](#-goals--motivation)
- [Architecture & Design Patterns](#-architecture--design-patterns)
- [Debate Roles](#-debate-roles)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Running Tests](#-running-tests)
- [Notes](#-notes)
- [Future Roadmap](#-future-roadmap)

---

## 🎯 Goals & Motivation

This project is built to show how a multi-agent debate system can be architected cleanly and maintained independently of any specific LLM provider.

- **Graph-based orchestration** instead of linear prompt chaining
- **Domain isolation** using ports and adapters
- **Reusable debating agents** for Optimist, Critic, and Judge roles
- **Testable core behavior** without a live LLM

---

## 🏗️ Architecture & Design Patterns

The application uses **Hexagonal Architecture** to separate core domain logic from external integrations.

```
                  ┌──────────────────────────────┐
                  │            ADAPTERS          │
                  │   (Ollama, Groq, Storage)    │
                  └──────────────┬───────────────┘
                                 │ (Implements)
                                 ▼
                  ┌──────────────────────────────┐
                  │             PORTS            │
                  │     (LLMPort, Repository)    │
                  └──────────────┬───────────────┘
                                 │ (Uses)
                                 ▼
                  ┌──────────────────────────────┐
                  │         CORE DOMAIN          │
                  │  (Agents, Models, Prompts)   │
                  └──────────────────────────────┘
```

### Core components

- `app/core/domain/agents`: Agent classes with specialized debate behavior
- `app/core/domain/ports/llm_port.py`: LLM interface abstraction
- `app/core/domain/prompts`: Jinja2 prompt templates
- `app/core/domain/utils/prompt_renderer.py`: Prompt compilation helper
- `app/core/application/workflows/debate`: LangGraph workflow and state graph

### Design patterns used

- **Ports & Adapters**: Keeps the domain independent of external tools
- **Template Method**: Base agent flow defines prompt building, generation, validation, and parsing
- **Dependency Injection**: Adapters are injected into agents at runtime
- **Strategy**: Prompt selection and rendering are isolated from the agent logic

---

## 🎭 Debate Roles

1. **Optimist**
   - Advocates for the topic and emphasizes positive possibilities
   - Template: `app/core/domain/prompts/optimist_prompt.j2`
2. **Critic**
   - Challenges assumptions, exposes risks, and questions validity
   - Template: `app/core/domain/prompts/critic_prompt.j2`
3. **Judge**
   - Reviews the debate history and issues a final evaluation
   - Template: `app/core/domain/prompts/judge_prompt.j2`

---

## 📂 Project Structure

```text
├── app/
│   ├── core/
│   │   ├── adapters/          # External adapters (Ollama, Groq, etc.)
│   │   │   ├── GroqAdapter.py
│   │   │   └── OllamaAdapter.py
│   │   ├── application/       # Workflow orchestration
│   │   │   └── workflows/debate
│   │   ├── domain/            # Core business logic
│   │   │   ├── agents/
│   │   │   ├── models/
│   │   │   ├── ports/
│   │   │   ├── prompts/
│   │   │   └── utils/
├── tests/                    # Unit and integration tests
│   ├── unit/
│   └── integration/
├── main.py                   # Minimal application entrypoint
├── pyproject.toml            # Dependencies and metadata
├── uv.lock                   # Lockfile for uv package manager
└── multi_agent_debate_PRD.md # Product requirements document
```

---

## 🛠️ Tech Stack

- Python >= 3.14
- LangGraph for state graph orchestration
- Jinja2 for prompt templating
- Ollama and Groq adapters for local LLM inference
- Pytest and Pytest-asyncio for testing
- `uv` as package manager

---

## 🚀 Installation & Setup

1. Install prerequisites
   - Install [Ollama](https://ollama.com/) or another supported local model runtime
   - Install [uv](https://github.com/astral-sh/uv)

2. Install dependencies
   ```bash
   uv sync
   ```

3. Activate the virtual environment
   - Windows (PowerShell):
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Run the app
   ```bash
   python main.py
   ```

---

## 🧪 Running Tests

- Run all tests
  ```bash
  python -m pytest
  ```

- Run unit tests only
  ```bash
  python -m pytest tests/unit
  ```

- Run integration tests
  ```bash
  python -m pytest tests/integration
  ```

---

## 📄 Notes

- `DebateWorkflow` is implemented in `app/core/application/workflows/debate/workflow.py`
- `LLMPort` abstraction is in `app/core/domain/ports/llm_port.py`
- Adapters are located in `app/core/adapters`
- Prompt templates are stored in `app/core/domain/prompts`

---

## 🗺️ Future Roadmap

- Add persistent debate storage via a repository adapter
- Add an interactive web UI or Streamlit frontend
- Add structured JSON schema validation for Judge output
- Improve turn tracking and debate-state reporting in LangGraph
