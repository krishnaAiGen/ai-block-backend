"""
Alternative embedding implementation using OpenAI embeddings
Use this if sentence-transformers has dependency issues
"""

import chromadb
import openai
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OpenAIEmbeddingManager:
    def __init__(self, collection_name: str = None, chroma_db_path: str = None):
        """Initialize ChromaDB client with OpenAI embeddings"""
        from source.config import settings
        
        self.collection_name = collection_name or settings.COLLECTION_NAME
        self.chroma_db_path = chroma_db_path or settings.CHROMA_DB_PATH
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        self.client = chromadb.PersistentClient(path=self.chroma_db_path)
        
        # Create custom embedding function for OpenAI
        self.embedding_function = self._create_openai_embedding_function()
        
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
    
    def _create_openai_embedding_function(self):
        """Create OpenAI embedding function for ChromaDB"""
        from source.config import settings
        
        class OpenAIEmbeddingFunction:
            def __init__(self, client, embedding_model):
                self.client = client
                self.embedding_model = embedding_model
            
            def __call__(self, input: List[str]) -> List[List[float]]:
                """Generate embeddings using OpenAI API"""
                try:
                    response = self.client.embeddings.create(
                        model=self.embedding_model,
                        input=input
                    )
                    return [data.embedding for data in response.data]
                except Exception as e:
                    logger.error(f"Error generating OpenAI embeddings: {e}")
                    raise
        
        return OpenAIEmbeddingFunction(self.openai_client, settings.OPENAI_EMBEDDING_MODEL)
    
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """Add schema chunks to ChromaDB collection"""
        try:
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                # Combine content with examples and keywords for better search
                content = chunk['content']
                processed_metadata = {}
                
                if 'metadata' in chunk:
                    metadata = chunk['metadata']
                    if 'examples' in metadata:
                        content += f" Examples: {' '.join(metadata['examples'])}"
                    if 'keywords' in metadata:
                        content += f" Keywords: {' '.join(metadata['keywords'])}"
                    
                    # Convert metadata to ChromaDB-compatible format (only str, int, float, bool)
                    for key, value in metadata.items():
                        if isinstance(value, list):
                            # Convert lists to comma-separated strings
                            processed_metadata[key] = ', '.join(map(str, value))
                        elif isinstance(value, (str, int, float, bool)):
                            processed_metadata[key] = value
                        else:
                            # Convert other types to string
                            processed_metadata[key] = str(value)
                
                documents.append(content)
                metadatas.append(processed_metadata)
                ids.append(chunk['id'])
            
            # Check if collection is empty or update existing
            existing_count = self.collection.count()
            if existing_count == 0:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Added {len(chunks)} chunks to collection using OpenAI embeddings")
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
            from source.config import settings
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_chunks": count,
                "status": "ready" if count > 0 else "empty",
                "embedding_model": f"OpenAI {settings.OPENAI_EMBEDDING_MODEL}"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)} 