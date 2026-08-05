import pytest

from app.core.domain.models.models import Speaker


@pytest.mark.asyncio
async def test_critic_routes_to_optimist_when_rounds_remaining(critic_node,initial_state_factory):
    state = initial_state_factory.create(
        current_speaker=Speaker.CRITIC
    )
    assert len(state["turn_context"].history) == 0
    result = await critic_node.execute(state)
    turn_context=result["turn_context"]
    assert len(turn_context.history) == 1
    assert turn_context.topic == state["turn_context"].topic
    assert turn_context.history[0].speaker == "critic"
    assert turn_context.history[0].content == "fake response"
    assert turn_context.round_number == 2
    assert result['current_speaker']==Speaker.OPTIMIST
    assert result["verdict"] is None

@pytest.mark.asyncio
async def test_critic_routes_to_judge_when_last_round(critic_node,initial_state_factory):
    state=initial_state_factory.create(
        current_speaker=Speaker.CRITIC,
        round_number=2
    )
    assert len(state["turn_context"].history) == 0
    result = await critic_node.execute(state)
    turn_context=result["turn_context"]
    assert turn_context.topic == state["turn_context"].topic
    assert len(turn_context.history) == 1
    assert turn_context.history[0].speaker == "critic"
    assert turn_context.history[0].content == "fake response"
    assert turn_context.round_number == 3
    assert result['current_speaker']==Speaker.JUDGE
    assert result["verdict"] is None
