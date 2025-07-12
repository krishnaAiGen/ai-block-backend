#!/usr/bin/env python3
"""
Test script to verify OpenAI embeddings work correctly
"""

import sys
import os

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

def test_openai_embeddings():
    """Test OpenAI embedding functionality"""
    try:
        from source.config import settings
        from source.embedding.embeddings_openai import OpenAIEmbeddingManager
        from source.data import SCHEMA_CHUNKS
        
        print("🧪 Testing OpenAI Embeddings...")
        print(f"📊 Using model: {settings.OPENAI_EMBEDDING_MODEL}")
        print(f"🔑 API Key configured: {'✅' if settings.OPENAI_API_KEY else '❌'}")
        
        # Initialize embedding manager
        print("\n📦 Initializing OpenAI Embedding Manager...")
        manager = OpenAIEmbeddingManager()
        
        # Add chunks
        print(f"📝 Adding {len(SCHEMA_CHUNKS)} schema chunks...")
        manager.add_chunks(SCHEMA_CHUNKS[:3])  # Test with first 3 chunks only
        
        # Get stats
        stats = manager.get_collection_stats()
        print(f"📊 Collection stats: {stats}")
        
        # Test search
        print("\n🔍 Testing semantic search...")
        test_queries = [
            "How to find recent transfers?",
            "What is an account?",
            "How to filter by amount?"
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            results = manager.search_similar(query, n_results=2)
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['id']} (distance: {result['distance']:.4f})")
        
        print("\n✅ OpenAI embeddings test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openai_embeddings() 