from app.core.domain.agents.judge import Judge
from app.core.domain.agents.critic import Critic
from unittest.mock import MagicMock
from app.core.domain.agents.optimist import Optimist
from app.core.domain.models.turn_context import TurnContext
from app.core.domain.ports.llm_port import LLMPort

def test_optimist_build_prompt():
    mock_llm = MagicMock(spec=LLMPort)
    agent = Optimist(llm=mock_llm)
    context = TurnContext(topic="Quantum Computing")

    prompt = agent.build_prompt(context)


    assert "You are the Optimist agent" in prompt
    assert "Topic: Quantum Computing" in prompt


def test_critic_build_prompt():
    mock_llm = MagicMock(spec=LLMPort)
    agent = Critic(llm=mock_llm)
    context = TurnContext(topic="Quantum Computing")

    prompt = agent.build_prompt(context)


    assert "You are the Critic agent" in prompt
    assert "Topic: Quantum Computing" in prompt






def test_judge_build_prompt():
    mock_llm = MagicMock(spec=LLMPort)
    agent = Judge(llm=mock_llm)
    context = TurnContext(topic="Quantum Computing")

    prompt = agent.build_prompt(context)


    assert "You are an impartial judge" in prompt
    

