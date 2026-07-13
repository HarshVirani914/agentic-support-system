from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    SparseVectorParams,
    PointStruct,
    Prefetch,
    FusionQuery,
    Fusion,
)
from app.config import settings
from app.core.embeddings import embedding_model, sparse_embedding_model


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.COLLECTION_NAME

    def create_collection(self) -> None:
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)

        if not collection_exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=embedding_model.dimension, distance=Distance.COSINE
                    )
                },
                sparse_vectors_config={"sparse": SparseVectorParams()},
            )
            print(f"✅ Created collection: {self.collection_name}")
        else:
            print(f"✅ Collection already exists: {self.collection_name}")

    def upsert_documents(self, documents: list[dict]) -> None:
        """Insert or update documents in the collection."""
        texts = [doc["text"] for doc in documents]
        dense_vectors = embedding_model.embed_texts(texts)
        sparse_vectors = sparse_embedding_model.embed_texts(texts)

        points = [
            PointStruct(
                id=idx,
                vector={"dense": dense_vectors[idx], "sparse": sparse_vectors[idx]},
                payload={
                    "text": doc["text"],
                    "metadata": doc.get("metadata", {}),
                },
            )
            for idx, doc in enumerate(documents)
        ]

        self.client.upsert(collection_name=self.collection_name, points=points)
        print(f"✅ Upserted {len(points)} documents")

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Hybrid dense + sparse search, fused with RRF."""
        dense_query = embedding_model.embed_text(query)
        sparse_query = sparse_embedding_model.embed_text(query)

        candidate_limit = max(limit * 4, 20)

        results = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(query=dense_query, using="dense", limit=candidate_limit),
                Prefetch(query=sparse_query, using="sparse", limit=candidate_limit),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
        )

        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": hit.payload.get("metadata", {}),
            }
            for hit in results.points
        ]


vector_store = VectorStore()
