from langgraph.checkpoint.memory import MemorySaver
from app.agents.graph import create_agent_graph
import app.agents.graph as graph_module


def _wire_fake_graph(monkeypatch, seen_histories):
    def fake_classifier(state):
        seen_histories.append(("classifier", list(state.get("messages", []))))
        return {"category": "general"}

    def fake_search(state):
        return {"documents": [{"text": "doc", "score": 0.9}]}

    def fake_generate(state):
        seen_histories.append(("generate", list(state.get("messages", []))))
        return {"answer": f"answer to: {state['question']}", "sources": state["documents"]}

    def fake_grade(state):
        return {"grounded": True, "grading_reason": "test", "retry_count": 0}

    monkeypatch.setattr("app.agents.graph.classifier_node", fake_classifier)
    monkeypatch.setattr("app.agents.graph.order_search_node", fake_search)
    monkeypatch.setattr("app.agents.graph.shipping_search_node", fake_search)
    monkeypatch.setattr("app.agents.graph.general_search_node", fake_search)
    monkeypatch.setattr("app.agents.graph.generate_node", fake_generate)
    monkeypatch.setattr("app.agents.graph.grade_node", fake_grade)

    test_graph = create_agent_graph(checkpointer=MemorySaver())
    monkeypatch.setattr(graph_module, "agent_graph", test_graph)
    return test_graph


def test_run_agent_appends_turn_to_message_history(monkeypatch):
    seen_histories = []
    _wire_fake_graph(monkeypatch, seen_histories)

    graph_module.run_agent("first question", thread_id="history-thread")

    config = {"configurable": {"thread_id": "history-thread"}}
    saved = graph_module.agent_graph.get_state(config)

    messages = saved.values["messages"]
    assert len(messages) == 2
    assert messages[0].content == "first question"
    assert messages[1].content == "answer to: first question"


def test_run_agent_passes_prior_turn_to_second_call(monkeypatch):
    seen_histories = []
    _wire_fake_graph(monkeypatch, seen_histories)

    graph_module.run_agent("first question", thread_id="history-thread-2")
    seen_histories.clear()

    graph_module.run_agent("follow-up question", thread_id="history-thread-2")

    classifier_history = next(h for name, h in seen_histories if name == "classifier")
    assert len(classifier_history) == 2
    assert classifier_history[0].content == "first question"
    assert classifier_history[1].content == "answer to: first question"


def test_run_agent_keeps_threads_independent(monkeypatch):
    seen_histories = []
    _wire_fake_graph(monkeypatch, seen_histories)

    graph_module.run_agent("thread a question", thread_id="thread-a")
    graph_module.run_agent("thread b question", thread_id="thread-b")

    config_a = {"configurable": {"thread_id": "thread-a"}}
    config_b = {"configurable": {"thread_id": "thread-b"}}

    messages_a = graph_module.agent_graph.get_state(config_a).values["messages"]
    messages_b = graph_module.agent_graph.get_state(config_b).values["messages"]

    assert messages_a[0].content == "thread a question"
    assert messages_b[0].content == "thread b question"
