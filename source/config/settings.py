"""
Configuration settings for AI Block Backend
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "AI Block Backend"
    API_DESCRIPTION: str = "Semantic search and GraphQL query generation for Kusama blockchain data"
    API_VERSION: str = "1.0.0"
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_MAX_TOKENS: int = 1500
    
    # ChromaDB Settings
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "kusama_schema"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # GraphQL Settings
    GRAPHQL_ENDPOINT: str = os.getenv("GRAPHQL_ENDPOINT", "https://af34c095-7b85-4186-acc9-2691039b60f7.squids.live/kusama-indexer@v1/api/graphql")
    GRAPHQL_TIMEOUT: int = int(os.getenv("GRAPHQL_TIMEOUT", "30"))
    
    # Search Settings
    DEFAULT_MAX_CHUNKS: int = 5
    MAX_CHUNK_CONTENT_LENGTH: int = 200
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> bool:
        """Validate required settings"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not self.GRAPHQL_ENDPOINT:
            raise ValueError("GRAPHQL_ENDPOINT environment variable is required")
        
        return True

# Global settings instance
settings = Settings() 