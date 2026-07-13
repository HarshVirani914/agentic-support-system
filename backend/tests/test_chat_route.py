from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_passes_thread_id_to_agent(monkeypatch):
    captured = {}

    def fake_run_agent(question, limit=3, thread_id="default"):
        captured["thread_id"] = thread_id
        return {"answer": "hi", "sources": [], "category": "general"}

    monkeypatch.setattr("app.api.routes.chat.run_agent", fake_run_agent)

    response = client.post(
        "/api/chat", json={"message": "hello", "thread_id": "abc-123"}
    )

    assert response.status_code == 200
    assert captured["thread_id"] == "abc-123"


def test_delete_thread_clears_checkpoint(monkeypatch):
    deleted = {}

    def fake_delete_thread(thread_id):
        deleted["thread_id"] = thread_id

    monkeypatch.setattr("app.api.routes.chat._checkpointer.delete_thread", fake_delete_thread)

    response = client.delete("/api/chat/abc-123")

    assert response.status_code == 204
    assert deleted["thread_id"] == "abc-123"


def test_delete_thread_empty_thread_id_returns_400():
    response = client.delete("/api/chat/%20")

    assert response.status_code == 400
    assert "Thread ID cannot be empty" in response.json()["message"]


def test_chat_response_includes_grounding_fields(monkeypatch):
    def fake_run_agent(question, limit=3, thread_id="default"):
        return {
            "answer": "hi",
            "sources": [],
            "category": "general",
            "retry_count": 1,
            "grounded": True,
            "grading_reason": "matches source",
        }

    monkeypatch.setattr("app.api.routes.chat.run_agent", fake_run_agent)

    response = client.post("/api/chat", json={"message": "hello"})
    body = response.json()

    assert body["retry_count"] == 1
    assert body["grounded"] is True
    assert body["grading_reason"] == "matches source"
