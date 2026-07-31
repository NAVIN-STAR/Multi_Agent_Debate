from collections.abc import Hashable

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.core.application.workflows.debate.Nodes import (
    CriticNode,
    JudgeNode,
    OptimistNode,
)
from app.core.application.workflows.debate.routing import route
from app.core.domain.models.turn_context import DebateState, Speaker

ROUTING_MAP: dict[Hashable, str] = {
    Speaker.OPTIMIST: "optimist",
    Speaker.CRITIC: "critic",
    Speaker.JUDGE: "judge",
}


class DebateGraph:
    def __init__(
        self,
        optimist_node: OptimistNode,
        critic_node: CriticNode,
        judge_node: JudgeNode,
    ) -> None:
        self._optimist_node = optimist_node
        self._critic_node = critic_node
        self._judge_node = judge_node

    def build(self) -> CompiledStateGraph:
        builder = StateGraph(DebateState)

        # 1. Register Nodes
        builder.add_node("optimist", self._optimist_node.execute)
        builder.add_node("critic", self._critic_node.execute)
        builder.add_node("judge", self._judge_node.execute)

        # 2. Wire Edges & Routing
        builder.add_edge(START, "optimist")
        builder.add_conditional_edges("optimist", route, ROUTING_MAP)
        builder.add_conditional_edges("critic", route, ROUTING_MAP)
        builder.add_edge("judge", END)

        # 3. Return Executable Application
        return builder.compile()
