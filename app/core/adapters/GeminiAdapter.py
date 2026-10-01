import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

from app.core.domain.errors.errors import (
    LLMAuthenticationError,
    LLMError,
    LLMRateLimitError,
    LLMServiceUnavailableError,
)
from app.core.domain.ports.llm_port import LLMPort

load_dotenv()
ERROR_MAP = {
    503: lambda msg: LLMServiceUnavailableError(message=msg, provider="Gemini"),
    429: lambda msg: LLMRateLimitError(provider="Gemini"),
    401: lambda msg: LLMAuthenticationError(message=msg, provider="Gemini"),
    403: lambda msg: LLMAuthenticationError(message=msg, provider="Gemini"),
}


class GeminiAdapter(LLMPort):
    """Adapter for generating text using Google Gemini API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

        if not self.api_key:
            raise ValueError(
                "Gemini API key must be provided or set in the GEMINI_API_KEY environment variable."
            )

        # Initialize the official Google GenAI Client
        self.client = genai.Client(api_key=self.api_key)

    async def generate(self, prompt: str) -> str:
        try:
            # Use the asynchronous client (client.aio)
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text or ""
        except genai_errors.APIError as e:  # noqa: BLE001
            clean_message = getattr(e, "message", str(e))
            error_factory = ERROR_MAP.get(e.code)
            if error_factory:
                raise error_factory(clean_message)
            raise LLMError(message=clean_message, provider="Gemini", is_transient=False)

        except Exception as e:
            raise LLMError(
                message=f"Network or connection failure: {e}",
                provider="Gemini",
                is_transient=True,
            )
