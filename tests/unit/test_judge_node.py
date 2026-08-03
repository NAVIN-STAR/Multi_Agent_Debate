import pytest

from app.core.domain.models.turn_context import Speaker


@pytest.mark.asyncio
async def test_judge_node(judge_node,initial_state_factory):
    state=initial_state_factory.create(
        current_speaker=Speaker.JUDGE,
        round_number=3
    )
    
    result = await judge_node.execute(state)
    turn_context=result['turn_context']
    assert state["turn_context"].round_number == 3
    assert len(state["turn_context"].history) == 0
    assert state['current_speaker']==Speaker.JUDGE
    assert turn_context.topic == state["turn_context"].topic
    assert len(turn_context.history) == 1
    assert turn_context.history[0].speaker == "judge"
    assert turn_context.history[0].content == "fake response"
    assert turn_context.round_number == 3
    assert result["current_speaker"] == Speaker.JUDGE
    assert result["verdict"] == "fake response"