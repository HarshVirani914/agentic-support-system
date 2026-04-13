from app.core.vectorstore import vector_store
from app.core.llm import llm


def query_rag(question: str, limit: int = 3) -> dict:
    """Query the RAG system."""
    
    # Retrieve relevant documents
    results = vector_store.search(question, limit=limit)
    
    if not results:
        return {
            "answer": "I don't have enough information to answer that question.",
            "sources": []
        }
    
    # Format context from retrieved documents
    context = "\n\n".join([
        f"Document {i+1}:\n{doc['text']}"
        for i, doc in enumerate(results)
    ])
    
    # Create prompt
    prompt = f"""You are a helpful customer support assistant. Answer the question based on the context provided.

Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer based on the context. If the context doesn't contain relevant information, say so."""
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    return {
        "answer": response.content,
        "sources": [
            {
                "text": doc["text"],
                "score": doc["score"]
            }
            for doc in results
        ]
    }
