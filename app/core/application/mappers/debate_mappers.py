from app.core.application.dto.debate_event import DebateEvent, DebateEventType
from app.core.application.dto.debate_models import DebateResponse
from app.core.domain.models.models import DebateState


def to_response(state: DebateState) -> DebateResponse:
    return DebateResponse(
                topic=state['turn_context'].topic,
                history=state['turn_context'].history,
                verdict=state['verdict'],
            )

def to_event(
    state: DebateState,
    event_type: DebateEventType,
) -> DebateEvent:
    last_message = state["turn_context"].history[-1]
    return DebateEvent(
    round_number=state["turn_context"].round_number,
    speaker=last_message.speaker,
    content=last_message.content,
    event_type=event_type,
)

def to_started_event(
    state: DebateState,
) -> DebateEvent:
    return DebateEvent(
        round_number=state["turn_context"].round_number,
        speaker=state["current_speaker"],
        content="",
        event_type=DebateEventType.STARTED,
    )

