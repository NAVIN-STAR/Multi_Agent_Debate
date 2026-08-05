import pytest

from app.core.application.dto.debate_event import DebateEventType
from app.core.application.dto.debate_models import DebateRequest, DebateResponse
from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.core.domain.models.models import Speaker


@pytest.mark.asyncio
async def test_stream_workflow(fake_llm):
    workflow = DebateWorkflow(fake_llm)

    request = DebateRequest(
        topic="Science is good.",
        max_rounds=2,
    )

    events = []

    async for event in workflow.stream(request):
        events.append(event)

    assert len(events) == 10

    expected = [
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

    actual = [
        (event.event_type, event.speaker)
        for event in events
    ]

    assert actual == expected

    for event in events:
        if event.event_type == DebateEventType.STARTED:
            assert event.content == ""
        else:
            assert event.content == "fake response"

    expected_rounds = [
    1,  # STARTED Optimist
    1,  # RESPONSE Optimist

    1,  # STARTED Critic
    2,  # RESPONSE Critic

    2,  # STARTED Optimist
    2,  # RESPONSE Optimist

    2,  # STARTED Critic
    3,  # RESPONSE Critic

    3,  # STARTED Judge
    3,  # FINISHED Judge
]

    actual_rounds = [
        event.round_number
        for event in events
    ]

    assert actual_rounds == expected_rounds