from langchain_core.messages import BaseMessage

MAX_RECENT_TURNS = 6


def _render(messages: list[BaseMessage]) -> list[str]:
    return [
        f"{'User' if message.type == 'human' else 'Assistant'}: {message.content}"
        for message in messages
    ]


def format_history(messages: list[BaseMessage], max_recent_turns: int = MAX_RECENT_TURNS) -> str:
    """
    Format conversation history into a plain-text transcript for prompts.

    Always keeps the first exchange (the user's original issue) plus the most recent
    `max_recent_turns` exchanges, so a long back-and-forth doesn't push the original
    complaint out of the window before the user asks the assistant to recall it.
    """
    if not messages:
        return ""

    first_turn = messages[:2]
    recent_turn_messages = max_recent_turns * 2
    recent = messages[-recent_turn_messages:]

    if len(messages) <= recent_turn_messages:
        return "\n".join(_render(messages))

    lines = _render(first_turn)
    lines.append("[...earlier messages omitted...]")
    lines.extend(_render(recent))
    return "\n".join(lines)
