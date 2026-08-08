# Codebase Graph: Multi-Agent Debate System

This file is tracked inside the repository under `docs/codebase_graph.md`. You can commit this to Git and update it as the project evolves.

---

## 📂 1. Directory & File Structure

```mermaid
graph TD
    root["📁 multi-agent-debate-system/"]
    root --> app["📁 app/"]
    root --> tests["📁 tests/"]
    root --> config_files["Configuration / PRD"]

    subgraph app_folder ["app/ Core Logic & Interface"]
        app --> core["📁 core/"]
        app --> presentation["📁 presentation/"]
        app --> ui["📁 ui/"]

        core --> adapters["📁 adapters/"]
        core --> domain["📁 domain/"]
        core --> application["📁 application/"]

        adapters --> ollama_adapter["📄 OllamaAdapter.py"]
        adapters --> groq_adapter["📄 GroqAdapter.py"]

        domain --> domain_agents["📁 agents/"]
        domain --> domain_models["📁 models/"]
        domain --> domain_ports["📁 ports/"]
        domain --> domain_prompts["📁 prompts/"]
        domain --> domain_utils["📁 utils/"]

        domain_agents --> agent_base["📄 base.py"]
        domain_agents --> agent_optimist["📄 optimist.py"]
        domain_agents --> agent_critic["📄 critic.py"]
        domain_agents --> agent_judge["📄 judge.py"]

        domain_models --> model_domain["📄 models.py"]
        domain_ports --> port_llm["📄 llm_port.py"]
        domain_prompts --> template_opt["📄 optimist_prompt.j2"]
        domain_prompts --> template_crit["📄 critic_prompt.j2"]
        domain_prompts --> template_judge["📄 judge_prompt.j2"]
        domain_utils --> prompt_renderer["📄 prompt_renderer.py"]

        application --> application_dto["📁 dto/"]
        application --> application_mappers["📁 mappers/"]
        application --> app_workflows["📁 workflows/debate/"]

        application_dto --> dto_event["📄 debate_event.py"]
        application_dto --> dto_models["📄 debate_models.py"]
        application_mappers --> mapper_debate["📄 debate_mappers.py"]

        app_workflows --> workflow_base_node["📄 base_node.py"]
        app_workflows --> workflow_nodes["📄 nodes.py"]
        app_workflows --> workflow_routing["📄 routing.py"]
        app_workflows --> workflow_graph["📄 graph.py"]
        app_workflows --> workflow_main["📄 workflow.py"]
      
        presentation --> presentation_api["📁 api/"]
        presentation_api --> api_app["📄 app.py"]
        presentation_api --> api_deps["📄 dependencies.py"]
        presentation_api --> api_mappers["📁 mappers/"]
        presentation_api --> api_routers["📁 routers/"]
        presentation_api --> api_schemas["📁 schemas/"]
      
        api_mappers --> api_mapper_file["📄 api_mapper.py"]
        api_routers --> api_router_file["📄 debate.py"]
        api_schemas --> api_schema_file["📄 debate_schemas.py"]

        ui --> ui_streamlit["📁 streamlit/"]
        ui_streamlit --> streamlit_app["📄 streamlit_app.py"]
        ui_streamlit --> streamlit_client["📄 api_client.py"]
        ui_streamlit --> streamlit_components["📁 components/"]
        streamlit_components --> streamlit_comp["📄 debate_component.py"]
    end

    subgraph test_folder ["tests/ Testing Suite"]
        tests --> test_unit["📁 unit/"]
        tests --> test_integration["📁 integration/"]
        tests --> test_fakes["📁 fakes/"]
        tests --> test_builders["📁 buliders/"]
        tests --> test_conftest["📄 conftest.py"]

        test_unit --> test_agent_prompt["📄 test_agent_prompt.py"]
        test_unit --> test_unit_opt["📄 test_optimist_node.py"]
        test_unit --> test_unit_crit["📄 test_critic_node.py"]
        test_unit --> test_unit_judge["📄 test_judge_node.py"]
        test_unit --> test_unit_graph["📄 test_graph.py"]

        test_integration --> test_int_ollama["📄 test_ollama_adapter.py"]
        test_integration --> test_int_groq["📄 test_groq_adapter.py"]
        test_integration --> test_int_opt["📄 test_optimist_agent.py"]
        test_integration --> test_int_crit["📄 test_critic_agent.py"]
        test_integration --> test_int_judge["📄 test_judge_agent.py"]
        test_integration --> test_int_workflow["📄 test_workflow.py"]
        test_integration --> test_int_stream_workflow["📄 test_stream_workflow.py"]
        test_integration --> test_int_api["📁 api/"]
      
        test_int_api --> test_api_debate["📄 test_debate_api.py"]
        test_int_api --> test_api_stream["📄 test_debate_stream_api.py"]

        test_fakes --> fake_llm["📄 fake_llm.py"]
        test_builders --> builder_factory["📄 debate_state_factory.py"]
    end

    subgraph configs ["Root Files"]
        config_files --> main_py["📄 main.py"]
        config_files --> prd_md["📄 multi_agent_debate_PRD.md"]
        config_files --> readme_md["📄 README.md"]
        config_files --> pyproject_toml["📄 pyproject.toml"]
        config_files --> uv_lock["📄 uv.lock"]
    end

    %% Styles
    classDef folder fill:#1E293B,stroke:#475569,stroke-width:2px,color:#F8FAFC;
    classDef pythonFile fill:#0F172A,stroke:#38BDF8,stroke-width:1px,color:#F1F5F9;
    classDef otherFile fill:#0F172A,stroke:#94A3B8,stroke-width:1px,color:#CBD5E1;

    class root,app,tests,core,adapters,domain,application,application_dto,application_mappers,app_workflows,domain_agents,domain_models,domain_ports,domain_prompts,domain_utils,presentation,presentation_api,api_mappers,api_routers,api_schemas,ui,ui_streamlit,streamlit_components,test_unit,test_integration,test_fakes,test_builders,test_int_api folder;
    class ollama_adapter,groq_adapter,agent_base,agent_optimist,agent_critic,agent_judge,model_domain,port_llm,prompt_renderer,dto_event,dto_models,mapper_debate,workflow_base_node,workflow_nodes,workflow_routing,workflow_graph,workflow_main,api_app,api_deps,api_mapper_file,api_router_file,api_schema_file,streamlit_app,streamlit_client,streamlit_comp,test_agent_prompt,test_unit_opt,test_unit_crit,test_unit_judge,test_unit_graph,test_int_ollama,test_int_groq,test_int_opt,test_int_crit,test_int_judge,test_int_workflow,test_int_stream_workflow,test_api_debate,test_api_stream,fake_llm,builder_factory,main_py pythonFile;
    class template_opt,template_crit,template_judge,prd_md,readme_md,pyproject_toml,uv_lock otherFile;
```

