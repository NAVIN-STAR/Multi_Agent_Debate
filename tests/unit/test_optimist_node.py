import pytest

from app.core.domain.models.models import Speaker


@pytest.mark.asyncio
async def test_optimist_node(optimist_node,initial_state_factory):
    state=initial_state_factory.create(
        current_speaker=Speaker.OPTIMIST
    )
    assert state["turn_context"].round_number == 1
    assert len(state["turn_context"].history) == 0
    result = await optimist_node.execute(state)

    assert len(result["turn_context"].history) == 1
    assert result["turn_context"].history[0].speaker == Speaker.OPTIMIST
    assert result["turn_context"].history[0].content == "fake response"
    assert result["turn_context"].round_number == 1
    assert result['current_speaker']==Speaker.CRITIC
    assert result["verdict"] is None