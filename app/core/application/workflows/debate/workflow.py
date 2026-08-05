from typing import cast

from langgraph.graph.state import CompiledStateGraph

from app.core.application.dto.debate_event import DebateEventType
from app.core.application.dto.debate_models import DebateRequest, DebateResponse
from app.core.application.mappers.debate_mappers import to_event, to_response, to_started_event
from app.core.application.workflows.debate.graph import DebateGraph
from app.core.application.workflows.debate.Nodes import (
    CriticNode,
    JudgeNode,
    OptimistNode,
)
from app.core.domain.agents.critic import Critic
from app.core.domain.agents.judge import Judge
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.models import (
    DebateState,
    Speaker,
    TurnContext,
)
from app.core.domain.ports.llm_port import LLMPort


class DebateWorkflow:
    def __init__(self, llm: LLMPort, max_rounds: int = 2) -> None:
        self.llm = llm
        self.max_rounds = max_rounds

    # Responsible for creating agents
    def _create_agents(self) -> tuple[Optimist, Critic, Judge]:
        return (Optimist(self.llm), Critic(self.llm), Judge(self.llm))

    # Responsible for creating nodes
    def _create_nodes(
        self, optimist: Optimist, critic: Critic, judge: Judge
    ) -> tuple[OptimistNode, CriticNode, JudgeNode]:
        return (OptimistNode(optimist), CriticNode(critic), JudgeNode(judge))

    # Responsible for building graph
    def _create_graph(
        self,
        optimist_node: OptimistNode,
        critic_node: CriticNode,
        judge_node: JudgeNode,
    ) -> CompiledStateGraph:
        return DebateGraph(
            optimist_node=optimist_node,
            critic_node=critic_node,
            judge_node=judge_node,
        ).build()

    def _create_initial_state(self, request: DebateRequest) -> DebateState:
        turn_context = TurnContext(
            topic=request.topic,
        )

        return {
            "turn_context": turn_context,
            "current_speaker": Speaker.OPTIMIST,
            "max_rounds": request.max_rounds,
            "verdict": None,
        }


    def _prepare_execution(
    self,
    request: DebateRequest,
) -> tuple[CompiledStateGraph, DebateState]:
        initial_state = self._create_initial_state(request)

        optimist, critic, judge = self._create_agents()

        optimist_node, critic_node, judge_node = self._create_nodes(
            optimist,
            critic,
            judge,
        )

        graph = self._create_graph(
            optimist_node,
            critic_node,
            judge_node,
        )

        return graph, initial_state



    async def run(self, request: DebateRequest):
        graph, initial_state = self._prepare_execution(request)

        result = cast(
            DebateState,
            await graph.ainvoke(initial_state),
        )
        return to_response(result)

    async def stream(self, request: DebateRequest):
        graph, initial_state = self._prepare_execution(request)

        # 1. Optimist is about to think
        yield to_started_event(initial_state)
        # 2. Stream graph execution
        first=True
        async for state in graph.astream(
                initial_state,
            stream_mode="values",
        ):
            state = cast(DebateState, state)

            #Skip first yield as it yields initial state with empty history
            if first:
                first = False
                continue

            # 3. Completed node
            if state["verdict"] is None:
                yield to_event(
                    state=state,
                    event_type=DebateEventType.RESPONSE,
                )
                yield to_started_event(state)
            else:
                yield to_event(
                    state,
                    DebateEventType.FINISHED,
                )
                break
