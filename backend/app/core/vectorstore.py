from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings
from app.core.embeddings import embedding_model


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.COLLECTION_NAME
    
    def create_collection(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)
        
        if not collection_exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=embedding_model.dimension,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created collection: {self.collection_name}")
        else:
            print(f"✅ Collection already exists: {self.collection_name}")
    
    def upsert_documents(self, documents: list[dict]):
        """Insert or update documents in the collection."""
        points = []
        for idx, doc in enumerate(documents):
            embedding = embedding_model.embed_text(doc["text"])
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "text": doc["text"],
                    "metadata": doc.get("metadata", {})
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"✅ Upserted {len(points)} documents")
    
    def search(self, query: str, limit: int = 5):
        """Search for similar documents."""
        query_embedding = embedding_model.embed_text(query)
        
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        )
        
        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": hit.payload.get("metadata", {})
            }
            for hit in results.points
        ]


vector_store = VectorStore()
