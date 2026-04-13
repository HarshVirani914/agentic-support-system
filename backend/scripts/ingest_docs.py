import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.vectorstore import vector_store


def load_documents(file_path: str) -> list[dict]:
    """Load and chunk documents from a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple chunking by sections (separated by double newlines)
    sections = [s.strip() for s in content.split('\n\n') if s.strip()]
    
    documents = []
    for idx, section in enumerate(sections):
        # Skip very short sections (like single # headers)
        if len(section) < 20:
            continue
        
        documents.append({
            "text": section,
            "metadata": {
                "source": file_path,
                "chunk_id": idx
            }
        })
    
    return documents


def main():
    print("🚀 Starting document ingestion...")
    
    # Create collection
    vector_store.create_collection()
    
    # Load documents
    data_dir = Path(__file__).parent.parent / "data"
    docs_file = data_dir / "sample_docs.txt"
    
    if not docs_file.exists():
        print(f"❌ File not found: {docs_file}")
        return
    
    print(f"📄 Loading documents from: {docs_file}")
    documents = load_documents(str(docs_file))
    print(f"📊 Loaded {len(documents)} document chunks")
    
    # Upsert to Qdrant
    print("⬆️  Uploading to Qdrant...")
    vector_store.upsert_documents(documents)
    
    print("\n✅ Document ingestion complete!")
    
    # Test search
    print("\n🔍 Testing search...")
    test_query = "What is the refund policy?"
    results = vector_store.search(test_query, limit=3)
    
    print(f"\nQuery: '{test_query}'")
    print(f"Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result['score']:.4f}")
        print(f"   Text: {result['text'][:100]}...")
        print()


if __name__ == "__main__":
    main()
