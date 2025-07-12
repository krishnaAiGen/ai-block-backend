"""
Embeddings and ChromaDB operations for semantic search
"""

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, collection_name: str = None, chroma_db_path: str = None, embedding_model: str = None):
        """Initialize ChromaDB client and collection"""
        from source.config import settings
        
        self.collection_name = collection_name or settings.COLLECTION_NAME
        self.chroma_db_path = chroma_db_path or settings.CHROMA_DB_PATH
        self.embedding_model = embedding_model or settings.EMBEDDING_MODEL
        
        self.client = chromadb.PersistentClient(path=self.chroma_db_path)
        
        # Initialize sentence transformer for embeddings
        self.sentence_transformer = SentenceTransformer(self.embedding_model)
        
        # Create embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """Add schema chunks to ChromaDB collection"""
        try:
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                # Combine content with examples and keywords for better search
                content = chunk['content']
                if 'metadata' in chunk:
                    metadata = chunk['metadata']
                    if 'examples' in metadata:
                        content += f" Examples: {' '.join(metadata['examples'])}"
                    if 'keywords' in metadata:
                        content += f" Keywords: {' '.join(metadata['keywords'])}"
                
                documents.append(content)
                metadatas.append(chunk.get('metadata', {}))
                ids.append(chunk['id'])
            
            # Check if collection is empty or update existing
            existing_count = self.collection.count()
            if existing_count == 0:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Added {len(chunks)} chunks to collection")
            else:
                logger.info(f"Collection already has {existing_count} items")
                
        except Exception as e:
            logger.error(f"Error adding chunks to collection: {e}")
            raise
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks based on query"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    chunk_data = {
                        'id': results['ids'][0][i],
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    }
                    formatted_results.append(chunk_data)
            
            logger.info(f"Found {len(formatted_results)} similar chunks for query: {query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {e}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_chunks": count,
                "status": "ready" if count > 0 else "empty"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)} 