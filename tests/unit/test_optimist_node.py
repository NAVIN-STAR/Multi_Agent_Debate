import pytest


@pytest.mark.asyncio
async def test_optimist_node(optimist_node,initial_state):
    result = await optimist_node.execute(initial_state)

    assert len(result["turn_context"].history) == 1
    assert result["turn_context"].history[0].speaker == "optimist"
    assert result["turn_context"].history[0].content == "fake response"
    assert result["turn_context"].round_number == 1
    assert result["verdict"] is None