---

## 🏗️ 2. Hexagonal Architecture (Ports & Adapters)

```mermaid
flowchart TB
    subgraph Presentation ["PRESENTATION LAYER (UI / API Interfaces)"]
        streamlit_app["Streamlit Web App<br/>(app/ui/streamlit/streamlit_app.py)"]
        fastapi_app["FastAPI API Server<br/>(app/presentation/api/app.py)"]
    end

    subgraph Adapters ["ADAPTERS (Infrastructure - External)"]
        ollama_adapter["OllamaAdapter<br/>(app/core/adapters/OllamaAdapter.py)"]
        groq_adapter["GroqAdapter<br/>(app/core/adapters/GroqAdapter.py)"]
    end

    subgraph Ports ["PORTS (Boundaries - Interfaces)"]
        llm_port["LLMPort<br/>(app/core/domain/ports/llm_port.py)"]
    end

    subgraph CoreDomain ["CORE DOMAIN (Pure Business Logic)"]
        subgraph Models ["Models"]
            turn_ctx["TurnContext / DebateMessage / Speaker / DebateState<br/>(app/core/domain/models/models.py)"]
        end

        subgraph Agents ["Agents"]
            base_agent["Agent (base.py)"]
            optimist["Optimist (optimist.py)"]
            critic["Critic (critic.py)"]
            judge["Judge (judge.py)"]
        end

        subgraph Utils ["Utils"]
            prompt_renderer["prompt_renderer.py"]
        end
    end

    subgraph Workflows ["APPLICATION WORKFLOW (Orchestrators & Nodes)"]
        debate_workflow["DebateWorkflow<br/>(app/core/application/workflows/debate/workflow.py)"]
        debate_graph["DebateGraph<br/>(app/core/application/workflows/debate/graph.py)"]
        base_node["BaseNode (base_node.py)"]
        optimist_node["OptimistNode (nodes.py)"]
        critic_node["CriticNode (nodes.py)"]
        judge_node["JudgeNode (nodes.py)"]
    end

    %% Dependency & Execution Flow
    streamlit_app -->|Sends requests / Streams events| fastapi_app
    fastapi_app -->|Invokes| debate_workflow
    debate_workflow -->|Creates & Configures| debate_graph
    debate_workflow -->|Coordinates| optimist_node
    debate_workflow -->|Coordinates| critic_node
    debate_workflow -->|Coordinates| judge_node

    ollama_adapter -->|Implements / Plugs into| llm_port
    groq_adapter -->|Implements / Plugs into| llm_port
    base_agent -->|Depends on / Uses| llm_port
    base_agent -->|Uses| turn_ctx

    optimist -->|Inherits / Extends| base_agent
    critic -->|Inherits / Extends| base_agent
    judge -->|Inherits / Extends| base_agent

    optimist -->|Uses| prompt_renderer
    critic -->|Uses| prompt_renderer
    judge -->|Uses| prompt_renderer

    prompt_renderer -->|Populates fields of| turn_ctx

    base_node -->|Composes / Wraps| base_agent
    optimist_node -->|Inherits| base_node
    critic_node -->|Inherits| base_node
    judge_node -->|Inherits| base_node

    debate_graph -->|Uses Nodes to execute| base_node

    %% Styles
    classDef presentation fill:#4B5563,stroke:#374151,stroke-width:2px,color:#FFFFFF;
    classDef adapters fill:#B91C1C,stroke:#EF4444,stroke-width:2px,color:#FFFFFF;
    classDef ports fill:#D97706,stroke:#F59E0B,stroke-width:2px,color:#FFFFFF;
    classDef core fill:#047857,stroke:#10B981,stroke-width:2px,color:#FFFFFF;
    classDef workflows fill:#1D4ED8,stroke:#3B82F6,stroke-width:2px,color:#FFFFFF;

    class streamlit_app,fastapi_app presentation;
    class ollama_adapter,groq_adapter adapters;
    class llm_port ports;
    class turn_ctx,base_agent,optimist,critic,judge,prompt_renderer core;
    class debate_workflow,debate_graph,base_node,optimist_node,critic_node,judge_node workflows;
```

