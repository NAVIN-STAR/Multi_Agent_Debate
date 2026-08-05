import pytest

from app.core.application.dto.debate_event import DebateEventType
from app.core.application.dto.debate_models import DebateRequest
from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.core.domain.models.models import Speaker


@pytest.mark.asyncio
async def test_stream_workflow(fake_llm):
    workflow = DebateWorkflow(fake_llm)
    request = DebateRequest(
        topic="Science is good.",
        max_rounds=2,
    )

    # Collect streaming events
    events = [event async for event in workflow.stream(request)]

    # 1. Verify total event count
    assert len(events) == 10

    # 2. Verify sequence of event types and active speakers
    expected_flow = [
        (DebateEventType.STARTED, Speaker.OPTIMIST),
        (DebateEventType.RESPONSE, Speaker.OPTIMIST),
        (DebateEventType.STARTED, Speaker.CRITIC),
        (DebateEventType.RESPONSE, Speaker.CRITIC),
        (DebateEventType.STARTED, Speaker.OPTIMIST),
        (DebateEventType.RESPONSE, Speaker.OPTIMIST),
        (DebateEventType.STARTED, Speaker.CRITIC),
        (DebateEventType.RESPONSE, Speaker.CRITIC),
        (DebateEventType.STARTED, Speaker.JUDGE),
        (DebateEventType.FINISHED, Speaker.JUDGE),
    ]
    actual_flow = [(event.event_type, event.speaker) for event in events]
    assert actual_flow == expected_flow

    # 3. Verify event payload content based on event type
    for event in events:
        if event.event_type == DebateEventType.STARTED:
            assert event.content == ""
        else:
            assert event.content == "fake response"

    # 4. Verify round progression across stream events
    expected_rounds = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3]
    actual_rounds = [event.round_number for event in events]
    assert actual_rounds == expected_rounds