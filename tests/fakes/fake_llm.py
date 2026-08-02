
from app.core.domain.ports.llm_port import LLMPort


class FakeLLM(LLMPort):
    async def generate(self, prompt: str) -> str:
        return "fake response"