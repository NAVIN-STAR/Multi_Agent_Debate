

from app.core.domain.models.models import DebateState, Speaker


def route(state: DebateState) -> Speaker:
    return state["current_speaker"]
    