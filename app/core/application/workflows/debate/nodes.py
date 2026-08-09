from app.core.application.workflows.debate.base_node import BaseNode
from app.core.domain.models.models import DebateState, Speaker, TurnContext


class OptimistNode(BaseNode):

    def update_state(self, state: DebateState, updated_context:TurnContext,) -> DebateState:
        return {
            "turn_context": updated_context,
            "max_rounds": state["max_rounds"],
            "current_speaker": Speaker.CRITIC,
            "verdict": state["verdict"],
        }



class CriticNode(BaseNode):
    def update_state(self, state: DebateState, updated_context: TurnContext,) -> DebateState:
        next_round=updated_context.round_number+1

        updated_context=TurnContext(
            topic=updated_context.topic,
            history=updated_context.history,
            round_number=next_round,
        )
        next_speaker = (
            Speaker.JUDGE if next_round > state["max_rounds"] else Speaker.OPTIMIST
        )
        return {
            "turn_context": updated_context,
            "max_rounds": state["max_rounds"],
            "current_speaker": next_speaker,
            "verdict": state["verdict"],
        }


class JudgeNode(BaseNode):

    def update_state(self, state: DebateState, updated_context: TurnContext,) -> DebateState:
        return {
            "turn_context": updated_context,
            "max_rounds": state["max_rounds"],
            "current_speaker": Speaker.JUDGE,
            "verdict": updated_context.history[-1].content,
        }
    



        
        
    
