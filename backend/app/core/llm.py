from langchain_groq import ChatGroq
from app.config import settings


def get_llm(temperature: float = 0.0, model: str = "llama-3.3-70b-versatile"):
    """Initialize Groq LLM."""
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=model,
        temperature=temperature
    )


llm = get_llm()