---

## 🎨 3. Low-Level Design (LLD) Class Hierarchy

```mermaid
classDiagram
    class LLMPort {
        <<Protocol / Interface>>
        +generate(prompt: str) str*
    }

    class OllamaAdapter {
        +client: AsyncClient
        +model: str
        +generate(prompt: str) str
    }

    class GroqAdapter {
        +client: AsyncGroq
        +api_key: str
        +model: str
        +base_url: str
        +generate(prompt: str) str
    }

    class Agent {
        <<Abstract>>
        +llm: LLMPort
        +name Speaker*
        +take_turn(turn_context: TurnContext) str
        +build_prompt(turn_context: TurnContext) str*
        +validate_response(response: str) void
        +parse_response(response: str) str
    }

    class Optimist {
        +name Speaker
        +build_prompt(turn_context: TurnContext) str
    }

    class Critic {
        +name Speaker
        +build_prompt(turn_context: TurnContext) str
    }

    class Judge {
        +name Speaker
        +build_prompt(turn_context: TurnContext) str
    }

    class BaseNode {
        <<Abstract>>
        +agent: Agent
        +update_state(state: DebateState, updated_context: TurnContext) DebateState*
        +execute(state: DebateState) DebateState
    }

    class OptimistNode {
        +update_state(state: DebateState, updated_context: TurnContext) DebateState
    }

    class CriticNode {
        +update_state(state: DebateState, updated_context: TurnContext) DebateState
    }

    class JudgeNode {
        +update_state(state: DebateState, updated_context: TurnContext) DebateState
    }

    class Speaker {
        <<Enum>>
        OPTIMIST = "optimist"
        CRITIC = "critic"
        JUDGE = "judge"
    }

    class DebateState {
        <<TypedDict>>
        +turn_context: TurnContext
        +current_speaker: Speaker
        +verdict: str | None
        +max_rounds: int
    }

    class DebateGraph {
        -optimist_node: OptimistNode
        -critic_node: CriticNode
        -judge_node: JudgeNode
        +build() CompiledStateGraph
    }

    class DebateWorkflow {
        +llm: LLMPort
        +max_rounds: int
        -_create_agents() tuple[Optimist, Critic, Judge]
        -_create_nodes(optimist, critic, judge) tuple[OptimistNode, CriticNode, JudgeNode]
        -_create_graph(opt_node, crit_node, judge_node) CompiledStateGraph
        -_create_initial_state(request) DebateState
        -_prepare_execution(request) tuple[CompiledStateGraph, DebateState]
        +run(request: DebateRequest) DebateResponse
        +stream(request: DebateRequest) AsyncGenerator
    }

    LLMPort <|.. OllamaAdapter : Implements
    LLMPort <|.. GroqAdapter : Implements
    Agent o-- LLMPort : Uses (Dependency Injection)
    Agent <|-- Optimist : Extends (Template Method)
    Agent <|-- Critic : Extends (Template Method)
    Agent <|-- Judge : Extends (Template Method)
    BaseNode o-- Agent : Composes (Wraps)
    BaseNode <|-- OptimistNode
    BaseNode <|-- CriticNode
    BaseNode <|-- JudgeNode
    DebateState o-- Speaker : Uses
    DebateWorkflow o-- LLMPort : Uses
    DebateWorkflow o-- DebateGraph : Builds
    DebateGraph o-- OptimistNode : Composes
    DebateGraph o-- CriticNode : Composes
    DebateGraph o-- JudgeNode : Composes
```

