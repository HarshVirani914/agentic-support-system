from app.agents.state import AgentState
from app.core.llm import llm
from app.utils.logger import logger

MAX_RETRIES = 2

LOW_CONFIDENCE_FALLBACK = (
    "I don't have enough information in our policy documents to answer this confidently — "
    "it may be specific to your account or order, which I don't have access to. Please "
    "contact our support team at support@example.com (or live chat) with your order number "
    "so a team member can look into it directly."
)


def _parse_grading_response(content: str) -> tuple[bool, str]:
    grounded = "GROUNDED: yes" in content
    reason_line = next(
        (line for line in content.splitlines() if line.startswith("REASON:")), ""
    )
    reason = reason_line.replace("REASON:", "").strip()
    return grounded, reason


def grade_node(state: AgentState) -> dict:
    question = state["question"]
    answer = state["answer"]
    documents = state.get("documents", [])
    retry_count = state.get("retry_count", 0)

    context = "\n\n".join(doc["text"] for doc in documents)
    grading_prompt = (
        f"Question: {question}\nAnswer: {answer}\nSources:\n{context}\n\n"
        "Is the answer fully supported by the sources? "
        "Respond in exactly this format:\nGROUNDED: yes|no\nREASON: <one sentence>"
    )
    response = llm.invoke(grading_prompt)
    grounded, reason = _parse_grading_response(response.content)

    logger.info(f"Grade | Grounded: {grounded} | Reason: {reason}")

    if grounded:
        return {
            "grounded": True,
            "grading_reason": reason,
            "retry_count": retry_count,
            "retries_exhausted": False,
        }

    if retry_count >= MAX_RETRIES:
        return {
            "grounded": False,
            "grading_reason": reason,
            "retry_count": retry_count,
            "retries_exhausted": True,
            "answer": LOW_CONFIDENCE_FALLBACK,
        }

    rewrite_prompt = (
        f"The question '{question}' was answered ungrounded because: {reason}\n"
        "Rewrite the question as a short, specific search query to retrieve better sources. "
        "Respond with only the rewritten query."
    )
    rewritten = llm.invoke(rewrite_prompt).content.strip()

    return {
        "grounded": False,
        "grading_reason": reason,
        "retry_count": retry_count + 1,
        "retries_exhausted": False,
        "question": rewritten,
    }
