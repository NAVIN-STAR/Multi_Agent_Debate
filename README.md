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
- **Interactive UI & APIs** supporting real-time streaming updates

---

## 🏗️ Architecture & Design Patterns

The application uses **Hexagonal Architecture** to separate core domain logic from external integrations.

```
       ┌────────────────────────────────────────────────────────┐
       │                   PRESENTATION LAYER                   │
       │           (Streamlit Web App, FastAPI Server)          │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Invokes)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                   APPLICATION WORKFLOW                 │
       │             (DebateWorkflow, DebateGraph)              │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Uses)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                         PORTS                          │
       │                       (LLMPort)                        │
       └───────────────────────────▲────────────────────────────┘
                                   │ (Implements / Plugs into)
       ┌───────────────────────────┴────────────────────────────┐
       │                       ADAPTERS                         │
       │                 (Ollama, Groq Adapters)                │
       └────────────────────────────────────────────────────────┘
                                   │ (Uses)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                      CORE DOMAIN                       │
       │           (Agents, models.py, prompts, utils)          │
       └────────────────────────────────────────────────────────┘
```

### Core components

- `app/core/domain/agents`: Agent classes with specialized debate behavior
- `app/core/domain/ports/llm_port.py`: LLM interface abstraction
- `app/core/domain/prompts`: Jinja2 prompt templates
- `app/core/domain/utils/prompt_renderer.py`: Prompt compilation helper
- `app/core/application/workflows/debate`: LangGraph workflow and state graph
- `app/presentation/api`: FastAPI application structure
- `app/ui/streamlit`: Streamlit frontend application

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
│   │   ├── application/       # Application logic & workflow orchestration
│   │   │   ├── dto/           # Data Transfer Objects
│   │   │   │   ├── debate_event.py
│   │   │   │   └── debate_models.py
│   │   │   ├── mappers/       # Core domain mappers
│   │   │   │   └── debate_mappers.py
│   │   │   └── workflows/     # LangGraph workflows
│   │   │       └── debate/
│   │   │           ├── base_node.py
│   │   │           ├── graph.py
│   │   │           ├── nodes.py
│   │   │           ├── routing.py
│   │   │           └── workflow.py
│   │   └── domain/            # Core business logic (isolated)
│   │       ├── agents/        # Specialized debating agents (Optimist, Critic, Judge)
│   │       ├── models/        # Pure domain models (models.py)
│   │       ├── ports/         # LLM boundary interfaces (llm_port.py)
│   │       ├── prompts/       # Jinja2 prompt templates
│   │       └── utils/         # Prompt rendering utility
│   ├── presentation/
│   │   └── api/               # FastAPI REST & Streaming WebSocket API endpoints
│   │       ├── app.py
│   │       ├── dependencies.py
│   │       ├── mappers/
│   │       ├── routers/
│   │       └── schemas/
│   └── ui/
│       └── streamlit/         # Streamlit web interface
│           ├── api_client.py
│           ├── streamlit_app.py
│           └── components/
├── docs/                      # Codebase architecture graphs & documentation
│   └── codebase_graph.md
├── tests/                    # Comprehensive Unit and Integration test suite
│   ├── unit/                 # Node and Graph tests
│   ├── integration/          # API, streaming, and adapter tests
│   ├── buliders/             # Test state builders (typo in directory name)
│   └── fakes/                # In-memory mock/fake implementations
├── main.py                   # CLI/minimal application entrypoint
├── pyproject.toml            # Project dependencies and configurations
├── uv.lock                   # Package lockfile
└── multi_agent_debate_PRD.md # Product Requirements Document
```

---

## 🛠️ Tech Stack

- **Core Logic & Language**: Python >= 3.14
- **State Orchestration**: LangGraph (for multi-agent conversation state graph)
- **API Framework**: FastAPI (providing HTTP POST endpoints and server-sent streaming events)
- **Frontend Client**: Streamlit (fully reactive web-based chat-like UI)
- **Prompt Templating**: Jinja2
- **LLM Integrations**: Groq (Llama-3.3-70b) and Ollama (local Phi-4-Mini) adapters
- **Testing Suite**: Pytest & Pytest-asyncio
- **Package Manager**: `uv` (fast dependency resolution and environment management)

---

## 🚀 Installation & Setup

1. Install prerequisites
   - Install [Ollama](https://ollama.com/) or configure your Groq credentials in `.env`
   - Install [uv](https://github.com/astral-sh/uv)

2. Create `.env` file from configuration settings:
   ```env
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   # OLLAMA_MODEL=phi-4-mini
   ```

3. Install dependencies
   ```bash
   uv sync
   ```

4. Activate the virtual environment
   - Windows (PowerShell):
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. Run the application
   - **CLI (Single Command execution)**:
     ```bash
     python main.py
     ```

   - **FastAPI Backend (Port 8000)**:
     ```bash
     uvicorn app.presentation.api.app:app --host 0.0.0.0 --port 8000 --reload
     ```

   - **Streamlit Frontend (Runs UI)**:
     ```bash
     streamlit run app/ui/streamlit/streamlit_app.py
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

- Detailed architecture diagrams, LLD, class hierarchy, and state transition maps are available in [codebase_graph.md](docs/codebase_graph.md).
- `DebateWorkflow` coordinates the execution and is located in `app/core/application/workflows/debate/workflow.py`.
- `LLMPort` abstraction interface is in `app/core/domain/ports/llm_port.py`.
- Adapters are located in `app/core/adapters/`.
- Prompt templates are stored in `app/core/domain/prompts/`.

---

## 🗺️ Future Roadmap

- `[x]` Add an interactive web UI / Streamlit frontend
- `[x]` Add FastAPI support with streaming events
- `[ ]` Add persistent debate storage via a repository adapter
- `[ ]` Add structured JSON schema validation for Judge output
- `[ ]` Improve turn tracking and debate-state reporting in LangGraph
