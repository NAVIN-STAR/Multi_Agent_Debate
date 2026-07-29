import pytest

from app.core.adapters.OllamaAdapter import OllamaAdapter
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.turn_context import TurnContext


@pytest.mark.asyncio
async def test_optimist_take_turn_integration():
    # 1. Arrange: Use a real adapter
    real_llm = OllamaAdapter()
    agent = Optimist(llm=real_llm)
    context = TurnContext(topic="Space Exploration")

    # 2. Act: Run the full debate turn
    response = await agent.take_turn(context)

    # 3. Assert: Verify the LLM successfully processed the template and returned a response
    assert isinstance(response, str)
    assert len(response) > 0
