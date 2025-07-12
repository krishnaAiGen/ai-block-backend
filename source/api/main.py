"""
FastAPI application for AI Block Backend
Provides semantic search and GraphQL query generation for Kusama blockchain data
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import requests
import json
import logging
import os
from source.embedding import EmbeddingManager
from source.agents import GraphQLQueryAgent, ResponseAgent
from source.data import SCHEMA_CHUNKS
from source.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Global variables
embedding_manager = None
query_agent = None
response_agent = None

class QueryRequest(BaseModel):
    query: str
    max_chunks: Optional[int] = settings.DEFAULT_MAX_CHUNKS

class QueryResponse(BaseModel):
    answer: str
    graphql_query: str
    raw_data: Optional[Dict[str, Any]] = None
    relevant_chunks: Optional[list] = None

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global embedding_manager, query_agent, response_agent
    
    try:
        # Validate environment first
        from source.utils import validate_environment
        validation = validate_environment()
        
        if not validation["valid"]:
            logger.error("Environment validation failed:")
            for error in validation["errors"]:
                logger.error(f"  - {error}")
            raise RuntimeError("Environment validation failed")
        
        if validation["warnings"]:
            for warning in validation["warnings"]:
                logger.warning(f"  - {warning}")
        
        # Initialize embedding manager and add chunks
        logger.info("Initializing embedding manager...")
        embedding_manager = EmbeddingManager()
        embedding_manager.add_chunks(SCHEMA_CHUNKS)
        
        # Initialize agents
        logger.info("Initializing AI agents...")
        query_agent = GraphQLQueryAgent()
        response_agent = ResponseAgent()
        
        logger.info("Startup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Block Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from source.utils import validate_environment, get_system_info
        
        stats = embedding_manager.get_collection_stats() if embedding_manager else {"error": "Not initialized"}
        validation = validate_environment()
        system_info = get_system_info()
        
        return {
            "status": "healthy" if validation["valid"] else "unhealthy",
            "embedding_manager": stats,
            "agents": {
                "query_agent": "ready" if query_agent else "not initialized",
                "response_agent": "ready" if response_agent else "not initialized"
            },
            "environment": validation,
            "system": system_info
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/answer", response_model=QueryResponse)
async def answer_query(request: QueryRequest):
    """
    Main endpoint that accepts a query, performs semantic search,
    generates GraphQL query, executes it, and returns natural language response
    """
    try:
        if not all([embedding_manager, query_agent, response_agent]):
            raise HTTPException(status_code=500, detail="Services not initialized")
        
        logger.info(f"Processing query: {request.query}")
        
        # Step 1: Semantic search for relevant chunks
        relevant_chunks = embedding_manager.search_similar(
            request.query, 
            n_results=request.max_chunks
        )
        
        if not relevant_chunks:
            raise HTTPException(status_code=404, detail="No relevant schema chunks found")
        
        # Step 2: Generate GraphQL query
        graphql_query = query_agent.generate_query(
            request.query,
            relevant_chunks,
            settings.GRAPHQL_ENDPOINT
        )
        
        # Step 3: Execute GraphQL query
        graphql_data = await execute_graphql_query(graphql_query)
        
        # Step 4: Generate natural language response
        natural_response = response_agent.generate_response(
            request.query,
            graphql_data,
            relevant_chunks
        )
        
        return QueryResponse(
            answer=natural_response,
            graphql_query=graphql_query,
            raw_data=graphql_data,
            relevant_chunks=[
                                 {
                     "id": chunk["id"],
                     "content": chunk["content"][:settings.MAX_CHUNK_CONTENT_LENGTH] + "..." if len(chunk["content"]) > settings.MAX_CHUNK_CONTENT_LENGTH else chunk["content"],
                     "metadata": chunk.get("metadata", {})
                 }
                for chunk in relevant_chunks
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def execute_graphql_query(query: str) -> Dict[str, Any]:
    """Execute GraphQL query against the endpoint"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "query": query
        }
        
        response = requests.post(
            settings.GRAPHQL_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=settings.GRAPHQL_TIMEOUT
        )
        
        response.raise_for_status()
        
        data = response.json()
        
        if "errors" in data:
            logger.error(f"GraphQL errors: {data['errors']}")
            return {"errors": data["errors"]}
        
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error executing GraphQL query: {e}")
        raise HTTPException(status_code=500, detail=f"GraphQL query failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in GraphQL execution: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/search-chunks")
async def search_chunks(request: QueryRequest):
    """Endpoint to search for relevant schema chunks"""
    try:
        if not embedding_manager:
            raise HTTPException(status_code=500, detail="Embedding manager not initialized")
        
        chunks = embedding_manager.search_similar(
            request.query,
            n_results=request.max_chunks
        )
        
        return {
            "query": request.query,
            "chunks": chunks
        }
        
    except Exception as e:
        logger.error(f"Error searching chunks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-query")
async def generate_query(request: QueryRequest):
    """Endpoint to generate GraphQL query from natural language"""
    try:
        if not all([embedding_manager, query_agent]):
            raise HTTPException(status_code=500, detail="Services not initialized")
        
        # Get relevant chunks
        relevant_chunks = embedding_manager.search_similar(
            request.query,
            n_results=request.max_chunks
        )
        
        if not relevant_chunks:
            raise HTTPException(status_code=404, detail="No relevant schema chunks found")
        
        # Generate query
        graphql_query = query_agent.generate_query(
            request.query,
            relevant_chunks,
            settings.GRAPHQL_ENDPOINT
        )
        
        return {
            "query": request.query,
            "graphql_query": graphql_query,
            "relevant_chunks": relevant_chunks
        }
        
    except Exception as e:
        logger.error(f"Error generating query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = {
            "total_chunks": len(SCHEMA_CHUNKS),
            "embedding_manager": embedding_manager.get_collection_stats() if embedding_manager else None,
            "graphql_endpoint": settings.GRAPHQL_ENDPOINT
        }
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Entry point moved to root main.py 