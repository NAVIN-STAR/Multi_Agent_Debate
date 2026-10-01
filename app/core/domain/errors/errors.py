class LLMError(Exception):
    """Base class for LLM related errors."""

    def __init__(self, message: str, provider: str, is_transient: bool):
        self.message = message
        self.provider = provider
        self.is_transient = is_transient
        super().__init__(
            f"[{self.provider}] (Transient: {self.is_transient}) - {self.message}"
        )


class LLMRateLimitError(LLMError):
    def __init__(self, provider: str, retry_after_seconds: float | None = None):
        self.retry_after_seconds = retry_after_seconds
        if retry_after_seconds:
            msg = f"Rate limit exceeded. Retry after {retry_after_seconds}s."
        else:
            msg = "Rate limit exceeded. Please wait before retrying."
        super().__init__(message=msg, provider=provider, is_transient=True)


class LLMServiceUnavailableError(LLMError):
    """Error raised when the LLM fails to generate text."""

    def __init__(self, message: str, provider: str):
        super().__init__(message=message, provider=provider, is_transient=True)


class LLMAuthenticationError(LLMError):
    def __init__(self, message: str, provider: str):
        super().__init__(message=message, provider=provider, is_transient=False)