---

## 🔄 4. Workflows & State Transitions (LangGraph)

```mermaid
stateDiagram-v2
    [*] --> Start : User Inputs Debate Topic & Max Rounds

    state Start {
        [*] --> InitState : Initialize DebateState<br/>(current_speaker = Speaker.OPTIMIST,<br/>max_rounds = N,<br/>round_number = 1)
    }

    InitState --> Router

    state Router <<choice>>
  
    Router --> OptimistNode : If current_speaker == Speaker.OPTIMIST
    Router --> CriticNode : If current_speaker == Speaker.CRITIC
    Router --> JudgeNode : If current_speaker == Speaker.JUDGE

    OptimistNode --> Router : Sets current_speaker = Speaker.CRITIC
  
    CriticNode --> Router : Increments round_number<br/>Sets current_speaker = Speaker.JUDGE (if round > max_rounds)<br/>Else current_speaker = Speaker.OPTIMIST

    JudgeNode --> [*] : Sets verdict = content of final judge message

    %% Notes
    note right of OptimistNode
        OptimistNode runs:
        - Gets history and topic
        - Renders optimist_prompt.j2
        - Generates Proponent argument
        - Appends to TurnContext.history
    end note

    note right of CriticNode
        CriticNode runs:
        - Gets history and topic
        - Renders critic_prompt.j2
        - Generates Challenging argument
        - Appends to TurnContext.history
    end note

    note right of JudgeNode
        JudgeNode runs:
        - Evaluates history
        - Renders judge_prompt.j2
        - Generates final verdict
        - Sets DebateState["verdict"]
    end note
```
