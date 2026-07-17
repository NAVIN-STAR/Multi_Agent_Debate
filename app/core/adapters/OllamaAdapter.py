from app.core.domain.ports.llm_port import LLMPort
from ollama import AsyncClient


class OllamaAdapter(LLMPort):
    def __init__(self,base_url:str="http://localhost:11434",model:str ="ministral-3:8b") -> None:
        self.client=AsyncClient(host=base_url)
        self.model=model

    async def generate(self, prompt: str) -> str:
        try:
            response= await self.client.generate(prompt=prompt,model=self.model,)

            return response.get('response', '')
        except Exception as e:
            raise RuntimeError(f"Failed to generate text from Ollama: {e}")
