import pytest

from app.core.application.workflows.debate.graph import DebateGraph
from app.core.application.workflows.debate.nodes import (
    CriticNode,
    JudgeNode,
    OptimistNode,
)
from app.core.domain.agents.critic import Critic
from app.core.domain.agents.judge import Judge
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.models import TurnContext
from app.core.domain.ports.llm_port import LLMPort
from tests.buliders.debate_state_factory import DebateStateFactory


class FakeLLM(LLMPort):
    async def generate(self, prompt: str) -> str:
        return "fake response"


@pytest.fixture
def fake_llm():
    return FakeLLM()


@pytest.fixture
def turn_context():
    return TurnContext(topic="Science is good.")


@pytest.fixture
def initial_state_factory():
    return DebateStateFactory


##Optimist
@pytest.fixture
def optimist_agent(fake_llm):
    return Optimist(fake_llm)


@pytest.fixture
def optimist_node(optimist_agent):
    return OptimistNode(optimist_agent)

#----------------------------------------------------------#


##Critic
@pytest.fixture
def critic_agent(fake_llm):
    return Critic(fake_llm)


@pytest.fixture
def critic_node(critic_agent):
    return CriticNode(critic_agent)

#----------------------------------------------------------#


##juge
@pytest.fixture
def judge_agent(fake_llm):
    return Judge(fake_llm)


@pytest.fixture
def judge_node(judge_agent):
    return JudgeNode(judge_agent)

#----------------------------------------------------------#


##DebateGraph

@pytest.fixture
def debate_graph(optimist_node,critic_node,judge_node):
    return DebateGraph(optimist_node= optimist_node,
        critic_node=critic_node,
        judge_node= judge_node,).build()


