import pytest


@pytest.mark.asyncio
async def test_graph_builds_successfully(debate_graph):
    assert debate_graph is not None


@pytest.mark.asyncio
async def test_graph_executes_complete_debate(debate_graph,initial_state_factory):
    state=initial_state_factory.create()
    result = await debate_graph.ainvoke(state)
    assert result["verdict"] == "fake response"
    assert len(result["turn_context"].history) == 5
    