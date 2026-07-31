

from app.core.domain.models.turn_context import DebateState, Speaker


def route(state: DebateState) -> Speaker:
    return state["current_speaker"]
    