import pytest

from app.core.application.dto.debate_models import DebateRequest
from app.core.application.workflows.debate.workflow import DebateWorkflow

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

    assert all(message.content == "fake response" for message in response.history)
