
from fastapi.testclient import TestClient

from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.presentation.api.app import app
from app.presentation.api.dependencies import get_workflow


def test_debate_api(fake_llm):
    app.dependency_overrides[get_workflow] = (lambda: DebateWorkflow(fake_llm))

    client = TestClient(app)

    response = client.post(
        "/debates", json={"topic": "Science is good", "max_rounds": 2}
    )
    assert response.status_code == 200

    data = response.json()

    assert data["topic"] == "Science is good"
    assert data["verdict"] == "fake response"
    assert len(data["history"]) == 5

    assert [message["speaker"] for message in data["history"]] == [
        "optimist",
        "critic",
        "optimist",
        "critic",
        "judge",
    ]
    app.dependency_overrides.clear()

def test_debate_uses_default_max_rounds(fake_llm):
    app.dependency_overrides[get_workflow] = (
        lambda: DebateWorkflow(fake_llm)
    )

    client = TestClient(app)

    response = client.post(
        "/debates/",
        json={
            "topic": "Science is good.",
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["history"]) == 5
    app.dependency_overrides.clear()

def test_debate_requires_topic(fake_llm):
    app.dependency_overrides[get_workflow] = (lambda: DebateWorkflow(fake_llm))
    client = TestClient(app)

    response = client.post(
        "/debates/",
        json={
            "max_rounds": 2,
        },
    )

    assert response.status_code == 422
    app.dependency_overrides.clear()


def test_debate_rejects_empty_topic(fake_llm):
    app.dependency_overrides[get_workflow] = (lambda: DebateWorkflow(fake_llm))
    client = TestClient(app)
    response = client.post(
        "/debates",
        json={
            "topic": "",
            "max_rounds": 2,
        },
    )

    assert response.status_code == 422
    app.dependency_overrides.clear()

def test_debate_rejects_blank_topic(fake_llm):
    app.dependency_overrides[get_workflow] = (lambda: DebateWorkflow(fake_llm))
    client = TestClient(app)
    response = client.post(
        "/debates",
        json={
            "topic": "   ",
            "max_rounds": 2,
        },
    )

    assert response.status_code == 422
    app.dependency_overrides.clear()


def test_debate_rejects_invalid_rounds(fake_llm):
    app.dependency_overrides[get_workflow] = (lambda: DebateWorkflow(fake_llm))
    client = TestClient(app)
    response = client.post(
        "/debates",
        json={
            "topic": "Science is good.",
            "max_rounds": 0,
        },
    )

    assert response.status_code == 422
    app.dependency_overrides.clear()