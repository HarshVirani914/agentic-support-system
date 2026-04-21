"""
Enhanced Knowledge Base Update Script

Usage:
    python scripts/update_knowledge_base.py [file_path]

Examples:
    python scripts/update_knowledge_base.py                    # Uses default sample_docs.txt
    python scripts/update_knowledge_base.py data/new_kb.txt    # Uses specific file
    python scripts/update_knowledge_base.py --clear            # Clear entire KB
"""

import sys
import argparse
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
        
        # Extract category from section (if it starts with ##)
        category = "general"
        if section.startswith("##"):
            category = section.split('\n')[0].replace("##", "").strip().lower()
        
        documents.append({
            "text": section,
            "metadata": {
                "source": file_path,
                "chunk_id": idx,
                "category": category
            }
        })
    
    return documents


def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    print("🗑️  Clearing knowledge base...")
    vector_store.create_collection()
    print("✅ Knowledge base cleared!")


def update_knowledge_base(file_path: str, append: bool = False):
    """
    Update the knowledge base with documents from a file.
    
    Args:
        file_path: Path to the document file
        append: If False, replaces entire KB. If True, appends to existing KB.
    """
    print("🚀 Starting knowledge base update...")
    print(f"📄 File: {file_path}")
    print(f"📝 Mode: {'APPEND' if append else 'REPLACE'}")
    print()
    
    # Check file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    # Recreate collection (clears existing data)
    if not append:
        print("🔄 Replacing entire knowledge base...")
        vector_store.create_collection()
    else:
        print("➕ Appending to existing knowledge base...")
    
    # Load documents
    print(f"📖 Loading documents from: {file_path}")
    documents = load_documents(str(file_path))
    
    if not documents:
        print("❌ Error: No valid documents found in file")
        return False
    
    print(f"📊 Loaded {len(documents)} document chunks")
    
    # Show preview
    print("\n📄 Document Preview:")
    for i, doc in enumerate(documents[:3], 1):
        category = doc['metadata'].get('category', 'unknown')
        preview = doc['text'][:80].replace('\n', ' ')
        print(f"  {i}. [{category}] {preview}...")
    
    if len(documents) > 3:
        print(f"  ... and {len(documents) - 3} more")
    
    # Upsert to Qdrant
    print("\n⬆️  Uploading to Qdrant Cloud...")
    try:
        vector_store.upsert_documents(documents)
        print("✅ Upload successful!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False
    
    # Test search
    print("\n🔍 Testing knowledge base...")
    test_queries = [
        "What is the refund policy?",
        "How long does shipping take?",
        "How do I reset my password?"
    ]
    
    for query in test_queries:
        results = vector_store.search(query, limit=1)
        if results:
            score = results[0]['score']
            status = "✅" if score > 0.5 else "⚠️"
            print(f"  {status} '{query}' -> Score: {score:.3f}")
        else:
            print(f"  ❌ '{query}' -> No results")
    
    print("\n🎉 Knowledge base update complete!")
    print(f"📊 Total documents in KB: {len(documents)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Update the customer support knowledge base"
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="data/sample_docs.txt",
        help="Path to the document file (default: data/sample_docs.txt)"
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing KB instead of replacing"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear the entire knowledge base"
    )
    
    args = parser.parse_args()
    
    # Handle clear command
    if args.clear:
        clear_knowledge_base()
        return
    
    # Resolve file path
    file_path = Path(__file__).parent.parent / args.file
    
    # Update knowledge base
    success = update_knowledge_base(str(file_path), append=args.append)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
