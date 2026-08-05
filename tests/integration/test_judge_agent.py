import pytest

from app.core.adapters.GroqAdapter import GroqAdapter
from app.core.adapters.OllamaAdapter import OllamaAdapter
from app.core.domain.agents.judge import Judge
from app.core.domain.models.models import TurnContext


@pytest.mark.asyncio
async def test_judge_take_turn_integration_ollama():
    # 1. Arrange: Use a real adapter
    real_llm = OllamaAdapter()
    agent = Judge(llm=real_llm)
    context = TurnContext(topic="Space Exploration")

    # 2. Act: Run the full debate turn
    response = await agent.take_turn(context)

    # 3. Assert: Verify the LLM successfully processed the template and returned a response
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_judge_take_turn_integration_groq():
    # 1. Arrange: Use a real adapter
    real_llm = GroqAdapter()
    agent = Judge(llm=real_llm)
    context = TurnContext(topic="Space Exploration")

    # 2. Act: Run the full debate turn
    response = await agent.take_turn(context)

    # 3. Assert: Verify the LLM successfully processed the template and returned a response
    assert isinstance(response, str)
    assert len(response) > 0
