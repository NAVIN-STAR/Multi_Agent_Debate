import pytest

from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.core.domain.models.turn_context import DebateRequest

expected_speakers = [
    "optimist",
    "critic",
    "optimist",
    "critic",
    "judge",
]
@pytest.mark.asyncio
async def test_workflow_integration(fake_llm):
    workflow = DebateWorkflow(fake_llm)
    request = DebateRequest(
    topic="Science is good.",
    max_rounds=2,
)
    response = await workflow.run(request)
    assert response.topic == request.topic
    assert response.verdict == "fake response"
    assert len(response.history) == 5


    assert [message.speaker for message in response.history] == expected_speakers


    for message in response.history:
        assert message.content == "fake response"
    