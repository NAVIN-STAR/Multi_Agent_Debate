import asyncio

from app.core.adapters.GroqAdapter import GroqAdapter
from app.core.application.dto.debate_models import DebateRequest
from app.core.application.workflows.debate.workflow import DebateWorkflow


async def main() -> None:
    llm = GroqAdapter()
    workflow = DebateWorkflow(llm=llm, max_rounds=2)

    request = DebateRequest(topic="Should remote work be the default for software teams?")
    response = await workflow.run(request)

    print("Topic:", response.topic)
    print("History:")
    for message in response.history:
        print(f"- {message.speaker}: {message.content}")
    print("Verdict:", response.verdict)

if __name__ == "__main__":
    asyncio.run(main())