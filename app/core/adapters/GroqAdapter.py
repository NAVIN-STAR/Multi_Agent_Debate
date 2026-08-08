import os

from dotenv import load_dotenv
from groq import AsyncGroq

from app.core.domain.ports.llm_port import LLMPort

load_dotenv()


class GroqAdapter(LLMPort):
    """Adapter for generating text through the Groq API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        # Falls back to .env values if parameters aren't explicitly passed
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("GROQ_MODEL",'qwen/qwen3.6-27b')
        self.base_url = base_url or os.getenv("GROQ_BASE_URL")

        if not self.api_key:
            raise ValueError("Groq API key must be provided or set in environment variables.")

        # Initialize the official AsyncGroq client
        self.client = AsyncGroq(
            api_key=self.api_key,
            base_url=self.base_url if self.base_url else None,
        )

    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Failed to generate text from Groq: {e}")