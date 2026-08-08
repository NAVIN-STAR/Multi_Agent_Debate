import json

from fastapi.testclient import TestClient

from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.presentation.api.app import app
from app.presentation.api.dependencies import get_workflow


def parse_sse_events(body: str) -> list[dict]:
    events = []

    for chunk in body.strip().split("\n\n"):
        if not chunk.startswith("data: "):
            continue

        payload = chunk.removeprefix("data: ")
        events.append(json.loads(payload))

    return events


def test_stream_debate(fake_llm):
    app.dependency_overrides[get_workflow] = lambda: DebateWorkflow(fake_llm)

    client = TestClient(app)

    with client.stream(
        "POST",
        "/debates/stream",
        json={
            "topic": "Science is good.",
            "max_rounds": 2,
        },
    ) as response:

        assert response.status_code == 200

        body = response.read().decode()
    app.dependency_overrides.clear()

    events = parse_sse_events(body)
    assert len(events) == 10

    assert [(event["event_type"], event["speaker"]) for event in events] == [
        ("started", "optimist"),
        ("response", "optimist"),
        ("started", "critic"),
        ("response", "critic"),
        ("started", "optimist"),
        ("response", "optimist"),
        ("started", "critic"),
        ("response", "critic"),
        ("started", "judge"),
        ("finished", "judge"),
    ]
