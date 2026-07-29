from app.core.application.workflows.debate.base_node import BaseNode
from app.core.domain.models.turn_context import DebateState


class OptimistNode(BaseNode):
    pass

class CriticNode(BaseNode):
    pass


class JudgeNode(BaseNode):

    def update_state(self, state: DebateState, response: str) -> DebateState:
        state["verdict"] = response
        return state
        
        
    
