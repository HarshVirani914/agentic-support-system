from langchain_core.messages import HumanMessage, AIMessage
from app.utils.conversation import format_history


def _turns(n: int) -> list:
    messages = []
    for i in range(n):
        messages.append(HumanMessage(content=f"question {i}"))
        messages.append(AIMessage(content=f"answer {i}"))
    return messages


def test_format_history_returns_everything_when_short():
    messages = _turns(3)
    result = format_history(messages, max_recent_turns=6)

    assert "question 0" in result
    assert "question 2" in result
    assert "[...earlier messages omitted...]" not in result


def test_format_history_keeps_first_turn_when_conversation_is_long():
    messages = _turns(10)
    result = format_history(messages, max_recent_turns=3)

    assert "question 0" in result
    assert "answer 0" in result
    assert "[...earlier messages omitted...]" in result
    assert "question 9" in result
    # A middle turn that's neither the first nor within the recent window
    # should have been dropped.
    assert "question 4" not in result


def test_format_history_returns_empty_string_for_no_messages():
    assert format_history([]) == ""
