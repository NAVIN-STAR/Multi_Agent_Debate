from typing import cast

from langgraph.graph.state import CompiledStateGraph

from app.core.application.workflows.debate.graph import DebateGraph
from app.core.application.workflows.debate.Nodes import (
    CriticNode,
    JudgeNode,
    OptimistNode,
)
from app.core.domain.agents.critic import Critic
from app.core.domain.agents.judge import Judge
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.turn_context import (
    DebateRequest,
    DebateResponse,
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
    def _create_agents(self)->tuple[Optimist, Critic, Judge]:
        return (Optimist(self.llm), Critic(self.llm), Judge(self.llm))

    # Responsible for creating nodes
    def _create_nodes(self, optimist: Optimist, critic: Critic, judge: Judge)->tuple[OptimistNode, CriticNode, JudgeNode]:
        return (OptimistNode(optimist), CriticNode(critic), JudgeNode(judge))

    # Responsible for building graph
    def _create_graph(
        self,
        optimist_node: OptimistNode,
        critic_node: CriticNode,
        judge_node: JudgeNode,
    )->CompiledStateGraph:
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

    def _map_to_response(self,result:DebateState)->DebateResponse:
        return DebateResponse(
            topic=result['turn_context'].topic,
            history=result['turn_context'].history,
            verdict=result['verdict'],
        )
        

    async def run(self, request: DebateRequest):
        initial_state = self._create_initial_state(request)

        optimist, critic, judge = self._create_agents()

        optimist_node, critic_node, judge_node = self._create_nodes(
            optimist,
            critic,
            judge,
        )
        graph=self._create_graph(
            optimist_node, critic_node, judge_node
        )
        result = cast(DebateState, await graph.ainvoke(initial_state))
        return self._map_to_response(result=result)

