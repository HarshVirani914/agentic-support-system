import os
from sentence_transformers import SentenceTransformer
from app.config import settings


class EmbeddingModel:
    def __init__(self):
        # Set HF_TOKEN if available (removes warning)
        if hasattr(settings, 'HF_TOKEN') and settings.HF_TOKEN:
            os.environ['HF_TOKEN'] = settings.HF_TOKEN
        
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_embedding_dimension()


embedding_model = EmbeddingModel()
