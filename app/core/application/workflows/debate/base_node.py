from abc import ABC, abstractmethod

from app.core.domain.agents.base import Agent
from app.core.domain.models.turn_context import DebateMessage, DebateState, TurnContext


class BaseNode(ABC):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent
        super().__init__()


    def update_state(self,state: DebateState, response: str,) -> DebateState:
        return state


    async def execute(self, state: DebateState) -> DebateState:
        turn_context = state["turn_context"]
        response = await self.agent.take_turn(turn_context=turn_context)

        message = DebateMessage(speaker=self.agent.name, content=response)
        new_context = TurnContext(
            topic=turn_context.topic,
            history=[*turn_context.history, message],
            round_number=turn_context.round_number,
        )
        new_state:DebateState= {
                        "turn_context": new_context,
                        "verdict": state["verdict"],
                    }
        return self.update_state(state=new_state,response=response)
