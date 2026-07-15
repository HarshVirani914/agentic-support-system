from langgraph.checkpoint.memory import MemorySaver
from app.agents.graph import create_agent_graph


def test_checkpointer_persists_state_across_invocations(monkeypatch):
    def fake_classifier(state):
        return {"category": "general"}

    def fake_search(state):
        return {"documents": [{"text": "doc", "score": 0.9}]}

    def fake_generate(state):
        return {"answer": "hello", "sources": state["documents"]}

    monkeypatch.setattr("app.agents.graph.classifier_node", fake_classifier)
    monkeypatch.setattr("app.agents.graph.order_search_node", fake_search)
    monkeypatch.setattr("app.agents.graph.shipping_search_node", fake_search)
    monkeypatch.setattr("app.agents.graph.general_search_node", fake_search)
    def fake_grade(state):
        return {"grounded": True, "grading_reason": "test", "retry_count": 0}

    monkeypatch.setattr("app.agents.graph.generate_node", fake_generate)
    monkeypatch.setattr("app.agents.graph.grade_node", fake_grade)

    graph = create_agent_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "test-thread"}}

    initial_state = {
        "question": "hi",
        "limit": 3,
        "category": "",
        "documents": [],
        "answer": "",
        "sources": [],
        "messages": [],
    }
    graph.invoke(initial_state, config=config)

    saved = graph.get_state(config)
    assert saved.values["answer"] == "hello"
