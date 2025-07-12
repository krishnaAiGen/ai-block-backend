"""
Embedding package for ChromaDB operations and semantic search
"""

# Use OpenAI embeddings directly as requested
from .embeddings_openai import OpenAIEmbeddingManager as EmbeddingManager

print("✅ Using OpenAI embeddings (text-embedding-ada-002)")

__all__ = ["EmbeddingManager"] 