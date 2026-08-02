import pytest

from app.core.application.workflows.debate.Nodes import OptimistNode
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.turn_context import Speaker, TurnContext
from app.core.domain.ports.llm_port import LLMPort


class FakeLLM(LLMPort):
    async def generate(self, prompt: str) -> str:
        return "fake response"

@pytest.fixture
def fake_llm():
    return FakeLLM()

@pytest.fixture
def turn_context():
    return TurnContext(
        topic="Science is good."
    )

@pytest.fixture
def initial_state(turn_context):
    return{
        "turn_context": turn_context,
        "current_speaker": Speaker.OPTIMIST,
        "max_rounds": 2,
        "verdict": None,    
    }

@pytest.fixture
def optimist_agent(fake_llm):
    return Optimist(fake_llm)


@pytest.fixture
def optimist_node(optimist_agent):
    return OptimistNode(optimist_agent)