import pytest

from app.core.adapters.OllamaAdapter import OllamaAdapter


@pytest.mark.asyncio
async def test_generate_returns_text():

    adapter = OllamaAdapter()

    response = await adapter.generate(
        "Explain why Python is popular."
    )

    assert isinstance(response, str)
    assert len(response) > 0
