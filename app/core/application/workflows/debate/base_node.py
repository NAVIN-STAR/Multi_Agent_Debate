from abc import ABC, abstractmethod

from app.core.domain.agents.base import Agent
from app.core.domain.models.models import DebateMessage, DebateState, TurnContext


class BaseNode(ABC):
    """Base class for workflow nodes that process a single agent turn."""

    def __init__(self, agent: Agent) -> None:
        self.agent = agent
        super().__init__()

    @abstractmethod
    def update_state(
        self,
        state: DebateState,
        updated_context: TurnContext,
    ) -> DebateState: ...

    async def execute(self, state: DebateState) -> DebateState:
        turn_context = state["turn_context"]
        response = await self.agent.take_turn(turn_context=turn_context)

        message = DebateMessage(speaker=self.agent.name, content=response)
        updated_context = TurnContext(
            topic=turn_context.topic,
            history=[*turn_context.history, message],
            round_number=turn_context.round_number,
        )
        return self.update_state(
            state=state,
            updated_context=updated_context,
        )
